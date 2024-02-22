"""Tutorial of using multiprocessing library."""
import logging
import multiprocessing as mp


logger = logging.getLogger(__name__)

def some_func(q):
    q.put(['hello', None, 42])

if __name__ == "__main__":
    mp.set_start_method('spawn')
    # Queue() is near clone of queue.Queue()
    q = mp.Queue()
    # args should be iterable, so (q,) not (q)
    p = mp.Process(target=some_func, args=(q,))
    p.start()
    print(q.get())
    p.join()
    