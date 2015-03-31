# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
import math

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """
  first = 'ConciseAgent'
  second = 'ConciseAgent'
  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class ConciseAgent(CaptureAgent):
  
  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)
    self.target = random.choice(self.getFood(gameState).asList())
    self.top = self.index > 1
    self.width = gameState.data.layout.width
    
    self.sideWeight = 0.5
    
  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index)
    moves = [(action, self.getSuccessor(gameState, action).getAgentPosition(self.index)) for action in actions]
    if gameState.getAgentPosition(self.index) == self.target:
      self.target = random.choice(self.getFood(gameState).asList())
    
    for newTarget in self.getFood(gameState).asList() + self.getCapsules(gameState):
      newTargetDistance = self.getMazeDistance(gameState.getAgentPosition(self.index), newTarget)
      targetDistance = self.getMazeDistance(gameState.getAgentPosition(self.index), self.target)
      
      newTargetWeight, targetWeight = 0, 0
      # adjust target weight by area chosen for agent
      if self.top:
        newTargetWeight += newTarget[1] * self.sideWeight
        targetWeight += self.target[1] * self.sideWeight
      else:
        newTargetWeight -= newTarget[1] * self.sideWeight
        targetWeight -= self.target[1] * self.sideWeight
      # adjust target weight by target distance
      newTargetWeight -= newTargetDistance
      targetWeight -= targetDistance
      
      if newTargetWeight > targetWeight:
        self.target = newTarget
    
    bestMove = None
    bestWeight = None
    agentPositions = []
    opponents = self.getOpponents(gameState)
    for i in range(3):
      agentPositions.append(gameState.getAgentPosition(i))
    for move in moves:
      weight = 0
      # adjust move weight by target distance
      weight -= self.getMazeDistance(move[1], self.target)
      
      #foodWeight = 0
      #for food in self.getFood(gameState).asList():
      #  foodWeight += self.getMazeDistance(gameState.getAgentPosition(self.index), food)
      #foodWeight /= len(self.getFood(gameState).asList())
      #weight -= pow(foodWeight, 0.5)
      
      #adjust move weight by opponent distance
      for i in range(3):
        if i in opponents and agentPositions[i] != None:
          opponentPos = gameState.getAgentPosition(i)
          dist = self.getMazeDistance(gameState.getAgentPosition(self.index), opponentPos)
          #adjust move weight by opponent ghost distance
          if (self.red and opponentPos[0] >= self.width/2) or ((not self.red) and opponentPos[0] < self.width/2):
            scaredTimer = gameState.data.agentStates[i].scaredTimer
            weight *= 1 - (1 / (1 + pow(dist, 0.5)))/(pow(scaredTimer+1, 0.5))
          #adjust move weight by opponent pacman distance
          else:
            scaredTimer = gameState.data.agentStates[self.index].scaredTimer
            if scaredTimer > 0 and scaredTimer > dist:
              weight *= 1 - (1 / pow(dist, 1.5))
      
      if bestWeight == None or weight > bestWeight:
        bestMove = move[0]
        bestWeight = weight
    
    print bestWeight
    return bestMove
    
  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

class FlowAgent(CaptureAgent):
  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)
    self.walls = gameState.getWalls()
    #self.food = self.getFood(gameState)
    self.width = gameState.data.layout.width
    self.height = gameState.data.layout.height
    self.spaces = gameState.data.layout.walls.asList(False)
    print self.spaces
    self.flowGrid = [[0.0 for y in range(self.height)] for x in range(self.width)]
    self.target = random.choice(self.getFood(gameState).asList())
    food = self.getFood(gameState)
    for x in range(self.width):
      for y in range(self.height):
        self.flowGrid[x][y] = 1 * food[x][y]
    #print self.flowGrid
    #self.tick = 0
    
  def chooseAction(self, gameState):
    #print "index: ", self.index, ", tick: ", self.tick
    #self.tick += 1
    #for index in self.getOpponents(gameState):
    #  print gameState.getAgentPosition(index)
    #for index in range(3):
    #  print gameState.getAgentPosition(index)
    self.updateFlow(gameState)
    print self.flowGrid
    if gameState.getAgentPosition(self.index) == self.target:
      self.target = random.choice(self.getFood(gameState).asList())
    for food in self.getFood(gameState).asList():
      newTarget = food
      newTargetDistance = self.getMazeDistance(gameState.getAgentPosition(self.index), newTarget)
      targetDistance = self.getMazeDistance(gameState.getAgentPosition(self.index), self.target)
      if 10*newTargetDistance + self.flowGrid[self.target[0]][self.target[1]] < 10*targetDistance + self.flowGrid[newTarget[0]][newTarget[1]]:
      #if newTargetDistance < targetDistance:
        self.target = newTarget
    
    actions = gameState.getLegalActions(self.index)
    moves = [(action, self.getSuccessor(gameState, action).getAgentPosition(self.index)) for action in actions]
    bestMove = None
    bestDistance = 9999
    for move in moves:
      distance = self.getMazeDistance(move[1], self.target)
      flow = self.flowGrid[move[1][0]][move[1][1]]
      if distance < bestDistance:
        bestMove = move[0]
        bestDistance = distance
    return bestMove
    
    return random.choice(gameState.getLegalActions(self.index))
  
  def updateFlow(self, gameState):
    newFlowGrid = [[0.0 for y in range(self.height)] for x in range(self.width)]
    food = self.getFood(gameState)
    pos = gameState.getAgentPosition(self.index)
    for x in range(1, self.width - 1):
      for y in range(1, self.height - 1):
        flows = [(x,y)]
        for pos in [(x,y+1),(x+1,y),(x,y-1),(x-1,y)]:
          if(not self.walls[pos[0]][pos[1]]):
            flows.append(pos)
        #print flows
        for flow in flows:
          newFlowGrid[flow[0]][flow[1]] += (self.flowGrid[x][y] / len(flows))
        #newFlowGrid[x][y] += self.flowGrid[x][y]
        if food[x][y]:
          newFlowGrid[x][y] += 1
        if x == pos[0] and y == pos[1]:
          newFlowGrid[x][y] = 0
    self.flowGrid = newFlowGrid
    
  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

class TestAgent(CaptureAgent):
  
  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)
    self.target = random.choice(self.getFood(gameState).asList())
    
  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index)
    moves = [(action, self.getSuccessor(gameState, action).getAgentPosition(self.index)) for action in actions]
    if gameState.getAgentPosition(self.index) == self.target:
      self.target = random.choice(self.getFood(gameState).asList())
    newTarget = random.choice(self.getFood(gameState).asList())
    newTargetDistance = self.getMazeDistance(gameState.getAgentPosition(self.index), newTarget)
    targetDistance = self.getMazeDistance(gameState.getAgentPosition(self.index), self.target)
    if newTargetDistance < targetDistance:
      self.target = newTarget
    bestMove = None
    bestDistance = 9999
    for move in moves:
      distance = self.getMazeDistance(move[1], self.target)
      if distance < bestDistance:
        bestMove = move[0]
        bestDistance = distance
    return bestMove
    
  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

class FirstAgent(CaptureAgent):
  
  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self, gameState)
  
  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index)
    action = random.choice(actions)
    #print "actions: ", actions
    #print "getTeam(): ", self.getTeam(gameState)
    pos = gameState.getAgentPosition(self.index)
    dirs = ( # north, east, south, west
      not gameState.hasWall(pos[0], pos[1]+1),
      not gameState.hasWall(pos[0]+1, pos[1]),
      not gameState.hasWall(pos[0], pos[1]-1),
      not gameState.hasWall(pos[0]-1, pos[1])
    )
    print "pos: ", pos, ", dirs: ", dirs
    return action
    
  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on). 
    
    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    ''' 
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py. 
    '''
    CaptureAgent.registerInitialState(self, gameState)

    ''' 
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    ''' 
    You should change this in your own agent.
    '''

    return random.choice(actions)

def nearestPoint( pos ):
  """
  Finds the nearest grid point to a position (discretizes).
  """
  ( current_row, current_col ) = pos

  grid_row = int( current_row + 0.5 ) 
  grid_col = int( current_col + 0.5 ) 
  return ( grid_row, grid_col )