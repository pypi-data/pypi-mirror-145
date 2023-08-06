import pandas as pd
import numpy as np
import os


def unison_shuffle_np_arrays(a: np.ndarray, b: np.ndarray):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]


def unison_shuffle_np_arrays_3(a: np.ndarray, b: np.ndarray, c: np.ndarray):
    assert len(a) == len(b) == len(c)
    p = np.random.permutation(len(a))
    return a[p], b[p], c[p]


def df_describe_nonscientific(df: pd.DataFrame):
    return df.describe().apply(lambda s: s.apply('{0:.5f}'.format))


def create_ohc_labels(labels_array):
    from sklearn.preprocessing import LabelBinarizer
    lb = LabelBinarizer()
    ret = lb.fit_transform(labels_array)
    return ret


def enable_gpu_growth():
    os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'


def force_cpu_training():
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def create_class_weights(y) -> dict:
    assert False, 'Needs testing and fixing.'
    # currently it is expected to receive a list of class labels
    # this should become some numpy array

    from sklearn.utils import class_weight
    class_weights = class_weight.compute_class_weight(class_weight='balanced',
                                                      classes=np.unique(y),
                                                      y=y)
    class_weight_dict = dict(enumerate(class_weights))
    return class_weight_dict

# https://keras.io/examples/timeseries/timeseries_anomaly_detection/