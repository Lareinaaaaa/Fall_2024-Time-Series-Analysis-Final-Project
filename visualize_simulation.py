"""
Created by Jiajun Chen and Xinyue on Dec 8 2024
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load simulated data (replace this with your actual simulation)
data = np.load('example_simulation.npz')
s_T = data['s_T'][:, :, 0]  # Shape (T, N), spin states over time
T, N = s_T.shape  # T: number of time steps, N: number of spins

# Convert 1D spins into 2D grid (Lx x Ly grid)
Lx, Ly = 5, 6  # Dimensions of the grid (must satisfy Lx * Ly = N)
assert Lx * Ly == N, "Grid dimensions must match total number of spins!"
s_T_grid = s_T.reshape(T, Ly, Lx)  # Reshape spin states into 2D grid (Ly x Lx)

# Create a 2D grid
x, y = np.meshgrid(np.arange(Lx), np.arange(Ly))  # Ensure grid matches s_T_grid's shape
z = np.zeros_like(x)  # All arrows originate from z=0 (flat grid)

# Initialize the plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Initial quiver plot
quiver = ax.quiver(x, y, z, np.zeros_like(x), np.zeros_like(y), s_T_grid[0],
                   length=0.8, normalize=True, color=['red' if s > 0 else 'blue' for s in s_T_grid[0].flatten()])

ax.set_title("2D Spin Grid Dynamics", fontsize=16, fontweight='bold')
ax.set_xlabel("i (Lx)", fontsize=12)
ax.set_ylabel("j (Ly)", fontsize=12)
ax.set_zlabel("Spin Direction", fontsize=12)
ax.set_xlim(-0.5, Lx - 0.5)
ax.set_ylim(-0.5, Ly - 0.5)
ax.set_zlim(-1.5, 1.5)
ax.view_init(elev=30, azim=30)  # Initial view angle

# Update function for animation
def update(frame):
    global quiver
    quiver.remove()  # Remove the existing arrows
    w = s_T_grid[frame]  # Spin states at the current time step
    quiver = ax.quiver(x, y, z, np.zeros_like(x), np.zeros_like(y), w, 
                       length=0.8, normalize=True, color=['red' if s > 0 else 'blue' for s in w.flatten()])
    # Dynamically adjust view angle for aesthetic effect
    ax.view_init(elev=30 + (frame % 60) / 2, azim=30 + (frame % 360) / 4)
    ax.set_title(f"2D Spin Grid Dynamics (Time Step {frame})", fontsize=16)

# Create the animation
ani = FuncAnimation(fig, update, frames=min(T, 200), interval=50)  # Ensure video is 10 seconds

# Save animation as MP4
ani.save("spin_grid_dynamics_simulation_new.mp4", writer="ffmpeg", fps=20)

plt.show()
