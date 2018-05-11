import numpy as np
import pandas as pandas
import corex.corex as ce


x = pandas.read_csv("BIG5/data.csv", sep="\t")
scores = x.ix[:, 7:]
scores = scores.as_matrix()

scores = scores - 1

layer1 = ce.Corex(n_hidden=5)
layer1.fit(scores)

print(layer1.clusters)
print(layer1.tcs)
print(sum(layer1.tcs))




