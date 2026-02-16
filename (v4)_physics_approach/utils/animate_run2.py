import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- CONFIGURATION ---
r_len = 3.0           # Length of the stick
stretch_amt = 1.5     # The "Stretch" part of V
turn_amt = 2.0        # The "Turn" part of V

# Geometry
origin = np.array([0, 0])
point_A = np.array([r_len, 0])             # START POINT
point_B = point_A + np.array([stretch_amt, turn_amt]) # END POINT

# --- SETUP PLOT ---
fig, ax = plt.subplots(figsize=(9, 7))
ax.set_xlim(-1, 6)
ax.set_ylim(-1, 4)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.3)
ax.set_title("Decomposing Vector V: From Point A to Point B")

# --- GRAPHIC ELEMENTS ---
# 1. The Stick (Blue)
stick_line, = ax.plot([], [], 'b-', linewidth=4, label='The Stick (r)')
stick_dot, = ax.plot([], [], 'bo', markersize=10)

# 2. The Ghost of Vector V (Red Dashed) - The "Target" path
target_line, = ax.plot([point_A[0], point_B[0]], [point_A[1], point_B[1]], 
                       'r--', linewidth=2, alpha=0.4, label='Vector V (Total Movement)')

# 3. Component Arrows
stretch_arrow = ax.quiver([0], [0], [0], [0], color='green', scale=1, scale_units='xy', angles='xy', width=0.015, label='Component 1: Stretch')
turn_arrow = ax.quiver([0], [0], [0], [0], color='purple', scale=1, scale_units='xy', angles='xy', width=0.015, label='Component 2: Turn')

# 4. Text Labels (Points A and B)
# We initialize them but set visible=False until needed or just keep them
label_A = ax.text(point_A[0], point_A[1]-0.3, "Point A\n(Start)", ha='center', fontsize=10, fontweight='bold', color='blue')
label_B = ax.text(point_B[0], point_B[1]+0.2, "Point B\n(End)", ha='center', fontsize=10, fontweight='bold', color='red')

# 5. Status Text
status_text = ax.text(0.2, 3.5, "", fontsize=11, fontweight='bold', color='black', bbox=dict(facecolor='white', alpha=0.8))

ax.legend(loc='lower right')

# --- ANIMATION LOGIC ---
def init():
    stick_line.set_data([], [])
    stick_dot.set_data([], [])
    stretch_arrow.set_UVC([0], [0])
    turn_arrow.set_UVC([0], [0])
    status_text.set_text("")
    return stick_line, stick_dot, stretch_arrow, turn_arrow, status_text

def update(frame):
    # Sequence:
    # 0-30:  Stretch (Green)
    # 30-60: Turn (Purple)
    # 60-100: Hold & Compare
    
    current_pos = point_A.copy()
    
    if frame < 30:
        # PHASE 1: STRETCHING (Along the stick)
        progress = frame / 30.0
        
        # Move stick tip
        current_x = point_A[0] + (stretch_amt * progress)
        current_y = point_A[1]
        
        # Draw Arrows
        stretch_arrow.set_offsets([point_A[0], point_A[1]])
        stretch_arrow.set_UVC([stretch_amt * progress], [0])
        
        turn_arrow.set_UVC([0], [0]) # Hide purple
        
        # Draw Stick
        stick_line.set_data([0, current_x], [0, current_y])
        stick_dot.set_data([current_x], [current_y])
        
        status_text.set_text(f"STEP 1: STRETCHING\nMoving along the stick.\nDoes Angle Change? NO.")
        
    elif frame < 60:
        # PHASE 2: TURNING (Perpendicular)
        # Start where stretch ended
        start_x = point_A[0] + stretch_amt
        start_y = point_A[1]
        
        progress = (frame - 30) / 30.0
        
        # Move stick tip
        current_x = start_x
        current_y = start_y + (turn_amt * progress)
        
        # Draw Arrows
        # Green is full size now
        stretch_arrow.set_offsets([point_A[0], point_A[1]])
        stretch_arrow.set_UVC([stretch_amt], [0])
        
        # Purple starts from end of Green
        turn_arrow.set_offsets([start_x, start_y])
        turn_arrow.set_UVC([0], [turn_amt * progress])
        
        # Draw Stick
        stick_line.set_data([0, current_x], [0, current_y])
        stick_dot.set_data([current_x], [current_y])
        
        # Calc Angle
        angle_deg = np.degrees(np.arctan2(current_y, current_x))
        status_text.set_text(f"STEP 2: TURNING\nMoving sideways.\nDoes Angle Change? YES ({angle_deg:.1f}°)")

    else:
        # PHASE 3: RESULT
        # Show everything static
        stretch_arrow.set_offsets([point_A[0], point_A[1]])
        stretch_arrow.set_UVC([stretch_amt], [0])
        
        turn_arrow.set_offsets([point_A[0] + stretch_amt, point_A[1]])
        turn_arrow.set_UVC([0], [turn_amt])
        
        stick_line.set_data([0, point_B[0]], [0, point_B[1]])
        stick_dot.set_data([point_B[0]], [point_B[1]])
        
        status_text.set_text("RESULT:\nVector V = Green + Purple.\nOnly Purple caused Rotation.")

    return stick_line, stick_dot, stretch_arrow, turn_arrow, status_text

ani = animation.FuncAnimation(fig, update, frames=100, init_func=init, interval=50, blit=True)

plt.show()