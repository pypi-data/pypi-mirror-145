# Copyright (c) 2022 Paul Irofti <paul@irofti.net>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import logging
import multiprocessing
import os
import pickle
import time
from collections.abc import Iterable
from pathlib import Path

import numpy as np
from sklearn.base import clone
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import ParameterGrid
from tensorflow.keras.models import load_model


class GridSearch:
    def __init__(
        self,
        clf,
        params,
        *,
        datadir="results",
        n_cpus=1,
        clf_type="sklearn",
    ):
        self.base_clf = clf
        self.datadir = datadir
        self.n_cpus = n_cpus
        self.clf_type = clf_type

        self.params = params

        self.clf_name = clf.__class__.__name__

        # Results
        self.best_estimator_ = None
        self.best_params_ = None
        self.best_score_ = 0
        self.labels_ = None
        self.estimators_ = []

        logging.basicConfig(level=logging.INFO)

    def fpfn(self, y_pred, y_true):
        if y_true is None:
            return None, None, None, None, None, None, None
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        tpr = tp / (tp + fn)
        tnr = tn / (tn + fp)
        ba = (tpr + tnr) / 2
        return ba, tpr, tnr, tn, fp, fn, tp

    def test_clf(self, params):
        X = params.pop("samples")
        y = params.pop("targets")
        start = time.time()

        if self.clf_type == "tensorflow":  # tf has no clone
            clf = self.base_clf
        else:
            clf = clone(self.base_clf)
        clf = clf.set_params(**params)
        y_pred = clf.fit_predict(X)

        ba, tpr, tnr, tn, fp, fn, tp = self.fpfn(y_pred, y)

        end = time.time()
        duration = end - start

        fname = f"{self.datadir}/{self.clf_name}" + self.experiment_file_params(params)

        if self.clf_type == "tensorflow":  # tf is not pickle compatible
            clf.metrics_ = [ba, tpr, tnr, duration, tn, fp, fn, tp]
            clf.save(fname)
            pickle.dump(
                [ba, tpr, tnr, duration, tn, fp, fn, tp],
                open(
                    fname + "/metrics",
                    "wb",
                ),
            )
        else:
            pickle.dump(
                [clf, ba, tpr, tnr, duration, tn, fp, fn, tp],
                open(
                    fname,
                    "wb",
                ),
            )
        return ba, tpr, tnr, duration

    def grid_make_iterable(self):
        for k, v in self.params.items():
            if not isinstance(self.params[k], Iterable):
                self.params[k] = [v]
            if isinstance(self.params[k], str):
                self.params[k] = [v]

    def grid_generate_search_space(self, X, y):
        self.params["samples"] = [X]
        self.params["targets"] = [y]
        self.grid_make_iterable()

        self.params = list(ParameterGrid(self.params))

    def experiment_exists(self, prefix, p):
        experiment = prefix + self.experiment_file_params(p)
        return os.path.isfile(experiment)

    def experiment_file_params(self, p):
        str_params = ""
        for k, v in p.items():
            if k == "samples" or k == "targets":
                continue
            str_params += f"-{k}_{v}"
        return str_params

    def grid_remove_existing_tests(self):
        prefix = f"{self.datadir}/{self.clf_name}"
        self.params = [p for p in self.params if not self.experiment_exists(prefix, p)]

    def grid_find_best_result(self):
        best_ba = 0
        p = Path(self.datadir)
        experiments = list(p.glob(f"{self.clf_name}-*"))
        for experiment in experiments:
            if os.path.isdir(experiment):  # tf
                clf = load_model(experiment)
                with open(str(experiment) + "/metrics", "rb") as fp:
                    [ba, tpr, tnr, duration, tn, fp, fn, tp] = pickle.load(fp)
            else:
                with open(experiment, "rb") as fp:
                    [clf, ba, tpr, tnr, duration, tn, fp, fn, tp] = pickle.load(fp)
            if ba > best_ba:
                best_ba = ba
                best_tpr = tpr
                best_tnr = tnr
                best_duration = duration
                best_exp = experiment
                best_clf = clf

        params = str(best_exp).split("-")[1:]
        params = ",".join(params)
        logging.info(
            f"{self.clf_name.upper()} BEST [{best_duration:.2f}s]"
            f"({params}): "
            f"ba {best_ba:.4f}, tpr {best_tpr:.4f}, tnr {best_tnr:.4f}"
        )

        self.best_score_ = best_ba
        self.best_estimator_ = best_clf
        if hasattr(best_clf, "get_params"):  # sklearn
            self.best_params_ = best_clf.get_params()
            self.labels_ = best_clf.labels_

    def grid_get_estimators(self):
        p = Path(self.datadir)
        experiments = list(p.glob(f"{self.clf_name}-*"))
        for experiment in experiments:
            with open(experiment, "rb") as fp:
                [clf, ba, tpr, tnr, duration, tn, fp, fn, tp] = pickle.load(fp)
                self.estimators_.append(clf)
                print(experiment)
                print(clf)

    def grid_find_mean_std(self):
        bas = []
        p = Path(self.datadir)
        params = "-".join(str(e[0]) for e in self.params[:-1])  # skip round parameter
        experiments = list(p.glob(f"{self.clf_name}-{params}*"))
        for experiment in experiments:
            with open(experiment, "rb") as fp:
                [ba, tpr, tnr, duration] = pickle.load(fp)
                bas.append(ba)

        max = np.max(bas)
        mean = np.mean(bas)
        std = np.std(bas)
        logging.info(
            f"{self.clf_name.upper()} {len(experiments)} rounds ({params}): "
            f"max {max:.4f}, mean {mean:.4f}, std {std:.4f}"
        )

    def grid_search_(self, X, y):
        self.grid_generate_search_space(X, y)
        self.grid_remove_existing_tests()

        # tf incompatible with mp according to tf issue #46316
        if self.n_cpus == 1 or self.clf_type == "tensorflow":
            for p in self.params:
                self.test_clf(p)
        else:
            pool_obj = multiprocessing.Pool(self.n_cpus)
            pool_obj.map(self.test_clf, self.params)

    def fit(self, X, y=None):
        self.grid_search_(X, y)
        if y is None:
            self.grid_get_estimators()
        else:
            self.grid_find_best_result()

    def test_rounds(self, X, y):
        self.grid_search_(X, y)
        self.grid_find_mean_std()
