import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

def make_zem_animation(path, r, v, t_max=6.0, fps=30, n_frames=150, title=""):
    r = np.array(r, dtype=float)
    v = np.array(v, dtype=float)
    eps = 1e-9
    
    # t* (unclipped) for closest approach of ||r + v t||
    t_star_unclipped = - float(np.dot(r, v)) / (float(np.dot(v, v)) + eps)
    t_star = float(np.clip(t_star_unclipped, 0.0, t_max))
    r_star = r + v * t_star
    
    # Pick animation end time
    t_end = min(t_max, max(1.0, 1.25 * t_star if t_star > 0 else 2.0))
    ts = np.linspace(0.0, t_end, n_frames)
    pts = r[None, :] + ts[:, None] * v[None, :]
    dists = np.linalg.norm(pts, axis=1)
    
    # Plot limits
    all_xy = np.vstack([pts, np.zeros((1,2)), r[None,:], r_star[None,:]])
    pad = 0.15 * max(1.0, np.max(np.linalg.norm(all_xy, axis=1)))
    xmin, ymin = np.min(all_xy, axis=0) - pad
    xmax, ymax = np.max(all_xy, axis=0) + pad
    
    fig, ax = plt.subplots(figsize=(6.2, 6.2))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel("x (relative)")
    ax.set_ylabel("y (relative)")
    ax.set_title(title if title else "Relative motion r(t) = r + v t, closest approach at t*")
    ax.grid(True, alpha=0.3)
    
    # Draw the relative-velocity direction line (through current point) for reference
    # We'll show a small arrow for v at the current point.
    v_norm = np.linalg.norm(v) + eps
    v_hat = v / v_norm
    
    # Static elements
    ax.plot(pts[:,0], pts[:,1], linewidth=1.5, alpha=0.5,
            label=r"path $r(t)=r+vt$ (constant relative velocity)")
    ax.scatter([0],[0], s=40)  # origin
    ax.text(0, 0, "  defense (origin)", va="center", fontsize=9)

    # Dashed: r(t*) from origin + direction of v through r(t*) — shows perpendicularity
    ax.plot([0, r_star[0]], [0, r_star[1]], linestyle="--", linewidth=1.2, alpha=0.8,
            color="C2", label=r"$r(t^*)$ (min distance)")
    L = 0.6 * max(1.0, np.max(np.linalg.norm(pts, axis=1)))
    p1 = r_star - v_hat * L
    p2 = r_star + v_hat * L
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], linestyle="--", linewidth=1.2, alpha=0.8,
            color="C3", label=r"direction of $v$")
    ax.text(0.5, 0.02, r"At closest approach: $r(t^*)\perp v$ (dot product = 0)",
            transform=ax.transAxes, fontsize=9, ha="center", va="bottom")

    # Mark closest-approach point r(t*)
    ax.scatter([r_star[0]],[r_star[1]], s=60)
    ax.text(r_star[0], r_star[1], r"  $r(t^*)$" + "\n closest approach", va="top", fontsize=9)
    
    # Lines that update (line= r(t), point= enemy, arrow= v)
    (line_rt,) = ax.plot([], [], linewidth=2.0, label=r"$r(t)$ (origin to enemy)")
    (point_rt,) = ax.plot([], [], marker="o", markersize=8, linestyle="None",
                          label=r"enemy position $r(t)$")
    (arrow_v,) = ax.plot([], [], linewidth=2.0, label=r"$v$ (relative velocity)")
    ax.legend(loc="upper right", fontsize=8)
    text_box = ax.text(
        0.02, 0.98, "", transform=ax.transAxes, va="top",
        bbox=dict(boxstyle="round", alpha=0.85)
    )
    
    # Helper to build a little arrow segment for v at point p
    def v_arrow(p, scale=0.25):
        L = scale * max(1.0, np.max(np.linalg.norm(pts, axis=1)))
        a = p
        b = p + v_hat * L
        return np.array([a, b])
    
    def init():
        line_rt.set_data([], [])
        point_rt.set_data([], [])
        arrow_v.set_data([], [])
        text_box.set_text("")
        return line_rt, point_rt, arrow_v, text_box
    
    def update(i):
        t = ts[i]
        p = pts[i]
        r_now = p
        d_now = dists[i]
        dot_now = float(np.dot(r_now, v))
        
        line_rt.set_data([0, r_now[0]], [0, r_now[1]])
        point_rt.set_data([r_now[0]], [r_now[1]])
        
        arr = v_arrow(r_now, scale=0.18)
        arrow_v.set_data(arr[:,0], arr[:,1])
        
        # Show the key facts: projection cancels at t*, so r(t*) ⟂ v
        dot_star = float(np.dot(r_star, v))
        d_star = float(np.linalg.norm(r_star))
        text_box.set_text(
            "Key idea: projection of r(t) onto v goes to zero at t*\n"
            "  ⇒ At closest approach, r(t*) has no component along v\n"
            "  ⇒ Equivalent: r(t*)·v = 0 (perpendicular)\n"
            f"t* (unclipped) = {-np.dot(r,v):.3f} / {np.dot(v,v):.3f} = {t_star_unclipped:.3f}\n"
            f"t* (clipped)   = {t_star:.3f}\n"
            f"Now: t={t:.3f}  |  |r(t)|={d_now:.3f}  |  r(t)·v={dot_now:.3f}\n"
            f"At t*: |r(t*)|={d_star:.3f}  |  r(t*)·v≈{dot_star:.3f}"
        )
        return line_rt, point_rt, arrow_v, text_box
    
    anim = FuncAnimation(fig, update, frames=n_frames, init_func=init, blit=True)

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    anim.save(str(path), writer=PillowWriter(fps=fps))
    plt.close(fig)
    return {
        "path": str(path),
        "t_star_unclipped": t_star_unclipped,
        "t_star_clipped": t_star,
        "r_star": r_star
    }

# Case 1: closing (t* > 0)
out1 = make_zem_animation(
    "viz_out/zem_closing.gif",
    r=[8.0, 5.0],
    v=[-3.2, -1.2],
    t_max=6.0,
    title=r"Closing case: $t^*>0$ and $r(t^*) \perp v$ (dot $\approx 0$)"
)

# Case 2: opening (t* < 0 so clip to 0)
out2 = make_zem_animation(
    "viz_out/zem_opening.gif",
    r=[8.0, 5.0],
    v=[+2.2, +1.1],
    t_max=6.0,
    title="Opening case: t* < 0 so we clip to 0 (closest future point is now)"
)

out1, out2