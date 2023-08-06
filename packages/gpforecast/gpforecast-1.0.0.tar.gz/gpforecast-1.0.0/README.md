# Time series forecasting with Gaussian Processes

## Related Publication
The theoretical description of the algorithm implemented in this software and empirical results can be found in:

"Time series forecasting with Gaussian Processes needs priors"\
Giorgio Corani, Alessio Benavoli, Marco Zaffalon\
Accepted at ECML-PKDD 2021\
Arxix preprint: https://arxiv.org/abs/2009.08102

## gpforecast package
The software includes a small package that builds the gaussian process and uses it to produce predictions. The package heavily relies on GPy. 
A convenience script can be used to run the GP over collections of timeseries.

## Installation

gpforecast requires Python 3.8+ to run.
Create a new conda environment named ENVNAME, install Python 3.8
```sh
conda create --name ENVNAME python=3.8
```
Activate the new environment to use it
```sh
conda activate ENVNAME
```
Install **gpforecast** with dependencies
```sh
pip install gpforecast
```

## Tutorial [Python]
```py
from gp import GP, get_sample_ts

# STEP 0. Get a sample time series (Monthly or Quarterly time series from M3)
f = 'quarterly'  # 'monthly' or 'quarterly'
sample = get_sample_ts(frequency=f)

# STEP 1. Construct our model
g = GP(frequency=f, priors=True)

# STEP 2. Build our model
g.build(sample['Y'])

# STEP 3. Forecast
res = g.forecast(len(sample['YY']), level=[80,95])

# STEP 4. Evaluating forecast accuracy {MAE, CRPS, LL}, you could implement your own!
mean = res.PointForecast
u95  = res.Hi95
acc = g.compute_indicators(sample['YY'], mean, u95, level=95)

# STEP 5. Forecasts Plot
import matplotlib.pyplot as plt

def forecast_plot(train, res):
    plt.style.use('ggplot')
    plt.figure(figsize=(16,8))
    plt.plot(list(range(1,len(train)+1)), train.reshape(-1,), color='black')
    plt.plot(list(range(len(train)+1,len(train)+len(res.PointForecast)+1)), 
             res.PointForecast, color='blue')
    levels = []
    for i in res.columns:
        if 'Lo' in i: levels.append(int(i[2:]))
    for i, l in enumerate(sorted(levels)):
        plt.fill_between(list(range(len(train)+1,len(train)+len(res.PointForecast)+1)), 
                         res['Lo'+str(l)], res['Hi'+str(l)], color='blue', alpha=0.3-0.1*i)
    plt.title('Forecasts from GP', loc='left', fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.gca().tick_params(axis='both', which='major', labelsize=12)
    
forecast_plot(sample['Y'], res)
```

## Tutorial [R]
**gpforecast** could be used in R thanks to [Reticulate](https://cran.r-project.org/web/packages/reticulate/index.html)
```R
install.packages("Reticulate")
```
```R
library(reticulate)
use_virtualenv("ENVNAME")           # python environment with gpforecast
gpforecast <- import("gpforecast")  # load Python module
# STEP 0. Get a sample time series (Monthly or Quarterly time series from M3)
f = 'monthly'  # 'monthly' or 'quarterly'
sample = gpforecast$get_sample_ts(frequency=f)

# STEP 1. Construct our model
g <- gpforecast$GP(frequency=f, priors=TRUE)

# STEP 2. Build our model
g$build(sample$Y)

# STEP 3. Forecast
res <- g$forecast(length(sample$YY), level=as.integer(c(80,95)))

# STEP 4. Evaluating forecast accuracy {MAE, CRPS, LL}, you could implement your own!
mean <- as.array(as.vector(t(res['PointForecast'])))
u95  <- as.array(as.vector(t(res['Hi95'])))
acc <- g$compute_indicators(sample$YY, mean, u95, level=as.integer(95))

# STEP 5. Forecasts Plot
library(ggplot2)

forecast_plot <- function(train, res) {
    options(repr.plot.width = 16, repr.plot.height = 8)
    train_df <- data.frame(
        X = 1:length(train), 
        Y = c(as.vector(t(train))))
    res$h = 1:length(res[,'PointForecast']) + length(sample$Y)
    p <- ggplot() +   
    geom_line(data = train_df, aes(X, Y), color = "black", size = 0.8) +
    geom_line(data = res, aes(h, res[,'PointForecast']), color = "blue", size = 0.8)
    levels <- list()
    l <-1
    for (i in colnames(res)) {
        if (grepl('Lo', i, fixed = TRUE)) {
            levels[l] <- substr(i,3,nchar(i))
            l <- l + 1
        }
    }
    levels <- sort(as.numeric(levels))
    for (i in 1:length(levels)) {
        lo <- paste0('Lo',levels[i])
        hi <- paste0('Hi',levels[i])
        p <- p +
        geom_ribbon(data = res, 
                aes_string(x='h', ymin=lo, ymax=hi), 
                alpha=0.4-0.1*i, fill = "blue")
    }
    p <- p + ggtitle('Forecasts from GP') + xlab('Time') +
    theme(
        axis.title.y=element_blank(),
        plot.title = element_text(size = 20),
        axis.title = element_text(size = 18),
        axis.text = element_text(size = 14))
    return (p)
}

forecast_plot(sample$Y, res)
```
---
## IDSIA - _Istituto Dalle Molle di Studi sull'Intelligenza Artificiale_
Lugano, Switzerland [idsia.ch](https://www.idsia.ch/)