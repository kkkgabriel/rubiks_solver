from rubiks import *

class solver():
    def __init__(self, startCube, h = lambda x: 1):
        self.startCube = startCube
        self.h = h
        self.queue = [(startCube.duplicate(), [])]
        self.solution = None
        self.solutionFound = False
        
    def solve(self, maxDepth=6, prune=True, display=True, verbose=True):
        currentScore = self.h((self.startCube, None))

        # keep track of max scores
        maxCube = self.startCube
        maxScore = currentScore
        maxMoves = []

        if verbose:
            print("The starting score of the cube is : {}".format(currentScore))
        while not self.solutionFound:
            try:
                queueItem = self.pop()
            except:
                if verbose:
                    print("Oh no no more item in the queue")
                break

            currentScore = self.h(queueItem)
            if verbose:
                print("The next score of the cube is : {}".format(currentScore))


            cube = queueItem[0]
            moves = queueItem[1]

            if currentScore > maxScore:
                maxScore = currentScore
                maxCube = cube
                maxMoves = moves

            if len(moves) <= maxDepth:
                if cube.checkSolved():
                    self.solution = moves
                    self.solutionFound = True
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
        
        if display:
            if self.solutionFound:
                print('Found Solution!')
                print(self.solution)
            else:
                maxCube.view()
                print("Max score in iteration: {}".format(maxScore))
                print(maxMoves)
                print('No solution found')
            
    def insert(self, cube):
        self.queue.append(cube)
        self.queue.sort(reverse=True, key=self.h)
        
    def pop(self):
        cube = self.queue[0]
        self.queue = self.queue[1:]
        return cube