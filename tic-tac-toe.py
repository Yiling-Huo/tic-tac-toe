import pygame

window_width = 550
window_height = 650

pink = '#EF7C8E' # cross
cream = '#F6ECE7' # background #FAE8E0
spearmint = '#B6E2D3' # circle
rosewater = '#D8A7B1' # grid
rosewater_dark = '#BC8892' # button shadow

def draw_board():
    board = pygame.Rect(30, 130, 490, 490)
    pygame.draw.rect(screen, rosewater, board)

# button code from:
# https://pythonprogramming.sssaltervista.org/buttons-in-pygame/?doing_wp_cron=1685564739.9689290523529052734375
class Playboard:
    def __init__(self,width,height,pos,onclickFunction=None):
        #Core attributes 
        self.pressed = False
        self.onclickFunction = onclickFunction
        self.y_pos = pos[1]

        # rectangle 
        self.rect = pygame.Rect(pos,(width,height))
        self.color = cream

    def draw(self):
        pygame.draw.rect(screen,self.color, self.rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    # print('click')
                    self.onclickFunction()
                    self.pressed = False

class Button:
    def __init__(self,text,width,height,pos,elevation,onclickFunction=None):
        #Core attributes 
        self.pressed = False
        self.onclickFunction = onclickFunction
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = rosewater

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = rosewater_dark
        #text
        self.text = text
        self.text_surf = button_font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = spearmint
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    # print('click')
                    self.onclickFunction()
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = rosewater

# onClickFunctions
def play():
    global board, turn, playing, player
    mouse_pos = pygame.mouse.get_pos()
    # print(mouse_pos)
    index = -1
    if playing:
        if mouse_pos[0] < 190:
            if mouse_pos[1] < 300:
                index = 0
            elif mouse_pos[1] > 310 and mouse_pos[1] < 460:
                index = 3
            elif mouse_pos[1] > 470:
                index = 6
        elif mouse_pos[0] > 200 and mouse_pos[0] < 350:
            if mouse_pos[1] < 300:
                index = 1
            elif mouse_pos[1] > 310 and mouse_pos[1] < 460:
                index = 4
            elif mouse_pos[1] > 470:
                index = 7
        elif mouse_pos[0] > 360:
            if mouse_pos[1] < 300:
                index = 2
            elif mouse_pos[1] > 310 and mouse_pos[1] < 460:
                index = 5
            elif mouse_pos[1] > 470:
                index = 8
        else:
            return
    else:
        return
    
    if isinstance(board[index], int):
        # player = 'O' if turn%2 == 0 else 'X'
        pygame.draw.rect(screen, cream, pygame.Rect(0, 0, 550, 130))
        play_animation(index, player)
        board[index] = player
        turn += 1

def play_animation(index, player):
    global players, locations
    screen.blit(players[player][0], locations[index])
    pygame.display.flip()
    start_time = pygame.time.get_ticks()
    delay = 75
    delay_count = 0
    while True:
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= delay:
            if delay_count > 1: # only need to delay twice
                break
            pygame.draw.rect(screen, cream, pygame.Rect(locations[index][0], locations[index][1], 150, 150))
            screen.blit(players[player][delay_count+1], locations[index])
            pygame.display.flip()
            delay_count += 1
            start_time = pygame.time.get_ticks()

def start():
    global playing
    playing = True
    pygame.draw.rect(screen, cream, pygame.Rect(0, 0, 550, 130))

def clear():
    global board, playing, turn
    playing = False
    board = [0,1,2,3,4,5,6,7,8]
    turn = 0
    start()

# game functions
def win():
    global board, all_win_combos
    for win_pattern in all_win_combos:
        if board[win_pattern[0]] == board[win_pattern[1]] == board[win_pattern[2]] and isinstance(board[win_pattern[0]], str):
            return True
    return False

def main():
    global screen, icon, clock, button_font
    global board, turn, playing, locations, players, player, all_win_combos
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('TicTacToe Lite')
    screen.fill(cream)
    button_font = pygame.font.Font(None,28)
    text_font = pygame.font.Font(None,50)

    # game 
    board = [0,1,2,3,4,5,6,7,8]
    turn = 0
    playing = False

    # player images
    cross = pygame.transform.scale(pygame.image.load('assets/cross-4.png'),(150,150))
    circle = pygame.transform.scale(pygame.image.load('assets/circle-4.png'),(150,150))
    cross_icon = pygame.transform.scale(pygame.image.load('assets/cross-4.png'),(50,50))
    circle_icon = pygame.transform.scale(pygame.image.load('assets/circle-4.png'),(50,50))

    # game basic info (best here or outside any loop?)
    locations = {0:(40, 140), 1:(200, 140), 2:(360, 140), 3:(40, 300), 4:(200, 300), 5:(360, 300), 6:(40, 460), 7:(200, 460), 8:(360, 460)}
    play_areas = [Playboard(150,150,location,play) for location in locations.values()]

    players = {'X':[pygame.transform.scale(pygame.image.load('assets/cross-1.png'),(150,150)), pygame.transform.scale(pygame.image.load('assets/cross-2.png'),(150,150)), pygame.transform.scale(pygame.image.load('assets/cross-3.png'),(150,150))], 'O':[pygame.transform.scale(pygame.image.load('assets/circle-1.png'),(150,150)), pygame.transform.scale(pygame.image.load('assets/circle-2.png'),(150,150)), pygame.transform.scale(pygame.image.load('assets/circle-3.png'),(150,150))]}

    all_win_combos = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

    # (re-)start buttons
    start_button = Button('start', 70, 25, (240, 75), 3, start)
    restart_button = Button('another game', 150, 25, (200, 85), 3, clear)
    
    # game loop
    draw_board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        for area in play_areas:
            area.draw()

        if not playing:
            message = text_font.render('Welcome to TicTacToe Lite!', True, rosewater_dark)
            screen.blit(message, message.get_rect(center = (275, 35)))
            start_button.draw()
        else:
            player = 'O' if turn%2 == 0 else 'X'
            message = text_font.render('Now playing:     ', True, rosewater_dark)
            screen.blit(message, message.get_rect(center = (275, 50)))
            screen.blit(circle_icon, (380, 27)) if player == 'O' else screen.blit(cross_icon, (380, 27))
            if win():
                pygame.draw.rect(screen, cream, pygame.Rect(0, 0, 550, 130))
                screen.blit(circle_icon, (200, 17)) if player == 'X' else screen.blit(cross_icon, (200, 17))
                message = text_font.render('       wins!', True, rosewater_dark)
                screen.blit(message, message.get_rect(center = (275, 42)))
                restart_button.draw()
            elif turn > 8:
                pygame.draw.rect(screen, cream, pygame.Rect(0, 0, 550, 130))
                message = text_font.render("It's a draw!", True, rosewater_dark)
                screen.blit(message, message.get_rect(center = (275, 42)))
                restart_button.draw()

        # draw already played slots
        for i in range(9):
            if board[i] == 'X':
                screen.blit(cross, locations[i])
            elif board[i] == 'O':
                screen.blit(circle, locations[i])
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()