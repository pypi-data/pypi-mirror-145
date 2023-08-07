from ipey.primitive.ellipse import Ellipse

class Circle(Ellipse):

    def __init__(self, p, r, prototype=None):
        super().__init__(p, (r,0), (0,r), prototype=prototype)

