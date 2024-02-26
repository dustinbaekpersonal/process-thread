"""Tutorial of using multiprocessing library."""
import logging
import multiprocessing as mp
import os
import time


# logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

def some_func(q):
    q.put(['hello', None, 42])
    

def f(x):
    return x**2


if __name__ == "__main__":
    
    ### 1. Queue ###
    mp.set_start_method('spawn')
    # Queue() is near clone of queue.Queue()
    q = mp.Queue()
    # args should be iterable, so (q,) not (q)
    p = mp.Process(target=some_func, args=(q,))
    p.start()
    logging.info(q.get())
    p.join()
    ################
    
    
    
    ### 2. pool ###
    with mp.Pool(processes=4) as pool:
        # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
        logging.info(pool.map(f, range(10)))
        
        # print same numbers in arbitrary order
        for i in pool.imap_unordered(f, range(10)):
            logging.info(i)
            
        # evaluate f(20) asynchronously
        res = pool.apply_async(f, (20,)) # runs in *only* one process
        logging.info(res.get(timeout=1)) # prints 400
        
        # evaluate "os.getpid()" asynchronously
        res = pool.apply_async(os.getpid, ()) # runs in *only* one process
        logging.info(res.get(timeout=1))             # prints the PID of that process

        # launching multiple evaluations asynchronously *may* use more processes
        multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
        logging.info([res.get(timeout=1) for res in multiple_results])

        # make a single worker sleep for 10 seconds
        res = pool.apply_async(time.sleep, (10,))
        try:
            logging.info(res.get(timeout=1))
        except mp.TimeoutError:
            logging.info("We lacked patience and got a multiprocessing.TimeoutError")

        logging.info("For the moment, the pool remains available for more work")

    # exiting the 'with'-block has stopped the pool
    logging.info("Now the pool is closed and no longer available")
        