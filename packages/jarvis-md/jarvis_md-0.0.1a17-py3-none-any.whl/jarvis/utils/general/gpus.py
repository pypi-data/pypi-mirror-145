import subprocess, re, os, random
from .printer import printd

def run_nvidia_smi():

    try:
        o = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        o = o.stdout.decode('utf-8').split('\n')
    except:
        o = []

    return o

def find_all(ignore_devices=[], **kwargs):
    """
    Method to find all available NVIDIA GPU(s) and associated usage status

    """
    lines = run_nvidia_smi()
    gpus = {}

    for n, line in enumerate(lines):
        
        # --- Look for _ MiB / _ MiB
        usage = re.findall('[0-9]*MiB', line)
        if len(usage) == 2 and n > 0:
            device = re.findall(' +[0-9]+', lines[n - 1])
            if len(device) > 0:
                if int(device[0]) not in ignore_devices:

                    gpus[int(device[0])] = {
                        'alloc': int(usage[0][:-3]),
                        'total': int(usage[1][:-3]),
                        'percentage': int(usage[0][:-3]) / int(usage[1][:-3])}

    return gpus

def find_available(percentage=0.5, alloc=5000, total=11000, **kwargs):
    """
    Method to find available NVIDIA GPU(s) based on criteria

    """
    return {k: v for k, v in find_all(**kwargs).items() if \
        (v['percentage'] < percentage) & \
        (v['alloc'] < alloc) & \
        (v['total'] > total)}

def autoselect(count=1, set_memory_growth=False, memory_limit=None, percentage=0.5, alloc=5000, total=11000, randomize=True, run_first_op=True, ignore_devices=[], verbose=True, **kwargs):
    """
    Method to autoselect available NVIDIA GPU(s)

      (1) Use currently set os.environ['CUDA_VISIBLE_DEVICES'] if present, otherwise
      (2) Use availabe GPU(s) based on count

    :params

      (int)   count             : total # of GPU(s) to allocate
      (int)   set_memory_growth : allow GPU memory to grow (prevents allocating all memory at outset) 
      (int)   memory_limit      : maximum GPU memory growth (in MiB)
      (float) percentage        : threshold for max current percentage usage
      (int)   alloc             : threshold for max current alloc GPU memory (MiB)
      (int)   total             : threshold for min current total GPU memory (MiB)
      (bool)  randomize         : if True, select random GPU meeting critiera; otherwise in PCI_BUS_ID order
      (bool)  run_first_op      : if True, runs one TF operation to allocate memory 
      (list)  ignore_devices    : list of CUDA devices (integers) to ignore

    By default, this method will select 1 GPU with:

      * percent usage < 50%
      * alloc GPU memory < 5000 MiB
      * total GPU memory > 11000 MiB

    """
    allocate_cuda_devices(count=count, percentage=percentage, alloc=alloc, total=total, randomize=randomize, ignore_devices=ignore_devices, verbose=verbose, **kwargs)
    allocate_mem(set_memory_growth=set_memory_growth, memory_limit=memory_limit, run_first_op=run_first_op, **kwargs)

def allocate_cuda_devices(count, percentage, alloc, total, randomize, verbose, **kwargs):

    os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
    DEVICES = os.environ.get('CUDA_VISIBLE_DEVICES', '')

    if len(DEVICES) > 0:
        printd('CUDA_VISIBLE_DEVICES already manually set to: {}'.format(DEVICES), verbose=verbose)
        return

    gpus = find_available(percentage=percentage, alloc=alloc, total=total, **kwargs)
    keys = list(gpus.keys())

    if len(keys) < count:
        printd('WARNING {} GPU device(s) requested but only {} available'.format(count, len(keys)), verbose=verbose)
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1' 
        return

    if count <= 0: 
        printd('CPU mode requested', verbose=verbose)
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1' 
        return

    if randomize:
        random.shuffle(keys)

    keys = sorted(keys[:count])
    DEVICES = ','.join([str(k) for k in keys])
    os.environ['CUDA_VISIBLE_DEVICES'] = DEVICES

    printd('CUDA_VISIBLE_DEVICES automatically set to: {}'.format(DEVICES), verbose=verbose)

def allocate_mem(set_memory_growth=False, memory_limit=None, run_first_op=True, **kwargs):
    """
    Method to run single tensor operation to allocate GPU memory

    """
    try: 
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')

        if set_memory_growth:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)

        if memory_limit is not None:
            for gpu in gpus:
                tf.config.set_logical_device_configuration(gpu, 
                    [tf.config.LogicalDeviceConfiguration(memory_limit=memory_limit)])

        if run_first_op:
            from tensorflow.keras import Input, layers
            layers.Dense(1)(Input((1,)))

    except: pass

def get_devices():
    """
    Method to return list of allocated devices

    """
    return [int(d) for d in os.environ.get('CUDA_VISIBLE_DEVICES', '').split(',') if d.isdigit()]
