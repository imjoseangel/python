#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Load CSV using Pandas from URL
from pandas import read_csv
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv'
names = [
    'preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class'
]
data = read_csv(url, names=names)

# shape
print(data.shape)

# head
print(data.head(20))

# descriptions
print(data.describe())

# class distribution
print(data.groupby('class').size())

# scatter plot matrix
scatter_matrix(data)
plt.show()