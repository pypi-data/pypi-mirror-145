
### HectorP

### Table of Contents

1. [Introduction](#introduction)
2. [Code Description](#code)
    1. [Installation](#installation)
    2. [Directory Structure](#directories)
    3. [Work Flow](#workflow)
3. [Bugs/Future Work](#bugs)
4. [Utilities](#utilities)
5. [Reference](#references)


### 1. Introduction <a name="introduction"></a>

<p>HectorP is a software package that can be used to estimate a trend in time series with temporal correlated noise. Trend estimation is a common task in geophysical research where one is interested in phenomena such as the increase in temperature, sea level or GNSS derived station position over time. The trend can be linear or a higher degree polynomial and in addition one can estimate periodic signals, offsets and post-seismic deformation. Together they represent the model that is fitted to the observations.</p>

<p>It is well known that in most geophysical time series the noise is correlated in time (Agnew, 1992; Beran, 1992) and this has a significant influence on the accuracy by which the model parameters can be estimated. Therefore, the use of a computer program such as HectorP is advisable. HectorP assumes that the user knows what type of temporal correlated noise exists in the observations and estimates both the model parameters and the parameters of the chosen noise model using the Restricted Maximum Likelihood Estimation (RMLE) method. Since for most observations the choice of noise model can be found from literature or by looking at the power spectral density, this is sufficient in most cases.</p>

<p>Instead of using HectorP, one can also use the [CATS](https://www.ngs.noaa.gov/gps-toolbox/cats.htm) software of Williams (2008). Another alternative is the program [est_noise](https://github.com/langbein-usgs/est_noise) of Langbein (2010). Recent versions include some tricks from Bos et al. (2013) to deal with missing data but with a different way to construct the covariance matrix (Langbein, 2017). HectorP is a complete rewrite of [Hector](https://teromovigo.com/hector/) which is written in C++. The reason for changing the programming language was the need to make maintenance of the code easier. The HectorP (Python)has around 8 times less lines of code than Hector (C++). In addition, Hector could not run on Windows and installation on a Mac computer was difficult. HectorP is a truly cross-platform application.</p>

<p> In the book by [Montillet and Bos (2020)](https://link.springer.com/book/10.1007/978-3-030-21718-1#about) more examples on the analysis of geodetic time series with temporal correlated noise can be found.</p>

<p> The next secion explains how to install HectorP on your computer, the best way to organise your files and the recommended work flow to analyse the time series.</p>

### 2. Code Description <a name="code"></a>

#### 2.i Installation <a name="installation"></a>

Packages needed:
  pandas
  scypi
  mpmath

#### 2.ii Directory Structure <a name="directories"></a>

#### 2.iii Work Flow <a name="workflow"></a>

### 3. Bugs/Future Work <a name="bugs"></a>

| N        | C++ (s) | Python (s) |
|:---      |     ---:|        ---:|
| 1000     |       5 |        2.4 |
| 3000     |       6 |        6.7 |
| 5000     |       7 |       13.6 |
| 8000     |      12 |       28.6 |
| 5000 10% |      16 |       63.8 |
| 8000 10% |      25 |            |
| 5000 20% |      26 |      138.0 |


### 4. Utilities <a name="utilities"></a>

### 5. References <a name="references"></a>
