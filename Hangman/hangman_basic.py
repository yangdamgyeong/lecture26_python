# 1. computer가 단어를 선택한다 -> 빈칸 보여주기
# 2. 사용자가 알파벳을 입력한다
# 3. updategame -> 게임의 상태를 업데이트한다.
# 4. 알파벳 다 맞췄으면 You win
# 5. 틀리면 updategame
# 6. 2-4번 반복
# 7. try가 7번이 넘었으면 You loose

import random
#자료 구조
limit_error = 7

def select_word():
    word_list = ['APPLE', 'BANANA', 'MAN', 'WOMAN', 'TOMATO']
    return random.choice(word_list)

#게임 로직
#1.

target_word = select_word()
# print(">> 컴퓨터가 선택한 단어 : ", target_word)
blank_char = '_'
word_screen = blank_char * len(target_word)

num_error = 0
while num_error < limit_error :
    #2.
    user_input = input('>> 알파벳 입력 : ').upper()
    #3. 게임 상태 업데이트
    #알파벳이 단어에 있으면 채워주기
    if target_word.find(user_input) == -1:
        num_error += 1 #없으면 오류 횟수 증가
        print(f'오답 : {num_error}회')
    else: # 알파벳이 단어에 있으면 채워주기
        for i in range(len(target_word)):
            if target_word[i] == user_input:
                word_screen = word_screen[:i] + user_input + word_screen[i+1:]
        print('정답 :', word_screen)
                                           
    #4. 단어를 다 맞췄으면(word_screen에 _가 없으면) 사용자 win
    if word_screen.count(blank_char) == 0:
        print('you win')
        break

    #5. 시도회수가 7번이 넘었으면 loose
if num_error >= limit_error:
    print('you loose... :', target_word)
