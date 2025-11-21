import random
import math
import statistics
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

# -------------------------------
# Packet and Queue Simulation
# -------------------------------
class Packet:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.start_service = None
        self.departure_time = None

def simulate_queue(arrival_rate, service_time_sampler, sim_time, max_packets=int(2e6)):
    """
    Simulates a single-server FIFO queue using discrete-event simulation.
    Returns lists of total delays and queueing delays.
    """
    t = 0.0
    next_arrival = random.expovariate(arrival_rate) if arrival_rate > 0 else float('inf')
    queue = deque()
    server_busy = False
    departure_time = float('inf')
    packets_completed = []
    current_serving = None
    packet_count = 0

    while t < sim_time and packet_count < max_packets:
        if next_arrival <= departure_time and next_arrival <= sim_time:
            # ---- Arrival Event ----
            t = next_arrival
            pkt = Packet(t)
            packet_count += 1
            if not server_busy:
                # Start service immediately
                pkt.start_service = t
                service_time = service_time_sampler()
                pkt.departure_time = t + service_time
                departure_time = pkt.departure_time
                current_serving = pkt
                server_busy = True
            else:
                queue.append(pkt)
            next_arrival = t + random.expovariate(arrival_rate)
        else:
            # ---- Departure Event ----
            if departure_time > sim_time:
                break
            t = departure_time
            if current_serving is not None:
                packets_completed.append(current_serving)
            if queue:
                next_pkt = queue.popleft()
                next_pkt.start_service = t
                service_time = service_time_sampler()
                next_pkt.departure_time = t + service_time
                departure_time = next_pkt.departure_time
                current_serving = next_pkt
                server_busy = True
            else:
                server_busy = False
                departure_time = float('inf')
                current_serving = None

    # ---- Collect Results ----
    delays = []
    queueing_times = []
    for p in packets_completed:
        total_delay = p.departure_time - p.arrival_time
        q_delay = p.start_service - p.arrival_time if p.start_service else 0.0
        delays.append(total_delay)
        queueing_times.append(q_delay)
    return delays, queueing_times

# -------------------------------
# Experiment Runner
# -------------------------------
def run_experiments(packet_size_bytes=1500, bandwidth_bps=10_000_000, rho_list=None, sim_time=120.0):
    """
    Runs simulations for M/M/1 and M/D/1 queues at different utilization (rho).
    Returns results in a Pandas DataFrame.
    """
    if rho_list is None:
        rho_list = [i/20 for i in range(1, 20)]  # 0.05 .. 0.95

    L_bits = packet_size_bytes * 8
    service_rate_packets = bandwidth_bps / L_bits   # mu (pkts/s)
    service_time_mean = 1.0 / service_rate_packets  # mean transmission time

    rows = []
    for rho in rho_list:
        arrival_rate = rho * service_rate_packets   # λ = ρ * μ

        # Service samplers
        mm1_sampler = lambda: random.expovariate(1.0 / service_time_mean)  # exponential
        md1_sampler = lambda: service_time_mean                           # deterministic

        # Simulate
        delays_mm, q_mm = simulate_queue(arrival_rate, mm1_sampler, sim_time)
        delays_md, q_md = simulate_queue(arrival_rate, md1_sampler, sim_time)

        mean_total_mm = statistics.mean(delays_mm) if delays_mm else float('nan')
        mean_queue_mm = statistics.mean(q_mm) if q_mm else 0.0
        mean_total_md = statistics.mean(delays_md) if delays_md else float('nan')
        mean_queue_md = statistics.mean(q_md) if q_md else 0.0

        # Analytic M/M/1
        mu = service_rate_packets
        lam = arrival_rate
        if lam < mu:
            analytic_total = 1.0 / (mu - lam)
            analytic_queue = rho / (mu - lam)
        else:
            analytic_total = float('inf')
            analytic_queue = float('inf')

        rows.append({
            "rho": rho,
            "arrival_rate_pkts_s": arrival_rate,
            "service_rate_pkts_s": service_rate_packets,
            "tx_delay_s": service_time_mean,
            "sim_total_mm1_s": mean_total_mm,
            "sim_queue_mm1_s": mean_queue_mm,
            "sim_total_md1_s": mean_total_md,
            "sim_queue_md1_s": mean_queue_md,
            "analytic_mm1_total_s": analytic_total,
            "analytic_mm1_queue_s": analytic_queue
        })

    return pd.DataFrame(rows)

# -------------------------------
# Main Script
# -------------------------------
if __name__ == "__main__":
    random.seed(42)
    rho_values = [i/25 for i in range(1, 25)]  # 0.04 .. 0.96
    df = run_experiments(rho_list=rho_values, sim_time=100.0)

    # Show first rows
    print(df.head(10))

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(df['rho'], df['sim_total_mm1_s'], label='Simulated M/M/1')
    plt.plot(df['rho'], df['sim_total_md1_s'], label='Simulated M/D/1')
    plt.plot(df['rho'], df['analytic_mm1_total_s'], '--', label='Analytic M/M/1')
    plt.xlabel('Utilization (ρ)')
    plt.ylabel('Average Total Delay (seconds)')
    plt.title('Transmission vs Congestion Delay Analyzer')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Save results
    df.to_csv("transmission_vs_congestion.csv", index=False)
    print("Results saved to transmission_vs_congestion.csv")
