from rubiks import *

# solver class
class solver():
    # parameters:
    #     startCube (cube): the cube you want to solve
    #     h (function): the heuristic that you want the solver to use to solve the cube
    #           The heuristic function should take in a tuple of (c, moves),
    #           where c is the cube which you want to get a score of 
    #           and where moves is a list of moves that the cube took to get to its state from the startCube
    def __init__(self, startCube, h = lambda x: 1):
        self.startCube = startCube
        self.h = h
        self.queue = [(startCube.duplicate(), [])]
        self.solution = None
        self.solutionFound = False
    
    # run the solving algorithm (depth first search)
    # parameters:   
    #       maxDepth (int): the maximum number of moves that the solution should have.
    #       prune (bool, optional, default to True): if true, the algorithm will remove next steps that have a 
    #           lower heuristic score than its previous state.
    #       display (bool, optional, default to True): if true, will display the solution found if found, 
    #           or display the state with the best heuristic score and the moves it took to get there
    #       verbose (bool, optional, default to true): if true, will display the heuristic scores of all the 
    #           states that the solver is looking through.
    def solve(self, maxDepth=6, prune=True, display=True, verbose=True):
        # get the current score of the cube
        currentScore = self.h((self.startCube, None))

        # keep track of max score, and corresponding cube and moves to get there
        maxCube = self.startCube
        maxScore = currentScore
        maxMoves = []

        if verbose:
            print("The starting score of the cube is : {}".format(currentScore))

        # loop as long as the solution is not found
        while not self.solutionFound:
            # pop from the queue, break if there are no more items in the queue
            try:
                queueItem = self.pop()
            except:
                if verbose:
                    print("Oh no no more item in the queue")
                break

            # get the score of the new item
            currentScore = self.h(queueItem)
            if verbose:
                print("The next score of the cube is : {}".format(currentScore))

            (cube, moves) = queueItem

            # update the maxScore, maxCube, maxMoves
            if currentScore > maxScore:
                maxScore = currentScore
                maxCube = cube
                maxMoves = moves

            # before checking the state of the cube, check if has too many moves
            if len(moves) <= maxDepth:

                # if we got the solution, store it!
                if cube.checkSolved():
                    self.solution = moves
                    self.solutionFound = True

                # otherwise, loop through all the moves, add the new states of the cube to the queue
                #       (of course, we do some checking if the new states are valid)
                else:
                    for m in MOVES:
                        # check if valid move
                        #   opposite moves like R and R' are invalid moves
                        #   if no moves are done yet, then there are no invalid moves
                        isValidMove = False
                        if len(moves) == 0:
                            isValidMove = True
                        elif m != OPP_MOVES[moves[-1]]:
                            isValidMove = True

                        # if prune mode, check if score is higher before inserting
                        if isValidMove:
                            newQueueItem = (cube.duplicate().move(m), moves + [m])
                            if not prune:
                                self.insert((cube.duplicate().move(m), moves + [m]))
                            elif self.h(newQueueItem) >= currentScore:
                                self.insert((cube.duplicate().move(m), moves + [m]))
        
        # display the solution or max cube
        if display:
            if self.solutionFound:
                print('Found Solution!')
                print(self.solution)
            else:
                maxCube.view()
                print("Max score in iteration: {}".format(maxScore))
                print(maxMoves)
                print('No solution found')
    
    # inserts a new cube into the solver's queue
    #       parameters: 
    #           cube (cube): new cube
    def insert(self, cube):
        # add cube to queue
        self.queue.append(cube)

        # sort cubes in the queue in descending order according to heuristic score
        self.queue.sort(reverse=True, key=self.h)
    
    # removes and returns the first item in the queue
    def pop(self):
        cube = self.queue[0]
        self.queue = self.queue[1:]
        return cube