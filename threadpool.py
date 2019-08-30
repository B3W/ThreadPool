# MIT License
#
# Copyright (c) 2019 Weston Berg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# References:
# https://docs.python.org/3/library/queue.html
# https://stackoverflow.com/a/7257510
'''
Module providing functionality similar to multiprocessing.ThreadPool
'''
import queue
import threading


class ThreadPool(object):
    @staticmethod
    def __terminator():
        '''
        Dummy function for terminating threads
        '''
        pass

    @staticmethod
    def __worker(task_queue):
        '''
        Behavior for thread to execute
        '''
        while True:
            # Get task when available
            func, args, kwargs = task_queue.get()

            # Exit condition
            if func == ThreadPool.__terminator:
                break

            try:
                # Execute function
                func(*args, **kwargs)
            except Exception as e:
                print(e)
            finally:
                # Signal to queue task is complete
                task_queue.task_done()

    def __init__(self, num_threads):
        self.threads = []  # Keeps track of threads
        self.task_queue = queue.Queue()  # Tracks tasks, unbounded

        # Create threads for thread pool
        for i in range(num_threads):
            thread = threading.Thread(target=self.__worker,
                                      args=(self.task_queue,))
            thread.start()

            self.threads.append(thread)

    def add_task(self, func, *args, **kwargs):
        '''
        Adds task to task queue
        '''
        queue_item = (func, args, kwargs)
        self.task_queue.put(queue_item)

    def wait_completion(self):
        '''
        Waits until all tasks in task queue have completed and joins threads
        '''
        self.task_queue.join()

        # Terminate threads
        for i in range(len(self.threads)):
            self.add_task(ThreadPool.__terminator)

        # Join threads
        for thread in self.threads:
            thread.join()
