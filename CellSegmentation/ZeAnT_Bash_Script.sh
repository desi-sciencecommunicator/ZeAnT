#!/bin/bash
#SBATCH --job-name=voluseg_gpu
#SBATCH --output=/resnick/groups/MYPATH/MYDIRECTORY/logs/%x_%j.out
#SBATCH --error=/resnick/groups/MYPATH/MYDIRECTORY/logs/%x_%j.err
#SBATCH --time=23:00:00          # 23 hours for buffer
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=180G                
#SBATCH --partition=gpu          # <-- TARGET THE GPU PARTITION
#SBATCH --gres=gpu:nvidia_l40s:1        # <-- REQUEST 1 GPU (any type)
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=MYEMAIL@caltech.edu

set -euo pipefail

# ── Temp dirs (keep your existing good practice) ───────────────────────────
export TMPDIR="/resnick/groups/MYPATH/MYDIRECTORY/tmp"
export TEMP=$TMPDIR
export TMP=$TMPDIR
mkdir -p "$TMPDIR"

# ── Logging ────────────────────────────────────────────────────────────────
echo "======================================"
echo "Job:       $SLURM_JOB_ID"
echo "Node:      $(hostname)"
echo "Started:   $(date)"
echo "======================================"

# ── Confirm GPU was allocated ───────────────────────────────────────────────
echo "--- GPU info ---"
nvidia-smi -L
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo "----------------"

# ── Activate conda (correct way in batch jobs) ─────────────────────────────
source /home/dascenci/miniconda3/etc/profile.d/conda.sh
conda activate voluseg_env

# ── Run ────────────────────────────────────────────────────────────────────
DATA_DIR="/resnick/groups/MYPATH/MYDIRECTORY/20250326_fish2"
cd "$DATA_DIR"

echo "Running voluseg on: $DATA_DIR"
python ZeAnT_Run_Voluseg.py

echo "======================================"
echo "Finished:  $(date)"
echo "======================================"
