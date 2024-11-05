from DotDict import DotDict
from triggers import Trigger


class Role():
    def __init__(self, role: DotDict, priority: int = 999):
        self.name = role.name
        self.description = role.description
        self.tasks = self._convert_tasks(role.tasks)

    def _convert_tasks(self, tasks):
        """Converts a list of tasks, handling sublists."""
        converted_tasks = []
        for task in tasks:
            if isinstance(task, list):
                # Recursively convert sublists
                converted_tasks.append(self._convert_tasks(task))
            else:
                converted_tasks.append(Job(DotDict(task)))
        return converted_tasks

    def __repr__(self):
        return f'{self.__dict__}'


class Job():
    def __init__(self, job: DotDict):
        print(job)
        self.name = job.name
        self.description = job.description
        self.trigger = Trigger(
            job.trigger) if job.trigger is not None else None
        self.click = job.click
        self.new_screen = job.new_screen
        if job.next is not None:
            if isinstance(job.next, list):
                jobs = [Job(sub_job) for sub_job in job]
                print(jobs)
                self.next = jobs
            else:
                self.next = Job(job.next)
        else:
            self.next = None
        import os
        os.system('clear')

    def __repr__(self):
        return str(self.__dict__)
