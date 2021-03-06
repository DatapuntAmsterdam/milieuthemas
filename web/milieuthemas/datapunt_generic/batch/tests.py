from django.test import TestCase, SimpleTestCase
from django.utils import timezone
from unittest import skip

from . import models
from . import batch


class EmptyJob(object):
    name = "empty"

    def tasks(self):
        return []


class SimpleJob(object):
    def __init__(self, name, *tasks):
        self.name = name
        self._tasks = tasks

    def tasks(self):
        return self._tasks


class JobTest(TestCase):
    def test_job_results_in_execution(self):
        e = batch.execute(EmptyJob())

        self.assertIsNotNone(e)
        self.assertIsNotNone(e.date_started)
        self.assertEqual(e.name, "empty")

    def test_successful_job_results_in_successful_execution(self):
        e = batch.execute(EmptyJob())

        self.assertIsNotNone(e.date_finished)
        self.assertEqual(e.status, models.JobExecution.STATUS_FINISHED)

    def test_job_keeps_track_of_task_executions(self):
        def noop():
            pass

        e = batch.execute(SimpleJob("simple", noop, noop))
        self.assertEqual(e.status, models.JobExecution.STATUS_FINISHED)
        self.assertIsNotNone(e.task_executions)

        t = e.task_executions.all()
        self.assertEqual(len(t), 2)
        self.assertEqual(t[0].status, models.TaskExecution.STATUS_FINISHED)
        self.assertEqual(t[1].status, models.TaskExecution.STATUS_FINISHED)

    def test_task_results_in_execution(self):
        class Task(object):
            def __init__(self):
                self.executed = False
                self.torn_down = False

            def execute(self):
                self.executed = True

            def tear_down(self):
                self.torn_down = True

        t = Task()

        batch.execute(SimpleJob("simple", t))
        self.assertEqual(t.executed, True)
        self.assertEqual(t.torn_down, True)


class DurationTestCase(SimpleTestCase):
    def test_duration(self):
        cases = [
            ((12, 0, 0), (12, 0, 7), "7s"),
            ((12, 0, 59), (12, 1, 8), "9s"),
            ((12, 0, 0), (12, 10, 4), "10m 4s"),
            ((12, 0, 0), (20, 4, 12), "8h 4m 12s"),
        ]

        for start, end, expected in cases:
            startdate = timezone.datetime(2000, 1, 1, start[0], start[1], start[2])
            enddate = timezone.datetime(2000, 1, 1, end[0], end[1], end[2])
            d = models._duration(startdate, enddate)
            self.assertEqual(d, expected)
