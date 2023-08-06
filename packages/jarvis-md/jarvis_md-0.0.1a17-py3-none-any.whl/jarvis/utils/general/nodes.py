import os, glob, shutil, time, json, socket
from .printer import printr, printd
from .hasher import sha1
from .gpus import autoselect, get_devices

class Port():

    def __init__(self):

        self.socket = None 

    def __enter__(self):

        return self

    def bind_random(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 0))

        return self.socket.getsockname()[1]

    def get_hostname(self):

        return socket.gethostname()

    def __exit__(self, exc_type, exc_value, traceback):

        if self.socket is not None:
            self.socket.close()

def get_worker_jsons(temp_dir, truncate=6, **kwargs):

    pattern = '{}/worker-'.format(temp_dir) + '?' * truncate + '.json'

    return sorted(glob.glob(pattern))

def get_worker_dicts(worker_jsons=None, **kwargs):

    worker_jsons = worker_jsons or get_worker_jsons(**kwargs)

    return [json.load(open(w, 'r')) for w in worker_jsons]

def join(n_workers=2, n_gpus=1, temp_dir='./join', name=None, port=None, sleep=2, timeout=120, truncate=6, **kwargs):

    with Port() as p:

        # --- Get hostname and random port
        name = name or p.get_hostname()
        port = port or p.bind_random()
        
        if not os.path.exists(temp_dir):
            printd('Creating temp_dir: {}'.format(temp_dir))
            os.makedirs(temp_dir, exist_ok=True)

        # --- Remove all old files
        for fname in get_worker_jsons(temp_dir, truncate=truncate):
            if time.time() - os.stat(fname).st_mtime > timeout:
                printd('Removing old worker JSON files: {}'.format(temp_dir))
                os.remove(fname)

        # --- Get allocated CUDA devices
        dicts = get_worker_dicts(temp_dir=temp_dir, truncate=truncate)
        ignore_devices = [d['gpus'] for d in dicts if d['name'] == name]
        autoselect(count=n_gpus, ignore_devices=ignore_devices, run_first_op=False, **kwargs)

        # --- Create and serialize worker_json
        worker_hash = sha1(time.time(), truncate=truncate)
        worker_json = '{}/worker-{}.json'.format(temp_dir, worker_hash)
        worker_dict = {
            'hash': worker_hash, 
            'name': name, 'port': port, 
            'gpus': get_devices(), 
            'done': False} 

        json.dump(worker_dict, open(worker_json, 'w'))

        # --- Await
        for _ in range(int(timeout / sleep)):
            workers = get_worker_jsons(temp_dir, truncate=truncate) 
            printr('PENDING: total of {}/{} workers joined'.format(len(workers), n_workers))
            if len(workers) >= n_workers: 
                break
            time.sleep(sleep)

    # --- Early exit
    if len(workers) != n_workers:
        printr('ERROR: total of {} workers joined ({} requested)'.format(len(workers, n_workers)))
        return

    # --- Mark current worker as done
    printr('COMPLETE: total of {}/{} workers joined'.format(len(workers), n_workers))
    worker_dict['done'] = True
    json.dump(worker_dict, open(worker_json, 'w'))
    dicts = get_worker_dicts(workers)

    # --- Remove worker files if complete
    if all([w['done'] for w in dicts]):

        # --- Remove worker files
        for w in workers:
            if os.path.exists(w):
                os.remove(w)

        if len(glob.glob('{}/*'.format(temp_dir))) == 0:
            shutil.rmtree(temp_dir)

    return dicts, worker_dict

def join_tf(n_workers=2, n_gpus=1, temp_dir='./join', name=None, port=None, sleep=2, timeout=120, truncate=6, **kwargs):
    """
    Method to join current node to cluster and await total of N nodes to join

    :params

      (int) n_workers       : required total number of workers before cluster is initialized
      (int) n_gpus          : gpus per worker
      (str) temp_dir        : temp directory used to cache worker config JSON files 
      (str) name            : hostname or IP address of current worker (if None, auto-populate)
      (int) port            : port to associate with current worker; if None then random open port is allocated

    """
    # --- Join
    dicts, worker_dict = join(n_workers=n_workers, n_gpus=n_gpus, temp_dir=temp_dir, name=name, port=port, sleep=sleep, timeout=timeout, truncate=truncate, **kwargs)

    # --- Create TF_CONFIG
    TF_CONFIG = {
        'cluster': {
            'worker': ['{}:{}'.format(w['name'], w['port']) for w in dicts]},
        'task': {
            'type': 'worker',
            'index': [w['hash'] for w in dicts].index(worker_dict['hash'])}}

    os.environ['TF_CONFIG'] = json.dumps(TF_CONFIG)
    printd('TF_CONFIG environment var set: {}'.format(TF_CONFIG))

    return TF_CONFIG
