import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process
from src.spn import SPNScheduler

class TestSPNScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = SPNScheduler()
        # Test case with 3 processes
        self.processes = [
            Process(pid=1, arrival_time=0, burst_time=6),
            Process(pid=2, arrival_time=0, burst_time=2),
            Process(pid=3, arrival_time=0, burst_time=4)
        ]
        for process in self.processes:
            self.scheduler.add_process(process)

    def test_spn_execution_order(self):
        metrics = self.scheduler.run()
        # Should execute in order: Process 2 (shortest), Process 3, Process 1 (longest)
        expected_timeline = [(0, 2), (2, 3), (6, 1)]
        self.assertEqual(self.scheduler.timeline, expected_timeline)

    def test_spn_completion_times(self):
        metrics = self.scheduler.run()
        # Process 2 completes first at t=2
        # Process 3 completes next at t=6
        # Process 1 completes last at t=12
        self.assertEqual(self.processes[0].completion_time, 12)  # Process 1
        self.assertEqual(self.processes[1].completion_time, 2)   # Process 2
        self.assertEqual(self.processes[2].completion_time, 6)   # Process 3

    def test_spn_waiting_times(self):
        metrics = self.scheduler.run()
        self.assertEqual(self.processes[0].waiting_time, 6)   # Process 1
        self.assertEqual(self.processes[1].waiting_time, 0)   # Process 2
        self.assertEqual(self.processes[2].waiting_time, 2)   # Process 3

    def test_spn_metrics(self):
        metrics = self.scheduler.run()
        self.assertAlmostEqual(metrics['avg_turnaround_time'], 6.67, places=2)
        self.assertAlmostEqual(metrics['avg_waiting_time'], 2.67, places=2)
        self.assertAlmostEqual(metrics['avg_response_time'], 2.67, places=2)

if __name__ == '__main__':
    unittest.main()