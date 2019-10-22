# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance, Queue
from game import Directions
import random, util
import searchAgents

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

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        numFoodLeft = len(newFood)
        if numFoodLeft == 0:
          return 1000
        minFoodDist = min([util.manhattanDistance(newPos, food) for food in newFood])
        minGhostDist = 100000000
        for (ghost, timer) in zip(newGhostStates, newScaredTimes):
          if timer > 0:
            continue
          minGhostDist = min(minGhostDist, util.manhattanDistance(newPos, ghost.getPosition()))
        # print minGhostDist
        if minGhostDist < 3:
          return -1000000000
        score = - numFoodLeft * 1000 - minFoodDist * 50
        "*** YOUR CODE HERE ***"
        # print score
        return score


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

    def minimax_solve(self, depth, gameState, agent):
      if depth == self.depth:
        return (self.evaluationFunction(gameState), None)
      if agent == 0:
        actions = gameState.getLegalActions(agent)
        if len(actions) == 0:
          return (self.evaluationFunction(gameState), None)
        nextGameStates = [gameState.generateSuccessor(agent, action) for action in actions]
        getMax = max([(self.minimax_solve(depth, nextGameState, agent + 1)[0], action) for nextGameState, action in zip(nextGameStates, actions)])
        return getMax
      else:
        nextAgent = (agent + 1) % gameState.getNumAgents()
        nextDepth = depth
        if nextAgent == 0:
          nextDepth += 1
        actions = gameState.getLegalActions(agent)
        if len(actions) == 0:
          return (self.evaluationFunction(gameState), None)
        nextGameStates = [gameState.generateSuccessor(agent, action) for action in actions]
        getMin = min([(self.minimax_solve(nextDepth, nextGameState, nextAgent)[0], action) for nextGameState, action in zip(nextGameStates, actions)])
        return getMin 
    
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        _, bestAction = self.minimax_solve(0, gameState, 0)
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def pruning_min(self, depth, gameState, agent, alpha, beta):
      if depth == self.depth:
        return self.evaluationFunction(gameState), None 
      nextAgent = (agent + 1) % gameState.getNumAgents()
      nextDepth = depth 
      if nextAgent == 0:
        nextDepth += 1
      bestScore = 1000000000000000
      bestAction = None
      actions = gameState.getLegalActions(agent)
      if len(actions) == 0:
        return self.evaluationFunction(gameState), None
      for action in actions:
        nextGameState = gameState.generateSuccessor(agent, action)
        if nextAgent == 0:
          value = self.pruning_max(nextDepth, nextGameState, alpha, beta)
        else:
          value = self.pruning_min(nextDepth, nextGameState, nextAgent, alpha, beta)
        # print value
        if value[0] <= bestScore:
          bestScore = value[0]
          bestAction = action
        if bestScore < alpha:
          return bestScore, bestAction
        beta = min(beta, bestScore)
      return bestScore, bestAction
      

    def pruning_max(self, depth, gameState, alpha, beta):
      if depth == self.depth:
        return self.evaluationFunction(gameState), None
      bestScore = -1000000000000000
      bestAction = None
      actions = gameState.getLegalActions(0)
      if len(actions) == 0:
        return self.evaluationFunction(gameState), None
      for action in actions:
        nextGameState = gameState.generateSuccessor(0, action)
        value = self.pruning_min(depth, nextGameState, 1, alpha, beta)
        if value[0] >= bestScore:
          bestScore = value[0]
          bestAction = action
        if bestScore > beta:
          return bestScore, bestAction 
        alpha = max(alpha, bestScore)
      return bestScore, bestAction

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        _, bestAction = self.pruning_max(0, gameState, -1000000000000000, 1000000000000000)
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimax_solve(self, depth, gameState, agent):
      if depth == self.depth:
        return (self.evaluationFunction(gameState), None)
      if agent == 0:
        actions = gameState.getLegalActions(agent)
        if len(actions) == 0:
          return (self.evaluationFunction(gameState), None)
        nextGameStates = [gameState.generateSuccessor(agent, action) for action in actions]
        getMax = None
        for nextGameState, action in zip(nextGameStates, actions):
          if getMax is None:
            getMax = (self.expectimax_solve(depth, nextGameState, agent + 1)[0], action)
          else:
            getMax = max(getMax, (self.expectimax_solve(depth, nextGameState, agent + 1)[0], action))
        return getMax
      else:
        nextAgent = (agent + 1) % gameState.getNumAgents()
        nextDepth = depth
        if nextAgent == 0:
          nextDepth += 1
        actions = gameState.getLegalActions(agent)
        if len(actions) == 0:
          return (self.evaluationFunction(gameState), None)
        getSum = 0
        nextGameStates = [gameState.generateSuccessor(agent, action) for action in actions]
        for nextGameState in nextGameStates:
          getSum += self.expectimax_solve(nextDepth, nextGameState, nextAgent)[0]
        getSum /= float(len(actions))
        return (getSum, None)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        _, bestAction = self.expectimax_solve(0, gameState, 0)
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    dist = getDist(currentGameState)
    newFood = currentGameState.getFood().asList()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    numFoodLeft = len(newFood)
    if numFoodLeft == 0:
      return 100000000
    minFoodDist = min([dist[food] for food in newFood])
    minGhostDist = 100000000
    minGhostScared = -1
    for (ghost, timer) in zip(newGhostStates, newScaredTimes):
      if timer > 0:
        pos = (int(ghost.getPosition()[0]), int(ghost.getPosition()[1]))
        temp = dist[pos]
        minGhostScared = temp
        continue
      minGhostDist = min(minGhostDist, dist[ghost.getPosition()])
    # print minGhostDist
    score = 0
    if minGhostDist < 3:
      score = -1000000000
    elif minGhostScared >= 0:
      score =  - minGhostScared
    else:
      score = - numFoodLeft * 1000 - minFoodDist * 50 - minGhostScared * 5
    "*** YOUR CODE HERE ***"
    return score + currentGameState.getScore() * 100000

def getDist(gameState):
  q = Queue()
  pacman = gameState.getPacmanPosition()
  q.push((0, pacman))
  check = {}
  walls = gameState.getWalls().asList()
  w = gameState.data.layout.width
  h = gameState.data.layout.height
  dist = {}
  while not q.isEmpty():
    d, cur = q.pop()
    if cur in check.keys():
      continue
    if cur in walls:
      continue
    if cur[0] <= 0 or cur[0] > w:
      continue
    if cur[1] <= 0 or cur[1] > h:
      continue
    check[cur] = 1
    dist[cur] = d
    next_cur = (cur[0] + 1, cur[1])
    q.push((d + 1, next_cur))
    next_cur = (cur[0] - 1, cur[1])
    q.push((d + 1, next_cur))
    next_cur = (cur[0], cur[1] + 1)
    q.push((d + 1, next_cur))
    next_cur = (cur[0], cur[1] - 1)
    q.push((d + 1, next_cur))
  return dist
# Abbreviation
better = betterEvaluationFunction

