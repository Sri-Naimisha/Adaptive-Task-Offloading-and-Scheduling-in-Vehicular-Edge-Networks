# import pandas as pd
# import matplotlib.pyplot as plt

# df = pd.read_csv("results.csv")

# def plot_metric(metric, ylabel, filename):
#     plt.figure()

#     for algo in df["Algorithm"].unique():
#         subset = df[df["Algorithm"] == algo]
#         plt.plot(subset["Vehicles"], subset[metric], marker='o', label=algo)

#     plt.xlabel("Number of Vehicles")
#     plt.ylabel(ylabel)
#     plt.title(f"{ylabel} vs Number of Vehicles")
#     plt.legend()
#     plt.grid(True)
#     plt.savefig(filename)
#     plt.show()

# plot_metric("Latency", "Latency", "latency.png")
# plot_metric("Throughput", "Throughput", "throughput.png")
# plot_metric("RSU/Edge Utilization", "RSU/Edge Utilization", "utilization.png")

# # ---------------- SCHEDULING PLOT ----------------
# df2 = pd.read_csv("scheduling_results.csv")

# plt.figure()

# for algo in df2["Algorithm"].unique():
#     subset = df2[df2["Algorithm"] == algo]
#     plt.plot(subset["Vehicles"], subset["Avg Waiting Time"], marker='o', label=algo)

# plt.xlabel("Number of Vehicles")
# plt.ylabel("Average Waiting Time")
# plt.title("Scheduling Comparison")
# plt.legend()
# plt.grid(True)
# plt.savefig("scheduling.png")
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

def plot_metric(metric, ylabel, filename):
    plt.figure()
    for algo in df["Algorithm"].unique():
        subset = df[df["Algorithm"] == algo]
        plt.plot(subset["Vehicles"], subset[metric], marker='o', label=algo)

    plt.xlabel("Number of Vehicles")
    plt.ylabel(ylabel)
    plt.title(f"{ylabel} vs Number of Vehicles")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.show()

plot_metric("Latency", "Latency", "latency.png")
plot_metric("Throughput", "Throughput", "throughput.png")
plot_metric("RSU/Edge Utilization", "RSU/Edge Utilization", "utilization.png")

# Scheduling plot
df2 = pd.read_csv("scheduling_results.csv")

plt.figure()
for algo in df2["Algorithm"].unique():
    subset = df2[df2["Algorithm"] == algo]
    plt.plot(subset["Vehicles"], subset["Avg Waiting Time"], marker='o', label=algo)

plt.xlabel("Number of Vehicles")
plt.ylabel("Average Waiting Time")
plt.title("Scheduling Comparison")
plt.legend()
plt.grid(True)
plt.savefig("scheduling.png")
plt.show()