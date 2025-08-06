import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process
from src.fcfs import FCFSScheduler

class TestFCFSScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = FCFSScheduler()
        # Test case with 3 processes
        self.processes = [
            Process(pid=1, arrival_time=0, burst_time=6),
            Process(pid=2, arrival_time=2, burst_time=4),
            Process(pid=3, arrival_time=4, burst_time=2)
        ]
        for process in self.processes:
            self.scheduler.add_process(process)

    def test_fcfs_execution_order(self):
        metrics = self.scheduler.run()
        expected_timeline = [(0, 1), (6, 2), (10, 3)]
        self.assertEqual(self.scheduler.timeline, expected_timeline)

    def test_fcfs_completion_times(self):
        metrics = self.scheduler.run()
        self.assertEqual(self.processes[0].completion_time, 6)   # Process 1
        self.assertEqual(self.processes[1].completion_time, 10)  # Process 2
        self.assertEqual(self.processes[2].completion_time, 12)  # Process 3

    def test_fcfs_waiting_times(self):
        metrics = self.scheduler.run()
        self.assertEqual(self.processes[0].waiting_time, 0)   # Process 1
        self.assertEqual(self.processes[1].waiting_time, 4)   # Process 2
        self.assertEqual(self.processes[2].waiting_time, 6)   # Process 3

    def test_fcfs_metrics(self):
        metrics = self.scheduler.run()
        self.assertAlmostEqual(metrics['avg_turnaround_time'], 7.33, places=2)
        self.assertAlmostEqual(metrics['avg_waiting_time'], 3.33, places=2)
        self.assertAlmostEqual(metrics['avg_response_time'], 3.33, places=2)

if __name__ == '__main__':
    unittest.main()