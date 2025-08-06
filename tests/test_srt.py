import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process
from src.srt import SRTScheduler

class TestSRTScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = SRTScheduler()
        # Test case with 3 processes
        self.processes = [
            Process(pid=1, arrival_time=0, burst_time=8),
            Process(pid=2, arrival_time=1, burst_time=4),
            Process(pid=3, arrival_time=2, burst_time=2)
        ]
        for process in self.processes:
            self.scheduler.add_process(process)

    def test_srt_preemption(self):
        metrics = self.scheduler.run()
        # Process 1 starts, gets preempted by Process 2, then by Process 3
        first_entries = self.scheduler.timeline[:3]
        expected_first_entries = [(0, 1), (1, 2), (2, 3)]
        self.assertEqual(first_entries, expected_first_entries)

    def test_srt_completion_order(self):
        metrics = self.scheduler.run()
        # Process 3 (shortest) should complete first
        # Process 2 should complete second
        # Process 1 (longest) should complete last
        self.assertTrue(self.processes[2].completion_time < self.processes[1].completion_time)
        self.assertTrue(self.processes[1].completion_time < self.processes[0].completion_time)

    def test_srt_response_times(self):
        metrics = self.scheduler.run()
        self.assertEqual(self.processes[0].response_time, 0)  # Process 1 starts immediately
        self.assertEqual(self.processes[1].response_time, 0)  # Process 2 starts when it arrives
        self.assertEqual(self.processes[2].response_time, 0)  # Process 3 starts when it arrives

    def test_srt_metrics(self):
        metrics = self.scheduler.run()
        # Verify the metrics are within expected ranges
        self.assertTrue(0 <= metrics['avg_turnaround_time'] <= 14)  # Max possible turnaround
        self.assertTrue(0 <= metrics['avg_waiting_time'] <= 10)     # Max possible waiting time
        self.assertTrue(0 <= metrics['avg_response_time'] <= 2)     # Max possible response time

if __name__ == '__main__':
    unittest.main()