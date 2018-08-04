"""

   Name: AYUSH GUPTA
   
   Date: May 29, 2016
   
   Description: This program utilizes pygame, and sprite classes from the
   pySprites file to create the game known as Space Invaders, a game made by
   Atari. This version has a few twists.
   
"""

# I - IMPORT AND INITIALIZE
import pygame, pySprites,random
pygame.init()
pygame.mixer.init()
     
def game():
    '''This function defines the main game for Space Invaders, it takes no 
    parameters, and returns nothing, which causes the main function to exit
    meaning the game has ended. '''  
    # DISPLAY
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Space Invaders by AYUSH")
     
    # ENTITIES
    background = pygame.Surface(screen.get_size())
    
    #ALIENS CREATION
    y_coordinate = 200
    alien_list = []
    
    #A row of aliens are created and appended to two lists, one list that contains 
    #groups of the aliens based on its row, and one that contains all the aliens together
    for alien_row in range (5):
        alien = 0
        points = (alien_row+1)*10
        for x_coordinate in range(0,550,50):
            alien = pySprites.Alien(screen,alien_row,(79+x_coordinate,y_coordinate), points)
            alien_list.append(alien)
        y_coordinate -= 30

    #Sound Effects    
    laser_sound = pygame.mixer.Sound("sounds/lasersound.wav")
    laser_sound.set_volume(0.8)
    alien_sound = pygame.mixer.Sound("sounds/aliensound.wav")
    alien_sound.set_volume(0.8)
    alien_pop = pygame.mixer.Sound("sounds/alienpop.wav")
    alien_pop.set_volume(0.7)
    bonussound = pygame.mixer.Sound("sounds/bonussound.wav")
    bonussound.set_volume(0.8)
    gameover_music = pygame.mixer.Sound("sounds/gameover.wav")
    gameover_music.set_volume(0.8)
          
    #SPRITES
    gameover = pygame.image.load("images/gameover.png")
    bonusmissile = pySprites.Missile(screen)
    wall = wallcreate(screen)
    bonusalien = pySprites.BonusAlien(screen)
    player = pySprites.Player(screen)
    scorekeeper = pySprites.ScoreKeeper(screen)
    liveskeeper = pySprites.LifeKeeper(screen)
    background_image = pySprites.Background(screen)
    endzoneleft = pySprites.EndZone(screen,0)
    endzoneright = pySprites.EndZone(screen,639)
    endzonebottom = pySprites.EndZone(screen,0,True)
    laser = pySprites.Laser(screen)
    endzoneSprites = pygame.sprite.Group(endzoneright,endzoneleft)
    playergroup = pygame.sprite.Group(player)
    alienSprites = pygame.sprite.Group(alien_list)
    alienlasers = pygame.sprite.Group()    
    extra_lives = pygame.sprite.Group()
    speedboostGroup = pygame.sprite.Group()
    bottomlayer = [background_image,scorekeeper,liveskeeper,endzoneSprites,endzonebottom]
    toplayer = [player,alienSprites,bonusalien,laser,alienlasers,wall,extra_lives,speedboostGroup,bonusmissile]
    allSprites = pygame.sprite.OrderedUpdates(bottomlayer,toplayer)

    
    # ASSIGN 
    keepGoing = True
    clock = pygame.time.Clock()
    bonusaliendead = False
    alienshoot_speed = 27
    heartspawn = False
    damagedelay = 0
    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
 
    # LOOP
    while keepGoing:
        
        # TIME
        clock.tick(30)
        
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scorekeeper.set_highscore()
                keepGoing = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and laser.rect.bottom < 0:
                    laser_sound.play()
                    laser.reset((player.rect.centerx,player.rect.top))
                    
        #Movement based on user pressing or holding right or left keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.go_left()
        elif keys[pygame.K_RIGHT]:
            player.go_right()
            
        if (liveskeeper.life_status() <= 0) or (len(alienSprites) == 0):
            scorekeeper.set_highscore()
            keepGoing = False    
                    
        if (random.randrange(200) == 0) and (bonusalien.rect.left > 800) and (not bonusaliendead):
            bonusalien.reset()
        
        #If the player laser collides with the bonus alien then the bonus alien's 
        #death animation is played and is killed
        if laser.rect.colliderect(bonusalien) and (not bonusaliendead):
            scorekeeper.add_score(40)
            bonusalien.death()
            laser.remove()
            bonusaliendead = True
            
        #For each wall pixel a random number is generated, if the number is 0,
        #and the alien is in +- 10 pixels of range of the wall pixel then a missile is dropped
        for wallpixel in wall:
            bonus_missile = random.randrange(400)
            if bonus_missile == 0 and bonusalien.rect.centerx in range(wallpixel.rect.centerx-10,wallpixel.rect.centerx+10):
                bonusmissile.reset((bonusalien.rect.centerx,bonusalien.rect.bottom))
                bonussound.play()
                
        #if the bonus alien's missile collides with a wall chunks of it are removed
        if pygame.sprite.spritecollide(bonusmissile, wall, True):
            damagedelay += 1
            #By delaying the time the laser is removed it allows it to progress further
            #into the walls
            if damagedelay == 6:
                bonusmissile.remove()
                damagedelay = 0
        
        for aliens in alienSprites:
            shoot = random.randrange(alienshoot_speed*16)
            shoot_random = random.randrange(alienshoot_speed*700)  
            #If randrange is equal to 1 and the aliens are in range of the players x coordinate they shoot 
            if shoot == 1 and aliens.rect.centerx in range (player.rect.centerx-20,player.rect.centerx+20):
                    alien_laser = pySprites.AlienLaser(screen,(aliens.rect.centerx,aliens.rect.bottom))
                    alienlasers.add(alien_laser)
                    alien_sound.play()
                    allSprites = pygame.sprite.OrderedUpdates(bottomlayer,toplayer)
                    
            #If randrange is equal to 1 the alien shoots this is to make it have
            #there are two separate scenarios to have it seem kind of random
            #and at the same time make it difficult for the player
            if shoot_random == 1:
                    alien_laser = pySprites.AlienLaser(screen,(aliens.rect.centerx,aliens.rect.bottom))
                    alienlasers.add(alien_laser)
                    alien_sound.play()
                    allSprites = pygame.sprite.OrderedUpdates(bottomlayer,toplayer)
                    

        #When an alien collides with the endzones they all change direction and move down 3 pixels
        alien_bottomwall = pygame.sprite.spritecollide(endzonebottom,alienSprites,False)
        for endzones in endzoneSprites:
            alien_wallcollision = pygame.sprite.spritecollide(endzones,alienSprites,False)
            if alien_wallcollision != []:
                for aliens in alienSprites:
                    if alien_bottomwall == []:
                        aliens.switch_direction()
                        aliens.go_down()
                        aliens.speed_up()
                        alienshoot_speed = aliens.get_speed()     
                    else:
                        aliens.switch_direction()
                        
        #If alien lasers collide with the player, the player loses a live and the
        #laser is killed
        for alien_laser in alienlasers:
            player_hit = pygame.sprite.spritecollide(alien_laser, playergroup, False)
            if player_hit != []:
                alien_laser.kill()
                liveskeeper.remove_life() 
        
        #To check for collision between a piece of the wall and the laser        
        for alien_laser in alienlasers:
            wall_hit = pygame.sprite.spritecollide(alien_laser,wall,False)
            if wall_hit !=[]:
                alien_laser.kill()
                for wallpieces in wall_hit:
                    wallpieces.kill()

                
        #If the player laser collides with an alien, the alien is killed, points are
        #added to the score and the laser is removed  
        alien_collided = pygame.sprite.spritecollide(laser, alienSprites, False)
        for aliens in alien_collided :
            scorekeeper.add_score(aliens.get_points())
            
            #This creates an extralife powerup based on a 5% chance when an alien is killed
            if random.randrange(15) == 0:
                heartspawn = True
                heart = pySprites.Heart(screen,aliens.rect.center)
                extra_lives.add(heart)
                allSprites = pygame.sprite.OrderedUpdates(bottomlayer,toplayer)
                
            #This creates a speedboost powerup by a random 5% chance, and ensures
            #that a extralife and speedboost don't come from the same one alien
            if (random.randrange(15) == 0) and (not heartspawn):
                speedboost = pySprites.SpeedBoost(screen,aliens.rect.center)
                speedboostGroup.add(speedboost)
                allSprites = pygame.sprite.OrderedUpdates(bottomlayer,toplayer)
            heartspawn = False
            alien_pop.play()
            aliens.death()
            laser.remove()
        
        #If the player collides with the heart they recieve an additional life
        if pygame.sprite.spritecollide(player, extra_lives, True):
            liveskeeper.add_life()
        
        #If the player collides with the speedboost powerup they recieve a temporary
        #movespeed increase and are able to shoot faster for about 5seconds
        if pygame.sprite.spritecollide(player, speedboostGroup, True):
            player.speed_up()
            laser.speed_up()
            
        
        #If the players lasers collide with the walls, the piece of the wall is 
        #killed and the laser is removed not killed
        wall_collided = pygame.sprite.spritecollide(laser,wall,False)
        for wallpieces in wall_collided:
            laser.remove()
            wallpieces.kill()
               
        # Refresh Screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)       
        pygame.display.flip() 
        
    screen.blit(gameover, (0, 0))
    gameover_music.play()
    pygame.display.flip()       
    return   

def loadscreen ():
    '''This function displays a menu screen, where the user can choose to 
    play the game or view the instruction screen, it returns keepGoing as a 
    boolean value if the player presses the exit button, aswell as playgame
    and instructionscreen as boolean values so the main function can determine
    which function to load.'''
    
    #Display
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Space Invaders by AYUSH")
     
    # ENTITIES
    background = pygame.Surface(screen.get_size())
    background_image = pySprites.Background(screen)
    title = pySprites.SpaceInvaderLogo(screen)
    mousepointer = pySprites.MouseTracker()
    playbutton = pySprites.PlayButton(screen)
    instructionbutton = pySprites.InstructionButton(screen)
    allSprites = pygame.sprite.OrderedUpdates(background_image,title,playbutton,instructionbutton,mousepointer)
    
    #Assign
    clock = pygame.time.Clock()
    keepGoing = True
    clicking = False
    click = True
    playgame = False
    instructionscreen = False
    
    #LOOP
    while keepGoing and not playgame and not instructionscreen:
        
        #TIME
        clock.tick(30)
        
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            #If the user has pressed the button down, clicking is set to True    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicking = True
            #If the user has pressed the button down and they let go, click is set to True
            elif event.type == pygame.MOUSEBUTTONUP and clicking:
                click = True
            else:
                clicking = False
                click = False
                
        #This swaps the image if the player is hovering the button with their mouse         
        if mousepointer.rect.colliderect(playbutton):
            playbutton.swap(True)
        else:
            playbutton.swap(False)
            
        #This swaps the image if the player is hovering the button with their mouse     
        if mousepointer.rect.colliderect(instructionbutton):
            instructionbutton.swap(True)
        else:
            instructionbutton.swap(False)
        
        #If the user has clicked, and the mouse was on the button then proceed                           
        if mousepointer.rect.colliderect(playbutton) and click:
            playgame = True
            
        #If the user has clicked, and the mouse was on the button then proceed     
        if mousepointer.rect.colliderect(instructionbutton) and click:
            instructionscreen = True
                    
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)       
        pygame.display.flip()
        
        
    return keepGoing,playgame,instructionscreen

def instructions():
    '''This function displays all the instructions for the player,
    and returns keepGoing as a boolean value if the user presses the exit 
    button, and back as a boolean value if they press the back button.'''
    
    #Display
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Space Invaders by AYUSH")
       
    #Entities
    instructions = pySprites.Instructions(screen)
    background = pygame.Surface(screen.get_size()) 
    background_image = pySprites.Background(screen)
    backbutton = pySprites.BackButton(screen)
    mousepointer = pySprites.MouseTracker()
    allSprites = pygame.sprite.OrderedUpdates(background_image,instructions,backbutton,mousepointer)
    
    #Assign
    keepGoing = True
    clock = pygame.time.Clock()
    clicking = False
    click = True
    back = False
    
    #Loop
    while keepGoing:
        
        #Time
        clock.tick(30)
        
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicking = True
            elif event.type == pygame.MOUSEBUTTONUP and clicking:
                click = True
            else:
                clicking = False
                click = False
                
        #This swaps the image if the player is hovering the button with their mouse        
        if mousepointer.rect.colliderect(backbutton):
            backbutton.swap(True)
        else:
            backbutton.swap(False)
            
        #If the user has clicked, and the mouse was on the button then proceed         
        if mousepointer.rect.colliderect(backbutton) and click:
            return back,keepGoing
        
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)       
        pygame.display.flip()
          
    return back,keepGoing

def wallcreate(screen):
    '''This function creates the walls for the player's defense. It returns
    a group of the walls together'''
   
    #WALL CREATION     
    wall = pygame.sprite.Group()
    
    #This list is to design the shape of the wall, where there is a 0,
    #the spot will be avoided and the x-coord will move forward and read the
    #next spot on the list to check for ones
    wallshape =[[0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0],
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
            [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1],
            [1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1],
            [1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1],
            [1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1],
            [1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1]]
    
    starty = 350
    startx = 65
    m = 65

    for wallnumber in range (5):
        #This loop goes through each nested list
        for wallrow in wallshape:
            #This loop goes through each integer in the list
            for brick in wallrow:
                if brick != 0:
                    wallpiece = pySprites.Wall(screen,startx,starty,wallnumber)
                    wall.add(wallpiece)
                startx += 5
            startx = 65
            starty +=3
        starty = 350    

    return wall


def main():
    '''This function defines the mainline logic for the program'''
    
    keepGoing = True
    back = False
    
    #Background Music
    pygame.mixer.music.load("sounds/backgroundmusic.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    
    #Loop
    while keepGoing:
        
        #Load screen returns boolean values based on events
        keepGoing,playgame,instructionscreen = loadscreen()
        
        #Based on the values from loadscreen different functions are loaded
        if keepGoing and playgame:
            keepGoing = game()
            
        elif keepGoing and instructionscreen:
            back,keepGoing = instructions()
            
        elif back and keepGoing:
            loadscreen()
            
    pygame.mixer.music.fadeout(2000)
    pygame.time.delay(4000) 
    pygame.quit()


main()   