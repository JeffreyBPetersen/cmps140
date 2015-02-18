# analysis.py
# -----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

def question2():
  answerDiscount = 0.9
  answerNoise = 0.0169 #highest noise to cross bridge to 3 significant figures
  return answerDiscount, answerNoise

def question3a():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = -2.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3b():
  answerDiscount = 0.3
  answerNoise = 0.2
  answerLivingReward = 0.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3c():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = -1.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3d():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 0.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3e():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 1.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question6():
  answerEpsilon = None
  answerLearningRate = None
  return 'NOT POSSIBLE'
  """
  Any episodes that do not cross the bridge do not contribute to learning to cross the bridge.
  This is as they can only reinforce stepping off the bridge at the start
  and/or avoiding the edges of the bridge.
  When making a random movement there is a 1/4 chance of moving towards the other end of the bridge.
  When making a random movement there is a 1/2 chance of falling off the bridge.
  When making a random movement there is a 1/4 chance of moving towards the starting end of the bridge.
  Any non-random movement will move towards the close end of the bridge after minimal learning
  unless the far end is already known.
  Thus e = 1 maximizes the chances of moving towards the far end.
  As there is at least a 1/2 chance of falling off in potentially recovering from backing up a space
  the chance of recovering from backing up a space can be capped at 1/2
  Given a 1/4 chance of progressing and a 1/2 chance of recovering from a 1/4 chance of backing up
  then a known overestimate of progressing 3/8 of the time from a space can be deduced.
  As there are 5 progressions that must be made to reach the far end of the bridge
  1/(3/8)^5 can be taken as a lower bound on the chance of reaching the far end.
  This gives approximately 134 episodes, which is more than twice 50 and shows that it is impossible to
  attain even a 50% chance of finding the optimal policy in 50 episodes.
  """
  
  return answerEpsilon, answerLearningRate
  # If not possible, return 'NOT POSSIBLE'
  
if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import analysis
  for q in [q for q in dir(analysis) if q.startswith('question')]:
    response = getattr(analysis, q)()
    print '  Question %s:\t%s' % (q, str(response))
