"""
Template for implementing QLearner  (c) 2015 Tucker Balch
Author: swang637
"""

import numpy as np
import random as rand

class QLearner(object):

    def author(self):
        return "swang637"

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0

        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna

        #initiate a q_table
        self.q_table = np.random.uniform(-1.0,1.0,(self.num_states, self.num_actions))

        #initiate dyna
        self.t_dic = {}
        self.r = (-1) * np.ones((num_states,num_actions))

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        #action = rand.randint(0, self.num_actions-1)
        if np.random.random() < self.rar:
            action = rand.randint(0,self.num_actions-1)
        else:
            action = np.argmax(self.q_table[s,:])
        self.a = action
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        #update q_table
        self.q_table[self.s, self.a] = ((1- self.alpha)* self.q_table[self.s,self.a])+ \
            self.alpha* (r+ self.gamma * self.q_table[s_prime,:].max())

        #update each rar
        self.rar = self.rar * self.radr

        #Use Dyna_Q
        if self.dyna != 0:
            #update reward
            self.r[self.s][self.a] = (1 - self.alpha) * (self.r[self.s][self.a]) + \
                self.alpha * r
            # update t_dic
            if self.t_dic.get((self.s,self.a)) is not None:
                self.t_dic[(self.s, self.a)].append(s_prime)
            else:
                self.t_dic[(self.s, self.a)] = [(s_prime)]

            #iteration in dyna
            for i in range(0, self.dyna):
                s_dyna = int(self.num_states * np.random.random())
                a_dyna = int(self.num_actions * np.random.random())

                if  self.t_dic.get((s_dyna,a_dyna)) == None:
                    s_prime_dyna = int(self.num_states * np.random.random())
                else:
                    s_prime_dyna = rand.choice(self.t_dic[s_dyna,a_dyna])

                r_dyna = self.r[s_dyna][a_dyna]

                #update q_table in dyna
                self.q_table[s_dyna,a_dyna] = ((1- self.alpha) * self.q_table[s_dyna,a_dyna]) + \
                    self.alpha * (r_dyna + self.gamma * self.q_table[s_prime_dyna,:].max())
        #new s and a
        self.s = s_prime
        if np.random.random_sample() < self.rar:
            action = rand.randint(0, self.num_actions -1)
        else:
            action = np.argmax(self.q_table[self.s, :])

        self.a = action

#        action = rand.randint(0, self.num_actions-1)
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
