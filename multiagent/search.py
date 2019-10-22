# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from collections import deque


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    visited_cell = []
    stacks = util.Stack()
    stacks.push((problem.getStartState(), ((-1, -1), None)))
    go_to_previous = {}
    final_cell = []
    while not stacks.isEmpty():
        current = stacks.pop()
        current_cell = current[0]
        if current_cell in visited_cell:
            continue
        visited_cell.append(current_cell)
        go_to_previous[current_cell] = current[1]
        if problem.isGoalState(current_cell):
            final_cell = current_cell
            break
        list_of_adj = problem.getSuccessors(current_cell)
        for adj_cell in list_of_adj:
            stacks.push((adj_cell[0], (current_cell, adj_cell[1])))
    # Trace the path
    res = []
    while True:
        prev = go_to_previous[final_cell]
        prev_cell = prev[0]
        prev_dir = prev[1]
        res.append(prev_dir)
        if problem.getStartState() == prev_cell:
            break
        final_cell = prev_cell
    res = res[::-1] #reverse path
    return res

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited_cell = []
    queue = util.Queue()
    start_state = problem.getStartState()
    queue.push((start_state, (start_state, None)))
    go_to_previous = {}
    final_cell = []
    while not queue.isEmpty() > 0:
        current = queue.pop()
        current_cell = current[0]
        # print(current_cell)
        if current_cell in visited_cell:
            continue
        visited_cell.append(current_cell)
        go_to_previous[current_cell] = current[1]
        if problem.isGoalState(current_cell):
            final_cell = current_cell
            break
        list_of_adj = problem.getSuccessors(current_cell)
        for adj_cell in list_of_adj:
            # print(adj_cell)
            queue.push((adj_cell[0], (current_cell, adj_cell[1])))
    # Trace the path
    res = []
    while True:
        prev = go_to_previous[final_cell]
        prev_cell = prev[0]
        prev_dir = prev[1]
        res.append(prev_dir)
        if problem.getStartState() == prev_cell:
            break
        final_cell = prev_cell
    res = res[::-1] #reverse path
    # print(len(res))
    return res
    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    dist = {}
    visited_cell = []
    pq = util.PriorityQueue()
    pq.push((problem.getStartState(), ((-1, -1), None)), 0)
    dist[problem.getStartState()] = 0
    go_to_previous = {}
    final_cell = []
    while not pq.isEmpty():
        current = pq.pop()
        current_cell = current[0]
        if current_cell in visited_cell:
            continue
        visited_cell.append(current_cell)
        go_to_previous[current_cell] = current[1]
        if problem.isGoalState(current_cell):
            final_cell = current_cell
            break
        list_of_adj = problem.getSuccessors(current_cell)
        for adj_cell in list_of_adj:
            cost = adj_cell[2]
            if adj_cell[0] not in visited_cell:
                dist[adj_cell[0]] = 1000000000000000000000
            if dist[current_cell] + cost < dist[adj_cell[0]]:
                dist[adj_cell[0]] = dist[current_cell] + cost
                pq.push((adj_cell[0], (current_cell, adj_cell[1])), dist[adj_cell[0]])
    # Trace the path
    res = []
    while True:
        prev = go_to_previous[final_cell]
        prev_cell = prev[0]
        prev_dir = prev[1]
        res.append(prev_dir)
        if problem.getStartState() == prev_cell:
            break
        final_cell = prev_cell
    res = res[::-1] #reverse path
    return res

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    dist = {}
    visited_cell = []
    pq = util.PriorityQueue()
    start_state = problem.getStartState()
    dist[start_state] = 0
    pq.push((start_state, ((-1, -1), None)), dist[start_state])
    go_to_previous = {}
    final_cell = []
    while not pq.isEmpty():
        current = pq.pop()
        current_cell = current[0]
        if current_cell in visited_cell:
            continue
        visited_cell.append(current_cell)
        go_to_previous[current_cell] = current[1]
        if problem.isGoalState(current_cell):
            final_cell = current_cell
            break
        list_of_adj = problem.getSuccessors(current_cell)
        for adj_cell in list_of_adj:
            cost = adj_cell[2]
            if adj_cell[0] not in visited_cell:
                dist[adj_cell[0]] = 1000000000000000000000
            if dist[current_cell] + cost< dist[adj_cell[0]]:
                dist[adj_cell[0]] = dist[current_cell] + cost
                prio = dist[adj_cell[0]] + heuristic(adj_cell[0], problem) 
                pq.push((adj_cell[0], (current_cell, adj_cell[1])), prio)
    # Trace the path
    res = []
    while True:
        prev = go_to_previous[final_cell]
        prev_cell = prev[0]
        prev_dir = prev[1]
        res.append(prev_dir)
        if start_state == prev_cell:
            break
        final_cell = prev_cell
    res = res[::-1] #reverse path
    return res
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
