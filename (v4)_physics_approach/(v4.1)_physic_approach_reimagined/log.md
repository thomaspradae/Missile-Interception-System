# RL Interception — Change Log

### **2026-02-26 15:26:00-05:00**

- Changed action space from **2D (right, up)** to **3D polar (m_raw, c_raw, s_raw)**.
- Added `_decode_action()`:
  - `m = (m_raw+1)/2 ∈ [0,1]`
  - direction = normalize([c_raw, s_raw])
  - output `action2 = (right, up) = m * direction`, so `||action2|| ≤ 1` always.
- Updated `step()` to use `action2` for lateral accel (physics unchanged).
- Updated ProNav output:
  - ProNav still computes old 2D `u=(u_right,u_up)`
  - Added `pronav_to_polar_action(u_right,u_up)` so ProNav can run in new action space.
- Verified: **ProNav still hits ~100%** with the polar action encoding.

### **2026-02-26 16:40:00-05:00**

Stage-1 curriculum applied (short range + slower speeds + fixed az noise):

- range_min=5km, range_easy_max=10km, collision_radius=300m
- defender speed set to 1200 m/s, enemy speed clipped to [700,1100] m/s
- azimuth misalignment: uniform ±30° every episode (no mixture), elevation noise ±5°
- dynamic t_max = min(60s, 3*d0/||v_def||)

Verified Stage-1 baseline: ProNav 50/50 hits (100%), mean time-to-hit ~30.5s, no violations.
Noted: ProNav sometimes requests u_raw_mag > 1 (ideal lateral demand exceeds actuator unit-ball), while executed control stays bounded by polar decode.

### **2026-02-26 19:23:42-05:00**

We made n_substeps equal to 1

### **2026-02-26 19:55:56-05:00**

Observation normalization added (safe, toggleable wrapper):

- Implemented `NormalizeObsWrapper` with `RunningMeanStd` (online mean/variance via Welford).
- Normalizes per-feature: `obs_norm = clip((obs - mean)/sqrt(var + eps), ±clip)`; affects observations only (no changes to actions, rewards, terminations, or physics).
- Added controls to avoid “mystery drift”:
  - `enabled` flag to bypass normalization
  - `update_stats` flag + `freeze()/unfreeze()` to stop/start stat updates (fixed transform once frozen)

- Sanity checks:
  - ProNav baseline matches with/without wrapper when using identical seeds (wrapper doesn’t affect dynamics because ProNav ignores obs).



---

**FOR LATER WHEN WE'RE WORKING ON IT**  
Two practical rules so it stays non-chaotic

1. **Warmup + freeze**
  - Let it collect stats for a short warmup (say 5k–20k steps)
  - Then freeze stats so the observation transform becomes fixed.
2. **Freeze stats during evaluation**
  - Always evaluate with `update_stats=False` so your eval numbers are comparable.

Here’s exactly how I’d use it in your workflow:

```
# Training env: normalize + learn running stats initially
env_train = NormalizeObsWrapper(missile_interception_3d(), enabled=True, update_stats=True, clip=5.0)

# Warmup stats for N steps using ProNav (or random actions), then freeze
def warmup_obs_stats(env, steps=10000, seed=0):
    obs, _ = env.reset(seed=seed)
    for k in range(steps):
        a = env.unwrapped.calculate_pronav()
        obs, r, term, trunc, info = env.step(a)
        if term or trunc:
            obs, _ = env.reset(seed=seed+1)
            seed += 1

warmup_obs_stats(env_train, steps=10000, seed=0)
env_train.freeze()  # stats fixed from now on

# Eval env: same wrapper, but stats frozen (or copy stats from train env)
env_eval = NormalizeObsWrapper(missile_interception_3d(), enabled=True, update_stats=False, clip=5.0)
env_eval.rms.mean = env_train.rms.mean.copy()
env_eval.rms.var  = env_train.rms.var.copy()
env_eval.rms.count = env_train.rms.count
```

### One more “don’t get burned later” tip

When you change curriculum stage (range/speed), you have two clean options:

- **Option A:** keep the same frozen stats (more stable, but normalization becomes a bit “off” as distribution shifts)
- **Option B:** unfreeze for a short warmup at the new stage, then freeze again (keeps normalization aligned)

I’d do B, because it’s still controlled and testable.

Next move (since normalization is now locked down): run your **random-policy stumble test** on Stage-1 and check min_dist percentiles. That will tell you if PPO is searching a world where lucky near-hits actually occur.

  
---

## 2026-03-02 12:47:34-05:00
Make the elevation angles at the start (theta) both 45.0 degs.

## 2026-03-02 13:32:04-05:00
Remove timeout condition, leave enemy hit ground, defense hit ground or defense hit enemy

## 2026-03-02 13:42:53-05:00
Going to try to train first with static targets

## 2026-03-03 18:19:05-05:00
