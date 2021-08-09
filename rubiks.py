from PIL import Image
import requests
from io import BytesIO
from random import randint
from copy import deepcopy

# just some moves that the cube has
MOVES = [
	"U", "U'",
	"D", "D'",
	"R", "R'",
	"L", "L'",
	"F", "F'",
	"B", "B'"
]

OPP_MOVES = {
    "U": "U'",
    "U'": "U",
    "D": "D'",
    "D'": "D",
    "R": "R'",
    "R'": "R",
    "L": "L'",
    "L'": "L",
    "F": "F'",
    "F'": "F",
    "B": "B'",
    "B'": "B"
}

# generate a scramble with n steps
def generateScramble(n):
    moves = [MOVES[randint(0, len(MOVES)-1)] for i in range(n)]
    for i in range(1,n):
        if moves[i-1] == OPP_MOVES[moves[i]]: 
            filtered_moves = deepcopy(MOVES)
            filtered_moves.remove(moves[i])
            moves[i] = filtered_moves[randint(0, len(filtered_moves)-1)]
    return ' '.join(moves)

# class of a cube 
class cube:
    # specify a string of 54 chars which correspond to the colours on the cube
    def __init__(self, colours='yyyyyyyyyrrrrrrrrrbbbbbbbbbwwwwwwwwwoooooooooggggggggg'):
        colours = list(colours)
        self.u = {i: n for i,n in enumerate(colours[0:9])} # y
        self.r = {i: n for i,n in enumerate(colours[9:18])} # r
        self.f = {i: n for i,n in enumerate(colours[18:27])} # b
        self.d = {i: n for i,n in enumerate(colours[27:36])} # w
        self.l = {i: n for i,n in enumerate(colours[36:45])} # o
        self.b = {i: n for i,n in enumerate(colours[45:54])} # g
        self.faces = [self.u, self.r, self.f, self.d, self.l, self.b]
        self.moves = []
        
    # make multiple moves by passing a single string
    #   parameters:
    #       moves (str): moves that you want the cube to execute, should exist in MOVES
    #           Note: these moves should be separated by a space, prime moves can be denoted using "'"
    #           Eg: c.move("R U R' U")
    def move(self, moves):
        # replace all "'" with "p"
        moves = moves.replace("'", "p")

        # split moves by \s
        moves = moves.split()

        # loop through all moves and execute
        for move in moves:
            self.singleMove(move)
        return self
    
    # make single moves by passsing a single string
    #   parameters:
    #       move (str): move that you want the cube to execute, should exist in MOVES
    def singleMove(self, move):
        eval('self.{}()'.format(move))
        return self
        
    # check if the cube is solved by checking that all faces have the same color
    def checkSolved(self):
        for faces in self.faces:
            faceValues = list(faces.values())
            if faceValues.count(faceValues[0]) != len(faceValues):
                return False
        return True
    
    #--------- misc -----------#
    # view the cube from the front
    #   parameters:
    #       bottom (bool): view the front from the bottom, default to False
    def view(self, bottom=False):
        hyphen = ''
        if not bottom:
            hyphen = '-'
        url = 'http://cube.rider.biz/visualcube.php?fmt=jpeg&size=150&r=y45x{}34&fc='.format(hyphen)
        state = self.getState()
        full_url = url + state

        response = requests.get(full_url)
        im = Image.open(BytesIO(response.content))
        display(im)

    # view the cube from the back
    #   parameters:
    #       bottom (bool): view the back from the bottom, default to False
    def view_back(self, bottom=False):
        hyphen = ''
        if not bottom:
            hyphen = '-'
        url = 'http://cube.rider.biz/visualcube.php?fmt=jpeg&size=150&r=y225x{}34&fc='.format(hyphen)
        state = self.getState()
        full_url = url + state

        response = requests.get(full_url)
        im = Image.open(BytesIO(response.content))
        display(im)

    # view the cube from the right
    #   parameters:
    #       bottom (bool): view the right from the bottom, default to False
    def view_right(self, bottom=False):
        hyphen = ''
        if not bottom:
            hyphen = '-'
        url = 'http://cube.rider.biz/visualcube.php?fmt=jpeg&size=150&r=y135x{}34&fc='.format(hyphen)
        state = self.getState()
        full_url = url + state

        response = requests.get(full_url)
        im = Image.open(BytesIO(response.content))
        display(im)

    # view the cube from the left
    #   parameters:
    #       bottom (bool): view the left from the bottom, default to False
    def view_left(self, bottom=False):
        hyphen = ''
        if not bottom:
            hyphen = '-'
        url = 'http://cube.rider.biz/visualcube.php?fmt=jpeg&size=150&r=y315x{}34&fc='.format(hyphen)
        state = self.getState()
        full_url = url + state

        response = requests.get(full_url)
        im = Image.open(BytesIO(response.content))
        display(im)
    
    # gets the state of the cube as a string of 54 chars, representing each of its colours
    #   Note: this is useful to check the state of the cube and developing heuristics
    def getState(self):
        return ''.join(
            list(self.u.values()) + \
            list(self.r.values()) + \
            list(self.f.values()) + \
            list(self.d.values()) + \
            list(self.l.values()) + \
            list(self.b.values()) \
        )

    # returns a new cube object with the same state as the current
    def duplicate(self):
        return cube(self.getState())
    
    #--------- M -----------#
    def M(self):
        self.f[1], self.f[4], self.f[7], self.u[1], self.u[4], self.u[7], self.b[7], self.b[4], self.b[1], self.d[1], self.d[4], self.d[7] = \
        self.u[1], self.u[4], self.u[7], self.b[7], self.b[4], self.b[1], self.d[1], self.d[4], self.d[7], self.f[1], self.f[4], self.f[7]
        return self
    
    def Mp(self):
        self.f[1], self.f[4], self.f[7], self.u[1], self.u[4], self.u[7], self.b[7], self.b[4], self.b[1], self.d[1], self.d[4], self.d[7] = \
        self.d[1], self.d[4], self.d[7], self.f[1], self.f[4], self.f[7], self.u[1], self.u[4], self.u[7], self.b[7], self.b[4], self.b[1]
        return self
    
    #--------- E -----------#
    def E(self):
        self.r[3], self.r[4], self.r[5], self.f[3], self.f[4], self.f[5], self.l[3], self.l[4], self.l[5], self.b[3], self.b[4], self.b[5] = \
        self.f[3], self.f[4], self.f[5], self.l[3], self.l[4], self.l[5], self.b[3], self.b[4], self.b[5], self.r[3], self.r[4], self.r[5]
        return self
        
    def Ep(self):
        self.r[3], self.r[4], self.r[5], self.f[3], self.f[4], self.f[5], self.l[3], self.l[4], self.l[5], self.b[3], self.b[4], self.b[5] = \
        self.b[3], self.b[4], self.b[5], self.r[3], self.r[4], self.r[5], self.f[3], self.f[4], self.f[5], self.l[3], self.l[4], self.l[5]
        return self
    
    #--------- S -----------#
    def S(self):
        self.u[3], self.u[4], self.u[5], self.r[1], self.r[4], self.r[7], self.d[5], self.d[4], self.d[3], self.l[7], self.l[4], self.l[1] = \
        self.l[7], self.l[4], self.l[1], self.u[3], self.u[4], self.u[5], self.r[1], self.r[4], self.r[7], self.d[5], self.d[4], self.d[3]
        return self
    
    def Sp(self):
        self.u[3], self.u[4], self.u[5], self.r[1], self.r[4], self.r[7], self.d[5], self.d[4], self.d[3], self.l[7], self.l[4], self.l[1] = \
        self.r[1], self.r[4], self.r[7], self.d[5], self.d[4], self.d[3], self.l[7], self.l[4], self.l[1], self.u[3], self.u[4], self.u[5]
        return self
        
    #--------- B -----------#
    def B(self):
        self._rotateFace(self.b)
        self.u[0], self.u[1], self.u[2], self.r[2], self.r[5], self.r[8], self.d[8], self.d[7], self.d[6], self.l[6], self.l[3], self.l[0] = \
        self.r[2], self.r[5], self.r[8], self.d[8], self.d[7], self.d[6], self.l[6], self.l[3], self.l[0], self.u[0], self.u[1], self.u[2]
        return self
    
    def Bp(self):
        self._rotateFace(self.b, False)
        self.u[0], self.u[1], self.u[2], self.r[2], self.r[5], self.r[8], self.d[8], self.d[7], self.d[6], self.l[6], self.l[3], self.l[0] = \
        self.l[6], self.l[3], self.l[0], self.u[0], self.u[1], self.u[2], self.r[2], self.r[5], self.r[8], self.d[8], self.d[7], self.d[6]
        return self
    
        
    #--------- F -----------#
    def F(self):
        self._rotateFace(self.f)
        self.u[6], self.u[7], self.u[8], self.r[0], self.r[3], self.r[6], self.d[2], self.d[1], self.d[0], self.l[8], self.l[5], self.l[2] = \
        self.l[8], self.l[5], self.l[2], self.u[6], self.u[7], self.u[8], self.r[0], self.r[3], self.r[6], self.d[2], self.d[1], self.d[0]
        return self
    
    def Fp(self):
        self._rotateFace(self.f, False)
        self.u[6], self.u[7], self.u[8], self.r[0], self.r[3], self.r[6], self.d[2], self.d[1], self.d[0], self.l[8], self.l[5], self.l[2] = \
        self.r[0], self.r[3], self.r[6], self.d[2], self.d[1], self.d[0], self.l[8], self.l[5], self.l[2], self.u[6], self.u[7], self.u[8]
        return self
        
    #--------- L -----------#
    def L(self):
        self._rotateFace(self.l)
        self.f[0], self.f[3], self.f[6], self.u[0], self.u[3], self.u[6], self.b[8], self.b[5], self.b[2], self.d[0], self.d[3], self.d[6] = \
        self.u[0], self.u[3], self.u[6], self.b[8], self.b[5], self.b[2], self.d[0], self.d[3], self.d[6], self.f[0], self.f[3], self.f[6]
        return self
        
        
    def Lp(self):
        self._rotateFace(self.l, False)
        self.f[0], self.f[3], self.f[6], self.u[0], self.u[3], self.u[6], self.b[8], self.b[5], self.b[2], self.d[6], self.d[3], self.d[0] = \
        self.d[0], self.d[3], self.d[6], self.f[0], self.f[3], self.f[6], self.u[0], self.u[3], self.u[6], self.b[8], self.b[5], self.b[2]
        return self
        
    #--------- R -----------#
    def R(self):
        self._rotateFace(self.r)
        self.f[2], self.f[5], self.f[8], self.u[2], self.u[5], self.u[8], self.b[6], self.b[3], self.b[0], self.d[2], self.d[5], self.d[8] = \
        self.d[2], self.d[5], self.d[8], self.f[2], self.f[5], self.f[8], self.u[2], self.u[5], self.u[8], self.b[6], self.b[3], self.b[0]
        return self
    
    def Rp(self):
        self._rotateFace(self.r, False)
        self.f[2], self.f[5], self.f[8], self.u[2], self.u[5], self.u[8], self.b[6], self.b[3], self.b[0], self.d[2], self.d[5], self.d[8] = \
        self.u[2], self.u[5], self.u[8], self.b[6], self.b[3], self.b[0], self.d[2], self.d[5], self.d[8], self.f[2], self.f[5], self.f[8]
        return self
    
    
    #--------- D -----------#
    def D(self):
        self._rotateFace(self.d)
        self.r[6], self.r[7], self.r[8], self.f[6], self.f[7], self.f[8], self.l[6], self.l[7], self.l[8], self.b[6], self.b[7], self.b[8] = \
        self.f[6], self.f[7], self.f[8], self.l[6], self.l[7], self.l[8], self.b[6], self.b[7], self.b[8], self.r[6], self.r[7], self.r[8]
        return self
    
    def Dp(self):
        self._rotateFace(self.d, False)
        self.r[6], self.r[7], self.r[8], self.f[6], self.f[7], self.f[8], self.l[6], self.l[7], self.l[8], self.b[6], self.b[7], self.b[8] = \
        self.b[6], self.b[7], self.b[8], self.r[6], self.r[7], self.r[8], self.f[6], self.f[7], self.f[8], self.l[6], self.l[7], self.l[8]
        return self
    
    #--------- U -----------#    
    def U(self):
        self._rotateFace(self.u)
        self.r[0], self.r[1], self.r[2], self.f[0], self.f[1], self.f[2], self.l[0], self.l[1], self.l[2], self.b[0], self.b[1], self.b[2] = \
        self.b[0], self.b[1], self.b[2], self.r[0], self.r[1], self.r[2], self.f[0], self.f[1], self.f[2], self.l[0], self.l[1], self.l[2]
        return self
    
    def Up(self):
        self._rotateFace(self.u, False)
        self.r[0], self.r[1], self.r[2], self.f[0], self.f[1], self.f[2], self.l[0], self.l[1], self.l[2], self.b[0], self.b[1], self.b[2] = \
        self.f[0], self.f[1], self.f[2], self.l[0], self.l[1], self.l[2], self.b[0], self.b[1], self.b[2], self.r[0], self.r[1], self.r[2]
        return self

    #--------- private -----------#    
    def _rotateFace(self, face, clockwise=True):
        newFace = '630741852'
        if not clockwise:
            newFace = '258147036'
        newFace = list(newFace)
        face[0], face[1], face[2], face[3], face[4], face[5], face[6], face[7], face[8] = \
        face[int(newFace[0])], face[int(newFace[1])], face[int(newFace[2])], face[int(newFace[3])], face[int(newFace[4])], face[int(newFace[5])], face[int(newFace[6])], face[int(newFace[7])], face[int(newFace[8])] 
        
        