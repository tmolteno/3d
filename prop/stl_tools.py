from stl.mesh import Mesh
from stl.base import RemoveDuplicates

import foil
import numpy as np

class STL:
    
    def __init__(self):
        self.blocks = []
        self.new_block()
        
    def new_block(self):
        b = Block()
        self.blocks.append(b)
    
    def add_line(self,line):
        self.blocks[-1].add_line(line)
        
    def gen_stl(self, fname):
        vertices = []
        faces = []
        
        cube = Mesh(np.concatenate([
            b.gen_stl().data.copy() for b in self.blocks
        ]),remove_duplicate_polygons=RemoveDuplicates.NONE)

        cube.save(fname)
          
          
class Block:
    ''' A block of equal length lines
    '''
    def __init__(self):
        self.lines = []
        self.n = None

        
    def add_line(self, line):
        ''' Each line is a list of 3D points (vertices)'''
        self.lines.append(line)
        self.n = len(line)

    def index(self, line, i):
        return (line*self.n + i)
    
    def gen_stl(self):
        
        vertices = []
        faces = []
        
        for l in self.lines:
            for v in l:
                vertices.append(v)
        
        faces = []
        for n, l in enumerate(self.lines[:-1]):
            for i, p in enumerate(l[:-1]):
                p0 = self.index(n,i)
                p1 = self.index(n,i+1)
                p2 = self.index(n+1, i)
                faces.append([p1,p0,p2])
                p0 = self.index(n+1,i)
                p1 = self.index(n+1,i+1)
                p2 = self.index(n, i+1)
                faces.append([p0,p1,p2])
        
               
        vertices = np.array(vertices)
        faces = np.array(faces)
        cube = Mesh(np.zeros(faces.shape[0], dtype=Mesh.dtype), remove_duplicate_polygons=RemoveDuplicates.NONE)
        for i, f in enumerate(faces):
            for j in range(3):
                cube.vectors[i][j] = vertices[f[j],:]

        return cube

if __name__ == "__main__":

    f1 = np.array([[0,1,2,3,4],[0,0,0,0,0],[0,0,0,0,0]]).T
    f2 = np.array([[0,1,2,3,4],[1,1,1,1,1],[0,0,0,0,0]]).T
    f3 = np.array([[0,1,2,3,4],[2,2,2,2.1,2],[1,1,1,1,1]]).T


    s = STL()
    
    s.add_line(f1)
    s.add_line(f2)
    s.add_line(f3)
    s.add_line(f1)
    
    s.new_block()
    s.add_line(np.array([f1[0],f2[0]]))
    s.add_line(np.array([f3[0]]))
    
    s.gen_stl('temp.stl')