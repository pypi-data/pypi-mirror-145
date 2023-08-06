import numpy as np

def get_module_gpu(name):
    """
    Method to get CuPy compatible modules if available and requested

    """
    if name == 'np':
        import cupy as np
        return np

    if name == 'ndimage': 
        from cupyx.scipy import ndimage
        return ndimage 

    if name == 'linalg': 
        from cupyx.scipy import linalg 
        return linalg 

    if name == 'stats': 
        from cupyx.scipy import stats 
        return stats 

def get_module_cpu(name):
    """
    Method to get NumPy compatible module (default)

    """
    if name == 'np':
        import numpy as np
        return np

    if name == 'ndimage': 
        from scipy import ndimage
        return ndimage 

    if name == 'linalg': 
        from scipy import linalg 
        return linalg 

    if name == 'stats': 
        from scipy import stats 
        return stats 

def get_module(name, use_cupy=False):

    if use_cupy:
        try:
            return get_module_gpu(name)
        finally: pass

    return get_module_cpu(name)

def get_modules(module_names=('np', 'ndimage'), use_cupy=False):
    """
    Method to get CuPy compatible modules if available and requested

    """
    if 'np' not in module_names:
        module_names = list(module_names) + ['np']

    return {n: get_module(name=n, use_cupy=use_cupy) for n in module_names}

def to_gpu(obj, cp):
    """
    Method to convert object to GPU

    """
    if type(obj) is np.ndarray:
        return cp.asarray(obj)

    if type(obj) in [list, tuple]:
        return [to_gpu(obj=o, cp=cp) for o in obj]

    if type(obj) is dict:
        return {k: to_gpu(obj=v, cp=cp) for k, v in obj.items()}

    return obj

def to_cpu(obj, cp, release_cupy_memory=False):
    """
    Method to convert object to CPU

    """
    if type(obj) is cp.ndarray:
        obj_cpu = cp.asnumpy(obj)
        del obj
        return obj_cpu

    if type(obj) is list:
        obj_cpu = [to_cpu(obj=o, cp=cp) for o in obj]
        for n in range(len(obj)):
            obj[n] = None
        return obj_cpu

    if type(obj) is dict:
        obj_cpu = {k: to_cpu(obj=v, cp=cp) for k, v in obj.items()}
        for k in obj:
            obj[k] = None
        return obj_cpu

    return obj

def cupy_compatible(func):
    """
    Decorator for CuPy compatible methods

      (1) Load CuPy modules (if available and request)
      (2) Convert all NumPy inputs to CuPy arrays
      (3) Call method
      (4) Convert all CuPy outputs back to NumPy (based on return_numpy flag)

    """
    def wrapper(*args, use_cupy=False, return_numpy=True, _nested_call=False, module_names=('np', 'ndimage'), release_cupy_memory=False, **kwargs):

        # --- Determine whether to use_cupy / return_numpy based on _nested_call status
        use_cupy = use_cupy or _nested_call
        return_numpy = return_numpy and (not _nested_call)

        # --- Get CuPy compatible modules
        modules = get_modules(module_names=module_names, use_cupy=use_cupy)
        CUPY_IS_LOADED = modules['np'] != np

        # --- Convert inputs to CuPy 
        if CUPY_IS_LOADED:
            args = [to_gpu(a, cp=modules['np']) for a in args]
            kwargs = {k: to_gpu(v, cp=modules['np']) for k, v in kwargs.items()}

        kwargs.update(modules)
        kwargs['_nested_call'] = use_cupy
        ret = func(*args, **kwargs)

        # --- Convert return to NumPy
        if CUPY_IS_LOADED:

            # --- Convert to CPU if needed
            if return_numpy:
                ret = to_cpu(ret, cp=modules['np']) 
                if release_cupy_memory:
                    release_cupy_memory_manual(**kwargs)

            # --- Convert to GPU if needed
            else:
                ret = to_gpu(ret, cp=modules['np'])

        return ret

    return wrapper

def cupy_non_compatible(func):
    """
    Decorator for CuPy non-compatible methods

      (1) Convert all CuPy inputs to NumPy arrays
      (3) Call method
      (4) Convert all NumPy outputs back to CuPy (based on return_cupy flag)

    """
    def wrapper(*args, use_cupy=False, return_cupy=True, _nested_call=False, **kwargs):

        # --- Determine whether to use_cupy / return_numpy based on _nested_call status
        use_cupy = use_cupy or _nested_call
        return_cupy = return_cupy

        # --- Get CuPy compatible modules (check if available)
        modules = get_modules(module_names=('np',), use_cupy=use_cupy)
        CUPY_IS_LOADED = modules['np'] != np

        # --- Convert inputs to CuPy 
        if CUPY_IS_LOADED:
            args = [to_cpu(a, cp=modules['np']) for a in args]
            kwargs = {k: to_cpu(v, cp=modules['np']) for k, v in kwargs.items()}

        kwargs['_nested_call'] = use_cupy
        ret = func(*args, **kwargs)

        # --- Convert return to NumPy
        if CUPY_IS_LOADED:
            return to_gpu(ret, cp=modules['np']) if return_cupy else to_cpu(ret, cp=modules['np'])

        return ret

    return wrapper

def release_cupy_memory_manual(verbose=False, **kwargs):

    try:

        import cupy

        mempool = cupy.get_default_memory_pool()
        pinned_mempool = cupy.get_default_pinned_memory_pool()

        mempool.free_all_blocks()
        pinned_mempool.free_all_blocks()

        if verbose:
            print('Memory pool: {} bytes'.format(mempool.total_bytes()))
            print('Pinned memory pool: {} bytes'.format(pinned_mempool.n_free_blocks()))

    except: pass
