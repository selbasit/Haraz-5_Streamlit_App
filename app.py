
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("Haraz-5_clustered_with_HCZONE_and_Sw.csv")
annotations = pd.read_csv("Zone_Annotations.csv")

# Sidebar options
st.sidebar.title("Zone Highlighter")
depth_min = float(df["DEPTH"].min())
depth_max = float(df["DEPTH"].max())
depth_range = st.sidebar.slider("Select Depth Range (m)", depth_min, depth_max, (depth_min, depth_max))

show_hc = st.sidebar.checkbox("Highlight HC Zones", value=True)
show_annotations = st.sidebar.checkbox("Show Custom Annotations", value=True)

# Filter by depth
df = df[(df["DEPTH"] >= depth_range[0]) & (df["DEPTH"] <= depth_range[1])]

# Plot setup
logs_to_plot = {
    "GR": "Gamma Ray",
    "RD": "Resistivity",
    "Porosity": "Porosity",
    "Vshale": "Vshale",
    "Sw": "Water Saturation"
}

num_logs = len(logs_to_plot)
fig, axes = plt.subplots(nrows=1, ncols=num_logs, figsize=(4 * num_logs, 10), sharey=True)

for i, (log, label) in enumerate(logs_to_plot.items()):
    ax = axes[i]
    ax.plot(df[log], df["DEPTH"], color="black", linewidth=0.8)
    ax.set_ylim(depth_range[1], depth_range[0])
    ax.set_xlabel(label)
    ax.set_title(f"{label} vs Depth")
    ax.grid(True)

    # Highlight HC zones
    if show_hc:
        for _, row in df[df["HC_ZONE"] == 1].iterrows():
            ax.axhspan(row["DEPTH"], row["DEPTH"] + 0.5, color="orange", alpha=0.3)

    # Custom Annotations
    if show_annotations:
        for _, row in annotations.iterrows():
            if row["End_Depth"] >= depth_range[0] and row["Start_Depth"] <= depth_range[1]:
                ax.axhspan(row["Start_Depth"], row["End_Depth"], color=row["Color"], alpha=0.3)
                mid_depth = (row["Start_Depth"] + row["End_Depth"]) / 2
                ax.text(0.95, mid_depth, row["Label"], transform=ax.get_yaxis_transform(),
                        fontsize=8, verticalalignment="center", horizontalalignment="right",
                        bbox=dict(boxstyle="round,pad=0.2", facecolor=row["Color"], alpha=0.4))

axes[0].set_ylabel("Depth (m)")
plt.tight_layout()
st.pyplot(fig)
