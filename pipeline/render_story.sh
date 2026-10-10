#!/bin/bash
cd /home/claude/reels
for k in st_notebook st_turboscribe st_suno st_gamma st_napkin st_perplexity; do
  python3 build7.py $k none scripts_story.json > logs_$k.txt 2>&1
done
echo done > logs_story_done.txt
