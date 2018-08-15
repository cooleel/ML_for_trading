import numpy as np
import LinRegLearner as lrl
import BagLearner as bl

class InsaneLearner(object):
    def __init__(self, learner=bl.BagLearner, kwargs={"learner":lrl.LinRegLearner,"kwargs":{}},bags=20, verbose=False):
        self.learners = []
        self.bags = bags
        self.verbose=verbose
        for i in xrange(0, bags):
            self.learners.append(learner(**kwargs))
    def author(self):
        return "swang637"
    def addEvidence(self, Xtrain, Ytrain):
        for i in xrange(0, self.bags):
            self.learners[i].addEvidence(Xtrain, Ytrain)
    def query(self, Xtest):
        result = np.zeros([Xtest.shape[0]])
        for i in xrange(0, self.bags):
            result = result + self.learners[i].query(Xtest)
        if self.verbose:
            print("this is result:",result/self.bags)
        return result/self.bags
