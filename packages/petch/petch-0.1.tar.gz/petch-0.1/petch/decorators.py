from petch.logging import log
import cProfile
import pstats
from time import time

def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        return result
    return wrap_func


def profile_function(func):
    def wrapper(*args, **kwargs):
        with cProfile.Profile() as pr:
            result = func(*args, **kwargs)
            stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.dump_stats(filename="profiling.prof")
        return result
    return wrapper

def log_funtion_and_input_output(func):
    def create_text(inputs):
        try: return '\n'.join([str(input) for input in inputs])
        except TypeError: return f"{str(inputs)}"
    def wrap(*args,**kwargs):
        results = func(*args,**kwargs)
        log(f"{create_text([func.__name__,'Input:',create_text(args),create_text(kwargs),'Output:',create_text(results)])}")
        return results
    return wrap