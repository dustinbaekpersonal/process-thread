"""Intro to multiprocessing library."""
import logging
import os
import random
import time
from joblib import Parallel, delayed
from typing import Callable, Optional
from multiprocessing import Pool

logging.basicConfig(level = logging.INFO)

#TODO: decorator gives error during multiprocessing
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        duration = round(end - start,6)
        logging.info(f"Time taken: {duration}")
        return duration
    return wrapper

######## Example 1. Estimating Pi using Monte Carlo Method ########
# Original approach without parallelisation
def estimate_nbr_points_in_quarter_circle(nbr_estimates: int) -> int:
    """Monte Carlo estimate of the number of points
    in a quarter circle using pure python.
    
    Args:
        nbr_estimates (int): number of estimates/attempts
    
    Returns:
        int: number of attempts that land inside unit circle
    """
    logging.info(f"Executing estimate_nbr_points_in_quarter_circle " +
                   f"with {nbr_estimates} on pid {os.getpid()}")
    start = time.time()
    nbr_trials_in_quarter_unit_circle = 0
    
    for _ in range(int(nbr_estimates)):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        is_in_unit_circle = (x * x + y * y <= 1.0)
        nbr_trials_in_quarter_unit_circle += is_in_unit_circle
    end = time.time()
    duration = round(end - start,4)
    logging.info(f"Time taken: {duration}")
    return nbr_trials_in_quarter_unit_circle


# Using multiprocessing for process-based parallelism
def estimate_nbr_points_multiprocessing(func: Callable, nbr_samples_in_total: int, num_cores: int):
    """Using multiprocessing Pool to parallelize CPU bound task with multiple cores."""
    # start = time.time()
    # instantiate Pool object for process-based parallelism
    pool = Pool(processes=num_cores)
    
    nbr_samples_per_worker = nbr_samples_in_total / num_cores
    logging.info(f"Making {nbr_samples_per_worker} samples per {num_cores} worker")

    #list of number of samples per process
    nbr_trials_per_process = [nbr_samples_per_worker] * num_cores

    # returns a list of results
    nbr_in_quarter_unit_circles = pool.map(func,
                                        nbr_trials_per_process)
    logging.info(nbr_in_quarter_unit_circles)
    pi_estimate = sum(nbr_in_quarter_unit_circles) * 4 / float(nbr_samples_in_total)
    
    # end = time.time()
    # duration = round(end-start, 4)
    # logging.info(f"Time taken using multiprocessing: {duration}")
    
    logging.info(pi_estimate)


#TODO: change trials object
def multiprocessor(func: Callable, num, num_cores: Optional[int] = os.cpu_count()):
    """Generalize multiprocessing pool.map to different functions."""
    if num_cores > os.cpu_count():
        raise ValueError(f"Maximum number of core available is {os.cpu_count()}.")
    
    pool = Pool(processes=num_cores)
    trials = [num/num_cores*n for n in range(1, num_cores+1)]
    res = pool.map(func, trials)
    return res


def not_embarrassingly_parallel(num: int):
    """This function is not embarrassingly parallel because it takes last output."""
    res = list()
    for n in range(int(num)):
        res.append(n)
    return res



if __name__ == "__main__":
    nbr_samples_in_total = 1e8
    estimate_nbr_points_in_quarter_circle(nbr_samples_in_total)
    estimate_nbr_points_multiprocessing(estimate_nbr_points_in_quarter_circle, nbr_samples_in_total, 10)
    
    # output = multiprocessor(not_embarrassingly_parallel, 100)
    # logging.info(output)
