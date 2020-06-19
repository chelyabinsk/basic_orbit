# 2-Body problem simulation using the pygame library


import pygame
import math
import sys


# Initialize the game engine
pygame.font.init()

clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Calibri', 20)
target_fps = 60
 
# Set the height and width of the screen
SIZE = [1280, 720]
 
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("2-Body Problem Animation")


class circle():
    def __init__(self,pos,vel,color,mass,num):
        self.x_vel, self.y_vel = vel
        self.x, self.y = pos
        self.color = color
        self.mass = mass
        self.num = num
        
    def update_velocity(self, x_vel, y_vel, override=False):
        self.x_vel += x_vel
        self.y_vel += y_vel
        if(override):
            self.x_vel = x_vel
            self.y_vel = y_vel
        
    def update_pos(self, pos=(),bouncein=False):
        if(pos != ()):
            self.x,self.y = pos
        else:
            if bouncein:
                if(self.x + self.x_vel > SIZE[0] or
                   self.x - self.x_vel < 0
                   ):
                    if(self.x > SIZE[0]):
                        self.x = SIZE[0] - 1
                    elif(self.x < 0):
                        self.x = 1
                    self.x_vel *= -1
                if(self.y + self.y_vel > SIZE[1] or
                   self.y - self.y_vel < 0
                   ):
                    if(self.y > SIZE[1]):
                        self.y = SIZE[1] - 1
                    elif(self.y < 0):
                        self.y = 1
                    self.y_vel *= -1
            self.x += self.x_vel
            self.y += self.y_vel           
    
    def get_text(self):
        msg = "n:{:.0f},x:{:.2f},y:{:.2f}\tvX:{:.2f},vY:{:.2f}".format(self.num,self.x,self.y,self.x_vel,self.y_vel)
        return msg
        
def draw_dot(screen,color,pos,radius):
    pygame.draw.circle(screen,color,pos,radius)
    
def g_between(dot1,dot2):
    r = math.sqrt((dot1.x-dot2.x)**2 + (dot1.y-dot2.y)**2) # Distance between the planets
    G = 6.67e-11 # Gravitational constant
    #print("r:{}".format(r))
    
    if(r > 0):            
        # Force and angle between the planets using Newton's Universal Law of Gravitation
        force = (G*dot1.mass*dot2.mass)/(r**2)
        theta = math.acos(abs(dot1.x-dot2.x)/r)

    
        x_vectorWhite = force*math.cos(theta)/dot1.mass
        x_vectorYellow = force*math.cos(theta)/dot2.mass

        y_vectorWhite = force*math.sin(theta)/dot1.mass
        y_vectorYellow = force*math.sin(theta)/dot2.mass

        
        if(dot1.x > dot2.x):
            x_vectorWhite = -x_vectorWhite

        if(dot1.y > dot2.y):
            y_vectorWhite = -y_vectorWhite

        
        dot1.update_velocity(x_vectorWhite,y_vectorWhite)
        dot2.update_velocity(x_vectorYellow,y_vectorYellow)
        
        # Print the new position
        msg1 = dot1.get_text()
        msg2 = dot2.get_text()
        
        sys.stdout.write("\r{}".format(msg1))
        


def draw_text():
    # Helper function to draw information to the screen
    WHITE = (255,255,255)
    # Position and velocity details of the two planets
    infoSurface = myfont.render("Position and Velocity of the Two Planets: ", False, WHITE)
    white_planet_text = "Position of the White Planet:   X: {:.0f}  Y: {:.0f}".format(c1.x,c1.y)
    posSurfaceWhite = myfont.render(white_planet_text, False, WHITE)
    
    yellow_planet_text = "Position of the Yellow Planet:   X: {:.0f}  Y: {:.0f}".format(c2.x,c2.y)
    posSurfaceYellow = myfont.render(yellow_planet_text, False, WHITE)

    white_vel = math.sqrt(c1.x_vel**2 + c1.y_vel**2)
    white_force_text = "Velocity of the White Planet:    V: {:.2f}  Vx: {:.2f}  Vy: {:.2f}".format(white_vel,
                                                                                       c1.x_vel,
                                                                                       c1.y_vel)
    forceSurfaceWhite = myfont.render(white_force_text, False, WHITE)
    
    yellow_vel = math.sqrt(c2.x_vel**2 + c2.y_vel**2)
    yellow_force_text = "Velocity of the Yellow Planet:    V: {:.2f}  Vx: {:.2f}  Vy: {:.2f}".format(yellow_vel,
                                                                                       c2.x_vel,
                                                                                       c2.y_vel)
    
    forceSurfaceYellow = myfont.render(yellow_force_text, False, WHITE)
    
    screen.blit(infoSurface,(0, 2))
    screen.blit(posSurfaceWhite,(0, 40))
    screen.blit(posSurfaceYellow,(0, 60))
    screen.blit(forceSurfaceWhite,(0, 100))
    screen.blit(forceSurfaceYellow,(0, 120))
    
# Create the two planets
c1 = circle((600,460), (-0.25, 0), [255,255,255], mass = 100, num = 1)
c2 = circle((500,400), (0, 0), [255,255,0], mass = 10e10, num = 2)


# Loop until the user clicks the close button.
done = False
while not done:

    for event in pygame.event.get():   # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True   # Flag that we are done so we exit this loop
 
    # Set the background and count the fps
    screen.fill([0,0,0])
    
    # Draw the two planets
    draw_dot(screen, c1.color, (round(c1.x), round(c1.y)), 5)    
    draw_dot(screen, c2.color, (round(c2.x), round(c2.y)), 10)    
    
    # Compute the force between the planets and update their positions
    g_between(c1,c2)
    c1.update_pos()
    c2.update_pos()
    
    draw_text()
    
    # Update the screen with what we've drawn.
    pygame.display.flip()
    clock.tick(target_fps)
