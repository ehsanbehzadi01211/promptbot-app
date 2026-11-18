#!/bin/bash
cd /home/claude/reels
python3 build7.py web1_page none scripts10.json > logs10b_web1.txt 2>&1
echo done > logs10b_done.txt
