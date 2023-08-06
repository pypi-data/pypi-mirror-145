import multiprocessing as mp


__all__ = ["mp_starmap"]


def _star_wrapper(arg):
    """
    Internal helper function used to allow multiple arguments for functions
    called by `mp_starmap`.
    """
    (func, args) = arg
    return func(*args)


def mp_starmap(func, argss, process_count=None, chunksize=1, pbar_func=None, pbar_kwargs=None):
    """
    Run `func(*argss[0])`, `func(*argss[1])`, ... in parallel and return the
    results as list in the same order.

    This function internally uses `multiprocessing.Pool.map` or
    `multiprocessing.Pool.imap` (depending on whether a progress bar is to be
    used), but supports multiple function arguments (similar to
    `multiprocessing.Pool.starmap`).

    The progress bar function argument `pbar_func` is compatible with `tqdm`,
    i.e. `tqdm.tqdm` (without parentheses!) is a valid choice. If it is `None`,
    no progress bar is used. Optional progress bar keyword arguments (e.g.,
    "unit") can be supplied via the `pbar_kwargs` argument.
    """

    argss_for_star_wrapper = tuple((func, args) for args in argss)
    
    with mp.Pool(processes=process_count) as pool:
        if pbar_func is None:
            # case 1: no progress bar
            return pool.map(func=_star_wrapper, iterable=argss_for_star_wrapper, chunksize=chunksize)
        else:
            # case 2: tqdm-compatible porgress bar
            results = []
            if pbar_kwargs is None:
                pbar_kwargs = {}
            with pbar_func(total=len(argss), **pbar_kwargs) as pbar:
                for result in pool.imap(func=_star_wrapper, iterable=argss_for_star_wrapper, chunksize=chunksize):
                    pbar.update()
                    results.append(result)
            return results
