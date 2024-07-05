import pygame, sys, random

########
# Appearance
########
window_width = 550
window_height = 650

pink = '#EF7C8E' # cross
cream = '#F6ECE7' # background #FAE8E0
spearmint = '#B6E2D3' # circle
rosewater = '#D8A7B1' # grid
rosewater_light = '#EBD3D8' # button when hover
rosewater_dark = '#BC8892' # button shadow, playboard grid, text
rosewater_dark_alt = '#997078' # winning animation

########
# Classes
########
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
                    self.onclickFunction()
                    self.pressed = False

# button code from:
# https://pythonprogramming.sssaltervista.org/buttons-in-pygame/?doing_wp_cron=1685564739.9689290523529052734375
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
            self.top_color = rosewater_light
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.onclickFunction()
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = rosewater

########
# Functions
########
#### onClickFunctions
def play():
    global board, turn, started, player, against_ai
    mouse_pos = pygame.mouse.get_pos()
    index = -1
    if started:
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
    if index >= 0:
        if isinstance(board[index], int):
            pygame.draw.rect(screen, cream, pygame.Rect(0, 0, 550, 130))
            play_player_animation(index, player)
            board[index] = player
            turn += 1
            if against_ai:
                ai_player = 'X' if player == 'O' else 'O'
                ai_play(ai_player)
    return

def ai_play(ai_player):
    global board, turn
    if win():
        return
    try:
        pygame.draw.rect(screen, cream, pygame.Rect(0, 0, 550, 130))
        # ai_player = player
        ai_index = ai_move()
        play_player_animation(ai_index, ai_player)
        board[ai_index] = ai_player
        turn += 1
    except KeyError:
        return

def play_player_animation(index, player):
    global players, locations, cross, circle, locations, board
    # draw already played slots, repeated from main(). Somehow has to repeat here otherwise already played slots will randomly not show when playing player animation
    for i in range(9):
        if board[i] == 'X':
            screen.blit(cross, locations[i])
        elif board[i] == 'O':
            screen.blit(circle, locations[i])
    # play first frame
    screen.blit(players[player][0], locations[index])
    pygame.display.flip()
    # play other frames
    start_time = pygame.time.get_ticks()
    delay = 75
    delay_count = 0
    while True:
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= delay:
            if delay_count > 2: # delay three times
                break
            pygame.draw.rect(screen, cream, pygame.Rect(locations[index][0], locations[index][1], 150, 150))
            screen.blit(players[player][delay_count+1], locations[index])
            pygame.display.flip()
            delay_count += 1
            start_time = pygame.time.get_ticks()

def start():
    global started, turn
    draw_board()
    started = True
    pygame.draw.rect(screen, cream, pygame.Rect(0, 0, 550, 130))

def start_ai():
    global started, turn, against_ai
    draw_board()
    against_ai = True
    started = True
    pygame.draw.rect(screen, cream, pygame.Rect(0, 0, 550, 130))

def clear():
    global board, turn, iter
    board = [0,1,2,3,4,5,6,7,8]
    turn = 0
    iter = 1
    start()

#### other gameplay functions
def draw_board():
    board = pygame.Rect(30, 130, 490, 490)
    pygame.draw.rect(screen, rosewater, board)

# win returns the index+1 of winning pattern if wins (which will be 'true' when checking if win() later), otherwise return false (+1 to handle the first index being zero == false)
def win():
    global board, all_win_combos
    for win_pattern in all_win_combos:
        if board[win_pattern[0]] == board[win_pattern[1]] == board[win_pattern[2]] == 'O' or board[win_pattern[0]] == board[win_pattern[1]] == board[win_pattern[2]] == 'X':
            return all_win_combos.index(win_pattern) + 1
    return False

def play_winning_animation(index):
    global winning_frames, iter
    if iter > 1:
        screen.blit(winning_frames[index][3], (40,140))
        pygame.display.flip()
    else:
        screen.blit(winning_frames[index][0], (40,140))
        pygame.display.flip()
        start_time = pygame.time.get_ticks()
        delay = 50
        delay_count = 0
        while True:
            current_time = pygame.time.get_ticks()
            if current_time - start_time >= delay:
                if delay_count > 2: # delay three times
                    iter += 1
                    break
                screen.blit(winning_frames[index][delay_count+1], (40,140))
                pygame.display.flip()
                delay_count += 1
                start_time = pygame.time.get_ticks()

def ai_move():
    global board, all_win_combos, player
    threat = {}
    about_win = {}
    for win_pattern in all_win_combos:
        this_threat = 0
        this_win = 0
        for i in win_pattern:
            if board[i] == player:
                this_threat += 1
            elif board[i] == 'X' if player == 'O' else 'O':
                this_win += 1
        try:
            threat[this_threat].append(win_pattern)
        except KeyError:
            threat[this_threat] = [win_pattern]
        try:
            about_win[this_win].append(win_pattern)
        except KeyError:
            about_win[this_win] = [win_pattern]
    if 2 in about_win:
        random.shuffle(about_win[2])
        for pt in about_win[2]:
            for p in pt:
                try:
                    int(board[p])
                    return p
                except ValueError:
                    continue
    for l in [2,1]:
        if l in threat:
            random.shuffle(threat[l])
            for pt in threat[l]:
                for p in pt:
                    try:
                        int(board[p])
                        return p
                    except ValueError:
                        continue
    return random.choice(board)

########
# Main game
########
def main():
    global screen, icon, clock, button_font
    global board, turn, started, iter, locations, players, player, all_win_combos, winning_frames, circle, cross, against_ai
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('TicTacToe Lite')
    screen.fill(cream)
    button_font = pygame.font.Font(None,28)
    text_font = pygame.font.Font(None,50)

    # manage double esc quit
    esc_pressed = False
    last_esc_time = 0
    double_esc_time = 500  # milliseconds

    # game attributes
    board = [0,1,2,3,4,5,6,7,8]
    turn = 0
    against_ai = False
    started = False
    iter = 1
    all_win_combos = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    locations = {0:(40, 140), 1:(200, 140), 2:(360, 140), 3:(40, 300), 4:(200, 300), 5:(360, 300), 6:(40, 460), 7:(200, 460), 8:(360, 460)}

    # images and animation frames
    cross = pygame.transform.scale(pygame.image.load('assets/cross-4.png'),(150,150))
    circle = pygame.transform.scale(pygame.image.load('assets/circle-4.png'),(150,150))
    cross_icon = pygame.transform.scale(pygame.image.load('assets/cross-4.png'),(50,50))
    circle_icon = pygame.transform.scale(pygame.image.load('assets/circle-4.png'),(50,50))
    players = {'X':[pygame.transform.scale(pygame.image.load('assets/cross-1.png'),(150,150)), pygame.transform.scale(pygame.image.load('assets/cross-2.png'),(150,150)), pygame.transform.scale(pygame.image.load('assets/cross-3.png'),(150,150)), pygame.transform.scale(pygame.image.load('assets/cross-4.png'),(150,150))], 'O':[pygame.transform.scale(pygame.image.load('assets/circle-1.png'),(150,150)), pygame.transform.scale(pygame.image.load('assets/circle-2.png'),(150,150)), pygame.transform.scale(pygame.image.load('assets/circle-3.png'),(150,150)), pygame.transform.scale(pygame.image.load('assets/circle-4.png'),(150,150))]}
    winning_frames = {0:[pygame.image.load('assets/win-1-'+str(i)+'.png') for i in range(1,5)], 1:[pygame.image.load('assets/win-2-'+str(i)+'.png') for i in range(1,5)], 2:[pygame.image.load('assets/win-3-'+str(i)+'.png') for i in range(1,5)], 3:[pygame.image.load('assets/win-4-'+str(i)+'.png') for i in range(1,5)], 4:[pygame.image.load('assets/win-5-'+str(i)+'.png') for i in range(1,5)], 5:[pygame.image.load('assets/win-6-'+str(i)+'.png') for i in range(1,5)], 6:[pygame.image.load('assets/win-7-'+str(i)+'.png') for i in range(1,5)], 7:[pygame.image.load('assets/win-8-'+str(i)+'.png') for i in range(1,5)]}

    # buttons
    start_button = Button('local play', 110, 25, (120, 75), 3, start)
    start_button_ai = Button('play against AI', 155, 25, (280, 75), 3, start_ai)
    restart_button = Button('another game', 150, 25, (200, 85), 3, clear)
    play_areas = [Playboard(150,150,location,play) for location in locations.values()]
    
    # main loop
    draw_board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # quit if esc key is pressed twice within double_esc_time (500ms)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esc_pressed = True
                    current_time = pygame.time.get_ticks()
                    if esc_pressed and (current_time - last_esc_time) < double_esc_time:
                        pygame.quit()
                        sys.exit()
                    esc_pressed = True
                    last_esc_time = current_time
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    esc_pressed = False
        # draw slots
        for area in play_areas:
            area.draw()
        # draw already played slots
        for i in range(9):
            if board[i] == 'X':
                screen.blit(cross, locations[i])
            elif board[i] == 'O':
                screen.blit(circle, locations[i])

        # manage buttons and messages
        if not started:
            message = text_font.render('Welcome to TicTacToe Lite!', True, rosewater_dark)
            screen.blit(message, message.get_rect(center = (275, 35)))
            start_button.draw()
            if not started:
                start_button_ai.draw()
        else:
            player = 'O' if turn%2 == 0 else 'X'
            message = text_font.render('Now playing:     ', True, rosewater_dark)
            screen.blit(message, message.get_rect(center = (275, 50)))
            screen.blit(circle_icon, (380, 27)) if player == 'O' else screen.blit(cross_icon, (380, 27))
            if win():
                # replace empty board with E-nd to prevent further playing
                board = ['E' if isinstance(item, int) else item for item in board] 
                # cover now playing text
                pygame.draw.rect(screen, cream, pygame.Rect(0, 0, 550, 130))
                # show win text and restart button
                screen.blit(circle_icon, (200, 17)) if player == 'X' else screen.blit(cross_icon, (200, 17)) # no longer needed in ai mode? --player == X instead of O because after the winning turn the turn turns once
                message = text_font.render('       wins!', True, rosewater_dark)
                screen.blit(message, message.get_rect(center = (275, 42)))
                restart_button.draw()
                # play winning animation
                if win() - 1 >= 0: # idk why but there is a frame after clicking another game when this still get run but win==0, so will mess up index when playing animation if don't check here
                    play_winning_animation(win() - 1)
                    iter += 1
            elif turn > 8:
                pygame.draw.rect(screen, cream, pygame.Rect(0, 0, 550, 130))
                message = text_font.render("It's a draw!", True, rosewater_dark)
                screen.blit(message, message.get_rect(center = (275, 42)))
                restart_button.draw()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()