#NYT's Connections - A Clone by SirNooby
import pygame
import math
import random

#Initialize Game Features
pygame.init()
pygame.mixer.init()

screen_width = 900
screen_height = 650

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Connections")
pygame.display.set_icon(pygame.image.load("Contents/Interface/icon.png"))

clock = pygame.time.Clock()
font = pygame.font.Font("Contents/Interface/franklin.ttf", 16)
font_h1 = pygame.font.Font("Contents/Interface/franklin.ttf", 24)

#Define the Selection Box Class
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 175
        self.height = 75
        self.color = "#323232"
        self.selected = False
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def display(self): #Render the generated box, and the text placed on top
        pygame.draw.rect(screen, self.color, (self.x, self.y, 175, 75), 0, 3)
        self.text_surface = font.render(self.text.upper(), True, (255, 255, 255) if not self.selected else (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, self.text_rect)

    def update(self, event, clicks): #Detect if a user has clicked a box
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):

                if self.selected and self.color == "#FFFFFF":
                    self.color = "#323232"
                    self.selected = False
                    player_selection.remove(self.text)
                    return -1 #Decrement the click count
                
                elif clicks < 4 and self.color == "#323232":
                    self.color = "#FFFFFF"
                    self.selected = True
                    player_selection.append(self.text)
                    return 1 #Increment click count
        return 0 #Add nothing on frames that do nothing


#Define the submission enter button
class EnterButton():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 50
        self.color = "#FFFFFF"
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def display(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0, 5)
        self.text_surface = font.render("Enter", True, (0, 0, 0))
        screen.blit(self.text_surface, (self.x+60, self.y+15))

    def update(self, event):
        global clicks
        global solved
        global player_lives

        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                for i in level_solutions:
                    if set(i[:4]) == set(player_selection):
                        clicks = 0
                        submission_correct = True
                        solved_set = i[4]
                        break
                    submission_correct = False

                if submission_correct:
                    solved += 1
                    for box in boxes:
                        if box.selected:
                            box.color = (72, 55, 132)
                            box.selected = False
                            box.text = solved_set
                            player_selection.clear()
                else:
                    player_lives -= 1


#Define the lives class
class LivesDisplay():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = "#FFFFFF"
        self.radius = 7

    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

#Load Important Functions and Declare Variables
#Define the color swapper for background
def palette_swap(surf, old_color, new_color):
    image_copy = pygame.Surface(background.get_size())
    image_copy.fill(new_color)
    surf.set_colorkey(old_color)
    image_copy.blit(surf, (0,0))
    return image_copy

#Load the scolling background
def Background_Loader(background):
    background_tiles = math.ceil(screen_width / background.get_width()) + 1
    for i in range(0, background_tiles):
        screen.blit(background, (i*background.get_width() +background_scroll,0))
        screen.blit(background, (i*background.get_width() +background_scroll, background.get_height() - 15))

background = pygame.transform.scale(pygame.image.load("Contents/Interface/background.png").convert_alpha(), (700, 350))
backgrounds = {
    0:palette_swap(background, (0,0,0), ("#70a9b8")), #Title Screen
    1:palette_swap(background, (0,0,0), ("#9982b8")), #Game Screen
    2:palette_swap(background, (0,0,0), ("#acad50")), #Custom Screen
    3:palette_swap(background, (0,0,0), ("#b02164"))  #Custom Game Screen
}

#Define the music player (JUKEBOX LIKE MINECRAFT!)
def Jukebox(track):
    pygame.mixer.music.load(music[track])
    pygame.mixer.music.play(-1)

music = {
    0:"Contents/Audio/title.mp3", #Title Screen
    1:"Contents/Audio/game.mp3", #Base Game
    2:"Contents/Audio/custom.mp3", #Creating Custom Game
    3:"Contents/Audio/customgame.mp3" #Playing Custom Game
}

sound_effects = [
    pygame.mixer.Sound("Contents/Audio/select.mp3")
]

#Define the random level generator
def level_generate():
    global version_levels
    random_level = random.randint(1, 14)
    level_loader = open("Contents/Puzzles/puzzles.txt")
    lines = level_loader.readlines()[random_level*5-5:random_level*5-1]
    level = [list(map(str, line.strip().split(","))) for line in lines]

    #Converts the taken items out into a 2D list
    de_level = [item for sublist in level for item in sublist[:4]]
    random.shuffle(de_level)
    shuffled_level = [de_level[i:i + 4] for i in range(0, len(de_level), 4)]
    return shuffled_level, level            

current_level, level_solutions = level_generate()

#Create main game components
#Create menu screens
def Title_Screen():
    global play_hitbox
    global custom_hitbox

    title_logo = pygame.transform.scale(pygame.image.load("Contents/Interface/title.png").convert_alpha(), (400, 75))
    version_text = font.render(version_number + " (Created By SirNooby)", True, (0, 0, 0))

    play_button = pygame.draw.rect(screen, ("#323232"), (310, 280, 250, 75), 0, 3)
    play_hitbox = pygame.Rect(310, 280, 250, 75)
    play_text = pygame.font.Font("Contents/Interface/franklin.ttf", 24).render("Play", True, (255, 255, 255))

    custom_button = pygame.draw.rect(screen, ("#323232"), (310, 410, 250, 75), 0, 3)
    custom_hitbox = pygame.Rect(310, 410, 250, 75)
    custom_text = pygame.font.Font("Contents/Interface/franklin.ttf", 24).render("Custom", True, (255, 255, 255))

    #Render all objects onto the plane
    screen.blit(title_logo, (240, 150))
    screen.blit(version_text, (15, 625))
    screen.blit(play_text, (415, 300))
    screen.blit(custom_text, (400, 430))
    
#Define the GameGenerator, drawing all sprites
def Game_Generator():
    pygame.draw.rect(screen, (167, 141, 201), (35, 85, 800, 520), 0, 5)
    screen.blit(pygame.transform.scale(pygame.image.load("Contents/Interface/title.png").convert_alpha(), (400, 75)), (240, 0))
    for box in boxes:
        box.display()

    lives = [LivesDisplay(600 + i*50, 535) for i in range(player_lives)]   
    lives_text = screen.blit(pygame.font.Font("Contents/Interface/franklin.ttf", 24).render("Mistakes Remaining: ", True, (255, 255, 255)), (340, 520))
 
    for i in lives:
        i.display()
    EnterButton(150,500).display()

#Create the custom level editor menu
def Custom_Level():
    global clear_hitbox
    global generate_hitbox

    title_logo = pygame.transform.scale(pygame.image.load("Contents/Interface/title.png").convert_alpha(), (400, 75))
    top_infobox = pygame.draw.rect(screen, ("#6c7a42"), (240, 125, 400, 60), 0, 3)
    message_infobox = pygame.draw.rect(screen, ("#6c7a42"), (240, 200, 400, 60), 0, 3)
    type_infobox = pygame.draw.rect(screen, ("#6c7a42"), (130, 240, 620, 85), 0, 3)
    debug_infobox = pygame.draw.rect(screen, ("#6c7a42"), (100, 400, 680, 100), 0, 3)
    debugtitle_infobox = pygame.draw.rect(screen, ("#6c7a42"), (120, 360, 200, 50), 0, 3)
    debuginstructions_infobox = pygame.draw.rect(screen, ("#abbd7b"), (165, 460, 540, 35), 6, 3)

    clear_box = pygame.draw.rect(screen, ("#6c7a42"), (160, 550, 175, 60), 0, 6)
    clear_hitbox = pygame.Rect(160, 550, 175, 60)

    generate_box = pygame.draw.rect(screen, ("#6c7a42") if len(custom_puzzle) == 4 else ("#323620"), (550, 550, 175, 60), 0, 6)
    generate_hitbox = pygame.Rect(550, 550, 175, 60)


    screen.blit(font_h1.render("Custom Connections Creator", True, (255,255,255)), (285, 125))
    screen.blit(font.render("Input categories seperated by commas", True, (255,255,255)), (310, 150))
    screen.blit(font_h1.render("Input Categories Here!", True, (255, 255, 255)), (320, 205))
    screen.blit(font_h1.render(input_text, True, (0,0,0)), (150, 250))
    screen.blit(font_h1.render("Debug Info:", True, (0,0,0)), (140, 365))
    screen.blit(font.render(debug_text, True, (0,0,0)), (120, 410))
    screen.blit(font.render("Correct submission are formatted: item1,item2,item3,item4,categoryname", True, (0,0,0)), (175, 465))
    screen.blit(font.render("Clear Custom Cache", True, (255,255,255)), (175, 565))
    screen.blit(font.render("Generate Puzzle", True, (255,255,255)), (580, 565))
    pygame.draw.rect(screen, (0,0,0), (140, 250, 600, 60), 5)
    screen.blit(title_logo, (240, 0))
    

#Generate main game varaibles and gameloop
background_scroll = 0
boxes = []
gamestate = "title"
solved = 0
clicks = 0
custom_puzzle = []
debug_text = "Enter single catergories seperated by commas until the generate button lights up!"
input_text = ""
player_lives = 4
player_selection = []
version_number = "V1.0.1"
version_levels = 5
running = True
Jukebox(0)

#Initialze Primary Game Loop
while running:

    #Capture user events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP: # #If the mouse has been pressed down, check if a selection box has been chosen
            if gamestate == "game" or gamestate == "customgame": #If a game has started render boxes
                for box in boxes:
                    sound_effects[0].play()
                    clicks += box.update(event, clicks)
                EnterButton(150, 500).update(event)

            if gamestate == "custom": #If a button was hit during custom game creator
                if clear_hitbox.collidepoint(event.pos): #Check if clear custom cache box has been hit
                    custom_puzzle.clear()
                    debug_text = "Custom Puzzle Cache has been wiped!"
                if generate_hitbox.collidepoint(event.pos): #Check if generate box has been hit
                    if len(custom_puzzle) == 4: #Shuffling algorithm (yes i could make this a function)
                        Jukebox(3)
                        de_level = [item for sublist in custom_puzzle for item in sublist[:4]]
                        random.shuffle(de_level)
                        shuffled_level = [de_level[i:i + 4] for i in range(0, len(de_level), 4)]
                        current_level, level_solutions = shuffled_level, custom_puzzle
                        boxes = [Box(50 + i * 200, 100 + v * 100, current_level[i][v]) for i in range(4) for v in range(4)]
                        gamestate = "customgame"
                    else:
                        debug_text = "(ERR:03) Unable to generate, make sure four categories have been entered"

            #Handle Title Screen buttons
            if gamestate == "title":
                if play_hitbox.collidepoint(event.pos):
                    gamestate = "game"
                    sound_effects[0].play()
                    boxes = [Box(50 + i * 200, 100 + v * 100, current_level[i][v]) for i in range(4) for v in range(4)]
                    Jukebox(1)

                if custom_hitbox.collidepoint(event.pos):
                    sound_effects[0].play()
                    gamestate = "custom"
                    Jukebox(2)

        #Handle the custom input (I hate this part)
        if event.type == pygame.KEYDOWN:
            if gamestate == "custom":
                if event.key == pygame.K_RETURN:
                    if len(custom_puzzle) !=4:
                        if len(input_text.split(",")) == 5:
                            custom_puzzle.append(input_text.split(","))
                            debug_text = "Category " + str(len(custom_puzzle)) + " submitted sucessfully! - " + str(input_text.split(","))
                            input_text = ""
                        else:
                            debug_text = "(ERR:01) Category unable to parse! Check if 5 items exist, all seperated by commas!"
                    else:
                        debug_text = "(ERR:02) Max Catergories Generated! Either create a game or restart!"  
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            
            #If player closes game
            if event.key == pygame.K_ESCAPE:
                if gamestate != "title":
                    gamestate = "title"
                    Jukebox(0)
                else:
                    running = False
    
    #Check different game states and apply methods
    if gamestate == "title":
        Background_Loader(backgrounds[0])
        Title_Screen()

    if gamestate == "custom":
        Background_Loader(backgrounds[2])
        Custom_Level()

    if gamestate == "game":
        Background_Loader(backgrounds[1])
        Game_Generator()

    if gamestate == "customgame":
        Background_Loader(backgrounds[3])
        Game_Generator()

    #Collect end cases
    if player_lives == 0:
        player_lives = 4
        Jukebox(0)
        gamestate = "title"

    if solved == 4:
        gamestate = "title"
        player_lives = 4
        player_selection.clear()
        solved = 0 

        for box in boxes:
            box.color = "#323232"
            box.selected = False
            box.text = "NEW GAME"

        current_level, level_solutions = level_generate()
        Jukebox(0)
        boxes = [Box(50 + i * 200, 100 + v * 100, current_level[i][v]) for i in range(4) for v in range(4)]

    #Continue to update the background every frame
    if abs(background_scroll) > background.get_width():
        background_scroll = 0  
    background_scroll -= 1 

    #Update the screen every frame
    clock.tick(60)
    pygame.display.update()