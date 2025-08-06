from abc import ABC, abstractmethod
from typing import List
from src.process import Process

class Scheduler(ABC):
    def __init__(self):
        self.processes: List[Process] = []
        self.current_time = 0
        self.timeline = []

    def add_process(self, process: Process):
        self.processes.append(process)

    def calculate_metrics(self):
        total_turnaround = 0
        total_waiting = 0
        total_response = 0
        n = len(self.processes)

        for process in self.processes:
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            total_turnaround += process.turnaround_time
            total_waiting += process.waiting_time
            total_response += process.response_time

        return {
            'avg_turnaround_time': total_turnaround / n,
            'avg_waiting_time': total_waiting / n,
            'avg_response_time': total_response / n
        }

    @abstractmethod
    def run(self) -> dict:
        """Execute the scheduling algorithm and return metrics"""
        pass