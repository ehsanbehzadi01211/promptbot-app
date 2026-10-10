#!/bin/bash
cd /home/claude/reels
for k in reel25_skill reel26_connector reel27_github; do
  python3 build6.py $k voices/$k.mp3 scripts9.json > logs9_$k.txt 2>&1
done
