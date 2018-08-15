"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=1489683273):
    np.random.seed(seed)
    #X = np.random.normal((500,2))
    X = np.random.normal(size = (100,3))
    # Here's is an example of creating a Y from randomly generated
    # X with multiple columns
    Y = 0.2 * X[:,0] + 0.3 * np.sin(X[:,1]) + 0.2 * np.cos(X[:,2])
    return X, Y

def best4DT(seed=1489683273):
    np.random.seed(seed)
    #X = np.zeros((100,2))
    #Y = np.random.random(size = (100,))*200-100
    X = np.random.normal(size = (100,2))
    Y = 0.2 * X[:,0] + 5 * X[:,1]**2
    return X, Y


def author():
    return 'swang637' #Change this to your user ID

if __name__=="__main__":
    print "they call me Monster!"
