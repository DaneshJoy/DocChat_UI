#!/bin/bash
# source /home/saeed/anaconda3/etc/profile.d/conda.sh
# conda activate deploy
uvicorn doc_store:app --host 0.0.0.0 --port 8088 --reload