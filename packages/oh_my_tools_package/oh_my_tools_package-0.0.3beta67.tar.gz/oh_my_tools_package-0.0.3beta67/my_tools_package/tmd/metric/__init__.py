# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 10:31 下午
# @Author  : jeffery
# @FileName: __init__.py.py
# @github  : https://github.com/jeffery0628
# @Description:

import pandas as pd
from sklearn.metrics import classification_report



class MetricTracker:
    def __init__(self, *keys, writer=None):
        self.writer = writer
        self._data = pd.DataFrame(index=keys, columns=['total', 'counts', 'average'])
        self.reset()

    def classification_report(self):
        return classification_report(self._labels, self._preds)

    def reset(self):
        self._preds = []
        self._labels = []
        for col in self._data.columns:
            self._data[col].values[:] = 0

    def update(self, key, value, n=1):
        if self.writer is not None:
            self.writer.add_scalar(key, value)
        self._data.total[key] += value * n
        self._data.counts[key] += n
        self._data.average[key] = self._data.total[key] / self._data.counts[key]

    def avg(self, key):
        return self._data.average[key]

    def result(self):
        return dict(self._data.average)
