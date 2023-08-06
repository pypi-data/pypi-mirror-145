import threading
import time
import datetime
from colorama import Fore


class TaskEater(threading.Thread):

    def __init__(self, name, task):
        threading.Thread.__init__(self)
        self.name = name
        self.task = task

    def run(self):
        self.timer()

    def timer(self):
        from task_app import utils
        while utils.seconds > 0:
            if not utils.ack:return
            mins, secs = divmod(utils.seconds, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            # print(timeformat)
            time.sleep(1)
            utils.seconds -= 1
        t = ChangeStatusTask(self.task)
        t.setDaemon(True)
        t.start()


class ChangeStatusTask(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self)
        self.task = task

    def run(self):
        time.sleep(1)
        self.change_status()

    def color_print(self, task, status):
        if status == 'active':
            print(Fore.YELLOW + f'Status Changed: {Fore.CYAN} {task.article} {Fore.YELLOW} -> {Fore.GREEN} '
                                f'{task.article.status} {Fore.YELLOW} at {Fore.BLUE} {datetime.datetime.now()} {Fore.RESET}')
        else:
            print(Fore.YELLOW + f'Status Changed: {Fore.CYAN} {task.article} {Fore.YELLOW} -> {Fore.RED} '
                                f'{task.article.status} {Fore.YELLOW} at {Fore.BLUE} {datetime.datetime.now()} {Fore.RESET}')

    def change_status(self):
        # change article status
        self.task.article.status = 'inactive' if self.task.article.status == 'active' else 'active'
        self.task.article.change_status_on = None
        self.task.article.save()
        self.color_print(self.task, self.task.article.status)
        # change task status
        self.task.status = 'completed'
        self.task.save()

