"""Multiprocessing with pandas"""
import multiprocessing as mp
from functools import partial

import pandas as pd


def do_something(args, df, what):
    name, index = args
    res_df = df.loc[index]
    res_df["FOO"] += what
    return res_df

def do_smt_parallel(asdf, df_given):
    with mp.Pool(processes = 4) as pool:
        # using partial allows map to take multiple arguments, by fixing df as df_given
        partial_func = partial(do_something, df = df_given, what = 100)
        results = pool.map(partial_func, asdf)
        final_df = pd.concat(results, axis = 0, ignore_index = True)
        return final_df

def do_big_thing(df_given):
    asdf = list(df_given.groupby(by = ["COVERED", "DAY"]).groups.items())

    return do_smt_parallel(asdf, df_given)


if __name__ == "__main__":
    df = pd.DataFrame(
    {
        "COVERED": [1] * 10,
        "DAY": ["Monday"] * 3 + ["Tuesday"] * 5 + ["Wednesday"] * 2,
        "FOO": [num for num in range(10)],
        "BAR": ["asfd"]*5 + ["qwer"]*5
    }
)
    print("Before", df)
    res = do_big_thing(df)
    print(res)

    
