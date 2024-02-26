import logging
import time
import random
import os
from joblib import Parallel, Memory, delayed

from parallelisation_mp import estimate_nbr_points_in_quarter_circle

logging.basicConfig(level = logging.INFO)

if __name__ == "__main__":
    nbr_samples_in_total = 1e8
    nbr_parallel_blocks = 10
    nbr_samples_per_worker = int(nbr_samples_in_total/nbr_parallel_blocks) 
    nbr_in_quarter_unit_circles = Parallel(n_jobs=nbr_parallel_blocks, verbose=1) \
            (delayed(estimate_nbr_points_in_quarter_circle)(nbr_samples_per_worker) \
    for sample_idx in range(nbr_parallel_blocks))
    
    pi_estimate = sum(nbr_in_quarter_unit_circles) * nbr_parallel_blocks  / float(nbr_samples_in_total)
    
    print(pi_estimate)
    
    """Avoid passing large structures; 
    passing large pickled objects to each process may be expensive. 
    e.g. a prebuilt cache of Pandas DataFrames in a dictionary object; 
    the cost of serializing these via the Pickle module negated the gains from parallelization, 
    and the serial version actually worked faster overall. 
    The solution in this case was to build the DataFrame cache using Python’s built- in shelve module"""
    
    
    ### Caching of function results ###
    memory = Memory("./joblib_cache", verbose=0)
    
    @memory.cache
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
    
    nbr_in_quarter_unit_circles = Parallel(n_jobs=nbr_parallel_blocks, verbose=1) \
            (delayed(estimate_nbr_points_in_quarter_circle)(nbr_samples_per_worker) \
    for sample_idx in range(nbr_parallel_blocks)) 

    pi_estimate = sum(nbr_in_quarter_unit_circles) * nbr_parallel_blocks  / float(nbr_samples_in_total)
    
    print(pi_estimate)
    
    