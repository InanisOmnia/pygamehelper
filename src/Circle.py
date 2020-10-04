from src.requirements import *

class Circle(): # IT ALL NEEDS ANNOTATING
    def __init__(self, position, radius):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == "position":
            self.__dict__["x"] = self.__dict__[name].x
            self.__dict__["y"] = self.__dict__[name].y
            
        elif name == "x":
            self.__dict__["position"] = pygame.math.Vector2(self.x, self.y)

        elif name == "y":
            self.__dict__["position"] = pygame.math.Vector2(self.x, self.y)

        elif name == "radius":
            if 0 > value:
                self.normalize()
            self.__dict__["diameter"] = self.radius * 2
            self.__dict__["area"] = self.radius ** 2 * math.pi

        elif name == "diameter":
            self.__dict__["radius"] = self.diameter / 2
            self.__dict__["area"] = self.radius ** 2 * math.pi

        elif name == "area":
            self.__dict__["radius"] = math.sqrt(self.area / math.pi)
            self.__dict__["diameter"] = self.radius / 2
    def copy(self):
        return Circle(self.postition, self.radius)

    def move(self, x, y):
        return Circle((self.pos.x + x, self.pos.y + y, self.radius))

    def move_ip(self, x, y):
        self.x += x
        self.Y += y

    def inflate(self, factor):
        return Circle(self.position, self.radius + factor)

    def inflate_ip(self, factor):
        self.radius += factor

    def clamp(self, circle):
        return Circle(circle.position, self.radius)

    def clamp_ip(self, circle):
        self.position = circle.position

    def clip(self, circle): # needs math optimisation
        length = math.dist(self.position, circle.position)
        length2 = abs(length - (self.radius + circle.radius))
        newrad = length2 / 2
        newdist = self.radius - newrad
        newvec = pygame.math.Vector2(circle.x - self.x, circle.y - self.y)
        newvec.scale_to_length(newdist)
        return Circle((self.x + newvec.x, self.y + newvec.y), newrad)
        
    def clipline():
        pass # waiting for math

    def union(self, circle):
        pass # waiting for math

    def union_ip(self):
        pass # waiting for math

    def unionall(self):
        pass # waiting for math

    def unionall_ip(self):
        pass # waiting for math

    def normalize(self):
        self.radius = abs(self.radius)

    def contains(self, circle):
        return math.dist(self.position, circle.position) + circle.radius <= self.radius

    def collidepoint(self, v1, v2 = None):
        if v2 == None:
            test_for = v1
        else:
            test_for = (v1, v2)
        return math.dist(self.position, test_for) <= self.radius        
        
    def collidecircle(self, circle):
        return math.dist(self.position, circle.position) < self.radius + circle.radius
        
    def collidelist(self, circles):
        for i in range(len(circles)):
            if math.dist(self.position, circles[i].position) < self.radius + circles[i].radius:
                return(i)

    def collidelistall(self, circles):
        for i in range(len(circles)):
            if math.dist(self.position, circles[i].position) < self.radius + circles[i].radius:
                   yield int(i)

    def collidedict(self, circles, use_values = 0):
        if use_values ==0:
            for circle in circles:
                if math.dist(self.position, circle.position) < self.radius + circle.radius:
                    return tuple(circle, circles[circle])
        else:
            for key in circles:
                circle = circles.get(key)
                if math.dist(self.position, circle.position) < self.radius + circle.radius:
                    return tuple((key, circle))                    
            

    def collidedictall(self, circles, use_values = 0):
        if use_values == 0:
            for circle in circles:
                if math.dist(self.position, circle.position) < self.radius + circle.radius:
                    yield tuple(circle, circles[circle])
        else:
            for key in circles:
                circle = circles.get(key)
                if math.dist(self.position, circle.position) < self.radius + circle.radius:
                    yield tuple((key, circle))
  
