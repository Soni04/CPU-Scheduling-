from typing import List
from src.process import Process
from src.scheduler import Scheduler

class SRTScheduler(Scheduler):
    def run(self) -> dict:
        self.current_time = 0
        ready_queue = []
        completed_processes = []
        current_process = None
        time_slice = 1  # For preemptive checking
        
        while len(completed_processes) < len(self.processes):
            # Add newly arrived processes to ready queue
            for process in self.processes:
                if (process not in completed_processes and 
                    process not in ready_queue and
                    process != current_process and
                    process.arrival_time <= self.current_time):
                    ready_queue.append(process)
            
            # Sort ready queue by remaining time
            ready_queue.sort(key=lambda x: x.remaining_time)
            
            # If we have a current process, check if it should be preempted
            if current_process and ready_queue:
                if ready_queue[0].remaining_time < current_process.remaining_time:
                    ready_queue.append(current_process)
                    current_process = None
            
            if not current_process:
                if not ready_queue:
                    self.current_time += 1
                    continue
                
                current_process = ready_queue.pop(0)
                # Record response time if first time selected
                if current_process.response_time == -1:
                    current_process.response_time = self.current_time - current_process.arrival_time
            
            # Execute the process for one time slice
            self.timeline.append((self.current_time, current_process.pid))
            self.current_time += time_slice
            current_process.remaining_time -= time_slice
            
            # Check if process is complete
            if current_process.remaining_time <= 0:
                current_process.completion_time = self.current_time
                completed_processes.append(current_process)
                current_process = None
                
        return self.calculate_metrics()