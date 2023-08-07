#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys, random, time, os, entities, vfx
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.display.set_caption('The Crushed Sky')
WINDOWWIDTH = 480*2
WINDOWHEIGHT = 280*2
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0,32)
Display = pygame.Surface((480,280))
# Font ------------------------------------------------------- #
def GenerateFont(FontImage,FontSpacing,TileSize,TileSizeY,color):
    FontOrder = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')']
    FontImage = pygame.image.load(FontImage).convert()
    NewSurf = pygame.Surface((FontImage.get_width(),FontImage.get_height())).convert()
    NewSurf.fill(color)
    FontImage.set_colorkey((0,0,0))
    NewSurf.blit(FontImage,(0,0))
    FontImage = NewSurf.copy()
    FontImage.set_colorkey((255,255,255))
    num = 0
    for char in FontOrder:
        FontImage.set_clip(pygame.Rect(((TileSize+1)*num),0,TileSize,TileSizeY))
        CharacterImage = FontImage.subsurface(FontImage.get_clip())
        FontSpacing[char].append(CharacterImage)
        num += 1
    FontSpacing['Height'] = TileSizeY
    return FontSpacing
def ShowText(Text,X,Y,Spacing,WidthLimit,Font,surface):
    Text += ' '
    OriginalX = X
    OriginalY = Y
    CurrentWord = ''
    for char in Text:
        if char not in [' ','\n']:
            try:
                Image = Font[str(char)][1]
                CurrentWord += str(char)
            except KeyError:
                pass
        else:
            WordTotal = 0
            for char2 in CurrentWord:
                WordTotal += Font[char2][0]
                WordTotal += Spacing
            if WordTotal+X-OriginalX > WidthLimit:
                X = OriginalX
                Y += Font['Height']
            for char2 in CurrentWord:
                Image = Font[str(char2)][1]
                surface.blit(Image,(X,Y))
                X += Font[char2][0]
                X += Spacing
            if char == ' ':
                X += Font['A'][0]
                X += Spacing
            else:
                X = OriginalX
                Y += Font['Height']
            CurrentWord = ''
        if X-OriginalX > WidthLimit:
            X = OriginalX
            Y += Font['Height']
    return X,Y
Font_base = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
          'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
          '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
          '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
          '(':[2],')':[2]}
Font_base_2 = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
          'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
          '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
          '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
          '(':[2],')':[2]}
Font_base_3 = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
          'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
          '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
          '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
          '(':[2],')':[2]}
Font_2 = GenerateFont('Data/Fonts/small_font.png',Font_base_3,5,8,(143,52,63)).copy()
Font_1 = GenerateFont('Data/Fonts/small_font.png',Font_base,5,8,(255,254,255)).copy()
Font_0 = GenerateFont('Data/Fonts/small_font.png',Font_base_2,5,8,(100,170,200)).copy()
# Functions -------------------------------------------------- #
def normalize(number,amount):
    if number > 0:
        if number < amount:
            number = 0
        else:
            number -= amount
    if number < 0:
        if number > -amount:
            number = 0
        else:
            number += amount
    return number
def cap(number,amount):
    if number > amount:
        number = amount
    if number < -amount:
        number = -amount
    return number

def Text2List(Text,Divider,intmode=False):
    List = []
    Current = ''
    for char in Text:
        if char != Divider:
            Current += char
        else:
            if intmode == True:
                try:
                    List.append(int(Current))
                except:
                    List.append(Current)
            else:
                List.append(Current)
            Current = ''
    return List

def load_map(name):
    pushable_list = ['crate.png']
    enemy_list = ['dropper.png','beamer.png']
    file = open('Data/Maps/' + name + '.txt','r')
    map_data = file.read()
    file.close()
    tiles = Text2List(map_data,'=')
    n = 0
    for tile in tiles:
        tiles[n] = Text2List(tile,';',True)
        n += 1
    for tile in tiles:
        tile[0] = Text2List(tile[0],'+')
    tile_map = {}
    pushables = []
    shards = []
    enemies = []
    boosts = []
    void_level = -1000
    for tile in tiles:
        for img in tile[0]:
            if img in pushable_list:
                pushables.append([img,tile[1]*23,tile[2]*16])
                tile[0].remove(img)
            if img == 'spawn.png':
                spawn = tile[1]*23,tile[2]*16-8
                tile[0].remove(img)
            if img == 'shards.png':
                shards.append([tile[1]*23,tile[2]*16,random.randint(0,20)]) # x, y, timer
                tile[0].remove(img)
            if img in enemy_list:
                enemies.append([img,tile[1]*23,tile[2]*16,random.randint(0,39),[tile[1]*23,tile[2]*16]]) # ID, x, y, timer, spawn
                tile[0].remove(img)
            if img == 'stamina_ball.png':
                boosts.append([img,tile[1]*23,tile[2]*16])
                tile[0].remove(img)
        if len(tile[0]) > 0:
            tile_map[str(tile[1]) + ';' + str(tile[2])] = tile
            if tile[2]*16 > void_level:
                void_level = tile[2]*16
    return tile_map,pushables,spawn,shards,enemies,boosts,void_level+128
# Images ----------------------------------------------------- #
no_physics_tiles = ['tree_0.png','tree_1.png','tree_2.png','tree_3.png','tree_4.png','tree_5.png','tree_6.png','pole_0.png','pole_1.png','pole_2.png','pole_3.png']
background_tiles = ['tree_0.png','tree_1.png','tree_2.png','tree_3.png','tree_4.png','tree_5.png','tree_6.png','pole_0.png','pole_1.png','pole_2.png','pole_3.png']
tile_list = os.listdir('Data/Images/Tiles')
tile_database = {}
for tile in tile_list:
    if tile[-1] == 'g':
        img = pygame.image.load('Data/Images/Tiles/' + tile).convert()
        img.set_colorkey((255,255,255))
        tile_database[tile] = img.copy()

stamina_img = pygame.image.load('Data/Images/stamina.png').convert()

text_box_filter = pygame.image.load('Data/Images/text_box_filter.png')
text_box_img = pygame.image.load('Data/Images/text_box.png').convert()

particle_list = os.listdir('Data/Images/Particles')
particle_database = {}
for particle in particle_list:
    if particle[-1] == 'g':
        img = pygame.image.load('Data/Images/Particles/' + particle).convert()
        img.set_colorkey((255,255,255))
        particle_database[particle] = img.copy()

player_dash_filter = pygame.image.load('Data/Images/vfx/player_filter.png').convert()

boss_eyes = pygame.image.load('Data/Images/eyes.png').convert()
boss_eyes.set_colorkey((255,255,255))
hand_img = pygame.image.load('Data/Images/hand.png').convert()
hand_img.set_colorkey((255,255,255))

knife_img = pygame.image.load('Data/Images/knife.png').convert()
knife_img.set_colorkey((255,255,255))
# Animations ------------------------------------------------- #
colorkey = (255,255,255)
player_idle = entities.animation([[0,10],[1,6],[2,10],[1,6]],'Data/Images/Player/Idle/',['loop'],colorkey)
player_eye = entities.animation([[0,60],[1,3],[2,3],[3,60],[2,3],[1,3]],'Data/Images/Player/Eye/',['loop'],colorkey)
crystal_main = entities.animation([[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3]],'Data/Images/Crystal/',['loop'],colorkey)
# Audio ------------------------------------------------------ #
next_sound = pygame.mixer.Sound('Data/SFX/Next.wav')
next_sound.set_volume(0.2)
text_fade_sound = pygame.mixer.Sound('Data/SFX/text_fade.wav')
text_fade_sound.set_volume(0.04)
ambience = pygame.mixer.Sound('Data/SFX/ambience.wav')
ambience.set_volume(0.8)
collect_sound = pygame.mixer.Sound('Data/SFX/collect.wav')
collect_sound.set_volume(0.09)
grass_0_sound = pygame.mixer.Sound('Data/SFX/grass_0.wav')
grass_0_sound.set_volume(0.3)
grass_1_sound = pygame.mixer.Sound('Data/SFX/grass_1.wav')
grass_1_sound.set_volume(0.3)
dash_sound = pygame.mixer.Sound('Data/SFX/dash.wav')
dropper_sound = pygame.mixer.Sound('Data/SFX/dropper.wav')
dropper_sound.set_volume(0.4)
beamer_sound = pygame.mixer.Sound('Data/SFX/beamer.wav')
beamer_sound.set_volume(0.8)
growl_sound = pygame.mixer.Sound('Data/SFX/growl.wav')
growl_sound.set_volume(0.6)
# Colors ----------------------------------------------------- #
SKY = (24,36,56)
TEXT_BOX = (67,77,109)
# Variables -------------------------------------------------- #
scroll_x = 0
scroll_y = 0
Right = False
Left = False
gravity = 4
x_movement = 0
SPEED_CAP = 5
shards_collected = 0
stamina = 100
Boosting = False
crystal = [100,100,0,0,0] # x, y, key, x_momentum, y_momentum
particles = []
show_text = ['Hey! Listen! Are you new around here?                                                   (press x)',70,[0,0],'crystal'] # message, timer, target, source
text_queue = ['Haha, just kidding, someone told me you were looking for an ancient temple with super rare artifacts in it.','Oh, was that supposed to be a secret?','Whatever, I can help you with that if you want. I don\'t do much else.','I\'m Crystal by the way.','You probably have no idea what you\'re doing... Let me help you with that. Use the arrow keys to move.','You can also use x to boost yourself upward. You can\'t do it forever though, watch your stamina on the top left of the screen.']
LEVEL = 1
DEATHS = 0
just_died = False
knives = []
shards_gained = 0
white_screen = False
sky_lines = []
# Setup ------------------------------------------------------ #
player_dir = 'r'
player = entities.entity(112,110,15,24)
player_animation_keys = [0,0]
player_animation_keys[0] = player_idle.start(player.x,player.y)
player_animation_keys[1] = player_eye.start(player.x,player.y)
player_particles = ['green1x1.png','lightgreen1x1.png']
dash = [None,0]

crystal[2] = crystal_main.start(crystal[0],crystal[1])
crystal_particles = ['blue1x1.png','lightblue1x1.png']
show_text[2] = [crystal[0],crystal[1]]

tree_particles = ['green1x1.png','bluegreen1x1.png','bluegreen1x1.png','green2x2_0.png','green2x2_1.png']

hand_particles = ['red1x1.png','light_red1x1.png','red1x1.png','dark_red1x1.png','dark_red1x1.png','dark_red1x1.png','dark_red1x1.png','dark_red1x1.png','dark_red1x1.png']

tile_map,pushables,spawn,shards,enemies,boosts,void_level = load_map('level_' + str(LEVEL))
player.x = spawn[0]
player.y = spawn[1]
level_timer = 0
end_level = 0
knives = []
hands = []

special_events = ['shard_assist','you_dumb','stop_please','stuck_level_2','ant','stuck_level_4']
level_text = {2:['I\'m not sure if you remember, but you can use C while moving to dash.'],
              3:['tnone','...','Stop, you don\'t know-','tcrystal','Hey look at that, the spirits of the temple are trying to talk to you. I guess they don\'t want you taking those artifacts.','Oh right, you didn\'t want me to talk about that.','I\'ll keep quiet now.'],
              4:['Look at that, the spirits have sent weird flying thingies to stop you.','Dashing would probably be useful here.'],
              5:['Wow, that\'s actually a lot less droppers than I expected.','These spirits are weak.','Or...','They have no friends.'],
              6:['Okay, when you take those beamers into consideration, it seems like the spirits of the temple REALLY want you dead.','There are the knives too I guess.'],
              7:['tnone','...','You\'re making a hu-','tcrystal','Those spirits are so power hungry. They know that if you take their artifacts, they\'ll lose their power while you become more powerful than they ever were.','...','I think I heard that those green blobs will fill you with energy.','Hurry up, we need to get all these blue thingies before the spirits can stop us.'],
              8:['After this area, we should have enough to get into the temple.'],
              9:['...','tboss','You unwittingly took an entity from below with you to acquire the shards of power.','You\'ll never get those artifacts!','Prepare for your eternal torment...','DIE'],
              10:['...','tnone','Made for Ludum Dare 40 compo(48 hours).','Made by DaFluffyPotato','Follow me on twitter (DaFluffyPotato)','Itch.io page: cmlsc.itch.io']}

n = 0
for pushable in pushables:
    pushables[n] = [entities.entity(pushable[1],pushable[2],16,16),pushable[0]]
    n += 1

pygame.mixer.music.load('Data/Music/main_2.wav')
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)
ambience.play(-1)
# Loop ------------------------------------------------------- #
while True:
    # Background --------------------------------------------- #
    Display.fill(SKY)
    if LEVEL == 9:
        Display.fill((0,0,0))
        Display.blit(boss_eyes,(216,123))
        if random.randint(1,5) == 1:
            if random.randint(1,2) == 1:
                particles.append([scroll_x+216+random.randint(0,17),scroll_y+136,'dark_red1x1.png',[0,0.125],random.randint(90,170),[scroll_x,scroll_y]])
            else:
                particles.append([scroll_x+243+random.randint(0,17),scroll_y+136,'dark_red1x1.png',[0,0.125],random.randint(90,170),[scroll_x,scroll_y]])
    screenR = pygame.Rect(scroll_x,scroll_y,480,280+48) # added 48 so it'll handle falling crates
    level_timer += 1
    kill = False
    # Sky Lines ---------------------------------------------- #
    color = (5,10,25)
    if LEVEL == 9:
        color = (63,39,49)
    for i in range(random.randint(1,2)):
        sky_lines.append([(scroll_x/2)+random.randint(0,540)-30,330,random.randint(8,40),random.randint(1,3)/2,color]) # x, y, size, speed, color
    for line in sky_lines:
        line[1] -= line[3]
        pos_y = int(line[1]-int(line[2]/2))
        if random.randint(1,6) == 1:
            line[2] -= 1
            if line[2] <= 0:
                sky_lines.remove(line)
                if LEVEL == 9:
                    for i in range(3):
                        particles.append([scroll_x+(line[0]-(scroll_x/2)),scroll_y+pos_y,'black4x4.png',[0,random.randint(0,100)/50-2],random.randint(20,60)])
        surf = pygame.Surface((1,line[2]))
        surf.fill(color)
        Display.blit(surf,(line[0]-(scroll_x/2),pos_y))
    # Particles ---------------------------------------------- #
    for particle in particles:
        # x, y, image_id, movement, time_left
        if particle[2] == 'black4x4.png':
            particle[0] += particle[3][0]
            particle[1] += particle[3][1]
            if len(particle) == 5:
                Display.blit(particle_database[particle[2]],(int(particle[0])-scroll_x,int(particle[1])-scroll_y))
            else:
                Display.blit(particle_database[particle[2]],(int(particle[0])-particle[5][0],int(particle[1])-particle[5][1]))
            particle[4] -= 1
            if particle[4] <= 0:
                particles.remove(particle)
    # Calculate Tiles ---------------------------------------- #
    active_tiles = []
    collision_tiles = []
    for y in range(24):
        for x in range(26):
            loc = str(x-2+int(scroll_x/23)) + ';' + str(y-2+int(scroll_y/16))
            if loc in tile_map:
                active_tiles.append(tile_map[loc])
                found = True
                for img in tile_map[loc][0]:
                    if img not in no_physics_tiles:
                        found = False
                if found == False:
                    collision_tiles.append([tile_map[loc][1]*23,tile_map[loc][2]*16,23,16])
    # Calculate Scroll --------------------------------------- #
    if end_level == 0:
        cam_dis_x = player.x-scroll_x-240
        cam_dis_y = player.y-scroll_y-140
        if abs(cam_dis_x) < 15:
            cam_dis_x = 0
        if abs(cam_dis_y) < 15:
            cam_dis_y = 0
        scroll_x += cam_dis_x/25
        scroll_y += cam_dis_y/25
    # Background Tiles --------------------------------------- #
    for tile in active_tiles:
        for img in tile[0]:
            if img in background_tiles:
                if img[:5] != 'grass':
                    Display.blit(tile_database[img],(tile[1]*23-scroll_x,tile[2]*16-scroll_y))
                else:
                    Display.blit(tile_database[img],(tile[1]*23-scroll_x,tile[2]*16-2-scroll_y))
                if img in ['tree_2.png','tree_3.png']:
                    if random.randint(1,60) == 1:
                        particles.append([tile[1]*23+random.randint(0,15),tile[2]*16+random.randint(0,3),random.choice(tree_particles),[random.randint(0,10)/100,0.2],random.randint(100,300)])
    # Player ------------------------------------------------- #
    if player.obj.rect.colliderect(screenR):
        on_screen = True
    else:
        on_screen = False
    stamina += 0.15
    if stamina > 10:
        stamina += 0.25
    if stamina > 100:
        stamina = 100
    pushables_active = []
    collision_tiles_main = collision_tiles.copy()
    for pushable in pushables:
        pushables_active.append(pushable[0])
        collision_tiles_main.append(pushable[0].obj.CollisionItem())
    if Right == True:
        x_movement += 1.5
        if x_movement > SPEED_CAP:
            x_movement = SPEED_CAP
    if Left == True:
        x_movement -= 1.5
        if x_movement < -SPEED_CAP:
            x_movement = -SPEED_CAP
    if x_movement > 0:
        player_dir = 'r'
    elif x_movement < 0:
        player_dir = 'l'
    x_movement = normalize(x_movement,1)
    bonus_movement = 0
    if dash[1] > 0:
        dash[1] -= 1
        if dash[0] == 'r':
            bonus_movement = 15*((8-dash[1])/8)
        if dash[0] == 'l':
            bonus_movement = -15*((8-dash[1])/8)
    if on_screen == True:
        collisions = player.move([0,int(gravity)],collision_tiles_main)
        if x_movement != 0:
            if collisions['bottom'] == True:
                if level_timer % 10 == 0:
                    random.choice([grass_0_sound,grass_1_sound]).play()
                    for i in range(random.randint(5,10)):
                        if player_dir == 'r':
                            particles.append([player.x,player.y+22,random.choice(tree_particles),[-(random.randint(0,75)/100),-(random.randint(0,50)/100)],random.randint(7,20)])
                        else:
                            particles.append([player.x+14,player.y+22,random.choice(tree_particles),[(random.randint(0,75)/100),-(random.randint(0,50)/100)],random.randint(7,20)])
    if collisions['bottom'] == True:
        stamina += 2
    player.push([x_movement+bonus_movement,0],collision_tiles,pushables_active)
    gravity += 0.25
    if Boosting == True:
        if stamina >= 4:
            if gravity > 0:
                gravity = 0.25
                stamina -= 7
            gravity -= 1.25
            stamina -= 5
            if gravity < -4:
                gravity = -4
    if gravity > 4:
        gravity = 4
    player_idle.play(player_animation_keys[0],Display,False)
    player_eye.play(player_animation_keys[1],Display,False)
    player_main = player_idle.next_image(player_animation_keys[0])
    player_cosmetic = player_eye.next_image(player_animation_keys[1])
    player_surf = player_main.copy()
    player_surf.blit(player_cosmetic,(8,7))
    if player_dir == 'l':
        player_surf = pygame.transform.flip(player_surf,True,False)
    Display.blit(player_surf,(player.x-scroll_x,player.y-scroll_y))
    c = 0
    if player_dir == 'l':
        c = -2
    particles.append([player.x+7+random.randint(0,2)+c,player.y+15+random.randint(0,2),random.choice(player_particles),[(random.randint(0,65)/100-0.325),(random.randint(0,100)/100)],random.randint(5,10)])
    if dash[1] > 0:
        try:
            if dash[0] == 'r':
                Display = vfx.blur(Display.copy(),player_dash_filter,player.x-scroll_x,player.y-scroll_y,[-(abs(x_movement+bonus_movement)/2),0],[0,0])
            if dash[0] == 'l':
                Display = vfx.blur(Display.copy(),player_dash_filter,player.x-scroll_x,player.y-scroll_y,[abs(x_movement+bonus_movement)/2,0],[0,0])
        except:
            pass
    if player.y > void_level:
        kill = True
    # Dialogue Triggers -------------------------------------- #
    if LEVEL == 1:
        if 'shard_assist' in special_events:
            if player.x > 300:
                if player.y < 75:
                    text_queue.append('You need to get those blue things to open up the temple.')
                    text_queue.append('I\'ll show you where the temple is once we get enough to get inside. Just don\'t do anything stupid like jump off the edge.')
                    special_events.remove('shard_assist')
        if 'you_dumb' in special_events:
            if kill == True:
                if DEATHS == 0:
                    text_queue.append('Wow, you aren\'t very smart. Just get the blue thing...')
                    special_events.remove('you_dumb')
        if 'stop_please' in special_events:
            if kill == True:
                if DEATHS == 2:
                    text_queue.append('Can you please stop doing that? We have things to do... Places to be...')
                    special_events.remove('stop_please')
    if LEVEL == 2:
        if 'stuck_level_2' in special_events:
            if level_timer > 600:
                if player.x < 200:
                    text_queue.append('Uh...')
                    text_queue.append('Did you not see that island to the right?')
                    special_events.remove('stuck_level_2')
    if LEVEL == 3:
        if 'ant' in special_events:
            if level_timer > 600:
                if player.x > spawn[0]+50:
                    if collisions['bottom'] == True:
                        text_queue.append('Hey look! An ANT!')
                        text_queue.append('You like never see those around here.')
                        text_queue.append('...')
                        text_queue.append('Did you really think I meant I\'d stay quiet and not talk?')
                        text_queue.append('I meant talking about the thing.')
                        text_queue.append('Duh.           ')
                        special_events.remove('ant')
    if LEVEL == 4:
        if 'stuck_level_4' in special_events:
            if level_timer > 750:
                if player.y > 0:
                    if collisions['bottom'] == True:
                        text_queue.append('Tapping X periodically in air to boost upward is more effective than holding X down. Also, using the box is probably a good idea.')
                        special_events.remove('stuck_level_4')
    # Pushables ---------------------------------------------- #
    for pushable in pushables:
        if pushable[0].obj.rect.colliderect(screenR):
            temp_collisions = collision_tiles.copy()
            for pushable2 in pushables_active:
                if pushable2.ID != pushable[0].ID:
                    temp_collisions.append(pushable2.obj.CollisionItem())
            pushable[0].move([0,4],temp_collisions)
            Display.blit(tile_database[pushable[1]],(pushable[0].x-scroll_x,pushable[0].y-scroll_y))
    # Tiles -------------------------------------------------- #
    for tile in active_tiles:
        for img in tile[0]:
            if img not in background_tiles:
                if img[:5] != 'grass':
                    Display.blit(tile_database[img],(tile[1]*23-scroll_x,tile[2]*16-scroll_y))
                else:
                    Display.blit(tile_database[img],(tile[1]*23-scroll_x,tile[2]*16-2-scroll_y))
    # Particles ---------------------------------------------- #
    for particle in particles:
        # x, y, image_id, movement, time_left
        if particle[2] != 'black4x4.png':
            particle[0] += particle[3][0]
            particle[1] += particle[3][1]
            if len(particle) == 5:
                Display.blit(particle_database[particle[2]],(int(particle[0])-scroll_x,int(particle[1])-scroll_y))
            else:
                Display.blit(particle_database[particle[2]],(int(particle[0])-particle[5][0],int(particle[1])-particle[5][1]))
            particle[4] -= 1
            if particle[4] <= 0:
                particles.remove(particle)
    # Shards ------------------------------------------------- #
    for shard in shards:
        shard[2] += 1
        if shard[2] == 60:
            shard[2] = 0
        if shard[2] < 30:
            Display.blit(tile_database['shards.png'],(shard[0]-scroll_x,shard[1]-scroll_y-3+int(shard[2]/10)))
        else:
            Display.blit(tile_database['shards.png'],(shard[0]-scroll_x,shard[1]-scroll_y-int((shard[2]-30)/10)))
        if random.randint(1,30) == 1:
            particles.append([shard[0]+random.randint(10,12),shard[1]+7,random.choice(crystal_particles),[0,(random.randint(0,10)/100)],random.randint(90,120)])
        shardR = pygame.Rect(shard[0]+7,shard[1]+6,4,5)
        if player.obj.rect.colliderect(shardR):
            if LEVEL == 9:
                if show_text[0] != level_text[9][0]:
                    collect_sound.play()
            else:
                collect_sound.play()
            shards.remove(shard)
            shards_collected += 1
            shards_gained += 1
    if shards == []: # level completed if this evaluates to true
        if end_level == 0:
            end_level = 1
    if end_level > 0:
        end_level += 1
        scroll_x += end_level*2
        if end_level > 30:
            shards_gained = 0
            scroll_y = 0
            end_level = 0
            level_timer = 0
            scroll_x = 5000
            LEVEL += 1
            if LEVEL != 10:
                pushables = []
                knives = []
                tile_map,pushables,spawn,shards,enemies,boosts,void_level = load_map('level_' + str(LEVEL))
                player.set_pos(spawn[0],spawn[1])
                stamina = 100
                movement_x = 0
                n = 0
                show_text = ['',70,[0,0],'crystal']
                for pushable in pushables:
                    pushables[n] = [entities.entity(pushable[1],pushable[2],16,16),pushable[0]]
                    n += 1
                if LEVEL == 9:
                    shards_collected = 0
                    white_screen = True
                    pygame.mixer.music.stop()
                    ambience.fadeout(1000)
            else:
                white_screen = True
                shards = [[0,0,0]]
            for message in level_text[LEVEL]:
                text_queue.append(message)
            if LEVEL == 2:
                if 'you_dumb' not in special_events:
                    text_queue.append('Although, considering that you were jumping of the edge earlier, I\'m guessing you don\'t remember.')
    # Boosts ------------------------------------------------- #
    for boost in boosts:
        Display.blit(tile_database[boost[0]],(boost[1]-scroll_x,boost[2]-scroll_y))
        boostR = pygame.Rect(boost[1]+7,boost[2]+2,5,10)
        if player.obj.rect.colliderect(boostR):
            boosts.remove(boost)
            stamina = 100
    # Enemies ------------------------------------------------ #
    for enemy in enemies:
        if enemy[0] == 'dropper.png':
            Display.blit(tile_database[enemy[0]],(enemy[1]-scroll_x,enemy[2]-scroll_y))
            if player_dir == 'r':
                c = 10
            if player_dir == 'l':
                c = -2
            dis = abs(player.x+c-enemy[1])
            dis_y = abs(player.y-enemy[2])
            true_dis = player.x-enemy[1]
            if dis_y < 200:
                if dis < 110:
                    if player.x+c < enemy[1]:
                        if dis > 5:
                            enemy[1] -= 2
                            if enemy[1] < enemy[4][0]-100:
                                enemy[1] = enemy[4][0]-99
                    if player.x+c > enemy[1]:
                        if dis > 5:
                            enemy[1] += 2
                            if enemy[1] > enemy[4][0]+100:
                                enemy[1] = enemy[4][0]+99
                enemy[3] += 1
                if enemy[3] == 40:
                    if LEVEL != 9:
                        dropper_sound.play()
                    elif show_text[0] == '':
                        dropper_sound.play()
                    knives.append([enemy[1]+3,enemy[2]+5,])
                    enemy[3] = 0
        elif enemy[0] == 'beamer.png':
            Display.blit(tile_database[enemy[0]],(enemy[1]-scroll_x,enemy[2]-scroll_y))
            dis = abs(player.x-enemy[1])
            dis_y = abs(player.y+12-enemy[2])
            true_dis = player.x-enemy[1]
            if dis < 220:
                enemy[3] += 1
                if enemy[3] <= 100:
                    if dis_y < 100:
                        if dis < 220:
                            if player.y+12 < enemy[2]:
                                if dis_y > 5:
                                    enemy[2] -= 1
                                    if enemy[2] < enemy[4][1]-100:
                                        enemy[2] = enemy[4][1]-100
                            if player.y+12 > enemy[2]:
                                if dis_y > 5:
                                    enemy[2] += 1
                                    if enemy[2] > enemy[4][1]+100:
                                        enemy[2] = enemy[4][1]+100
                if enemy[3] > 100:
                    closest = 500
                    if true_dis < 0:
                        laserR = pygame.Rect(enemy[1]-496,enemy[2]+2,500,3)
                    if true_dis > 0:
                        laserR = pygame.Rect(enemy[1]+6,enemy[2]+2,500,3)
                    for tile in collision_tiles_main:
                        tileR = pygame.Rect(tile[0],tile[1],tile[2],tile[3])
                        if laserR.colliderect(tileR):
                            dis_x = 501
                            if true_dis > 0:
                                dis_x = tile[0]-(enemy[1]+6)
                            if true_dis < 0:
                                dis_x = (enemy[1]+6)-(tile[0]+tile[2])-2
                            if dis_x < closest:
                                closest = dis_x
                                
                    if enemy[3] <= 145:
                        if true_dis < 0:
                            pygame.draw.line(Display,(143,52,63),(enemy[1]+4-scroll_x,enemy[2]+3-scroll_y),(enemy[1]-496-scroll_x,enemy[2]+3-scroll_y))
                        if true_dis > 0:
                            pygame.draw.line(Display,(143,52,63),(enemy[1]+6-scroll_x,enemy[2]+3-scroll_y),(enemy[1]+506-scroll_x,enemy[2]+3-scroll_y))
                if enemy[3] == 145:
                    if LEVEL != 9:
                        beamer_sound.play()
                    elif show_text[0] == '':
                        beamer_sound.play()
                if enemy[3] > 145:
                    laser_surf = pygame.Surface((abs(closest),3))
                    laser_surf.fill((143,52,63))
                    for i in range(int(closest/10)):
                        start_x = random.randint(0,closest-1)
                        start_y = random.randint(0,2)
                        pygame.draw.line(laser_surf,(223,65,74),(start_x,start_y),(start_x+random.randint(3,8),start_y))
                    if true_dis < 0:
                        laserR = pygame.Rect(enemy[1]-496+(500-closest),enemy[2]+2,closest,3)
                        Display.blit(laser_surf,(enemy[1]-496-scroll_x+(500-closest),enemy[2]+2-scroll_y))
                    if true_dis > 0:
                        laserR = pygame.Rect(enemy[1]+6,enemy[2]+2,closest,3)
                        Display.blit(laser_surf,(enemy[1]+6-scroll_x,enemy[2]+2-scroll_y))
                    if true_dis != 0:
                        if laserR.colliderect(player.obj.rect):
                            kill = True
                if enemy[3] == 160:
                    enemy[3] = 0
    # Knives ------------------------------------------------- #
    for knife in knives:
        Display.blit(knife_img,(knife[0]-scroll_x,knife[1]-scroll_y))
        knifeR = pygame.Rect(knife[0],knife[1],4,9)
        for tile in collision_tiles_main:
            tileR = pygame.Rect(tile[0],tile[1],tile[2],tile[3])
            if tileR.colliderect(knifeR):
                try:
                    knives.remove(knife)
                except:
                    pass
        if knifeR.colliderect(player.obj.rect):
            kill = True
        knife[1] += 5
        if knife[1] > void_level+100:
            try:
                knives.remove(knife)
            except:
                pass
    # Crystal ------------------------------------------------ #
    if LEVEL != 9:
        dis_x = player.x+random.randint(0,150)-crystal[0]-70
        dis_y = player.y+random.randint(0,150)-crystal[1]-65
        if abs(dis_x) < 30:
            crystal[3] = normalize(crystal[3],1)
        else:
            rate_x = dis_x/(abs(dis_x)+abs(dis_y))
            crystal[3] += (dis_x/50)*abs(rate_x)
        if abs(dis_y) < 30:
            crystal[4] = normalize(crystal[4],1)
        else:
            rate_y = dis_y/(abs(dis_x)+abs(dis_y))
            crystal[4] += (dis_y/50)*abs(rate_y)
        crystal[3] = cap(crystal[3],8)
        crystal[4] = cap(crystal[4],8)
        crystal[0] += int(crystal[3])
        crystal[1] += int(crystal[4])
        crystal_main.move(crystal[2],crystal[0]-scroll_x,crystal[1]-scroll_y)
        crystal_main.play(crystal[2],Display)
        particles.append([crystal[0]+random.randint(0,3),crystal[1]+3,random.choice(crystal_particles),[0,(random.randint(0,50)/100)],random.randint(1,60)])
        if show_text[3] == 'crystal':
            show_text[2] = [crystal[0]-scroll_x+1,crystal[1]-scroll_y+2]
    # Hands -------------------------------------------------- #
    if LEVEL == 9:
        if len(hands) < 2:
            if random.randint(1,120) == 1:
                if random.randint(1,2) == 1:
                    hands.append([scroll_x + 490,player.y-random.randint(0,20),'l'])
                else:
                    hands.append([scroll_x - 100,player.y-random.randint(0,20),'r'])
        for hand in hands:
            hand_copy = hand_img.copy()
            if hand[2] == 'r':
                hand_copy = pygame.transform.flip(hand_copy,True,False)
                hand[0] += 6
                if hand[0] > scroll_x+530:
                    hands.remove(hand)
            else:
                hand[0] -= 6
                if hand[0] < scroll_x-100:
                    hands.remove(hand)
            handR = pygame.Rect(hand[0],hand[1],63,35)
            if player.obj.rect.colliderect(handR):
                kill = True
            Display.blit(hand_copy,(hand[0]-scroll_x,hand[1]-scroll_y))
            for i in range(30):
                particles.append([hand[0]+32+random.randint(0,5),hand[1]+random.randint(7,28),random.choice(hand_particles),[0,random.randint(0,50)/100-0.25],random.randint(1,30)])
            for i in range(10):
                particles.append([hand[0]+32+random.randint(0,5),hand[1]+random.randint(0,35),random.choice(hand_particles),[0,random.randint(0,100)/100-0.5],random.randint(1,30)])
    # White Screen ------------------------------------------- #
    if white_screen == True:
        Display.fill((255,255,255))
        if show_text[0] == '':
            if text_queue == []:
                white_screen = False
                if LEVEL == 10:
                    pygame.quit()
                    sys.exit()
    if (kill == True) or (just_died == True):
        if shards != []:
            if show_text[0] != level_text[9][0]:
                Display.fill((0,0,0))
                Display.blit(boss_eyes,(216,123))
    # GUI ---------------------------------------------------- #
    stamina_copy = stamina_img.copy()
    if stamina < 100:
        if stamina < 0:
            stamina = 0
        clip_out = pygame.Surface((100-int(stamina),10))
        stamina_copy.blit(clip_out,(1+int(stamina),1))
        stamina_copy.set_colorkey((0,0,0))

    if white_screen == False:
        Display.blit(stamina_copy,(2,2))
        Display.blit(tile_database['shards.png'],(-6,19))
    
    ShowText(str(shards_collected),11,22,1,380,Font_1,Display)

    if show_text[0] != '':
        show_text[1] += 6
    else:
        show_text[1] -= 6
    if show_text[1] > 350:
        show_text[1] = 350
    if show_text[1] < 70:
        show_text[1] = 70
    if show_text[1] != 70:
        text_box_copy = text_box_img.copy()
        if show_text[3] == 'boss':
            text_box_copy.set_colorkey((67,77,109))
            red_surf = pygame.Surface((400,75))
            red_surf.fill((63,39,49))
            red_surf.blit(text_box_copy,(0,0))
            text_box_copy = red_surf.copy()
        paste_surf = pygame.Surface((8,1))
        paste_surf.fill((255,255,255))
        for y in range(75):
            for x in range(50):
                color = text_box_filter.get_at((x*8,y))
                if color[0] > show_text[1]:
                    text_box_copy.blit(paste_surf,(x*8,y))
        text_box_copy.set_colorkey((255,255,255))
        Display.blit(text_box_copy,(40,200))
        if show_text[1] > 150:
            dis_x = show_text[2][0]-80
            dis_y = show_text[2][1]-200
            if on_screen == True:
                if show_text[3] == 'crystal':
                    pygame.draw.polygon(Display,TEXT_BOX,([70,200],[dis_x/3+80,dis_y/3+200],[90,200]),0)
            if int(len(show_text[0])*((show_text[1]-150)/200)) == len(show_text[0]):
                if show_text[0][-1] == '-':
                    show_text[0] = ''
                    show_text[1] = 155
            used_font = Font_1.copy()
            if show_text[3] == 'none':
                used_font = Font_0.copy()
            if show_text[3] == 'boss':
                used_font = Font_2.copy()
            ShowText(show_text[0][:int(len(show_text[0])*((show_text[1]-150)/200))],50,206,1,380,used_font,Display)
    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RIGHT:
                Right = True
            if event.key == K_LEFT:
                Left = True
            if event.key == ord('x'):
                if show_text[0] == '':
                    Boosting = True
                elif show_text[1] >= 155:
                    next_sound.play()
                    show_text[0] = ''
                    if show_text[1] > 155:
                        show_text[1] = 155
                    if text_queue == []:
                        text_fade_sound.play()
            if event.key == ord('c'):
                if stamina >= 10:
                    if x_movement != 0:
                        dash_sound.play()
                        stamina -= 10
                        if x_movement > 0:
                            dash = ['r',8]
                        if x_movement < 0:
                            dash = ['l',8]
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                Right = False
            if event.key == K_LEFT:
                Left = False
            if event.key == ord('x'):
                Boosting = False
    # Manage Text Queue -------------------------------------- #
    while (show_text[0] == '') and (text_queue != []):
        if text_queue[0] == 'tcrystal':
            show_text[3] = 'crystal'
        elif text_queue[0] == 'tnone':
            show_text[3] = 'none'
        elif text_queue[0] == 'tboss':
            show_text[3] = 'boss'
        else:
            show_text[0] = text_queue[0]
            if show_text[0] == level_text[9][2]:
                pygame.mixer.music.load('Data/Music/boss.wav')
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
        text_queue.remove(text_queue[0])
    # Die ---------------------------------------------------- #
    just_died = False
    if LEVEL == 10:
        kill = False
    if kill == True:
        if show_text[0] != level_text[9][0]:
            growl_sound.play()
        particles = []
        hands = []
        Right = False
        Left = False
        shards_collected -= shards_gained
        shards_gained = 0
        pushables = []
        tile_map,pushables,spawn,shards,enemies,boosts,void_level = load_map('level_' + str(LEVEL))
        player.set_pos(spawn[0],spawn[1])
        knives = []
        stamina = 100
        movement_x = 0
        n = 0
        for pushable in pushables:
            pushables[n] = [entities.entity(pushable[1],pushable[2],16,16),pushable[0]]
            n += 1
        DEATHS += 1
        just_died = True
    # Update ------------------------------------------------- #
    screen.blit(pygame.transform.scale(Display,(480*2,280*2)),(0,0))
    pygame.display.update()
    mainClock.tick(40)
    
