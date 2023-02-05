import pygame as py
from random import randint
import time
import random
from _thread import start_new_thread

'''
BUGS TO FIX
BG music plays once
'''

py.init()
dimensions = (width, height) = (700, 700)
screen = py.display.set_mode(dimensions)
font = py.font.Font('ARCADE_N.ttf', 32)
bfont = py.font.Font('ARCADE_N.ttf', 38)
ifont = py.font.Font('ARCADE_N.ttf', 10)
global bgs 
bgs = ['bg/space.png', 
'bg/sky.png',
'bg/forest.png',
'bg/night.jpeg',
'bg/mountain.png']
txt_colors = [py.Color("white"), py.Color("black"), py.Color("gray"), py.Color("white"), py.Color("black")]
button_txt_colors = [py.Color("black"), py.Color("black"), py.Color("black"), py.Color("black"), py.Color("black")]
pcolors = [py.Color("salmon"), (245, 217, 59), (245, 217, 59), py.Color("salmon"), (245, 217, 59)]
scolors = [py.Color("light salmon"), (250, 230, 122), (250, 230, 122), py.Color("light salmon"), (250, 230, 122)]
freeze_colors = [py.Color("light blue"), py.Color("dark blue"), py.Color("light blue"), py.Color("light blue"), py.Color("dark blue")]
greens = [py.Color("green"), py.Color("dark green"), py.Color("green"), py.Color("green"), py.Color("dark green")]
index = 0
py.mixer.init()

class User():
    def __init__(self, name):
        self.name = name
        self.es = 0
        self.ms = 0
        self.hs = 0
    
    def update_high_scores(self, score, level):
        if level == 1 and score > self.es: self.es = score
        elif level == 2 and score > self.ms: self.ms = score
        elif score > self.hs: self.hs = score
    
    def get_highscores(self):
        return f'{self.name};*|{self.es};*|{self.ms};*|{self.hs}'

    def __eq__(self, __o: object) -> bool:
        return self.name == __o.name

def text_animation(text, font, color, start_time):
    elapsed_time = time.time() - start_time
    chars_to_display = int(elapsed_time * 30)
    screen_text = font.render(text[:chars_to_display], 1, color)
    status = len(text) == len(text[:chars_to_display])
    return screen_text, status

def play_bg_music(filename):
    sound = py.mixer.Sound('sounds/' + filename)
    sound.set_volume(0.3)
    py.mixer.Channel(0).play(sound)

def play_effect(filename):
    py.mixer.Channel(1).play(py.mixer.Sound('sounds/' + filename))

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

def update_users():
    global users
    users = []
    with open('leaderboard.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if len(line) > 9:
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
    update_users()
    selection = 0
    prev_selection = None
    selections = {0: True, 1: False, 2: False, 3: False, 4: False}
    while start:      

        title_text = font.render('TIME CRUNCH', True, txt_color)
        textRect = title_text.get_rect()
        textRect.center = (width // 2, height // 10)

        if selections[0]:
            start_text = bfont.render('|START|', True, py.Color("white"))
        else:
            start_text = font.render('START', True, py.Color("gray"))
        stextrect = start_text.get_rect()
        stextrect.center = (width // 2, height // 4)

        if selections[1]:
            lb_text = bfont.render('|LEADERBOARD|', True, py.Color("white"))
        else:
            lb_text = font.render('LEADERBOARD', True, py.Color("gray"))
        lbtextrect = lb_text.get_rect()
        lbtextrect.center = (width // 2, height // 2.6)

        if selections[2]:
            theme_text = bfont.render('|CHANGE THEME|', True, py.Color("white"))
        else:
            theme_text = font.render('CHANGE THEME', True, py.Color("gray"))
        theme_text_rect = theme_text.get_rect()
        theme_text_rect.center = (width // 2, height // 1.9)

        if selections[3]:
            i_text = bfont.render('|INSTRUCTIONS|', True, py.Color("white"))
        else:
            i_text = font.render('INSTRUCTIONS', True, py.Color("gray"))
        i_rect = i_text.get_rect()
        i_rect.center = (width // 2, height // 1.45)

        if selections[4]:
            quit_text = bfont.render('|QUIT|', True, py.Color("white"))
        else:
            quit_text = font.render('QUIT', True, py.Color("gray"))
        qtextrect = quit_text.get_rect()
        qtextrect.center = (width // 2, height // 1.2)

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    start = False
                    break
                elif event.key == py.K_UP:
                    prev_selection = selection
                    selection -= 1
                    if selection < 0:
                        selection = len(selections) - 1
                    selections[prev_selection] = False
                    selections[selection] = True
                    play_effect('cycle.wav')
                elif event.key == py.K_DOWN:
                    prev_selection = selection
                    selection += 1
                    if selection >= len(selections):
                        selection = 0
                    selections[prev_selection] = False
                    selections[selection] = True
                    play_effect('cycle.wav')
                elif event.key == py.K_RETURN:
                    play_effect('select.wav')
                    if selection == 0:
                        name_input()
                        start = False
                        continue
                    elif selection == 1:
                        level_select(None)
                        start = False
                    elif selection == 2:
                        theme_select()
                        start = False
                    elif selection == 3:
                        instructions()
                        start = False
                    elif selection == 4:
                        start = False
                        exit()
            elif event.type == py.QUIT:
                exit()
        img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
        screen.blit(img, (0, 0))
        screen.blit(title_text, textRect)
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

    btext = font.render("Press ENTER to Return", True, txt_color)
    brect = btext.get_rect()
    brect.center = (width // 2, height * 0.9)

    title = font.render("How To Play", True, txt_color)
    title_rect = title.get_rect()
    title_rect.center = (width // 2, height // 8)

    s1 = s2 = s3 = s4 = s5 = s6 = s7 = s8 = s9 = s10 = s11 = None
    st1 = st2 = st3 = st4 = st5 = st6 = st7 = st8 = st9 = st10 = False
    running = True
    while running:
        texts = [[btext, brect], [title, title_rect]]
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    running = False
                    break
                elif event.key == py.K_RETURN:
                    play_effect('select.wav')
                    main()
                    exit()
            elif event.type == py.QUIT:
                exit()
        if s1 == None:
            s1 = time.time()
        else:
            i1, st1 = text_animation("The goal of the game is to guess as many words as you can", ifont, txt_color, s1)
            i1_rect = (40, height // 3)
            texts.append([i1, i1_rect])
        if st1 and s2 == None:
            s2 = time.time()
        elif st1:
            i2, st2 = text_animation("with a time constraint and a limit on guesses. There are", ifont, txt_color, s2)
            i2_rect = (40, (height // 3) + 20)
            texts.append([i2, i2_rect])
        if st2 and s3 == None:
            s3 = time.time()
        elif st2:
            i3, st3 = text_animation("3 levels, easy, medium, and hard easy mode has you guess", ifont, txt_color, s3)
            i3_rect = (40, (height // 3) + 40)
            texts.append([i3, i3_rect])
        if st3 and s4 == None:
            s4 = time.time()
        elif st3:
            i4, st4 = text_animation("a 4 letter word with 30 seconds and 12 letter guesses, medium", ifont, txt_color, s4)
            i4_rect = (40, (height // 3) + 60)
            texts.append([i4, i4_rect])
        if st4 and s5 == None:
            s5 = time.time()
        elif st4:
            i5, st5 = text_animation("mode has you guess a 5 letter word with 25 seconds and 10", ifont, txt_color, s5)
            i5_rect = (40, (height // 3) + 80)
            texts.append([i5, i5_rect])
        if st5 and s6 == None:
            s6 = time.time()
        elif st5:
            i6, st6 = text_animation("letter guesses hard mode has you guess a 6 letter word", ifont, txt_color, s6)
            i6_rect = (40, (height // 3) + 100)
            texts.append([i6, i6_rect])
        if st6 and s7 == None:
            s7 = time.time()
        elif st6:
            i7, st7 = text_animation("with 20 seconds and eight letter guesses. You get 10 points", ifont, txt_color, s7)
            i7_rect = (40, (height // 3) + 120)
            texts.append([i7, i7_rect])
        if st7 and s8 == None:
            s8 = time.time()
        elif st7:
            i8, st8 = text_animation("for every letter guessed correctly and one point is taken", ifont, txt_color, s8)
            i8_rect = (40, (height // 3) + 140)
            texts.append([i8, i8_rect])
        if st8 and s9 == None:
            s9 = time.time()
        elif st8:
            i9, st9 = text_animation("away for every letter guesed incorrectly. Every 3 turns you will", ifont, txt_color, s9)
            i9_rect = (40, (height // 3) + 160)
            texts.append([i9, i9_rect])
        if st9 and s10 == None:
            s10 = time.time()
        elif st9:
            i10, st10 = text_animation("get a random power up which can be freeze time, reveal one letter,", ifont, txt_color, s10)
            i10_rect = (40, (height // 3) + 180)
            texts.append([i10, i10_rect])
        if st10 and s11 == None:
            s11 = time.time()
        elif st10:
            i11, _ = text_animation("3 extra guesses, or 5 extra guesses. Powerups do not stack up.", ifont, txt_color, s11)
            i11_rect = (40, (height // 3) + 200)
            texts.append([i11, i11_rect])
        img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
        screen.blit(img, (0, 0))
        draw_screen(screen, texts)
        py.display.flip()
        py.display.update()
        clock.tick(60)

def theme_select():
    clock = py.time.Clock()
    theme = 0
    running = True
    while running: 

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    running = False
                    break
                elif event.key == py.K_RIGHT:
                    play_effect('cycle.wav')
                    theme += 1
                    if theme > len(bgs) - 1:
                        theme = 0
                    change_themes(theme)
                    scolor = primary_color
                elif event.key == py.K_LEFT:
                    play_effect('cycle.wav')
                    theme -= 1
                    if theme < 0:
                        theme = len(bgs) - 1
                    change_themes(theme)
                elif event.key == py.K_RETURN:
                    play_effect('select.wav')
                    main()
                    running = False
                    continue
            elif event.type == py.QUIT:
                exit()
        
        title_text = font.render("SELECT THEME", True, txt_color)
        title_rect = title_text.get_rect()
        title_rect.center = (width // 2, height // 10)

        i1_text = font.render("Use arrow keys", True, txt_color)
        i1_rect = i1_text.get_rect()
        i1_rect.center = (width // 2, height // 2)

        i2_text = font.render("to change theme", True, txt_color)
        i2_rect = i2_text.get_rect()
        i2_rect.center = (width // 2, (height // 2) + 34)

        s_text = font.render("Press ENTER to select", True, txt_color)
        s_rect = s_text.get_rect()
        s_rect.center = (width // 2, (height // 5) * 4)

        img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
        screen.blit(img, (0, 0))
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
    user_text = ''
    input_rect = py.Rect(0, 0, 320, 35)
    input_rect.center = (width // 2, height // 3)
    color_active = py.Color('white')
    color_passive = py.Color('light gray')
    color = color_passive

    title_text = font.render("Enter Name BELOW", True, txt_color)
    title_rect = title_text.get_rect()
    title_rect.center = (width // 2, height * 0.15)
    

    active = True

    selection = True

    while start:      
        if selection:
            start_text = bfont.render('START', True, py.Color("white"))
        else:
            start_text = font.render('START', True, py.Color("gray"))
        stextrect = start_text.get_rect()
        stextrect.center = (width // 2, (height // 5) * 3)

        if not selection:
            back_text = bfont.render('BACK', True, py.Color("white"))
        else:
            back_text = font.render('BACK', True, py.Color("gray"))
        back_rect = back_text.get_rect()
        back_rect.center = (width // 2, (height // 5) * 4)

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    start = False
                    break
                elif event.key == py.K_RETURN and selection:
                    play_effect('select.wav')
                    level_select(user_text.upper())
                    start = False
                    continue
                elif event.key == py.K_RETURN and not selection:
                    play_effect('select.wav')
                    main()
                    exit()
                elif event.key == py.K_UP or event.key == py.K_DOWN:
                    play_effect('cycle.wav')
                    selection = not selection
                elif event.key == py.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif len(user_text) < 10 and event.unicode.isalpha():
                    user_text += event.unicode
                
            elif event.type == py.QUIT:
                start = False
                break
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
        screen.blit(start_text, stextrect)
        screen.blit(back_text, back_rect)
        py.display.flip()
        py.display.update()
        clock.tick(60)

def level_select(username):
    clock = py.time.Clock()
    start = True
    selection = 0
    prev_selection = None
    selections = {0: True, 1: False, 2: False, 3: False}
    while start:
        lstext = font.render('Level Select', True, txt_color)
        lsrect = lstext.get_rect()
        lsrect.center = (width // 2, (height * 0.1))

        if selections[0]:
            easy_text = bfont.render('EASY', True, py.Color("white"))
        else:
            easy_text = font.render('EASY', True, py.Color("grey"))
        easy_rect = easy_text.get_rect()
        easy_rect.center = (width // 2, (height // 5) * 1)

        if selections[1]:
            medium_text = bfont.render('MEDIUM', True, py.Color("white"))
        else:
            medium_text = font.render('MEDIUM', True, py.Color("grey"))
        medium_rect = medium_text.get_rect()
        medium_rect.center = (width // 2, (height // 5) * 2)

        if selections[2]:
            hard_text = bfont.render('HARD', True, py.Color("white"))
        else:
            hard_text = font.render('HARD', True, py.Color("grey"))
        hard_rect = hard_text.get_rect()
        hard_rect.center = (width // 2, (height // 5) * 3)

        if selections[3]:
            back_text = bfont.render('BACK', True, py.Color("white"))
        else:
            back_text = font.render('BACK', True, py.Color("grey"))
        back_rect = back_text.get_rect()
        back_rect.center = (width // 2, (height // 5) * 4)

        for event in py.event.get():
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        start = False
                        break
                    elif event.key == py.K_UP:
                        play_effect('cycle.wav')
                        prev_selection = selection
                        selection -= 1
                        if selection < 0:
                            selection = len(selections) - 1
                        selections[prev_selection] = False
                        selections[selection] = True
                    elif event.key == py.K_DOWN:
                        play_effect('cycle.wav')
                        prev_selection = selection
                        selection += 1
                        if selection >= len(selections):
                            selection = 0
                        selections[prev_selection] = False
                        selections[selection] = True
                    elif event.key == py.K_RETURN:
                        play_effect('select.wav')
                        if selection == 0:
                            if username == None:
                                leader_boards(1)
                            else:
                                game(1, username)
                            start = False
                            continue
                        elif selection == 1:
                            if username == None:
                                leader_boards(2)
                            else:
                                game(2, username)
                            start = False
                            continue
                        elif selection == 2:
                            if username == None:
                                leader_boards(3)
                            else:
                                game(3, username)
                            start = False
                            continue
                        elif selection == 3:
                            main()
                            exit()
                elif event.type == py.QUIT:
                    start = False
                    break

        screen.fill(txt_color)
        img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
        screen.blit(img, (0, 0))
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

        back_text = font.render('Press ENTER to return', True, txt_color)
        back_rect = back_text.get_rect()
        back_rect.center = (width // 2, (height // 11) * 10)


        format_score(leader_board[0], level)

        while running:
            for event in py.event.get():
                if event.type == py.KEYDOWN:
                        if event.key == py.K_ESCAPE:
                            running = False
                            break
                        elif event.key == py.K_RETURN:
                            play_effect('select.wav')
                            main()
                            exit()
                elif event.type == py.QUIT:
                    running = False
                    break

            screen.fill(txt_color)
            img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
            screen.blit(img, (0, 0))
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
    power_ups = {0: "Reveal One Letter", 1: "Freeze Time", 2: "+3 Guesses", 3: "+5 Guesses", 4: "Double Points", 5: "Add 20 Seconds", 6: "Skip Word", 7: "Immunity", 8: "Jeopardy"}
    power_up = None
    temp_power_up = None
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
    double_points = False
    add_time = False
    skip = False
    immunity = False
    jeopardy = False
    while play:
        if freeze_time:
            target_tm = None
        elif add_time: 
            target_tm += 20
            temp_tm += 20
        try: 
            if target_tm > 60: target_tm -= 60
        except TypeError: 
            target_tm = 0
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
            if not immunity:
                play = False
            else:
                buffer = 0
            target_tm = tm + guesstime + buffer
            buffer = 3
            temp_tm = target_tm
            if target_tm >= 60: target_tm -= 60
            continue
        if not freeze_time and int(temp_tm - int(time.ctime()[17:19])) < 60:
            clock_text = font.render(str(temp_tm - int(time.ctime()[17:19])), True, py.Color("red"))
        elif not freeze_time and int(temp_tm - int(time.ctime()[17:19])) >= 60:
            clock_text = font.render(str(target_tm - int(time.ctime()[17:19])), True, py.Color("red"))
        else:
            clock_text = font.render('FROZEN', True, freeze_color)
        if add_time: 
            target_tm -= 20
            temp_tm -= 20
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
                            letters_used.append(guess)
                            correct_letters_guessed.append(guess)
                            correct = True
                            for c in word:
                                if c not in letters_used:
                                    correct = False
                                    break
                            if not correct:
                                play_effect('correct.wav')
                        elif guess not in letters_used:
                            letters_used.append(guess)
                        if power_up == 4 or power_up == 8:
                            temp_power_up = power_up
                            power_up = None
                        if correct:
                            points_gained = (10 * len(word)) - (len(letters_used) - len(correct_letters_guessed))
                            if double_points: 
                                points_gained *= 2
                                double_points = False
                            elif jeopardy:
                                points_gained = score // 2
                                jeopardy = False
                            score += points_gained
                            counter += 1
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
                            if jeopardy:
                                prev_score = score
                                score //= 2
                    elif chr(event.key) == '1' and has_power and power_up != None:
                        play_effect('power_up.wav')
                        if power_up == 0:
                            for w in word:
                                if w not in correct_letters_guessed:
                                    correct_letters_guessed.append(w)
                                    letters_used.append(w)
                                    break
                            correct = True
                            for c in word:
                                if c not in letters_used:
                                    correct = False
                                    break
                            points_gained = (10 * len(word)) - (len(letters_used) - len(correct_letters_guessed))
                            score += points_gained
                            counter += 1
                            correct_word = word.upper()
                            word, _, letters_used, correct_letters_guessed, words = select_new_word(word, words)
                            tm = int(time.ctime()[17:19])
                            target_tm = tm + guesstime + buffer
                            temp_tm = target_tm
                            if target_tm >= 60: target_tm -= 60
                        elif power_up == 1:
                            freeze_time = True
                        elif power_up == 2:
                            num_guesses += 3
                            plus_three = True
                        elif power_up == 3:
                            num_guesses += 5
                            plus_five = True
                        elif power_up == 4 and len(letters_used) == 0 and len(correct_letters_guessed) == 0:
                            double_points = True
                            temp_power_up = power_up
                        elif power_up == 5:
                            add_time = True
                        elif power_up == 6:
                            skipped_word = word.upper()
                            skip = True
                            word, _, letters_used, correct_letters_guessed, words = select_new_word(word, words)
                        elif power_up == 7:
                            immunity = True
                        elif power_up == 8 and len(letters_used) == 0 and len(correct_letters_guessed) == 0:
                            jeopardy = True
                            temp_power_up = power_up
                        power_up = None
                        has_power = False
                    elif event.key == py.K_ESCAPE:
                        play = False
                        exit()
                        
            except ValueError:
                continue
        
        if correct:
            power_up, temp_power_up, has_power = correct_screen(counter, clock, correct_word, points_gained, power_ups, temp_power_up, power_up, has_power)
            if freeze_time: freeze_time = False
            elif plus_three: 
                num_guesses -= 3
                plus_three = False
            elif plus_five:
                num_guesses -= 5
                plus_five = False
            elif add_time:
                add_time = False
            continue
        elif incorrect:
            t = int(time.ctime()[17:19])
            target_time = t + 3
            if target_time >= 60: target_time -= 60
            start_new_thread(play_effect, ('incorrect.wav',))
            while int(time.ctime()[17:19]) != target_time:
                wrong_text = font.render(f'{incorrect_word}', True, py.Color("red"))
                message_text = font.render(f'was the correct answer', True, txt_color)
                wrong_rect = wrong_text.get_rect()
                message_rect = message_text.get_rect()
                wrong_rect.center = (width // 2, height // 2)
                message_rect.center = (width // 2, height // 2 + 34)

                if jeopardy:
                    points_lost = prev_score - score
                    points_lost_text = font.render(f'You lost {points_lost} points', True, txt_color)
                    pl_rect = points_lost_text.get_rect()
                    pl_rect.center = (width // 2, height * 0.8)

                screen.fill(txt_color)
                img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
                screen.blit(img, (0, 0))
                if jeopardy: draw_screen(screen, [[wrong_text, wrong_rect], [message_text, message_rect], [points_lost_text, pl_rect]])
                else: draw_screen(screen, [[wrong_text, wrong_rect], [message_text, message_rect]])
                py.display.flip()
                py.display.update()
                clock.tick(60)
            if not immunity:
                play = False
            if jeopardy: jeopardy = False
            continue
        elif skip:
            t = int(time.ctime()[17:19])
            target_time = t + 3
            if target_time >= 60: target_time -= 60
            while int(time.ctime()[17:19]) != target_time:
                wrong_text = font.render(f'{skipped_word}', True, py.Color("red"))
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
            skip = False
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

def correct_screen(counter, clock, correct_word, points_gained, power_ups, temp_power_up, power_up, has_power):
    t = int(time.ctime()[17:19])
    target_time = t + 3
    if target_time >= 60: target_time -= 60
    tmp_power_up = random.randint(0,8)
    play_effect('correct_word.wav')
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
            temp_power_up = None
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
        if temp_power_up != None:
            power_up = temp_power_up
        py.display.flip()
        py.display.update()
        clock.tick(60)
    return power_up, temp_power_up, has_power

def end(score, level, username):
    clock = py.time.Clock()
    start = True
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

            back_text = font.render('Press ENTER to Return', True, txt_color)
            back_rect = back_text.get_rect()
            back_rect.center = (width // 2, (height // 5) * 4)

            for event in py.event.get():
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        start = False
                        break
                    elif event.key == py.K_RETURN:
                        play_effect('select.wav')
                        main()
                        exit()
                elif event.type == py.QUIT:
                    start = False
                    break
            screen.fill(txt_color)
            img = py.transform.scale(py.image.load(bg_path).convert(), (width, height))
            screen.blit(img, (0, 0))
            draw_screen(screen, [[score_text, scoretx_rect], [scoret, scoret_rect], [back_text, back_rect]])
            py.display.flip()
            py.display.update()
            clock.tick(60)
    except AttributeError as e:
        print(str(e))
        main()
        exit()


if __name__ == "__main__":
    start_new_thread(change_themes, (0,))
    start_new_thread(play_bg_music, ('bg_music.wav',))
    time.sleep(1.9)
    main()