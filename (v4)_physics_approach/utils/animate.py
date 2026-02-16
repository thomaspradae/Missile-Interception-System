import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- 1. AESTHETICS CONFIGURATION ---
plt.style.use('default') 

# --- 2. SIMULATION SETUP ---
# Reduced frames significantly as requested
dt = 0.1             # Larger time steps
total_time = 4.0     # Shorter duration
frames = int(total_time / dt)

# INITIAL STATE DEFINITIONS (CONSTANTS)
# We store these to reset later
R_M_START = np.array([0.0, 0.0, 0.0])
V_M_START = np.array([0.0, 0.0, 1.0]) 

R_T_START = np.array([2.0, 4.0, 1.0])
V_T_START = np.array([2.5, 0.5, 0.0]) 

# Mutable Global State
r_M_pos = R_M_START.copy()
v_M = V_M_START.copy()
r_T_pos = R_T_START.copy()
v_T = V_T_START.copy()

# History arrays
M_trail = []
T_trail = []

# --- 3. HELPER FUNCTIONS ---
def get_magnitude(vec):
    return np.sqrt(vec.dot(vec))

def get_projection(vec_a, vec_b):
    mag_b = get_magnitude(vec_b)
    if mag_b == 0: return np.zeros(3)
    return (np.dot(vec_a, vec_b) / (mag_b**2)) * vec_b

# --- 4. ANIMATION SETUP ---
fig = plt.figure(figsize=(14, 10)) 
ax = fig.add_subplot(111, projection='3d')

def update(frame):
    global r_M_pos, r_T_pos, v_M, v_T, M_trail, T_trail
    
    # --- RESET LOGIC ---
    # If we are at frame 0, snap everything back to start
    if frame == 0:
        r_M_pos = R_M_START.copy()
        r_T_pos = R_T_START.copy()
        M_trail = []
        T_trail = []
    
    # --- CAMERA PRESERVATION ---
    current_elev = ax.elev
    current_azim = ax.azim
    
    ax.clear()
    
    if current_elev is not None:
        ax.view_init(elev=current_elev, azim=current_azim)

    # --- PHYSICS ---
    # Only move if we aren't on the very first frame (to show start pos)
    if frame > 0:
        r_M_pos += v_M * dt
        r_T_pos += v_T * dt
    
    M_trail.append(r_M_pos.copy())
    T_trail.append(r_T_pos.copy())
    
    # --- CALCULATIONS ---
    r_vec = r_T_pos - r_M_pos
    dist = get_magnitude(r_vec)
    
    v_rel = v_T - v_M
    
    v_parallel = get_projection(v_rel, r_vec)
    v_perp = v_rel - v_parallel
    
    cross_prod = np.cross(r_vec, v_rel)
    if dist > 0.1:
        omega = cross_prod / (dist**2)
    else:
        omega = np.array([0,0,0])

    # --- DRAWING ---

    # 1. TRAILS
    m_hist = np.array(M_trail)
    t_hist = np.array(T_trail)
    if len(m_hist) > 1:
        ax.plot(m_hist[:,0], m_hist[:,1], m_hist[:,2], color='blue', alpha=0.2, linewidth=3)
        ax.plot(t_hist[:,0], t_hist[:,1], t_hist[:,2], color='red', alpha=0.2, linewidth=3)

    # 2. OBJECTS
    ax.scatter(*r_M_pos, color='blue', s=150, label='Interceptor')
    ax.scatter(*r_T_pos, color='red', s=150, label='Target')

    # 3. LOS
    ax.plot([r_M_pos[0], r_T_pos[0]], 
            [r_M_pos[1], r_T_pos[1]], 
            [r_M_pos[2], r_T_pos[2]], 
            color='green', linestyle='--', linewidth=3, alpha=0.6, label='LOS (r)')

    # --- QUIVER HELPER ---
    def draw_vec(start, vec, color, label, scale=1.0, lw=3):
        mag = get_magnitude(vec)
        if mag == 0: return
        direction = vec / mag
        
        ax.quiver(
            start[0], start[1], start[2],
            direction[0], direction[1], direction[2],
            color=color, label=label, 
            length=mag * scale, 
            linewidth=lw, arrow_length_ratio=0.2, normalize=True
        )

    # --- VECTORS ---
    
    # A. Absolute Velocities
    draw_vec(r_M_pos, v_M, 'darkblue', 'Abs Vel (M)', scale=1.5, lw=2)
    draw_vec(r_T_pos, v_T, 'darkred', 'Abs Vel (T)', scale=1.5, lw=2)

    # B. Relative Velocity Triangle
    draw_vec(r_T_pos, v_rel, 'teal', 'Total Rel Vel', scale=1.0, lw=3)
    draw_vec(r_T_pos, v_parallel, 'magenta', 'Parallel (Closing)', scale=1.0, lw=2)
    draw_vec(r_T_pos, v_perp, 'darkorange', 'Perpendicular (Rotation)', scale=1.0, lw=4)

    # C. Omega
    draw_vec(r_M_pos, omega, 'purple', 'Omega', scale=15.0, lw=4)

    # --- PLOT LIMITS ---
    ax.set_xlim([-2, 14])
    ax.set_ylim([-2, 8])
    ax.set_zlim([0, 8])
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Frame {frame}: Orange Arrow is the "Lever" for Rotation')
    
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left', fontsize='small')

# Create Animation (repeat=True ensures it loops)
ani = animation.FuncAnimation(fig, update, frames=frames, interval=100, repeat=True)

plt.show()