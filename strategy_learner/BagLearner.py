'''
BagLearner
Shanshan Wang
swang637
'''

import numpy as np
import collections as cl

class BagLearner(object):

    def __init__(self, learner, kwargs={}, bags = 20, boost = False, verbose = False):
        self.bags = bags
        self.verbose = verbose
        self.learner = learner
        self.kwargs = kwargs
        self.boost = boost
        self.learners = []
        for i in range(0,bags):
            self.learners.append(self.learner(**kwargs))
        np.random.seed(seed=0)
    def author(self):
        return 'swang637'

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        for learner in self.learners:
            indc = np.random.randint(dataX.shape[0], size = dataX.shape[0])
            learner.addEvidence(dataX[indc], dataY[indc])
    def query(self,testX):
        result = []
        for learner in self.learners:
            result.append(learner.query(testX))

        result = np.transpose(result)
        returns = [max(cl.Counter(x).iteritems(), key = lambda x : x[1])[0] for x in result]
        return np.array(returns)
if __name__=="__main__":
    print "This is Bag leaner\n"
