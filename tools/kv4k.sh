#!/bin/zsh
# Kapitel-Film 720p -> 4K (Real-ESRGAN x2plus, Masterfile V2.85) -> Desktop 4K all-intra + Handy-Hochformat 1920 px.
# Aufruf: tools/kv4k.sh KV2 kv2 40     (Quelle assets-roh/vid/KV2.mp4, Ziel site/assets/vid/sub/kv2(.mp4|-p.mp4), posm 40 %)
# Wartet, bis die GPU frei ist (nie zwei Upscales gleichzeitig).
set -e
zmodload zsh/mathfunc
cd "${0:A:h}/.."
SRC=assets-roh/vid/$1.mp4; NAME=$2; PX=$3
UP=~/Library/Caches/video-upscale; W=$UP/work/wurzelwerk; mkdir -p $W site/assets/vid/sub
while pgrep -f upscale_vid.py >/dev/null; do sleep 60; done
ffmpeg -v error -y -i $SRC -vf fps=30 -c:v libx264 -crf 12 -pix_fmt yuv420p -an $W/$1-30.mp4
$UP/venv/bin/python $UP/upscale_vid.py --gewichte $UP/RealESRGAN_x2plus.pth --in $W/$1-30.mp4 --out $W/$1-4k.mp4 --breite 3840
# Desktop: 4K, nachgeschärft, all-intra (Scroll-Spulen ohne Blockfehler)
ffmpeg -v error -y -i $W/$1-4k.mp4 -vf "unsharp=5:5:0.4" -c:v libx264 -crf 27 -g 1 -bf 0 -pix_fmt yuv420p -an -movflags +faststart site/assets/vid/sub/$NAME.mp4
# Handy: Hochformat-Ausschnitt 888x1920 an derselben Stelle wie data-posm
CW=$(( int((3413 - 888) * PX / 100.0) ))
ffmpeg -v error -y -i $W/$1-4k.mp4 -vf "scale=3413:1920:flags=bicubic,crop=888:1920:$CW:0,unsharp=5:5:0.5" -c:v libx264 -crf 26 -g 1 -bf 0 -pix_fmt yuv420p -an -movflags +faststart site/assets/vid/sub/$NAME-p.mp4
ls -la site/assets/vid/sub/$NAME*.mp4
echo FERTIG $NAME
