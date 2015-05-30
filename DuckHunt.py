"""
    Program......: challenge12_3.py
    Author.......: Michael Rouse
    Date.........: 3/24/13
    Description..: My Own version of "Duck Hunt"
"""
from livewires import games, color
import pygame.display, pygame.mouse
from random import randint, randrange

# Setup game window
games.init(screen_width=640, screen_height=480, fps=50)
pygame.display.set_caption("Duck Hunt")

# Tree and grass to bring to the front
foreground = games.Sprite(image=games.load_image("Sprites/foreground.png"), left=0, bottom=390)
games.screen.add(foreground)

# CLASS ====================================
# Name.........: Cursor
# Description..: Sets mouse to the crosshair
# Syntax.......: Cursor()
# ==========================================
class Cursor(games.Sprite):
    """ Cursor Object """
    clicked = False
    
    xPos = games.mouse.x
    yPos = games.mouse.y
    
    def __init__(self):
        """ Cursor Initializer """
        super(Cursor, self).__init__(image=games.load_image("Sprites/cursor.png"), x=games.mouse.x, y=games.mouse.y)
        
        self.mouseClicked = False
        self.mouseCounter = 0

        # Load gunshot sound
        self.gunShotSound = games.load_sound("Sounds/shot.wav")
        
    def update(self):
        # Keep the sprite at the same x and y location as the mouse
        self.x = Cursor.xPos
        self.y = Cursor.yPos

        # Remove and readd to put on top of any birds
        games.screen.remove(self)
        games.screen.add(self)
        
    def tick(self):
        """ Check For Mouse Click """
        if not Game.paused and not Game.over:
            # Check if the mouse was clicked
            if games.mouse.is_pressed(0) and not Cursor.clicked:
                # Play Gunshot Sound and add Total Sounds
                Cursor.clicked = True
                self.gunShotSound.play()
                Game.totalShots += 1
            
            # Avoid repeated mouse clicks 
            if Cursor.clicked:
                if self.mouseCounter > 10 and not games.mouse.is_pressed(0):
                    Cursor.clicked = False
                    self.mouseCounter = 0

                else:
                    self.mouseCounter += 1

            # Update cursor position
            Cursor.xPos = games.mouse.x
            Cursor.yPos = games.mouse.y

            # Bring the tree and grass infront of all the ducks
            foreground.elevate()


# CLASS ====================================
# Name.........: Duck
# Description..: Class for a duck
# Syntax.......: Duck()
# ==========================================
class Duck(games.Sprite):
    """ Duck Class """
    def __init__(self, duckType):     
        # Colors Available
        colors = [3, "black", "blue", "red"]
        duckColor = colors[duckType]
           
        # Sprites for the Duck
        self.flyRight = [3, games.load_image("Sprites/" + duckColor + "/duck1.png"), games.load_image("Sprites/" + duckColor + "/duck2.png"),
                            games.load_image("Sprites/" + duckColor + "/duck3.png")]
        
        self.flyStraightRight = [3, games.load_image("Sprites/" + duckColor + "/duck4.png"), games.load_image("Sprites/" + duckColor + "/duck5.png"),
                                    games.load_image("Sprites/" + duckColor + "/duck6.png")]

        self.flyLeft = [3, games.load_image("Sprites/" + duckColor + "/duck7.png"), games.load_image("Sprites/" + duckColor + "/duck8.png"),
                           games.load_image("Sprites/" + duckColor + "/duck9.png")]

        self.flyStraightLeft = [3, games.load_image("Sprites/" + duckColor + "/duck10.png"), games.load_image("Sprites/" + duckColor + "/duck11.png"),
                                   games.load_image("Sprites/" + duckColor + "/duck12.png")]

        self.die = [3, games.load_image("Sprites/" + duckColor + "/duckDie1.png"), games.load_image("Sprites/" + duckColor + "/duckDie2.png"),
                       games.load_image("Sprites/" + duckColor + "/duckDie3.png")]

        # Intialize Duck Sprite At Random X-Location
        super(Duck, self).__init__(image=self.flyRight[1], x=randint(10, 470), y=350, dx=0, dy=-1)
        
        # Point Values Based On Duck Color
        pointValues = {"blue": 25, "red": 50, "black": 75}
        
        # Direction Constants
        self.RIGHT = 1
        self.LEFT = 2
        
        # Duck Variables
        self.alive = True
        self.direction = randint(1, 2)
        self.straight = False # True if duck is flying straight
        self.points = pointValues[duckColor]
        
        # Animation Frames
        self.frames = [4, self.flyRight[2], self.flyRight[3], self.flyRight[2], self.flyRight[1]]
        
        # Points above the duck's head when it's shot
        self.deathScore = games.Text(value=str(self.points), size=25, x=self.x, y=self.top - 5, color=color.white)
        
        # Animation Variables
        self.dieDelay = 0 # Delay Duck Falling
        self.continueDeath = False
        self.animationCount = 0
        self.frame = 1 # What frame of the animation?
        self.directionCount = 0
        
        # Set velocity based on direction
        if self.direction == self.RIGHT:
            self.dx = .5
                   
        else:
            self.dx = -.5

    def change_direction(self):
        """ Decide to change duck's direction """
        randomNum = randint(1, 340)
        
        if randomNum % 5 == 0:
            # Switch the duck's direction
            if self.direction == self.RIGHT:
                self.direction = self.LEFT
                self.dx = -.5
                
            else:
                self.direction = self.RIGHT
                self.dx = .5
        
        # Decide if it will fly straight or not
        randomNum = randint(1, 340)
        
        if randomNum % 5 == 0:
            # Change duck to straight or up
            self.straight = not self.straight
        
    def update(self):
        """ Update the sprite """
        global foreground
        
        if not Game.paused and not Game.over:
            # Check if the duck is alive
            if self.alive:
                # Duck is alive
                if self.bottom < 0 or self.right < 0 or self.left > 640:
                    # Duck is off the screen, destroy
                    self.destroy()

                # Check if the duck should try and change directions
                if self.directionCount < 100:
                    self.directionCount += 1
                
                else:
                    self.change_direction()
                    self.directionCount = 0
                
                # Check if the duck is going straight and change velocity
                if self.straight:
                    self.dy = 0
                
                    if self.direction == self.RIGHT:
                        self.dx = 1
                    
                    else:
                        self.dx = -1
                    
                else:
                    # Duck is flying upwards
                    self.dy = -1

                
                # Update the animation frames based on duck's velocity
                if not self.alive:
                    self.frames = [2, self.die[2], self.die[3]]
                    
                elif self.direction == self.RIGHT:
                    if self.straight:
                        self.frames = [4, self.flyStraightRight[2], self.flyStraightRight[3], self.flyStraightRight[2], self.flyStraightRight[1]]
                        
                    else:
                        self.frames = [4, self.flyRight[2], self.flyRight[3], self.flyRight[2], self.flyRight[1]]
                
                elif self.direction == self.LEFT:
                    if self.straight:
                        self.frames = [4, self.flyStraightLeft[2], self.flyStraightLeft[3], self.flyStraightLeft[2], self.flyStraightLeft[1]]

                    else:
                        self.frames = [4, self.flyLeft[2], self.flyLeft[3], self.flyLeft[2], self.flyLeft[1]]

                if self.frame > self.frames[0]:
                    self.frame = 1
                    
                # Check for mouse clicks
                if Cursor.clicked:
                    # Prevent the shooting of a duck that's behind the tree
                    if not (Cursor.xPos in range(150, 240) and Cursor.yPos in range(220, 390)):
                        # Check if the mouse was over the duck
                        if Cursor.xPos in range(self.left, self.right) and Cursor.yPos in range(self.top, self.bottom):
                            # Duck was shot - Kill it
                            self.shot()
                        
            else:
                # Duck is Dead, Destroy once it hits the ground
                if self.bottom > 370:
                    self.destroy()
                
    def shot(self):
        """ Kill the duck """
        Game.update_score(self.points)
        
        self.alive = False # Set the duck to dead
        
        self._replace(self.die[1]) # Replace with starting death animation
        
        self.frame = 1
        self.animationCount = 0
        
        # Freeze the duck
        self.dx = 0
        self.dy = 0
        
        # Display score above ducks head
        self.deathScore.x = self.x
        self.deathScore.y = self.top - 10
        
        games.screen.add(self.deathScore)

    def update_animation(self):
        self.animationCount += 1
        
        if self.animationCount >= 17:
            # Change animation for falling dead duck
            if not self.alive:
                if self.continueDeath:
                    self.dy = 2
                    
                    # Advance the Death Animation
                    frames = [2, self.die[3], self.die[2]]
                    
                    self._replace(frames[self.frame])

                    self.frame += 1

                    # Make Sure the frame stays within the correct range
                    if self.frame > frames[0]:
                        self.frame = 1
                
            # Change animation for duck that's not dead
            else:
                if self.frame > self.frames[0]:
                    self.frame = 1

                self._replace(self.frames[self.frame])

                self.frame += 1

                if self.frame > self.frames[0]:
                    self.frame = 1
                    
            # Reset the animation counter
            self.animationCount = 0
            
    def tick(self):
        """ Tick Method """
        # Tick only if game is not paused
        if not Game.paused:
            if not self.alive:
                # This will display the point value above the head and when it's done the duck will start to fall
                if self.dieDelay > 50 and not self.continueDeath:
                    self.dy = 1
                    
                    self.continueDeath = True
                    self.frame = 1
                    games.screen.remove(self.deathScore)

                elif not self.continueDeath:
                    self.dieDelay += 1
                    
            # This elif will help birds continue to fly
            # At the correct angle and direction after restuming from a pause
            elif (self.dx == 0) and (self.dy == -1):
                if not self.straight:
                    if self.direction == self.RIGHT:
                        self.dx = .5
                    
                    else:
                        self.dx = -.5
            
            # Update the Duck's animation
            self.update_animation()

        elif Game.paused:
            # Game is Paused - Freeze the duck
            self.dx = 0
            self.dy = 0

# CLASS ====================================
# Name.........: Clock
# Description..: Displays the clock object on the screen
# Syntax.......: Clock()
# ==========================================
class Clock(games.Sprite):
    """ Class for displaying the Clock """
    def __init__(self):
        super(Clock, self).__init__(image=Game.image, x=0, y=0)

        # Timer Display
        self.timer = games.Text(value="1:00", size=50, x=300, y=435, color=color.white)
        games.screen.add(self.timer)
        
        self.clockCount = 0
        self.seconds = 60
        
        # Sound For Last 10 Seconds
        self.sound = games.load_sound("Sounds/beep.wav")

        self.started = False

    # Start the clock
    def start_clock(self):
        self.started = True
    
    def update(self):
        # Check if clock has run out of time
        if self.seconds <= 0:
            self.started = False
            Game.over = True

            games.mouse.is_visible = True # Show mouse
        
        # Change the clock's color to red when it gets down to the last minute
        if self.seconds <= 10:
            self.timer.color = color.red

        # Keep the clock in the same position
        self.timer.left = 280

    # Update the Clock's Label
    def update_clock(self):
        label = "0:"
        
        if self.seconds < 10:
            label += "0" + str(self.seconds)

        else:
            label += str(self.seconds)

        # Play sound on final 10 seconds
        if self.seconds < 11:
            self.sound.play()

        # Update The Clock's Label
        self.timer.value = label

    # Perform the Clock countdown
    def tick(self):
        # Only Do Countdown if not paused and playing the game
        if self.started and not Game.paused:
            if self.clockCount >= 100:
                self.seconds -= 1

                # Show the new time on the clock
                self.update_clock()

                self.clockCount = 1
                
            else:
                self.clockCount += 1

# CLASS ====================================
# Name.........: Game
# Description..: Will spawn ducks/check for pause
# Syntax.......: Game()
# ==========================================
class Game(games.Sprite):
    """ Duck Spawner Class """
    image = games.load_image("sprites\spawner.png")

    # Scoring
    score = 0 
    ducksHit = 0
    totalShots = 0 # Total Shots Taken
    totalDucks = 0 # Total Ducks Spawned

    # State of Game
    paused = False # True when game is paused
    over = False # True when game is over
    
    # Label for total points
    scoreLabel = games.Text(value="0", size=25, left=500, y=428, color=color.white)
    games.screen.add(scoreLabel)

    # Label for number of ducks shot
    ducksShotLabel = games.Text(value="0", size=30, x=70, y=418, color=color.white)
    games.screen.add(ducksShotLabel)
    
    def __init__(self):
        super(Game, self).__init__(image=Game.image, x=0, y=0)

        # Instructions Labels
        self.instructions = games.Text(value="Shoot as many ducks as possible in 1 minute!", size=35, x=320, y=100, color=color.white)
        self.instructions2 = games.Text(value="Press \"P\" To Pause", size=35, x=320, y=140, color=color.white)
        games.screen.add(self.instructions)
        games.screen.add(self.instructions2)
        
        # Paused Game Sprite
        self.paused = games.Sprite(image=games.load_image("Sprites/paused.png"), x=320, y=240, dx=0, dy=0)
                                      
        # Final Results Labels
        self.results = games.Text(value="", size=35, x=320, y=100, color=color.white) # How many ducks were hit
        self.results2 = games.Text(value="", size=35, x=320, y=140, color=color.white)# Accuracy

        # Counters to delay events
        self.spawnCounter = 0
        self.menuCounter = 0
        
        self.keyDelay = 0
        self.keyDelayStart = False
        
        self.playing = False # Set to true after instructions go away
        
        # Create the timer for the game
        self.gameTimer = Clock()
        games.screen.add(self.gameTimer)
        
    def spawn(self):
        """ Spawn a duck """
        # Generate a radnom colored duck
        new_duck = Duck(randint(1, 3))

        Game.totalDucks += 1
            
        games.screen.add(new_duck)

    def update(self):
        # Check if the game time is up
        if Game.over:
            self.menuCounter = 0
            self.playing = False
            Game.over = True

            # Show results
            self.results.value = "You hit " + str(Game.ducksHit) + " of " + str(Game.totalDucks) + " ducks!"
            self.results2.value = "Accuracy: " + str(int((int(Game.ducksHit) / Game.totalShots) * 100)) + "%"

            games.screen.add(self.results)          
            games.screen.add(self.results2)
            
            self.destroy()
            
    def tick(self):
        if self.playing and not Game.paused and not Game.over:
            # Keep counting until the duck spawner should spawn a new duck
            self.spawnCounter += 1

            if self.spawnCounter >= 75:
                self.spawn()
                self.spawnCounter = 0
            
        elif not Game.paused and not Game.over:
            # Keep counting until the menu should dissapear
            if self.menuCounter >= 250:
                games.screen.remove(self.instructions)
                games.screen.remove(self.instructions2)
                self.menuCounter = 0
                self.playing = True
                self.gameTimer.start_clock()
                
            else:
                self.menuCounter += 1
        
        elif not Game.paused and not Game.over:
            # Keep the final results until they should dissapear
            if self.menuCounter >= 500:
                self.destroy()
                exit
                
            else:
                self.menuCounter += 1
        
        # Check for the pause button to be pressed
        if games.keyboard.is_pressed(games.K_p) and not Game.over:
            if self.keyDelay == 0:
                # Pause or unpause the game
                Game.paused = not Game.paused
                self.keyDelayStart = True
                
                # Display the pause sprite if on pause, remove if not
                if Game.paused:
                    games.screen.add(self.paused)
                    games.screen.add(self.instructions)
                                   
                else:
                    # Keep mouse at position it was in when it paused to avoid cheating
                    pygame.mouse.set_pos(Cursor.xPos, Cursor.yPos)

                    # Remove pause label and instructions
                    games.screen.remove(self.paused)
                    games.screen.remove(self.instructions)
        
        # Advance the keyboard delay
        if self.keyDelayStart:
            if self.keyDelay > 10:
                self.keyDelay = 0
                self.keyDelayStart = False

            else:
                self.keyDelay += 1

    def update_score(points):
        """ Update The Game Score """
        Game.score += points
        Game.ducksHit += 1

        Game.scoreLabel.value = Game.score
        Game.ducksShotLabel.value = Game.ducksHit

        Game.scoreLabel.left = 500

# FUNCTION ==================================
# Name.........: Main
# Description..: Will start the game
# Syntax.......: main()
# ==========================================
def main():
    # Setup background
    games.screen.background = games.load_image("background.png", transparent=False)

    game = Game()
    crosshair = Cursor()
    
    games.screen.add(game)
    games.screen.add(crosshair)

    games.mouse.is_visible = False

    games.screen.mainloop()


# Start!
main()
