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


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

-        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        # newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        curFood = currentGameState.getFood()
        # print("\n\n\n")
        # print("successorGameState \n",successorGameState)
        # print("newPos \n",newPos)
        # print("newFood \n",newFood)
        # print("newGhostStates \n",newGhostStates)
        # print("newScaredTimes \n",newScaredTimes)

        if successorGameState.isWin():
            return float('inf')

        ghostPositions = []
        for ghost in newGhostStates:
            ghostPositions.append(ghost.getPosition())

        # finish with the variables, start with the distance (bfs)
        # case of if encounter ghost
        if newPos in ghostPositions: # meet the gost
            target_ghost = ghostPositions.index(newPos) # the ghost we are dealing with
            if newScaredTimes[target_ghost] == 0: # if meet the ghost and the ghost is not scare, leave, otherwise, we will lose
                return -1
            else: # if is scared, we can eat it , with a lot of score
                return float('inf')

        # case of meeting a food:
        food_position = curFood.asList() # position for all the food in the grid
        if newPos in food_position:
            return float('inf')

        # case of none of the 2 above, use the food_position to find the distance to food:
        all_heu = []
        for food in food_position:
            all_heu.append(manhattanDistance(newPos, food))

        return 1 / min(all_heu)


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

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getminimax(self, gameState, agent_ind, depth, agent_num):
        """
        Helper function for getAction.

        # if agent == 0, pacman, max
        # else ghost, min
        """

        # if not the last agent
        next_agent_ind = agent_ind + 1
        next_depth = depth

        # if is the last agent
        if agent_ind == agent_num - 1:  # the last agent. add another depth
            next_depth = depth + 1
            next_agent_ind = 0

        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return [None, self.evaluationFunction(gameState)]
        # agent_ind = currLevel % agent_num

        if agent_ind == 0:  # pacman, from negative infinity to the maximum score
            score = -float('inf')
        else:  # ghost, from positive infinity to xthe minimum score
            score = float('inf')

        all_actions = gameState.getLegalActions(agent_ind)

        # print("all_actions", all_actions)
        bestAction = None
        for action in all_actions:
            succState = gameState.generateSuccessor(agent_ind, action)
            result = self.getminimax(succState, next_agent_ind, next_depth, agent_num)
            child_score = result[1]
            if agent_ind == 0:
                if score < child_score:
                    # print("action,", action)
                    score = child_score
                    bestAction = action
            else:
                if score > child_score:
                    score = child_score
                    bestAction = action
                    # best_action = action

        # print("depth:", depth, " agent_ind", agent_ind, " agent_num", agent_num, " action", best_action)

        return [bestAction, score]


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
        best_result =  self.getminimax(gameState, 0, 0, gameState.getNumAgents())
        return best_result[0]  # return the result
        # return self.getminimax(gameState, 0, gameState.getNumAgents())

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getaplhabeta(self, gameState, agent_ind, depth, agent_num, alpha, beta):
        """
        Helper function for getAction.

        # if agent == 0, pacman, max
        # else ghost, min
        """

        # if not the last agent
        next_agent_ind = agent_ind + 1
        next_depth = depth

        # if is the last agent
        if agent_ind == agent_num - 1:  # the last agent. add another depth
            next_depth = depth + 1
            next_agent_ind = 0

        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return [None, self.evaluationFunction(gameState)]
        # agent_ind = currLevel % agent_num

        if agent_ind == 0:  # pacman, from negative infinity to the maximum score
            score = -float('inf')
        else:  # ghost, from positive infinity to xthe minimum score
            score = float('inf')

        all_actions = gameState.getLegalActions(agent_ind)

        # print("all_actions", all_actions)
        bestAction = None

        if agent_ind == 0:  # max
            for action in all_actions:
                succState = gameState.generateSuccessor(agent_ind, action)
                result = self.getaplhabeta(succState, next_agent_ind, next_depth, agent_num, alpha, beta)
                child_score = result[1]
                alpha = max(alpha, child_score)
                if score < child_score:
                    # print("action,", action)
                    score = child_score
                    bestAction = action
                if beta <= alpha:
                    break
            return [bestAction, alpha]
        else:  # min
            for action in all_actions:
                succState = gameState.generateSuccessor(agent_ind, action)
                result = self.getaplhabeta(succState, next_agent_ind, next_depth, agent_num, alpha, beta)
                child_score = result[1]
                beta = min(beta, child_score)
                if score > child_score:
                    score = child_score
                    bestAction = action
                if beta <= alpha:
                    break
            return [bestAction, beta]

        return [bestAction, score]

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        best_result =  self.getaplhabeta(gameState, 0, 0, gameState.getNumAgents(), -float('inf'), float('inf'))
        return best_result[0]  # return the result


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getexpectimax(self, gameState, agent_ind, depth, agent_num):
        """
        Helper function for getAction.

        # if agent == 0, pacman, max
        # else ghost, min
        """

        # if not the last agent
        next_agent_ind = agent_ind + 1
        next_depth = depth

        # if is the last agent
        if agent_ind == agent_num - 1:  # the last agent. add another depth
            next_depth = depth + 1
            next_agent_ind = 0

        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return [None, self.evaluationFunction(gameState)]
        # agent_ind = currLevel % agent_num

        if agent_ind == 0:  # pacman, from negative infinity to the maximum score
            score = -float('inf')
        else:  # ghost, from positive infinity to xthe minimum score
            score = float('inf')

        all_actions = gameState.getLegalActions(agent_ind)

        # print("all_actions", all_actions)
        bestAction = None
        min_scores = []
        for action in all_actions:
            succState = gameState.generateSuccessor(agent_ind, action)
            result = self.getexpectimax(succState, next_agent_ind, next_depth, agent_num)
            child_score = result[1]
            if agent_ind == 0:
                if score < child_score:
                    # print("action,", action)
                    score = child_score
                    bestAction = action
            else:
                min_scores.append(child_score)
                # if score > child_score:
                    # score = child_score
                    # bestAction = action
                    # best_action = action
                score = sum(min_scores) / len(min_scores)

        # print("depth:", depth, " agent_ind", agent_ind, " agent_num", agent_num, " action", best_action)
        
        return [bestAction, score]

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        best_result =  self.getexpectimax(gameState, 0, 0, gameState.getNumAgents())
        return best_result[0]  # return the result


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    pos = currentGameState.getPacmanPosition()
    ghostState = currentGameState.getGhostStates()
    scaredTimes = [gs.scaredTimer for gs in ghostState]

    # get all the positions
    ghostPositions = []
    for ghost in ghostState:
        ghostPositions.append(ghost.getPosition())
    foodPosition = currentGameState.getFood()
    wallPosition = currentGameState.getWalls()
    capsulePosition = currentGameState.getCapsules()
    width = wallPosition.width
    length = wallPosition.height

    if currentGameState.isWin():
        return float('inf')
    if currentGameState.isLose():
        return -float('inf')    
    
    # score for the over all grid
    score = currentGameState.getScore()

    # use bfs for food to help avoid the block that bothers the manhattan distance
    # depth limit at 5
    food_depth = -1
    max_depth = 3
    ghost_dis = -1
    # cur_depth
    frontier = []
    frontier.append((pos[0], pos[1], 0))  # depth of the pos is 0
    while (len(frontier) > 0 and frontier[0][2] < max_depth):
        if food_depth >= 0 and ghost >= 0:  # if already have find food and ghost, break the loop
            break
        cur = frontier.pop(0)
        cur_x = cur[0]
        cur_y = cur[1]
        cur_depth = cur[2]
        if cur_y != 0 and wallPosition[cur_x][cur_y - 1] == False: # up
            if ghost_dis < 0 and (cur_x, cur_y - 1) in ghostPositions and scaredTimes[ghostPositions.index((cur_x, cur_y - 1))] == 0:  # ghost still not found, is ghost, ghost is not scared
                ghost_dis = cur_depth
            elif food_depth < 0 and (cur_x, cur_y - 1) in foodPosition:  # never met food, has food
                food_depth = cur_depth
            else:
                frontier.append((cur_x, cur_y - 1, cur_depth + 1))
        if cur_y != length - 1 and wallPosition[cur_x][cur_y + 1] == False: # down
            if ghost_dis < 0 and (cur_x, cur_y + 1) in ghostPositions and scaredTimes[ghostPositions.index((cur_x, cur_y + 1))] == 0:  # ghost still not found, is ghost, ghost is not scared
                ghost_dis = cur_depth
            elif food_depth < 0 and (cur_x, cur_y + 1) in foodPosition:  # never met food, has food
                food_depth = cur_depth
            else:
                frontier.append((cur_x, cur_y + 1, cur_depth + 1))
        if cur_x != 0 and wallPosition[cur_x - 1][cur_y] == False: # left
            if ghost_dis < 0 and (cur_x - 1, cur_y) in ghostPositions and scaredTimes[ghostPositions.index((cur_x - 1, cur_y))] == 0:  # ghost still not found, is ghost, ghost is not scared
                ghost_dis = cur_depth
            elif food_depth < 0 and (cur_x - 1, cur_y) in foodPosition:  # never met food, has food
                food_depth = cur_depth
            else:
                frontier.append((cur_x - 1, cur_y, cur_depth + 1))
        if cur_x != width - 1 and wallPosition[cur_x + 1][cur_y] == False: # left
            if ghost_dis < 0 and (cur_x + 1, cur_y) in ghostPositions and scaredTimes[ghostPositions.index((cur_x + 1, cur_y))] == 0:  # ghost still not found, is ghost, ghost is not scared
                ghost_dis = cur_depth
            elif food_depth < 0 and (cur_x + 1, cur_y) in foodPosition:  # never met food, has food
                food_depth = cur_depth
            else:
                frontier.append((cur_x + 1, cur_y, cur_depth + 1))

    for cp in capsulePosition:
        cp_dis = manhattanDistance(cp, pos)
        score -= cp_dis

    if food_depth < 0:  # does not find food with bfs
        all_heu = []
        for food in foodPosition.asList():
            all_heu.append(manhattanDistance(pos, food))
        food_depth = min(all_heu)
    
    # if ghost_dis < 0 and ghost_dis == 0:
    #     return 1 / food_depth
    # print('food_depth', food_depth)
    # print('ghost_dis', ghost_dis)
    # if ghost_dis == 0:
    #     return float('inf')
    # return ((1 / food_depth) - (1 / ghost_dis))

    return (score - food_depth + ghost_dis)





# Abbreviation
better = betterEvaluationFunction
