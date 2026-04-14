<<<<<<< HEAD
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- MOBILITY ----------------
df = pd.read_csv("mobility_results.csv")

vehicles = sorted(df["Vehicles"].unique())

mobility_lat = df[df["Algorithm"]=="MOBILITY"]["Latency"]
proposed_lat = df[df["Algorithm"]=="PROPOSED"]["Latency"]

mobility_util = df[df["Algorithm"]=="MOBILITY"]["RSU Utilization"]
proposed_util = df[df["Algorithm"]=="PROPOSED"]["RSU Utilization"]

# ---- Latency Graph ----
plt.figure()
plt.plot(vehicles, mobility_lat, marker='o', label="MOBILITY")
plt.plot(vehicles, proposed_lat, marker='o', label="PROPOSED")
plt.xlabel("Number of Vehicles")
plt.ylabel("Latency")
plt.title("Latency vs Number of Vehicles")
plt.legend()
plt.grid()
plt.show()

# ---- RSU Utilization ----
plt.figure()
plt.plot(vehicles, mobility_util, marker='o', label="MOBILITY")
plt.plot(vehicles, proposed_util, marker='o', label="PROPOSED")
plt.xlabel("Number of Vehicles")
plt.ylabel("RSU Utilization")
plt.title("RSU Utilization vs Vehicles")
plt.legend()
plt.grid()
plt.show()


# ---------------- SCHEDULING ----------------
df_sched = pd.read_csv("scheduling_results.csv")

edf = df_sched[df_sched["Algorithm"]=="EDF"]["Avg Waiting Time"]
proposed = df_sched[df_sched["Algorithm"]=="PROPOSED_SCHED"]["Avg Waiting Time"]

plt.figure()
plt.plot(vehicles, edf, marker='o', label="EDF")
plt.plot(vehicles, proposed, marker='o', label="PROPOSED")
plt.xlabel("Number of Vehicles")
plt.ylabel("Avg Waiting Time")
plt.title("Scheduling Comparison (EDF vs Proposed)")
plt.legend()
plt.grid()
=======
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
>>>>>>> 49708a2a2ba04cbe9f2cce6faf1c562626b071a1
plt.show()