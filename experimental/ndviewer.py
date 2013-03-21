from itertools import product
from galry import *


VS = """
float n = texinfo.x;
float d = texinfo.y;
float dinv = 1./d;

// Normalized dimensions.
float di0 = (dim.x + .5) * dinv;
float di1 = (dim.y + .5) * dinv;

vec2 boxpos = vec2(-1 + (2 * dim.x + 1) * dinv, 1 - (2 * dim.y + 1) * dinv);

// Texture coordinates.
// WARNING: reverse order here!
vec2 coord0 = vec2(di0, index);
vec2 coord1 = vec2(di1, index);

// Get the data value for the given index, and the given dimension.
float x0 = texture2D(texture, coord0).x;
float x1 = texture2D(texture, coord1).x;

vec2 position = boxpos + dinv * vec2(x0, x1);

"""


FS = """
out_color = vec4(1., 1., 0., .5);
"""



class NDVisual(Visual):
    def initialize(self, data):
        n, d = data.shape
        data = np.tile(data.reshape((n, d, 1)), (1, 1, 3))
        self.data = data
        self.size = n*d*d
        # self.is_static = True
        
        index = np.linspace(0., 1., n)
        index = np.tile(index, d*d)
        
        dim = np.array([(i, j) for i, j in product(range(d), range(d))])
        dim = np.repeat(dim, n, axis=0)
        
        # texture info with the texture size, the offset and the step for
        # obtaining a value from the integer indices and obtaining a normalized
        # tex coord
        texinfo = (float(n), float(d))
        
        self.add_attribute('index', vartype='float', ndim=1, data=index)
        self.add_attribute('dim', vartype='float', ndim=2, data=dim)
        self.add_texture('texture', ncomponents=3, ndim=2, data=self.data)
        self.add_uniform('texinfo', vartype='float', ndim=len(texinfo),
            data=texinfo)
            
        self.primitive_type = 'POINTS'
        
        self.add_vertex_main(VS)
        self.add_fragment_main(FS)
        

n, d = 10000, 8
data = .15 * np.random.randn(n, d)

data[:n/4, 1] *= .25
data[:n/4, 1] += .75

data[2*n/4:3*n/4, 3] *= .25
data[2*n/4:3*n/4, 3] -= .75

visual(NDVisual, data)


show()

