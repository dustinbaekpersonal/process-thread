# Ref: https://docs.python.org/3/library/multiprocessing.html
import multiprocessing as mp

# 1. Using Pool
def f(x):
    return x*x

# 2. communication between processes: Queue
def func_queue(q):
    q.put([42, None, "hello"])
    
# 3. communication between processes: Pipe
def func_pipe(conn):
    conn.send([42, None, "hello"])
    conn.close()

# 4. synchronisation btw processes
def f_sync(l, i):
    l.acquire()
    try:
        print("Hello World!", i)
    finally:
        l.release()

# 5. sharing state between processes: shared memory
# Data can be stored in a shared memory map using Value or Array.
# when doing concurrent programming it is usually best to avoid using shared state as far as possible. 
# This is particularly true when using multiple processes.
def f_share_state(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

# 6. sharing state between processes: server process
# A manager object returned by Manager() controls a server process which holds Python objects and allows other processes to manipulate them using proxies.
# A manager returned by Manager() will support types list, dict, Namespace, Lock, RLock, Semaphore, BoundedSemaphore, Condition, Event, Barrier, Queue, Value and Array
def f_manager(d, l):
    d[1] = "1"
    d["2"] = 2
    d[0.25] = None
    l.reverse()

if __name__ == "__main__":
    # # 1.
    # with mp.Pool(5) as p:
    #     print(p.map(f, [num for num in range(10)]))
    
    # # 2.
    # q = mp.Queue()
    # p = mp.Process(target = func_queue, args=(q,))
    # p.start()
    # print(q.get())
    # p.join()
    
    # # 3.
    # parent_conn, child_conn = mp.Pipe()
    # p = mp.Process(target = func_pipe, args = (child_conn,))
    # p.start()
    # print(parent_conn.recv())
    # p.join()

    # # 4.
    # lock = mp.Lock()
    # for num in range(10):
    #     p = mp.Process(target = f_sync, args = (lock, num))
    #     p.start()
    
    # # 5.
    # # The 'd' and 'i' arguments used when creating num and arr are typecodes of the kind used by the array module: 
    # # 'd' indicates a double precision float and 'i' indicates a signed integer. 
    # # These shared objects will be process and thread-safe.
    # num = mp.Value("d", 0.0)
    # arr = mp.Array("i", range(10))
    
    # p = mp.Process(target = f_share_state, args = (num, arr))
    # p.start()
    # p.join()
    
    # print(num.value)
    # print(arr[:])
    
    # 6.
    with mp.Manager() as manager:
        d = manager.dict()
        l = manager.list(range(10))
        
        p = mp.Process(target = f_manager, args = (d, l))
        p.start()
        p.join()
        print(d, l)
    
