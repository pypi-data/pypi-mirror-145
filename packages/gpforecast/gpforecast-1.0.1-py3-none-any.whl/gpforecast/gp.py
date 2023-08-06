import GPy
import numpy as np
import pandas as pd
import scipy.stats as stats
import properscoring as ps
from collections.abc import Iterable
import logging

def get_sample_ts(frequency):
    if frequency == 'monthly':
        # return a monthly ts from M3
        return {
            'Y': np.array([
                2640,2640,2160,4200,3360,2400,3600,1920,4200,4560,480,3720,5640,2880,1800,
                3120,2400,2520,9000,2640,3120,2880,8760,5160,2160,8280,4920,3120,6600,4080,
                588,1680,6720,2040,6480,1920,3600,2040,2760,3840,960,2280,1320,2160,4800,3000,
                3120,5880,2640,2400]).reshape(-1,1),
            'YY': np.array([
                2280,480,5040,1920,840,2520,1560,1440,240,1800,4680,1800,1680,3720,2160,480,
                2040,1440
            ])
        }
    if frequency == 'quarterly':
        # return a quarterly ts from M3
        return {
            'Y': np.array([
                3142.63,3190.75,3178.69,3170.94,3124.38,3170,3200.94,3176.75,3170.44,3268.67,
                3198.25,3383.35,3389.78,3368.6,3383.7,4950.95,5086.1,5203.95,5302.75,5268.75,
                5406.85,5472.5,5656.4,5770.3,5677.2,5725.85,5742,5706.6,5591.95,5605.15,5630,
                5589.2,5551.25,5592.15,5481.6,5511.55]).reshape(-1,1),
            'YY': np.array([5531.5,5670.6,5730,5798.45,5809.05,5707.05,5661.75,6176.6])
        }
    else:
        raise Exception(f"wrong frequency: {frequency}")


class GP():

    def __init__(self, frequency, period = 1, priors = True):
        self.set_frequency(frequency)
        self.set_period(period)

        self.Q = 2
        self.restarts = 1
        self.normalize = True

        self.has_priors = priors is not False
        if self.has_priors:
            if priors == True:
                priors = self.default_priors()
            self.init_priors(priors)

        self.Y = None
        self.X_train = None
        self.gp_model = None

        self.logger = logging.getLogger("forgp")
        self.logger.info(f"GP{self.has_priors}, Q={self.Q}, restarts={self.restarts}")


    def standard_prior(self, data):
        """ Get the priors hash from the array of priors data 
        
        This method will name the values in the data according to the ordering used in the
        hierarchical probabilistic programming prior estimation code. 
        This is:
        - std devs
        - means (variance, periodic then exp, cos for the different Qs)
        - alpha 
        - beta
        """

        names = ["p_std_var", "p_std_other", "p_mu_var", "p_mu_periodic"]
        if self.Q >= 1:
            names += ["p_mu_exp1", "p_mu_cos1"]
        if self.Q >= 2:
            names += [ "p_mu_exp2", "p_mu_cos2"]
        names += [ "p_alpha", "p_beta" ]

        return dict(zip(names, data))

    def priors_array(self, data):
        """ Set priors from array
        """
        priors = {
            "p_std_var": data[0], "p_std_other": data[1], 
            "p_mu_var": data[2], "p_mu_rbf": data[3], 
            "p_mu_periodic": data[4]
        }

        for i in range(1, self.Q+1):
            priors[f"p_mu_exp{i}"] = data[5 + (i-1)*2]
            priors[f"p_mu_cos{i}"] = data[6 + (i-1)*2]

        self.has_priors = True
        self.init_priors(priors)

    def default_priors(self):
        """ Get default prior values """
        
        priors = None

        if self.Q == 2 and self.sampling_freq == 12: 
            priors = {
                "p_std_var": 1.0, "p_std_other": 1.0, 
                "p_mu_var": -1.5, "p_mu_rbf": 1.1, 
                "p_mu_periodic": 0.2, "p_mu_exp1": -0.7, "p_mu_cos1": 0.5, "p_mu_exp2": 1.1, "p_mu_cos2": 1.6, 
        
            }
        elif self.Q == 2 and self.sampling_freq == 4:
            priors = {
                "p_std_var":1.340, "p_std_other": 0.938, 
                "p_mu_var": -1.731,  "p_mu_rbf": 0.0, 
                "p_mu_periodic": 1.519, "p_mu_exp1": 1.265, "p_mu_cos1": 0.673, "p_mu_exp2": 0.693, "p_mu_cos2": 0.308,
            }
        else:
            priors = {
                "p_std_var": 1.0, "p_std_other": 1.0, 
                "p_mu_var": -1.5, "p_mu_rbf": 1.1, 
                "p_mu_periodic": 0.2, "p_mu_exp1": -0.7, "p_mu_cos1": 0.5, "p_mu_exp2": 1.1, "p_mu_cos2": 1.6, 
            }
        
        # yearly 1.94, -1.22, 1.48, 0.87
        return priors

    def init_priors(self, priors):
        """ Initialize the prior parameters crearing the GPy priors """

        self.prior_var = GPy.priors.LogGaussian(priors["p_mu_var"], priors["p_std_var"])
        self.prior_lscal_rbf = GPy.priors.LogGaussian(priors["p_mu_rbf"], priors["p_std_other"]) 
        self.prior_lscal_std_periodic = GPy.priors.LogGaussian(priors["p_mu_periodic"], priors["p_std_other"]) 
                
        if self.Q >= 1: 
            self.prior_lscal_exp_short = GPy.priors.LogGaussian(priors["p_mu_exp1"], priors["p_std_other"])
            self.prior_lscal_cos_short = GPy.priors.LogGaussian(priors["p_mu_cos1"], priors["p_std_other"])
        
        if self.Q == 2:
            self.prior_lscal_exp_long = GPy.priors.LogGaussian(priors["p_mu_exp2"], priors["p_std_other"])
            self.prior_lscal_cos_long = GPy.priors.LogGaussian(priors["p_mu_cos2"], priors["p_std_other"])


    def set_period(self, period = 1):
        """ Set the period of the series

        Multiple expected periods can be supported by providing an array
        """

        # check for non iterables and make an array
        if not isinstance(period, Iterable):
            self.periods = [ period ]
        else:
            self.periods = period

    def set_frequency(self, frequency):
        """ Set the data's frequency 
        
        The frequency can be either a standard value (monthly, quarterly, yearly, weekly, daily)
        or a float defining the "resolution" of the timeseries

        Parameters
        ----------
            frequency : str|number
                This can be either a standard value among: monthly, quarterly, yearly and weekly 
                or a numeric value
        """
        if type(frequency) != str:
            self.sampling_freq = frequency
        elif frequency == 'monthly':
            self.sampling_freq = 12
        elif frequency == 'quarterly':
            self.sampling_freq = 4
        elif frequency == 'yearly':
            self.sampling_freq = 1
        elif frequency == 'weekly':
            self.sampling_freq = 365.25/7.0
        else:
            raise Exception(f"wrong frequency: {frequency}")

    def set_q(self, Q):
        """ Set the number of spectral kernels (exp+cos) """

        self.Q = Q

    def build(self, Yin, X = None):
        """ Fit a gaussian process using the specified train values """
        use_bias = True

        if X is None:
            X = np.linspace(1/self.sampling_freq,len(Yin)/self.sampling_freq,len(Yin))
            X = X.reshape(len(X),1)
        
        Y = Yin

        #the yearly case is managed on its own.
        lin = GPy.kern.Linear(input_dim=1)
        
        if self.has_priors:
            self.logger.debug(f"Setting Variance Prior {self.prior_var}")
            lin.variances.set_prior(self.prior_var)
        K = lin

        if use_bias: 
            bias = GPy.kern.Bias(input_dim=1)
            if self.has_priors:
                self.logger.debug(f"Setting Bias Prior {self.prior_var}")
                bias.variance.set_prior(self.prior_var)
            K = K + bias
    
        rbf = GPy.kern.RBF(input_dim=1)
        if self.has_priors:
            self.logger.debug(f"Setting RBF priors var {self.prior_var} and lengthscale {self.prior_lscal_rbf}")
            rbf.variance.set_prior(self.prior_var)
            rbf.lengthscale.set_prior(self.prior_lscal_rbf)
            
        K = K + rbf

        for period in self.periods:
            #the second component  is the stdPeriodic
            periodic = GPy.kern.StdPeriodic(input_dim=1)
            periodic.period.fix(period) # period is set to 1 year by default

            if self.has_priors:
                self.logger.debug(f"Setting periodic {period} lscale {self.prior_lscal_std_periodic}")
                periodic.lengthscale.set_prior(self.prior_lscal_std_periodic)
                periodic.variance.set_prior(self.prior_var)
            K = K + periodic

        #now initiliazes the  (Q-1) SM components. Each component is rfb*cos, where
        #the variance of the cos is set to 1.
        for ii in range(0, self.Q):
            cos =  GPy.kern.Cosine(input_dim=1)
            cos.variance.fix(1)
            rbf =  GPy.kern.RBF(input_dim=1) #input dim, variance, lenghtscale
    
            if self.has_priors:
                if (ii==0):
                        rbf.variance.set_prior(self.prior_var)
                        rbf.lengthscale.set_prior(self.prior_lscal_exp_long)
                        cos.lengthscale.set_prior(self.prior_lscal_cos_long)
                elif (ii==1):
                        rbf.variance.set_prior(self.prior_var)
                        rbf.lengthscale.set_prior(self.prior_lscal_exp_short)               
                        cos.lengthscale.set_prior(self.prior_lscal_cos_short)
            K = K + cos * rbf
                
        GPmodel = GPy.models.GPRegression(X, Y, kernel=K, normalizer=self.normalize)

        if self.has_priors:
            GPmodel.likelihood.variance.set_prior(self.prior_var)
        
        try:
            GPmodel.optimize_restarts(self.restarts, robust=True)
        except:
            #in the rare case the single optimization numerically fails
            GPmodel.optimize_restarts(5, robust=True)
        
        self.gp_model = GPmodel
        self.Y = Y
        self.X_train = X
        self.mean = np.mean(Y)
        self.std  = np.std(Y, ddof=1)
        return GPmodel


    def forecast(self, X_forecast, level=[80, 95]):
        if self.gp_model == None:
            raise Exception("gp not built")

        if type(X_forecast) == int:
            lastTrain = self.X_train[-1]
            endTest = lastTrain + 1/self.sampling_freq * X_forecast
            X = np.linspace(lastTrain + 1/self.sampling_freq, endTest, X_forecast)
            X = X.reshape(len(X), 1)
        else:
            X = X_forecast
    
        m,v = self.gp_model.predict(X)
        s = np.sqrt(v)

        m = m.reshape(-1,)
        v = v.reshape(-1,)
        s = s.reshape(-1,)

        res = pd.DataFrame(data={"PointForecast" : m, "Var" : v})
        if not isinstance(level, Iterable):
            level=[level]
        for l in level:
            tmp = (1 - l/100) / 2
            res[f'Lo{l}'] = m - s * stats.norm.ppf(1.-tmp)
            res[f'Hi{l}'] = m + s * stats.norm.ppf(1.-tmp)
        
        return res

    def compute_indicators(self, Ytest, mean, upper, level, normalize=True):
        if self.gp_model == None:
            raise Exception("gp not built")

        if normalize:
            Ytest = (Ytest - self.mean) / self.std
            mean = (mean - self.mean) / self.std
            upper = (upper - self.mean) / self.std

        sigma = (upper - mean)/ stats.norm.ppf(1 - (1-level/100)/2)
        fcast = mean
        
        crps = np.zeros(len(Ytest))
        ll = np.zeros(len(Ytest))
            
        for jj in range(len(Ytest)):
            crps[jj]    = ps.crps_gaussian(Ytest[jj], mu=fcast[jj], sig=sigma[jj])
            ll[jj]      = stats.norm.logpdf(x=Ytest[jj], loc=fcast[jj], scale=sigma[jj])
        
        mae = np.mean(np.abs(Ytest  - fcast))
        crps = np.mean(crps)
        ll = np.mean(ll)

        acc = pd.DataFrame(data={"mae":[mae], "crps":[crps], "ll":[ll]})
        acc.index=[""] * len(acc)
        return(acc)