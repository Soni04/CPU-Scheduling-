from scheduler import Scheduler
from process import Process
from typing import List

class FCFSScheduler(Scheduler):
    def run(self) -> dict:
        # Sort processes by arrival time
        self.processes.sort(key=lambda x: x.arrival_time)
        
        self.current_time = 0
        ready_queue = []
        completed_processes = []
        
        while len(completed_processes) < len(self.processes):
            # Add newly arrived processes to ready queue
            for process in self.processes:
                if process not in completed_processes and process not in ready_queue:
                    if process.arrival_time <= self.current_time:
                        ready_queue.append(process)
            
            if not ready_queue:
                self.current_time += 1
                continue
                
            # Get the first process from ready queue
            current_process = ready_queue.pop(0)
            
            # If first response, record response time
            if current_process.response_time == -1:
                current_process.response_time = self.current_time - current_process.arrival_time
            
            # Execute the process
            self.timeline.append((self.current_time, current_process.pid))
            self.current_time += current_process.burst_time
            current_process.completion_time = self.current_time
            completed_processes.append(current_process)
            
        return self.calculate_metrics()