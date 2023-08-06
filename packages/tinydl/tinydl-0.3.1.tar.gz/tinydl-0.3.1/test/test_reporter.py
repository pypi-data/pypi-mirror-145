import unittest

import torch

from tinydl.reporter import ConsoleReporter
from tinydl.metric import BinaryCrossentropy, RocAuc
from tinydl.stage import Stage


class TestConsoleReporter(unittest.TestCase):

    def test_add_single_metric(self):
        reporter = ConsoleReporter()
        reporter.add_metrics(BinaryCrossentropy())
        num_metrics = len(reporter._metrics)

        self.assertEqual(num_metrics, 1)

    def test_add_list_of_metrics(self):
        reporter = ConsoleReporter()
        reporter.add_metrics([BinaryCrossentropy(), RocAuc()])
        num_metrics = len(reporter._metrics)

        self.assertEqual(num_metrics, 2)

    def test_add_duplicate_metrics(self):
        reporter = ConsoleReporter()
        reporter.add_metrics([BinaryCrossentropy(), BinaryCrossentropy()])
        num_metrics = len(reporter._metrics)

        self.assertEqual(num_metrics, 1)

    def test_add_flush_metric(self):
        reporter = ConsoleReporter()
        reporter.add_metrics(BinaryCrossentropy())
        reporter.flush_metrics()
        num_metrics = len(reporter._metrics)

        self.assertEqual(num_metrics, 0)

    def test_add_remove_metric(self):
        reporter = ConsoleReporter()
        reporter.add_metrics(BinaryCrossentropy())
        reporter.remove_metrics(BinaryCrossentropy())
        num_metrics = len(reporter._metrics)

        self.assertEqual(num_metrics, 0)

    def test_get_calculations(self):
        reporter = ConsoleReporter()
        reporter.add_metrics(BinaryCrossentropy())
        scores = torch.rand(100)
        targets = torch.rand(100)
        reporter.calculate_metrics(
            stage=Stage.TRAIN, scores=scores, targets=targets)

        self.assertEqual(len(reporter.reports), 1)
