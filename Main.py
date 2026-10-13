DEBUG = False
DEBUG_EVENT = "Locked holes"
SOUND_EFFECTS_ENABLED = True
WIGGLE_TITLE = True
MOUSE_POINTER = True
#Imports

import pygame, sys, time, random

#Initialisation
pygame.init()
pygame.mixer.quit()
pygame.mixer.init()
screen = pygame.display.set_mode((1280,720))
screen.fill(color="White")
pygame.display.set_caption("8 Ball Chaos")
pygame.display.set_icon(pygame.image.load('./Resources/Icon/Icon.png').convert_alpha())
frame_rate = 288
font_size = 50
game_font = pygame.font.Font("Resources\Text\Jersey_15\Jersey15-Regular.ttf", font_size)
if MOUSE_POINTER:
    pygame.mouse.set_visible(False)


from math import degrees, atan, sin, cos, floor
import numpy as np
from FadeScreen import Fade
from Spritesheet import SpriteSheet
from UsedClasses import *
#Runs on startup - loads everything that needs to be loaded including pygame, vars, surfaces ect.


#Assign the clock class to an object and set the framerate to frame_rate
clock = pygame.time.Clock()
clock.tick(frame_rate)
previous_time_since_start = time.time()

#Essential Vars

#IS_LOADING will be checked when making an input to prevent any further inputs from being done if this is true
IS_LOADING = False

#WHAT_AM_I_RENDERING will determine what is rendered and will allow the program to loop in one menu, bettering performance and will exit once this is equal to a number different to what it was before.
WHAT_AM_I_RENDERING = 0
#WAIR = 0 - Render the main menu
#WAIR = 1 - Render the play menu
#WAIR = 2 - Render the game ("With Events" rules)
#WAIR = 3 - Render the game ("Without Events" rules)
#WAIR = 4 - Render the settings menu
#WAIR = 5 - Render the customisation menu
#WAIR = 6 - Render the test scene (will not be used in final submission)

#LOADING_SCREEN holds the loading screen texture as it is pretty much used everywhere
LOADING_SCREEN = pygame.image.load("Resources\Backgrounds\Loading_Screen.png").convert()

#DATA_STORAGE holds all sprites that need to be used for that frame in this list. Sprites held depends on the value of WAIR. They will always be held in the same order, shown below.
#This definition is not strictly necessary but will help me remember everything about data_storage during programming.
DATA_STORAGE = {
    "Buttons" : [],
    "User input variables" : [],
    "Game variables" : [],
    "Balls" : [],
    "Other" : [],
    "Background image" : []
}


#Attempt to load profile pictures
try:
    player_1_pfp = pygame.image.load("Resources\Profile_pictures\Player1.png").convert()
    player_1_pfp = pygame.transform.scale(player_1_pfp, (96,96))
except:
    player_1_pfp = pygame.image.load("Resources\Menu\DefaultPFP.png").convert()
    player_1_pfp = pygame.transform.scale(player_1_pfp, (96,96))

try:
    player_2_pfp = pygame.image.load("Resources\Profile_pictures\Player2.png").convert()
    player_2_pfp = pygame.transform.scale(player_2_pfp, (96,96))
except:
    player_2_pfp = pygame.image.load("Resources\Menu\DefaultPFP.png").convert()
    player_2_pfp = pygame.transform.scale(player_2_pfp, (96,96))



#Stores info about the players: could have been put into DATA_STORAGE but I felt it would fit better as its own dictionary
PLAYER_INFO = {
    "Player1" : {
        "Cue" : "Default",
        "PFP" : player_1_pfp,
    },
    "Player2" : {
        "Cue" : "Default",
        "PFP" : player_2_pfp,
    }
}


#A list of possible random events that can happen
RANDOM_EVENTS = [
    "None", # I think that's fairly obvious
    "Black hole", # Gravitates all balls towards the white ball
    "50 caliber", # Sets cue power to 250%
    "Iced out", # Makes the table friction much lower
    "Broken table", # Makes a crack appear in the table that is also a hole
    "Locked holes", # Disables a random two or three holes
    "Blind", # Blinds the user except for a small hole to show the white ball
    "MASSive", # Pentuples the mass of the white ball
    "Hacking", # Shoots a ray in the direction the ball will go
]

#So i can import some vars from main.py into UsedClasses.py without running the entirety of the code and causing a crash
if __name__ == "__main__":


    #Calculate Delta Time (Time since last frame was rendered)
    def CalculateDeltaTime(previous_time_since_start):
        clock.tick(frame_rate)
        time_since_start = time.time()
        delta_time = time_since_start - previous_time_since_start
        return delta_time



    # Checks the mouse pos to see if a button is being hovered over and updates the states of each button accordingly
    def UpdateButtonStates(buttons):
        mouse_position = pygame.mouse.get_pos()
        for button in buttons:
            if button.BeingHoveredOver(mouse_position) and button.cs == 0:
                button.cs = 1   
            elif button.BeingHoveredOver(mouse_position) != True:
                button.cs = 0





    #Loading resources - Takes WAIR to be able to know what to render.
    def LoadResources():
        global WHAT_AM_I_RENDERING, DATA_STORAGE, PLAYER_INFO
        Buttons.ForgetAll() # Reset buttons




#Load the resources for the main menu

        if WHAT_AM_I_RENDERING == 0:#Main menu

            title_shadow = pygame.image.load("Resources\Menu\Title shadow.png").convert_alpha()
            title_shadow.set_alpha(64)
            
            #(((Button 1 top left),(Button 1 bottom right),(Button 2 top left),(Button 2 bottom right),(Button 3 top left),(Button 3 bottom right)))
            DATA_STORAGE = {
                "Buttons" : (Buttons(width_and_height=(260,96), text = "Play", centre_position = (640,320), border=10, shadow=True),
                            Buttons(width_and_height=(320,96), text = "Config", centre_position = (640,440), border=10, shadow=True),
                            Buttons(width_and_height=(570,96), text = "Customisation", centre_position = (640,560), border=10, shadow=True)),
                "User input variables" : [],
                "Game variables" : [],
                "Balls" : [],
                "Textures" : {
                    "Title" : pygame.image.load("Resources\Menu\Title.png").convert_alpha(),
                    "Title shadow" : title_shadow
                    },
                #Menu texture
                "Background image" : (pygame.image.load("Resources\Menu\Background.png").convert())
            }
            
            





#Load the resources for the menu which you get to when pressing play
        elif WHAT_AM_I_RENDERING == 1:#Play menu

            title_shadow = pygame.image.load("Resources\Menu\Title shadow.png").convert_alpha()
            title_shadow.set_alpha(64)

            DATA_STORAGE = {
                "Buttons" : (Buttons(width_and_height=(258,96), text = "Back", centre_position = (640,320), border=10, shadow=True),
                            Buttons(width_and_height=(300,96), text = "Events", centre_position = (640,440), border=10, shadow=True),
                            Buttons(width_and_height=(400,96), text = "No events", centre_position = (640,560), border=10, shadow=True)),
                "User input variables" : [],
                "Game variables" : [],
                "Balls" : [],
                "Textures" : {
                    "Title" : pygame.image.load("Resources\Menu\Title.png").convert_alpha(),
                    "Title shadow" : title_shadow
                    },
                "Background image" : (pygame.image.load("Resources\Menu\BackgroundWithTutorial.png").convert())
            }

            


#Load the resources for the main game
        elif WHAT_AM_I_RENDERING == 2 or WHAT_AM_I_RENDERING == 3:#In game (With events or without events)

            bbp = (925, 400) # bbp short for black ball position because otherwise it would be REALLY convoluted and hard to read the following list of tuples

            lock_texture = pygame.image.load("Resources\In_Game_Assets\Lock.png")
            lock_texture = pygame.transform.scale(lock_texture, (lock_texture.get_width()*5,lock_texture.get_height()*5))



            #Generate ball positions and randomise each position
            ball_pos_list = [(bbp[0]-60,bbp[1]),
                            (bbp[0]-30,bbp[1]-17.5),
                            (bbp[0]-30,bbp[1]+17.5),
                            (bbp[0],bbp[1]+35),
                            (bbp[0],bbp[1]-35),
                            (bbp[0]+60,bbp[1]),
                            (bbp[0]+30,bbp[1]-17.5),
                            (bbp[0]+30,bbp[1]+17.5),
                            (bbp[0]+30,bbp[1]-52.5),
                            (bbp[0]+30,bbp[1]+52.5),
                            (bbp[0]+60,bbp[1]-35),
                            (bbp[0]+60,bbp[1]+35),
                            (bbp[0]+60,bbp[1]-70),
                            (bbp[0]+60,bbp[1]+70)]
            random.shuffle(ball_pos_list)



            DATA_STORAGE = {

                #Button instances
                "Buttons" : (Buttons(width_and_height=(258,96), text = "Menu", centre_position = (640,320), border=10, shadow=True),
                            Buttons(width_and_height=(513,96), text = "Again", centre_position = (640,440), border=10, shadow=True)),
                
                # Vars storing information pertaining to user inputs
                "User input variables" : { # Vars to be passed between functions
                    "Mouse position" : (0,0), # Mouse position
                    "Shot made" : False, # Shot made flag
                    "Locked" : False
                },


                # Vars storing information pertaining to game logic and other things in the main loop of the game
                "Game variables" : {

                    #Stores most information about the table
                    "Table bounds" : {

                        #Table sides
                        "Bottom" : pygame.Rect((0,656),(1280,64)),

                        "Top" : pygame.Rect((0,80),(1280,64)),
                        
                        "Left": pygame.Rect((0,80),(64,640)),

                        "Right" : pygame.Rect((1216,80),(64,640)),


                        #Table holes
                        "Holes" : (pygame.Rect((626,80),(28,76)),
                                    pygame.Rect((35,115),(64,64)),
                                    pygame.Rect((1183,114),(64,64)),
                                    pygame.Rect((626,644),(28,76)),
                                    pygame.Rect((35,622),(64,64)),
                                    pygame.Rect((1182,622),(64,64)))
                        },



                    #Other game variables
                    "Shot power" : 50000,
                    "Shot power change" : 20000/frame_rate,
                    "White sunk" : False,
                    "Black sunk" : False,
                    "First collide" : None,
                    "Extend turn" : False,
                    "Player lost" : None,
                    "End game" : False,
                    "Punish for remaining turn" : False,
                    "Reward for remaining turn" : False,
                    "Tick once per shot" : False,
                    "White picked up" : False,

                    #The bound in which the white ball can be placed
                    "White bounds" : pygame.Rect((64,144),(288,512)),


                    #Stores whether each event is active
                    "Events" : {
                        "Black hole" : False,
                        "50 caliber" : False, # Sets cue power to 250%
                        "Iced out" : False, # Makes the table friction much lower
                        "Broken table" : False, # Makes a crack appear in the table that is also a hole
                        "Locked holes" : False, # Disables a random two holes
                        "Blind" : False, # Blinds the user except for a small hole to show the white ball
                        "MASSive" : False, # pentuples the mass of the ball
                        "Hacking": False # Shoots a ray out of the white ball to show where it goes
                    }
                    },


                #Stores an instance of each ball
                "Balls" : {
                    "White ball" : Balls(texture="White", position = (282.5,bbp[1]), mass= 170),
                    "Yellow Solid ball" : Balls(texture="Yellow_Solid", position = ball_pos_list.pop(), ball_type="Solid"),
                    "Blue Solid ball" : Balls(texture="Blue_Solid", position = ball_pos_list.pop(), ball_type="Solid"),
                    "Red ball" : Balls(texture="Red_Solid", position = ball_pos_list.pop(), ball_type="Solid"),
                    "Pink ball" : Balls(texture="Pink_Solid", position = ball_pos_list.pop(), ball_type="Solid"),
                    "Orange ball" : Balls(texture="Orange_Solid", position = ball_pos_list.pop(), ball_type="Solid"),
                    "Green ball" : Balls(texture="Green_Solid", position = ball_pos_list.pop(), ball_type="Solid"),
                    "Maroon ball" : Balls(texture="Maroon_Solid", position = ball_pos_list.pop(), ball_type="Solid"),
                    "Black ball" : Balls(texture="Black", position = bbp, ball_type="Black"),
                    "Yellow Stripe ball" : Balls(texture="Yellow_Stripe", position = ball_pos_list.pop(), ball_type="Stripe"),
                    "Blue Stripe ball" : Balls(texture="Blue_Stripe", position = ball_pos_list.pop(), ball_type="Stripe"),
                    "Red Stripe ball" : Balls(texture="Red_Stripe", position = ball_pos_list.pop(), ball_type="Stripe"),
                    "Pink Stripe ball" : Balls(texture="Pink_Stripe", position = ball_pos_list.pop(), ball_type="Stripe"),
                    "Orange Stripe ball" : Balls(texture="Orange_Stripe", position = ball_pos_list.pop(), ball_type="Stripe"),
                    "Green Stripe ball" : Balls(texture="Green_Stripe", position = ball_pos_list.pop(), ball_type="Stripe"),
                    "Maroon Stripe ball" : Balls(texture="Maroon_Stripe", position = ball_pos_list.pop(), ball_type="Stripe"),
                    },

                #Stores sound effects used during gameplay
                "Sounds" : {
                    "Cue" : [
                        pygame.mixer.Sound("Resources\Sounds\Cue_hit_1.wav"),
                        pygame.mixer.Sound("Resources\Sounds\Cue_hit_2.wav")
                    ],
                    "Ball" : [
                        pygame.mixer.Sound("Resources\Sounds\Ball_hit_1.wav"),
                        pygame.mixer.Sound("Resources\Sounds\Ball_hit_2.wav"),
                        pygame.mixer.Sound("Resources\Sounds\Ball_hit_3.wav"),
                        pygame.mixer.Sound("Resources\Sounds\Ball_hit_4.wav")
                    ],
                },

                #Stores other general info
                "Other" : {
                    "Ball shadow" : (pygame.image.load("Resources\In_Game_Assets\Ball_shadow.png")).convert(),
                    #The texture which is shown when the "blind" event is active
                    "Blind texture" : (pygame.image.load("Resources\In_Game_Assets\Darkness.png")).convert_alpha(),
                    "Crack texture": (pygame.image.load("Resources\In_Game_Assets\Crack.png")).convert_alpha(),
                    "Crack hitbox" : pygame.Rect((626,80),(28,720)),
                    "Lock texture" : lock_texture.convert_alpha(),
                },


                #Stores the background image
                "Background image" : pygame.image.load("Resources\In_Game_Assets\Table.png").convert()
            }



#Load the resources for the configuration menu
        elif WHAT_AM_I_RENDERING == 4:#Config menu

            title_shadow = pygame.image.load("Resources\Menu\Title shadow.png").convert_alpha()
            title_shadow.set_alpha(64)

            DATA_STORAGE = {
                "Buttons" : (
                    Buttons(width_and_height=(258,96), text = "Back", centre_position = (640,320), border=10, shadow=True),
                    Buttons(width_and_height=(513,96), text = f"Debug : {DEBUG}", centre_position = (640,440), border=10, shadow=True),
                    Buttons(width_and_height=(700,96), text = f"Sound effects : {SOUND_EFFECTS_ENABLED}", centre_position = (640,560), border=10, shadow=True),
                    ),
                "User input variables" : [],
                "Game variables" : [],
                "Balls" : [],
                "Textures" : {
                    "Title" : pygame.image.load("Resources\Menu\Title.png").convert_alpha(),
                    "Title shadow" : title_shadow
                    },
                "Background image" : (pygame.image.load("Resources\Menu\Background.png").convert())
            }

        



#Load the resources for the customisation menu
        elif WHAT_AM_I_RENDERING == 5:#Customisation menu

            title_shadow = pygame.image.load("Resources\Menu\Title shadow.png").convert_alpha()
            title_shadow.set_alpha(64)

            p1_text = PLAYER_INFO["Player1"]["Cue"]
            p2_text = PLAYER_INFO["Player2"]["Cue"]


            DATA_STORAGE = {
                "Buttons" : (
                    Buttons(width_and_height=(258,96), text = "Back", centre_position = (640,320), border=10, shadow=True),
                    Buttons(width_and_height=(900,96), text = f"P1 Cue: {p1_text}", centre_position = (640,440), border=10, shadow=True, text_size=70),
                    Buttons(width_and_height=(900,96), text = f"P2 Cue: {p2_text}", centre_position = (640,560), border=10, shadow=True, text_size=70),
                    ),
                "User input variables" : [],
                "Game variables" : [],
                "Balls" : [],
                "Textures" : {
                    "Title" : pygame.image.load("Resources\Menu\Title.png").convert_alpha(),
                    "Title shadow" : title_shadow,
                    "Cue textures" : SpriteSheet("Resources\In_Game_Assets\Cues.png"),
                    "Cue names" : ["Default", "Mahogany", "Gilded", "Crimson red", "Ocean blue", "Grass green", "Twig"]
                    },
                "Background image" : (pygame.image.load("Resources\Menu\Background.png").convert())
            }





#These will be called when a function is a bit long to just be put into the check in the main loop


#Left mouse button pressed down functions
    #Functions corresponding to the button that was pressed
    def LMBDFunctions():
        global DATA_STORAGE, WHAT_AM_I_RENDERING, IS_LOADING
        buttons = DATA_STORAGE["Buttons"]
        mouse_position = pygame.mouse.get_pos()

        #Turns the button dark while hovered over and pressed down on
        if buttons is not None:
            for button in buttons:
                if button.BeingHoveredOver(mouse_position):
                    button.cs = 2          


#Left mouse button unpressed functions
    def LMBUFunctions():
        global DATA_STORAGE, WHAT_AM_I_RENDERING, IS_LOADING, DEBUG, SOUND_EFFECTS_ENABLED
        buttons = DATA_STORAGE["Buttons"]
        mouse_position = pygame.mouse.get_pos()



        #Main menu buttons 
        if WHAT_AM_I_RENDERING == 0:
            for button in buttons:
                if button.BeingHoveredOver(mouse_position):
                    #Play button
                    if button.id == 0:
                        WHAT_AM_I_RENDERING = 1
                        IS_LOADING = True
                    #Config button
                    elif button.id == 1:
                        WHAT_AM_I_RENDERING = 4
                        IS_LOADING = True
                    #Customisation button
                    elif button.id == 2:
                        WHAT_AM_I_RENDERING = 5
                        IS_LOADING = True
        



        #Play menu buttons
        elif WHAT_AM_I_RENDERING == 1:
            buttons = DATA_STORAGE["Buttons"]
            for button in buttons:
                if button.BeingHoveredOver(mouse_position):
                    #Back button
                    if button.id == 0:
                        WHAT_AM_I_RENDERING = 0
                        IS_LOADING = True
                    #Events button
                    elif button.id == 1:
                        WHAT_AM_I_RENDERING = 2
                        IS_LOADING = True
                    #No events button
                    elif button.id == 2:
                        WHAT_AM_I_RENDERING = 3
                        IS_LOADING = True




        #Configuration menu buttons
        elif WHAT_AM_I_RENDERING == 4:
            buttons = DATA_STORAGE["Buttons"]
            for button in buttons:
                if button.BeingHoveredOver(mouse_position):
                    #Back button
                    if button.id == 0:
                        WHAT_AM_I_RENDERING = 0
                        IS_LOADING = True

                    #Debug button
                    elif button.id == 1:

                        #Changes the state of debug
                        DEBUG = not DEBUG
                        button.text = f"Debug : {DEBUG}"
                        button.BakeTextRenderInfo()
                        button.BakeButtonRenderInfo()

                    #SFX enable/disable
                    elif button.id == 2:

                        #Changes the state of DATA_STORAGE["Sounds"]["Enabled"]
                        SOUND_EFFECTS_ENABLED = not SOUND_EFFECTS_ENABLED
                        button.text = f"Sound effects: {SOUND_EFFECTS_ENABLED}"
                        button.BakeTextRenderInfo()
                        button.BakeButtonRenderInfo()




        #Customisation menu buttons
        elif WHAT_AM_I_RENDERING == 5:
            buttons = DATA_STORAGE["Buttons"]
            for button in buttons:
                if button.BeingHoveredOver(mouse_position):
                    #Back button
                    if button.id == 0:
                        WHAT_AM_I_RENDERING = 0
                        IS_LOADING = True



                    #P1 change cue button
                    elif button.id == 1:

                        #Scrolls through the different cues and equips them for player 1
                        selected_cue = DATA_STORAGE["Textures"]["Cue names"].index(PLAYER_INFO["Player1"]["Cue"])
                        selected_cue += 1
                        try:
                            DATA_STORAGE["Textures"]["Cue names"][selected_cue]
                        except:
                            PLAYER_INFO["Player1"]["Cue"] = DATA_STORAGE["Textures"]["Cue names"][0]
                        else:
                            PLAYER_INFO["Player1"]["Cue"] = DATA_STORAGE["Textures"]["Cue names"][selected_cue]


                        #Changes the text on the button
                        p1_text = PLAYER_INFO["Player1"]["Cue"]
                        button.text = f"P1 Cue: {p1_text}"
                        button.BakeTextRenderInfo()
                        button.BakeButtonRenderInfo()


                    #P2 change cue button
                    elif button.id == 2:


                        #Scrolls through the different cues and equips them for player 1
                        selected_cue = DATA_STORAGE["Textures"]["Cue names"].index(PLAYER_INFO["Player2"]["Cue"])
                        selected_cue += 1
                        try:
                            DATA_STORAGE["Textures"]["Cue names"][selected_cue]
                        except:
                            PLAYER_INFO["Player2"]["Cue"] = DATA_STORAGE["Textures"]["Cue names"][0]
                        else:
                            PLAYER_INFO["Player2"]["Cue"] = DATA_STORAGE["Textures"]["Cue names"][selected_cue]


                        #Changes the text on the button
                        p2_text = PLAYER_INFO["Player2"]["Cue"]
                        button.text = f"P2 Cue: {p2_text}"
                        button.BakeTextRenderInfo()
                        button.BakeButtonRenderInfo()




        #When the game is being played
        elif WHAT_AM_I_RENDERING == 2 or WHAT_AM_I_RENDERING == 3:


            #Allow a shot to be taken if no balls are moving
            if not DATA_STORAGE["User input variables"]["Locked"] and not DATA_STORAGE["Game variables"]["White picked up"]:
                DATA_STORAGE["User input variables"]["Mouse position"] = mouse_position # Update mouse position on release
                DATA_STORAGE["User input variables"]["Shot made"] = True # Raise the shot made flag

    #Main Menu screen
    def MainMenuRender():
        global WHAT_AM_I_RENDERING, IS_LOADING, LOADING_SCREEN
        buttons = DATA_STORAGE["Buttons"]
        background_image_texture = DATA_STORAGE["Background image"]
        title = DATA_STORAGE["Textures"]["Title"]
        title_shadow = DATA_STORAGE["Textures"]["Title shadow"]
        fade_black = Fade(time_in_seconds= 0.5,fade_in=True, tween= "quadratic_in", frame_rate= frame_rate)
        if MOUSE_POINTER:
            mouse_pointer = pygame.image.load("Resources\Cursors\Mouse_Cursor.png").convert_alpha()
            mouse_pointer = pygame.transform.scale_by(mouse_pointer, 3.0)
        

        frame_counter = 0
        add_per_frame = 2/frame_rate
        current_rotation = 0
        title_pos = (640, 150)

        while len(fade_black) > 0:
            title = DATA_STORAGE["Textures"]["Title"]
            title_shadow = DATA_STORAGE["Textures"]["Title shadow"]
            if WIGGLE_TITLE:
                title_shadow = pygame.transform.rotate(title_shadow, current_rotation - 5.76)
                title = pygame.transform.rotate(title, current_rotation - 5.76)
            current_rotation += sin(frame_counter)/25
            frame_counter += add_per_frame
            if DEBUG:
                print(current_rotation)

            screen.blit(background_image_texture, (0,0))
            screen.blit(title_shadow, (title_pos[0] - title_shadow.get_width()/2 + 3,title_pos[1] - title_shadow.get_height()/2 + 3))
            screen.blit(title, (title_pos[0] - title.get_width()/2,title_pos[1] - title.get_height()/2))
            for button in buttons:
                button.Render(screen)

            LOADING_SCREEN.set_alpha(fade_black.pop())                
            screen.blit(LOADING_SCREEN,(0,0))
            #Update the display
            pygame.display.update()
            clock.tick(frame_rate)
        
        while WHAT_AM_I_RENDERING == 0:

            title = DATA_STORAGE["Textures"]["Title"]
            title_shadow = DATA_STORAGE["Textures"]["Title shadow"]
            if WIGGLE_TITLE:
                title_shadow = pygame.transform.rotate(title_shadow, current_rotation - 5.76)
                title = pygame.transform.rotate(title, current_rotation - 5.76)
            current_rotation += sin(frame_counter)/25
            frame_counter += add_per_frame
            if DEBUG:
                print(current_rotation)

            clock.tick(frame_rate)
            UpdateButtonStates(buttons)

            #Look at what keys are pressed
            for event in pygame.event.get(pump = True):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    LMBDFunctions()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    LMBUFunctions()
            
            if IS_LOADING is True:
                fade_black = Fade(time_in_seconds= 0.5,fade_in=False, tween= "quadratic_in", frame_rate= frame_rate)

                screengrab = screen.copy()

                while len(fade_black) > 0:
                
                    screen.blit(screengrab, (0,0))

                    LOADING_SCREEN.set_alpha(fade_black.pop())                
                    screen.blit(LOADING_SCREEN,(0,0))
                    #Update the display
                    pygame.display.update()
                    clock.tick(frame_rate)
                IS_LOADING = False
            else:
                screen.blit(background_image_texture, (0,0))
                for button in buttons:
                    button.Render(screen)
                screen.blit(title_shadow, (title_pos[0] - title_shadow.get_width()/2 + 3,title_pos[1] - title_shadow.get_height()/2 + 3))
                screen.blit(title, (title_pos[0] - title.get_width()/2,title_pos[1] - title.get_height()/2))

                if MOUSE_POINTER:
                    screen.blit(mouse_pointer, pygame.mouse.get_pos())
                
                #Update the display
                pygame.display.update()
            

    def PlayMenuRender():
        global WHAT_AM_I_RENDERING, IS_LOADING, LOADING_SCREEN
        buttons = DATA_STORAGE["Buttons"]
        background_image_texture = DATA_STORAGE["Background image"]
        fade_black = Fade(time_in_seconds= 0.5,fade_in=True, tween= "quadratic_in", frame_rate= frame_rate)
        if MOUSE_POINTER:
            mouse_pointer = pygame.image.load("Resources\Cursors\Mouse_Cursor.png").convert_alpha()
            mouse_pointer = pygame.transform.scale_by(mouse_pointer, 3.0)

        frame_counter = 0
        add_per_frame = 2/frame_rate
        current_rotation = 0
        title_pos = (640, 150)
        
        
        while len(fade_black) > 0:

            title = DATA_STORAGE["Textures"]["Title"]
            title_shadow = DATA_STORAGE["Textures"]["Title shadow"]
            if WIGGLE_TITLE:
                title_shadow = pygame.transform.rotate(title_shadow, current_rotation - 5.76)
                title = pygame.transform.rotate(title, current_rotation - 5.76)
            current_rotation += sin(frame_counter)/25
            frame_counter += add_per_frame

            if DEBUG:
                print(current_rotation)
                
            screen.blit(background_image_texture, (0,0))
            for button in buttons:
                button.Render(screen)
            screen.blit(title_shadow, (title_pos[0] - title_shadow.get_width()/2 + 3,title_pos[1] - title_shadow.get_height()/2 + 3))
            screen.blit(title, (title_pos[0] - title.get_width()/2,title_pos[1] - title.get_height()/2))
            

            LOADING_SCREEN.set_alpha(fade_black.pop())                
            screen.blit(LOADING_SCREEN,(0,0))
            #Update the display
            pygame.display.update()
            clock.tick(frame_rate)
        

        while WHAT_AM_I_RENDERING == 1:

            title = DATA_STORAGE["Textures"]["Title"]
            title_shadow = DATA_STORAGE["Textures"]["Title shadow"]
            if WIGGLE_TITLE:
                title_shadow = pygame.transform.rotate(title_shadow, current_rotation - 5.76)
                title = pygame.transform.rotate(title, current_rotation - 5.76)
            current_rotation += sin(frame_counter)/25
            frame_counter += add_per_frame

            clock.tick(frame_rate)
            UpdateButtonStates(buttons)
            

            #Look at what keys are pressed
            for event in pygame.event.get(pump = True):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    LMBDFunctions()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    LMBUFunctions()
            
            if IS_LOADING is True:
                fade_black = Fade(time_in_seconds= 0.5,fade_in=False, tween= "quadratic_in", frame_rate= frame_rate)

                screengrab = screen.copy()

                while len(fade_black) > 0:
                
                    screen.blit(screengrab, (0,0))

                    LOADING_SCREEN.set_alpha(fade_black.pop())                
                    screen.blit(LOADING_SCREEN,(0,0))
                    #Update the display
                    pygame.display.update()
                    clock.tick(frame_rate)
                IS_LOADING = False
            else:
                screen.blit(background_image_texture, (0,0))
                for button in buttons:
                    button.Render(screen)
                screen.blit(title_shadow, (title_pos[0] - title_shadow.get_width()/2 + 3,title_pos[1] - title_shadow.get_height()/2 + 3))
                screen.blit(title, (title_pos[0] - title.get_width()/2,title_pos[1] - title.get_height()/2))

                if MOUSE_POINTER:
                    screen.blit(mouse_pointer, pygame.mouse.get_pos())

                #Update the display
                pygame.display.update()


    #------------------------------------------------------------------------------------------------------------
    def ConfigMenuRender():
        global WHAT_AM_I_RENDERING, IS_LOADING, LOADING_SCREEN
        buttons = DATA_STORAGE["Buttons"]
        background_image_texture = DATA_STORAGE["Background image"]
        fade_black = Fade(time_in_seconds= 0.5,fade_in=True, tween= "quadratic_in", frame_rate= frame_rate)
        if MOUSE_POINTER:
            mouse_pointer = pygame.image.load("Resources\Cursors\Mouse_Cursor.png").convert_alpha()
            mouse_pointer = pygame.transform.scale_by(mouse_pointer, 3.0)

        frame_counter = 0
        add_per_frame = 2/frame_rate
        current_rotation = 0
        title_pos = (640, 150)
        
        
        while len(fade_black) > 0:

            title = DATA_STORAGE["Textures"]["Title"]
            title_shadow = DATA_STORAGE["Textures"]["Title shadow"]
            if WIGGLE_TITLE:
                title_shadow = pygame.transform.rotate(title_shadow, current_rotation - 5.76)
                title = pygame.transform.rotate(title, current_rotation - 5.76)
            current_rotation += sin(frame_counter)/25
            frame_counter += add_per_frame

            if DEBUG:
                print(current_rotation)
                
            screen.blit(background_image_texture, (0,0))
            for button in buttons:
                button.Render(screen)
            screen.blit(title_shadow, (title_pos[0] - title_shadow.get_width()/2 + 3,title_pos[1] - title_shadow.get_height()/2 + 3))
            screen.blit(title, (title_pos[0] - title.get_width()/2,title_pos[1] - title.get_height()/2))
            

            LOADING_SCREEN.set_alpha(fade_black.pop())                
            screen.blit(LOADING_SCREEN,(0,0))
            #Update the display
            pygame.display.update()
            clock.tick(frame_rate)
        

        while WHAT_AM_I_RENDERING == 4:

            title = DATA_STORAGE["Textures"]["Title"]
            title_shadow = DATA_STORAGE["Textures"]["Title shadow"]
            if WIGGLE_TITLE:
                title_shadow = pygame.transform.rotate(title_shadow, current_rotation - 5.76)
                title = pygame.transform.rotate(title, current_rotation - 5.76)
            current_rotation += sin(frame_counter)/25
            frame_counter += add_per_frame

            clock.tick(frame_rate)
            UpdateButtonStates(buttons)
            
            
            #Look at what keys are pressed
            for event in pygame.event.get(pump = True):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    LMBDFunctions()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    LMBUFunctions()
            
            if IS_LOADING is True:
                fade_black = Fade(time_in_seconds= 0.5,fade_in=False, tween= "quadratic_in", frame_rate= frame_rate)

                screengrab = screen.copy()

                while len(fade_black) > 0:
                
                    screen.blit(screengrab, (0,0))

                    LOADING_SCREEN.set_alpha(fade_black.pop())                
                    screen.blit(LOADING_SCREEN,(0,0))
                    #Update the display
                    pygame.display.update()
                    clock.tick(frame_rate)
                IS_LOADING = False
            else:
                screen.blit(background_image_texture, (0,0))
                for button in buttons:
                    button.Render(screen)
                screen.blit(title_shadow, (title_pos[0] - title_shadow.get_width()/2 + 3,title_pos[1] - title_shadow.get_height()/2 + 3))
                screen.blit(title, (title_pos[0] - title.get_width()/2,title_pos[1] - title.get_height()/2))

                if MOUSE_POINTER:
                    screen.blit(mouse_pointer, pygame.mouse.get_pos())

                #Update the display
                pygame.display.update()

    #---------------------------------------------------------------------------------------------------------

    def CustomisationMenuRender():
        global WHAT_AM_I_RENDERING, IS_LOADING, LOADING_SCREEN
        buttons = DATA_STORAGE["Buttons"]
        background_image_texture = DATA_STORAGE["Background image"]
        fade_black = Fade(time_in_seconds= 0.5,fade_in=True, tween= "quadratic_in", frame_rate= frame_rate)
        if MOUSE_POINTER:
            mouse_pointer = pygame.image.load("Resources\Cursors\Mouse_Cursor.png").convert_alpha()
            mouse_pointer = pygame.transform.scale_by(mouse_pointer, 3.0)


        #Title 'wiggle'
        frame_counter = 0
        add_per_frame = 2/frame_rate
        current_rotation = 0
        title_pos = (640, 150)



        #Cue pullout animation variables
        degrees_to_rotate_cue = 30
        seconds_of_rotation = 0.75

        #Getting textures ready
        previous_cue_1 = PLAYER_INFO["Player1"]["Cue"]
        previous_cue_2 = PLAYER_INFO["Player2"]["Cue"]
        cue_p1 = DATA_STORAGE["Textures"]["Cue textures"].ReturnSpriteAndData("Cues",PLAYER_INFO["Player1"]["Cue"] + ".png")
        cue_p1 = pygame.transform.scale_by(cue_p1, 3)
        cue_p1 = pygame.transform.rotate(cue_p1, 270)
        cue_p1_time = degrees_to_rotate_cue
        cue_p2 = DATA_STORAGE["Textures"]["Cue textures"].ReturnSpriteAndData("Cues",PLAYER_INFO["Player2"]["Cue"] + ".png")
        cue_p2 = pygame.transform.scale_by(cue_p2, 3)
        cue_p2 = pygame.transform.rotate(cue_p2, 90)
        cue_p2_time = degrees_to_rotate_cue
        time_modifier = degrees_to_rotate_cue/frame_rate/seconds_of_rotation

        cue_p1_location = (270,280)
        cue_p2_location = (1010,280)

        

        #load profile pictures
        player_1_pfp = pygame.transform.scale2x(PLAYER_INFO["Player1"]["PFP"])
        player_2_pfp = pygame.transform.scale2x(PLAYER_INFO["Player2"]["PFP"])
        
        
        #Loading into customisation menu
        while len(fade_black) > 0:

            title = DATA_STORAGE["Textures"]["Title"]
            title_shadow = DATA_STORAGE["Textures"]["Title shadow"]
            if WIGGLE_TITLE:
                title_shadow = pygame.transform.rotate(title_shadow, current_rotation - 5.76)
                title = pygame.transform.rotate(title, current_rotation - 5.76)
            current_rotation += sin(frame_counter)/25
            frame_counter += add_per_frame

            if DEBUG:
                print(current_rotation)
                
            screen.blit(background_image_texture, (0,0))
            for button in buttons:
                button.Render(screen)
            screen.blit(title_shadow, (title_pos[0] - title_shadow.get_width()/2 + 3,title_pos[1] - title_shadow.get_height()/2 + 3))
            screen.blit(title, (title_pos[0] - title.get_width()/2,title_pos[1] - title.get_height()/2))
            screen.blit(player_1_pfp, (100, 100))
            screen.blit(player_2_pfp, (988, 100))
            screen.blit(cue_p1, (cue_p1_location[0] - cue_p1.get_width()/2, cue_p1_location[1] - cue_p1.get_height()/2))
            screen.blit(cue_p2, (cue_p2_location[0] - cue_p2.get_width()/2, cue_p2_location[1] - cue_p2.get_height()/2))

            

            LOADING_SCREEN.set_alpha(fade_black.pop())                
            screen.blit(LOADING_SCREEN,(0,0))

            #Update the display
            pygame.display.update()
            clock.tick(frame_rate)
        

        #after loading into customisation menu
        while WHAT_AM_I_RENDERING == 5:


            # title wiggle
            title = DATA_STORAGE["Textures"]["Title"]
            title_shadow = DATA_STORAGE["Textures"]["Title shadow"]
            if WIGGLE_TITLE:
                title_shadow = pygame.transform.rotate(title_shadow, current_rotation - 5.76)
                title = pygame.transform.rotate(title, current_rotation - 5.76)
            current_rotation += sin(frame_counter)/25
            frame_counter += add_per_frame

            
            #checking if the cue equipped has changed since the last frame
            if previous_cue_1 != PLAYER_INFO["Player1"]["Cue"]:
                cue_p1 = DATA_STORAGE["Textures"]["Cue textures"].ReturnSpriteAndData("Cues",PLAYER_INFO["Player1"]["Cue"] + ".png")
                cue_p1 = pygame.transform.scale_by(cue_p1, 3)
                cue_p1 = pygame.transform.rotate(cue_p1, 270)
                previous_cue_1 = PLAYER_INFO["Player1"]["Cue"]
                cue_p1_time = degrees_to_rotate_cue
            if previous_cue_2 != PLAYER_INFO["Player2"]["Cue"]:
                cue_p2 = DATA_STORAGE["Textures"]["Cue textures"].ReturnSpriteAndData("Cues",PLAYER_INFO["Player2"]["Cue"] + ".png")
                cue_p2 = pygame.transform.scale_by(cue_p2, 3)
                cue_p2 = pygame.transform.rotate(cue_p2, 90)
                previous_cue_2 = PLAYER_INFO["Player2"]["Cue"]
                cue_p2_time = degrees_to_rotate_cue

            clock.tick(frame_rate)
            UpdateButtonStates(buttons)
            
            
            #Look at what keys are pressed
            for event in pygame.event.get(pump = True):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    LMBDFunctions()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    LMBUFunctions()
            


            #Loading out of the customisation screen
            if IS_LOADING is True:
                fade_black = Fade(time_in_seconds= 0.5,fade_in=False, tween= "quadratic_in", frame_rate= frame_rate)

                screengrab = screen.copy()

                while len(fade_black) > 0:
                
                    screen.blit(screengrab, (0,0))

                    LOADING_SCREEN.set_alpha(fade_black.pop())                
                    screen.blit(LOADING_SCREEN,(0,0))
                    #Update the display
                    pygame.display.update()
                    clock.tick(frame_rate)
                IS_LOADING = False

            
            
            #Running the customisation screen
            else:

                #static parts
                screen.blit(background_image_texture, (0,0))
                for button in buttons:
                    button.Render(screen)
                screen.blit(title_shadow, (title_pos[0] - title_shadow.get_width()/2 + 3,title_pos[1] - title_shadow.get_height()/2 + 3))
                screen.blit(title, (title_pos[0] - title.get_width()/2,title_pos[1] - title.get_height()/2))
                screen.blit(player_1_pfp, (100, 100))
                screen.blit(player_2_pfp, (988, 100))


                #Cue pullout animation
                if cue_p1_time > 0:
                    cue_p1_time -= time_modifier
                    cue_p1_rotated = pygame.transform.rotate(cue_p1, degrees_to_rotate_cue - (cue_p1_time**2)/degrees_to_rotate_cue)
                if cue_p2_time > 0:
                    cue_p2_time -= time_modifier
                    cue_p2_rotated = pygame.transform.rotate(cue_p2, (cue_p2_time**2)/degrees_to_rotate_cue - degrees_to_rotate_cue)

                screen.blit(cue_p1_rotated, (cue_p1_location[0] - (cue_p1_rotated.get_width()/2),cue_p1_location[1] - (cue_p1_rotated.get_height()/2)))
                screen.blit(cue_p2_rotated, (cue_p2_location[0] - (cue_p2_rotated.get_width()/2),cue_p2_location[1] - (cue_p2_rotated.get_height()/2)))


                #fancy custom mouse pointer
                if MOUSE_POINTER:
                    screen.blit(mouse_pointer, pygame.mouse.get_pos())

                #Update the display
                pygame.display.update()
    #---------------------------------------------------------------------------------------------------------

    # i MAY just be the indentation meister 

    def CalculateCollidingBalls(balls):
        balls_to_collide = []
        for ball in balls:
            if balls[ball].enabled:
                for colliding_ball in balls:
                    if balls[colliding_ball].enabled: # Ever so slightly faster to do it this way (ugly i know)
                        if ball != colliding_ball:
                            if balls[ball].collision_rect.colliderect(balls[colliding_ball].collision_rect):
                                distance = (balls[ball].position[0] - balls[colliding_ball].position[0])**2 + (balls[ball].position[1] - balls[colliding_ball].position[1])**2
                                # dist * 1.05 for tolerance
                                if (balls[ball].size + balls[colliding_ball].size)**2 > distance*1.05 and (colliding_ball, ball) not in balls_to_collide:
                                    balls_to_collide.append((ball,colliding_ball))
        return balls_to_collide


    def CalculateCueAngle(mouse_pos, ball_centre):
        vector = []
        for index in range(0,2):
            vector.append(mouse_pos[index] - ball_centre[index])
        if vector[1] < 0: # If vector y is less than zero:
            vector[1] *= -1


            if vector[0] > 0: # If vector x is more than zero:
                return degrees(atan(vector[0]/vector[1]))
            

            elif vector[0] < 0: # If vector x is less than zero:
                vector[0] *= -1
                return 360 - degrees(atan(vector[0]/vector[1]))
            

            else: # Vector X is equal to zero
                return 0



        elif vector[1] > 0: # If vector y is more than zero:
            vector[1] *= -1


            if vector[0] > 0: # If vector x is more than zero:
                return 180 + degrees(atan(vector[0]/vector[1]))
            

            elif vector[0] < 0: # If vector x is less than zero:
                return 180 + degrees(atan(vector[0]/vector[1]))
            

            else: # Vector X is equal to zero
                return 180
            

        else: # Vector Y is equal to zero
            
            
            if vector[0] < 0:
                return 270
            

            elif vector[0] >= 0:
                return 90




    def CalculateCollisionRebound(ball, colliding_ball):

        # Retrieved from https://scipython.com/blog/two-dimensional-collisions/ 10th march 2025

        mass_total = ball.mass + colliding_ball.mass

        ball_mass_ratio = 2 * colliding_ball.mass / mass_total
        colliding_ball_mass_ratio = 2 * ball.mass / mass_total
        d = np.linalg.norm(ball.size - colliding_ball.size)**2
        ball_velocity, colliding_ball_velocity = np.array(ball.velocity), np.array(colliding_ball.velocity)
        ball_centre = np.array(ball.position) + np.array(ball.size)
        colliding_ball_centre = np.array(colliding_ball.position) + np.array(colliding_ball.size)

        d = np.linalg.norm(ball_centre - colliding_ball_centre)**2

        ball_dot_over_abs = np.dot((ball_velocity - colliding_ball_velocity), (ball_centre - colliding_ball_centre)) / d
        colliding_ball_dot_over_abs = np.dot((colliding_ball_velocity - ball_velocity), (colliding_ball_centre - ball_centre)) / d
        new_ball_velocity = ball_velocity - ball_mass_ratio * ball_dot_over_abs * (ball_centre - colliding_ball_centre)
        new_colliding_ball_velocity = colliding_ball_velocity - colliding_ball_mass_ratio * colliding_ball_dot_over_abs * (colliding_ball_centre - ball_centre)
        
        if DEBUG:
            print(ball_velocity, ball_mass_ratio, ball_dot_over_abs, (colliding_ball_centre - ball_centre), ball_dot_over_abs)
            print(colliding_ball_velocity, colliding_ball_mass_ratio, (ball_centre - colliding_ball_centre), colliding_ball_dot_over_abs)
            print(new_ball_velocity, new_colliding_ball_velocity)

        return new_ball_velocity, new_colliding_ball_velocity





    def CalculateCuePosFromAngle(player, ball, shot_power, fifty_caliber_enabled):
        if not fifty_caliber_enabled:
            ball_centre = np.array([ball.position[0] + ball.size, ball.position[1] + ball.size])
            mouse_pos = np.array(pygame.mouse.get_pos())
            cue_vector = ball_centre - mouse_pos
            cue_angle = 360 - CalculateCueAngle(mouse_pos, ball_centre) #Does trig to find angle
            cue = player.ReturnRotatedCue(cue_angle)
            cue_width_height = np.array([cue.get_width(), cue.get_height()])
            cue_vector_magnitude = np.linalg.norm(cue_vector)
            cue_vector = cue_vector/cue_vector_magnitude * shot_power/125
            cue_pos = ball_centre + 0.25*cue_vector - cue_width_height/2 + np.array([210*sin(np.radians(cue_angle)), 210*cos(np.radians(cue_angle))])
        else:
            ball_centre = np.array([ball.position[0] + ball.size, ball.position[1] + ball.size])
            mouse_pos = np.array(pygame.mouse.get_pos())
            cue_vector = ball_centre - mouse_pos
            cue_angle = 360 - CalculateCueAngle(mouse_pos, ball_centre) #Does trig to find angle
            cue = player.ReturnRotatedBFG(cue_angle)
            cue_width_height = np.array([cue.get_width(), cue.get_height()])
            cue_vector_magnitude = np.linalg.norm(cue_vector)
            cue_vector = cue_vector/cue_vector_magnitude
            cue_pos = ball_centre + cue_vector*20 - cue_width_height/2 + np.array([210*sin(np.radians(cue_angle)), 210*cos(np.radians(cue_angle))])
        return cue, cue_pos
        




    def ReturnRandomEvent():
        global RANDOM_EVENTS
        return RANDOM_EVENTS[random.randint(0,len(RANDOM_EVENTS) - 1)]


    #---------------------------------------------------------------------------------------------------
    def GameRender(random_events):
        #General setup
        global WHAT_AM_I_RENDERING, IS_LOADING, LOADING_SCREEN
        background_image_texture = DATA_STORAGE["Background image"]
        balls = DATA_STORAGE["Balls"]
        table_bounds = DATA_STORAGE["Game variables"]["Table bounds"]
        fade_black = Fade(time_in_seconds= 0.5,fade_in=True, tween= "quadratic_in", frame_rate= frame_rate)
        DATA_STORAGE["Other"]["Blind texture"] = pygame.transform.scale2x(DATA_STORAGE["Other"]["Blind texture"])

        #Setting up power vars
        shot_power = DATA_STORAGE["Game variables"]["Shot power"]
        power_change_value = DATA_STORAGE["Game variables"]["Shot power change"]

        #Sounds
        cue_sounds = DATA_STORAGE["Sounds"]["Cue"]
        ball_sounds = DATA_STORAGE["Sounds"]["Ball"]

        #Setting up mouse textures
        if MOUSE_POINTER:
            previous_500ms_cycle = 0
            mouse_pointer = [
                pygame.image.load("Resources\Cursors\Mouse_Cursor.png").convert_alpha(),
                pygame.image.load("Resources\Cursors\Mouse_Cursor_Power.png").convert_alpha(),
                pygame.image.load("Resources\Cursors\Mouse_Cursor_Power_1.png").convert_alpha(),
                pygame.image.load("Resources\Cursors\Mouse_Cursor_Power_2.png").convert_alpha(),
                pygame.image.load("Resources\Cursors\Mouse_Cursor_Power_3.png").convert_alpha(),
                pygame.image.load("Resources\Cursors\Mouse_Cursor_Power_4.png").convert_alpha(),
                pygame.image.load("Resources\Cursors\Mouse_Cursor_Power_5.png").convert_alpha(),
                pygame.image.load("Resources\Cursors\Mouse_Cursor_Power_6.png").convert_alpha(),
                pygame.image.load("Resources\Cursors\Mouse_Cursor_PowerMAX.png").convert_alpha()
                ]
            for pos in range(0,len(mouse_pointer)):
                mouse_pointer[pos] = pygame.transform.scale_by(mouse_pointer[pos],3.0)

        #Adjust volume
        for sound in cue_sounds:
            sound.set_volume(0.5)
        for sound in ball_sounds:
            sound.set_volume(0.5)
        
        #Keys for adjusting power 
        key_held_time = 0

        #Stores which holes will be locked
        holes_to_lock = []
        
        #Stores the number of shots taken
        number_of_shots_taken = 0



        #Used for FPS
        if DEBUG:
            frame_list = []



        current_players_turn = 1


        #Set up players
        player1 = Player(1, cue_name=PLAYER_INFO["Player1"]["Cue"], pfp=PLAYER_INFO["Player1"]["PFP"])
        player2 = Player(2, cue_name=PLAYER_INFO["Player2"]["Cue"], pfp=PLAYER_INFO["Player2"]["PFP"])




        #LOADING IN
        #Loading screens
        while len(fade_black) > 0:
                
            screen.blit(background_image_texture, (0,0))
            LOADING_SCREEN.set_alpha(fade_black.pop()) 
            for ball in balls:
                balls[ball].Render(screen)              
            screen.blit(LOADING_SCREEN,(0,0))
            #Update the display
            pygame.display.update()
            previous_time_since_start = time.time()
            clock.tick(frame_rate)






        #IN GAME
        #Repeat until a player loses  
        while WHAT_AM_I_RENDERING in (2,3) and not DATA_STORAGE["Game variables"]["End game"]:


            if DEBUG:
                previous_frame_time = time.time()

            #Will be used to have a stable speed between frames
            delta_time = CalculateDeltaTime(previous_time_since_start)
            previous_time_since_start = time.time()
            





            # Key presses

            keys_pressed_down = pygame.key.get_pressed()
            
            #Look at what keys states have changed, IE just been pressed but only just now
            for event in pygame.event.get(pump = True):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    LMBDFunctions()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    LMBUFunctions()




                    #Putting down the white ball
                    if DATA_STORAGE["Game variables"]["White picked up"] and not DATA_STORAGE["User input variables"]["Locked"]:
                        allow_put_down = True
                        
                        for ball in balls:
                            if ball != "White ball":
                                if balls[ball].collision_rect.colliderect(balls["White ball"].collision_rect):
                                    allow_put_down = False
                        for hole in table_bounds["Holes"]:
                            if balls["White ball"].collision_rect.colliderect(hole):
                                allow_put_down = False
                        if allow_put_down:
                            balls["White ball"].picked_up = False
                            DATA_STORAGE["Game variables"]["White picked up"] = False
                


                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    if DEBUG:
                        for ball in balls:
                            balls[ball].velocity = np.array([random.randint(-2000,2000),random.randint(-2000,2000)])
                elif event.type == pygame.KEYDOWN:
                    if DEBUG:
                        if event.key == pygame.K_SPACE:
                            for ball in balls:
                                balls[ball].velocity = np.array([0,0])
                                balls[ball].position = (random.randint(300,1000),random.randint(100,600))
                


                #For moving the white ball while it is picked up
                elif event.type == pygame.MOUSEMOTION:
                    if DATA_STORAGE["Game variables"]["White picked up"] and not DATA_STORAGE["User input variables"]["Locked"]:
                        if DEBUG:
                            print(np.array(pygame.mouse.get_pos()) + (balls["White ball"].size/2))
                        balls["White ball"].collision_rect.topleft = np.array(pygame.mouse.get_pos()) - balls["White ball"].size
                        balls["White ball"].collision_rect = balls["White ball"].collision_rect.clamp(DATA_STORAGE["Game variables"]["White bounds"])
                        balls["White ball"].position = balls["White ball"].collision_rect.topleft
                        balls["White ball"].enabled = False
                        if DEBUG:
                            print(balls["White ball"].position)


                # Lets the user scroll to change their power
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        shot_power += 5000 - (shot_power%5000) # Using MOD to set the power to increments of 5%
                    elif event.y < 0:
                        shot_power -= 5000 + (shot_power%5000)


            #Checking which keys are pressed down and held

            #Shot power
            #force shot power to be 250% if 50 caliber event is active
            if DATA_STORAGE["Game variables"]["Events"]["50 caliber"]:
                shot_power = 250000


            #Adjusting power with arrow keys or W/S
            else:
                if keys_pressed_down[pygame.K_UP] or keys_pressed_down[pygame.K_w]:

                    shot_power += power_change_value * (key_held_time/5)**2/frame_rate + 0.3 # Make the increase in power grow exponentially

                    key_held_time += 1
                    if DEBUG:
                        print(f"increased value of shot_power to: {shot_power}")


                elif keys_pressed_down[pygame.K_DOWN] or keys_pressed_down[pygame.K_s]:

                    shot_power -= power_change_value * (key_held_time/5)**2/frame_rate + 0.3 # Make the decrease in power grow exponentially

                    key_held_time += 1
                    if DEBUG:
                        print(f"decreased value of shot_power to: {shot_power}")
                
                
                #Cap the max power at 100,000 or 100% and minumum to 10, or 0.1%
                else:
                    key_held_time = 0
                if shot_power > 100000:
                    shot_power = 100000
                if shot_power < 10:
                    shot_power = 10

            
            #Background
            screen.blit(background_image_texture, (0,0))


            

            for ball in balls:
                balls[ball].collision_rect = pygame.Rect((balls[ball].position[0],balls[ball].position[1]),(balls[ball].size * 2,balls[ball].size * 2))
            
            
            
            # Before any collision calcs are done, find out which balls are colliding
            balls_to_collide = CalculateCollidingBalls(balls)


            # Loop over balls and check if any are touching a hole

            if DATA_STORAGE["Game variables"]["Events"]["Locked holes"]:
                if DATA_STORAGE["Game variables"]["Tick once per shot"]:
                    DATA_STORAGE["Game variables"]["Tick once per shot"] = False
                    for num_of_locks in range(0, random.randint(2,3)):
                        to_append = random.randint(1,6)
                        while to_append in holes_to_lock:
                            to_append = random.randint(1,6)
                        holes_to_lock.append(to_append)
                if DEBUG:
                    print(holes_to_lock)



            #Check what balls have been potted
            for ball in balls:
                iteration_variable = 0
                for hole in table_bounds["Holes"]:
                    iteration_variable += 1
                    if iteration_variable not in holes_to_lock:
                        if DEBUG:
                            pygame.draw.rect(screen, "red", hole)
                        if balls[ball].collision_rect.colliderect(hole) and not balls[ball].picked_up:
                            balls[ball].is_falling = True
                            if ball == "White ball":
                                if balls[ball].enabled:
                                    balls[ball].fallen_before = False
                                DATA_STORAGE["Game variables"]["White picked up"] = True

                                DATA_STORAGE["Game variables"]["White sunk"] = True
                                DATA_STORAGE["Game variables"]["Punish for remaining turn"] = True



                            #Determine if a player has won or lost after 8 ball has been potted
                            elif ball == "Black ball":
                                any_balls_enabled = False
                                for player in (player1, player2):
                                    if player.player_num == current_players_turn:
                                        for ball in balls:
                                            if balls[ball].ball_type == player.ball_type and balls[ball].enabled:
                                                any_balls_enabled = True
                                if any_balls_enabled:
                                    DATA_STORAGE["Game variables"]["Player lost"] = current_players_turn
                                else:
                                    DATA_STORAGE["Game variables"]["Player lost"] = 3 - current_players_turn





                            # If it's first pot, set that player's balls to be the potted ball's type
                            else:
                                if player1.ball_type is None:
                                    if current_players_turn == 1:
                                        player1.ball_type = balls[ball].ball_type
                                        if balls[ball].ball_type == "Solid":
                                            player2.ball_type = "Stripe"
                                        else:
                                            player2.ball_type = "Solid"
                                    else:
                                        player2.ball_type = balls[ball].ball_type
                                        if balls[ball].ball_type == "Solid":
                                            player1.ball_type = "Stripe"
                                        else:
                                            player1.ball_type = "Solid"
                                for player in (player1,player2):
                                    if player.player_num == current_players_turn:
                                        if balls[ball].ball_type == player.ball_type:
                                            DATA_STORAGE["Game variables"]["Reward for remaining turn"] = True
                    
                    #show the lock texture
                    else:
                        tl_pos = np.array([hole.center[0] - (DATA_STORAGE["Other"]["Lock texture"].get_width()/2),hole.center[1] - (DATA_STORAGE["Other"]["Lock texture"].get_height()/2)])
                        tl_pos -= np.array([640,320])
                        tl_pos[0] *= 0.97
                        tl_pos[1] *= 0.925
                        tl_pos += np.array([640,320])
                        screen.blit(DATA_STORAGE["Other"]["Lock texture"], tl_pos)




                #Basically the holes code above but with a fat hitbox and a crack
                if DATA_STORAGE["Game variables"]["Events"]["Broken table"]:
                    hole = DATA_STORAGE["Other"]["Crack hitbox"]
                    screen.blit(DATA_STORAGE["Other"]["Crack texture"], (620,80))
                    if DEBUG:
                        pygame.draw.rect(screen, "red", hole)
                    if balls[ball].collision_rect.colliderect(hole):
                        balls[ball].is_falling = True
                        if ball == "White ball":
                            DATA_STORAGE["Game variables"]["White picked up"] = True
                            balls["White ball"].picked_up = True
                            DATA_STORAGE["Game variables"]["White sunk"] = True
                            DATA_STORAGE["Game variables"]["Punish for remaining turn"] = True

                        elif ball == "Black ball":
                            any_balls_enabled = False
                            for player in (player1, player2):
                                if player.player_num == current_players_turn:
                                    for ball in balls:
                                        if balls[ball].ball_type == player.ball_type and balls[ball].enabled:
                                            any_balls_enabled = True
                            if any_balls_enabled:
                                DATA_STORAGE["Game variables"]["Player lost"] = current_players_turn
                            else:
                                DATA_STORAGE["Game variables"]["Player lost"] = 3 - current_players_turn

                        # If it's first pot, set that player's balls to be the potted ball's type
                        else:
                            if player1.ball_type is None:
                                if current_players_turn == 1:
                                    player1.ball_type = balls[ball].ball_type
                                    if balls[ball].ball_type == "Solid":
                                        player2.ball_type = "Stripe"
                                    else:
                                        player2.ball_type = "Solid"
                                else:
                                    player2.ball_type = balls[ball].ball_type
                                    if balls[ball].ball_type == "Solid":
                                        player1.ball_type = "Stripe"
                                    else:
                                        player1.ball_type = "Solid"
                            for player in (player1,player2):
                                if player.player_num == current_players_turn:
                                    if balls[ball].ball_type == player.ball_type:
                                        DATA_STORAGE["Game variables"]["Reward for remaining turn"] = True
                                        if DEBUG:
                                            print(DATA_STORAGE["Game variables"]["Extend turn"])


            
            #Increase mass of the white ball if MASSive event is active
            if DATA_STORAGE["Game variables"]["Events"]["MASSive"]:
                balls["White ball"].mass = 850
            else:
                balls["White ball"].mass = balls["White ball"].org_mass



            # Collide balls
            for ball_pair in balls_to_collide:
                if DEBUG:
                    print(balls_to_collide)
                ball = ball_pair[0]
                colliding_ball = ball_pair[1]
                if balls[ball].enabled and balls[colliding_ball].enabled:
                    if DATA_STORAGE["Game variables"]["First collide"] is None:
                        if ball == "White ball":
                            DATA_STORAGE["Game variables"]["First collide"] = balls[colliding_ball].ball_type
                        elif colliding_ball == "White ball":
                            DATA_STORAGE["Game variables"]["First collide"] = balls[ball].ball_type
                    balls[ball].position, balls[colliding_ball].position = balls[ball].UnCollideBalls(balls[colliding_ball])
                    balls[ball].velocity, balls[colliding_ball].velocity = CalculateCollisionRebound(balls[ball], balls[colliding_ball])
                    
                    #clicking sound effect when balls collide
                    if SOUND_EFFECTS_ENABLED:
                        ball_sounds[random.randint(0,len(ball_sounds) - 1)].play()
            
            


            # Ball friction
            for ball in balls:
                for speed in range(0,2): # Do for both X and Y of ball
                    #lower friction if iced out event is active
                    if DATA_STORAGE["Game variables"]["Events"]["Iced out"]:
                        balls[ball].velocity[speed] = balls[ball].velocity[speed] * (1 - delta_time*0.15) # Don't tie to framerate
                    else:
                        balls[ball].velocity[speed] = balls[ball].velocity[speed] * (1 - delta_time*0.65) # Don't tie to framerate
                    if balls[ball].velocity[speed] < 2 and balls[ball].velocity[speed] > -2: # If it's small, just set it to 0.
                        balls[ball].velocity[speed] = 0.0
            

            

            #check if all balls are stationary
            no_balls_moving = True
            for ball in balls: 
                for speed in balls[ball].velocity:
                    if speed != 0:
                        no_balls_moving = False



            # When all balls are stationary
            if no_balls_moving:
                #punish for white getting sunk
                if DATA_STORAGE["Game variables"]["White sunk"]:
                    DATA_STORAGE["Game variables"]["Extend turn"] = False
                    DATA_STORAGE["Game variables"]["Reward for remaining turn"] = False


                #This is only triggered once per turn, so I can use it to trigger anything exactly once
                if DATA_STORAGE["User input variables"]["Locked"]:

                    for player in (player1,player2):
                        if player.player_num == current_players_turn:
                            if DATA_STORAGE["Game variables"]["First collide"] != player.ball_type and player.ball_type is not None:
                                DATA_STORAGE["Game variables"]["Reward for remaining turn"] = False
                                DATA_STORAGE["Game variables"]["Punish for remaining turn"] = True

                            if DEBUG:
                                print(DATA_STORAGE["Game variables"]["First collide"], "self is ", player.ball_type)
                                print(DATA_STORAGE["Game variables"]["Reward for remaining turn"],DATA_STORAGE["Game variables"]["Punish for remaining turn"],DATA_STORAGE["Game variables"]["Extend turn"])

                    DATA_STORAGE["Game variables"]["Tick once per shot"] = True
                    holes_to_lock = []

                    if DEBUG:
                        print("Locked")
                    if not DATA_STORAGE["Game variables"]["Reward for remaining turn"]:
                        if not DATA_STORAGE["Game variables"]["Extend turn"] or DATA_STORAGE["Game variables"]["Punish for remaining turn"]:
                            if DEBUG:
                                print(DATA_STORAGE["Game variables"]["Extend turn"])
                            current_players_turn = 3 - current_players_turn # Flips between which player's turn it is
                            if DEBUG:
                                print("Not extended turn")
                                print("Player now taking turn is", current_players_turn)


                        DATA_STORAGE["Game variables"]["Punish for remaining turn"] = False
                        # Make sure the right ball was hit or that any ball was hit
                        DATA_STORAGE["Game variables"]["Extend turn"] = False
                        if DEBUG:
                            print(DATA_STORAGE["Game variables"]["Extend turn"])


                #Resetting some vars between turns    
                DATA_STORAGE["Game variables"]["Punish for remaining turn"] = False
                DATA_STORAGE["Game variables"]["Reward for remaining turn"] = False    
                DATA_STORAGE["Game variables"]["Extend turn"] = False
                


                # Random events
                if DATA_STORAGE["User input variables"]["Locked"]:
                    if random_events:
                        selected_event = ReturnRandomEvent()
                        if DEBUG:
                            print(selected_event)
                            global DEBUG_EVENT
                            selected_event = DEBUG_EVENT
                        #Reset events
                        for event in DATA_STORAGE["Game variables"]["Events"]:
                            DATA_STORAGE["Game variables"]["Events"][event] = False
                        #Event selection
                        match selected_event:
                            case "None":
                                pass
                            case "Big ball":
                                DATA_STORAGE["Game variables"]["Events"]["Big ball"] = True
                            case "50 caliber":
                                if number_of_shots_taken > 10:
                                    DATA_STORAGE["Game variables"]["Events"]["50 caliber"] = True
                                else:
                                    selected_event = "None"
                            case "Black hole":
                                if number_of_shots_taken > 10:
                                    DATA_STORAGE["Game variables"]["Events"]["Black hole"] = True
                                else:
                                    selected_event = "None"
                            case "MASSive":
                                DATA_STORAGE["Game variables"]["Events"]["MASSive"] = True
                            case "Blind":
                                DATA_STORAGE["Game variables"]["Events"]["Blind"] = True
                            case "Iced out":
                                DATA_STORAGE["Game variables"]["Events"]["Iced out"] = True
                            case "Broken table":
                                if number_of_shots_taken > 10:
                                    DATA_STORAGE["Game variables"]["Events"]["Broken table"] = True
                                else:
                                    selected_event = "None"
                            case "Hacking":
                                DATA_STORAGE["Game variables"]["Events"]["Hacking"] = True
                            case "Locked holes":
                                DATA_STORAGE["Game variables"]["Events"]["Locked holes"] = True

                    else:
                        selected_event = None
                
                
                
                
                
                #other things
                DATA_STORAGE["User input variables"]["Locked"] = False
                DATA_STORAGE["Game variables"]["First collide"] = None

                # End the game if one of the players has lost
                if DATA_STORAGE["Game variables"]["Player lost"] is not None:
                    DATA_STORAGE["Game variables"]["End game"] = True

                if DATA_STORAGE["Game variables"]["White sunk"]:
                    if not DATA_STORAGE["Game variables"]["White picked up"]:
                        balls["White ball"].enabled = True
                    DATA_STORAGE["Game variables"]["Extend turn"] = True
                    balls["White ball"].texture = pygame.transform.scale(balls["White ball"].texture,(balls["White ball"].size*2, balls["White ball"].size*2)) # Return to org size
                    if DEBUG:
                        print(DATA_STORAGE["Game variables"]["Extend turn"])  
                



                for ball in balls:
                    if ball == "White ball":
                        ball_centre = (balls[ball].position[0]+balls[ball].size,balls[ball].position[1]+balls[ball].size)
                        if DEBUG:
                            pygame.draw.line(screen, "Red", ball_centre, pygame.mouse.get_pos(), 5)
                        if DATA_STORAGE["User input variables"]["Shot made"] == True: # Shot has been made
                            mouse_position_on_release = (DATA_STORAGE["User input variables"]["Mouse position"])
                            if not (ball_centre == mouse_position_on_release): # Prevent program from dying if both ball and mouse position are the same pixel
                                DATA_STORAGE["User input variables"]["Shot made"] = False # Aknowledge shot
                                DATA_STORAGE["User input variables"]["Locked"] = True
                                number_of_shots_taken += 1
                                ball_vector = np.array([mouse_position_on_release[0] - ball_centre[0], mouse_position_on_release[1] - ball_centre[1]])
                                ball_vector_magnitude = np.linalg.norm(ball_vector)
                                ball_vector = ball_vector/ball_vector_magnitude
                                balls[ball].velocity = np.array([float(ball_vector[0]*shot_power * 3)*(1/frame_rate),float(ball_vector[1]*shot_power * 3)*(1/frame_rate)])
                                if DATA_STORAGE["Game variables"]["Events"]["Black hole"]:
                                    for ball in balls:
                                        if ball != "White ball":
                                            balls[ball].velocity = np.array([balls["White ball"].position[0] - balls[ball].position[0], balls["White ball"].position[1] - balls[ball].position[1]])
                                if SOUND_EFFECTS_ENABLED:
                                    cue_sounds[random.randint(0,len(cue_sounds)-1)].play()
                                
                                if DEBUG:
                                    print(f"Ball vector is {ball_vector}")
                                    print(f"Ball velocity is {balls[ball].velocity}")
                        for player in (player1,player2):
                            if player.player_num == current_players_turn and not DATA_STORAGE["Game variables"]["White picked up"]:
                                cue, cue_pos = CalculateCuePosFromAngle(player, balls[ball], shot_power, DATA_STORAGE["Game variables"]["Events"]["50 caliber"])
                                screen.blit(cue, cue_pos)
                
            else:
                DATA_STORAGE["User input variables"]["Locked"] = True



            for ball in balls: #limit speed
                if not DATA_STORAGE["Game variables"]["Events"]["50 caliber"]:
                    directional_velocity = (balls[ball].velocity[0]**2 + balls[ball].velocity[1]**2)**0.5
                    if directional_velocity > 2000:
                        velo_mult = directional_velocity/2000
                        balls[ball].velocity /= velo_mult

                temp_old_position = balls[ball].old_position
                collided = False
                balls[ball].collision_rect.topleft = balls[ball].position
                for side in table_bounds:
                    if DEBUG:
                        print(table_bounds[side])
                        print(balls[ball].collision_rect)
                    if side == "Top" or side == "Bottom":
                        if balls[ball].collision_rect.colliderect(table_bounds[side]):
                            collided = True
                            progress = balls[ball].DetermineTimeOfCollisionWall(table_bounds[side])
                            if DEBUG:
                                pygame.draw.rect(screen, "Red", table_bounds[side])
                                pygame.draw.rect(screen, "Red", balls[ball].collision_rect)
                            #collision for top and bottom walls
                            mid_position = (balls[ball].position[0] + (balls[ball].velocity[0] * delta_time * progress),balls[ball].position[1] + (balls[ball].velocity[1] * delta_time * progress))
                            if side == "Bottom":
                                if DEBUG:
                                    print(f"Side is {side}")
                                if balls[ball].velocity[1] > 0:
                                    if DEBUG:
                                        print(f"{side} has flipped {balls[ball]} velocity, which is now {balls[ball].velocity}")
                                    balls[ball].velocity[1] *= -1
                            elif side == "Top":
                                if DEBUG:
                                    print(f"Side is {side}")
                                if balls[ball].velocity[1] < 0:
                                    if DEBUG:
                                        print(f"{side} has flipped {balls[ball]} velocity, which is now {balls[ball].velocity}")
                                    balls[ball].velocity[1] *= -1

                            balls[ball].position = (mid_position[0] + (balls[ball].velocity[0] * delta_time * (1-progress)), mid_position[1] + (balls[ball].velocity[1] * delta_time * (1-progress)))
                    elif side == "Right" or side == "Left":
                        #collision for left and right
                        if balls[ball].collision_rect.colliderect(table_bounds[side]):
                            collided = True
                            progress = balls[ball].DetermineTimeOfCollisionWall(table_bounds[side])
                            if DEBUG:
                                pygame.draw.rect(screen, "Red", table_bounds[side])
                                pygame.draw.rect(screen, "Red", balls[ball].collision_rect)

                            mid_position = (balls[ball].position[0] + (balls[ball].velocity[0] * delta_time * progress),balls[ball].position[1] + (balls[ball].velocity[1] * delta_time * progress))
                            if side == "Left":
                                if balls[ball].velocity[0] < 0:
                                    balls[ball].velocity[0] *= -1
                            elif side == "Right":
                                if balls[ball].velocity[0] > 0:
                                    balls[ball].velocity[0] *= -1
                            
                            balls[ball].position = (mid_position[0] + (balls[ball].velocity[0] * delta_time * (1-progress)), mid_position[1] + (balls[ball].velocity[1] * delta_time * (1-progress)))

                if not collided:
                    balls[ball].old_position = balls[ball].position
                    balls[ball].position = (balls[ball].position[0] + (balls[ball].velocity[0] * delta_time),balls[ball].position[1] + (balls[ball].velocity[1] * delta_time))
                else:
                    balls[ball].old_position = temp_old_position


                #Render balls
                if balls[ball].is_falling:
                    balls[ball].ProgressFall()
                balls[ball].Render(screen)
                balls[ball].size = balls[ball].org_size


                if DEBUG:
                    for ball_pair in balls_to_collide:
                        ball = ball_pair[0]
                        colliding_ball = ball_pair[1]
                        ball_centre = (balls[ball].position[0] + balls[ball].size, balls[ball].position[1] + balls[ball].size)
                        col_ball_centre = (balls[colliding_ball].position[0] + balls[colliding_ball].size, balls[colliding_ball].position[1] + balls[colliding_ball].size)
                        pygame.draw.line(screen, "Blue", ball_centre, col_ball_centre, 3)
            
            if DATA_STORAGE["Game variables"]["Events"]["Blind"]:
                ball_centre = (balls["White ball"].position[0] + balls["White ball"].size, balls["White ball"].position[1] + balls["White ball"].size)
                screen.blit(DATA_STORAGE["Other"]["Blind texture"], (ball_centre[0] - DATA_STORAGE["Other"]["Blind texture"].get_width() / 2, ball_centre[1] - DATA_STORAGE["Other"]["Blind texture"].get_height() / 2))
                if DEBUG:
                    for ball in balls:
                        pygame.draw.rect(screen, "Red", balls[ball].collision_rect)
            
            
            # Hacking event
            if DATA_STORAGE["Game variables"]["Events"]["Hacking"]:
                ball_centre = (balls["White ball"].position[0] + balls["White ball"].size, balls["White ball"].position[1] + balls["White ball"].size)
                ball_centre_shadow = (balls["White ball"].position[0] + balls["White ball"].size + 3, balls["White ball"].position[1] + balls["White ball"].size + 3)
                mouse_pos_shadow = [(pygame.mouse.get_pos())[0] + 3, (pygame.mouse.get_pos())[1] + 3]
                pygame.draw.line(screen, "Black", ball_centre_shadow, mouse_pos_shadow, 5)
                pygame.draw.line(screen, "White", ball_centre, pygame.mouse.get_pos(), 5)
            


            # Giving player info text a shadow
            for player in (player1,player2):
                if player.player_num == current_players_turn:
                    screen.blit(player.frame_shadow, (7,7))
                    screen.blit(player.pfp, (14,14))
                    screen.blit(player.frame_texture, (2,2))
                    blit_top_left_pos = [150,10]
                    any_balls_enabled = False

                    #display the remaining balls that must be potted
                    for ball in balls:
                        if balls[ball].enabled and balls[ball].ball_type == player.ball_type:
                            scaled_ball = pygame.transform.scale(balls[ball].texture, (64,64))
                            ball_shadow = pygame.transform.scale(balls[ball].shadow, (64,64))
                            screen.blit(ball_shadow, (blit_top_left_pos[0] + 3, blit_top_left_pos[1] + 3))
                            screen.blit(scaled_ball, blit_top_left_pos)
                            blit_top_left_pos[0] += 76
                            any_balls_enabled = True

                    #if there is no more solid/stripe balls to pot, switch to displaying the black ball
                    if not any_balls_enabled:
                        if balls["Black ball"].enabled and player.ball_type is not None:
                            player.ball_type = "Black"
                            ball_shadow = pygame.transform.scale(balls["Black ball"].shadow, (64,64))
                            scaled_ball = pygame.transform.scale(balls["Black ball"].texture, (64,64))
                            screen.blit(ball_shadow, (blit_top_left_pos[0] + 3, blit_top_left_pos[1] + 3))
                            screen.blit(scaled_ball,blit_top_left_pos)




                    if DEBUG:
                        first_collision = DATA_STORAGE["Game variables"]["First collide"]
                        
                        if player.ball_type is not None:
                            player_text = game_font.render(f"Currently P{current_players_turn}'s turn. Ball type to pot is {player.ball_type.lower()}s. First hit is {first_collision}.", True, "Black")
                            player_text.set_alpha(64)
                            screen.blit(player_text, (3,3))
                            player_text = game_font.render(f"Currently P{current_players_turn}'s turn. Ball type to pot is {player.ball_type.lower()}s. First hit is {first_collision}.", True, "White")
                            screen.blit(player_text, (0,0))
                        else:
                            player_text = game_font.render(f"Currently P{current_players_turn}'s turn. No balls potted yet. First hit is {first_collision}.", True, "Black")
                            player_text.set_alpha(64)
                            screen.blit(player_text, (3,3))
                            player_text = game_font.render(f"Currently P{current_players_turn}'s turn. No balls potted yet. First hit is {first_collision}.", True, "White")
                            screen.blit(player_text, (0,0))

                    #Show the random event that was selected
                    if random_events:
                        try:
                            random_event_text = game_font.render(f"Random event: {selected_event}", True, "Black")
                            random_event_text.set_alpha(64)
                            screen.blit(random_event_text, (1273 - random_event_text.get_width(),13))
                            random_event_text = game_font.render(f"Random event: {selected_event}", True, "White")
                            screen.blit(random_event_text, (1270 - random_event_text.get_width(),10))
                        except:
                            random_event_text = game_font.render(f"Random event: None", True, "Black")
                            random_event_text.set_alpha(64)
                            screen.blit(random_event_text, (1273 - random_event_text.get_width(),13))
                            random_event_text = game_font.render(f"Random event: None", True, "White")
                            screen.blit(random_event_text, (1270 - random_event_text.get_width(),10))




            # Giving power of shot text a shadow (and a fancy line thingamabob)
            if not DATA_STORAGE["User input variables"]["Locked"] and not MOUSE_POINTER:
                power_text = game_font.render(f"Current power: {str(shot_power/1000)[0:5]}%", True, "Black")
                power_text.set_alpha(64)
                if balls["White ball"].position[0] > 640: #half screen resolution
                    text_tl = (balls["White ball"].position[0] - power_text.get_width(), balls["White ball"].position[1] + balls["White ball"].size)
                    pygame.draw.line(screen, "Black", (text_tl[0] + 3, text_tl[1] + power_text.get_height() + 3), (text_tl[0] + power_text.get_width() + 3, text_tl[1] + power_text.get_height() + 3), 4)
                    pygame.draw.line(screen, "Black", (text_tl[0] + power_text.get_width() + 3, text_tl[1] + power_text.get_height() + 3), (balls["White ball"].position[0] + balls["White ball"].size + 3, balls["White ball"].position[1] + balls["White ball"].size + 3), 4)
                    screen.blit(power_text, (text_tl[0] + 3, text_tl[1] + 3))
                    power_text = game_font.render(f"Current power: {str(shot_power/1000)[0:5]}%", True, "White")
                    pygame.draw.line(screen, "White", (text_tl[0], text_tl[1] + power_text.get_height()), (text_tl[0] + power_text.get_width(), text_tl[1] + power_text.get_height()), 4)
                    pygame.draw.line(screen, "White", (text_tl[0] + power_text.get_width(), text_tl[1] + power_text.get_height()), (balls["White ball"].position[0] + balls["White ball"].size, balls["White ball"].position[1] + balls["White ball"].size), 4)
                    screen.blit(power_text, text_tl)
                else:
                    text_tl = (balls["White ball"].position[0] + balls["White ball"].size*2, balls["White ball"].position[1] + balls["White ball"].size)
                    pygame.draw.line(screen, "Black", (text_tl[0] + 3, text_tl[1] + power_text.get_height() + 3), (text_tl[0] + power_text.get_width() + 3, text_tl[1] + power_text.get_height() + 3), 4)
                    pygame.draw.line(screen, "Black", (text_tl[0] + 3, text_tl[1] + power_text.get_height() + 3), (balls["White ball"].position[0] + balls["White ball"].size + 3, balls["White ball"].position[1] + balls["White ball"].size + 3), 4)
                    screen.blit(power_text, (balls["White ball"].position[0] + balls["White ball"].size*2 + 3, balls["White ball"].position[1] + balls["White ball"].size + 3))
                    pygame.draw.line(screen, "White", (text_tl[0], text_tl[1] + power_text.get_height()), (text_tl[0] + power_text.get_width(), text_tl[1] + power_text.get_height()), 4)
                    pygame.draw.line(screen, "White", (text_tl[0], text_tl[1] + power_text.get_height()), (balls["White ball"].position[0] + balls["White ball"].size, balls["White ball"].position[1] + balls["White ball"].size), 4)
                    power_text = game_font.render(f"Current power: {str(shot_power/1000)[0:5]}%", True, "White")
                    screen.blit(power_text, (balls["White ball"].position[0] + balls["White ball"].size*2, balls["White ball"].position[1] + balls["White ball"].size))




            if DEBUG:
                #--------------------------------------------------------------------
                #JUST USED TO SEE FPS IN THE TESTING BIT
                try:
                    frame_list.append(1/(time.time()-previous_frame_time))
                except:
                    frame_list.append(288)

                if len(frame_list) > 288:
                    del frame_list[0]
                average = round(sum(frame_list)/len(frame_list))

                fps_text = game_font.render(f"FPS:{average}", True, "White")
                screen.blit(fps_text, pygame.mouse.get_pos())

                #-----------------------------------------------------------------





            #Update the display
            if DATA_STORAGE["Game variables"]["End game"]:
                screengrab = screen.copy()
            if MOUSE_POINTER:
                if no_balls_moving:
                    power_level = floor(shot_power/100000*6)
                    if power_level <= 6:
                        screen.blit(mouse_pointer[power_level+1], pygame.mouse.get_pos())
                    else:
                        if pygame.time.get_ticks() % 100 < 50:
                            screen.blit(mouse_pointer[8], pygame.mouse.get_pos())
                        else:
                            screen.blit(mouse_pointer[1], pygame.mouse.get_pos())
                else:
                    screen.blit(mouse_pointer[0], pygame.mouse.get_pos())
            pygame.display.update()

        fade_black = Fade(time_in_seconds= 0.5,fade_in=False, tween= "quadratic_in", frame_rate= frame_rate, fade_from=0, fade_to=192)
        dark_screen = pygame.image.load("Resources\In_Game_Assets\Black_screen.png").convert()
        while len(fade_black) > 0:
            screen.blit(screengrab, (0,0))
            screen.blit(dark_screen, (0,0))
            dark_screen.set_alpha(fade_black.pop())
            #Update the display
            pygame.display.update()
            previous_time_since_start = time.time()
            clock.tick(frame_rate)
        buttons = DATA_STORAGE["Buttons"]
        while not IS_LOADING:
            delta_time = CalculateDeltaTime(previous_time_since_start)
            previous_time_since_start = time.time()

            screen.blit(screengrab, (0,0))
            screen.blit(dark_screen, (0,0))
            for button in buttons:
                if button.BeingHoveredOver(pygame.mouse.get_pos()):
                    button.cs = 1
                    if pygame.mouse.get_pressed()[0]:
                        button.cs = 2
                else:
                    button.cs = 0

                for event in pygame.event.get(pump= True):
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        for button in buttons:
                            if button.BeingHoveredOver(pygame.mouse.get_pos()):
                                if button.id == 0:
                                    # Main menu
                                    IS_LOADING = True
                                    WHAT_AM_I_RENDERING = 0

                                elif button.id == 1:
                                    # Play again
                                    IS_LOADING = True
                                    
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                button.Render(screen)
            winner_text = game_font.render(f"P{3 - DATA_STORAGE['Game variables']['Player lost']} won!", True, "White")
            winner_text = pygame.transform.scale2x(winner_text)
            screen.blit(winner_text, (640 - winner_text.get_width()/2,150))

            if DEBUG:
                fps_text = game_font.render(f"FPS:{1/time.time()-previous_time_since_start}", True, "White")
                screen.blit(fps_text, (0,0))
                print("IS_LOADING state is", IS_LOADING)
                print("Updated screen")

            if MOUSE_POINTER:
                screen.blit(mouse_pointer[0], pygame.mouse.get_pos())

            pygame.display.update()

        fade_black = Fade(time_in_seconds= 0.5,fade_in=False, tween= "quadratic_in", frame_rate= frame_rate)
        screengrab = screen.copy()
        while len(fade_black) > 0:
        
            screen.blit(screengrab, (0,0))
            for button in buttons:
                button.cs = 0
                button.Render(screen)

            LOADING_SCREEN.set_alpha(fade_black.pop())              
            screen.blit(LOADING_SCREEN,(0,0))
            #Update the display
            pygame.display.update()
            clock.tick(frame_rate)
        IS_LOADING = False
        #Update the display
        pygame.display.update()


        
            
    #---------------------------------------------------------------------------------------------------------



    #Main program loop
            
    while True:
        
        #Load required resources
        LoadResources()
        IS_LOADING = False
        
        if WHAT_AM_I_RENDERING == 0:
            MainMenuRender()
        elif WHAT_AM_I_RENDERING == 1:
            PlayMenuRender()
        elif WHAT_AM_I_RENDERING == 2:
            GameRender(True)
        elif WHAT_AM_I_RENDERING == 3:
            GameRender(False)
        elif WHAT_AM_I_RENDERING == 4:
            ConfigMenuRender()
        elif WHAT_AM_I_RENDERING == 5:
            CustomisationMenuRender()

        
        #Get Delta Time
        delta_time = CalculateDeltaTime(previous_time_since_start)
        previous_time_since_start = time.time()
        
        #if the X (close) button is pressed, quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit