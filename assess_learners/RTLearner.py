
import numpy as np

class RTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size =leaf_size
        self.verbose = verbose
        self.tree = np.array([])

    def author(self):
        return 'swang637' # replace tb34 with your Georgia Tech username

    def buildTree(self,dataX,dataY):

        if dataX.shape[0] <= self.leaf_size:
            return np.array([[-1,dataY.mean(),-1,-1]])
        elif len(np.unique(dataY))==1:

            return np.array([[-1,dataY[0],-1,-1]])
        else:
            max_feature_index = dataX.shape[1]
            i = np.random.randint(max_feature_index) #determine the best feature by random

            splitVal = np.median(dataX[:,i])  #get the split value
            split_index_left = dataX[:,i] <= splitVal #get the split index for lefttree
            split_index_right = dataX[:,i] > splitVal # get the split index for righttree
            if (np.count_nonzero(split_index_left==False)==len(split_index_left)) or (np.count_nonzero(split_index_right==False)==len(split_index_right)):
                return  np.array([[-1,dataY.mean(),-1,-1]])
            #get the left tree
            lefttree = self.buildTree(dataX[dataX[:,i] <= splitVal],dataY[dataX[:,i] <= splitVal])
            #get the right tree
            righttree = self.buildTree(dataX[dataX[:,i] > splitVal],dataY[dataX[:,i] > splitVal])
            root = np.array([[int(i),splitVal,1, lefttree.shape[0] + 1]])
            tmp = np.append(root,lefttree, axis = 0)
            return  np.append(tmp, righttree, axis = 0)

    def addEvidence(self,dataX,dataY):
        self.tree = self.buildTree(dataX,dataY)

    def query(self,Xtest):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        Ytest = np.array([])
        for row in Xtest:
            loop = True
            k = 0
            while loop:
                fac = int(self.tree[k][0])
                splitVal = self.tree[k][1]
                if fac == -1:
                    loop = False
                    Ytest = np.append(Ytest,splitVal)
                else:
                    if row[fac] <= splitVal:
                        k = int(k + self.tree[k][2])
                    else:
                        k = int(k + self.tree[k][3])
        return Ytest

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
