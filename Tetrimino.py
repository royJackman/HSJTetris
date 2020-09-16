adj = [[0,1], [1,0], [0,-1], [-1,0]]
diag = [[1,1], [1,-1], [-1,-1], [-1, 1]]
faradj = [[0,2], [2,0], [0,-2], [-2,0]]

def get_next(arr, clockwise, prev):
    return arr[(arr.index(prev) + (1 if clockwise else -1)) % len(arr)]

class Tetrimino:
    def __init__(self, squares, colors = (0.5, 0.5, 0.5)):
        self.direction = 0
        self.squares = squares
        self.color = colors
    
    def __str__(self):
        return str(self.squares)
    
    def bottom(self):
        retval = {}
        for i in self.squares:
            if i[1] in retval.keys():
                if i[0] > retval[i[1]]:
                    retval[i[1]] = i[0]
            else:
                retval[i[1]] = i[0]
        return [[v, k] for k, v in retval.items()]
    
    def rotate(self, clockwise):
        retval = []
        for i in range(len(self.squares)):
            if self.squares[i] == [0,0]: 
                retval.append([0,0])
            elif self.squares[i] in faradj:
                retval.append(get_next(faradj, clockwise, self.squares[i]))
            elif self.squares[i] in adj:
                retval.append(get_next(adj, clockwise, self.squares[i]))
            elif self.squares[i] in diag:
                retval.append(get_next(diag, clockwise, self.squares[i]))
        return retval

def I(): return Tetrimino([[0,0], [0,-1], [0, 1], [0,2]], (0, 204/256, 204/256))
def O(): return Tetrimino([[0,0], [0,-1], [1, -1], [1,0]], (1, 1, 0))
def T(): return Tetrimino([[0,0], [0,-1], [1, 0], [0,1]], (153/256, 51/256, 1))
def S(): return Tetrimino([[0,0], [0,1], [1, 0], [1,-1]], (51/256, 1, 51/256))
def Z(): return Tetrimino([[0,0], [0,-1], [1, 0], [1,1]], (1, 51/256, 51/256))
def J(): return Tetrimino([[0,0], [0,-1], [-1, -1], [0,1]], (0, 0, 1))
def L(): return Tetrimino([[0,0], [0,-1], [-1, 1], [0,1]], (1, 178/256, 102/256))

DEFAULTS = [I, O, T, S, Z, J, L]