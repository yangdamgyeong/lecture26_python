from hangman import Hangman
import re

def load_word_list():
    word_list = []
    with open('HangMan/voca.txt', 'rt', encoding='utf-8')as f:
        for voca in f:
            voca = voca.lstrip()
            if not voca:
                continue
            match = re.match(r'^[a-zA-A]+', voca)
            if match:
                pure_word = match.group()
                remaining_text = voca[len(pure_word):]
                if remaining_text and re.match(r'^\s', remaining_text):
                    if not re.search(r'[a-zA-Z]', remaining_text):
                        word_list.append(pure_word)

    return word_list

print()
print('============ Hangman =============')


#단어 선택
hangman = Hangman(load_word_list())
print(f'{hangman.display_word}, ({len(hangman.word)}글자)')

while True:
    # 알파벳 입력
    letter = input('>> 알파벳 입력 : ')
    if not letter.isalpha():
        print('알파벳을 입력하세요.')
        continue
    
    # 정답 확인
    result = hangman.check_letter(letter)
    if result == Hangman.RIGHT:
        print(f'정답 : {hangman.display_word}')
    elif result == Hangman.WRONG:
        print(f'오답 : {hangman.num_try}회 시도')
    else:
        print(hangman.error_status)
        continue

    # 승패확인
    result = hangman.is_win()
    if result == Hangman.WIN:
        print(f'YOU WIN~~ : {hangman.num_try}회 시도')
        break
    elif result == Hangman.LOOSE:
        print(f'YOU LOOSE~~ : {hangman.word}')
        break




