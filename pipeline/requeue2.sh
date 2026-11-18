#!/bin/bash
cd /home/claude/reels
while kill -0 2795 2>/dev/null; do sleep 5; done
for k in reel19_imgprompt reel23_vprompt; do
  mv out/$k.mp4 out/${k}_old2.mp4
  python3 build6.py $k voices/$k.mp3 scripts8.json > logs6c_$k.txt 2>&1
done
