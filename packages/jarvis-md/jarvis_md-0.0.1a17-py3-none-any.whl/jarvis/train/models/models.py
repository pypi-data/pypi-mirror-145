import os, glob
import h5py, json
import tensorflow as tf
from tensorflow.keras import layers, callbacks
from ...utils.general import *

# --- Attempt add-on libraries
try:
    import tensorflow_addons as tfa
except:
    tfa = None

# =================================================================
# SAVE / LOAD METHODS
# =================================================================

def load_newest_model(func):

    def wrapper(model=None, *args, **kwargs):

        model, saved = _load_newest_model(model=model, *args, **kwargs)

        KWARGS_TO_REMOVE = [
            'weights_loaded',
            'completed_iterations']

        kwargs = {k: v for k, v in kwargs.items() if k not in KWARGS_TO_REMOVE}

        return func(model=model, saved=saved, **kwargs)

    return wrapper 

def _load_newest_model(output_dir, model=None, compile=True, completed_iterations=0, save_format='h5', graphs=None, **kwargs):

    # --- Find model(s)
    saved = find_models(output_dir, save_format=save_format, **kwargs)

    # --- Check if model is already loaded
    if model.optimizer is not None:
        if model.optimizer.iterations.numpy() > 0:
            return model, saved

    if saved['offset'] > 0:

        printd('Loading existing model: {}'.format(saved['models'][-1]))

        # --- Load complete model
        if model is None:
            model = tf.keras.models.load_model(saved['models'][-1], compile=compile)
            saved['loaded'] = 'complete_model'

        # --- Load weights and optimizer
        else:
            model = load_weights(model, saved, graphs, output_dir, **kwargs)
            model = load_optimizer(model, saved, completed_iterations, **kwargs)
            saved['loaded'] = 'weights_and_optimizer_only'

    return model, saved

def find_models(output_dir, save_format='h5', N=3, **kwargs):
    """
    Method to find Tensorflow SavedModel or HDF5 files in output_dir

    """
    saved = {
        'format': save_format,
        'models': [],
        'params': [],
        'offset': 0,
        'loaded': ''}

    # --- Look for HDF5 files
    if len(glob.glob('{}/hdf5/*.hdf5'.format(output_dir))) > 0:

        saved['format'] = 'h5'
        saved['models'] = find_and_format_models('{}/hdf5/*.hdf5'.format(output_dir), save_format='h5', N=N)
        saved['params'] = saved['models']

    elif len(glob.glob('{}/tf/*'.format(output_dir))) > 0:

        saved['format'] = 'tf'
        saved['models'] = find_and_format_models('{}/tf/*/saved_model.pb'.format(output_dir), save_format='tf', N=N)
        saved['models'] = [os.path.dirname(m) + '/' for m in saved['models']]
        saved['params'] = ['{}variables/variables'.format(m) for m in saved['models']] 
        
    # --- Determine model offset
    if len(saved['models']) > 0:
        saved['offset'] = max([int(find_model_offset(s, saved['format'])) for s in saved['models']]) + 1

    return saved

def find_and_format_models(pattern, save_format, N=3):
    
    matches = sorted(glob.glob(pattern))

    if len(matches) == 0:
        return matches

    # --- Check if naming format is consistent
    if len(find_model_offset(matches[0], save_format)) == N:
        return matches

    # --- Rename all files if naming format is inconsistent
    for src in matches:

        src = os.path.dirname(src) + '/' if save_format == 'tf' else src
        dst = model_name(int(find_model_offset(src, save_format)), output_dir, save_format=save_format)
        os.rename(src=src, dst=dst)

    return sorted(glob.glob(pattern)) 

def find_model_offset(path, save_format='h5'):
    """
    Method to find model offset based of standard naming scheme

      (1) Keras HDF5: hdf5/model_{xxx}.hdf5 
      (2) SavedModel: tf/model_{xxx}/saved_model.pb

    """
    return os.path.basename(path).split('model_')[-1][:-5] if save_format == 'h5' else \
           path.split('/')[-2].split('model_')[-1]

def load_weights(model, saved, graphs=None, output_dir=None, weights_loaded=False, **kwargs):
    """
    Method to load weights into existing Model object 

    Note that the model itself should already be built and compiled already to ensure that
    any custom functions are defined (cannot be serialized in HDF5 format).

    """
    if weights_loaded:
        return model

    # --- Load weights
    try:
        model.load_weights(saved['params'][-1])

    except:
        printd('WARNING model architecture is different than saved path, attemping to load weights from individual graphs')
        assert type(graphs) is dict 
        for k, graph in graphs.items():
            if saved['format'] == 'h5':
                param_path = glob.glob('{}/hdf5/{}/*.hdf5'.format(output_dir, k))
            if saved['format'] == 'tf':
                param_path = glob.glob('{}/tf/{}/*/variables/variables'.format(output_dir, k))
            if len(param_path) > 0:
                param_path = sorted(param_path)[-1]
                printd('Loading weights for graph {}: {}'.format(k, param_path))
                graph.load_weights(param_path)

    return model

def load_optimizer(model, saved, completed_iterations=0, **kwargs):
    """
    Method to load optimizer configurations 

    """
    # --- Load optimizer (HDF5)
    if saved['format'] == 'h5':
        with h5py.File(saved['models'][-1], 'r') as m:
            config = json.loads(m.attrs['training_config'])['optimizer_config']['config']
            completed_iterations = m['optimizer_weights']['iter:0'][()] if 'iter:0' in m['optimizer_weights'] else \
                    list(m['optimizer_weights']['training'].values())[0]['iter:0'][()]
            model.optimizer = model.optimizer.from_config(config)
            model.optimizer.iterations.assign(completed_iterations)

    # --- Load optimizer
    if saved['format'] == 'tf':
        model.optimizer = tf.keras.models.load_model(saved['models'][-1]).optimizer
        model.optimizer.iterations.assign(completed_iterations)

    return model

def model_name(offset, output_dir, subdir='/', save_format='h5'):
    """
    Method to create a model path name based on standard naming scheme

      (1) Keras HDF5: hdf5/{subdir/}model_{xxx}.hdf5 
      (2) SavedModel: tf/{subdir/}model_{xxx}/

    """
    subdir = '{}{}'.format('hdf5', subdir) if save_format == 'h5' else \
             '{}{}'.format('tf', subdir)

    return '{}/{}model_{:03d}.hdf5'.format(output_dir, subdir, offset) if save_format == 'h5' else \
           '{}/{}model_{:03d}/'.format(output_dir, subdir, offset)

def resave(output_dir='./', model=None, fname=None):
    """
    Method to resave model without training / optimizer configurations

    """
    # --- Load existing
    model, saved = _load_newest_model(output_dir, model, compile=False)
    fname = fname or model_name(saved['offset'], output_dir, save_format=saved['format'])

    if model is not None:
        printd('Saving updated model: {}'.format(fname))
        model.save(fname, save_format=saved['format'])

    else:
        printd('ERROR no existing model weights found')

# =================================================================
# TRAIN METHODS
# =================================================================

@load_newest_model
def train(model, saved, client, steps, save_freq=10, output_dir='.', tf_board=True, jmodels=None, graphs=None, **kwargs):
    """
    Wrapper method to run model.fit_generator(...)

      (1) Run 100 steps per epoch (default)
      (2) Run N number of epoch(s) until save_freq is obtained
      (3) Serialize model as *.hdf5
      (4) Repeat until total steps is achieved

    Default parameters for model.fit_generator() function:

      * steps_per_epoch     = 100
      * validation_steps    = 100
      * validation_freq     = 5

    """
    # --- Initialize arguments
    DEFAULTS = {
        'steps_per_epoch': 100,
        'validation_steps': 100,
        'validation_freq': 5,
        'validation_data': None}

    kwargs = {**DEFAULTS, **kwargs}
    kwargs['epochs'] = int(round(steps / kwargs['steps_per_epoch']))

    if kwargs['validation_data'] is None:
        kwargs.pop('validation_steps')
        kwargs.pop('validation_freq')

    # --- Determine number of steps needed to reach goal
    kwargs['initial_epoch'] = int(round(model.optimizer.iterations.numpy() / kwargs['steps_per_epoch']))
    if kwargs['initial_epoch'] >= kwargs['epochs']:
        printd('Training already complete ({} iterations)'.format(model.optimizer.iterations.numpy()))
        return

    # --- Create callbacks
    _callbacks = kwargs.pop('callbacks', [])

    # --- Add tensorboard
    if tf_board:
        jmodels = jmodels or '{}/jmodels'.format(os.path.dirname(output_dir))
        tf_dir = '{}/logdirs/{}'.format(jmodels, os.path.basename(os.path.abspath(output_dir)))
        _callbacks.append(callbacks.TensorBoard(log_dir=tf_dir))

    # --- Create Jarvis model saver
    js = JarvisModelSaver(
        saved=saved,
        client=client, 
        output_dir=output_dir, 
        save_freq=save_freq, 
        graphs=graphs)

    _callbacks.append(js)

    # --- Loop
    model.fit(callbacks=_callbacks, **kwargs)

    # --- Save final model
    js.save()

# =================================================================
# CUSTOM CALLBACK FOR CLIENT AND MODEL SAVE 
# =================================================================

class JarvisModelSaver(callbacks.Callback):

    def __init__(self, saved, client, output_dir, save_freq=5, graphs=None):

        self.saved = saved 
        self.client = client
        self.output_dir = output_dir
        self.save_freq = save_freq
        self.graphs = graphs or {}

        # --- TODO: auto-extract graphs if complete model is loaded
        if saved['loaded'] == 'complete_model' and len(graphs) > 0:
            printd('WARNING passed graphs are not linked to model loaded with keras.models.load_model(...) and will not be saved')
            self.graphs = {}

        # --- Prepare model output directory 
        subdir = 'hdf5' if saved['format'] == 'h5' else 'tf'
        os.makedirs('{}/{}'.format(output_dir, subdir), exist_ok=True)

        for k, graph in self.graphs.items():
            if graph is not None:
                os.makedirs('{}/{}/{}'.format(output_dir, subdir, k), exist_ok=True)

    def on_epoch_end(self, epoch, logs=None, **kwargs):

        if not epoch % self.save_freq:
            self.save()

    def save(self):

        # --- Save client
        self.client.to_yml('{}/client.yml'.format(self.output_dir))

        # --- Save model
        try:
            self.model.save(model_name(self.saved['offset'], self.output_dir, save_format=self.saved['format']))
        except:
            save_format = 'h5' if self.saved['format'] == 'tf' else 'tf'
            self.model.save(model_name(self.saved['offset'], self.output_dir, save_format=save_format))

        # --- Save subgraphs
        for k, graph in self.graphs.items():
            if graph is not None:
                graph.save(model_name(self.saved['offset'], self.output_dir, subdir='/{}/'.format(k), save_format=self.saved['format']))

        self.saved['offset'] += 1

# =================================================================
# MODEL BUILDING METHODS
# =================================================================

def create_block_components(names=None, dims=2, kernel_size=3, dilation_rate=1, leaky_relu=True, se_net=False, gn=False, groups=8, ws=False, **kwargs):

    kernel_size = (1, kernel_size, kernel_size) if dims == 2 else (kernel_size, kernel_size, kernel_size)
    dilation_rate = (1, dilation_rate, dilation_rate) if dims == 2 else (dilation_rate, dilation_rate, dilation_rate)

    # --- padding == same, z-size == 1
    kwargs_z1 = {
        'kernel_size': kernel_size,
        'dilation_rate': dilation_rate,
        'padding': 'same',
        'kernel_initializer': 'he_normal'}

    # --- padding = valid, z-size == 2
    kwargs_z2 = {
        'kernel_size': (2, 1, 1),
        'dilation_rate': dilation_rate,
        'padding': 'valid',
        'kernel_initializer': 'he_normal'}

    # --- padding = valid, z-size == 2
    kwargs_z3 = {
        'kernel_size': (3, 1, 1),
        'dilation_rate': dilation_rate,
        'padding': 'valid',
        'kernel_initializer': 'he_normal'}

    # --- padding = same, z-size = 1, filters = 1
    kwargs_f1 = {
        'kernel_size': (1, 1, 1),
        'padding': 'same',
        'kernel_initializer': 'he_normal'}

    # --- padding = same, z-size = 1, filters = 7
    kwargs_f7 = {
        'kernel_size': (1, 7, 7) if dims == 2 else (7, 7, 7),
        'dilation_rate': dilation_rate,
        'padding': 'same',
        'kernel_initializer': 'he_normal'}

    # --- Weight standardization
    if ws or gn: 
        kwargs_z1['kernel_regularizer'] = create_weight_standardization 
        kwargs_z2['kernel_regularizer'] = create_weight_standardization
        kwargs_z3['kernel_regularizer'] = create_weight_standardization
        kwargs_f1['kernel_regularizer'] = create_weight_standardization
        kwargs_f7['kernel_regularizer'] = create_weight_standardization

    # --- Define block components
    conv_z1 = lambda x, filters, strides : layers.Conv3D(filters=filters, strides=strides, **kwargs_z1)(x)
    conv_z2 = lambda x, filters, strides : layers.Conv3D(filters=filters, strides=strides, **kwargs_z2)(x)
    conv_z3 = lambda x, filters, strides : layers.Conv3D(filters=filters, strides=strides, **kwargs_z3)(x)
    conv_f1 = lambda x, filters, strides : layers.Conv3D(filters=filters, strides=strides, **kwargs_f1)(x)
    conv_f7 = lambda x, filters, strides : layers.Conv3D(filters=filters, strides=strides, **kwargs_f7)(x)
    tran_z1 = lambda x, filters, strides : layers.Conv3DTranspose(filters=filters, strides=strides, **kwargs_z1)(x)
    conv_fc = lambda x, filters : layers.Conv3D(filters=filters, **kwargs_f1)(x)

    norm = lambda x : layers.BatchNormalization()(x)
    relu = lambda x : layers.LeakyReLU()(x) if leaky_relu else layers.ReLU()(x)

    # --- Group Normalization
    if gn:
        if tfa is None:
            printd('ERROR GroupNormalization() requires Tensorflow-Addon which is not available; regular BatchNormalization() is used instead')
        else:
            norm = lambda x : tfa.layers.GroupNormalization(groups=groups)(x)

    # --- Modify for SE-Net (append to all ReLU activation functions)
    if se_net:
        relu = lambda x : create_se(layers.LeakyReLU()(x) if leaky_relu else layers.ReLU()(x), **kwargs)

    concat = lambda *x : layers.Concatenate()(list(x))

    # --- Return local vars
    names = names or ('conv_z1', 'conv_z2', 'conv_z3', 'conv_f1', 'conv_f7', 'tran_z1', 'conv_fc', 'norm', 'relu', 'concat')
    lvars = locals()

    return [lvars.get(n) for n in names] 

def create_blocks(names=None, dims=2, strides=None, **kwargs):
    """
    Method to create standard (Conv-BN-ReLU) blocks

    """
    # --- Create components
    conv_z1, conv_z2, conv_z3, conv_f1, conv_f7, tran_z1, conv_fc, norm, relu, concat = create_block_components(names=None, dims=dims, **kwargs)

    # --- Define stride-1, stride-2 blocks
    if strides is None:
        strides = (1, 2, 2) if dims == 2 else (2, 2, 2)

    conv1 = lambda filters, x : relu(norm(conv_z1(x, filters, strides=1)))
    conv7 = lambda filters, x : relu(norm(conv_f7(x, filters, strides=1)))
    bneck = lambda filters, x : relu(norm(conv_f1(x, filters, strides=1)))
    convZ = lambda filters, x : relu(norm(conv_z2(x, filters, strides=1)))
    conv2 = lambda filters, x : relu(norm(conv_z1(x, filters, strides=strides)))
    tran2 = lambda filters, x : relu(norm(tran_z1(x, filters, strides=strides)))

    proj2 = lambda filters, x : conv_z2(x, filters, strides=1)
    proj3 = lambda filters, x : conv_z3(x, filters, strides=1)

    # --- Return local vars
    names = names or ('conv1', 'conv7', 'bneck', 'convZ', 'conv2', 'tran2', 'proj2', 'proj3')
    lvars = locals()

    return [lvars.get(n) for n in names] 

def create_blocks_preactivation(names=None, dims=2, strides=None, **kwargs):
    """
    Method to create full preactivation (BN-ReLU-Conv) blocks popularized by ResNet / DenseNet

    """
    # --- Create components
    conv_z1, conv_z2, conv_z3, conv_f1, conv_f7, tran_z1, conv_fc, norm, relu, concat = create_block_components(names=None, dims=dims, **kwargs)

    # --- Define stride-1, stride-2 blocks
    if strides is None:
        strides = (1, 2, 2) if dims == 2 else (2, 2, 2)

    conv1 = lambda filters, x : conv_z1(relu(norm(x)), filters, strides=1) 
    conv7 = lambda filters, x : conv_f7(relu(norm(x)), filters, strides=1) 
    bneck = lambda filters, x : conv_f1(relu(norm(x)), filters, strides=1)
    convZ = lambda filters, x : conv_z2(relu(norm(x)), filters, strides=1) 
    conv2 = lambda filters, x : conv_z1(relu(norm(x)), filters, strides=strides) 
    tran2 = lambda filters, x : tran_z1(relu(norm(x)), filters, strides=strides) 

    proj2 = lambda filters, x : conv_z2(x, filters, strides=1)
    proj3 = lambda filters, x : conv_z3(x, filters, strides=1)

    # --- Return local vars
    names = names or ('conv1', 'conv7', 'bneck', 'convZ', 'conv2', 'tran2', 'proj2', 'proj3')
    lvars = locals()

    return [lvars.get(n) for n in names] 

def create_blocks_sampling(names=None, dims=2, strides=None):
    """
    Method to create pooling and upsampling blocks

    """
    # --- Define stride-1, stride-2 blocks
    if strides is None:
        strides = (1, 2, 2) if dims == 2 else (2, 2, 2)

    # --- Define average pool 
    pool = lambda x : layers.AveragePooling3D(
        pool_size=strides,
        strides=strides,
        padding='same')(x)

    # --- Define upsample 
    zoom = lambda x : layers.UpSampling3D(
        size=strides)(x)

    # --- Return local vars
    names = names or ('pool', 'zoom')
    lvars = locals()

    return [lvars.get(n) for n in names] 

def create_weight_standardization(kernel):
    """
    Method to apply weight standardization to 2D kernel

    """
    axis = (0, 1, 2) if len(kernel.shape) == 4 else (0, 1, 2, 3)

    mu = tf.math.reduce_mean(kernel, axis=axis, keepdims=True)
    sd = tf.math.reduce_std(kernel, axis=axis, keepdims=True)

    kernel = tf.math.divide_no_nan(kernel - mu, sd)

def create_dense_block(x, k=8, n=3, b=8, dims=2, verbose=False):
    """
    Method to create a single dense block:

      (1) Each dense block is composed of a total of `n` single dense layers
      (2) Each single dense layer outputs a total of `k` feature maps
      (3) If the concatenated intermediate feature map > b in size, use bottleneck operation

    :params

      (tf Tensor) x : input into block
      (int)       k : growth factor
      (int)       n : number of convolutions in block
      (int)       b : bottleneck ratio (compress concatenated feature maps to b before conv)

    """
    dense, bneck, concat = create_blocks_preactivation(names=('conv1', 'bneck', 'concat'), dims=dims)

    ds_layer = None

    for i in range(n):

        # --- Concatenate all prior layers
        cc_layer = concat(cc_layer, ds_layer) if ds_layer is not None else x

        # --- Bottleneck if needed
        bn_layer = bneck(b, cc_layer) if cc_layer.shape.as_list()[-1] > b else cc_layer

        # --- Perform dense operation
        ds_layer = dense(k, bn_layer)

        # --- Print
        if verbose:
            print('Creating layer {:02d}: cc_layer = {}'.format(i, cc_layer.shape))
            print('Creating layer {:02d}: bn_layer = {}'.format(i, bn_layer.shape))
            print('Creating layer {:02d}: ds_layer = {}'.format(i, ds_layer.shape))

    return concat(cc_layer, ds_layer)

def create_se(x, r=4, min_features=8, kernel_initializer='he_normal', **kwargs):
    """
    Method to create squeeze-and-excitation module

    :params

      (int) r            : compression ratio
      (int) min_features : min number of features for compression 

    """
    # --- Squeeze (global pool)
    l0 = layers.GlobalAveragePooling3D()(x)

    # --- Excitation (reduce channels to 1 / R)
    f_ = max(int(x.shape[-1] / r), min_features)
    l1 = layers.Dense(f_, activation='relu', kernel_initializer=kernel_initializer)(l0)

    # --- Scale (expand channels to original size)
    l2 = layers.Dense(x.shape[-1], activation='sigmoid', kernel_initializer=kernel_initializer)(l1)
    l2 = layers.Reshape((1, 1, 1, x.shape[-1]))(l2)    

    return x * l2 

def rename_layers(model):
    """
    Method to rename all layers with '/' to '_'

    NOTE: this is needed to serialize as HDF5

    """
    for layer in model.layers:
        if layer.name.find('/') > -1:
            layer._name = layer._name.replace('/', '_')

    return model
