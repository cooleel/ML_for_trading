import numpy as np

class BagLearner(object):

    def __init__(self, learner, kwargs, bags = 20, boost = False, verbose = False):
        self.bags = bags
        self.verbose = verbose
        self.learner = learner
        self.kwargs = kwargs
        self.learnersBag = []
        for i in range(0,bags):
            self.learnersBag.append(self.learner(**kwargs))

    def author(self):
        return 'swang637'

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        dataY = dataY.reshape((dataX.shape[0],1))
        data = np.concatenate((dataX, dataY), axis = 1)

        if(self.verbose):
            print "original data is\n",data

        for i in range(0, self.bags):
            row_index = np.random.randint(data.shape[0], size= data.shape[0])
            data_shuffle = data[row_index,:]
            dataX_shuffle = data_shuffle[:,0:-1]
            dataY_shuffle = data_shuffle[:,-1]
            self.learnersBag[i].addEvidence(dataX_shuffle, dataY_shuffle)

    def query(self,Xtest):

        if (self.verbose):
            print "query Xtest is\n", Xtest

        Ypred_bag = np.empty((0, Xtest.shape[0]))
        for i in range(0, self.bags):
            Y_entry = [self.learnersBag[i].query(Xtest)]
            Ypred_bag = np.append(Ypred_bag, Y_entry, axis=0)

        Y = Ypred_bag.mean(0)

        if (self.verbose):
            print "prediction bag Ypred_bag is\n", Ypred_bag
        if (self.verbose):
            print "prediction Y is\n",Y
        return Y

if __name__=="__main__":
    print "This is Bag leaner\n"
