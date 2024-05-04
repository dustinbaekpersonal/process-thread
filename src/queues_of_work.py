"""With a Pool, we can split up a chunk of predefined work up front among the available CPUs. 
This is less helpful if we have dynamic workloads, though, and particularly if we have workloads that arrive over time.
For this sort of workload, we might want to use a Queue"""

"""multiprocessing.Queue objects give us nonpersistent queues 
that can send any pickleable Python objects between processes. 
They carry an overhead, as each object must be pickled to be sent 
and then unpickled in the consumer (along with some locking operations). 
This cost is not negligible. 
However, if workers are processing larger jobs, 
the communication overhead is probably acceptable."""

"""
Only one process can get an item at a time, 
as the Queue object takes care of synchronizing the accesses. 
If there’s no work in the queue, the .get() blocks until a task is available. 
When primes are found, they are put back on the definite_primes_queue for consumption by the parent process.
"""
import argparse
import math
import multiprocessing as mp
import time
import os


### Using two Queues for interprocess communication(IPC) ###
# b"" is bytes string which is interpreted as seq of bytes instead of characters
FLAG_ALL_DONE = b'WORK_FINISHED' # known as sentinel, as it guarantees termination of processing
FLAG_WORKER_FINISHED_PROCESSING = b'WORKER_FINISHED_PROCESSING'

def check_prime(possible_primes_queue, definite_primes_queue):
    """possible_primes_queue is parent process, definite_primes_queue is child process."""
    while True:
        # consumes number from queue
        n = possible_primes_queue.get()
        if n == FLAG_ALL_DONE:
            # flag that our results have all been pushed to the results queue
            definite_primes_queue.put(FLAG_WORKER_FINISHED_PROCESSING)
            break
        else:
            # if number is even, then not prime, so continue to next item
            if n % 2 == 0:
                continue
            for i in range(3, int(math.sqrt(n))+1, 2):
                if n % i == 0:
                    break
            else:
                definite_primes_queue.put(n)
                


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project Description")
    parser.add_argument(
        "nbr_workers", 
        type=int,
        choices= range(1, os.cpu_count()+1),
        help="Number of workers e.g. 1, 2, 4, 8"

    )
    args = parser.parse_args()
    primes = []
    
    manager = mp.Manager()
    possible_primes_queue = manager.Queue()
    definite_primes_queue = manager.Queue()
    
    # pool = mp.Pool(processes=args.nbr_workers)
    processes = []
    for _ in range(args.nbr_workers):
        p = mp.Process(
            target=check_prime, args=(possible_primes_queue, definite_primes_queue)
        )
        processes.append(p)
        p.start()
    
    print(processes)
    
    t1 = time.time()
    number_range = range(100_000_000, 101_000_000)
    # add jobs to the inbound work queue
    for possible_prime in number_range: 
        possible_primes_queue.put(possible_prime)

    # add poison pills to stop the remote workers
    for n in range(args.nbr_workers): 
        possible_primes_queue.put(FLAG_ALL_DONE)
    
    print(possible_primes_queue)
    print(definite_primes_queue)

    processors_indicating_they_have_finished = 0 
    while True:
        new_result = definite_primes_queue.get() # block while waiting for results 
        if new_result == FLAG_WORKER_FINISHED_PROCESSING:
            processors_indicating_they_have_finished += 1
            if processors_indicating_they_have_finished == args.nbr_workers:
                break

        else:
            primes.append(new_result)
    assert processors_indicating_they_have_finished == args.nbr_workers
    print("Took:", time.time() - t1) 
    print(len(primes), primes[:10], primes[-10:])
    
    """There is quite an overhead to using a Queue, due to the pickling and synchronization. 
    As you can see in Figure 9-14, using a Queue-less single-process solution is significantly faster than using two or more processes. 
    The reason in this case is because our workload is very light—the communication cost dominates the overall time for this task"""
    
    """Consider using a task graph for resilience. 
    Data science tasks requiring long-running queues are frequently served well by specifying pipelines of work in acyclic graphs. 
    Two strong libraries are Airflow and Luigi. 
    These are very frequently used in industrial settings and enable arbitrary task chaining, online monitoring, and flexible scaling."""