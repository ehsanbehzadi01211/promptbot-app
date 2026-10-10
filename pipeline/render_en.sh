#!/bin/bash
# render English shorts in order; log to logs_en.txt
cd /home/claude/reels
for k in "$@"; do
  python3 build7.py $k /home/claude/reels-media/media/$k.mp3 scripts_en.json > logs_en_$k.txt 2>&1
  echo "$k $?" >> logs_en.txt
done
echo DONE >> logs_en.txt
