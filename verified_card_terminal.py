"""Test whether your golden card is true or not"""

while True:
    card_number = input('write your card number: ')
    if len(card_number) != 16:
        print('Error:(golden card shoud have 16 number.)')
    else:
        list_num = []
        res_addition = 0
        for index in range(16):
            if index % 2 != 0:
                list_num.append(int(card_number[index]))
            elif index % 2 == 0:
                duplicate_num = str(int(card_number[index]) * 2)
                if len(duplicate_num) < 2:
                    result = int(duplicate_num[0])
                    list_num.append(result)
                else:
                    result = int(duplicate_num[0]) + int(duplicate_num[1])
                    list_num.append(result)

        for i in list_num[:(len(card_number) - 1)]:
            res_addition += i

        c = res_addition % 10
        d = 10 - c

        if d == int(list_num[-1]):
            print('*********Card verified*********')
        else:
            print('*********False card*********')
    answer = input('Wanna try again (y/n): ')
    print('\n')
    if answer == 'n':
        break
    else:
        continue
