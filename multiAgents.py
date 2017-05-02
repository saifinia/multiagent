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
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        xy3 = successorGameState.getCapsules()
        xy2=newFood.asList()
        stopscore=0
        i,distance01=1,0
        if action=="Stop":
            stopscore=-1000
        for x1, y1 in xy2:
            distance01 = distance01 + (abs(newPos[0] - x1) + abs(newPos[1] - y1))
            i = i + 1
        preGhostPosition=currentGameState.getGhostPosition(1)
        preGhostDistance=util.manhattanDistance(preGhostPosition,newPos)
        if preGhostDistance>3:
            preGhostDistance=3
        return preGhostDistance+successorGameState.getScore()-\
               distance01/i-100*len(xy3)+stopscore
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
        self.pacmanIndex = 0

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

        numagents = gameState.getNumAgents() - 1
        depth = self.depth
        positiveinfinite = float('Inf')
        negativeinfinite = -float('Inf')
        maxvaluewithaction = []

        def max_value(gameState, depth, numofagents):
            maxvalues = [negativeinfinite]
            if gameState.isWin() is True or gameState.isLose() is True or depth == 0:
                return self.evaluationFunction(gameState)
            agentlegalactions = gameState.getLegalActions(0)
            for action in agentlegalactions:
                if action == "Stop":
                    continue
                successorstate = gameState.generateSuccessor(0, action)
                maxvalues.append(min_value(successorstate, depth, 1, numofagents))
            return max(maxvalues)

        def min_value(gameState, depth, agentindex, numofagents):
            minvalues = [positiveinfinite]
            if gameState.isWin() is True or gameState.isLose() is True or depth == 0:
                return self.evaluationFunction(gameState)
            if agentindex < numofagents:
                agentlegalactions = gameState.getLegalActions(agentindex)
                for action in agentlegalactions:
                    if action == "Stop":
                        continue
                    successorstate = gameState.generateSuccessor(agentindex, action)
                    minvalues.append(min_value(successorstate, depth, agentindex + 1, numofagents))
                return min(minvalues)
            if agentindex >= numofagents:
                agentlegalactions = gameState.getLegalActions(agentindex)
                for action in agentlegalactions:
                    if action == "Stop":
                        continue
                    successorstate = gameState.generateSuccessor(agentindex, action)
                    minvalues.append(max_value(successorstate, depth - 1, numofagents))
                return min(minvalues)

        if gameState.isWin() is True or gameState.isLose() is True or depth == 0:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(0):
            if action == "Stop":
                continue
            successorstate = gameState.generateSuccessor(0, action)
            maxvaluewithaction.append((action, min_value(successorstate, depth, 1, numagents)))
        value = negativeinfinite
        for action, minvalue in maxvaluewithaction:
            if minvalue > value:
                value = minvalue
                argaction = action
        return argaction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numagents = gameState.getNumAgents() - 1
        depth = self.depth
        positiveinfinite = float('Inf')
        negativeinfinite = -float('Inf')
        def max_value(gameState,alpha,beta,depth,numofagents):
            if gameState.isWin() is True or gameState.isLose() is True or depth == 0:
                return self.evaluationFunction(gameState)
            v=negativeinfinite
            for action in gameState.getLegalActions(0):
                if action == "Stop":
                    continue
                successor=gameState.generateSuccessor(0,action)
                v=max(v,min_value(successor,alpha,beta,depth,1,numofagents))
                if v>beta: return v
                alpha=max(alpha,v)
            return v
        def min_value(gameState,alpha,beta,depth,agentindex,numofagents):
            if gameState.isWin() is True or gameState.isLose() is True or depth == 0:
                return self.evaluationFunction(gameState)
            v=positiveinfinite
            if agentindex < numofagents:
                for action in gameState.getLegalActions(agentindex):
                    if action=="Stop":
                        continue
                    successor=gameState.generateSuccessor(agentindex,action)
                    v=min(v,min_value(successor,alpha,beta,depth,agentindex+1,numofagents))
                    if v<alpha: return v
                    beta=min(beta,v)
                return v
            if agentindex >= numofagents:
                for action in gameState.getLegalActions(agentindex):
                    if action=="Stop":
                        continue
                    successor=gameState.generateSuccessor(agentindex,action)
                    v=min(v,max_value(successor,alpha,beta,depth-1,numofagents))
                    if v<alpha: return v
                    beta=min(beta,v)
                return v
        v=negativeinfinite
        alpha=negativeinfinite
        beta=positiveinfinite
        if gameState.isWin() is True or gameState.isLose() is True or depth == 0:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(0):
            if action == "Stop":
                continue
            successor = gameState.generateSuccessor(0, action)
            minvalue=min_value(successor, alpha,beta, depth, 1, numagents)
            if minvalue>v:
                argaction=action
                v=minvalue
            if v > positiveinfinite: return action
            alpha = max(alpha, v)
        return argaction

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
        numagents = gameState.getNumAgents() - 1
        depth = self.depth
        positiveinfinite = float('Inf')
        negativeinfinite = -float('Inf')
        def max_value(gameState,alpha,beta,depth,numofagents):
            if gameState.isWin() is True or gameState.isLose() is True or depth == 0:
                return self.evaluationFunction(gameState)
            v=negativeinfinite
            for action in gameState.getLegalActions(0):
                if action == "Stop":
                    continue
                successor=gameState.generateSuccessor(0,action)
                v=max(v,min_value(successor,alpha,beta,depth,1,numofagents))
                if v>beta: return v
                alpha=max(alpha,v)
            return v
        def min_value(gameState,alpha,beta,depth,agentindex,numofagents):
            if gameState.isWin() is True or gameState.isLose() is True or depth == 0:
                return self.evaluationFunction(gameState)
            v=0
            i=0
            if agentindex < numofagents:
                for action in gameState.getLegalActions(agentindex):
                    if action=="Stop":
                        continue
                    successor=gameState.generateSuccessor(agentindex,action)
                    v=v+min_value(successor,alpha,beta,depth,agentindex+1,numofagents)
                    i=i+1
                return v/i
            if agentindex>=numofagents:
                for action in gameState.getLegalActions(agentindex):
                    if action=="Stop":
                        continue
                    successor=gameState.generateSuccessor(agentindex,action)
                    v=v+max_value(successor,alpha,beta,depth-1,numofagents)
                    i=i+1
                return v/i
        v=negativeinfinite
        alpha=negativeinfinite
        beta=positiveinfinite
        if gameState.isWin() is True or gameState.isLose() is True or depth == 0:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(0):
            if action == "Stop":
                continue
            successor = gameState.generateSuccessor(0, action)
            minvalue=min_value(successor, alpha,beta, depth, 1, numagents)
            if minvalue>v:
                argaction=action
                v=minvalue
            if v > positiveinfinite: return action
            alpha = max(alpha, v)
        return argaction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
     (1)The distance between ghost and gamestate should be considered when evaluating the score of
     current state. So I divided the distance in two groups: manhatten distance <= 3
     and manhatten distance > 3. If the manhatten distance is far enough, it should get the same effect.
     (2) The distance between pacman and food is also important. However, too much food in this graphic so
     I have to consider the mean of all the food.
     (3) The capsule length should also be considered. I found that during my experience, the multiple should be large
     and the pacman will run well.
    """
    "*** YOUR CODE HERE ***"
    xy1 = currentGameState.getPacmanPosition()
    xy2 = currentGameState.getFood()
    xy3=currentGameState.getCapsules()
    numofagents=currentGameState.getNumAgents()
    xy2=xy2.asList()
    distance00=float('Inf')
    distance01=0
    i=1
    for j in range(1,numofagents):
        x0,y0=currentGameState.getGhostPosition(j)
        distance00=min(distance00,abs(xy1[0] - x0) + abs(xy1[1] - y0))
    if distance00>3:
        distance00=3
    for x1, y1 in xy2:
        distance01 = distance01+(abs(xy1[0] - x1) + abs(xy1[1] - y1))
        i=i+1
    return distance00-distance01/i-50*len(xy3)+currentGameState.getScore()


# Abbreviation
better = betterEvaluationFunction

