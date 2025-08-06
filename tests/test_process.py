import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process

class TestProcess(unittest.TestCase):
    def setUp(self):
        self.process = Process(pid=1, arrival_time=0, burst_time=5, priority=1)

    def test_process_initialization(self):
        self.assertEqual(self.process.pid, 1)
        self.assertEqual(self.process.arrival_time, 0)
        self.assertEqual(self.process.burst_time, 5)
        self.assertEqual(self.process.priority, 1)
        self.assertEqual(self.process.remaining_time, 5)
        self.assertEqual(self.process.completion_time, 0)
        self.assertEqual(self.process.turnaround_time, 0)
        self.assertEqual(self.process.waiting_time, 0)
        self.assertEqual(self.process.response_time, -1)

    def test_process_string_representation(self):
        expected = "Process 1 (Arrival: 0, Burst: 5, Priority: 1)"
        self.assertEqual(str(self.process), expected)

if __name__ == '__main__':
    unittest.main()