from stl import mesh
import foil
import numpy as np

class STL:
  
  def __init__(self):
    self.lines = []
    self.n = None
    
  def add_line(self, line):
    ''' Each line is a list of 3D points (vertices)'''
    self.lines.append(line)
    self.n = len(line)

  def index(self, line, i):
    return (line*self.n + i)
  
  def gen_stl(self, fname):
    
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
    
    #print vertices
    
    vertices = np.array(vertices)
    faces = np.array(faces)
    
    # Create the mesh
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "cube.stl"
    cube.save(fname)

if __name__ == "__main__":

    f1 = np.array([[0,1,2,3,4],[0,0,0,0,0],[0,0,0,0,0]]).T
    f2 = np.array([[0,1,2,3,4],[1,1,1,1,1],[0,0,0,0,0]]).T
    f3 = np.array([[0,1,2,3,4],[2,2,2,3,2],[0,0,0,0,0]]).T


    s = STL()
    s.add_line(f1)
    s.add_line(f2)
    s.add_line(f3)
    
    s.gen_stl('temp.stl')