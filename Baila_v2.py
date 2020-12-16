import pygame
import pygame_menu
import pygame.freetype
from random import choice

pygame.init()
surface = pygame.display.set_mode((1200, 900),pygame.RESIZABLE) #4:3
pygame.display.set_caption("Baila")

#värvid
charcoal = (21, 27, 31)
neon_orange = (253, 95, 0)

#kaardid on 585:850

def word_wrap(surf, text, font, color=(0, 0, 0)):
    """
    https://stackoverflow.com/questions/52197785/pygame-text-line-break
    """
    font.origin = True
    words = text.split(' ')
    width, height = surf.get_size()
    line_spacing = font.get_sized_height() + 2
    x, y = 300, line_spacing + (Y // 2 + 150)
    space = font.get_rect(' ')
    for word in words:
        bounds = font.get_rect(word)
        if x + bounds.width + bounds.x >= width-300:
            x, y = 300, y + line_spacing
        if x + bounds.width + bounds.x >= width-300:
            raise ValueError("word too wide for the surface")
        if y + bounds.height - bounds.y >= height:
            raise ValueError("text to long for the surface")
        font.render_to(surf, (x,y), None, color)
        x += bounds.width + space.width
    return x, y


def kaardi_pilt(a, scale): #a- kaardi nimi #scale - kaardi skaala(float)
    pilt = pygame.image.load(f"kaardid_pildid\{a}.png")
    pilt_kohandatud = pygame.transform.rotozoom(pilt, 0, scale)
    return pilt_kohandatud

def cards():
    """
    loeme kaardid_info'st reeglid ja loome sõnastiku, võtmeks kaardi nimi, 
    elemendiks selle kaardi reegel
    """
    fail = open("kaardid_info.txt", encoding='UTF-8')
    sõnastik = {}
    for rida in fail:
        a = rida.strip("\n").split("-")
        sõnastik[a[0]] = a[1]
    return sõnastik


def start_the_game():
    kaardid_sõnastik = cards()
    run = True
    mängitud = [] #list kuhu lähevad kaardid, mis juba loositud
    kaartide_arv = 4 * len(kaardid_sõnastik)
    
    surface.fill(my_theme.background_color)

    X = surface.get_width()
    Y = surface.get_height()
    
    surface.blit(kaardi_pilt("pack",0.5),(X // 2 - 400, Y // 2 - 400))
    uus_kaart = pygame.Rect((X // 2 - 400, Y // 2 - 400),(650*0.5,945*0.5))

    pygame.display.update()
    while run:
        X = surface.get_width()
        Y = surface.get_height()
        
        surface.fill(my_theme.background_color)
        surface.blit(kaardi_pilt("pack",0.5),(X // 2 - 400, Y // 2 - 400))
        uus_kaart = pygame.Rect((X // 2 - 400, Y // 2 - 400),(650*0.5,945*0.5))
        text_box = pygame.Rect((X // 2, Y // 2 + Y // 4),(600,400))

        font = pygame.freetype.SysFont('Impact', (X+Y)//100)
        
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
##            if event.type == pygame.VIDEORESIZE:
##                old_surface_saved = surface
##                surface = pygame.display.set_mode((X, Y),pygame.RESIZABLE)
##                # On the next line, if only part of the window
##                # needs to be copied, there's some other options.
##                surface.blit(old_surface_saved, (0,0))
##                del old_surface_saved
            
            if len(mängitud) == kaartide_arv:
                
                word_wrap(surface, "Kaardid otsas, mäng läbi", font, neon_orange)
                pygame.display.update()
                run = False
                
            if keys[pygame.K_1]:
                
                reegel_box = pygame.Rect((X // 2 + 100, Y // 2 - 400),(585*0.5,850*0.5))
                kaart = choice(list(kaardid_sõnastik.keys())) #valime suvalise kaardi
                while mängitud.count(kaart) == 4: #kui kaart on neli korda juba tõmmatud, siis seda enam ei tõmba, tõmbab teise kaardi
                    kaart = choice(list(kaardid_sõnastik.keys()))
                mängitud.append(kaart) # kaart läheb "maha"
                
                surface.blit(kaardi_pilt(kaart,0.5),(X // 2 + 100, Y // 2 - 400))
                pygame.display.update()
                pygame.time.wait(200)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if uus_kaart.collidepoint(event.pos): # kui vajutad kaardipaki peale
                    reegel_box = pygame.Rect((X // 2 + 100, Y // 2 - 400),(585*0.5,850*0.5))
                    
                    kaart = choice(list(kaardid_sõnastik.keys())) #valime suvalise kaardi
                    while mängitud.count(kaart) == 4: #kui kaart on neli korda juba tõmmatud, siis seda enam ei tõmba, tõmbab teise kaardi
                        kaart = choice(list(kaardid_sõnastik.keys()))
                    mängitud.append(kaart) # kaart läheb "maha"
                    
                    surface.blit(kaardi_pilt(kaart,0.5),(X // 2 + 100, Y // 2 - 400))
                    pygame.display.update()
                    pygame.time.wait(200)
                    
                if reegel_box.collidepoint(event.pos): #kui vajutad hetkel loositud kaardile
                    surface.blit(kaardi_pilt(kaart,0.5),(X // 2 + 100, Y // 2 - 400))
                    
                    reegel = kaardid_sõnastik[kaart]
                    word_wrap(surface, reegel,font, neon_orange)

                    
                    pygame.display.update()
                    pygame.time.wait(200)   

            if keys[pygame.K_ESCAPE]:
                run = False
            if keys[pygame.K_2]:
                surface.blit(kaardi_pilt(kaart,0.5),(X // 2 + 100, Y // 2 - 400))
                
                reegel = kaardid_sõnastik[kaart]
                word_wrap(surface, reegel,font, neon_orange)
                
                pygame.display.update()
                pygame.time.wait(100)
    menu.mainloop(surface)
    
def nupud(): #menüü, mis näitab, mis nupud mida teevad    
    run = True
    while run:
        
        X = surface.get_width()
        Y = surface.get_height()
        font = pygame.font.SysFont('Impact', (X+Y)//100)
        
        surface.fill(my_theme.background_color)
        
        text1 = font.render("1 - edasi", True, neon_orange, my_theme.background_color)
        textRect1 = text1.get_rect()
        textRect1.center = (X // 2, Y // 2 - 50)
        surface.blit(text1, textRect1)
        
        text2 = font.render("2 - reegel", True, neon_orange, my_theme.background_color)
        textRect2 = text2.get_rect()
        textRect2.center = (X // 2, Y // 2)
        surface.blit(text2, textRect2)
        
        text3 = font.render("ESCAPE - tagasi ", True, neon_orange, my_theme.background_color)
        textRect3 = text3.get_rect()
        textRect3.center = (X // 2, Y // 2 + 50)
        surface.blit(text3, textRect3)

        pygame.display.update()
        
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys[pygame.K_ESCAPE]:
                run = False
    menu.mainloop(surface)

my_theme = pygame_menu.themes.THEME_DARK.copy()
my_theme.title_background_color = (0, 0, 6)
my_theme.background_color = charcoal
my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
my_theme.widget_font = pygame_menu.font.FONT_HELVETICA
my_theme.widget_font_color = neon_orange

while True:
    X = surface.get_width()
    Y = surface.get_height()
    menu = pygame_menu.Menu(Y,X, 'Baila: The Game', theme = my_theme)

    menu.add_button('Alusta mängu', start_the_game)
    menu.add_button('Nupud', nupud)
    menu.add_button('Välju', pygame_menu.events.EXIT)

    menu.mainloop(surface)
