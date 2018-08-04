"""

   Name: AYUSH GUPTA
   
   Date: May 29, 2016
   
   Description:This program utilizes pygame, and and its various methods
   and classes to create sprites for the Space Invaders game. 
   
"""
import pygame


class Player(pygame.sprite.Sprite):
    ''' This class defines the sprite for the player aircraft.'''
    
    def __init__ (self,screen):
        ''' This initializer takes a screen surface as a parameter, initializes
        the aircraft images, and rect attributes, and start xy of the aircraft.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.__aircraft = pygame.image.load("images/playerairship.gif")
        self.image = self.__aircraft
        self.rect = self.image.get_rect()  
        self.rect.center = (320,456)
        self.__screen = screen
        self.__movespeed = 3
        self.__speedtimer = 0
        
    def go_left(self):
        ''' This method modifies the center of the images by moving it 3 pixels
        to the left '''
        self.rect.centerx -= self.__movespeed
    
    def speed_up(self):
        '''This method increases the player's move speed so they can move around
        faster'''
        self.__movespeed = 6
    
    def go_right(self):
        ''' This method modifies the center of the image by moving it 3 pixels
        to the right'''
        self.rect.centerx += self.__movespeed
        
    def update(self):
        '''This method is called automatically to reposition the
        player sprite on the screen. It also ensures the speed boost powerup
        only lasts for a certain duration'''
        
        if self.__movespeed == 6:
            self.__speedtimer += 1
            
        #This is for the speed boost powerup, to make it only last for a few seconds    
        if self.__speedtimer == 100:
            self.__movespeed = 3
            self.__speedtimer = 0
            
        if self.rect.right > self.__screen.get_width():
            self.rect.right = self.__screen.get_width()
        if self.rect.left < 0:
            self.rect.left = 0
            
class Alien(pygame.sprite.Sprite):
    ''' This class defines the sprite for the alien aircrafts. '''
    
    def __init__ (self,screen,aircraft,startposition,points):
        '''This initializer takes a screen surface, a number corresponding to
        the alien row for the  image to be loaded, and a start xy 
        position for each alien as parameters, it then gets the rect attributes
        initializes the image and xy of each alien'''
        
        pygame.sprite.Sprite.__init__(self)
        self.__alienstill = []
        self.__alienmove = []
        
        for alien_image in range (1,6):
            self.__alienstill.append(pygame.image.load("images/Alien" + str(alien_image)\
                                                       +".gif"))
            self.__alienmove.append(pygame.image.load("images/Alien"+ str(alien_image*10)\
                                                      +".gif"))
        
        self.__alienaircraft = aircraft
        self.__screen = screen
        self.__side = True
        self.image = self.__alienstill[aircraft]
        self.rect = self.image.get_rect()
        self.rect.center = startposition
        self.__points = points
        self.__swap = True  
        self.__timer =  27
        self.__stutter_timer = 0
        self.__godowncounter = 1
        self.__speedcounter = 1
        self.__directioncounter = 1
        self.__death = False
        self.__deathdelay = 0
        
    def get_points(self):
        '''This method returns the points for the alien'''
        return self.__points
    
    def get_speed(self):
        '''This method returns the current speed/timer value'''
        return self.__timer
    
    def death(self):
        '''This method sets the self.__death variable to true'''
        self.__death = True
        
    def go_down (self):
        '''This method causes the aliens to move down 3 pixels''' 
        if self.__godowncounter % 8 != 0:
            self.__godowncounter += 1
        else:
            self.rect.centery += 3
            
    def switch_direction(self):
        '''This method swaps the current boolean value for self.__side'''
        self.__side = not self.__side
        
    def image_swap(self):
        '''This method swaps the image so the aliens look like they are moving
        and not gliding, it checks that self.__swap is not set to death 
        before swapping images'''   
        if self.__swap != 'death':
            self.__swap = not self.__swap
            if self.__swap:
                self.image = self.__alienstill[self.__alienaircraft]
            else:
                self.image = self.__alienmove[self.__alienaircraft]
            
        
    def speed_up(self):
        '''This method increases the speed for the aliens, it reduces
        the delay between each image swap and shift'''
        if self.__timer > 3:
            self.__timer -= 2
        
    def update (self):
        '''This update method checks if the alien is set to die, if it is 
        then it swaps the aliens image, sets self.__swap to death and gives 
        it time to make it apparent to the player that it is dead, it also 
        shifts the aliens left or right based on the self.__side variable'''
        
        if self.__death:
            self.__deathdelay += 1
            self.__swap = 'death'
            self.image = pygame.image.load("images/death1.gif")
        if self.__death and self.__deathdelay % 5 == 0:
            self.kill()
            
        self.__stutter_timer += 1
        
        #This if statement adds a delay, so the aliens don't move too fast 
        #or swap images too fast
        if self.__stutter_timer % self.__timer == 0:
            self.__stutter_timer = 0
            if self.__side:
                self.rect.centerx += 2
            else:
                self.rect.centerx -= 2
            self.image_swap()
            

class AlienLaser(pygame.sprite.Sprite):
    '''This class defines the sprite for the lasers shot by the aliens'''
        
    def __init__ (self,screen,startposition):
        '''This initializer method takes the screen and startposition as a tuple
        for parameters, it initializes the start position and image for each 
        enemy alien laser.'''
            
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.image = pygame.Surface((1,8))
        self.image.fill((255,255,255))
            
        self.rect = self.image.get_rect()
        self.rect.center = startposition
            
    def update(self):
        '''This update method shifts the alien lasers down, toward the player
        by 7 pixels. Upon the top of the laser reaching the bottom, the laser is
        killed'''         
        self.rect.centery += 7
        if self.rect.top > 480:
            self.kill()

class EndZone(pygame.sprite.Sprite):
    '''This class defines the sprite for the left and right endzones, aswell as
    the bottom, this is so the aliens are within these boundaries and respond
    when collision occurs between them'''
    
    def __init__(self, screen, x_position, bottom_endzone = False):
        '''This initializer takes the screen, x-position and a boolean value if 
        it is called for the bottom endzone. It initializes the endzone 
        and position, based on the parameters given'''
        
        pygame.sprite.Sprite.__init__(self)

        if not bottom_endzone:
            self.image = pygame.Surface((1, screen.get_height()))
            self.image = self.image.convert()
            self.image.fill((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.left = x_position
            self.rect.top = 0
        else:
            #If a boolean value of True is passed in for bottom_endzone
            #then the endzone is for the bottom
            self.image = pygame.Surface((screen.get_width(), 1))
            self.image = self.image.convert()
            self.image.fill((0,0,0))            
            self.rect = self.image.get_rect()
            self.rect.center = (320,330) 
            
class Laser(pygame.sprite.Sprite):
    '''This class defines the sprite for the lasers shot by the player'''
        
    def __init__ (self,screen):
        '''This initializer method takes the screen as a parameter, it initializes
        the start position and image for the player's laser. It sets
        the starting position of the laser off the screen'''
            
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.image = pygame.Surface((1,8))
        self.image.fill((255,255,255)) 
        self.rect = self.image.get_rect()
        self.rect.bottom = -1
        self.__speed = 10
        self.__speedtimer = 0
        
    def reset(self,playerposition):
        '''This method resets the position of the laser so it appears right
        above the player'''
        self.rect.center = playerposition
        
    def remove(self):
        '''This method sets the laser to be off screen'''
        self.rect.center = (-40,-100)
        
    def speed_up(self):
        '''This method increases the laser speed'''
        self.__speed = 15
        
    def update(self):
        '''This update method makes the laser go upwards towards the aliens,
        it also keeps track of how long the speedpowerup lasts''' 
        
        self.rect.centery -= self.__speed
        
        if self.__speed == 15:
            self.__speedtimer += 1
            
        #This adds a duration to the speed powerup, once the time is up the 
        #speed is set back to normal
        if self.__speedtimer == 100:
            self.__speed = 10
            self.__speedtimer = 0
        
class Background(pygame.sprite.Sprite):
    '''This class defines the sprite for the Background'''
    
    def __init__ (self,screen):
        '''This initializer takes the screen as a parameter, it initializes the 
        image and position of the background sprite'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/background.png")
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2,screen.get_height()/2)

class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines the sprite for the scorekeeper.'''
    
    def __init__(self,screen):
        '''This intializer takes the screen as a parameter, it initializes
        the font and starting score'''
        pygame.sprite.Sprite.__init__(self)
        
        self.__font = pygame.font.Font("fonts/font.ttf",16)
        self.__currentscore = 0
        self.__highscore = self.current_highscore()
    
    def add_score (self,points):
        '''This method takes points as a parameter, and upon being called
        adds those points to the score'''
        self.__currentscore += points
        
    def set_highscore(self):
        '''This method compares the current score with the highscore, and if the
        highscore is greater than or equal to the current score, it will be set
        as the new highscore in the text file '''
        
        self.__highscore = int(self.__highscore)
        if self.__currentscore >= self.__highscore:
            change_score = open('Highscore.txt','w')
            change_score.write(str(self.__currentscore))
            change_score.close()
            
    
    def current_highscore(self):
        '''This method reads the highscore textfile and returns the highscore integer value'''
        try:
            highscorefile  = open('Highscore.txt','r')
            self.__highscore = int(highscorefile.readline())
            highscorefile.close()
        except IOError:
            self.__highscore = 0
            
        return self.__highscore

    def score_status (self):
        '''This method returns the current score'''
        return self.__currentscore
        
    def update(self):
        '''This method is automatically called to update the scoreboard, and
        display the title of "Super Breakout"'''
        score_display = "Score: " + str(self.__currentscore) + "  " * 5 + \
            "SPACE INVADERS" + "  "*5  + "Highscore: " + str(self.__highscore)
        self.image = self.__font.render(score_display, 1, (0,255,0))
        self.rect = self.image.get_rect()
        self.rect.center = (325,18)
        
        if self.__currentscore > int(self.__highscore):
            self.__highscore = self.__currentscore
        
class LifeKeeper(pygame.sprite.Sprite):
    '''This class defines the sprite for the lifekeeper.'''
    
    def __init__(self,screen):
        '''This initializer takes the screen as a parameter, it initializes
        the starting lives and font.'''
        pygame.sprite.Sprite.__init__(self)
        self.__lives = 3
        self.__font = pygame.font.Font("fonts/font.ttf", 16)
    
    def remove_life(self):
        '''This method removes one life from the lives variable upon being
        called.'''
        self.__lives -= 1
        
    def add_life(self):
        '''This method adds an extra life for the players lives'''
        self.__lives += 1
        
    def life_status (self):
        '''This method returns the number represented by the lives variable'''
        return self.__lives
        
    def update(self):
        '''This method is automatically called to update the lives and
        display it for the player.'''
        life_display = "Lives " + str(self.__lives)
        self.image = self.__font.render(life_display, 1, (0,255,0))
        self.rect = self.image.get_rect()
        self.rect.center = (50,470)

class BonusAlien (pygame.sprite.Sprite):
    '''This class defines the sprite for the bonus red alien'''
     
    def __init__ (self,screen):
        '''This intializer takes the screen as a paramater, it initializes
        the center point of the bonus alien, ensuring it is off screen till
        it is randomly spawned in.'''
            
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.image = pygame.image.load("images/Bonus.gif")          
        self.rect = self.image.get_rect()
        self.rect.center = (800,-100)
        self.__death = False
        self.__deathdelay = 0
        
    def death(self):
        '''This method sets the self.__death boolean value to True'''
        self.__death = True
        
    def reset(self):
        '''This method resets the position of the alien so it is at
        the top of the screen but off to the left, and it will eventually 
        appear for the player shoot'''
        if self.__death != 'dead':
            self.rect.center = (-20,50)
            
    def update(self):
        '''This update method increases the center x value of the bonus
        alien by 5 every time it is called'''
        
        if self.__death != 'dead':
            self.rect.centerx += 5
        else:
            self.rect.center = (800,-100)
        
        if self.__death:
            self.__deathdelay += 1
        
        #Each image is loaded with a 3 tick delay between each    
        if self.__deathdelay == 1:
            self.image = pygame.image.load("images/bonusdeath1.gif")
        elif self.__deathdelay == 4:
            self.image = pygame.image.load("images/bonusdeath2.gif")
        elif self.__deathdelay == 7:
            self.image = pygame.image.load("images/bonusdeath3.gif")
        elif self.__deathdelay >= 10:
            self.__death = 'dead'

class PlayButton(pygame.sprite.Sprite):
    '''This class defines the sprite for the PlayButton that is on the
    load screen.'''
    
    def __init__(self,screen):
        '''This initializer method takes the screen as a parameter,
        it loads 2 images for the play button and initalizes the starting image 
        for the playbutton, it also places it on the screen'''
        
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.__images = [pygame.image.load("images/playnotpressed.png"),\
                         pygame.image.load("images/playpressed.png")]
        
        self.image = self.__images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (320,320)
        
    def swap(self,swap = False):
        '''This method takes swap as a boolean value, and switches the image
        upon being called'''
        if swap:
            self.image = self.__images[1]
        else:
            self.image = self.__images[0]
            
class MouseTracker(pygame.sprite.Sprite):
    '''This class defines the sprite for the MouseTracker.'''
    
    def __init__(self):
        '''This initializer creates a surface and makes a circle over'''
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, (0, 0, 0), (25, 25), 25, 0)
        self.rect = self.image.get_rect()
         
    def update(self):
        '''This method updates the circle so it follows the mouse pointer.'''
        # Moves the center of the circle to where the mouse is pointing
        self.rect.center = pygame.mouse.get_pos()
        
class InstructionButton(pygame.sprite.Sprite):
    '''This class defines the sprite for the Instruction button'''
    
    def __init__(self,screen):
        '''This initializer method takes the screen as a parameter, it loads
        the images and initializes the starting image and position.'''
        
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.__images = [pygame.image.load("images/instructionnotpressed.png"),\
                         pygame.image.load("images/instructionpressed.png")]
        
        self.image = self.__images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (320,360)
        
    def swap(self,swap = False):
        '''This method takes swap as a boolean value, and switches the image
        upon being called'''
        if swap:
            self.image = self.__images[1]
        else:
            self.image = self.__images[0]
            
class BackButton(pygame.sprite.Sprite):
    '''This class defines the sprite for the BackButton on the instruction page'''
    
    def __init__(self,screen):
        '''This initializer method takes the screen as a parameter, it loads
        the images and initializes the starting image and position.'''   
        
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.__images = [pygame.image.load("images/backnotpressed.png"),\
                         pygame.image.load("images/backpressed.png")]
        
        self.image = self.__images[0]
        self.rect = self.image.get_rect()
        self.rect.right = 640
        self.rect.bottom = 480
        
    def swap(self,swap = False):
        '''This method takes swap as a boolean value, and switches the image
        upon being called'''        
        if swap:
            self.image = self.__images[1]
        else:
            self.image = self.__images[0]
            
class SpaceInvaderLogo(pygame.sprite.Sprite):
    '''This class defines the sprite for the Space Invaders logo on the load screen'''
    
    def __init__ (self,screen):
        '''This initializer takes the screen as a parameter, it initializes
        the image and position of the image''' 
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/spaceinvaders.png")
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2+15,130)
        

class Wall(pygame.sprite.Sprite):
    ''' This class defines the sprite for the Wall(s) that protect the player'''
    
    def __init__(self,screen,startx,starty,wallnumber):
        '''This initializer takes the screen, start x and y positions as well as
        the wall number as parameters, it initializes the image and position
        for the walls. Based on the wallnumber passed in the walls x position
        are shifted'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((6,6))
        self.image.fill((0,255,0))
        self.image.convert()
        self.rect = self.image.get_rect()
        
        #Shifts the walls based on the parameter passed when creating it
        self.rect.center = ((startx+150*wallnumber),starty)
           
            
class Instructions(pygame.sprite.Sprite):
    '''This class defines the sprite for the Instructions text'''
    
    def __init__(self,screen):
        '''This initializer method takes the screen as a parameter, and initializes
        the instructions text in a list, it then renders each line of text onto the
        surface'''
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/instructionsbackground.gif")
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2,screen.get_height()/2)
        

class Heart(pygame.sprite.Sprite):
    '''This class defines the sprite for the Heart'''
    
    def __init__(self,screen,startposition):
        '''This initializer takes the screen and start position as a tuple for
        parameters, it initializes the image and position of the heart when
        created.'''
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/heart.gif")
        self.rect = self.image.get_rect()
        self.rect.center = startposition
    
    def update(self):
        '''This update method shifts the heart down 3 pixels each time,
        when the top of the heart reaches the bottom it kills the heart'''
        self.rect.centery += 3
        
        if self.rect.top > 480:
            self.kill()

class SpeedBoost(pygame.sprite.Sprite):
    '''This class defines the sprite for the SpeedBoost'''
    
    def __init__(self,screen,startposition):
        '''This initializer takes the screen and start position as a tuple
        for parameters. It initializes the image and position of the speed
        boost powerup.'''
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/speedboost.gif")
        self.rect = self.image.get_rect()
        self.rect.center = startposition
        
        
    def update(self):
        '''This update method shifts the powerup down 3 pixels each time,
        when the top of the powerup reaches the bottom it kills the powerup'''
        self.rect.centery += 3
        
        if self.rect.top > 480:
            self.kill()
            
class Missile(pygame.sprite.Sprite):
    '''This class defines the sprite for the missile shot by the bonus alien'''
        
    def __init__ (self,screen):
        '''This initializer method takes the screen and startposition as a tuple
        for parameters, it initializes the start position and image for the missile.'''
            
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bonusmissile.gif")
        
        self.rect = self.image.get_rect()
        self.rect.center = (-40,490)
        self.__shoot = True
        
    def reset(self,position):
        '''This method respositions the missile so it appears to come from
        the bonus alien'''
        if self.__shoot:
            self.rect.center = position
            self.__shoot = False
    
    def remove(self):
        '''This method repositions the missile off the screen'''
        self.rect.center = (-40,300)
            
    def update(self):
        '''This update method shifts the missile down, toward the walls
        by 2 pixels. Upon the top of the missile reaching the bottom self.__shoot
        is set to true'''         
        self.rect.centery += 2
        
        #This allows the missile to be shot again without constantly reappearing
        #from the bonus alien
        if self.rect.top > 530:
            self.__shoot = True
        
        
        
        
        
        
        
        
        
        
            
    
        
            