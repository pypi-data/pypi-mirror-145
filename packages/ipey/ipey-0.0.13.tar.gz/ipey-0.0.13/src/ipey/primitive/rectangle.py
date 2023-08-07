from ipey.primitive.polygon import Polygon


class Rectangle(Polygon):

    def __init__(self, p, w, h, prototype = None):
        
        points = []
        pp = (p[0], p[1] - h)
        ppp = (pp[0] + w, pp[1])
        pppp = (ppp[0], p[1])

        points.append(p)
        points.append(pp)
        points.append(ppp)
        points.append(pppp)

        super().__init__(points, prototype=prototype)
        
        
class RectangleC(Polygon):

    def __init__(self, c, w, h, prototype = None):
        points = []
        p = (c[0] + w/2, c[1] + h/2)
        pp = (c[0] + w/2, c[1] - h/2)
        ppp = (c[0] - w/2, c[1] - h/2)
        pppp = (c[0] - w/2, c[1] + h/2)

        points.append(p)
        points.append(pp)
        points.append(ppp)
        points.append(pppp)

        super().__init__(points, prototype=prototype)       



