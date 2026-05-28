import threading
from time import sleep

class ThreadTest:
    def __init__(self):
        self.tasks = []
        self.thread_running = True
        self.thread = threading.Thread(target=self._thread_func)
        self.thread.start()
    
    def _thread_func(self):
        while self.thread_running:
            if len(self.tasks) > 0:
                print(self.tasks)
    def increment_task(self):
        self.tasks.append(1)

new_thread_test = ThreadTest()
sleep(2)
new_thread_test.increment_task()