#!/bin/bash
cd /home/claude/reels
for k in news_claude_ws demo_gpt6 reel28s reel29s reel30s; do
  python3 build7.py $k none scripts11.json > logs11_$k.txt 2>&1
  echo "$k $?" >> logs11_done.txt
done
