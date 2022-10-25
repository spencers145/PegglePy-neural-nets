# refer to the vectors.py module for information on these functions
from trigger_events import TimedEvent
from vectors import Vector

from config import bluePegImg, hitBluePegImg, orangePegImg, hitOrangePegImg, greenPegImg, hitGreenPegImg


class Peg:
    def __init__(self, x : int, y : int, color = "blue"):
        self.pos = Vector(x, y)  # position
        self.vel = Vector(0, 0)  # velocity, used for collision calculation

        self.radius = 14

        self.mass = 22 # magic number, just pulled this one out of thin air

        self.posAdjust = self.radius # this is used to draw the image for the peg in the correct position
        self.isHit = False
        self.isVisible = True
        self.isPowerUp = False
        self.isOrange = False
        
        self.color = color
        self.points = 10

        self.pegImg = bluePegImg

        self.pegScreenLocation = 0 # default 0, this is to be given a different value
        self.pegScreenLocation2 = 0 # default will be 0 unless the peg happens to be on the segment boundary

        self.ballStuckTimer = TimedEvent() # used for when the ball gets stuck


    def reset(self):
        self.vel = Vector(0, 0)  # velocity, used for collision calculation

        self.radius = 14

        self.mass = 20 # magic number, just pulled this one out of thin air

        self.posAdjust = self.radius # this is used to draw the image for the peg in the correct position
        self.isHit = False
        self.isVisible = True
        self.isPowerUp = False
        self.isOrange = False
        
        self.color = "blue"
        self.points = 10

        self.pegImg = bluePegImg

        self.pegScreenLocation = 0 # default 0, this is to be given a different value
        self.pegScreenLocation2 = 0 # default will be 0 unless the peg happens to be on the segment boundary

        self.ballStuckTimer = TimedEvent() # used for when the ball gets stuck


    def update_color(self):
        # set the appropiate color peg image if it is has been hit or not
        if self.isHit:
            self.posAdjust = 25 #the image for hit pegs is actually slightly larger, so this variable is to adjust for this
            if self.color == "blue":
                self.pegImg = hitBluePegImg
            if self.color == "orange":
                self.pegImg = hitOrangePegImg
            if self.color == "green":
                self.pegImg = hitGreenPegImg 
        else:
            if self.color == "blue":
                self.pegImg = bluePegImg
            if self.color == "orange":
                self.points = 100
                self.pegImg = orangePegImg
            if self.color == "green":
                self.pegImg = greenPegImg
                self.points = 10
            
