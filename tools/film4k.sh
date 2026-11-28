#!/bin/zsh
# One-Take als Stations-Dateien (Masterfile V2.85/V2.87): Desktop 3840×2160 (Real-ESRGAN 2560 → bicubic 3840), Handy 892×1440,
# all-intra (-g 1, keine B-Bilder) gegen Blockfehler beim Spulen, je Datei < 100 MB. Schnitt bildgenau an den Stationsankern.
set -e
zmodload zsh/mathfunc
cd "$(dirname "$0")/.."
IN=assets-roh/vid/WWONE-1440.mp4; OUT=site/assets/vid/rund
T=(0 4.5 9.6 13.6 16.6 20.6 24.4 28.0 30.04)
C=(-c:v libx264 -preset medium -pix_fmt yuv420p -g 1 -bf 0 -an -movflags +faststart)
for i in {1..8}; do
  a=$(( int(rint(${T[$i]} * 30)) )); b=$(( int(rint(${T[$((i+1))]} * 30)) ))
  sel="select='between(n,$a,$((b-1)))',setpts=N/30/TB"
  ffmpeg -v error -y -i $IN -vf "$sel,scale=3840:2160:flags=bicubic,unsharp=5:5:0.4" $C -crf 27 -r 30 $OUT/f$i.mp4
  ffmpeg -v error -y -i $IN -vf "$sel,crop=892:1440:834:0,unsharp=5:5:0.5" $C -crf 26 -r 30 $OUT/f$i-p.mp4
  echo "f$i frames $a-$((b-1)) $(du -h $OUT/f$i.mp4 | cut -f1) / $(du -h $OUT/f$i-p.mp4 | cut -f1)"
done
