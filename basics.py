"""Tutorial of using multiprocessing library."""
import multiprocessing as mp


def some_func(q):
    q.put('hello')
    

if __name__ == "__main__":
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=some_func, args=(q))
    p.start()
    print()
    