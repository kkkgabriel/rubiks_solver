#------------- increments -----------------#
numberOfPairedCornerNEdges_i = 5
numberOfPairedCornerNEdges_d = 2
oneStepCornerEdgePair_i = 3
oneStepCornerEdgePair_d = 1
middleEdgePairing_i = 2

#------------- piece index (DO NOT REARRANGE) -----------------#
top_corners = [ # clockwise starting from top piece
    [8,9,20],[2,45,11],[0,36,47],[6,18,38]
]
bottom_corners = [ # clockwise starting from top piece
    [29,26,15],[35,17,51],[33,53,42],[27,44,24]
]
top_middle_centers = [ # uf, ul, ub, ur
    [4,22], [4,40], [4,49],[4,13]
]
middle_centers = [ # fl,lb,br,rf
    [13,22], [22,40], [40,49], [49,13],
]
bottom_middle_centers = [ # df, dl, db, dr
    [31,22], [31,40], [31,49],[31,13]
]
top_edges = [
    [7,19],[3,37],[1,46],[5,10]
]
side_edges = [
    [12,23],[21,41],[39,50],[48,14] # clockwise from top
]
bottom_edges = [
    [28,25],[30,43],[34,52], [32,16]
]

#------------ counting the number of correct colors on face ------------#
def numberOfCorrectColorsOnFace(queueItem):
    cube = queueItem[0]
    score = 0
    for face in cube.faces:
        center = face[4]
        score += list(face.values()).count(center)
    return score

# -------------- counting number of top corner-edge pairs matched ----------- #
top_pairs = [[[6,7], [18,19]],[[7,8], [19,20]],[[5,6],[9,10]],[[2,5],[10,11]],[[1,2],[45,46]],[[0,1],[46,47]],[[0,3],[36,37]],[[3,6],[37,38]]]
mid_pairs = [[[9,12],[20,24]],[[23,26],[12,15]],[[45,48],[11,14]],[[48,51],[14,17]],[[47,50],[36,39]],[[50,53],[39,42]],[[38,41],[18,21]],[[41,44],[21,24]]]
bottom_pairs = [[[27,28],[24,25]],[[28,29],[25,26]],[[29,32],[15,16]],[[32,35],[16,17]],[[34,35],[51,52]],[[33,34],[52,53]],[[30,33],[42,43]],[[27,30],[43,44]]]
corner_edge_pairs = top_pairs + mid_pairs + bottom_pairs
def numberOfPairedCornerNEdges(queueItem):
    cube = queueItem[0]
    score = 0
    state = cube.getState()
    for pair in corner_edge_pairs:
        (p1, p2) = pair
        (n1, n2) = p1
        (n3, n4) = p2
        if state[n1] == state[n2] and state[n3] == state[n4]:
            score += numberOfPairedCornerNEdges_i
        else:
            score -= numberOfPairedCornerNEdges_d
    return score

# -------------------- counting number of edge corner pairs that are one step away -----------------------#
def oneStepCornerEdgePair(queueItem):
    cube = queueItem[0]
    score = 0
    state = cube.getState()
    score_increment = 0
    for top_corner in top_corners: # 4 corners
        for side_edge in side_edges:
            if state[side_edge[0]] == state[top_corner[1]] and state[side_edge[1]] == state[top_corner[2]]:
                score_increment += oneStepCornerEdgePair_i
                
        for top_edge in top_edges:
            if state[top_edge[0]] == state[top_corner[0]] and state[top_edge[1]] == state[top_corner[2]]:
                score_increment += oneStepCornerEdgePair_i
            if state[top_edge[0]] == state[top_corner[0]] and state[top_edge[1]] == state[top_corner[1]]:
                score_increment += oneStepCornerEdgePair_i
                
    for bottom_corner in bottom_corners:
        for bottom_edge in bottom_edges:
            if state[bottom_edge[0]] == state[bottom_corner[0]] and state[bottom_edge[1]] == state[bottom_corner[1]]:
                score_increment += oneStepCornerEdgePair_i
            if state[bottom_edge[0]] == state[bottom_corner[0]] and state[bottom_edge[1]] == state[bottom_corner[2]]:
                score_increment += oneStepCornerEdgePair_i
        for side_edge in side_edges:
            if state[side_edge[0]] == state[bottom_corner[2]] and state[side_edge[1]] == state[bottom_corner[1]]:
                score_increment += oneStepCornerEdgePair_i
    if score_increment > 0:
        score += score_increment
    else:
        score -= oneStepCornerEdgePair_d
    return score

# -------------------- counting number of edge middle pairs -----------------------#
def middleEdgePairing(queueItem):
    cube = queueItem[0]
    score = 0
    state = cube.getState()
    centersAndEdges = [
        [top_middle_centers, top_edges],
        [middle_centers, side_edges],
        [bottom_middle_centers, bottom_edges]
    ]
    for centerAndEdge in centersAndEdges:
        (centers, edges) = centerAndEdge
        for center, edge in zip(centers, edges):
            if state[center[0]] == state[edge[0]] and state[center[1]] == state[edge[1]]:
                score +=1
    return score

# -------------------- counting number of 'solid rows' -----------------------#
def numberOfSolidRows(queueItem):
    # Row mappings
    rows = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8]]
    cube = queueItem[0]
    score = 0
    for face in cube.faces:
        for row in rows:
            count = set()
            for tile in row:
                count.add(face[tile])
            if len(count) == 1:
                score += 4
            if len(count) == 2:
                score += 2
            if len(count) == 3:
                score -= 2
    return score

# -------------------- counting number of 'solid faces' -----------------------#
def numberOfSolidFaces(queueItem):
    # Row mappings
    cube = queueItem[0]
    score = 0
    for face in cube.faces:
        faceCount = set()
        for color in face.values():
            faceCount.add(color)
        score += ((5 - len(faceCount)) / 4) * 0.5

    return score

#--------------- compound heuristics: numberOfSolidRows + numberOfSolidFaces ------------------#
def numberOfSolidRowsWithSolidFace(queueItem):
    # Row mappings
    rows = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8]]
    cube = queueItem[0]
    score = 0
    for face in cube.faces:
        faceCount = set()
        for color in face.values():
            faceCount.add(color)
        score += ((5 - len(faceCount)) / 4) * 0.5

        for row in rows:
            rowCount = set()
            for tile in row:
                rowCount.add(face[tile])
            if len(rowCount) == 1:
                score += 4
            if len(rowCount) == 2:
                score += 2
            if len(rowCount) == 3:
                score -= 2
    return score

#--------------- compound heuristics: oneStepCornerEdgePair + numberOfPairedCornerNEdges ------------------#
def adaptedCFOP(queueItem):
    return oneStepCornerEdgePair(queueItem) + numberOfPairedCornerNEdges(queueItem) + middleEdgePairing(queueItem)

def adaptedCFOP2(queueItem):
    return numberOfPairedCornerNEdges(queueItem) + numberOfSolidFaces(queueItem)

def adaptedCFOP3(queueItem):
    return numberOfPairedCornerNEdges(queueItem) + middleEdgePairing(queueItem) + numberOfSolidFaces(queueItem)

def adaptedCFOP4(queueItem):
    return numberOfPairedCornerNEdges(queueItem) + middleEdgePairing(queueItem)