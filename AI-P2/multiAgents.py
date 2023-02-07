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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPositions = [i.getPosition() for i in newGhostStates]
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        # print(currentGameState.getPacmanPosition())
        # print(successorGameState.getPacmanPosition())
        # print(action)
        # print("new Pos:", newPos)
        # print("new Food:", newFood.asList())
        # # print("new GhostStates:", newGhostStates)
        # print("new GhostPositions:", newGhostPositions)
        # print("new ScaredTimes:", newScaredTimes)
        "*** YOUR CODE HERE ***"

        food_loc = [i for i in newFood.asList()]
        food_dist = [manhattanDistance(i,newPos) for i in food_loc]
        distance_to_ghosts = [manhattanDistance(i,newPos) for i in newGhostPositions]
        closest_ghost_dist = min(distance_to_ghosts)

        food_count = len(food_loc)
        if(food_count==0):
            if(closest_ghost_dist==1 or closest_ghost_dist==0):
                return -1000
            elif(closest_ghost_dist>1):
                return (successorGameState.getScore() + newScaredTimes[0]) + (1-float(1/closest_ghost_dist))

        else:
            if(closest_ghost_dist==1 or closest_ghost_dist==0):
                return -1000
            elif(closest_ghost_dist>1):
                return (successorGameState.getScore() + float(1 / min(food_dist)) + newScaredTimes[0]) +(1-float(1/closest_ghost_dist))


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

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

        "*** YOUR CODE HERE ***"
        def min_value(gameState,currentDepth,agentIndex):
            if(currentDepth==self.depth):
                return self.evaluationFunction(gameState)
            elif(gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            if ((agentIndex + 1) == gameState.getNumAgents()):
                currentDepth += 1
            v=float('inf')
            for action in gameState.getLegalActions(agentIndex):
                if((agentIndex + 1) == gameState.getNumAgents()):
                    nextState = gameState.generateSuccessor(agentIndex, action)
                    v = min(v, max_value(nextState, currentDepth, (agentIndex + 1) % gameState.getNumAgents()))
                else:
                    nextState = gameState.generateSuccessor(agentIndex, action)
                    v=min(v,min_value(nextState,currentDepth,(agentIndex + 1) % gameState.getNumAgents()))
            return v
        def max_value(gameState,currentDepth,agentIndex):
            if(currentDepth==self.depth):
                return self.evaluationFunction(gameState)
            elif(gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            v=float('-inf')
            for action in gameState.getLegalActions(agentIndex):
                nextState = gameState.generateSuccessor(agentIndex,action)
                v=max(v,min_value(nextState,currentDepth,(agentIndex + 1) % gameState.getNumAgents()))
            return v
        v = float('-inf')
        act=None
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            temp=min_value(nextState,0,1)
            if(temp>=v):
                v=temp
                act=action
        return act





class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def min_value(gameState,currentDepth,agentIndex,alpha,beta):
            if(currentDepth==self.depth):
                return self.evaluationFunction(gameState)
            elif(gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            if ((agentIndex + 1) == gameState.getNumAgents()):
                currentDepth += 1
            v=float('inf')
            for action in gameState.getLegalActions(agentIndex):
                if((agentIndex + 1) == gameState.getNumAgents()):
                    nextState = gameState.generateSuccessor(agentIndex, action)
                    v = min(v, max_value(nextState, currentDepth, (agentIndex + 1) % gameState.getNumAgents(),alpha,beta))
                    if(v<alpha):
                        return v
                    beta=min(v,beta)
                else:
                    nextState = gameState.generateSuccessor(agentIndex, action)
                    v=min(v,min_value(nextState,currentDepth,(agentIndex + 1) % gameState.getNumAgents(),alpha,beta))
                    if(v<alpha):
                        return v
                    beta=min(v,beta)
            return v
        def max_value(gameState,currentDepth,agentIndex,alpha,beta):
            if(currentDepth==self.depth):
                return self.evaluationFunction(gameState)
            elif(gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            v=float('-inf')
            for action in gameState.getLegalActions(agentIndex):
                nextState = gameState.generateSuccessor(agentIndex,action)
                v=max(v,min_value(nextState,currentDepth,(agentIndex + 1) % gameState.getNumAgents(),alpha,beta))
                if (v > beta):
                    return v
                alpha= max(v, alpha)
            return v
        v = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        act=None
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            temp=min_value(nextState,0,1,alpha,beta)
            if(temp>=v):
                v=temp
                act=action
                alpha=max(v,alpha)
        return act




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
        def exp_value(gameState,currentDepth,agentIndex):
            if(currentDepth==self.depth):
                return self.evaluationFunction(gameState)
            elif(gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            if ((agentIndex + 1) == gameState.getNumAgents()):
                currentDepth += 1
            v=0
            for action in gameState.getLegalActions(agentIndex):
                if((agentIndex + 1) == gameState.getNumAgents()):
                    nextState = gameState.generateSuccessor(agentIndex, action)
                    v += max_value(nextState, currentDepth, (agentIndex + 1) % gameState.getNumAgents())
                else:
                    nextState = gameState.generateSuccessor(agentIndex, action)
                    v+=exp_value(nextState,currentDepth,(agentIndex + 1) % gameState.getNumAgents())
            return float(v/len(gameState.getLegalActions(agentIndex)))
        def max_value(gameState,currentDepth,agentIndex):
            if(currentDepth==self.depth):
                return self.evaluationFunction(gameState)
            elif(gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            v=float('-inf')
            for action in gameState.getLegalActions(agentIndex):
                nextState = gameState.generateSuccessor(agentIndex,action)
                v=max(v,exp_value(nextState,currentDepth,(agentIndex + 1) % gameState.getNumAgents()))
            return v
        v = float('-inf')
        act=None
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            temp=exp_value(nextState,0,1)
            if(temp>=v):
                v=temp
                act=action
        return act


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    Don't forget to use pacmanPosition, foods, scaredTimers, ghostPositions!
    DESCRIPTION: <write something here so we know what you did>
    """

    pacmanPosition = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    ghostPositions = [i.getPosition() for i in ghostStates]
    scaredTimers = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositions = currentGameState.getGhostPositions()
    capules_positions = currentGameState.getCapsules()

    "*** YOUR CODE HERE ***"
    food_loc = [i for i in foods.asList()]
    food_dist = [manhattanDistance(i, pacmanPosition) for i in food_loc]
    distance_to_ghosts = [manhattanDistance(i, pacmanPosition) for i in ghostPositions]
    closest_ghost_dist = min(distance_to_ghosts)
    food_count = len(food_loc)
    if (food_count == 0):
        return 1000
    else:
        if (closest_ghost_dist == 1 or closest_ghost_dist == 0):
            return -1000
        elif (closest_ghost_dist > 1):
            return (currentGameState.getScore() + 2*float(1 / min(food_dist)) + scaredTimers[0]) + (
                        1 - float(1 / closest_ghost_dist))-(len(capules_positions)*20)

# Abbreviation
better = betterEvaluationFunction
