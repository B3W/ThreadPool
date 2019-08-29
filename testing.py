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
