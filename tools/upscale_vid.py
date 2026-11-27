"""Video kostenlos lokal hochskalieren mit Real-ESRGAN auf der Apple-GPU (MPS). Ergebnis 30 fps, Master crf 12.

Modelle (Gewichte von github.com/xinntao/Real-ESRGAN/releases):
  x2plus   RealESRGAN_x2plus.pth (v0.2.1)        720P -> 2560x1440, beste Gesichter/Details, ca. 3-6 s/Bild auf M2
  general  realesr-general-x4v3.pth (v0.2.5.0)    schnell, glättet Gesichter (Plastik) -> nur Notlösung
           optional --wdn realesr-general-wdn-x4v3.pth --staerke 0.5

Aufruf: <venv mit torch>/bin/python tools/upscale_vid.py --gewichte X.pth --in a.mp4 --out b.mp4 [--breite 2560]
Danach: tools/vid.sh <out-ohne-.mp4> <name> [loop]
Getestet 26.11.2026 (SERVICE POINT): x4plus über ncnn/MoltenVK 60-90 s/Bild = zu langsam.
"""
import argparse, json, subprocess, time
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F


class SRVGG(nn.Module):
    def __init__(s, feat=64, conv=32, up=4):
        super().__init__()
        L = [nn.Conv2d(3, feat, 3, 1, 1), nn.PReLU(feat)]
        for _ in range(conv):
            L += [nn.Conv2d(feat, feat, 3, 1, 1), nn.PReLU(feat)]
        L += [nn.Conv2d(feat, 3 * up * up, 3, 1, 1)]
        s.body, s.up, s.ps = nn.ModuleList(L), up, nn.PixelShuffle(up)

    def forward(s, x):
        o = x
        for m in s.body:
            o = m(o)
        return s.ps(o) + F.interpolate(x, scale_factor=s.up, mode='nearest')


class RDB(nn.Module):
    def __init__(s, nf=64, gc=32):
        super().__init__()
        s.conv1 = nn.Conv2d(nf, gc, 3, 1, 1); s.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1)
        s.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1); s.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1)
        s.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1)

    def forward(s, x):
        l = lambda t: F.leaky_relu(t, .2)
        x1 = l(s.conv1(x)); x2 = l(s.conv2(torch.cat((x, x1), 1))); x3 = l(s.conv3(torch.cat((x, x1, x2), 1)))
        x4 = l(s.conv4(torch.cat((x, x1, x2, x3), 1))); x5 = s.conv5(torch.cat((x, x1, x2, x3, x4), 1))
        return x5 * .2 + x


class RRDB(nn.Module):
    def __init__(s, nf=64):
        super().__init__()
        s.rdb1, s.rdb2, s.rdb3 = RDB(nf), RDB(nf), RDB(nf)

    def forward(s, x):
        return s.rdb3(s.rdb2(s.rdb1(x))) * .2 + x


class RRDBNetX2(nn.Module):
    def __init__(s, nf=64, nb=23):
        super().__init__()
        s.conv_first = nn.Conv2d(12, nf, 3, 1, 1)
        s.body = nn.Sequential(*[RRDB(nf) for _ in range(nb)])
        s.conv_body = nn.Conv2d(nf, nf, 3, 1, 1)
        s.conv_up1 = nn.Conv2d(nf, nf, 3, 1, 1); s.conv_up2 = nn.Conv2d(nf, nf, 3, 1, 1)
        s.conv_hr = nn.Conv2d(nf, nf, 3, 1, 1); s.conv_last = nn.Conv2d(nf, 3, 3, 1, 1)

    def forward(s, x):
        l = lambda t: F.leaky_relu(t, .2)
        f = s.conv_first(F.pixel_unshuffle(x, 2))
        f = f + s.conv_body(s.body(f))
        f = l(s.conv_up1(F.interpolate(f, scale_factor=2, mode='nearest')))
        f = l(s.conv_up2(F.interpolate(f, scale_factor=2, mode='nearest')))
        return s.conv_last(l(s.conv_hr(f)))


def load(p):
    sd = torch.load(p, map_location='cpu')
    return sd.get('params_ema', sd.get('params', sd))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gewichte', required=True); ap.add_argument('--in', dest='src', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--breite', type=int, default=2560)
    ap.add_argument('--wdn'); ap.add_argument('--staerke', type=float, default=.5)
    ap.add_argument('--bilder', type=int, default=0, help='nur die ersten N Bilder (Test)')
    a = ap.parse_args()
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                               'stream=width,height', '-of', 'json', a.src]))['streams'][0]
    w, h = info['width'], info['height']
    W = a.breite; H = round(W * h / w / 2) * 2
    sd = load(a.gewichte)
    if 'conv_first.weight' in sd:
        net = RRDBNetX2()
    else:
        net = SRVGG()
        if a.wdn:
            wd = load(a.wdn); sd = {k: a.staerke * sd[k] + (1 - a.staerke) * wd[k] for k in sd}
    net.load_state_dict(sd)
    dev = torch.device('mps')
    net = net.eval().half().to(dev)
    rd = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', a.src, '-r', '30', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                          stdout=subprocess.PIPE)
    wr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30',
                           '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-pix_fmt', 'yuv420p', a.out],
                          stdin=subprocess.PIPE)
    n, t0 = 0, time.time()
    with torch.no_grad():
        while not a.bilder or n < a.bilder:
            buf = rd.stdout.read(w * h * 3)
            if len(buf) < w * h * 3:
                break
            x = torch.from_numpy(np.frombuffer(buf, np.uint8).reshape(h, w, 3).copy()).to(dev)
            x = x.permute(2, 0, 1)[None].half() / 255
            y = net(x).float().clamp(0, 1)
            if y.shape[-1] != W:
                y = F.interpolate(y, size=(H, W), mode='bicubic', antialias=True, align_corners=False).clamp(0, 1)
            wr.stdin.write((y[0].permute(1, 2, 0) * 255 + .5).byte().cpu().numpy().tobytes())
            n += 1
            if n % 15 == 0:
                print(f'{n} Bilder, {(time.time() - t0) / n:.2f} s/Bild', flush=True)
    rd.kill(); wr.stdin.close(); wr.wait()
    print(f'fertig {a.out}: {n} Bilder {W}x{H}, {time.time() - t0:.0f} s', flush=True)


if __name__ == '__main__':
    main()
