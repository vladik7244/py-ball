import numpy as np

def nonlin(x, deriv = False):
    if deriv == True: return x*(1-x)
    return 1/(1+np.exp(-x))
x = np.array([[1, 1, 1],
              [0, 1, 1],
              [0, 1, 0]])

y = np.array([[0, 1, 0],
              [1, 1, 1],
              [0, 1, 0]])

np.random.seed(1)
synapse0 = np.random.random((3, 3)) - 1


for j in xrange(60000):
    layer0 = x
    layer1 = nonlin(np.dot(layer0, synapse0))
    layer1_error = y - layer1
    if j % 10000:
        print("Error: " + str(np.mean(np.abs(layer1_error))))
    layer1_delta = layer1_error * nonlin(layer1, deriv=True)
    synapse0 += layer0.T.dot(layer1_delta)
print("Outputs: ")
print(synapse0)
print(layer1)
