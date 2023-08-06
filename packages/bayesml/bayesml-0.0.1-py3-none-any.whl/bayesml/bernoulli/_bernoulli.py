# -*- coding: utf-8 -*-
# Author: Yuta Nakahara <yuta.nakahara@aoni.waseda.jp>
import warnings
import numpy as np
from scipy.stats import beta as ss_beta
# from scipy.stats import betabino as ss_betabinom
import matplotlib.pyplot as plt

from .. import base
from .._exceptions import ParameterFormatError, DataFormatError, CriteriaError, ResultWarning

class GenModel(base.Generative):
    def __init__(self,*,p=0.5,h_alpha=0.5,h_beta=0.5,seed=None):
        if p < 0.0 or p > 1.0:
            raise(ParameterFormatError("p must be in [0,1]."))
        self.p = p

        if h_alpha < 0.0:
            raise(ParameterFormatError("h_alpha must be a positive real value."))
        self.h_alpha = h_alpha

        if h_beta < 0.0:
            raise(ParameterFormatError("h_beta must be a positive real value."))
        self.h_beta = h_beta

        self.rng = np.random.default_rng(seed)

    def set_h_params(self,h_alpha,h_beta):
        if h_alpha < 0.0:
            raise(ParameterFormatError("h_alpha must be a positive real value."))
        self.h_alpha = h_alpha

        if h_beta < 0.0:
            raise(ParameterFormatError("h_beta must be a positive real value."))
        self.h_beta = h_beta

    def get_h_params(self):
        return {"h_alpha":self.h_alpha, "h_beta":self.h_beta}
    
    def save_h_params(self,filename):
        np.savez_compressed(filename,h_alpha=self.h_alpha,h_beta=self.h_beta)

    def load_h_params(self,filename):
        h_params = np.load(filename)
        if "h_alpha" not in h_params.files or "h_beta" not in h_params.files:
            raise(ParameterFormatError(filename+" must be a NpzFile with keywords: \"h_alpha\" and \"h_beta\"."))
        self.set_h_params(h_params["h_alpha"], h_params["h_beta"])
        
    def gen_params(self):
        self.p = self.rng.beta(self.h_alpha,self.h_beta)
        
    def set_params(self,p):
        if p < 0.0 or p > 1.0:
            raise(ParameterFormatError("p must be in [0,1]."))
        self.p = p

    def get_params(self):
        return {"p":self.p}

    def save_params(self,filename):
        np.savez_compressed(filename,p=self.p)

    def load_params(self,filename):
        params = np.load(filename)
        if "p" not in params.files:
            raise(ParameterFormatError(filename+" must be a NpzFile with a keyword: \"p\"."))
        self.set_params(params["p"])

    def gen_sample(self,sample_size):
        if sample_size <= 0:
            raise(DataFormatError("sample_size must be a positive integer."))
        return self.rng.binomial(1,self.p,sample_size)
        
    def save_sample(self,filename,sample_size):
        np.savez_compressed(filename,X=self.rng.binomial(1,self.p,sample_size))

    def visualize_model(self,sample_size=20,sample_num=5):
        if sample_size <= 0:
            raise(DataFormatError("sample_size must be a positive integer."))
        if sample_num <= 0:
            raise(DataFormatError("sample_num must be a positive integer."))
        print(f"p:{self.p}")
        fig, ax = plt.subplots(figsize=(5,sample_num))
        for i in range(sample_num):
            X = self.gen_sample(sample_size)
            print(f"X{i}:{X}")
            if i == 0:
                ax.barh(i,X.sum(),label=1,color="C0")
                ax.barh(i,sample_size-X.sum(),left=X.sum(),label=0,color="C1")
            else:
                ax.barh(i,X.sum(),color="C0")
                ax.barh(i,sample_size-X.sum(),left=X.sum(),color="C1")
        ax.legend()
        ax.set_xlabel("Number of occurrences")
        plt.show()

class LearnModel(base.Posterior,base.PredictiveMixin):
    def __init__(self,h0_alpha=0.5,h0_beta=0.5):
        if h0_alpha < 0.0:
            raise(ParameterFormatError("h0_alpha must be a positive real value."))
        self.h0_alpha = h0_alpha
        if h0_beta < 0.0:
            raise(ParameterFormatError("h0_beta must be a positive real value."))
        self.h0_beta = h0_beta
        self.hn_alpha = self.h0_alpha
        self.hn_beta = self.h0_beta
        self.p_alpha = self.hn_alpha
        self.p_beta = self.hn_beta
    
    def set_h0_params(self,h0_alpha,h0_beta):
        if h0_alpha < 0.0:
            raise(ParameterFormatError("h0_alpha must be a positive real value."))
        self.h0_alpha = h0_alpha
        if h0_beta < 0.0:
            raise(ParameterFormatError("h0_beta must be a positive real value."))
        self.h0_alpha = h0_alpha
        self.h0_beta = h0_beta
        self.hn_alpha = self.h0_alpha
        self.hn_beta = self.h0_beta
        self.p_alpha = self.hn_alpha
        self.p_beta = self.hn_beta

    def get_h0_params(self):
        return {"h0_alpha":self.h0_alpha, "h0_beta":self.h0_beta}
    
    def save_h0_params(self,filename):
        np.savez_compressed(filename,h0_alpha=self.h0_alpha,h0_beta=self.h0_beta)

    def load_h0_params(self,filename):
        h0_params = np.load(filename)
        if "h0_alpha" not in h0_params.files or "h0_beta" not in h0_params.files:
            raise(ParameterFormatError(filename+" must be a NpzFile with keywords: \"h0_alpha\" and \"h0_beta\"."))
        self.set_h0_params(h0_params["h0_alpha"], h0_params["h0_beta"])

    def get_hn_params(self):
        return {"hn_alpha":self.hn_alpha, "hn_beta":self.hn_beta}
    
    def save_hn_params(self,filename):
        np.savez_compressed(filename,hn_alpha=self.hn_alpha,hn_beta=self.hn_beta)

    def reset_hn_params(self):
        self.hn_alpha = self.h0_alpha
        self.hn_beta = self.h0_beta
        self.p_alpha = self.hn_alpha
        self.p_beta = self.hn_beta

    def update_posterior(self,X):
        if type(X) is np.ndarray:
            if X.size != np.sum(X==1) + np.sum(X==0):
                raise(DataFormatError("Elements of X must be 0 or 1."))
        elif X != 0 and X != 1:
            raise(DataFormatError("Elements of X must be 0 or 1."))
        self.hn_alpha += np.sum(X==1)
        self.hn_beta += np.sum(X==0)

    def estimate_params(self,loss="squared"):
        if loss == "squared":
            return self.hn_alpha / (self.hn_alpha + self.hn_beta)
        elif loss == "0-1":
            if self.hn_alpha > 1.0 and self.hn_beta > 1.0:
                return (self.hn_alpha - 1.0) / (self.hn_alpha + self.hn_beta - 2.0)
            elif self.hn_alpha > 1.0:
                return 1.0
            elif self.hn_beta > 1.0:
                return 0.0
            else:
                warnings.warn("MAP estimate doesn't exist for the current hn_alpha and hn_beta.",ResultWarning)
                return None
        elif loss == "abs":
            return ss_beta.median(self.hn_alpha,self.hn_beta)
        elif loss == "KL":
            return ss_beta(self.hn_alpha,self.hn_beta)
        else:
            raise(CriteriaError("Unsupported loss function! "
                                "This function supports \"squared\", \"0-1\", \"abs\", and \"KL\"."))
    
    def estimate_interval(self,credibility=0.95):
        if credibility < 0.0 or credibility > 1.0:
            raise(CriteriaError("credibility must be in [0,1]."))
        return ss_beta.interval(credibility,self.hn_alpha,self.hn_beta)
    
    def visualize_posterior(self):
        p_range = np.linspace(0,1,100,endpoint=False)
        fig, ax = plt.subplots()
        ax.plot(p_range,self.estimate_params(loss="KL").pdf(p_range))
        ax.set_xlabel("p")
        ax.set_ylabel("posterior")
        plt.show()
    
    def get_p_params(self):
        return {"p_alpha":self.p_alpha, "p_beta":self.p_beta}
    
    def save_p_params(self,filename):
        np.savez_compressed(filename,p_alpha=self.p_alpha,p_beta=self.p_beta)
    
    def calc_pred_dist(self):
        self.p_alpha = self.hn_alpha
        self.p_beta = self.hn_beta

    def make_prediction(self,loss="squared"):
        if loss == "squared":
            return self.p_alpha / (self.p_alpha + self.p_beta)
        elif loss == "0-1" or loss == "abs":
            if self.p_alpha > self.p_beta:
                return 1
            else:
                return 0
        elif loss == "KL":
            return np.array((self.p_beta / (self.p_alpha + self.p_beta),
                             self.p_alpha / (self.p_alpha + self.p_beta)))
            # return ss_betabinom(1,self.p_alpha,self.p_beta)
        else:
            raise(CriteriaError("Unsupported loss function! "
                                "This function supports \"squared\", \"0-1\", \"abs\", and \"KL\"."))

    def pred_and_update(self,x,loss="squared"):
        if x != 0 and x != 1:
            raise(DataFormatError("x must be 0 or 1."))
        self.calc_pred_dist()
        prediction = self.make_prediction(loss=loss)
        self.update_posterior(x)
        return prediction
