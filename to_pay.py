
command = ''

while command != 'quit':
    command = input('what to do : ')

    if command.startswith('clear'):
        code = command.split()[1]
        with open('list\\' + 'who_buy_what_list.txt', encoding = 'utf-8') as wbwl:
            lread = wbwl.read().split('\n')
            for i in range(len(lread)):
                if lread[i].startswith(code + ' '):
                    while lread[i] != '-----':
                        lread.pop(i)
                    lread.pop(i)
                    break

        with open('list\\' + 'who_buy_what_list.txt', 'w', encoding = 'utf-8') as wbwl:
            for line in lread:
                wbwl.write(line + '\n')

        print('clear successful!')

    elif command != 'quit':
        print('input error!')
