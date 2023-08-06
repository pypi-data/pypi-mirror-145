import os

import numpy as np
import pandas as pd
import tensorflow
from joblib import Parallel, delayed
from tqdm import tqdm

from useckit import AutoEvaluator


class AutoAuthenticator(AutoEvaluator):
    def __init__(self,
                 x_train: np.ndarray,  # training data (mandatory)
                 y_train: np.ndarray,  # training labels (mandatory)
                 x_val: np.ndarray,  # validation data (mandatory)
                 y_val: np.ndarray,  # validation labels (mandatory)
                 nb_classes: int,  # number of classes (mandatory)
                 unknown_set: set,  # set of integers with classes that are excluded i.e., unknown identities
                 model=None,
                 epochs=100,
                 ):
        super().__init__(x_train, y_train, x_val, y_val, nb_classes)

        self.epochs = epochs

        self.UNKNOWN_SET = unknown_set if unknown_set is None else set()
        self.KNOWN_SET = set()
        for i in range(nb_classes):
            self.KNOWN_SET.add(i)
        self.KNOWN_SET = self.KNOWN_SET.difference(self.UNKNOWN_SET)

        self.MODELS_HAVE_TRAINED = False
        self.user_model = model

        self.AUTOENCODERS = dict()
        for i in range(nb_classes):
            self.AUTOENCODERS.update({i: None})

    def _get_mae(self, a: np.ndarray, b: np.ndarray):
        """Calculates the mean absolute error (MAE) between a and b."""
        from sklearn.metrics import mean_absolute_error
        # return np.mean(np.abs(a - b))
        return mean_absolute_error(a, b)

    def _get_mse(self, a: np.ndarray, b: np.ndarray):
        """Performs MSE calculation for a single value, returns only one value"""
        #from sklearn.metrics import mean_squared_error
        return np.sqrt(((a - b)**2).mean())

    def _make_model(self):
        from tensorflow.keras import Sequential
        from tensorflow.keras import layers

        # total values per sample, i.e., shape of (3, 1200,) = 3*1200 = 3600
        params = np.prod(np.array(self.input_shape))

        if self.user_model is None:
            model = Sequential()
            model.add(layers.Dense(50, activation='relu', input_shape=self.input_shape))
            model.add(layers.Flatten())
            model.add(layers.Dense(params, activation='sigmoid'))
            model.add(layers.Reshape(self.input_shape))
            model.build(input_shape=self.input_shape)
            model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc', 'mse'])
            return model
        else:
            clone = tensorflow.keras.models.clone_model(self.user_model)
            clone.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc', 'mse'])
            return clone

    def set_model(self, model):
        self.user_model = model

    def reset_state(self) -> None:
        for i in range(self.nb_classes):
            self.AUTOENCODERS[i] = None
        self.MODELS_HAVE_TRAINED = False

    def fit(self) -> None:
        self.reset_state()

        for i in range(self.nb_classes):
            # find the elements in the training data that belong to class `i`
            # the `y_train` consists of one hot encoded arrays
            # here we apply np.argmax to get the integer-encoding per array and then compare it with i, resulting
            # in a mask of bools that we can use as an indexer for a local array `x_train` (note the missing 'self.'.).
            training_indexes = np.argmax(self.y_train, axis=1) == i
            x_train = self.x_train[training_indexes]

            model = self._make_model()

            print('++ Fitting AE', i, '/', self.nb_classes - 1, '++')

            history = model.fit(
                x_train,
                x_train,
                verbose=2,
                epochs=self.epochs,
                callbacks=[
                    tensorflow.keras.callbacks.EarlyStopping(monitor="mse",
                                                             patience=25,
                                                             mode="min",
                                                             restore_best_weights=True)
                ],
            )

            preds = model.predict(x_train)
            mse_list = []

            assert len(preds) == len(x_train)
            for pred, x in zip(preds, x_train):
                mse_list.append(self._get_mse(pred, x))

            # store model in internal array
            self.AUTOENCODERS[i] = {'model': model,
                                    'history': history,
                                    'training_data': x_train,
                                    'mse_list': mse_list,
                                    'training_max_mse_threshold': max(mse_list)}
            self.MODELS_HAVE_TRAINED = True

    def _determine_distances_to_cluster_border(self, sample: np.ndarray):
        possible_matches = []
        for i in range(self.nb_classes):
            model = self.AUTOENCODERS[i]['model']
            class_threshold = self.AUTOENCODERS[i]['training_max_mse_threshold']

            pred = model.predict(np.array([sample]))
            pred_mse = self._get_mse(pred, sample)

            distance = pred_mse - class_threshold
            possible_matches.append(distance)
            possible_matches.append(distance * -1)
            possible_matches.append(np.nextafter(distance, 1))
            possible_matches.append(np.nextafter(distance, -1))
            possible_matches.append(np.nextafter(distance * -1, 1))
            possible_matches.append(np.nextafter(distance * -1, -1))
        return possible_matches

    def _check_sample_against_all_autoencoders(self, sample: np.ndarray, t: int = 0, impl: int = 1):
        assert len(sample.shape) == 2, str(sample.shape)

        possible_matches = []

        for i in range(self.nb_classes):
            model = self.AUTOENCODERS[i]['model']
            class_threshold = self.AUTOENCODERS[i]['training_max_mse_threshold']

            pred = model.predict(np.array([sample]))
            pred_mse = self._get_mse(pred, sample)

            if pred_mse + t <= class_threshold:
                possible_matches.append({'class': i, 'pred_mse': pred_mse, 'class_threshold': class_threshold})

        if len(possible_matches) == 0:
            return False, None, None  # reject as negative
        elif len(possible_matches) == 1:
            return True, possible_matches[0]['class'], possible_matches
        elif len(possible_matches) > 1:
            # impl == 1: sort by mse and return first element with smallest error.
            # impl == 2: sort by maximum reversed distance between pred_mse and class_threshold
            assert impl in {1, 2}
            if impl == 1:
                possible_matches = sorted(possible_matches, key=lambda k: k['pred_mse'])
            elif impl == 2:
                possible_matches = sorted(possible_matches, key=lambda k: abs(k['class_threshold'] - k['pred_mse']),
                                          reverse=True)
            return True, possible_matches[0]['class'], possible_matches

    def ohc2class(self, ohc):
        return np.argmax(ohc, axis=1)[0]

    def _do_eval(self, t, x_val, y_val):
        tp = fp = tn = fn = 0
        for x_val_sample, label_ohc in zip(x_val, y_val):
            label = np.argmax(label_ohc)
            accept, predicted_class_nb, info = self._check_sample_against_all_autoencoders(x_val_sample, t=t)
            if accept:
                if predicted_class_nb == label:
                    tp += 1
                else:
                    fp += 1
            else:  # reject
                if predicted_class_nb in self.UNKNOWN_SET:
                    tn += 1
                else:
                    fn += 1
        return {'t': t, 'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn}

    def _do_eval_vec(self, possible_thresholds, x_val, y_val):
        assert len(x_val) == len(y_val)
        tp = fp = tn = fn = 0
        possible_matches = []

        print('Predicting thresholds ...')
        for i in tqdm(range(self.nb_classes)):  # for all existing classes / autoencoders
            model = self.AUTOENCODERS[i]['model']

            pred = model.predict(x_val)
            pred_mse = np.square(pred - x_val).mean(axis=1).mean(axis=1)  # calc vectorized mse
            # pred_rmse = np.sqrt(pred_mse)

            possible_matches.append({'ae_class': [i]*len(x_val),
                                     'pred_mse': pred_mse,
                                     'y_val': y_val,
                                     'x_val_id': list(range(len(x_val)))})

        df = pd.DataFrame(possible_matches)
        df = df.apply(pd.Series.explode).reset_index(drop=True)  # factorizes lists into rows
        df['ground_truth'] = df['y_val'].apply(np.argmax)

        print('Testing thresholds ...')

        def tester(threshold, autoencoders):
            t = threshold
            tp, fp, fn, tn = 0, 0, 0, 0

            for id in df['x_val_id'].unique():  # determine closest ae for all samples
                min_mse = df.loc[df.x_val_id == id].pred_mse.min()
                closest_ae_df = df.loc[(df.x_val_id == id) & (df.pred_mse == min_mse)]
                closest_ae = closest_ae_df.ae_class.values[0]
                assert len(closest_ae_df) == 1, 'Multiple same closest distances exist!'
                ground_truth = closest_ae_df.ground_truth.values[0]

                #print(f'Predicted for sample with id {id} the class {closest_ae} (ground truth: {ground_truth}).')

                predicted_class = closest_ae
                true_class = ground_truth
                minimum_threshold = autoencoders[predicted_class]['training_max_mse_threshold']

                accept: bool = (min_mse+t <= minimum_threshold)
                reject: bool = (min_mse+t > minimum_threshold)
                correct_prediction: bool = (predicted_class == true_class)
                wrong_prediction: bool = (predicted_class != true_class)

                # sanity check variable to see if we actually increase something in the if/elif/else below
                sum_pre = (tp+fp+fn+tn)

                if accept:  # ACCEPT (POSITIVE)
                    if correct_prediction:  # CORRECT PRED
                        tp += 1
                    elif wrong_prediction:  # WRONG PRED
                        fp += 1
                elif reject:  # REJECT (NEGATIVE)
                    if correct_prediction:  # CORRECT PRED:
                        fn += 1
                    elif wrong_prediction:  # WRONG PRED
                        tn += 1

                # sanity check if really some increase happened in the if/elif/else above
                sum_post = (tp+fp+fn+tn)
                assert sum_post == (sum_pre + 1)

            return {'t': t, 'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn}

        # create shallow copy of autoencoders due to pickling errors
        autoencoders = {}
        for key in self.AUTOENCODERS.keys():
            autoencoders.update({key: {'training_max_mse_threshold': self.AUTOENCODERS[key]['training_max_mse_threshold']}})

        evaluation_lst = Parallel(n_jobs=os.cpu_count())(delayed(tester)(t, autoencoders.copy()) for t in possible_thresholds)
        # evaluation_lst_flat = [item for sublist in evaluation_lst for item in sublist]

        results_df = pd.DataFrame(evaluation_lst)
        results_df['acc'] = (results_df['tp'] + results_df['tn']) / \
                            (results_df['tp'] + results_df['fp'] + results_df['tn'] + results_df['fn'])
        results_df['tpr'] = results_df['tp'] / (results_df['tp'] + results_df['fn'])
        results_df['fpr'] = results_df['fp'] / (results_df['fp'] + results_df['tn'])
        results_df['tnr'] = results_df['tn'] / (results_df['tn'] + results_df['fp'])
        results_df['fnr'] = results_df['fn'] / (results_df['fn'] + results_df['tp'])

        return results_df

        """
                for x_val_sample, label_ohc in zip(x_val, y_val):
                    label = np.argmax(label_ohc)
                    accept, predicted_class_nb, info = self._check_sample_against_all_autoencoders(x_val_sample, t=t)
                    if accept:
                        if predicted_class_nb == label:
                            tp += 1
                        else:
                            fp += 1
                    else:  # reject
                        if predicted_class_nb in self.UNKNOWN_SET:
                            tn += 1
                        else:
                            fn += 1
                return {'t': t, 'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn}"""

    def evaluate(self, x_val=None, y_val=None):
        if x_val is None or y_val is None:
            # check that both parameters are given
            assert x_val == y_val
            x_val = self.x_val
            y_val = self.y_val

        self.fit()

        print('Determining thresholds', flush=True)
        possible_thresholds = Parallel(n_jobs=os.cpu_count(), backend='threading') \
            (delayed(self._determine_distances_to_cluster_border) \
            (x_val_sample) for x_val_sample in tqdm(x_val))
        possible_thresholds = [element for sublist in possible_thresholds for element in sublist]
        possible_thresholds.append(0)
        possible_thresholds = sorted(list(set(possible_thresholds)))

        print(f'Determined {len(possible_thresholds)} thresholds.')

        use_multithreading = False
        use_vectorized = True
        print(f'Testing possible thresholds (use_multithreading: {use_multithreading})', flush=True)
        if use_multithreading:
            results_lst = Parallel(n_jobs=os.cpu_count(), backend='threading') \
                          (delayed(self._do_eval)(t, x_val, y_val) for t in tqdm(possible_thresholds))
        elif use_vectorized:
            results_lst = self._do_eval_vec(possible_thresholds, x_val, y_val)
        else:
            results_lst = [self._do_eval(t, x_val, y_val) for t in tqdm(possible_thresholds)]
        return results_lst

    def accept_single_sample(self, sample, threshold) -> bool:
        if not self.MODELS_HAVE_TRAINED:
            self.fit()

        acceptance, best_ae_class, info = self._check_sample_against_all_autoencoders(sample, t=threshold)
        return acceptance

    def accept_samples(self, list_of_samples, threshold) -> list:
        return Parallel(n_jobs=os.cpu_count(), backend='threading') \
               (delayed(self.accept_single_sample)(sample, threshold) for sample in list_of_samples)