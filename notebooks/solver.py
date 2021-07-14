from rubiks import *

class solver():
    def __init__(self, startCube, h = lambda x: 1):
        self.startCube = startCube
        self.h = h
        self.queue = [(startCube.duplicate(), [])]
        self.solution = None
        self.solutionFound = False
        
    def solve(self, maxDepth=6):
        while not self.solutionFound:
            queueItem = self.pop()
            cube = queueItem[0]
            moves = queueItem[1]
            if len(moves) <= maxDepth:
                if cube.checkSolved():
                    self.solution = moves
                    self.solutionFound = True
                else:
                    for m in MOVES:
                        if len(moves) == 0:
                            self.insert((cube.duplicate().move(m), moves + [m]))
                        elif m != OPP_MOVES[moves[-1]]:
                            self.insert((cube.duplicate().move(m), moves + [m]))
                            
        if self.solutionFound:
            print('Found Solution!')
            print(self.solution)
        else:
            print('Nopee')
        
    def insert(self, cube):
        self.queue.append(cube)
        self.queue.sort(reverse=True, key=self.h)
        
    def pop(self):
        cube = self.queue[0]
        self.queue = self.queue[1:]
        return cube