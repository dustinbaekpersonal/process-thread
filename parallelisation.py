"""Intro to multiprocessing library."""
import logging
import os
import random
import time
from multiprocessing import Pool

logging.basicConfig(level = logging.INFO)


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        duration = round(end - start,6)
        logging.info(f"Time taken: {duration}")
        return duration
    return wrapper

# Example 1. Estimating Pi using Monte Carlo Method
# @timer
def estimate_nbr_points_in_quarter_circle(nbr_estimates):
    """Monte Carlo estimate of the number of points
    in a quarter circle using pure python."""
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
    logging.info(duration)
    return nbr_trials_in_quarter_unit_circle


def estimate_nbr_points_multiprocessing(nbr_samples_in_total, num_cores: int):
    """Using multiprocessing Pool to parallelize CPU bound task with multiple cores."""
    # number of CPU cores to use
    nbr_parallel_blocks = num_cores
    # instantiate Pool object for process-based parallelism
    pool = Pool(processes=nbr_parallel_blocks)
    
    nbr_samples_per_worker = nbr_samples_in_total / nbr_parallel_blocks
    logging.info(f"Making {nbr_samples_per_worker} sampels per {nbr_parallel_blocks} worker")

    #list of number of samples per process
    nbr_trials_per_process = [nbr_samples_per_worker] * nbr_parallel_blocks

    # returns a list of results
    nbr_in_quarter_unit_circles = pool.map(estimate_nbr_points_in_quarter_circle,
                                        nbr_trials_per_process)
    logging.info(nbr_in_quarter_unit_circles)
    pi_estimate = sum(nbr_in_quarter_unit_circles) * 4 / float(nbr_samples_in_total)
    logging.info(pi_estimate)


if __name__ == "__main__":
    nbr_samples_in_total = 1e4
    # estimate_nbr_points_in_quarter_circle(nbr_samples_in_total)
    estimate_nbr_points_multiprocessing(nbr_samples_in_total, 4)
    