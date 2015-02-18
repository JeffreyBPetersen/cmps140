# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    #for each iteration set each state's value to the value of the best getQValue(state,action)
    for _ in range(self.iterations):
      newValues = util.Counter()
      for state in self.mdp.getStates():
        bestAction = None
        if not self.mdp.getPossibleActions(state):
          newValues[state] = self.getValue(state)
        else:
          for action in self.mdp.getPossibleActions(state):
            if bestAction == None:
              bestAction = action
            elif self.getQValue(state, action) > self.getQValue(state, bestAction):
              bestAction = action
          newValues[state] = self.getQValue(state, bestAction)
      self.values = newValues
          
    
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    #return summed weighted values of possible transitions on action
    value = 0
    for transition in self.mdp.getTransitionStatesAndProbs(state, action):
      value += (self.getValue(transition[0]) * self.discount + self.mdp.getReward(state, action, transition[0])) * transition[1]
    #  print "Discount: ", self.discount, ", getReward: ", self.mdp.getReward(state, action, transition[0]), ", Transition: ", transition
    #print "State: ", state, ", Action: ", action, ", QValue: ", value
    return value
    
    util.raiseNotDefined()

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    #return action for highest getQValue(state,action)
    bestAction = None
    for action in self.mdp.getPossibleActions(state):
      if bestAction == None:
        bestAction = action
      elif self.getQValue(state, action) > self.getQValue(state, bestAction):
        bestAction = action
    return bestAction
    
    util.raiseNotDefined()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
