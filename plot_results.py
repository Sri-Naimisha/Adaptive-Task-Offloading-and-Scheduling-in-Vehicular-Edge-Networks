import pandas as pd
import matplotlib.pyplot as plt

# ---------------- MOBILITY RESULTS ----------------
df = pd.read_csv("mobility_results.csv")

vehicles = sorted(df["Vehicles"].unique())

mobility_lat = df[df["Algorithm"] == "MOBILITY"]["Latency"]
proposed_lat = df[df["Algorithm"] == "PROPOSED"]["Latency"]

mobility_util = df[df["Algorithm"] == "MOBILITY"]["RSU Utilization"]
proposed_util = df[df["Algorithm"] == "PROPOSED"]["RSU Utilization"]

# ---- Latency Graph ----
plt.figure()
plt.plot(vehicles, mobility_lat, marker='o', label="MOBILITY")
plt.plot(vehicles, proposed_lat, marker='o', label="PROPOSED")
plt.xlabel("Number of Vehicles")
plt.ylabel("Latency")
plt.title("Latency vs Number of Vehicles")
plt.legend()
plt.grid(True)
plt.savefig("latency.png")
plt.show()

# ---- RSU Utilization Graph ----
plt.figure()
plt.plot(vehicles, mobility_util, marker='o', label="MOBILITY")
plt.plot(vehicles, proposed_util, marker='o', label="PROPOSED")
plt.xlabel("Number of Vehicles")
plt.ylabel("RSU Utilization")
plt.title("RSU Utilization vs Vehicles")
plt.legend()
plt.grid(True)
plt.savefig("rsu_utilization.png")
plt.show()


# ---------------- SCHEDULING RESULTS ----------------
df_sched = pd.read_csv("scheduling_results.csv")

edf = df_sched[df_sched["Algorithm"] == "EDF"]["Avg Waiting Time"]
proposed = df_sched[df_sched["Algorithm"] == "PROPOSED_SCHED"]["Avg Waiting Time"]

# ---- Scheduling Graph ----
plt.figure()
plt.plot(vehicles, edf, marker='o', label="EDF")
plt.plot(vehicles, proposed, marker='o', label="PROPOSED")
plt.xlabel("Number of Vehicles")
plt.ylabel("Average Waiting Time")
plt.title("Scheduling Comparison (EDF vs Proposed)")
plt.legend()
plt.grid(True)
plt.savefig("scheduling.png")
plt.show()