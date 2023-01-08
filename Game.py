import pygame as py
from random import randint
import time

'''
Add typing capabilities
Add timer
Add scoring
'''

py.init()
dimensions = (width, height) = (500, 700)
screen = py.display.set_mode(dimensions)
font = py.font.Font('freesansbold.ttf', 32)

def main():
    clock = py.time.Clock()
    start = True
    scolor = py.Color("gray")
    qcolor = py.Color("gray")
    while start:      

        title_text = font.render('Fi_l In Th_ Bl_nk', True, py.Color("black"))
        textRect = title_text.get_rect()
        textRect.center = (width // 2, height // 5)

        start_text = font.render('START', True, py.Color("black"))
        stextrect = start_text.get_rect()
        stextrect.center = (width // 2, height // 2.5)
        start_button = py.Rect(0, 0, 200, 60)
        start_button.center = (width // 2, height // 2.5)

        quit_text = font.render('QUIT', True, py.Color("black"))
        qtextrect = quit_text.get_rect()
        qtextrect.center = (width // 2, int(height * 0.6))
        quit_button = py.Rect(0, 0, 200, 60)
        quit_button.center = (width // 2, int(height * 0.6))

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
                if start_button.collidepoint(mpos): 
                    scolor = py.Color("light gray") 
                else:
                    scolor = py.Color("gray")
                if quit_button.collidepoint(mpos):
                    qcolor = py.Color("light gray")
                else:
                    qcolor = py.Color("gray")
            elif event.type == py.MOUSEBUTTONDOWN:
                if scolor == py.Color("light gray"):
                    name_input()
                    start = False
                    continue
                elif qcolor == py.Color("light gray"):
                    start = False
                    break
        screen.fill(py.Color("white"))
        
        screen.blit(title_text, textRect)
        py.draw.rect(screen, scolor, start_button)
        py.draw.rect(screen, qcolor, quit_button)
        screen.blit(start_text, stextrect)
        screen.blit(quit_text, qtextrect)
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
        else: returnval += '_ '
    return returnval

def return_guessed_letters(letters_guessed, correct_letters):
    returnval = ""
    for letter in letters_guessed:
        if letter not in correct_letters:
            returnval += letter + ' '
    return returnval

def select_new_word(word, words):
    try:
        w, l = pick_word(words.remove(word))
        return w, l, [], []
    except ValueError:
        w, l = pick_word(words)
        return w, l, [], []

def draw_screen(screen, objects):
    for obj in objects:
        screen.blit(obj[0], obj[1])
    
def name_input():
    clock = py.time.Clock()
    start = True
    scolor = py.Color("gray")
    base_font = py.font.Font(None, 32)
    user_text = ''
    input_rect = py.Rect(0, 0, 150, 32)
    input_rect.center = (width // 2, height // 2)
    color_active = py.Color('light gray')
    color_passive = py.Color('gray')
    color = color_passive
    active = False
    while start:      

        start_text = font.render('START', True, py.Color("black"))
        stextrect = start_text.get_rect()
        stextrect.center = (width // 2, (height // 5) * 4)
        start_button = py.Rect(0, 0, 200, 60)
        start_button.center = (width // 2, (height // 5) * 4)

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    start = False
                    break
                if event.key == py.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif len(user_text) < 10:
                    user_text += event.unicode
            elif event.type == py.QUIT:
                start = False
                break
            elif event.type == py.MOUSEMOTION:
                mpos = py.mouse.get_pos()
                if start_button.collidepoint(mpos): 
                    scolor = py.Color("light gray") 
                else:
                    scolor = py.Color("gray")
            elif event.type == py.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if scolor == py.Color("light gray") and len(user_text) > 0:
                    level_select(user_text)
                    start = False
                    continue
        if active:
            color = color_active
        else:
            color = color_passive

        screen.fill(py.Color("white"))
        py.draw.rect(screen, color, input_rect)
        name_text = base_font.render(user_text, True, py.Color("black"))
        name_rect = name_text.get_rect()
        name_rect.center = (width // 2, height // 2)
        screen.blit(name_text, name_rect)
        input_rect.w = 150
        py.draw.rect(screen, scolor, start_button)
        screen.blit(start_text, stextrect)
        py.display.flip()
        py.display.update()
        clock.tick(60)

def level_select(username):
    clock = py.time.Clock()
    start = True
    ecolor = py.Color("gray")
    mcolor = py.Color("gray")
    hcolor = py.Color("gray")
    while start:
        easy_text = font.render('EASY', True, py.Color("black"))
        easy_rect = easy_text.get_rect()
        easy_rect.center = (width // 2, (height // 5) * 2)
        easy_button = py.Rect(0, 0, 200, 60)
        easy_button.center = (width // 2, (height // 5) * 2)

        medium_text = font.render('MEDIUM', True, py.Color("black"))
        medium_rect = medium_text.get_rect()
        medium_rect.center = (width // 2, (height // 5) * 3)
        medium_button = py.Rect(0, 0, 200, 60)
        medium_button.center = (width // 2, (height // 5) * 3)

        hard_text = font.render('HARD', True, py.Color("black"))
        hard_rect = hard_text.get_rect()
        hard_rect.center = (width // 2, (height // 5) * 4)
        hard_button = py.Rect(0, 0, 200, 60)
        hard_button.center = (width // 2, (height // 5) * 4)

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
                        ecolor = py.Color("light gray") 
                    else:
                        ecolor = py.Color("gray")
                    if medium_button.collidepoint(mpos): 
                        mcolor = py.Color("light gray") 
                    else:
                        mcolor = py.Color("gray")
                    if hard_button.collidepoint(mpos): 
                        hcolor = py.Color("light gray") 
                    else:
                        hcolor = py.Color("gray")
                elif event.type == py.MOUSEBUTTONDOWN:
                    if ecolor == py.Color("light gray"):
                        game(1, username)
                        start = False
                        continue
                    elif mcolor == py.Color("light gray"):
                        game(2, username)
                        start = False
                        continue
                    elif hcolor == py.Color("light gray"):
                        game(3, username)
                        start = False
                        continue
        screen.fill(py.Color("white"))
        py.draw.rect(screen, ecolor, easy_button)
        py.draw.rect(screen, mcolor, medium_button)
        py.draw.rect(screen, hcolor, hard_button)
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)
        py.display.flip()
        py.display.update()
        clock.tick(60)
    
def game(level, username):
    clock = py.time.Clock()
    play = True
    ncolor = py.Color("gray")
    with open("words.txt", 'r') as f:
        words = f.readlines()
        f.close()
    word, length = pick_word(words)
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

    while play:
        if int(time.ctime()[17:19]) == target_tm:
            incorrect_word = word.upper()
            incorrect = True
            word, length, letters_used, correct_letters_guessed = select_new_word(word, words)
            t = int(time.ctime()[17:19])
            target_time = t + 3
            if target_time >= 60: target_time -= 60
            while int(time.ctime()[17:19]) != target_time:
                wrong_text = font.render(f'{incorrect_word}', True, py.Color("red"))
                message_text = font.render(f'was the correct answer', True, py.Color("black"))
                wrong_rect = wrong_text.get_rect()
                message_rect = message_text.get_rect()
                wrong_rect.center = (width // 2, height // 2)
                message_rect.center = (width // 2, height // 2 + 34)
                screen.fill(py.Color("white"))
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
        clock_text = font.render(str(temp_tm - int(time.ctime()[17:19])), True, py.Color("red"))
        clock_rect = clock_text.get_rect()
        clock_rect.center = (width // 2, height * 0.1)
        points_gained = 0

        if len(word) != word_length: word, length = pick_word(words)

        score_text = font.render(f'Score: {score}', True, py.Color("black"))
        scorerect = score_text.get_rect()
        scorerect.center=(width // 2, height * 0.25)

        text = font.render(return_blank_word(word, correct_letters_guessed), True, py.Color("black"))
        textrect = text.get_rect()
        textrect.center = (width // 2, height // 2)

        lg = font.render(return_guessed_letters(letters_used, correct_letters_guessed), True, py.Color("black"))
        lgrect = lg.get_rect()
        lgrect.center = (width // 2, height * 0.75)

        print(word)
        correct = False
        incorrect = False

        for event in py.event.get():
            try:
                if event.type == py.QUIT:
                    play = False
                    break
                elif event.type == py.KEYDOWN and chr(event.key).isalpha():
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
                        print(score)
                        correct_word = word.upper()
                        word, length, letters_used, correct_letters_guessed = select_new_word(word, words)
                        tm = int(time.ctime()[17:19])
                        target_tm = tm + guesstime + buffer
                        temp_tm = target_tm
                        if target_tm >= 60: target_tm -= 60
                    elif len(letters_used) - len(correct_letters_guessed) == num_guesses:
                        incorrect_word = word.upper()
                        incorrect = True
                        word, length, letters_used, correct_letters_guessed = select_new_word(word, words)
            except ValueError:
                continue
        
        if correct:
            t = int(time.ctime()[17:19])
            target_time = t + 3
            if target_time >= 60: target_time -= 60
            while int(time.ctime()[17:19]) != target_time:
                correct_text = font.render(f'{correct_word}', True, py.Color("green"))
                message_text = font.render(f'was correct: +{points_gained}', True, py.Color("black"))
                correct_rect = correct_text.get_rect()
                message_rect = message_text.get_rect()
                correct_rect.center = (width // 2, height // 2)
                message_rect.center = (width // 2, height // 2 + 34)
                screen.fill(py.Color("white"))
                draw_screen(screen, [[correct_text, correct_rect], [message_text, message_rect]])
                py.display.flip()
                py.display.update()
                clock.tick(60)
            continue
        elif incorrect:
            t = int(time.ctime()[17:19])
            target_time = t + 3
            if target_time >= 60: target_time -= 60
            while int(time.ctime()[17:19]) != target_time:
                wrong_text = font.render(f'{incorrect_word}', True, py.Color("red"))
                message_text = font.render(f'was the correct answer', True, py.Color("black"))
                wrong_rect = wrong_text.get_rect()
                message_rect = message_text.get_rect()
                wrong_rect.center = (width // 2, height // 2)
                message_rect.center = (width // 2, height // 2 + 34)
                screen.fill(py.Color("white"))
                draw_screen(screen, [[wrong_text, wrong_rect], [message_text, message_rect]])
                py.display.flip()
                py.display.update()
                clock.tick(60)
            play = False
            continue
        screen.fill(py.Color("white"))
        draw_screen(screen, [[text, textrect], [lg, lgrect], [score_text, scorerect], [clock_text, clock_rect]])

        py.display.flip()
        py.display.update()
        clock.tick(60)
    end(score, level, username)

def end(score, level, username):
    clock = py.time.Clock()
    start = True
    scolor = py.Color("gray")
    while start:
        score_text = font.render("Your final score was", True, py.Color("black"))
        scoretx_rect = score_text.get_rect()
        scoretx_rect.center = (width // 2, height // 2)

        scoret = font.render(f'{score}', True, py.Color("green"))
        scoret_rect = scoret.get_rect()
        scoret_rect.center = (width // 2, height // 2 + 34)

        back_text = font.render('BACK TO MENU', True, py.Color("black"))
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
                    scolor = py.Color("light gray") 
                else:
                    scolor = py.Color("gray")
            elif event.type == py.MOUSEBUTTONDOWN:
                if scolor == py.Color("light gray"):
                    main()
                    start = False
                    continue
        screen.fill(py.Color("white"))
        py.draw.rect(screen, scolor, back_button)
        draw_screen(screen, [[score_text, scoretx_rect], [scoret, scoret_rect], [back_text, back_rect]])
        py.display.flip()
        py.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
