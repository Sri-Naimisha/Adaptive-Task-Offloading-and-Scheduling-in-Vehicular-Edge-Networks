import traci
import random
import math
import csv
import glob
import copy

# ---------------- SETTINGS ----------------
ALGORITHMS = ["MOBILITY", "DEADLINE", "PARTIAL", "PROPOSED"]
VEHICLE_COUNTS = [50, 100, 200, 400]
RUNS = 3

RSU_RANGE = 300

RSU_CAPACITY = 1
EDGE_CAPACITY = 2   # 🔥 balanced

MAX_QUEUE = 6       # 🔥 drop threshold


RSUS = {
    "RSU1": (500, 500),
    "RSU2": (1000, 500),
    "RSU3": (500, 1000),
    "RSU4": (1000, 1000)
}


# ---------------- HELPERS ----------------
def find_sumocfg():
    return glob.glob("*.sumocfg")[0]

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def nearest_rsu(pos):
    best, dmin = None, float("inf")
    for r, p in RSUS.items():
        d = dist(pos, p)
        if d < dmin:
            best, dmin = r, d
    return best if dmin <= RSU_RANGE else None

def generate_task():
    return {
        "compute": random.randint(4, 12),
        "deadline": random.uniform(2, 8),
        "priority": random.choice([1, 2])
    }

# 🔥 realistic latency model
def delay(task, q_len, mode):
    c = task["compute"]

    if mode == "LOCAL":
        return c * 0.9 + 1

    if mode == "RSU":
        return c * 0.6 + q_len * 3.0 + 1

    if mode == "EDGE":
        return c * 0.5 + q_len * 2.0 + 0.8

    if mode == "V2V":
        return c * 0.7 + 1

# ---------------- WORKLOAD ----------------
def generate_workload(limit):
    workload = []

    traci.start(["sumo", "-c", find_sumocfg()])

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        step_tasks = []
        vehicles = traci.vehicle.getIDList()[:limit]

        # 🔥 load increases with vehicles
        prob = min(0.5 + (limit / 500), 0.98)

        for v in vehicles:
            if random.random() < prob:
                task = generate_task()
                pos = traci.vehicle.getPosition(v)
                rsu = nearest_rsu(pos)

                step_tasks.append((task, rsu))

        workload.append(step_tasks)

    traci.close()
    return workload

# ---------------- ALGO ----------------
def run_algo(algo, workload):

    RSU_Q = {r: [] for r in RSUS}
    EDGE_Q = []

    RSU_BUSY = {r: 0 for r in RSUS}
    EDGE_BUSY = 0

    total_steps = 0
    stats = {"lat": [], "completed": 0}

    def decide(task, rsu):

        if algo == "MOBILITY":
            return "RSU" if rsu else "LOCAL"

        if algo == "DEADLINE":
            if rsu and task["deadline"] < 4:
                return "RSU"
            return "LOCAL"

        if algo == "PARTIAL":
            if rsu and task["compute"] > 8:
                return "RSU"
            elif task["compute"] > 6:
                return "V2V"
            return "LOCAL"

        # 🔥 FINAL PROPOSED (balanced + smart)
        if algo == "PROPOSED":
            if rsu:
                load = len(RSU_Q[rsu])

                # avoid congestion
                if load > 2:
                    if len(EDGE_Q) < 3:
                        return "EDGE"
                    else:
                        return "LOCAL"

                # urgent tasks
                if task["deadline"] < 3:
                    return "RSU"

                # heavy tasks
                if task["compute"] > 8:
                    return "EDGE"

                return "V2V"

        return "LOCAL"

    def process():
        nonlocal EDGE_BUSY

        # RSU
        for r in RSUS:
            q = RSU_Q[r]

            if q:
                RSU_BUSY[r] += 1

            if algo == "PROPOSED":
                q.sort(key=lambda x: (x["deadline"], x["compute"]))
            elif algo == "DEADLINE":
                q.sort(key=lambda x: x["deadline"])

            for _ in range(min(RSU_CAPACITY, len(q))):
                t = q.pop(0)
                stats["lat"].append(delay(t, len(q), "RSU"))
                stats["completed"] += 1

        # EDGE
        if EDGE_Q:
            EDGE_BUSY += 1

        for _ in range(min(EDGE_CAPACITY, len(EDGE_Q))):
            t = EDGE_Q.pop(0)
            stats["lat"].append(delay(t, len(EDGE_Q), "EDGE"))
            stats["completed"] += 1

    # simulate
    for step_tasks in workload:
        total_steps += 1

        for task, rsu in step_tasks:
            decision = decide(task, rsu)

            if decision == "LOCAL":
                stats["lat"].append(delay(task, 0, "LOCAL"))
                stats["completed"] += 1

            elif decision == "V2V":
                stats["lat"].append(delay(task, 0, "V2V"))
                stats["completed"] += 1

            elif decision == "RSU" and rsu:
                if len(RSU_Q[rsu]) < MAX_QUEUE:
                    RSU_Q[rsu].append(task)

            elif decision == "EDGE":
                if len(EDGE_Q) < MAX_QUEUE:
                    EDGE_Q.append(task)

        process()

    avg_lat = sum(stats["lat"]) / len(stats["lat"])
    throughput = stats["completed"] / total_steps

    rsu_util = sum(RSU_BUSY.values()) / (len(RSUS) * total_steps)
    edge_util = EDGE_BUSY / total_steps

    util = (rsu_util + edge_util) / 2

    return avg_lat, throughput, util

# ---------------- MAIN ----------------
def main():

    random.seed(42)

    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Vehicles","Algorithm","Latency","Throughput","RSU/Edge Utilization"])

    for v in VEHICLE_COUNTS:

        print(f"\n=== Vehicles: {v} ===")

        avg_results = {a: [0,0,0] for a in ALGORITHMS}

        for r in range(RUNS):
            print(f"Run {r+1}")

            workload = generate_workload(v)

            for algo in ALGORITHMS:
                lat, thr, util = run_algo(algo, copy.deepcopy(workload))

                avg_results[algo][0] += lat
                avg_results[algo][1] += thr
                avg_results[algo][2] += util

        for algo in ALGORITHMS:
            avg_lat = avg_results[algo][0] / RUNS
            avg_thr = avg_results[algo][1] / RUNS
            avg_util = avg_results[algo][2] / RUNS

            with open("results.csv", "a", newline="") as f:
                csv.writer(f).writerow([v, algo, avg_lat, avg_thr, avg_util])

    print("\n✅ FINAL IEEE-ready results saved.")


if __name__ == "__main__":
    main()
