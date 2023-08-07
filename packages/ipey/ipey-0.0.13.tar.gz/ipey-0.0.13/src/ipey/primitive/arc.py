from ipey.primitive import Primitive
import xml.etree.ElementTree as ET
import math

class Arc(Primitive):

    def __init__(self, p1, p2, p3, prototype=None):
        '''
        Create a arc starting at p1, going through p2 and ending at p3.
        '''
        super().__init__(prototype=prototype)

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.onlyConsiderEndpointsInBB = False

        self.points = [p1,p2,p3]

    def getBB(self):
        if self.onlyConsiderEndpointsInBB:
            points = [self.p1, self.p3]
        else:
            points = []

            cx, cy, r = self.findCircle(self.p1[0], self.p1[1], self.p2[0], self.p2[1], self.p3[0], self.p3[1])

            dx1 = self.p1[0] - cx
            dy1 = self.p1[1] - cy

            dx3 = self.p3[0] - cx
            dy3 = self.p3[1] - cy

            a1 = math.atan2(dy1, dx1) * 180 / math.pi
            a3 = math.atan2(dy3, dx3) * 180 / math.pi

            if a1 < 0:
                a1 = 360 + a1
            if a3 < 0:
                a3 = 360 + a3

            #print(a1,a3, self.isClockwise())

            if not self.isClockwise():
                tmp = a1
                a1 = a3
                a3 = tmp

            s1 = int(a1 / 90)
            s3 = int(a3 / 90)

            #print(a1,a3)
            #print(s1, s3)

            points.append(self.p1)
            points.append(self.p3)

            first = True
            for i in range(4):
                s = (s1 + i) % 4

                if s == s3 and not (a3 < a1 and first):
                    break 

                if s == 0:
                    points.append((cx, cy + r))
                if s == 1:
                    points.append((cx - r, cy))
                if s == 2:
                    points.append((cx, cy - r))
                if s == 3:
                    points.append((cx + r, cy))

                first = False

        maxX = max(points, key=lambda item:item[0])[0]
        maxY = max(points, key=lambda item:item[1])[1]
        minX = min(points, key=lambda item:item[0])[0]
        minY = min(points, key=lambda item:item[1])[1]

        #print(((minX, minY), (maxX, maxY)))
        return ((minX, minY), (maxX, maxY))


    def translate(self, x, y):
        self.p1 = (self.p1[0] + x, self.p1[1] + y)
        self.p2 = (self.p1[0] + x, self.p1[1] + y)
        self.p3 = (self.p1[0] + x, self.p1[1] + y)

    #TODO fix rotation
    def rotate(self, a, pivot=None):
        if pivot:
            xP, yP = pivot
        else:
            xP = 0
            yP = 0
            for p in self.points:
                xP += p[0]
                yP += p[1]
                
            yP /= len(self.points)
            xP /= len(self.points)


        s = math.sin(a)
        c = math.cos(a)
        for i, p in enumerate(self.points):
            p = (p[0] - xP, p[1] - yP)
            p = (p[0] * c + p[1] * s, p[0] * s + p[1] * c)
            self.points[i] = (p[0] + xP, p[1] + yP)

    def draw(self):
        elem = ET.Element('path')
        self.addProperties(elem)

        p1X = self.p1[0] + self.xP
        p1Y = self.p1[1] + self.yP
        p2X = self.p2[0] + self.xP
        p2Y = self.p2[1] + self.yP
        p3X = self.p3[0] + self.xP
        p3Y = self.p3[1] + self.yP
        

        cx, cy, r = self.findCircle(p1X, p1Y, p2X, p2Y, p3X, p3Y)

        
        if self.isClockwise():
            r2 = r
        else:
            r2 = -r

        elem.text = f'{p1X} {p1Y} m \n {r} 0 0 {r2} {cx} {cy} {p3X} {p3Y} a'
        return elem


    def isClockwise(self):

        a = 0

        a += self.p1[0] * self.p2[1] - self.p1[1] * self.p2[0]
        a += self.p2[0] * self.p3[1] - self.p2[1] * self.p3[0]
        a += self.p3[0] * self.p1[1] - self.p3[1] * self.p1[0]

        return a > 0

    def findCircle(self, x1, y1, x2, y2, x3, y3):
        x12 = x1 - x2
        x13 = x1 - x3
    
        y12 = y1 - y2
        y13 = y1 - y3
    
        y31 = y3 - y1
        y21 = y2 - y1

        x31 = x3 - x1
        x21 = x2 - x1
    
        # x1^2 - x3^2
        sx13 = pow(x1, 2) - pow(x3, 2)
    
        # y1^2 - y3^2
        sy13 = pow(y1, 2) - pow(y3, 2)
    
        sx21 = pow(x2, 2) - pow(x1, 2)
        sy21 = pow(y2, 2) - pow(y1, 2)
    
        f = (((sx13) * (x12) + (sy13) * (x12) + (sx21) * (x13) + (sy21) * (x13)) // (2 * ((y31) * (x12) - (y21) * (x13))))
                
        g = (((sx13) * (y12) + (sy13) * (y12) + (sx21) * (y13) + (sy21) * (y13)) // (2 * ((x31) * (y12) - (x21) * (y13))))
    
        c = (-pow(x1, 2) - pow(y1, 2) - 2 * g * x1 - 2 * f * y1)
    
        # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0
        # where centre is (h = -g, k = -f) and
        # radius r as r^2 = h^2 + k^2 - c
        cx = -g
        cy = -f
        sqr_of_r = cx**2 + cy ** 2 - c
    
        # r is the radius
        r = math.sqrt(sqr_of_r)
    
        return cx, cy, r
