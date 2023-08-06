import time
from .printer import printd

def timeit(func):

    def wrapper(*args, **kwargs):

        t0 = time.time()
        ret = func(*args, **kwargs)
        printd('Elapsed time: {:0.5f} sec'.format(time.time() - t0), verbose=kwargs.get('verbose', True))

        return ret

    return wrapper
