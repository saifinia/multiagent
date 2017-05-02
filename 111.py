"*** YOUR CODE HERE ***"
numagents = gameState.getNumAgents() - 1
depth = self.depth * (numagents)
positiveinfinite = float('Inf')
negativeinfinite = -float('Inf')
maxvaluewithaction = []


def max_value(gameState, depth, numofagents):
    maxvalues = [negativeinfinite]
    if gameState.isWin() is True or gameState.isLose() is True or depth == 0:
        return self.evaluationFunction(gameState)
    agentlegalactions = gameState.getLegalActions(0)
    for action in agentlegalactions:
        successorstate = gameState.generateSuccessor(0, action)
        if action == "Stop":
            continue
        maxvalues.append(min_value(successorstate, depth - 1, 1, numofagents))
    return max(maxvalues)


def min_value(gameState, depth, agentindex, numofagents):
    minvalues = [positiveinfinite]
    if gameState.isWin() is True or gameState.isLose() is True or depth == 0:
        return self.evaluationFunction(gameState)
    if agentindex < numofagents:
        agentlegalactions = gameState.getLegalActions(agentindex)
        for action in agentlegalactions:
            successorstate = gameState.generateSuccessor(agentindex, action)
            if action == "Stop":
                continue
            minvalues.append(min_value(successorstate, depth - 1, agentindex + 1, numofagents))
        return min(minvalues)
    if agentindex == numofagents:
        agentlegalactions = gameState.getLegalActions(agentindex)
        for action in agentlegalactions:
            successorstate = gameState.generateSuccessor(agentindex, action)
            if action == "Stop":
                continue
            minvalues.append(max_value(successorstate, depth - 1, numofagents))
        return min(minvalues)


for action in gameState.getLegalActions(1):
    successorstate = gameState.generateSuccessor(1, action)
    maxvaluewithaction.append((action, min_value(successorstate, depth, 1, numagents)))
value = negativeinfinite
for action, minvalue in maxvaluewithaction:
    if minvalue > value:
        value = minvalue
        argaction = action
return argaction