'''
Testing Module
'''
import threadpool
from collections import deque
from timeit import default_timer as timer


# Function for workers to run
def f(queue, x):
    queue.append(x)


if __name__ == '__main__':
    WORKER_CNT = 10
    RUN_CNT = 10000

    # Construct thread pool with specified workers
    pool = threadpool.ThreadPool(WORKER_CNT)

    # Construct queue to store values in
    q = deque(maxlen=RUN_CNT)

    # Start feeding workers tasks
    start = timer()

    for i in range(RUN_CNT):
        pool.add_task(f, q, i)

    end = timer()

    # Wait
    pool.wait_completion()

    # Check accuracy
    for i in range(RUN_CNT):
        # Make sure all numbers made it into q
        # i.e. all tasks completed successfully
        if i not in q:
            print('%d missing from queue' % (i))
            exit(1)

    print('Tasks completed successfully!')
    print('Elapsed Task Time: %.6f' % (end - start))
