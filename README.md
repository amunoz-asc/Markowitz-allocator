# Markowitz-allocator
Public version of Markowitz allocator class 

### Description

This repository features an allocator that uses the theory developed by Markowitz for portfolio allocation. It was developed in the context of Acensi Finance's NewPortAl project and seeks to understand the theory of portfolio allocation and extend it.

### How to use it

We need to obtain the historical data of the assets, such as their value over a month, a year or several years. This information (called observations in the code) should be delivered to the class as a matrix such that each row should correspond to the price of the same asset for each time interval.
If we are working with N assets, then this matrix must have dimensions N x n° of observations, and the vector with the names of each asset must be N long.
Images with examples of the output and the use of the functions described in this repository can be found on the wiki.
