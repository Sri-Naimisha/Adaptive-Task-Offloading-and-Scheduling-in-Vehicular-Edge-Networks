import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")
algos = df["Algorithm"].unique()

def plot(metric, ylabel):
    plt.figure()

    for a in algos:
        sub = df[df["Algorithm"] == a].sort_values("Vehicles")
        plt.plot(sub["Vehicles"], sub[metric], marker='o', label=a)

    plt.xlabel("Number of Vehicles")
    plt.ylabel(ylabel)
    plt.title(f"{ylabel} vs Number of Vehicles")
    plt.legend()
    plt.grid()

    plt.show()

plot("Latency", "Latency")
plot("Throughput", "Throughput")
plot("RSU/Edge Utilization", "RSU/Edge Utilization")