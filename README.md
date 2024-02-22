<!-- ABOUT THE PROJECT -->
## About The Project

This is a project to use process-based and thread-based parallelism.

* Parallelize a CPU-bound task with Process or Pool objects
* Parallelize an I/O-bound task in a Pool with threads using the (oddly named) dummy module
* Share pickled work via a Queue
* Share state between parallelized workers, including bytes, primitive data types, dictionaries, and lists

## Lessons
1. Joblib is useful when function output can be cached in disk or can share Numpy data between process

## Improvement
1. Figure out how to use decorator with multiprocessing
2. Figure out how to generalize multiprocessing pool.map to use for different functions.

### Built With

* High Performance Python

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

### Installation

1. Clone the repo
    ```bash
    git clone git@github.com:dustinbaekpersonal/process-thread.git
    ```

2. Create virtual environment and activate
    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    ```

<!-- USAGE EXAMPLES -->
## Usage

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

- [x] Create README.md template
- [ ]
