# -*- coding: utf-8 -*-
# Author: Yuta Nakahara <yuta.nakahara@aoni.waseda.jp>

from abc import ABCMeta, abstractmethod

class Generative(metaclass=ABCMeta):
    @abstractmethod
    def set_h_params(self):
        pass

    @abstractmethod
    def get_h_params(self):
        pass
    
    @abstractmethod
    def save_h_params(self):
        pass

    @abstractmethod
    def load_h_params(self):
        pass

    @abstractmethod
    def gen_params(self):
        pass

    @abstractmethod
    def set_params(self):
        pass

    @abstractmethod
    def get_params(self):
        pass

    @abstractmethod
    def save_params(self):
        pass

    @abstractmethod
    def load_params(self):
        pass

    @abstractmethod
    def gen_sample(self):
        pass

    @abstractmethod
    def save_sample(self):
        pass

    @abstractmethod
    def visualize_model(self):
        pass

class Posterior(metaclass=ABCMeta):
    @abstractmethod
    def set_h0_params(self):
        pass

    @abstractmethod
    def get_h0_params(self):
        pass
    
    @abstractmethod
    def save_h0_params(self):
        pass

    @abstractmethod
    def load_h0_params(self):
        pass

    @abstractmethod
    def get_hn_params(self):
        pass
    
    @abstractmethod
    def save_hn_params(self):
        pass

    @abstractmethod
    def reset_hn_params(self):
        pass

    @abstractmethod
    def update_posterior(self):
        pass

    @abstractmethod
    def estimate_params(self):
        pass

    @abstractmethod
    def visualize_posterior(self):
        pass

class PredictiveMixin(metaclass=ABCMeta):
    @abstractmethod
    def get_p_params(self):
        pass
    
    @abstractmethod
    def save_p_params(self):
        pass

    @abstractmethod
    def calc_pred_dist(self):
        pass

    @abstractmethod
    def make_prediction(self):
        pass
    
    @abstractmethod
    def pred_and_update(self):
        pass
    
    