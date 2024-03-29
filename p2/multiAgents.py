# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"
    #print "scores: ", scores, ", bestScore: ", bestScore, ", bestIndices: ", bestIndices, ", chosenIndex: ", chosenIndex

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    score = 0
    pacPos = successorGameState.getPacmanPosition()
    foodList = successorGameState.getFood().asList()
    ghostable = []
    for ghostState in newGhostStates:
      ghostPos = ghostState.getPosition()
      #print "ghostState: ", ghostState, ", ghostPos: ", ghostPos
      #print "pacPos: ", pacPos
      ghostable.append((ghostPos[0],ghostPos[1]))
      ghostable.append((ghostPos[0],ghostPos[1] - 1))
      ghostable.append((ghostPos[0],ghostPos[1] + 1))
      ghostable.append((ghostPos[0] - 1,ghostPos[1]))
      ghostable.append((ghostPos[0] + 1,ghostPos[1]))
    if len(foodList) > 0:
      score -= abs(pacPos[0] - foodList[0][0]) + abs(pacPos[1] - foodList[0][1])
    if len(successorGameState.getFood().asList()) < len(currentGameState.getFood().asList()):
      score = 0
    if pacPos in ghostable:
      score -= 500
    #print "ghostable: ", ghostable
    #print "pacPos: ", pacPos
    #print "score: ", score
    #print "currentFood: ", successorGameState.getFood().asList(), "\n"
    return score
    
    return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    #print "gameState.getNumAgents(): ", gameState.getNumAgents()
    #print "self.depth: ", self.depth
    
    scoreActions = []
    for action in gameState.getLegalActions(0):
      scoreActions.append((self.minimaxHelper(1, 0, gameState.generateSuccessor(0, action)), action))
    bestScore = max(scoreActions)[0]
    bestActions = [scoreAction[1] for scoreAction in scoreActions if scoreAction[0] == bestScore]
    #print "scoreActions: ", scoreActions
    #print "bestScore: ", bestScore
    #print "bestActions: ", bestActions
    return random.choice(bestActions)
    
    util.raiseNotDefined()
    
  def minimaxHelper(self, current_agent, current_depth, gameState):
    #print "current_agent: ", current_agent
    #print "current_depth: ", current_depth
    if current_agent == gameState.getNumAgents():
      current_agent = 0
      current_depth += 1
      if current_depth == self.depth:
        #print "self.evaluationFunction(gameState): ", self.evaluationFunction(gameState)
        return self.evaluationFunction(gameState)
    
    #print "gameState.getLegalActions(current_agent): ", gameState.getLegalActions(current_agent)
    scores = []
    actions = gameState.getLegalActions(current_agent)
    if len(actions) == 0:
      return self.evaluationFunction(gameState)
    for action in actions:
      scores.append(self.minimaxHelper(current_agent + 1, current_depth, gameState.generateSuccessor(current_agent, action)))
    #print "scores: ", scores
    if current_agent == 0:
      return max(scores)
    return min(scores)

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    scoreActions = []
    alpha, beta = float("-inf"), float("inf")
    for action in gameState.getLegalActions(0):
      result = self.abHelper(alpha, beta, 1, 0, gameState.generateSuccessor(0, action))
      scoreActions.append((result[0], action))
      alpha, beta = result[1], result[2]
    bestScore = max(scoreActions)[0]
    bestActions = [scoreAction[1] for scoreAction in scoreActions if scoreAction[0] == bestScore]
    #print "scoreActions: ", scoreActions
    #print "bestScore: ", bestScore
    #print "bestActions: ", bestActions
    return random.choice(bestActions)
    
    util.raiseNotDefined()
    
  def abHelper(self, alpha, beta, current_agent, current_depth, gameState): #returns (score, alpha, beta)
    if current_agent == gameState.getNumAgents():
      current_agent = 0
      current_depth += 1
      if current_depth == self.depth:
        #print "self.evaluationFunction(gameState): ", self.evaluationFunction(gameState)
        return (self.evaluationFunction(gameState), alpha, beta)
    scores = []
    actions = gameState.getLegalActions(current_agent)
    if len(actions) == 0:
      return (self.evaluationFunction(gameState), alpha, beta)
    for action in actions:
      result = self.abHelper(alpha, beta, current_agent + 1, current_depth, gameState.generateSuccessor(current_agent, action))
      if current_agent == 0:
        if result[0] >= beta:
          return (result[0], alpha, beta)
        alpha = max(result[0], alpha)
      else:
        if result[0] <= alpha:
          return (result[0], alpha, beta)
        beta = max(result[0], beta)
      scores.append(result[0])
      alpha, beta = result[1], result[2]
    if current_agent == 0:
      return (max(scores), alpha, beta)
    return (min(scores), alpha, beta)
    

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    scoreActions = []
    for action in gameState.getLegalActions(0):
      scoreActions.append((self.emHelper(1, 0, gameState.generateSuccessor(0, action)), action))
    bestScore = max(scoreActions)[0]
    bestActions = [scoreAction[1] for scoreAction in scoreActions if scoreAction[0] == bestScore]
    #print "scoreActions: ", scoreActions
    #print "bestScore: ", bestScore
    #print "bestActions: ", bestActions
    return random.choice(bestActions)
    
    util.raiseNotDefined()
    
  def emHelper(self, current_agent, current_depth, gameState):
    if current_agent == gameState.getNumAgents():
      current_agent = 0
      current_depth += 1
      if current_depth == self.depth:
        #print "self.evaluationFunction(gameState): ", self.evaluationFunction(gameState)
        return self.evaluationFunction(gameState)
    
    #print "gameState.getLegalActions(current_agent): ", gameState.getLegalActions(current_agent)
    scores = []
    actions = gameState.getLegalActions(current_agent)
    if len(actions) == 0:
      return self.evaluationFunction(gameState)
    for action in actions:
      scores.append(self.emHelper(current_agent + 1, current_depth, gameState.generateSuccessor(current_agent, action)))
    #print "scores: ", scores
    if current_agent == 0:
      return max(scores)
    return sum(scores) / len(scores)

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  scoreModifier = 0
  pacPos = currentGameState.getPacmanPosition()
  foodList = currentGameState.getFood().asList()
  if len(foodList) > 0:
    scoreModifier -= abs(pacPos[0] - foodList[0][0]) + abs(pacPos[1] - foodList[0][1])
  return currentGameState.getScore() + scoreModifier
  
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

