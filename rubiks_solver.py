from solver import *
from rubiks import *
from heuristics import *

def solve(state):
	c = cube(colours=state)
	s = solver(c, h=adaptedCFOP2)
	s.solve(maxDepth=10, display=False, verbose=False, earlyTermination=1000)
	if s.solutionFound:
		return s.solution
	return None