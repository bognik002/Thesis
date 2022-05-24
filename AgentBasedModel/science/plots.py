from numpy import unique
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns


class TransitionMatrix:
    def __init__(self, states: list = None):
        self.labels = ['stationary', 'bullish', 'bearish', 'destructive', 'speculative']
        if states:
            self.matrix = self._initialize(states)
        else:
            self.matrix = self._create_empty()

    def _create_empty(self):
        matrix = list()
        for _ in range(len(self.labels)):
            tmp = list()
            for _ in range(len(self.labels)):
                tmp.append(0)
            matrix.append(tmp)
        return matrix

    def _initialize(self, states):
        # Matrix initialization
        matrix = self._create_empty()

        # Transition matrix calculation
        for i in range(len(states) - 1):
            for st1 in states[i]:
                for st2 in states[i+1]:
                    idx1 = self.labels.index(st1)
                    idx2 = self.labels.index(st2)
                    matrix[idx1][idx2] += 1
        return matrix

    def update(self, states):
        matrix = self._initialize(states)
        for i in range(len(self.labels)):
            for j in range(len(self.labels)):
                self.matrix[i][j] += matrix[i][j]


class TimeMatrix:
    def __init__(self, states: list = None, labels: list = None):
        self.labels = ['stationary', 'bullish', 'bearish', 'destructive', 'speculative']
        self.matrix = list() if states is None else self._initialize(states)

    def _initialize(self, states):
        matrix = list()
        for values in states:
            tmp = {label: 0 for label in self.labels}
            for v in values:
                tmp[v] += 1
            matrix.append(tmp)
        return matrix

    def update(self, states):
        if not self.matrix:
            self.matrix = self._initialize(states)
        else:
            for i, values in enumerate(states):
                for v in values:
                    self.matrix[i][v] += 1


def heatmap_transition(transition_matrix: TransitionMatrix, prob: bool = True, annot: bool = True, figsize=(6, 6)):
    data = DataFrame(transition_matrix.matrix, columns=transition_matrix.labels, index=transition_matrix.labels)
    if prob:
        data = data / sum(data.sum())

    plt.figure(figsize=figsize)
    sns.heatmap(data, annot=annot, vmin=0, cbar=False, cmap='Blues')
    plt.show()


def heatmap_time(matrix: TimeMatrix, size=None, window=0, prob: bool = True, annot: bool = True, figsize=(6, 6)):
    data = DataFrame(matrix.matrix)
    if prob:
        data = data / data.sum()

    if size:
        data.index = [size + i * size - window for i in range(data.shape[0])]

    plt.figure(figsize=figsize)
    sns.heatmap(data.T, annot=annot, vmin=0, cbar=False, cmap='Blues')
    plt.show()
