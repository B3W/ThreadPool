'''
Module providing functionality similar to multiprocessing.ThreadPool
'''
import queue
import threading


class ThreadPool(object):
    @staticmethod
    def __terminator():
        pass

    @staticmethod
    def __worker(task_queue):
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
        self.task_queue = queue.Queue(num_threads)  # Tracks tasks

        # Create threads for thread pool
        for i in range(num_threads):
            thread = threading.Thread(target=self.__worker,
                                      args=(self.task_queue,))
            thread.start()

            self.threads.append(thread)

    def add_task(self, func, *args, **kwargs):
        '''
        Adds task to task queue. Blocks until queue slot is available.
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
