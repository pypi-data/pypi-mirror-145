# IPEY

**ipey** is a python package that lets you programatically create **Ipe** drawings from python code. The project can be found on <a href='https://github.com/mwallinger-tu/ipey'>Github</a>. The image below was created with python, ipey and some math.

<img src="spiral.png"/>

# Install

**ipey** is available via pypi and can be installed by 

```bash
pip install ipey
```

# Basic Usage

In this very basic example we create a ipe document, add a primitive and save the file. First, we create an empty document and add the first page to it. Then, we create a circle at position (x=400, y=400) with a radius of 20. Finally, we store the document as *simple.xml*.

```python
from ipey.document import Document
from ipey.primitive import Circle

document = Document()
page = document.createPage()

circle = Circle((400,400), 20)
page.add(circle)

document.write('simple.xml')
```

## Document Properties

Document objects have different properties that can be specified. The standard size uses the size of the Ipe basic style sheet. Here, we set the size to a square shape of sidelength 1000.

```python
document = Document()
document.width = 1000
document.height = 1000
```

Furthermore, it is also possible to crop the drawing to the content. In this case the widht and height of the document is ignored and the bounding box of all elements in the scene is used to compute the appropriate document size. A margin can be used to keep elements away from the document border. If left unspecified the margin for all sides is 64.


```python
from ipey.document import Margin

margin = Margin(top=100, bottom=100, left=100, right=200)
margin.bottom = 200

document = Document()
document.crop = True
document.margin = margin
```

Lastly, documents can be initialized with existing style sheets and a custom settings.ini. Style sheets are specified as a list of style sheets (including path) and appended to the document. For example, if custom colors are defined in such a style sheet they can then be used by assigning their name to the color property of elements.

```python
document = Document(settings_path='my/path/to/settings.ini', 
                    styles=['mystyle1.isy', 'path/to/my/style.isy'])
```

## Pages, Layers, Views and Elements

It is possible to add multiple pages to a document. This can be achieved by either creating empty pages or copying an existing page (including all elements in a page at the time of copying).

```pythonfrom ipey.helper import convertColor
from ipey.document import Document
from ipey.primitive import Circle

document = Document()
page1 = document.createPage()
page2 = document.createPage()

circle = Circle((400,400), 20)
page1.add(circle)

page3 = document.copyPage(page1)
```

Adding elements to a page can be achieved by either just appending the element or specifying a second element. Just adding an element will result in a drawing where the newest element is always the topmost. When a given element is also used, it can either be placed right before or right after the element in the drawing.


```python
from ipey.document import Document
from ipey.primitive import Circle

document = Document()
page = document.createPage()

circle1 = Circle((400,400), 20)
page.add(circle)
circle2 = Circle((410,410), 20)
page.add(circle)
circle3 = Circle((420,420), 20)
page.add(circle)

circle4 = Circle((390,390), 20)
page.addBefore(circle4, circle1)

circle5 = Circle((430,430), 20)
page.addAfter(circle5, circle3)
```


Layers are simply created by adding the layer name to an element.

```python
from ipey.document import Document
from ipey.primitive import Circle, Rectangle

document = Document()
page = document.createPage()


circle = Circle((400,400), 20)
circle.layer = 'circles'
page.add(circle)

rect = Rectangle((300,400),200,200)
rect.layer = 'rectangles'
page.add(rect)
```

Views can be added to page by specifying a name for the view and either a single layer or a list of layers. In the following example we create three views for the elements created above. One that only shows rectangles, one that only shows circles and one that shows circles and rectangles.

```python
page.createView('circleView', 'circles')
page.createView('rectangleView', 'rectangles')
page.createView('bothView', ['circles', 'rectangles'])
```

It is also possible to add and remove layers from views, as well as removing a view from the page.

```python
page.addToView('bothView', ['lines', 'labels'])
page.removeFromView('bothView', 'labels')
page.removeView('bothView')
```

## Elements

Ipe drawings consist of elements. Currently, the following elements are supported.

### Circle
Circles are created by specifying a center point and the radius.

```python
from ipey.primitive import Circle

circle = Circle((100,100), 50)
```

### Ellipse
Ellipsis are created by specifying three points - a center point, the vertex and the co-vertex.

```python
from ipey.primitive import Ellipse

ellipse = Ellipse((100,100), (150,100), (100,200))
```

### Rectangle

Two variants of creating rectangles are available. *Rectangle* creates a rectangle with anchor point at the left bottom corner. *RectangleC* with anchor point in the center.

```python
from ipey.primitive import Rectangle, RectangleC

rect = Rectangle((200,200), 100, 50)
rectC = RectangleC((400,400), 100, 50)
```

### Line
Lines are specified by giving a list of points. It is possible to add points to an existing line.

```python
from ipey.primitive import Line

line = Line([(0,0), (100,100), (0,100)])
line.addPoint((300,300))
```
### Arc
Arcs are created by specifying three points. The arc is starting at p1, going through p2 and ending at p3.

```python
from ipey.primitive import Arc

arc = Arc((300,300), (400,400), (500, 300))
```

### Polygon
Polygons are initialized by a list of points.
```python
from ipey.primitive import Polygon

polygon = Polygon([(0,0), (100,100), (0,100)])
polygon.addPoint((300,300))
```

### Spline
Splines are initialized by a list of points and the spline type.

```python
from ipey.primitive import Spline, SplineType

spline1 = Spline([(0,0), (100,100), (0,100)], SplineType.BSPLINE)
spline2 = Spline([(0,0), (100,100), (0,100)], SplineType.CARDINAL)
spline3 = Spline([(0,0), (100,100), (0,100)], SplineType.SPIRO)

```
### Glyph
Glyphs are initialized by an anchor point and a glyph type. If glyphs are specified in custom style sheets than the assigned name can be used. 

```python
from ipey.primitive import Glyph

glyph = Glyph((100,100), type='mark/fdisk(sfx)')
```
### Label and Minipage
Labels and minipages are initialized with string representing the label text and an anchor point. Additionally, text alignment options can be specified. The *isMath* attribute specifies if a text is considered normal or in math mode.

```python
from ipey.primitive import Label, Minipage

label = Label('test', (200, 300))
page.add(label)

label = Label('math_{yes}', (400, 300))
label.isMath = True
page.add(label)

label = Label('long red text in center', (400, 500))
label.vAlign = 'center'
label.hAlign = 'center'
label.stroke = 'red'
label.size = 'LARGE'
page.add(label)

minipage = Minipage('this is a very long text that should be displayed as a minipage with automatic line breaks depending on the width', (100, 700))
minipage.width = 200
page.add(minipage)
```

### Element Properties

For all elements different drawing properties can be set. Not all properties work on every element. Colors can be specified by name, as defined in the style sheets, or with hex colors. Hex colors are automatically converted. Similarly, the pen size can be given named or as a float number.

```python
from ipey.primitive import Line

line = Line([(100,100), (150,150), (200,200)])

line.fill = 'blue'
line.fill = '#4488FF'
line.stroke = 'red'
line.stroke = '#AF0000'

line.pen = 'fat'
line.pen = '5'

line.opacity = 0.5
line.stroke_opacity = 0.5
line.dash = 'dashed'
line.layer = 'lines'
line.arrow = True
line.rarrow = True
```

### Cloning Element Styles

For all elements it is possible to pass an existing element of the same type. This copies the style of the passed element to the new element. In the example below a orange circle with a red fat border is created. A second larger circle at (200,200) is then created by using the first circle as prototype.

```python
from ipey.primitive import Circle

circle1 = Circle((100,100), 50)
circle1.stroke = 'red'
circle1.pen = 'fat'
circle1.fill = 'orange'

circle2 = Circle(200,200), 100, prototype=circle1)
```

## Complex examples

In the two examples showcased here we create more complex drawing. The first example is more of artistic nature. We create n rectangles of different colors and rotate them around a center point while also shrinking at each iteration.

For this we first create the document and add a page. Then, we create the first rectangle and add it to the page. Afterwards, in each iteration we clone the previous rectangle. The points of the cloned rectangle are transformed, such that a spiral rotation is achieved.

```python
from ipey.document import Document, Margin
from ipey.primitive import Polygon

colors = ['#fafa6e','#edf76f','#e0f470','#d4f171','#c8ed73','#bcea75','#b0e678','#a5e27a','#99de7c','#8eda7f','#83d681','#79d283','#6ecd85','#64c987','#5ac489','#50bf8b','#46bb8c','#3cb68d','#32b18e','#28ac8f','#1ea78f','#12a28f','#039d8f','#00988e','#00938d','#008e8c','#00898a','#008488','#007e86','#007983','#057480','#0e6f7d','#156a79','#1a6575','#1e6071','#225b6c','#255667','#275163','#294d5d','#2a4858']

colors.reverse()
n = len(colors)
factor = 0.92
factory = 0.8

document = Document()
document.crop = True
document.margin = Margin(top=0, bottom=0, left=0, right=0)
page = document.createPage()

rect = Polygon([(0,0), (0, 600), (600,600), (600,0)])
rect.stroke = colors[0]
rect.fill = colors[0]
page.add(rect)

for i in range(1,n):
    rect = rect.clone()
    rect.stroke = colors[i]
    rect.fill = colors[i]
    points = rect.points
    newP = []

    for j in range(4):
        p1 = points[j]
        p2 = points[(j + 1) % 4]

        dx = p2[0] - p1[0]
        dy = p2[1] - p2[0]

        pNew = (p1[0] + dx * factor, p1[1] + dy * factor)
        newP.append(pNew)

    rect.points = newP
    page.add(rect)


document.write('examples/output/spiral.xml')
```

in the second example we compute the convex hull of a given point set but visualize every step of the algorithm in Ipe as its own page.

The points are initialized randomly and represented by glyphs. Every step of the algorithm is given its own page and the current convex hull of the step is represented as lines.

```python
from ipey.document import Document
from ipey.primitive import Glyph, Line, Polygon
import random

def get_slope(p1, p2):
    if p1[0] == p2[0]:
        return float('inf')
    else:
        return 1.0*(p1[1]-p2[1])/(p1[0]-p2[0])

def get_cross_product(p1,p2,p3):
    return ((p2[0] - p1[0])*(p3[1] - p1[1])) - ((p2[1] - p1[1])*(p3[0] - p1[0]))

points = [(random.randint(0,500),random.randint(0,500)) for i in range(40)]

document = Document()
document.crop = True

pagePoints = document.createPage()

for p in points:
    glyph = Glyph(p, 'mark/fdisk(sfx)')
    glyph.fill = '#000000'
    glyph.stroke = '#ffffff'
    glyph.pen = 'fat'

    pagePoints.add(glyph)

points.sort(key=lambda x:[x[0],x[1]])
start = points.pop(0)

hull = [start]

points.sort(key=lambda p: (get_slope(p,start), -p[1],p[0]))

for p in points:
    hull.append(p)
    while len(hull) > 2 and get_cross_product(hull[-3],hull[-2],hull[-1]) < 0:
        hull.pop(-2)

    page = document.copyPage(pagePoints)
    line = Line(hull)
    page.add(line)
    line.stroke = 'green'

page = document.copyPage(pagePoints)
poly = Polygon(hull)
page.add(poly)

document.write('examples/output/convexHull.xml')
```