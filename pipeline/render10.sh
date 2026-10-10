#!/bin/bash
cd /home/claude/reels
python3 build7.py web1_page voices/web1_page.mp3 scripts10.json > logs10_web1.txt 2>&1
python3 build7.py web2_speed none scripts10.json > logs10_web2.txt 2>&1
echo done > logs10_done.txt
