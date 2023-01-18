import pygame as py
from random import randint
import time
from user import User
import random

py.init()
dimensions = (width, height) = (700, 700)
screen = py.display.set_mode(dimensions)
font = py.font.Font('ARCADE_N.ttf', 32)
ifont = py.font.Font('ARCADE_N.ttf', 10)
users = []

global bgs 
bgs = ['bg/space.png', 
'bg/sky.png',
'bg/forest.png',
'bg/night.jpeg',
'bg/beach.png']
txt_colors = [py.Color("white"), py.Color("black"), py.Color("gray"), py.Color("white"), py.Color("black")]
button_txt_colors = [py.Color("black"), py.Color("black"), py.Color("black"), py.Color("black"), py.Color("black")]
pcolors = [py.Color("salmon"), (245, 217, 59), (245, 217, 59), py.Color("salmon"), (245, 217, 59)]
scolors = [py.Color("light salmon"), (250, 230, 122), (250, 230, 122), py.Color("light salmon"), (250, 230, 122)]
freeze_colors = [py.Color("light blue"), py.Color("dark blue"), py.Color("light blue"), py.Color("light blue"), py.Color("dark blue")]
greens = [py.Color("green"), py.Color("dark green"), py.Color("green"), py.Color("green"), py.Color("dark green")]
index = 0


def change_themes(index):
    global bg_path 
    bg_path = bgs[index]
    global txt_color
    txt_color = txt_colors[index]
    global button_txt_color 
    button_txt_color= button_txt_colors[index]
    global primary_color 
    primary_color = pcolors[index]
    global secondary_color 
    secondary_color = scolors[index]
    global freeze_color 
    freeze_color = freeze_colors[index]
    global green
    green = greens[index]

change_themes(index)

def update_users():
    with open('leaderboard.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            users.append(str_to_usr(line))
        f.close()

def str_to_usr(userstr):
    data = userstr.split(';*|')
    u = User(data[0])
    try:
        u.update_high_scores(int(data[1]), 1)
        u.update_high_scores(int(data[2]), 2)
        u.update_high_scores(int(data[3]), 3)
        return u
    except IndexError:
        return None

def usr_to_str(user: User):
    return user.name + ";*|" + str(user.es) + ";*|" + str(user.ms) + ";*|" + str(user.hs)

def main():
    clock = py.time.Clock()
    start = True
    scolor = primary_color
    qcolor = primary_color
    lcolor = primary_color
    tcolor = primary_color
    icolor = primary_color
    update_users()
    while start:      

        title_text = font.render('TIME CRUNCH', True, txt_color)
        textRect = title_text.get_rect()
        textRect.center = (width // 2, height // 10)

        start_text = font.render('START', True, button_txt_color)
        stextrect = start_text.get_rect()
        stextrect.center = (width // 2, height // 4)
        start_button = py.Rect(0, 0, 200, 60)
        start_button.center = (width // 2, height // 4)

        lb_text = font.render('LEADERBOARD', True, button_txt_color)
        lbtextrect = lb_text.get_rect()
        lbtextrect.center = (width // 2, height // 2.6)
        lb_button = py.Rect(0, 0, 400, 60)
        lb_button.center = (width // 2, height // 2.6)

        theme_text = font.render('CHANGE THEME', True, button_txt_color)
        theme_text_rect = theme_text.get_rect()
        theme_text_rect.center = (width // 2, height // 1.9)
        theme_button = py.Rect(0, 0, 400, 60)
        theme_button.center = (width // 2, height // 1.9)

        i_text = font.render('INSTRUCTIONS', True, button_txt_color)
        i_rect = i_text.get_rect()
        i_rect.center = (width // 2, height // 1.45)
        i_button = py.Rect(0, 0, 400, 60)
        i_button.center = (width // 2, height // 1.45)

        quit_text = font.render('QUIT', True, button_txt_color)
        qtextrect = quit_text.get_rect()
        qtextrect.center = (width // 2, height // 1.2)
        quit_button = py.Rect(0, 0, 200, 60)
        quit_button.center = (width // 2, height // 1.2)

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    start = False
                    break
            elif event.type == py.QUIT:
                exit()
            elif event.type == py.MOUSEMOTION:
                mpos = py.mouse.get_pos()
                if start_button.collidepoint(mpos): 
                    scolor = secondary_color 
                else:
                    scolor = primary_color
                if quit_button.collidepoint(mpos):
                    qcolor = secondary_color
                else:
                    qcolor = primary_color
                if lb_button.collidepoint(mpos):
                    lcolor = secondary_color
                else:
                    lcolor = primary_color
                if theme_button.collidepoint(mpos):
                    tcolor = secondary_color
                else:
                    tcolor = primary_color
                if i_button.collidepoint(mpos):
                    icolor = secondary_color
                else:
                    icolor = primary_color
            elif event.type == py.MOUSEBUTTONDOWN:
                if scolor == secondary_color:
                    name_input()
                    start = False
                    continue
                elif qcolor == secondary_color:
                    start = False
                    exit()
                    break
                elif lcolor == secondary_color:
                    level_select(None)
                    start = False
                elif tcolor == secondary_color:
                    theme_select()
                    start = False
                elif icolor == secondary_color:
                    instructions()
                    start = False
        img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
        screen.blit(img, (0, 0))
        screen.blit(title_text, textRect)
        py.draw.rect(screen, scolor, start_button)
        py.draw.rect(screen, qcolor, quit_button)
        py.draw.rect(screen, lcolor, lb_button)
        py.draw.rect(screen, tcolor, theme_button)
        py.draw.rect(screen, icolor, i_button)
        screen.blit(start_text, stextrect)
        screen.blit(quit_text, qtextrect)
        screen.blit(lb_text, lbtextrect)
        screen.blit(theme_text, theme_text_rect)
        screen.blit(i_text, i_rect)
        py.display.flip()
        py.display.update()
        clock.tick(60)

def instructions():
    clock = py.time.Clock()

    bcolor = primary_color
    btext = font.render("BACK", True, button_txt_color)
    brect = btext.get_rect()
    brect.center = (width // 2, height * 0.9)
    bbutton = py.Rect(0, 0, 200, 60)
    bbutton.center = (width // 2, height * 0.9)

    title = font.render("How To Play", True, txt_color)
    title_rect = title.get_rect()
    title_rect.center = (width // 2, height // 8)

    i1 = ifont.render("The goal of the game is to guess as many words as you can", True, txt_color)
    i1_rect = i1.get_rect()
    i1_rect.center = (width // 2, height // 3)

    i2 = ifont.render("with a time constraint and a limit on guesses. There are", True, txt_color)
    i2_rect = i2.get_rect()
    i2_rect.center = (width // 2, (height // 3) + 20)

    i3 = ifont.render("3 levels, easy, medium, and hard easy mode has you guess", True, txt_color)
    i3_rect = i3.get_rect()
    i3_rect.center = (width // 2, (height // 3) + 40)

    i4 = ifont.render("a 4 letter word with 30 seconds and 12 letter guesses, medium", True, txt_color)
    i4_rect = i4.get_rect()
    i4_rect.center = (width // 2, (height // 3) + 60)

    i5 = ifont.render("mode has you guess a 5 letter word with 25 seconds and 10", True, txt_color)
    i5_rect = i5.get_rect()
    i5_rect.center = (width // 2, (height // 3) + 80)

    i6 = ifont.render("letter guesses hard mode has you guess a 6 letter word", True, txt_color)
    i6_rect = i6.get_rect()
    i6_rect.center = (width // 2, (height // 3) + 100)

    i7 = ifont.render("with 20 seconds and eight letter guesses. You get 10 points", True, txt_color)
    i7_rect = i7.get_rect()
    i7_rect.center = (width // 2, (height // 3) + 120)

    i8 = ifont.render("for every letter guessed correctly and one point is taken", True, txt_color)
    i8_rect = i8.get_rect()
    i8_rect.center = (width // 2, (height // 3) + 140)

    i9 = ifont.render("away for every letter guesed incorrectly. Every 3 turns you will", True, txt_color)
    i9_rect = i9.get_rect()
    i9_rect.center = (width // 2, (height // 3) + 160)

    i10 = ifont.render("get a random power up which can be freeze time, reveal one letter,", True, txt_color)
    i10_rect = i10.get_rect()
    i10_rect.center = (width // 2, (height // 3) + 180)

    i11 = ifont.render("3 extra guesses, or 5 extra guesses. Powerups do not stack up", True, txt_color)
    i11_rect = i11.get_rect()
    i11_rect.center = (width // 2, (height // 3) + 200)

    running = True
    while running:
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    running = False
                    break
            elif event.type == py.QUIT:
                exit()
            elif event.type == py.MOUSEMOTION:
                mpos = py.mouse.get_pos()
                if bbutton.collidepoint(mpos): 
                    bcolor = secondary_color 
                else:
                    bcolor = primary_color
            elif event.type == py.MOUSEBUTTONDOWN:
                if bcolor == secondary_color:
                    main()
                    running = False
                    continue

        img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
        screen.blit(img, (0, 0))
        py.draw.rect(screen, bcolor, bbutton)
        draw_screen(screen, [[i1, i1_rect], [i2, i2_rect], [i3, i3_rect], [i4, i4_rect], [i5, i5_rect], [btext, brect], 
        [i6, i6_rect], [i7, i7_rect], [i8, i8_rect], [i9, i9_rect], [i10, i10_rect], [i11, i11_rect], [title, title_rect]])
        py.display.flip()
        py.display.update()
        clock.tick(60)

def theme_select():
    clock = py.time.Clock()
    theme = 0
    running = True
    scolor = primary_color
    while running: 

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    running = False
                    break
                elif event.key == py.K_RIGHT:
                    theme += 1
                    if theme > len(bgs) - 1:
                        theme = 0
                    change_themes(theme)
                    scolor = primary_color
                elif event.key == py.K_LEFT:
                    theme -= 1
                    if theme < 0:
                        theme = len(bgs) - 1
                    change_themes(theme)
            elif event.type == py.QUIT:
                exit()
            elif event.type == py.MOUSEMOTION:
                mpos = py.mouse.get_pos()
                if sb.collidepoint(mpos): 
                    scolor = secondary_color 
                else:
                    scolor = primary_color
            elif event.type == py.MOUSEBUTTONDOWN:
                if scolor == secondary_color:
                    main()
                    running = False
                    continue
        
        title_text = font.render("SELECT THEME", True, txt_color)
        title_rect = title_text.get_rect()
        title_rect.center = (width // 2, height // 10)

        i1_text = font.render("Use arrow keys", True, txt_color)
        i1_rect = i1_text.get_rect()
        i1_rect.center = (width // 2, height // 2)

        i2_text = font.render("to change theme", True, txt_color)
        i2_rect = i2_text.get_rect()
        i2_rect.center = (width // 2, (height // 2) + 34)

        s_text = font.render("SELECT", True, button_txt_color)
        s_rect = s_text.get_rect()
        s_rect.center = (width // 2, (height // 5) * 4)
        sb = py.Rect(0, 0, 200, 60)
        sb.center = (width // 2, (height // 5) * 4)

        img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
        screen.blit(img, (0, 0))
        py.draw.rect(screen, scolor, sb)
        draw_screen(screen, [[title_text, title_rect], [i1_text, i1_rect], [i2_text, i2_rect], [s_text, s_rect]])
        py.display.flip()
        py.display.update()
        clock.tick(60)

def pick_word(words):
    word = words[randint(0, len(words)-1)].split('\n')[0]
    return word.split('\n')[0], len(word)

def return_blank_word(word, letters_guessed):
    returnval = ""
    for c in word:
        if c in letters_guessed:
            returnval += c.upper()
        else: returnval += '_'
    return returnval

def return_guessed_letters(letters_guessed, correct_letters):
    returnval = ""
    for letter in letters_guessed:
        if letter not in correct_letters:
            returnval += letter + ' '
    return returnval

def select_new_word(word, words):
    word += '\n'
    words.remove(word)
    w, l = pick_word(words)
    return w, l, [], [], words

def draw_screen(screen, objects):
    for obj in objects:
        screen.blit(obj[0], obj[1])
    
def name_input():
    clock = py.time.Clock()
    start = True
    scolor = primary_color
    bcolor = primary_color
    user_text = ''
    input_rect = py.Rect(0, 0, 320, 35)
    input_rect.center = (width // 2, height // 3)
    color_active = py.Color('white')
    color_passive = py.Color('light gray')
    color = color_passive

    title_text = font.render("Enter Name BELOW", True, txt_color)
    title_rect = title_text.get_rect()
    title_rect.center = (width // 2, height * 0.15)
    

    active = False
    while start:      

        start_text = font.render('START', True, button_txt_color)
        stextrect = start_text.get_rect()
        stextrect.center = (width // 2, (height // 5) * 3)
        start_button = py.Rect(0, 0, 200, 60)
        start_button.center = (width // 2, (height // 5) * 3)

        back_text = font.render('BACK', True, button_txt_color)
        back_rect = back_text.get_rect()
        back_rect.center = (width // 2, (height // 5) * 4)
        back_button = py.Rect(0, 0, 200, 60)
        back_button.center = (width // 2, (height // 5) * 4)

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    start = False
                    break
                elif event.key == py.K_RETURN:
                    level_select(user_text.upper())
                    start = False
                    continue
                elif event.key == py.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif len(user_text) < 10 and event.unicode.isalpha():
                    user_text += event.unicode
                
            elif event.type == py.QUIT:
                start = False
                break
            elif event.type == py.MOUSEMOTION:
                mpos = py.mouse.get_pos()
                if start_button.collidepoint(mpos): 
                    scolor = secondary_color 
                else:
                    scolor = primary_color
                if back_button.collidepoint(mpos):
                    bcolor = secondary_color
                else:
                    bcolor = primary_color
            elif event.type == py.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if scolor == secondary_color and len(user_text) > 0:
                    level_select(user_text.upper())
                    start = False
                    continue
                elif bcolor == secondary_color:
                    main()
                    exit()
                    start = False
                    continue
        if active:
            color = color_active
        else:
            color = color_passive

        screen.fill(txt_color)
        img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
        screen.blit(img, (0, 0))
        py.draw.rect(screen, color, input_rect)
        name_text = font.render(user_text.upper(), True, button_txt_color)
        name_rect = name_text.get_rect()
        name_rect.center = (width // 2, height // 3)
        screen.blit(name_text, name_rect)
        screen.blit(title_text, title_rect)
        py.draw.rect(screen, scolor, start_button)
        py.draw.rect(screen, bcolor, back_button)
        screen.blit(start_text, stextrect)
        screen.blit(back_text, back_rect)
        py.display.flip()
        py.display.update()
        clock.tick(60)

def level_select(username):
    clock = py.time.Clock()
    start = True
    ecolor = primary_color
    mcolor = primary_color
    hcolor = primary_color
    bcolor = primary_color
    while start:
        lstext = font.render('Level Select', True, txt_color)
        lsrect = lstext.get_rect()
        lsrect.center = (width // 2, (height * 0.1))
        easy_text = font.render('EASY', True, button_txt_color)
        easy_rect = easy_text.get_rect()
        easy_rect.center = (width // 2, (height // 5) * 1)
        easy_button = py.Rect(0, 0, 200, 60)
        easy_button.center = (width // 2, (height // 5) * 1)

        medium_text = font.render('MEDIUM', True, button_txt_color)
        medium_rect = medium_text.get_rect()
        medium_rect.center = (width // 2, (height // 5) * 2)
        medium_button = py.Rect(0, 0, 200, 60)
        medium_button.center = (width // 2, (height // 5) * 2)

        hard_text = font.render('HARD', True, button_txt_color)
        hard_rect = hard_text.get_rect()
        hard_rect.center = (width // 2, (height // 5) * 3)
        hard_button = py.Rect(0, 0, 200, 60)
        hard_button.center = (width // 2, (height // 5) * 3)

        back_text = font.render('BACK', True, button_txt_color)
        back_rect = back_text.get_rect()
        back_rect.center = (width // 2, (height // 5) * 4)
        back_button = py.Rect(0, 0, 200, 60)
        back_button.center = (width // 2, (height // 5) * 4)

        for event in py.event.get():
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        start = False
                        break
                elif event.type == py.QUIT:
                    start = False
                    break
                elif event.type == py.MOUSEMOTION:
                    mpos = py.mouse.get_pos()
                    if easy_button.collidepoint(mpos): 
                        ecolor = secondary_color 
                    else:
                        ecolor = primary_color
                    if medium_button.collidepoint(mpos): 
                        mcolor = secondary_color 
                    else:
                        mcolor = primary_color
                    if hard_button.collidepoint(mpos): 
                        hcolor = secondary_color 
                    else:
                        hcolor = primary_color
                    if back_button.collidepoint(mpos):
                        bcolor = secondary_color
                    else:
                        bcolor = primary_color
                elif event.type == py.MOUSEBUTTONDOWN:
                    if ecolor == secondary_color:
                        if username == None:
                            leader_boards(1)
                        else:
                            game(1, username)
                        start = False
                        continue
                    elif mcolor == secondary_color:
                        if username == None:
                            leader_boards(2)
                        else:
                            game(2, username)
                        start = False
                        continue
                    elif hcolor == secondary_color:
                        if username == None:
                            leader_boards(3)
                        else:
                            game(3, username)
                        start = False
                        continue
                    elif bcolor == secondary_color:
                        main()
                        exit()
                        start = False
                        continue

        screen.fill(txt_color)
        img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
        screen.blit(img, (0, 0))
        py.draw.rect(screen, ecolor, easy_button)
        py.draw.rect(screen, mcolor, medium_button)
        py.draw.rect(screen, hcolor, hard_button)
        py.draw.rect(screen, bcolor, back_button)
        screen.blit(lstext, lsrect)
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)
        screen.blit(back_text, back_rect)
        py.display.flip()
        py.display.update()
        clock.tick(60)

def format_score(usr: User, level: int):
    if level == 1: score = usr.es
    elif level == 2: score = usr.ms
    else: score = usr.hs

    string = usr.name
    for x in range(12-len(string)):
        string += '-'

    temp_str = ""
    for x in range(5 - len(str(score))):
        temp_str += '0'
    string += temp_str + str(score)
    return string

def leader_boards(level):
    clock = py.time.Clock()
    running = True
    try:
        with open('leaderboard.txt', 'r') as f:
            stats = f.readlines()
            leader_board = []
            x = len(stats)
            for i in range(x):
                temp_highest = 0
                temp_highest_usr = None
                for stat in stats:
                    if int(stat.split(";*|")[level]) > temp_highest and str_to_usr(stat) not in leader_board:
                        temp_highest = int(stat.split(";*|")[level])
                        temp_highest_usr = str_to_usr(stat)
                leader_board.append(temp_highest_usr)
            f.close()
        if level == 1:
            title_text = font.render("Easy Mode Leaderboad", True, txt_color)
        elif level == 2:
            title_text = font.render("Medium Mode Leaderboad", True, txt_color)
        else:
            title_text = font.render("Hard Mode Leaderboad", True, txt_color)
        title_rect = title_text.get_rect()
        title_rect.center = (width // 2, height // 5)

        heading_text = font.render("NAME         SCORE", True, txt_color)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (width // 2, height // 3)

        leader_board_text = []
        for usr in range(len(leader_board[:5])):
            text = font.render(format_score(leader_board[usr], level), True, txt_color)
            rect = text.get_rect()
            rect.center = (width // 2, (height // 11) * (4.75 + usr))
            leader_board_text.append([text, rect])
        
        bcolor = primary_color
        back_text = font.render('BACK', True, button_txt_color)
        back_rect = back_text.get_rect()
        back_rect.center = (width // 2, (height // 11) * 10)
        back_button = py.Rect(0, 0, 200, 60)
        back_button.center = (width // 2, (height // 11) * 10)


        format_score(leader_board[0], level)

        while running:
            
            for event in py.event.get():
                if event.type == py.KEYDOWN:
                        if event.key == py.K_ESCAPE:
                            running = False
                            break
                elif event.type == py.QUIT:
                    running = False
                    break
                elif event.type == py.MOUSEMOTION:
                    mpos = py.mouse.get_pos()
                    if back_button.collidepoint(mpos):
                        bcolor = secondary_color
                    else:
                        bcolor = primary_color
                elif event.type == py.MOUSEBUTTONDOWN:
                    if bcolor == secondary_color:
                        main()
                        exit()
                        running = False
                        continue

            screen.fill(txt_color)
            img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
            screen.blit(img, (0, 0))
            py.draw.rect(screen, bcolor, back_button)
            draw_screen(screen, [[title_text, title_rect], [heading_text, heading_rect], 
            [leader_board_text[0][0], leader_board_text [0][1]], [leader_board_text[1][0], leader_board_text[1][1]], [leader_board_text[2][0], leader_board_text[2][1]], 
            [leader_board_text[3][0], leader_board_text[3][1]], [leader_board_text[4][0], leader_board_text[4][1]], [back_text, back_rect]])
            py.display.flip()
            py.display.update()
            clock.tick(60)
    except IndexError:
        main()
        exit()

def game(level, username):
    has_power = False
    power_ups = {0: "Reveal One Letter", 1: "Freeze Time", 2: "+3 guesses", 3: "+5 guesses"}
    power_up = None
    counter = 0
    clock = py.time.Clock()
    play = True
    with open("words.txt", 'r') as f:
        words = f.readlines()
        f.close()
    word, _= pick_word(words)
    score = 0
    if level == 1:
        guesstime = 30
        buffer = 3
        word_length = 4
        num_guesses = 12
    elif level == 2:
        guesstime = 25
        buffer = 3
        word_length = 5
        num_guesses = 10
    elif level == 3:
        guesstime = 20
        buffer = 3
        word_length = 6
        num_guesses = 8
    letters_used = []
    correct_letters_guessed = []
    tm = int(time.ctime()[17:19])
    target_tm = tm + guesstime
    temp_tm = target_tm
    if target_tm >= 60: target_tm -= 60
    freeze_time = False
    plus_three = False
    plus_five = False
    while play:
        if freeze_time:
            target_tm = None
        if int(time.ctime()[17:19]) == target_tm:
            incorrect_word = word.upper()
            incorrect = True
            word, length, letters_used, correct_letters_guessed, words = select_new_word(word, words)
            t = int(time.ctime()[17:19])
            target_time = t + 3
            if target_time >= 60: target_time -= 60
            while int(time.ctime()[17:19]) != target_time:
                wrong_text = font.render(f'{incorrect_word}', True, py.Color("red"))
                message_text = font.render(f'was the correct answer', True, txt_color)
                wrong_rect = wrong_text.get_rect()
                message_rect = message_text.get_rect()
                wrong_rect.center = (width // 2, height // 2)
                message_rect.center = (width // 2, height // 2 + 34)
                screen.fill(txt_color)
                img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
                screen.blit(img, (0, 0))
                draw_screen(screen, [[wrong_text, wrong_rect], [message_text, message_rect]])
                py.display.flip()
                py.display.update()
                clock.tick(60)
            tm = int(time.ctime()[17:19])
            target_tm = tm + guesstime + buffer
            temp_tm = target_tm
            if target_tm >= 60: target_tm -= 60
            play = False
            continue
        if not freeze_time and int(temp_tm - int(time.ctime()[17:19])) <= 30:
            clock_text = font.render(str(temp_tm - int(time.ctime()[17:19])), True, py.Color("red"))
        elif not freeze_time and int(temp_tm - int(time.ctime()[17:19])) > 30:
            clock_text = font.render(str(target_tm - int(time.ctime()[17:19])), True, py.Color("red"))
        else:
            clock_text = font.render('FROZEN', True, freeze_color)
        clock_rect = clock_text.get_rect()
        clock_rect.center = (width // 2, height * 0.1)
        points_gained = 0

        if len(word) != word_length:
            words.remove(word + '\n')
            word, length = pick_word(words)

        score_text = font.render(f'Score: {score}', True, txt_color)
        scorerect = score_text.get_rect()
        scorerect.center=(width // 2, height * 0.25)

        guesses_used = len(letters_used) - len(correct_letters_guessed)
        guess_text = font.render(f'{guesses_used} out of {num_guesses}', True, txt_color)
        guess_rect = guess_text.get_rect()
        guess_rect.center = (width // 2, height * 0.18)

        text = font.render(return_blank_word(word, correct_letters_guessed), True, txt_color)
        textrect = text.get_rect()
        textrect.center = (width // 2, height // 2)

        lg = font.render(return_guessed_letters(letters_used, correct_letters_guessed), True, txt_color)
        lgrect = lg.get_rect()
        lgrect.center = (width // 2, height * 0.75)

        if power_up != None and has_power:
            p_header = font.render("Press 1 to use", True, txt_color)
            h_rect = p_header.get_rect()
            h_rect.center = (width // 2, height * 0.33)
            p_text = font.render(f'{power_ups[power_up]}', True, txt_color)
            p_rect = p_text.get_rect()
            p_rect.center = (width // 2, height * 0.4)
            
        print(word)
        correct = False
        incorrect = False

        for event in py.event.get():
            try:
                if event.type == py.QUIT:
                    play = False
                    break
                elif event.type == py.KEYDOWN:
                    if chr(event.key).isalpha():
                        guess = chr(event.key)
                        if guess in word and guess not in letters_used:
                            print("correct")
                            letters_used.append(guess)
                            correct_letters_guessed.append(guess)
                        elif guess not in letters_used:
                            letters_used.append(guess)
                        correct = True
                        for c in word:
                            if c not in letters_used:
                                correct = False
                                break
                        if correct:
                            print("you guessed everything")
                            points_gained = (10 * len(word)) - (len(letters_used) - len(correct_letters_guessed))
                            score += points_gained
                            counter += 1
                            print(score)
                            correct_word = word.upper()
                            word, _, letters_used, correct_letters_guessed, words = select_new_word(word, words)
                            tm = int(time.ctime()[17:19])
                            target_tm = tm + guesstime + buffer
                            temp_tm = target_tm
                            if target_tm >= 60: target_tm -= 60
                        elif len(letters_used) - len(correct_letters_guessed) == num_guesses:
                            incorrect_word = word.upper()
                            incorrect = True
                            word, _, letters_used, correct_letters_guessed, words = select_new_word(word, words)
                    elif chr(event.key) == '1' and has_power and power_up != None:
                        print("power up used")
                        if power_up == 0:
                            for w in word:
                                if w not in correct_letters_guessed:
                                    correct_letters_guessed.append(w)
                                    letters_used.append(w)
                                    break
                        elif power_up == 1:
                            freeze_time = True
                        elif power_up == 2:
                            num_guesses += 3
                            plus_three = True
                        elif power_up == 3:
                            num_guesses += 5
                            plus_five = True
                        power_up = None
                        has_power = False
                    elif event.key == py.K_ESCAPE:
                        play = False
                        exit()
                        
            except ValueError:
                continue
        
        if correct:
            t = int(time.ctime()[17:19])
            target_time = t + 3
            if target_time >= 60: target_time -= 60
            tmp_power_up = random.randint(0,3)
            while int(time.ctime()[17:19]) != target_time:
                cmessage_text = font.render("Great Job!", True, green)
                correct_text = font.render(f'{correct_word}', True, green)
                message_text = font.render(f'was correct: +{points_gained}', True, txt_color)
                cmessage_rect = cmessage_text.get_rect()
                correct_rect = correct_text.get_rect()
                message_rect = message_text.get_rect()
                cmessage_rect.center = (width // 2, height // 3)
                correct_rect.center = (width // 2, height // 2)
                message_rect.center = (width // 2, height // 2 + 34)
                screen.fill(txt_color)
                img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
                screen.blit(img, (0, 0))
                if counter % 3 == 0 and counter != 0:
                    power_up = tmp_power_up
                    power_header = font.render("You earned", True, txt_color)
                    header_rect = power_header.get_rect()
                    header_rect.center = (width // 2, (height // 3) * 2)
                    power_text = font.render(f'{power_ups[power_up]}', True, freeze_color)
                    power_rect = power_text.get_rect();
                    power_rect.center = (width // 2, ((height // 3) * 2) + 34)
                    draw_screen(screen, [[correct_text, correct_rect], [message_text, message_rect], 
                    [power_text, power_rect], [power_header, header_rect], [cmessage_text, cmessage_rect]])
                    has_power = True
                else:
                    draw_screen(screen, [[correct_text, correct_rect], [message_text, message_rect], [cmessage_text, cmessage_rect]])
                py.display.flip()
                py.display.update()
                clock.tick(60)
            if freeze_time: freeze_time = False
            elif plus_three: 
                num_guesses -= 3
                plus_three = False
            elif plus_five:
                num_guesses -= 5
                plus_five = False
            continue
        elif incorrect:
            t = int(time.ctime()[17:19])
            target_time = t + 3
            if target_time >= 60: target_time -= 60
            while int(time.ctime()[17:19]) != target_time:
                wrong_text = font.render(f'{incorrect_word}', True, py.Color("red"))
                message_text = font.render(f'was the correct answer', True, txt_color)
                wrong_rect = wrong_text.get_rect()
                message_rect = message_text.get_rect()
                wrong_rect.center = (width // 2, height // 2)
                message_rect.center = (width // 2, height // 2 + 34)
                screen.fill(txt_color)
                img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
                screen.blit(img, (0, 0))
                draw_screen(screen, [[wrong_text, wrong_rect], [message_text, message_rect]])
                py.display.flip()
                py.display.update()
                clock.tick(60)
            play = False
            continue
        screen.fill(txt_color)
        img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
        screen.blit(img, (0, 0))
        if power_up != None and has_power:
            draw_screen(screen, [[text, textrect], [lg, lgrect], [score_text, scorerect], [clock_text, clock_rect], 
            [p_text, p_rect], [p_header, h_rect], [guess_text, guess_rect]])
        else:
            draw_screen(screen, [[text, textrect], [lg, lgrect], [score_text, scorerect], [clock_text, clock_rect], [guess_text, guess_rect]])

        py.display.flip()
        py.display.update()
        clock.tick(60)
    end(score, level, username)

def end(score, level, username):
    clock = py.time.Clock()
    start = True
    scolor = primary_color
    try:
        u = User(username)
        if u not in users:
            with open('leaderboard.txt', 'a') as f:
                u.update_high_scores(score, level)
                users.append(u)
                f.write(users[-1].get_highscores() + '\n')
                f.close()
        else:
            with open('leaderboard.txt', 'w') as f:
                f.truncate(0)
                for i in users:
                    if i == u:
                        i.update_high_scores(score, level)
                    f.write(i.get_highscores() + '\n')
                f.close()

        while start:
            score_text = font.render("Your final score was", True, txt_color)
            scoretx_rect = score_text.get_rect()
            scoretx_rect.center = (width // 2, height // 2)

            scoret = font.render(f'{score}', True, green)
            scoret_rect = scoret.get_rect()
            scoret_rect.center = (width // 2, height // 2 + 34)

            back_text = font.render('BACK TO MENU', True, button_txt_color)
            back_rect = back_text.get_rect()
            back_rect.center = (width // 2, (height // 5) * 4)
            back_button = py.Rect(0, 0, 400, 60)
            back_button.center = (width // 2, (height // 5) * 4)

            for event in py.event.get():
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        start = False
                        break
                elif event.type == py.QUIT:
                    start = False
                    break
                elif event.type == py.MOUSEMOTION:
                    mpos = py.mouse.get_pos()
                    if back_button.collidepoint(mpos): 
                        scolor = secondary_color 
                    else:
                        scolor = primary_color
                elif event.type == py.MOUSEBUTTONDOWN:
                    if scolor == secondary_color:
                        main()
                        exit()
                        start = False
                        continue
            screen.fill(txt_color)
            img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
            screen.blit(img, (0, 0))
            py.draw.rect(screen, scolor, back_button)
            draw_screen(screen, [[score_text, scoretx_rect], [scoret, scoret_rect], [back_text, back_rect]])
            py.display.flip()
            py.display.update()
            clock.tick(60)
    except AttributeError:
        main()
        exit()


if __name__ == "__main__":
    main()
