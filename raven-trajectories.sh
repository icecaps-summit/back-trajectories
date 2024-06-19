#!/usr/bin/bash

cd /home/vonw/work/software/icecaps-summit/back-trajectories

/home/vonw/anaconda3/envs/work/bin/python create-raven-trajectories.py
/home/vonw/anaconda3/envs/work/bin/python raven-trajectory-plots.py

eval (ssh-agent -c)
ssh-add ~/.ssh/id_rsa
git add .
d=$(date -d "yesterday" -u -I)
git commit -m "Daily trajectories for ${d}"
git push
