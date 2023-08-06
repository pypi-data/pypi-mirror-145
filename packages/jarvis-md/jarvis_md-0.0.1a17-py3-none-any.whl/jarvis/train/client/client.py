import os, shutil, glob, yaml
import numpy as np, pandas as pd
from ...utils import io
from ...utils.db import DB
from ...utils.general import *
from ...utils.general import tools as jtools
from ...utils.display import interleave

class Client():

    def __init__(self, *args, **kwargs):
        """
        Method to initialize client

        """
        # --- Initialize client 
        self.init_client(*args, **kwargs)
        self.init_client_custom(*args, **kwargs)

        # --- Initialize batch composition 
        self.prepare_batch(**kwargs)

        # --- Initialize custom functions
        self.load_func = kwargs.pop('load', None) or io.load
        self.daug_func = kwargs.get('augment', None)
        self.prep_func = kwargs.get('preprocess', None)

        self.init_empty_fnames = getattr(self, 'init_empty_fnames', None) or kwargs.pop('empty_fnames', None) or np.zeros
        self.init_empty_header = getattr(self, 'init_empty_header', None) or kwargs.pop('empty_header', None) or np.ones

        # --- Initialize in-memory
        if self.specs['in_memory']:
            self.load_data_in_memory()

    def init_client(self, *args, **kwargs):
        """
        Method to load metadata from YML

        """
        # --- Serialization attributes
        self.ATTRS = ['_id', '_db', 'current', 'batch', 'specs']

        DEFAULTS = {
            '_db': None,
            'data_in_memory': {},
            'indices': {'train': {}, 'valid': {}},
            'current': {'train': {}, 'valid': {}},
            'batch': {'fold': -1, 'size': None, 'sampling': None, 'training': {'train': 0.8, 'valid': 0.2}},
            'specs': {'xs': {}, 'ys': {}, 'load_kwargs': {}, 'in_memory': False, 'tiles': [False] * 4}}

        # --- Initialize configs
        configs = jtools.parse_args(*args, **kwargs)
        paths = configs.pop('paths')
        files = configs.pop('files')

        # --- Extract client
        client = '{}{}'.format(paths['code'], files['yml']) if files['yml'] is not None else './client.yml'

        # --- Load client
        if not os.path.exists(client):
            printd('WARNING location of client.yml file could not be determined')

        else:
            with open(client, 'r') as y:
                y = yaml.load(y, Loader=yaml.FullLoader)
                recursive_set(y, kwargs.pop('configs', {}), append_lists=False, existing_keys_only=True)
                configs = y

        # --- Initialize default values
        for key, d in DEFAULTS.items():
            configs[key] = {**DEFAULTS[key], **configs.get(key, {})} if type(d) is dict else \
                configs.get(key, None) or DEFAULTS[key]

        # --- Set attributes
        for attr, config in configs.items():
            setattr(self, attr, config)

        # --- Set (init) specs
        self.set_specs()

        # --- Set custom layers
        if kwargs.get('custom_layers', False):
            self.specs['xs'].update(self.specs.pop('ys'))
            self.specs['ys'] = {}

        # --- Find db path 
        full = self._db
        if not os.path.exists(full or ''):
            if self._id['project'] is not None:

                code = paths['code'] or jtools.get_paths(
                    project_id=self._id['project'], 
                    version_id=self._id['version'], 
                    alt_path=client)['code']

                full = '{}{}'.format(code, full)

        # --- Load
        kwargs.pop('prefix', None)
        kwargs.pop('subdir', None)

        ext = 'yml' if (full or '')[-3:] == 'yml' else 'csv'
        kwargs[ext] = full

        self.db = DB(*args, **kwargs)

    def init_client_custom(self, *args, **kwargs):

        pass

    def to_dict(self):
        """
        Method to create dictionary of metadata

        """
        return {attr: getattr(self, attr) for attr in self.ATTRS}

    def to_yml(self, fname='./client.yml', **kwargs):
        """
        Method to serialize metadata to YML 

        """
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        with open(fname, 'w') as y:
            yaml.dump(self.to_dict(), y, sort_keys=False, **kwargs)

    def check_data_is_loaded(func):
        """
        Method (decorator) to ensure the self.data / self.meta is loaded

        """
        def wrapper(self, *args, **kwargs):

            if self.db.fnames.size == 0:
                self.db.load_csv()

            return func(self, *args, **kwargs)

        return wrapper

    @check_data_is_loaded
    def load_data_in_memory(self, MAX_SIZE=32):
        """
        Method to load all required fnames into memory

        """
        # --- Find exams used in current training 
        mask = self.rows_to_load()

        # --- Find keys to load
        to_load = self.fnames_to_load()

        # --- TODO: Check if dataset exceeds MAX_SIZE

        # --- Load exams into self.data_in_memory
        for sid, fnames, header in self.db.cursor(mask=mask, drop_duplicates=True, subset=to_load, use_cache=False, flush=True):
            for key in to_load:
                if fnames[key] not in self.data_in_memory:
                    load_kwargs = self.get_load_kwargs(full_res=True) 
                    self.data_in_memory[fnames[key]] = self.load_func(fnames[key], **load_kwargs)
                    if type(self.data_in_memory[fnames[key]]) is tuple:
                        self.data_in_memory[fnames[key]] = self.data_in_memory[fnames[key]][0]

        # --- Change default load function
        self.load_func = self.find_data_in_memory
    
    @check_data_is_loaded
    def load_data_in_cache(self, cache='/cache', dst_root=None, compression=None, rewrite=False, jars_objects=True, **kwargs):
        """
        Method to copy all required fnames into local cache (e.g., SSD/NVME)

        By default, HDF5 files (Jarvis objects) will be reserialized without compression. 

        If necessary, manually pass "chunks=None" as well if chunking should be removed (e.g., 3D models).

        :params

          (str) cache    : path to local cache directory
          (str) dst_root : full path to local cache directory for current project (optional)

        By default, dst_root is combination of: [ cache ] / [ project_id ]

        """
        # --- Find exams used in current training 
        mask = self.rows_to_load()

        # --- Find keys to load
        to_load = self.fnames_to_load()

        # --- TODO: Check if dataset exceeds MAX_SIZE

        # --- Load exams into cache
        src_root = self.db.paths['data']
        dst_root = dst_root or '{}/{}'.format(cache, self._id['project'].replace('-', '_').replace('/', '_'))

        self.db.fnames_expanded = {}
        for sid, fnames, header in self.db.cursor(mask=mask, drop_duplicates=True, subset=to_load, use_cache=False, flush=True):
            for key in to_load:
                dst = fnames[key].replace(src_root, dst_root, 1)
                if os.path.exists(fnames[key]) and (not os.path.exists(dst) or rewrite):

                    if fnames[key][-5:] == '.hdf5' and jars_objects:
                        data, meta = io.load(fnames[key])
                        io.save(fname=dst, data=data, meta=meta, compression=compression, verbose=False, **kwargs)

                    elif os.path.isfile(fnames[key]):
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copy(src=fnames[key], dst=dst)

                    elif os.path.isdir(fnames[key]):
                        shutil.copytree(src=fnames[key], dst=dst)

        # --- Change root
        self.db.paths['data'] = dst_root
        self.db.fnames_expanded = {}

    @check_data_is_loaded
    def unload_data_in_cache(self, cache='/cache', dst_root=None, override_warning=False):
        """
        Method to delete files from local cache

        """
        # --- Find exams used in current training 
        mask = self.rows_to_load()

        # --- Find keys to load
        to_load = self.fnames_to_load()

        # --- Load exams into cache
        dst_root = dst_root or '{}/{}'.format(cache, self._id['project'].replace('-', '_').replace('/', '_'))

        if dst_root != self.db.paths['data']:
            self.db.paths['data'] = dst_root

        if ('/data/raw' in self.db.paths['data']) and not override_warning:
            printd('WARNING attempting to delete data from /data/raw')
            return

        self.db.fnames_expanded = {}
        for sid, fnames, header in self.db.cursor(mask=mask, drop_duplicates=True, subset=to_load, flush=True):
            for key in to_load:

                if os.path.exists(fnames[key]):

                    if os.path.isfile(fnames[key]):
                        os.remove(fnames[key])

                    elif os.path.isdir(fnames[key]):
                        shutil.rmtree(fnames[key])

        # --- Reset paths
        self.db.paths['data'] = ''
        self.db.load_paths()

        # --- Remove folder if empty
        for _, _, files in os.walk(dst_root):
            if len(files) > 0:
                return

        shutil.rmtree(dst_root)

    def rows_to_load(self):
        """
        Method to return mask of rows to load

        """
        mask = np.zeros(self.db.fnames.shape[0], dtype='bool') 
        for split in ['train', 'valid']:
            for key, rate in self.batch['sampling'][split].items():
                if rate > 0:
                    mask = mask | self.db.header[key].to_numpy()

        return mask

    def fnames_to_load(self):
        """
        Method to return list of fnames column entries to load

        """
        to_load = []
        to_load += [v['loads'] for v in self.specs['xs'].values() if v['loads'] in self.db.fnames]
        to_load += [v['loads'] for v in self.specs['ys'].values() if v['loads'] in self.db.fnames]

        return to_load

    def find_data_in_memory(self, fname, infos=None, **kwargs):
        """
        Method to retrieve loaded data 

        """
        data = self.data_in_memory.get(fname, None)

        # --- Process JarvisArrays
        if hasattr(data, 'to_numpy') and hasattr(data, 'attrib') and len(infos.get('shape', [])) == 3:
            shape = [s if s > 0 else t for s, t in zip(infos['shape'], data.data.shape)]
            if tuple(shape) != data.data.shape[:len(shape)]:
                data = data.new_array(
                    data=io.extract_data(data.to_numpy(), infos, **kwargs),
                    dtype=data.attrib.dtype,
                    calculate_stats=False)

            return data

        return io.extract_data(data, infos).copy() if ((type(data) is np.ndarray) and len(infos.get('shape', [])) == 3) else data
        
    @check_data_is_loaded
    def prepare_batch(self, fold=None, sampling_rates=None, training_rates={'train': 0.8, 'valid': 0.2}, shard=0, shards=1, shard_seed=0, verbose=True, **kwargs):
        """
        Method to prepare composition of data batches

        :params

          (int)  fold           : fold to use as validation 
          (dict) sampling_rates : rate to load each stratified cohort
          (dict) training_rates : rate to load from train / valid splits

        """
        # --- Set rates
        self.set_training_rates(training_rates)
        self.set_sampling_rates(sampling_rates)

        # --- Set default fold
        fold = fold or self.batch['fold']

        # --- Set data shard
        if shards > 1:
            mask_shard = np.zeros(self.db.fnames.shape[0], dtype='bool') 
            for split in ['train', 'valid']:
                for key, rate in self.batch['sampling'][split].items():
                    if rate > 0:
                        mask_shard = mask_shard | np.array(self.db.header[key])
            p = np.arange(np.count_nonzero(mask_shard)) % shards
            if shard_seed > -1:
                np.random.seed(shard_seed)
                p = p[np.random.permutation(p.size)]
            mask_shard[mask_shard > 0] = (p == shard)

        for split in ['train', 'valid']:

            # --- Determine mask corresponding to current split 
            if fold == -1:
                mask = np.ones(self.db.header.shape[0], dtype='bool')
            elif split == 'train': 
                mask = self.db.header['valid'] != fold
                mask = mask.to_numpy()
            elif split == 'valid':
                mask = self.db.header['valid'] == fold
                mask = mask.to_numpy()

            # --- Apply shard
            if shards > 1:
                mask = mask & mask_shard

            # --- Reset indices
            self.indices[split] = {}

            # --- Find indices for current cohort / split 
            for key in self.batch['sampling'][split].copy():
                self.indices[split][key] = np.nonzero(np.array(self.db.header[key]) & mask)[0]
                if len(self.indices[split][key]) == 0:
                    printd('WARNING {} cohort with key == {} contains no data, rescaling sampling rates accordingly'.format(split, key), verbose=verbose)
                    self.indices[split].pop(key)
                    self.batch['sampling'][split].pop(key)
                    self.set_sampling_rates()

            assert len(self.indices[split]) > 0, 'ERROR {} cohort contains no data'

            for cohort in self.indices[split]:

                # --- Randomize indices for next epoch
                if cohort not in self.current[split]:
                    self.current[split][cohort] = {'epoch': -1, 'count': 0}
                    self.prepare_next_epoch(split=split, cohort=cohort)

                # --- Reinitialize old index
                else:
                    self.shuffle_indices(split, cohort)
    
    def set_training_rates(self, rates={'train': 0.8, 'valid': 0.2}):

        assert 'train' in rates
        assert 'valid' in rates

        self.batch['training'] = rates

    def set_sampling_rates(self, rates=None):

        sampling_rates = rates or self.batch['sampling']

        if type(sampling_rates) is dict:
            sampling_rates = sampling_rates.copy()

        if sampling_rates is None:
            sampling_rates = {'train': None, 'valid': None}

        if ('train' not in sampling_rates) or ('valid' not in sampling_rates) or (len(sampling_rates) != 2):
            sampling_rates = {'train': sampling_rates.copy(), 'valid': sampling_rates.copy()}

        self.batch['sampling'] = {}
        self.sampling_rates = {}

        for split, rates in sampling_rates.items():

            # --- Default, all cases without stratification
            if rates is None:
                self.db.header['all'] = True
                rates = {'all': 1.0}

            if 'all' in rates and 'all' not in self.db.header:
                self.db.header['all'] = True

            # --- Scale all rates so that total adds to 100%
            rates = {k: v / sum(list(rates.values())) for k, v in rates.items() if v > 0}

            keys = sorted(rates.keys())
            vals = [rates[k] for k in keys]
            vals = [sum(vals[:n]) for n in range(len(vals) + 1)]

            lower = np.array(vals[:-1])
            upper = np.array(vals[1:])

            self.batch['sampling'][split] = rates

            self.sampling_rates[split] = {
                'cohorts': keys,
                'lower': np.array(lower),
                'upper': np.array(upper)} 

    # ====================================================================================
    # def init_normalization(self):
    #     """
    #     Method to initialize normalization functions as defined by self.spec
    #
    #     arr = (arr.clip(min, max) - shift) / scale
    #
    #     There three methods for defining parameters in *.yml file:
    #
    #       (1) shift: 64      ==> use raw value if provided
    #       (2) shift: 'mu'    ==> use corresponding column in DataFrame
    #       (3) shift: '$mean' ==> use corresponding Numpy function
    #
    #     """
    #     self.norm_lambda = {'xs': {}, 'ys': {}}
    #     self.norm_kwargs = {'xs': {}, 'ys': {}}
    #
    #     # --- Lambda function for extracting kwargs
    #     extract = lambda x, row, arr : row[x] if x[0] != '@' else getattr(np, x[1:])(arr)
    #
    #     for a in ['xs', 'ys']:
    #         for key, specs in self.specs[a].items():
    #             if specs['norms'] is not None:
    #
    #                 norms = specs['norms']
    #
    #                 # --- Initialize random transforms
    #                 if 'rands' not in norms:
    #                     norms['rands'] = {}
    #
    #                 norms['rands']['scale'] = {**norms['rands'].get('scale', {}), **norms.pop('rand_scale', {})}
    #                 norms['rands']['shift'] = {**norms['rands'].get('shift', {}), **norms.pop('rand_shift', {})}
    #
    #                 # --- Set up appropriate lambda function
    #                 if 'mapping' in norms:
    #                     l = self.map_array
    #
    #                 elif 'clip' in norms and ('shift' in norms or 'scale' in norms):
    #                     l = lambda x, clip, rand_shift, rand_scale, shift=0, scale=1, **kwargs : \
    #                         (x.clip(**clip) - (shift * rands(**rand_shift))) / (scale * rands(**rand_scale))
    #
    #                 elif 'clip' in norms:
    #                     l = lambda x, clip, **kwargs : x.clip(**clip)
    #
    #                 else:
    #                     l = lambda x, rand_shift, rand_scale, shift=0, scale=1, **kwargs : \
    #                         (x - (shift * rands(**rand_shift))) / (scale * rands(**rand_scale))
    #
    #                 self.norm_lambda[a][key] = l
    #
    #                 # --- Set up appropriate kwargs function 
    #                 self.norm_kwargs[a][key] = lambda row, arr, norms : \
    #                     {k: extract(v, row, arr) if type(v) is str else v for k, v in norms.items()}
    # ====================================================================================

    @check_data_is_loaded
    def print_cohorts(self):
        """
        Method to generate summary of cohorts

        ===========================
        TRAIN
        ===========================
        cohort-A: 1000
        cohort-B: 1000
        ...
        ===========================
        VALID
        ===========================
        cohort-A: 1000
        cohort-B: 1000
        ...

        """
        keys = sorted(self.indices['train'].keys())

        for split in ['train', 'valid']:
            printb(split.upper())
            for cohort in keys:
                size = self.indices[split][cohort].size
                printd('{}: {:06d}'.format(cohort, size))

    def set_specs(self, specs=None):

        self.specs.update(specs or {})

        # --- Initialize xs, ys
        for arr in ['xs', 'ys']:
            for k in self.specs[arr]:

                DEFAULTS = {
                    'dtype': None,
                    'input': True,
                    'loads': None,
                    'norms': None, 
                    'shape': None,
                    'xform': None}

                self.specs[arr][k] = {**DEFAULTS, **self.specs[arr][k]}

                # --- Initialize shape
                if type(self.specs[arr][k]['shape']) is list:
                    self.specs[arr][k]['shape'] = {
                        'saved': self.specs[arr][k]['shape'].copy(),
                        'input': self.specs[arr][k]['shape'].copy()}

                for field in ['saved', 'input']:
                    assert field in self.specs[arr][k]['shape']

                # --- Initialize norms
                if self.specs[arr][k]['norms'] is not None:
                    if 'clip' in self.specs[arr][k]['norms']:
                        if 'max' in self.specs[arr][k]['norms']['clip']:
                            self.specs[arr][k]['norms']['clip']['a_max'] = self.specs[arr][k]['norms']['clip'].pop('max')
                        if 'min' in self.specs[arr][k]['norms']['clip']:
                            self.specs[arr][k]['norms']['clip']['a_min'] = self.specs[arr][k]['norms']['clip'].pop('min')

                    for name in ['scale', 'shift']:
                        if 'rand_{}'.format(name) in self.specs[arr][k]['norms']:
                            if 'rands' not in self.specs[arr][k]['norms']:
                                self.specs[arr][k]['norms']['rands'] = {}
                            self.specs[arr][k]['norms']['rands'][name] = self.specs[arr][k]['norms'].pop('rand_{}'.format(name))

    def get_specs(self):

        extract = lambda x : {
            'shape': [None if t else s for s, t in zip(x['shape']['input'], self.specs['tiles'])],
            'dtype': x['dtype']}

        specs_ = {'xs': {}, 'ys': {}} 
        for k in specs_:
            for key, spec in self.specs[k].items():
                if spec['input']:
                    specs_[k][key] = extract(spec)

        return specs_

    def get_inputs(self, Input):
        """
        Method to create dictionary of Keras-type Inputs(...) based on self.specs

        """
        specs = self.get_specs()

        return {k: Input(
            shape=specs['xs'][k]['shape'],
            dtype=specs['xs'][k]['dtype'],
            name=k) for k in specs['xs']}

    def load(self, row, db=None, **kwargs):

        if db is None:
            db = self.db

        arrays = {'xs': {}, 'ys': {}}
        for k in arrays:
            for key, spec in self.specs[k].items():

                # --- Load from file 
                if spec['loads'] in db.fnames.columns:
                    load_kwargs = self.get_load_kwargs(row, spec['shape']['saved'], **kwargs)
                    arrays[k][key] = self.load_func(row[spec['loads']], **{**spec, **load_kwargs})
                    if type(arrays[k][key]) is tuple:
                        arrays[k][key] = arrays[k][key][0]
                    if arrays[k][key] is None:
                        arrays[k][key] = self.init_empty_fnames(shape=spec['shape']['saved'], dtype=spec['dtype'])

                # --- Load from row
                else:
                    if spec['loads'] is None:
                        arrays[k][key] = self.init_empty_header(shape=spec['shape']['saved'], dtype=spec['dtype'])
                    else:
                        if kwargs['infos'] is not None:
                            kwargs['index'] = self.prepare_index_from_infos(kwargs['infos'], row, db)
                        if kwargs['index'] is None:
                            arrays[k][key] = np.array(row[spec['loads']])
                        else:
                            arrays[k][key] = np.array(db.header[spec['loads']][kwargs['index']['rows']])

        return arrays

    def get_load_kwargs(self, row=None, shape=None, index=None, full_res=False, **kwargs):
        """
        Method to load kwargs

        The infos dict is constructed based on the following rules:

          (1) standard  : infos['shape'] from self.specs; infos['point'] from row
          (2) index     : infos['index'] from kwargs['index'] 
          (3) full_res  : infos = None 

        """
        load_kwargs = self.specs['load_kwargs'].copy()

        if full_res:
            load_kwargs['infos'] = None
            return load_kwargs

        infos = {}

        if index is None:

            z = row.get('coord-z', 0.5) if 'coord-z' in row else row.get('coord', 0.5)
            y = row.get('coord-y', 0.5)
            x = row.get('coord-x', 0.5)

            infos['point'] = [z, y, x] 
            infos['shape'] = shape[:3]

        else:

            infos['index'] = index 

        i = lambda x : x.get('infos', {}) or {}
        load_kwargs['infos'] = {**infos, **i(load_kwargs), **i(kwargs)}

        return load_kwargs

    def prepare_next_epoch(self, split, cohort):

        assert cohort in self.indices[split]

        # --- Increment current
        self.current[split][cohort]['epoch'] += 1
        self.current[split][cohort]['count'] = 0 

        # --- Generate new seed (try/catch needed for 32-/64-bit compatability)
        try:
            self.current[split][cohort]['rseed'] = np.random.randint(2 ** 32)
        except:
            self.current[split][cohort]['rseed'] = np.random.randint(2 ** 16)

        # --- Random shuffle
        self.shuffle_indices(split, cohort)

    def shuffle_indices(self, split, cohort):

        # --- Seed
        np.random.seed(self.current[split][cohort]['rseed'])

        # --- Shuffle indices
        s = self.indices[split][cohort].size
        p = np.random.permutation(s)
        self.indices[split][cohort] = self.indices[split][cohort][p]

    def prepare_next_array(self, split=None, cohort=None, row=None, rows=None, infos=None, db=None):

        if db is None:
            db = self.db

        # ===========================================================
        # LOAD MANUALLY SPECIFIED ROW(S)
        # ===========================================================

        if row is not None or rows is not None:

            rows = np.array(row).ravel() if row is not None else np.array(rows).ravel()
            row = db.row(rows[0])
            index = None if rows.size == 1 else self.prepare_index_from_rows(rows, db)

            return {'row': row, 'split': split, 'cohort': cohort, 'index': index}

        # ===========================================================
        # LOAD RANDOM ROW
        # ===========================================================

        if split is None:
            split = 'train' if np.random.rand() < self.batch['training']['train'] else 'valid'

        if cohort is None:
            if self.sampling_rates[split] is not None:
                i = np.random.rand()
                i = (i < self.sampling_rates[split]['upper']) & (i >= self.sampling_rates[split]['lower'])
                i = int(np.nonzero(i)[0])
                cohort = self.sampling_rates[split]['cohorts'][i]
            else:
                cohort = sorted(self.indices[split].keys())[0]

        c = self.current[split][cohort]

        if c['count'] > self.indices[split][cohort].size - 1:
            self.prepare_next_epoch(split, cohort)
            c = self.current[split][cohort]

        ind = self.indices[split][cohort][c['count']]
        row = db.row(index=ind)

        # --- Increment counter
        c['count'] += 1

        return {'row': row, 'split': split, 'cohort': cohort, 'index': None} 

    def prepare_index_from_rows(self, rows, db):
        """
        Method to convert rows into infos['index'] dictionary

        See jarvis.utils.io.extract_data(...) for more information.

        :params

          (np.ndarray) rows : all rows to load

        """
        unique = lambda x : np.unique(db.header[x][rows]) \
            if x in db.header else np.array(0.5) 

        # --- Find axis that is tiling
        for axis, c in zip([0, 0, 1, 2], ['coord', 'coord-z', 'coord-y', 'coord-x']):
            vals = unique(c)

            if vals.size > 1:
                return {'vals': vals.astype('float'), 'axis': axis, 'rows': rows}

        printd('ERROR no tiling axis is found')
        return {'vals': np.linspace(0, rows.size), 'axis': 0, 'rows': rows}

    def prepare_index_from_infos(self, infos, row, db):
        """
        Method to convert infos['point'] / infos['shape'] into index['row'] for purposes of header loading

        Note: this method assumes that infos at most tile along a single axis

        """
        rows = np.ones(db.fnames.shape[0], dtype='bool')
        fnames = db.fnames_expand()
        cols = self.fnames_to_load()
        for col in cols:
            rows = rows & (fnames[col] == row[col]).to_numpy()

        rows = np.nonzero(rows)[0]

        # --- Find subset based on tiles
        axis = np.nonzero(np.array(infos['shape']) > 0)[0]
        if axis.size > 1:
            printd('WARNING more than a single axis appears to be tiling based on passed infos dict')
        if axis.size == 1:
            point = infos['point'][axis[0]]
            shape = infos['shape'][axis[0]]
            point = np.round(point * rows.size)
            lower = point - np.floor(shape / 2)
            upper = lower + shape
            rows = rows[int(lower):int(upper)]

        return {'rows': rows}

    @cupy_compatible
    def get(self, split=None, cohort=None, row=None, rows=None, infos=None, test=False, db=None, flexible_dtype=True, warp_gen=None, use_cupy=False, _nested_call=False, **kwargs):
        """
        Method to load and process data 

        :params

          (str)  split  : train or valid (default, pick randomly based on training_rates)
          (str)  cohort : cohort to sample from (default, all)
          (int)  row    : get data from specified single row (ignore split or cohort)
          (iter) rows   : get data from specified multiple rows (ignore split or cohort)

            For iterable rows load, the following is assumed:
              
              * All rows are derived from the same file
              * All rows together yield a batch of data
              * Array size returned is standard arr.ndim + 1 (e.g. tiles are stacked along axis=0)

            For loading arbitrary data shapes of a single volume, passing a custom infos dict 
            is recommended over passing an iterable rows argument.

        """
        # --- Load data
        kwargs = self.prepare_next_array(split=split, cohort=cohort, row=row, rows=rows, infos=infos, db=db)
        arrays = self.load(infos=infos, db=db, **kwargs)

        # --- Process 
        arrays = self.augment(arrays, test=test, warp_gen=warp_gen, use_cupy=use_cupy, _nested_call=_nested_call, **kwargs)
        arrays = self.preprocess(arrays, test=test, use_cupy=use_cupy, _nested_call=_nested_call, **kwargs)
        arrays = self.arrs_to_numpy(arrays, **kwargs)
        arrays = self.normalize(arrays, test=test, use_cupy=use_cupy, _nested_call=_nested_call, **kwargs)

        # --- Ensure that spec matches
        for k in ['xs', 'ys']:
            for key in arrays[k]:
                shape = self.specs[k][key]['shape']['input']

                # --- Modify shapes for index-type loading
                if kwargs['index'] is not None:
                    shape = [-1] + shape

                # --- Modify shapes for index-type loading
                if infos is not None:
                    shape = arrays[k][key].shape

                # --- Modify shape (if possible)
                try:
                    arrays[k][key] = arrays[k][key].reshape(shape)
                except: pass

                # --- Modify dtype (delete reference to old array for CuPy-safe operation)
                dtype = self.specs[k][key]['dtype']
                if not (flexible_dtype and (dtype[0] == arrays[k][key].dtype.kind)):
                    new_array = arrays[k][key].astype(dtype)
                    arrays[k][key] = None
                    arrays[k][key] = new_array 

        return arrays

    def arrs_to_numpy(self, arrays, **kwargs):
        """
        Method to convert arrays to Numpy (if alternate load function is provided)

        """
        for k in ['xs', 'ys']:
            for key in arrays[k]:
                if hasattr(arrays[k][key], 'to_numpy'):
                    arrays[k][key] = arrays[k][key].to_numpy()

        return arrays

    def augment(self, arrays, test, **kwargs):
        """
        Method to add custom data augmentation algorithms to data

        """
        if self.daug_func is not None and kwargs.get('indices', None) is None and not test:
            arrays = self.daug_func(arrays, self.specs, **kwargs)

        return arrays

    def preprocess(self, arrays, **kwargs): 
        """
        Method to add custom preprocessing algorithms to data

        """
        if self.prep_func is not None:
            arrays = self.prep_func(arrays, self.specs, **kwargs)

        return arrays

    def create_random_crops(self, arrays, N, xs=None, ys=None, mask=None, shape=None, constant_values=0, **kwargs):
        """
        Method to create N random crops from source data

        """
        xs = xs or list(arrays['xs'].keys())
        ys = ys or list(arrays['ys'].keys())

        src_shape = np.array(arrays['xs'][xs[0]].shape[:3])
        dst_shape = np.array(shape or self.specs['xs'][xs[0]]['shape']['input'][:3])
        Z, Y, X = dst_shape
        Z0, Y0, X0 = np.ceil(dst_shape / 2).astype('int')

        xs = [x for x in xs if arrays['xs'][x].shape[:3] == tuple(src_shape)]
        ys = [y for y in ys if arrays['ys'][y].shape[:3] == tuple(src_shape)]
        xs = {k: [] for k in xs}
        ys = {k: [] for k in ys}

        # --- Pad inputs
        pad = lambda x, c=constant_values : np.pad(x, ((Z0, Z0), (Y0, Y0), (X0, X0), (0, 0)), constant_values=c)
        padded = {}
        padded['xs'] = {k: pad(arrays['xs'][k]) for k in xs}
        padded['ys'] = {k: pad(arrays['ys'][k]) for k in ys}

        # --- Find sampling mask
        if mask is None:
            mask = np.ones(src_shape, dtype='bool')
        if not mask.any():
            mask[:] = True
        if mask.ndim == 3:
            mask = np.expand_dims(mask, axis=-1)
        mask = pad(mask, c=0) 

        Zs, Ys, Xs, _ = np.nonzero(mask)
        p = np.random.permutation(len(Zs))
        if p.size < N:
            p = np.concatenate([p] * (int(N / p.size) + 1))

        for i in p[:N]:

            # --- Find random offsets
            z = Zs[i] - Z0 + 1
            y = Ys[i] - Y0 + 1
            x = Xs[i] - X0 + 1

            # --- Crop
            for k in xs:
                xs[k].append(padded['xs'][k][z:z+Z, y:y+Y, x:x+X])

            for k in ys:
                ys[k].append(padded['ys'][k][z:z+Z, y:y+Y, x:x+X])

        # --- Stack
        arrs = {}
        arrs['xs'] = {k: np.stack(v) for k, v in xs.items()}
        arrs['ys'] = {k: np.stack(v) for k, v in ys.items()}

        return arrs

    def normalize(self, arrays, row, test, **kwargs):
        """
        Method to normalize data based on self.specs['norms'] 

        arr = (arr.clip(min, max) - shift) / scale

        There three methods for defining parameters in *.yml file:

          (1) shift: 64      ==> use raw value if provided
          (2) shift: 'mu'    ==> use corresponding column in DataFrame
          (3) shift: '@mean' ==> use corresponding Numpy function

        """
        for a in ['xs', 'ys']:
            for key, specs in self.specs[a].items():
                if specs['norms'] is not None:
                    norms = self.extract_norm_kwargs(row, arrays[a][key], specs['norms'], **kwargs)
                    arrays[a][key] = self.perform_norm(arrays[a][key], test=test, dtype=specs['dtype'], **norms, **kwargs)

        return arrays

    @cupy_compatible
    def extract_norm_kwargs(self, row, arr, norms, np=np, **kwargs):

        extract = lambda x, row, arr : row[x] if x[0] != '@' else getattr(np, x[1:])(arr)

        return {k: extract(v, row, arr) if type(v) is str else v for k, v in norms.items()}

    @cupy_compatible
    def perform_norm(self, arr, clip=None, shift=None, scale=None, rands=None, mapping=None, test=False, np=np, dtype='float32', **kwargs):
        """
        Method to apply provided normalization

        :params

          (bool) test : if True, do not perform random normalizations

        """
        if mapping is not None:
            arr = self.map_array(arr, mapping, **kwargs)

        if test:
            rands = None

        if clip is not None:
            arr = np.clip(arr, out=arr, **clip)

        if rands is not None:
            if 'scale' in rands:
                scale *= self.random_float(**rands['scale']) 
            if 'shift' in rands:
                shift *= self.random_float(**rands['shift']) 

        if shift is not None:
            if arr.dtype == 'uint8':
                arr_ = arr.astype(dtype)
                arr_ = arr_ - shift
            else:
                arr_ = arr - shift 
            arr = None
            arr = arr_

        if scale is not None:
            arr_ = arr / scale 
            arr = None
            arr = arr_

        return arr

    @cupy_compatible
    def random_float(self, lower=1.0, upper=1.0, np=np, **kwargs):

        return np.random.rand() * (upper - lower) + lower 

    @cupy_compatible
    def map_array(self, arr, mapping, np=np, **kwargs):
        """
        Method to map values in array

        NOTE: only values in mapping dict will be propogated

        """
        arr_ = np.zeros(arr.shape, dtype='float32')

        for k, v in mapping.items():
            arr_[arr == k] = v

        del arr

        return arr_

    def test(self, n=None, split=None, cohort=None, aggregate=False, **kwargs):
        """
        Method to test self.get() method

        :params

          (int) n     : number of iterations; if None, then all rows
          (int) lower : lower bounds of row to load
          (int) upper : upper bounds of row to load

        """
        if aggregate:
            keys = lambda x : {k: [] for k in self.specs[x]}
            arrs = {'xs': keys('xs'), 'ys': keys('ys')} 

        # --- Iterate
        for i in range(n):

            printp('Loading iteration: {:06d}'.format(i), (i + 1) / n)
            arrays = self.get(split=split, cohort=cohort, **kwargs)

            if aggregate:
                for k in arrays:
                    for key in arrs[k]:
                        arrs[k][key].append(arrays[k][key][int(arrays[k][key].shape[0] / 2)])

        printd('Completed {} self.get() iterations successfully'.format(n), ljust=140)

        if aggregate:
            stack = lambda x : {k: np.stack(v) for k, v in x.items()}
            return {'xs': stack(arrs['xs']), 'ys': stack(arrs['ys'])}

    def montage(self, xs, ys=None, N=5, n=None, split=None, cohort=None, func=None, **kwargs):
        """
        Method to load montage of self.get() arrs 

        """
        n = n or N ** 2

        # --- Aggregate
        dats, lbls = [], []

        for i in range(n):

            printp('Loading iteration: {:06d}'.format(i), (i + 1) / n)
            arrays = self.get(split=split, cohort=cohort, **kwargs)

            dats.append(arrays['xs'][xs])

            if ys is not None:
                lbls.append(arrays['ys'][ys])

                # --- Apply label conversion and slice extraction function
                if func is not None:
                    dats[-1], lbls[-1] = func(dat=arrays['xs'][xs], lbl=arrays['ys'][ys], **kwargs)

        # --- Interleave dats
        dats = interleave(np.stack(dats), N=N)

        # --- Interleave lbls
        if ys is not None:
            lbls = interleave(np.stack(lbls), N=N)

        return dats, lbls

    def generator(self, split, batch_size=None, xs_only=False, **kwargs):
        """
        Method to wrap the self.get() method in a Python generator for training input

        """
        batch_size = batch_size or self.batch['size']
        if batch_size is None:
            printd('ERROR batch size must be provided if not already set')

        # --- Define efficient reshape and restack methods
        reshape = lambda x, arrs, k : x.reshape([-1] + self.specs[arrs][k]['shape']['input'])
        restack = lambda xs, k : np.stack([x[k] for x in xs]) if len(xs) > 1 else xs[0][k]

        while True:

            xs = []
            ys = []

            for i in range(batch_size):

                arrays = self.get(split=split, **kwargs) 
                xs.append(arrays['xs'])
                ys.append(arrays['ys'])

            xs = {k: reshape(restack(xs, k), 'xs', k) for k in self.specs['xs'] if self.specs['xs'][k]['input']}
            ys = {k: reshape(restack(ys, k), 'ys', k) for k in self.specs['ys'] if self.specs['ys'][k]['input']}

            if xs_only:
                xs.update(ys)
                ys = {}

            yield xs, ys

    def generator_test(self, split, cohorts=None, expand=False, xs_only=False, **kwargs):

        # --- Determine cohorts
        if type(cohorts) is str:
            cohorts = [cohorts]
        cohorts = cohorts or self.indices[split].keys()

        # --- Determine indices from cohorts
        indices = np.concatenate([self.indices[split][c] for c in cohorts])
        indices = np.sort(indices)

        # --- Create temporary new database
        db = self.db.new_db('single-pass-{}'.format(split), 
            fnames=self.db.fnames, 
            header=self.db.header)
        db.load_expanded_fnames()
        db.fnames.index = np.arange(db.fnames.shape[0])
        db.header.index = np.arange(db.header.shape[0])

        # --- Determine if drop_duplicates based on self.specs['tiles']
        drop_duplicates = any(self.specs['tiles']) or expand 
        subset = self.fnames_to_load() if drop_duplicates else None

        # --- Infer infos if needed
        if drop_duplicates:
            infos = {'point': [0.5, 0.5, 0.5]}
            shape = list(self.specs['xs'].values())[0]['shape']['saved']
            infos['shape'] = [1 - s if t else 0 for s, t in zip(shape[:3], self.specs['tiles'])]
        else:
            infos = None

        for sid, fnames, header in db.cursor(indices=indices, drop_duplicates=drop_duplicates, subset=subset, use_cache=False, **kwargs):

            arrays = self.get(row=sid, infos=infos, test=True, db=db)

            arrays['xs'] = {k: np.expand_dims(v, axis=0) for k, v in arrays['xs'].items()}
            arrays['ys'] = {k: np.expand_dims(v, axis=0) for k, v in arrays['ys'].items()}

            if xs_only:
                arrays['xs'].update(arrays['ys'])
                arrays['ys'] = {}

            yield arrays['xs'], arrays['ys']

    def create_generators(self, test=False, **kwargs):

        if test:
            gen_train = self.generator_test('train', **kwargs)
            gen_valid = self.generator_test('valid', **kwargs)

        else:
            gen_train = self.generator('train', **kwargs)
            gen_valid = self.generator('valid', **kwargs)

        return gen_train, gen_valid

class WarpClient(Client):

    def init_client_custom(self, create_warp=None, warp_kwargs={}, warp_count=1, warp_key='wrp', *args, **kwargs):

        # --- Initialize warp function and kwargs
        self.warp_func = create_warp
        self.warp_kwargs = warp_kwargs

        # --- Initialize empty default DB()
        self.init_warp_db(warp_count=warp_count, warp_key=warp_key, **kwargs)

        # --- Initialize warp key
        self.warp_key = sorted(self.specs['xs'].keys())[0]

        self.batch['fold'] = -1

    def init_warp_db(self, warp_count=1, warp_key='wrp', project_id='warp', prefix=None, sform=None, **kwargs):

        # --- Init warp_key and specs 
        self.warp_key = warp_key
        if 'shape' in self.warp_kwargs:
            self.specs['xs'][warp_key] = {
                'dtype': 'float16',
                'loads': self.warp_key,
                'shape': [3] + self.warp_kwargs['shape']}
            self.set_specs()
        self.specs['load_kwargs']['verbose'] = False

        # --- Set client id
        if self._id['project'] is None:
            self._id['project'] = project_id

        if self.db.fnames.size > 0:
            return

        def try_db(**kwargs):

            try:
                self.db = DB(**kwargs)
            except:
                pass

        # --- (1) Load existing DB
        try_db(
            project_id=project_id,
            prefix=prefix or 'db-all-{}'.format(self.init_warp_subdir('-')))

        if self.db.fnames.size > 0:
            return

        # --- (2) Load default DB
        fnames = pd.DataFrame(index=['w{:05d}'.format(n) for n in range(warp_count)])
        fnames[warp_key] = ''

        try_db(
            project_id=project_id,
            prefix=prefix or 'db-all-{}'.format(self.init_warp_subdir('-')),
            fnames=fnames, 
            sform=sform or self.init_warp_sform(), **kwargs)

        if self.db.fnames.size > 0:
            return

        # --- (3) Load default DB without project_id
        try_db(fnames=fnames, **kwargs)
        printd('ERROR please set warp project_id in Jarvis paths.yml')

    def init_warp_subdir(self, token='_'):
        """
        Method to attempt reasonable subdir generation from self.warp_kwargs

        """
        to_list = lambda x : list(x) if type(x) in [list, tuple] else list([x])
        path = [to_list(self.warp_kwargs[key]) for key in sorted(self.warp_kwargs.keys())[::-1]]
        path = [p for p_ in path for p in p_]

        return token.join(['{:03d}'.format(p) if type(p) is int else str(p).replace('.', 'f') for p in path])

    def init_warp_sform(self):

        return {self.warp_key: '{root}/proc/%s/{sid}/%s.hdf5' % (self.init_warp_subdir(), self.warp_key)}

    def init_empty_fnames(self, **kwargs):

        return self.warp_func(**{**kwargs, **self.warp_kwargs})

    def preprocess(self, arrays, **kwargs):

        return arrays

    def generator(self, nCr=3, **kwargs):
        
        while True:

            disp = self.get(split='train', return_numpy=False, **kwargs)['xs'][self.warp_key]
            for _ in range(nCr - 1):
                disp += self.get(split='train', return_numpy=False, **kwargs)['xs'][self.warp_key]

            yield disp

    def create_all_warps(self, warp_count=None, warp_key=None, load=None, **kwargs):

        if load is not None:
            self.load_func = load

        if (warp_count or warp_key) is not None:
            self.init_warp_db(
                warp_count=(warp_count or self.warp_count), 
                warp_key=(warp_key or self.warp_key), **kwargs)

        self.db.create_column(col=self.warp_key, fdefs=[{
            'lambda': lambda : {self.warp_key: self.load_func(data=self.warp_func(**self.warp_kwargs))},
            'kwargs': {},
            'return': {}
            }], **kwargs)

        self.db.to_yml()
