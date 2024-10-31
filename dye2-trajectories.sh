#!/usr/bin/bash

cd /home/vonw/work/software/icecaps-summit/back-trajectories

/home/vonw/anaconda3/envs/work/bin/python create-dye2-trajectories.py
/home/vonw/anaconda3/envs/work/bin/python dye2-trajectory-plots.py

eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa
git add .
d=$(date -d "yesterday" -u -I)
git commit -m "Daily trajectories for ${d}"
git push
