# Orbit simulation using the pygame library


import pygame
import math


# Initialize the game engine
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Calibri', 20)
target_fps = 60
 
# Set the height and width of the screen
SIZE = [1000, 1000]
 
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Snow Animation")


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
        
    def update_pos(self, pos=()):
        if(pos != ()):
            self.x,self.y = pos
        else:
            self.x += self.x_vel
            self.y += self.y_vel           
    
    def show(self):
        print("n:{},x:{},y:{}\nvX:{},vY:{}".format(self.num,self.x,self.y,self.x_vel,self.y_vel))
        
def draw_dot(screen,color,pos,radius,width):
    pygame.draw.circle(screen,color,pos,radius,width)
    
def g_between(dot1,dot2,fps):
    r = math.sqrt((dot1.x-dot2.x)**2 + (dot1.y-dot2.y)**2) # Distance between the planet and the sun
    G = 6.67e-11 # Gravitational constant
#    print("r:{}".format(r))
    
    if(r > 0):
        if(fps == 0):
            fps = target_fps
            
        # Force and angle between the planets
        force = (G*dot1.mass*dot2.mass)/r
        print("F:{}".format(force))
        
        theta = math.acos(abs(dot1.x-dot2.x)/r)
        print(theta)
    
        x_vector = force*math.cos(theta)/(fps/60)/dot1.mass
        y_vector = force*math.sin(theta)/(fps/60)/dot1.mass
        
        if(dot1.x > dot2.x):
            x_vector = -1 * x_vector
        if(dot1.y > dot2.y):
            y_vector = -1 * y_vector
        
        
        
        print("r:{},\ntheta:{}".format(r,x_vector,y_vector,theta))
        
        dot1.update_velocity(x_vector,y_vector)
        
        # Print the new position
        dot1.show()
    if((r) <= 2):
        dot1.update_velocity(0,0,True)
 


# Create one circle
c1 = circle((450,450),(1.2,0),[255,255,255], mass=1, num=1)
c2 = circle((500,500),(0,0),[255,255,0], mass=10**10, num=1)


# Loop until the user clicks the close button.
done = False
while not done:
    fps = clock.get_fps()
#    print("fps:{}".format(fps))
    for event in pygame.event.get():   # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True   # Flag that we are done so we exit this loop
 
    # Set the screen background
    screen.fill([0,0,0])
    
    # Draw my dot (planet)
    draw_dot(screen,c1.color,(round(c1.x),round(c1.y)),5,0)    
    # Draw the focus (sun)
    draw_dot(screen,c2.color,(round(c2.x),round(c2.y)),10,0)    
    
    # Do physics stuff
    g_between(c1,c2,fps)
    c1.update_pos()
    
    # Draw FPS Counter
    fpssurface = myfont.render(str(round(fps)), False, (255, 255, 255))
    # Draw X,Y details
    possurface = myfont.render("The planet position is: " + "  X:"+str(round(c1.x))+"  Y:"+str(round(c1.y)), False, (255, 255, 255))
    # Draw Forces details
    forcesruface = myfont.render("The planet velocity is:  " + "  V:"+str(round(math.sqrt(c1.x_vel**2+c1.y_vel**2),2)) + "  Vx:"+str(round(c1.x_vel,2))+"  Vy:"+str(round(c1.y_vel,2)), False, (255, 255, 255))
    screen.blit(fpssurface,(380,300 + 0))
    screen.blit(possurface,(300,300 + 20))
    screen.blit(forcesruface,(300,300 + 40))
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    clock.tick(target_fps)
 
# Be IDLE friendly. If you forget this line, the program will 'hang' on exit
pygame.quit()

del fps
del target_fps
