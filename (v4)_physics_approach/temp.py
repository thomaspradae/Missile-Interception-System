# dump_tb_scalars.py
import os, glob, csv
from tensorboard.backend.event_processing import event_accumulator

LOGDIR = "tb_missile/PPO_1"   # adjust to your real path if needed

event_files = glob.glob(os.path.join(LOGDIR, "events.out.tfevents.*"))
assert event_files, f"No event files found in {LOGDIR}"

# pick the newest event file
event_file = max(event_files, key=os.path.getmtime)
ea = event_accumulator.EventAccumulator(event_file)
ea.Reload()

print("Tags:", ea.Tags()["scalars"])

# Dump a few common SB3 tags (add more if you want)
tags = [
    "rollout/ep_rew_mean",
    "rollout/ep_len_mean",
    "train/approx_kl",
    "train/value_loss",
    "train/entropy_loss",
]

rows = []
for tag in tags:
    if tag not in ea.Tags()["scalars"]:
        continue
    for ev in ea.Scalars(tag):
        rows.append((ev.step, tag, ev.value))

rows.sort(key=lambda x: (x[0], x[1]))

out_csv = "tb_dump.csv"
with open(out_csv, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["step", "tag", "value"])
    w.writerows(rows)

print("Wrote", out_csv)
