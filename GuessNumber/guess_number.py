# 1. 컴퓨터가 숫자를 생각한다. (1~ 50) limit = 50
# 2. 사용자가 숫자를 말한다.
# 3. 숫자가 맞으면 사용자 win
# 4. 틀리면 컴퓨터가 up,down을 알려준다.
# 5. 2~4번까지 7번 반복 try = 7
# 6. 7번 내에 맞추지 못하면 computer Win

import random

limit = 50
try_limit = 7
num_try = 0

# def secret_number():


print("=====숫자 맞추기 게임=====")
secret_number = random.randint(1,limit)
while num_try < try_limit:
    
    target = int(input('>> 숫자를 입력하세요 : '))
    if target == secret_number:
        print('>> you win~~~')
    elif target < secret_number:
        print('up')
    else:
        print('down')
    num_try += 1

if num_try == try_limit:
    print('you loose~~~')





