import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# File path
file_path = r"C:\Users\13916\Desktop\tij_InVS.dat"

# Read data
data = pd.read_csv(file_path, delimiter=r'\s+', header=None)
data.columns = ['t', 'i', 'j']

# Ensure nodes are basic Python int type
data['i'] = data['i'].astype(int)
data['j'] = data['j'].astype(int)

# Create graph object
G = nx.Graph()

# Get minimum and maximum time
min_time = data['t'].min()
max_time = data['t'].max()

# Define total animation duration (in milliseconds)
total_duration = 10000  # 10 seconds

# Define the number of frames for the animation
num_frames = 100  # Set the number of frames for the animation

# Calculate the interval between frames to ensure total duration is 10 seconds
interval = total_duration / num_frames  # Interval in milliseconds per frame

# Create a figure and an axis for plotting
fig, ax = plt.subplots(figsize=(10, 8))

# Initialize the graph layout with a default layout for the first time
G.add_nodes_from(set(data['i']).union(set(data['j'])))  # Add all nodes initially for layout calculation
pos = nx.spring_layout(G, seed=42, k=0.5)  # Adjust `k` to make the layout less tight

# Create colormaps for nodes and edges
node_cmap = cm.get_cmap('Purples')  # Purple gradient for nodes
edge_cmap = cm.get_cmap('plasma')   # Plasma gradient for edges
norm_time = mcolors.Normalize(vmin=min_time, vmax=max_time)

# Initialization function to draw an empty graph
def init():
    ax.clear()
    nx.draw(
        G, 
        pos, 
        with_labels=True, 
        node_size=100, 
        node_color='lightblue', 
        edge_color='gray', 
        font_size=8, 
        ax=ax
    )
    ax.set_title("Temporal Network of Contacts Between Individuals", fontsize=14)
    return ax,

# Update function to add edges step by step and update the graph
def update(frame):
    global pos
    # Calculate the current time based on the frame number
    current_time = min_time + frame * (max_time - min_time) / num_frames
    next_time = min_time + (frame + 1) * (max_time - min_time) / num_frames

    # Select edges to add for the current time step
    edges_to_add = data[(data['t'] >= current_time) & (data['t'] < next_time)]

    # Add new edges to the graph
    for _, row in edges_to_add.iterrows():
        G.add_edge(int(row['i']), int(row['j']))

    # Only update layout if the graph is not empty and positions are available
    if len(G.nodes) > 0:
        pos = nx.spring_layout(G, pos=pos, seed=42, iterations=5, k=0.5)

    # Calculate node degrees and map to colors (using Purples colormap)
    node_degrees = [G.degree(node) for node in G.nodes]
    if max(node_degrees) > 0:  # Avoid division by zero
        node_colors = [node_cmap(degree / max(node_degrees)) for degree in node_degrees]
    else:
        node_colors = ['#d3d3d3'] * len(G.nodes)  # Default color for nodes with degree 0

    # Assign edge colors based on their time
    edge_colors = [edge_cmap(norm_time(data.loc[data.index == edge[-1], 't'].values[0]))
                   if edge in data.values else 'gray'
                   for edge in G.edges]

    ax.clear()
    nx.draw(
        G, 
        pos, 
        with_labels=True, 
        node_size=100, 
        node_color=node_colors,  # Use Purple gradient for nodes
        edge_color=edge_colors, 
        edge_cmap=edge_cmap, 
        font_size=8, 
        ax=ax
    )
    ax.set_title(f"Time: {int(current_time)}s to {int(next_time)}s", fontsize=14)
    return ax,

# Create the animation and assign it to a variable
ani = animation.FuncAnimation(
    fig, update, frames=num_frames, init_func=init, interval=interval, blit=False, repeat=False
)
ani.save('network_animation_high_res.mp4', writer='ffmpeg', fps=fps, dpi=300)
# Show the animation
plt.show()
