from process import Process
from fcfs import FCFSScheduler
from round_robin import RoundRobinScheduler
from spn import SPNScheduler
from srt import SRTScheduler

def print_metrics(algorithm_name: str, metrics: dict):
    print(f"\n{algorithm_name} Metrics:")
    print(f"Average Turnaround Time: {metrics['avg_turnaround_time']:.2f}")
    print(f"Average Waiting Time: {metrics['avg_waiting_time']:.2f}")
    print(f"Average Response Time: {metrics['avg_response_time']:.2f}")

def main():
    # Create sample processes
    processes = [
        Process(pid=1, arrival_time=0, burst_time=8),
        Process(pid=2, arrival_time=1, burst_time=4),
        Process(pid=3, arrival_time=2, burst_time=9),
        Process(pid=4, arrival_time=3, burst_time=5)
    ]

    # Test FCFS
    fcfs = FCFSScheduler()
    for p in processes:
        fcfs.add_process(Process(p.pid, p.arrival_time, p.burst_time))
    metrics = fcfs.run()
    print_metrics("First Come First Serve (FCFS)", metrics)
    print("Timeline:", fcfs.timeline)

    # Test Round Robin (quantum = 2)
    rr = RoundRobinScheduler(time_quantum=2)
    for p in processes:
        rr.add_process(Process(p.pid, p.arrival_time, p.burst_time))
    metrics = rr.run()
    print_metrics("Round Robin (RR)", metrics)
    print("Timeline:", rr.timeline)

    # Test Shortest Process Next
    spn = SPNScheduler()
    for p in processes:
        spn.add_process(Process(p.pid, p.arrival_time, p.burst_time))
    metrics = spn.run()
    print_metrics("Shortest Process Next (SPN)", metrics)
    print("Timeline:", spn.timeline)

    # Test Shortest Remaining Time
    srt = SRTScheduler()
    for p in processes:
        srt.add_process(Process(p.pid, p.arrival_time, p.burst_time))
    metrics = srt.run()
    print_metrics("Shortest Remaining Time (SRT)", metrics)
    print("Timeline:", srt.timeline)

if __name__ == "__main__":
    main()