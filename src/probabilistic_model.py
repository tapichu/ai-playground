# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "BSD-new"

"""
Abstract base class for probabilistic models
"""

from abc import ABCMeta, abstractmethod
import os.path
import pickle

class ProbabilisticModel(metaclass=ABCMeta):

    def __init__(self, model_file):
        cwd = os.path.dirname(__file__)
        self.__model_file = os.path.join(cwd, model_file)

        if os.path.isfile(self.__model_file):
            self.model = pickle.load(open(self.__model_file, "rb"))
        else:
            self.build_probabilistic_model()
            pickle.dump(self.model, open(self.__model_file, "wb"))

    @abstractmethod
    def build_probabilistic_model(self):
        pass

    @abstractmethod
    def calculate_probabilities(self, k):
        pass

    @abstractmethod
    def probability(self, elem):
        pass

