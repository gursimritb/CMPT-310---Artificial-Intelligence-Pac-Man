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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        #keep track of score 
        score = successorGameState.getScore()

        #idea - more points for being close to found, less points for being close to ghosts, unless it is scared

        #use mann dist
        from util import manhattanDistance

        #find nearest food
        food_tracker = newFood.asList()

        #check if food left
        if food_tracker:
            best_food = min(manhattanDistance(newPos, food) for food in food_tracker) #closest food
            score += 20/best_food #encouring Pac Man to move to the nearst food

        #check ghost pos
        for ghost in newGhostStates:
            dist_to_ghost = manhattanDistance(newPos, ghost.getPosition())
            scared_time = ghost.scaredTimer

            #check if ghost scared - not dangerous
            if scared_time > 0:
                score += 25/dist_to_ghost
            else:
                if dist_to_ghost > 0:
                    score -= 10/dist_to_ghost

        #Pac Man was stopping after running it, so deduct pointsw so it keeps moving
        if action == Directions.STOP:
            score -= 25

        return score

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        # idea - Pac Man wants to win or lose as quick as possible, multiple min layers for the multiple ghosts
        
        #value function
        def value(agentIndex, depth, gameState):
            #check if max depth hit or terminal state (win or lose)
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            #if Pac Man's turn - the max value
            if agentIndex == 0:
                return max_value(agentIndex, depth, gameState)
            
            #if ghost's turn - the min value
            else:
                return min_value(agentIndex, depth, gameState)

        #max value function - Pac Man
        def max_value(agentIndex, depth, gameState):

            #get the legal actions
            legal_actions = gameState.getLegalActions(agentIndex)

            #check if legal actions left
            if len(legal_actions) == 0:
                return self.evaluationFunction(gameState)

            #get max value
            max_value = -99999
            for action in legal_actions:
                successor_game = gameState.generateSuccessor(agentIndex, action)
                #based off the lecture slides
                max_value = max(max_value, value(1, depth, successor_game))
            return max_value

        #min value function - ghosts
        def min_value(agentIndex, depth, gameState):
            #get legal actions
            legal_actions = gameState.getLegalActions(agentIndex)

            #check if legal actions left
            if len(legal_actions) == 0:
                return self.evaluationFunction(gameState)

            #get min value
            min_value = 99999
            num_agents = gameState.getNumAgents()
            for action in legal_actions:
                successor_game = gameState.generateSuccessor(agentIndex,action)
                #check if last ghost
                if agentIndex == (num_agents - 1):
                    min_value = min(min_value, value(0, depth+1, successor_game))
                #not the last ghost, continue min value function with next ghost
                else:
                    min_value = min(min_value, value(agentIndex+1, depth, successor_game))
            return min_value

        #use the minmax algorithm, starting with Pac Man
        legal_actions = gameState.getLegalActions(0)
        best_action = None
        best_score = -99999

        #evaluate each action
        for action in legal_actions:
            #get the new state after Pac Man moves
            successor_game = gameState.generateSuccessor(0,action)
            #get score of next agent
            score = value(1,0, successor_game)
            if score > best_score:
                best_score = score
                best_action = action
        
        return best_action

        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # idea - keep structure same as minmax but add alpha and beta values for the best values overall 
        def value(agentIndex, depth, gameState, alpha, beta):
            #check if max depth hit or terminal state (win or lose)
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            #if Pac Man's turn - the max value
            if agentIndex == 0:
                return max_value(agentIndex, depth, gameState, alpha, beta)
            
            #if ghost's turn - the min value
            else:
                return min_value(agentIndex, depth, gameState, alpha, beta)
        
        #max value function - Pac Man
        def max_value(agentIndex, depth, gameState, alpha, beta):

            #get the legal actions
            legal_actions = gameState.getLegalActions(agentIndex)

            #check if legal actions left
            if len(legal_actions) == 0:
                return self.evaluationFunction(gameState)

            #get max value
            max_value = -99999
            for action in legal_actions:
                successor_game = gameState.generateSuccessor(agentIndex, action)
                #based off the lecture slides
                max_value = max(max_value, value(1, depth, successor_game, alpha, beta))
                
                #check if max value greater than beta
                if max_value > beta:
                    return max_value
                
                #update alpha
                alpha = max (alpha, max_value)
            
            return max_value
        
        #min value function - ghosts
        def min_value(agentIndex, depth, gameState, alpha, beta):
            #get legal actions
            legal_actions = gameState.getLegalActions(agentIndex)

            #check if legal actions left
            if len(legal_actions) == 0:
                return self.evaluationFunction(gameState)

            #get min value
            min_value = 99999
            num_agents = gameState.getNumAgents()
            for action in legal_actions:
                successor_game = gameState.generateSuccessor(agentIndex,action)
                
                #check if last ghost
                if agentIndex == (num_agents - 1):
                    min_value = min(min_value, value(0, depth+1, successor_game, alpha, beta))
                
                #not the last ghost, continue min value function with next ghost
                else:
                    min_value = min(min_value, value(agentIndex+1, depth, successor_game, alpha, beta))
            
                #check if min_value < alpha
                if min_value < alpha:
                    return min_value
                
                #update beta
                beta = min(beta, min_value)

            return min_value

        #use the updated minmax structure with alpha and beta algorithm, starting with Pac Man
        legal_actions = gameState.getLegalActions(0)
        best_action = None
        best_score = -99999
        alpha = -99999
        beta = 99999

        #evaluate each action
        for action in legal_actions:
            #get the new state after Pac Man moves
            successor_game = gameState.generateSuccessor(0,action)
            
            #get score of next agent
            score = value(1,0, successor_game, alpha, beta)
            if score > best_score:
                best_score = score
                best_action = action
            
            #compare score and beta to prune
            if score > beta:
                return best_action
            
            #update alpha because goal is to maximize Pac Man's score
            alpha = max(alpha,score)
    
        return best_action

        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #idea - use max function for Pac Man with num_agents, change the min function to an expected value funstion for ghosts
                
        #value function
        def value(agentIndex, depth, gameState):
            #check if max depth hit or terminal state (win or lose)
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            #if Pac Man's turn - the max value
            if agentIndex == 0:
                return max_value(agentIndex, depth, gameState)
            
            #if ghost's turn - the min value
            else:
                return exp_value(agentIndex, depth, gameState)

        #max value function - Pac Man
        def max_value(agentIndex, depth, gameState):

            #get the legal actions
            legal_actions = gameState.getLegalActions(agentIndex)

            #check if legal actions left
            if len(legal_actions) == 0:
                return self.evaluationFunction(gameState)

            #get max value
            max_value = -99999
            for action in legal_actions:
                successor_game = gameState.generateSuccessor(agentIndex, action)
                
                #based off the lecture slides, use agentIndex+1 to get the next agent
                max_value = max(max_value, value(1, depth, successor_game))
            
            return max_value

        #exp_value function - ghosts
        def exp_value(agentIndex, depth, gameState):
            #get legal actions
            legal_actions = gameState.getLegalActions(agentIndex)

            #check if legal actions left
            if len(legal_actions) == 0:
                return self.evaluationFunction(gameState)

            #get exp value, num_agents, total_actions, prob
            expected_value = 0
            num_agents = gameState.getNumAgents()
            total_actions = len(legal_actions)
            prob = 1/total_actions #assuming all uniform cost

            #loop over actions
            for action in legal_actions:
                successor_game = gameState.generateSuccessor(agentIndex,action)
                
                #check if last ghost
                if agentIndex == (num_agents - 1):
                    expected_value += prob * value(0, depth+1, successor_game)

                #not the last ghost, continue exp_value function with next ghost
                else:
                    expected_value += prob * value(agentIndex+1, depth, successor_game)
            
            return expected_value

        #use the expectimax algorithm, starting with Pac Man
        legal_actions = gameState.getLegalActions(0)
        best_action = None
        best_score = -99999

        #evaluate each action
        for action in legal_actions:

            successor_game = gameState.generateSuccessor(0,action)
            
            #get score of next agent
            score = value(1,0, successor_game)
            if score > best_score:
                best_score = score
                best_action = action
        
        return best_action
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: I took the base from what I did in Q1 and used GameState instead of successorGameState.
    I also added to the score when there is a capsule nearby and subtracted from the score if food is left. 

    """
    "*** YOUR CODE HERE ***"
    #extracting information from the current game state
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghost_states = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    
    #keep track of score 
    score = currentGameState.getScore()

    #use mann dist
    from util import manhattanDistance

    #find nearest food
    food_tracker = food.asList()

    #check if food left
    if food_tracker:
        best_food = min(manhattanDistance(pos, food) for food in food_tracker) #closest food
        score += 20/best_food #encouring Pac Man to move to the nearst food

    #push Pac Man to eat all the food, and win as soon as posible 
    amount_food_left = len(food_tracker)
    if amount_food_left > 0:
        score -= 10
    
    #check if capsules left
    if capsules:
        best_cap = min (manhattanDistance(pos,capsule) for capsule in capsules)
        score += 25/best_cap #encouraging Pac Man to move to the capsules over the food

    #check ghost pos
    for ghost in ghost_states:
        dist_to_ghost = manhattanDistance(pos, ghost.getPosition())
        scared_time = ghost.scaredTimer

        #check if ghost scared - not dangerous and Pac Man can eat it
        if scared_time > 0:
            score += 25/dist_to_ghost
        else:
            #if ghost not scared, Pac Man should stay away
            if dist_to_ghost > 0:
                score -= 10/dist_to_ghost 

    #Pac Man was stops, so increase a negative score to keep him moving
    if currentGameState.getPacmanState().getDirection() == Directions.STOP:
        score -= 25
    
    return score
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
