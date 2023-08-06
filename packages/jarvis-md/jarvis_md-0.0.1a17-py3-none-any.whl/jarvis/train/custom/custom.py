import numpy as np
import tensorflow as tf
from tensorflow.keras import losses, metrics, layers, backend

# =================================================================
# DISABLE EAGER EXEC FOR MASKED LOSS FUNCTIONS
# =================================================================

# --- TF2.1
# model.compile(..., experimental_run_tf_function=False)

# --- TF2.2
# NOTES: works however metrics do not calculate
# if tf.__version__[:3] == '2.2':
#     tf.compat.v1.disable_eager_execution()

# =================================================================

# =================================================================
# CUSTOM KERAS LOSSES (LAYERS)
# =================================================================

class CustomLayer(layers.Layer):
    
    def __init__(self, func=None, scale=1.0, name=None, key='', add_loss=True, add_metric=False, metric_aggregate='mean', **kwargs):
        
        super(CustomLayer, self).__init__(name=name)
        self.func = func
        self.scale = scale
        self.key = key
        self._add_loss = add_loss
        self._add_metric = add_metric
        self._metric_aggregate = metric_aggregate

    def call(self, y_true, y_pred, weights=None, **kwargs):

        val = self.func(y_true=y_true, 
            y_pred=y_pred,
            sample_weight=weights) * self.scale

        if self._add_loss:
            self.add_loss(val)

        if self._add_metric:
            self.add_metric(val, name=self.key, aggregation=self._metric_aggregate)
        
        return {self.key: val}

    def get_config(self):

        config = super().get_config().copy()

        config.update({
            'scale': self.scale,
            'key': self.key,
            '_add_loss': self._add_loss,
            '_add_metric': self._add_metric,
            '_metric_aggregate': self._metric_aggregate})

        return config
        
class SCE(CustomLayer):
    
    def __init__(self, key='sce', **kwargs):
        
        super(SCE, self).__init__(
            func=losses.SparseCategoricalCrossentropy(from_logits=True),
            key=key, **kwargs)

class BCE(CustomLayer):
    
    def __init__(self, key='bce', **kwargs):
        
        super(BCE, self).__init__(
            func=losses.BinaryCrossentropy(from_logits=True),
            key=key, **kwargs)

class MSE(CustomLayer):
    
    def __init__(self, key='mse', **kwargs):
        
        super(MSE, self).__init__(
            func=losses.MeanSquaredError(),
            key=key, **kwargs)

class MAE(CustomLayer):
    def __init__(self, key='mae', **kwargs):
        
        super(MAE, self).__init__(
            func=losses.MeanAbsoluteError(),
            key=key, **kwargs)

class Huber(CustomLayer):
    
    def __init__(self, key='sl1', delta=1.0, **kwargs):
        
        super(Huber, self).__init__(
            func=losses.Huber(delta),
            key=key, **kwargs)

class MNE(CustomLayer):
    
    def __init__(self, dims=3, key='mne', **kwargs):
        
        super(MNE, self).__init__(
            func=self.mne,
            key=key, **kwargs)

        self.dims = dims

    def mne(self, y_true, y_pred, sample_weight=None):

        err = tf.math.abs(tf.cast(y_true, tf.float32) - tf.cast(y_pred, tf.float32)) ** self.dims

        return tf.math.reduce_mean(err * sample_weight)

    def get_config(self):

        config = super().get_config().copy()

        config.update({
            'dims': self.dims})

        return config

class DSC(layers.Layer):

    def __init__(self, classes=[1], name=None, key='dsc', metric_aggregate='mean', **kwargs):

        super(DSC, self).__init__(name=name)
        self.key = key
        self.classes = classes
        self._metric_aggregate = metric_aggregate

    def dsc(self, y_true, y_pred, sample_weight=None, cls=1):

        true = y_true[..., 0] == cls

        if y_pred.shape[-1] > 1:
            pred = tf.math.argmax(y_pred, axis=-1) == cls 
        else:
            assert cls == 1, 'ERROR single-element Dice score logit implies a binary prediction task with cls == 1'
            pred = y_pred[..., 0] > 0

        if sample_weight is not None:
            true = true & (sample_weight[..., 0] != 0) 
            pred = pred & (sample_weight[..., 0] != 0)

        A = tf.math.count_nonzero(true & pred) * 2
        B = tf.math.count_nonzero(true) + tf.math.count_nonzero(pred)

        return tf.math.divide_no_nan(
            tf.cast(A, tf.float32), 
            tf.cast(B, tf.float32))

    def call(self, y_true, y_pred, weights, **kwargs):

        dsc = {}

        for cls in self.classes:

            key = '{}_{}'.format(self.key, cls)
            dsc[key] = self.dsc(y_true, y_pred, weights, cls=cls)
            self.add_metric(dsc[key], name=key, aggregation=self._metric_aggregate)

        return dsc

    def get_config(self):

        config = super().get_config().copy()

        config.update({
            'key': self.key,
            'classes': self.classes,
            '_metric_aggregate': self._metric_aggregate})

        return config

# =================================================================
# CUSTOM KERAS LOSSES (LEGACY)
# =================================================================

def bce(weights, scale=1.0):

    loss = losses.BinaryCrossentropy(from_logits=True)

    def bce(y_true, y_pred):

        return loss(y_true=y_true, y_pred=y_pred, sample_weight=weights) * scale

    return bce 

def sce(weights, scale=1.0):

    loss = losses.SparseCategoricalCrossentropy(from_logits=True)

    def sce(y_true, y_pred):

        return loss(y_true=y_true, y_pred=y_pred, sample_weight=weights) * scale

    return sce 

def mse(weights, scale=1.0):

    loss = losses.MeanSquaredError()

    def mse(y_true, y_pred):

        return loss(y_true=y_true, y_pred=y_pred, sample_weight=weights) * scale

    return mse

def mae(weights, scale=1.0):

    loss = losses.MeanAbsoluteError()

    def mae(y_true, y_pred):

        return loss(y_true=y_true, y_pred=y_pred, sample_weight=weights) * scale

    return mae

def mne(weights, scale=1.0, dims=3):

    def mne(y_true, y_pred):

        err = tf.math.abs(y_true - y_pred) ** dims

        return tf.math.reduce_mean(err * weights) * scale

    return mne 

def sl1(weights, scale=1.0, delta=1.0):

    loss = losses.Huber(delta=delta)

    def sl1(y_true, y_pred):

        return loss(
            y_true=tf.expand_dims(y_true, axis=-1), 
            y_pred=tf.expand_dims(y_pred, axis=-1),
            sample_weight=weights) * scale

    return sl1

def dsc(weights=None, scale=1.0, cls=1):
    """
    Method for generalized multi-class (up to 9) Dice score calculation

    :params

      (int) cls : class to use to for Dice score calculation (default = 1)

    """
    def calc_dsc(y_true, y_pred, c):
        """
        Method to calculate Dice coefficient

        """
        true = y_true[..., 0] == c

        if y_pred.shape[-1] > 1:
            pred = tf.math.argmax(y_pred, axis=-1) == c
        else:
            assert c == 1, 'ERROR single-element Dice score logit implies a binary prediction task with cls == 1'
            pred = y_pred[..., 0] > 0

        if weights is not None:
            true = true & (weights[..., 0] != 0) 
            pred = pred & (weights[..., 0] != 0)

        A = tf.math.count_nonzero(true & pred) * 2
        B = tf.math.count_nonzero(true) + tf.math.count_nonzero(pred)

        return tf.math.divide_no_nan(tf.cast(A, tf.float32), tf.cast(B, tf.float32)) * scale

    def dsc_1(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 1) 

    def dsc_2(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 2) 

    def dsc_3(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 3) 

    def dsc_4(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 4) 

    def dsc_5(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 5) 

    def dsc_6(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 6) 

    def dsc_7(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 7) 

    def dsc_8(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 8) 

    def dsc_9(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 9) 

    funcs = {
        1: dsc_1,
        2: dsc_2,
        3: dsc_3,
        4: dsc_4,
        5: dsc_5,
        6: dsc_6,
        7: dsc_7,
        8: dsc_8,
        9: dsc_9}

    assert cls < 10, 'ERROR only up to 9 classes implemented in custom.dsc() currently'

    return [funcs[i] for i in range(1, cls + 1)]

# =================================================================
# CUSTOM KERAS METRICS 
# =================================================================

def acc(weights=None, epsilon=1e-6):
    """
    Method to implement masked accuracy on raw softmax cross-entropy logits

    NOTE: weights tensor is treated as a mask (values binarized)

    """

    def accuracy(y_true, y_pred):

        y_pred = tf.expand_dims(backend.argmax(y_pred), axis=-1)

        y_true = tf.cast(y_true, tf.int64)
        y_pred = tf.cast(y_pred, tf.int64)

        num = y_true == y_pred
        den = y_true > -1

        if weights is not None:
            num = num & (weights != 0) 
            den = den & (weights != 0) 

        num = tf.math.count_nonzero(num)
        den = tf.math.count_nonzero(den)

        num = tf.cast(num, tf.float32)
        den = tf.cast(den, tf.float32) + epsilon

        return num / den

    return accuracy

def softmax_ce_sens(weights=None, threshold=0.5, epsilon=1e-6):
    """
    Method to implement masked sensitivity (recall) on raw softmax cross-entropy logits

    NOTE: weights tensor is treated as a mask (values binarized)

    """
    def softmax_ce_sens(y_true, y_pred):

        p = tf.nn.softmax(y_pred)
        tp = (p[..., 1:] > threshold) & (y_true == 1)

        if weights is not None:
            tp = tp & (weights != 0)
            y_true = (y_true == 1) & (weights != 0)

        num = tf.math.count_nonzero(tp) 
        den = tf.math.count_nonzero(y_true)

        num = tf.cast(num, tf.float32)
        den = tf.cast(den, tf.float32) + epsilon

        return num / den

    return softmax_ce_sens 

def softmax_ce_ppv(weights=None, threshold=0.5, epsilon=1e-6):
    """
    Method to implement masked PPV (precision) on raw softmax cross-entropy logits

    NOTE: weights tensor is treated as a mask (values binarized)

    """
    def softmax_ce_ppv(y_true, y_pred):

        p = tf.nn.softmax(y_pred)
        pp = p[..., 1:] > threshold
        tp = pp & (y_true == 1)

        if type(weights) is not float:
            tp = tp & (weights != 0)
            pp = pp & (weights != 0)

        num = tf.math.count_nonzero(tp) 
        den = tf.math.count_nonzero(pp)

        num = tf.cast(num, tf.float32)
        den = tf.cast(den, tf.float32) + epsilon

        return num / den

    return softmax_ce_ppv

# =================================================================
# CUSTOM SIGMOID CROSS-ENTROPY 
# =================================================================

def focal_sigmoid_ce(weights=1.0, scale=1.0, gamma=2.0, alpha=0.25):
    """
    Method to implement focal sigmoid (binary) cross-entropy loss

    """
    def focal_sigmoid_ce(y_true, y_pred):

        # --- Calculate standard cross entropy with alpha weighting
        loss = tf.nn.weighted_cross_entropy_with_logits(
            labels=y_true, logits=y_pred, pos_weight=alpha)

        # --- Calculate modulation to pos and neg labels 
        p = tf.math.sigmoid(y_pred)
        modulation_pos = (1 - p) ** gamma
        modulation_neg = p ** gamma

        mask = tf.dtypes.cast(y_true, dtype=tf.bool)
        modulation = tf.where(mask, modulation_pos, modulation_neg)

        return tf.math.reduce_mean(modulation * loss * weights * scale)

    return focal_sigmoid_ce

def sigmoid_ce_sens(weights=1.0, threshold=0.5, epsilon=1e-6):
    """
    Method to implement sensitivity (recall) on raw sigmoid (binary) cross-entropy logits

    """
    def sigmoid_ce_sens(y_true, y_pred):

        p = tf.math.sigmoid(y_pred)
        tp = (p > threshold) & (y_true == 1)

        num = tf.math.count_nonzero(tp) 
        den = tf.math.count_nonzero(y_true)

        num = tf.cast(num, tf.float32)
        den = tf.cast(den, tf.float32) + epsilon

        return num / den

    return sigmoid_ce_sens

def sigmoid_ce_ppv(weights=1.0, threshold=0.5, epsilon=1e-6):
    """
    Method to implement PPV (precision) on raw sigmoid (binary) cross-entropy logits

    """
    def sigmoid_ce_ppv(y_true, y_pred):

        p = tf.math.sigmoid(y_pred)
        tp = (p > threshold) & (y_true == 1)

        num = tf.math.count_nonzero(tp) 
        den = tf.math.count_nonzero(p > threshold)

        num = tf.cast(num, tf.float32)
        den = tf.cast(den, tf.float32) + epsilon

        return num / den

    return sigmoid_ce_ppv

# =================================================================
# CUSTOM LAYERS AND FUNCTIONS 
# =================================================================

def flatten(x):
    """
    Method to flatten all defined axes (e.g. not None)

    WARNING: If possible, layers.Flatten(...) is preferred for speed and HDF5 serialization compatibility

    """
    # --- Calculate shape
    ll = x._shape_as_list()
    ss = [s for s in tf.shape(x)]

    shape = []
    adims = []

    for l, s in zip(ll, ss):
        if l is None:
            shape.append(s)
        else:
            shape.append(1)
            adims.append(l)

    shape[-1] = np.prod(adims)

    return tf.reshape(x, shape)

class VAESampling(layers.Layer):
    
    def __init__(self, name=None):

        super(VAESampling, self).__init__(name=name)

    def call(self, inputs):
        """
        Method to sample latent vector z given inputs = (z_mu, z_sd_log)

        :return

          (tf.Tensor) randomly sampled feature vectors of shape (batch_size, fmaps_size)

        """
        z_mu, z_sd_log = inputs

        # --- Create random sampling parameters 
        batch_size = tf.shape(z_mu)[0]
        fmaps_size = tf.shape(z_mu)[-1]
        epsilon = tf.keras.backend.random_normal(shape=(batch_size, fmaps_size))

        # --- Reshape inputs to vectors
        z_mu     = tf.reshape(z_mu,     [batch_size, fmaps_size])
        z_sd_log = tf.reshape(z_sd_log, [batch_size, fmaps_size])

        return z_mu + tf.exp(0.5 * z_sd_log) * epsilon
