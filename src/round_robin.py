from scheduler import Scheduler
from process import Process
from typing import List
from collections import deque

class RoundRobinScheduler(Scheduler):
    def __init__(self, time_quantum: int = 2):
        super().__init__()
        self.time_quantum = time_quantum

    def run(self) -> dict:
        self.current_time = 0
        ready_queue = deque()
        completed_processes = []
        
        while len(completed_processes) < len(self.processes):
            # Add newly arrived processes to ready queue
            for process in self.processes:
                if (process not in completed_processes and 
                    process not in ready_queue and 
                    process.arrival_time <= self.current_time):
                    ready_queue.append(process)
            
            if not ready_queue:
                self.current_time += 1
                continue
            
            # Get the next process from ready queue
            current_process = ready_queue.popleft()
            
            # If first response, record response time
            if current_process.response_time == -1:
                current_process.response_time = self.current_time - current_process.arrival_time
            
            # Calculate execution time for this quantum
            execution_time = min(self.time_quantum, current_process.remaining_time)
            
            # Execute the process for the quantum
            self.timeline.append((self.current_time, current_process.pid))
            self.current_time += execution_time
            current_process.remaining_time -= execution_time
            
            # Check for new arrivals during this quantum
            for process in self.processes:
                if (process not in completed_processes and 
                    process not in ready_queue and 
                    process != current_process and 
                    process.arrival_time <= self.current_time):
                    ready_queue.append(process)
            
            # If process is not complete, add back to ready queue
            if current_process.remaining_time > 0:
                ready_queue.append(current_process)
            else:
                current_process.completion_time = self.current_time
                completed_processes.append(current_process)
                
        return self.calculate_metrics()