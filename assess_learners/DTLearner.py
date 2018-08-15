import numpy as np
import scipy

class DTLearner(object):
    #set up the initial
    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size =leaf_size
        self.verbose = verbose
        self.tree = np.array([])

    def author(self):
        return 'swang637' # replace tb34 with your Georgia Tech username

    def buildTree(self,dataX,dataY):
        #a dictionary to store the corrcoef
        fa_dict = {}
        if dataX.shape[0] <= self.leaf_size:
            return np.array([[-1,dataY.mean(),-1,-1]]) #return when
        elif (np.count_nonzero(dataY == dataY[0]) == len(dataY)) and (dataX.shape[0] > self.leaf_size):
            return np.array([[-1,dataY[0],-1,-1]])    # return when there is one Y
        else:
            for i in range(0,dataX.shape[1]):
                corrcoef_matrix = np.corrcoef(dataX[:,i],dataY)
                corrcoef = corrcoef_matrix[0,1]
                fa_dict[i] = corrcoef
            #determine the best feature to split on by corrcoef
            i = int(max(fa_dict))
            splitVal = np.median(dataX[:,i])   # get the splitVal
            split_index_left = dataX[:,i] <= splitVal
            split_index_right = dataX[:,i] > splitVal
            if (np.count_nonzero(split_index_left==False)==len(split_index_left)) or (np.count_nonzero(split_index_right==False)==len(split_index_right)):
                return  np.array([[-1,dataY.mean(),-1,-1]])

            #print out the left Tree
            lefttree = self.buildTree(dataX[dataX[:,i] <= splitVal],dataY[dataX[:,i] <= splitVal])
            #print out the right tree
            righttree = self.buildTree(dataX[dataX[:,i] > splitVal],dataY[dataX[:,i] > splitVal])
            #get the root of the tree
            root = np.array([[int(i),splitVal,1, lefttree.shape[0] + 1]])
            temp = np.append(root,lefttree, axis = 0)
            return  np.append(temp, righttree, axis = 0)

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
    print "the secret clue is 'Desicion Tree'"
