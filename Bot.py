
import telebot 
import json
import datetime

API_TOKEN='5925350659:AAHpjfR8i-gah2l02XABQTsMSpDfBt2sSSU'

bot = telebot.TeleBot(API_TOKEN)

calc = False


def transform_vvod(): # Преобразование цифр в числа
    global var_l
    global var1
    var_l = list(var1)
    n = 0
    for n in range(len(var_l)):
        if var_l[n] == "1" or var_l[n] == "2" or var_l[n] == "3" or var_l[n] == "4" \
            or var_l[n] == "5" or var_l[n] == "6" or var_l[n] == "7" or var_l[n] == "8" \
                or var_l[n] == "9" or var_l[n] == "0":
                    i = int(var_l[n])
                    var_l[n] = i

    if var_l[0] == "-":
        var_l.pop(0)
        var_l[0] = var_l[0] * -1
    elif var_l[0] == "+":
        var_l.pop(0)

    if var_l[0] == "(" and var_l[1] == "-":
        var_l.pop(1)
        var_l[1] = var_l[1] * -1
    elif var_l[0] == "(" and var_l[1] == "+":
        var_l.pop(1)
    
    n = 0
    for n in range(len(var_l)): 
        if var_l[n] == "(" or var_l[n] == "+" or var_l[n] == "-" or var_l[n] == "/" \
             or var_l[n] == "*":
                if var_l[n + 1] == "-":
                    var_l[n+2] = var_l[n+2] * -1
                    var_l[n+1] = ""
                elif var_l[n+1] == " " and var_l[n+2] == "-":
                    var_l[n+3] = var_l[n+3] * -1
                    var_l[n+2] = ""

def clean_vvod(): # Удаление пробелов.
    n = 0
    global var_2
    var_2 = []
    for n in range(len(var_l)):
        if var_l[n] != " ":
            var_2.append(var_l[n])

def goin_vvod(): # Сращивание разрозненных цифр в одну строку
    global var_3
    global var_4
    var_3 = []
    var_4 = []
    n = 0
    f = str()
    for n in range(len(var_2)):
        if type(var_2[n]) == int:
            f = f + str(var_2[n])
        else:
            var_3.append(f)
            var_3.append(var_2[n])
            f = str()
    var_3.append(f)
    for n in range(len(var_3)):
        if var_3[n] != "":
            var_4.append(var_3[n])

def fin_var(): # Преобразование строк цифр в числа
    global var_fin
    var_fin = []
    n = 0
    for n in range(len(var_4)):
        if var_4[n] == "+" or var_4[n] == "-" or var_4[n] == "/" or var_4[n] == "*" \
            or var_4[n] == "i" or var_4[n] == "j" or var_4[n] == "(" or var_4[n] == ")":
            var_fin.append(var_4[n])
        else:
            h = int(var_4[n])
            var_fin.append(h)


# InList = [2, '+', '(', 96, '-', 6, 'j', ')', '-', '(', 45, '+', 5, 'j', ')', '*', 4, '/', '(', -45, '+', 19, 'j', ')'] # Input data

def Complex_calculator(inlist):
    
    for i in range(len(inlist)): # Remove "()" and include complex numbers into sub-lists
        intl = []
        temp = 0
        if inlist[i] == '(':
            for k in range(i + 1, i + 4):
                temp = inlist[k]
                intl.append(temp)
                inlist[i] = intl

    # print(f'\nInput list after first filter: {inlist}')

    def filter_list(mylist): # Remove "trash": elements remained after first filter (like: 45, '-', 6, 'j', ')')
        i = 0
        while i < len(mylist):
                if type(mylist[i]) == list:
                    mylist.pop(i + 1)
                i += 1
        return mylist

    for count in range(5):
        inlist = filter_list(inlist)

    # print(f'\nInput list after second filter: {inlist}')

    for i in range(len(inlist)): # Remove "+" and "-" in sub-lists
        if type(inlist[i]) == list:
            for k in range(len(inlist[i]) - 1):
                if inlist[i][k] == '+':
                    inlist[i].remove(inlist[i][k])
                elif inlist[i][k] == '-':
                    inlist[i][k + 1] = 0 - inlist[i][k + 1]
                    inlist[i].remove(inlist[i][k])
    
    # print(f'\nInput list after third filter: {inlist}')

    for i in range(len(inlist)): # Transform real number into complex one based on statement: a = a + 0j
        inner = []
        if type(inlist[i]) != list and type(inlist[i]) != str:
            inner.append(inlist[i])
            inner.append(0)
            inlist[i] = inner
    
    # print(f'\nInput list after fourth filter: {inlist}')

    def multiplication(list1, list2): # Multiplication formula used: (a + bj) * (c + dj) = (ac - bd) + (bc + ad)
        x1 = 0
        x2 = 0
        mult_list = []
        for i in range(len(list1) - 1):
            x1 = ((list1[i] * list2[i]) - (list1[i+1] * list2[i + 1]))
            x2 = ((list1[i+1] * list2[i]) + (list1[i] * list2[i + 1]))
            mult_list.append(round(x1, 3))
            mult_list.append(round(x2, 3))
            return mult_list

    def division(list1, list2): # Division formula used: (a + bj) / (c + dj) = ((ac + bd) / (c^2 + d^2)) + ((bc - ad) / (c^2 + d^2)) 
        x1 = 0
        x2 = 0
        div_list = []
        for i in range(len(list1) - 1):
            x1 = ((list1[i] * list2[i]) + (list1[i+1] * list2[i + 1])) / (list2[i]**2 + list2[i + 1]**2)
            x2 = ((list1[i+1] * list2[i]) - (list1[i] * list2[i + 1])) / (list2[i]**2 + list2[i + 1]**2)
            div_list.append(round(x1, 3))
            div_list.append(round(x2, 3))
            return div_list

    def addition(list1, list2):
        x1 = 0
        x2 = 0
        add_list = []
        for i in range(len(list1) - 1):
            x1 = list1[i] + list2[i]
            x2 = list1[i+1] + list2[i + 1]
            add_list.append(round(x1, 3))
            add_list.append(round(x2, 3))
            return add_list

    def subtraction(list1, list2):
        x1 = 0
        x2 = 0
        sub_list = []
        for i in range(len(list1) - 1):
            x1 = list1[i] - list2[i]
            x2 = list1[i+1] - list2[i + 1]
            sub_list.append(round(x1, 3))
            sub_list.append(round(x2, 3))
            return sub_list

    count_add = count_mult = 0
    for i in inlist:
        if i == '*' or i == '/':
            count_mult = count_mult + 1
        elif i == '+' or i == '-':
            count_add = count_add + 1

        for j in range(count_mult+1):

            for i in range(len(inlist) - 1):
                if inlist[i] == '*':
                    inlist[i] = multiplication(inlist[i - 1], inlist[i + 1])
                    inlist.pop(i - 1)
                    inlist.pop(i)
                    # print(inlist)
                    break

                elif inlist[i] == '/':
                    inlist[i] = division(inlist[i - 1], inlist[i + 1])
                    inlist.pop(i - 1)
                    inlist.pop(i)
                    # print(inlist)
                    break

    for j in range(count_add+1):

        for i in range(len(inlist) - 1):
            if inlist[i] == '+':
                inlist[i] = addition(inlist[i - 1], inlist[i + 1])
                inlist.pop(i - 1)
                inlist.pop(i)
                # print(inlist)
                break

            elif inlist[i] == '-':
                inlist[i] = subtraction(inlist[i - 1], inlist[i + 1])
                inlist.pop(i - 1)
                inlist.pop(i)
                # print(inlist)
                break
    
    out_string = ''
    if inlist[0][1] > 0:
        out_string = f'{inlist[0][0]} + {inlist[0][1]}j'
        return out_string
    else:
        out_string = f'{inlist[0][0]} - {abs(inlist[0][1])}j'
        return out_string

# CompResult = Complex_calculator(InList)
# print(f'\nYour result: {CompResult}\n')

# text =['56','/','8','-','14']

def calculation (list):
    for i in list:
        if isinstance(i,str)==False:
            i=str(i)
    # print(list)
    count_add = count_mult = 0
    for i in list:
        if i == '*' or i == '/':
            count_mult = count_mult + 1
        elif i == '+' or i == '-':
            count_add = count_add + 1

        for j in range(count_mult+1):

            for i in range(len(list) - 1):
                if list[i] == '*':
                    list[i] = int(list[i + 1]) * int(list[i - 1])
                    list.pop(i - 1)
                    list.pop(i)
                    # print(list)
                    break

                elif list[i] == '/':
                    list[i] = int(list[i -1]) / int(list[i + 1])
                    list.pop(i - 1)
                    list.pop(i)
                    # print(list)
                    break

    for j in range(count_add+1):

        for i in range(len(list) - 1):
            if list[i] == '+':
                list[i] = int(list[i + 1]) + int(list[i - 1])
                list.pop(i - 1)
                list.pop(i)
                # print(list)
                break

            elif list[i] == '-':
                list[i] = int(list[i - 1]) - int(list[i + 1])
                # print(list[i+1])
                list.pop(i - 1)
                list.pop(i)
                # print(list)
                break
    return (list)

# calculation(text)

def make_answer (s,dig, error):
    s = "".join(s)
    dig = "".join(map(str, dig))
    answer=''
    current_date_time =str(datetime.datetime.now())
    if error==True: answer=current_date_time+' '+ s+' '+'решение не может быть найдено, ошибка в выражении '+'\n'
    else:
        answer=current_date_time+' '+s+' = '+dig+'\n'
    return answer

def save_log(answer_in_string):
    with open("log.txt", 'a', encoding='utf-8') as fh:

        fh.write(answer_in_string)


@bot.message_handler(commands=['start'])
def start_message(message):
    global data
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/Команды', '/Логи')
    bot.send_message(message.chat.id, 'Привет! \n \
    Это калькулятор простых и комплексных числел! \n \
        Чтобы посмотреть доступные команды, нажми кнопку "Команды" \n \
        Чтобы посмотреть историю вычислений, нажми кнопку "Логи"', reply_markup=keyboard)
    
@bot.message_handler(commands=['Команды'])
def comands_message(message):
    bot.send_message(message.chat.id,'Чтобы посчитать просто число, введи команду: \n \
        /Простое и через пробел уравнение (все знаки и числа через пробел)\n \
            /Простое 2 + 3')
    bot.send_message(message.chat.id,'Чтобы посчитать комплексное число, введите команду: \n \
        /Комплексное и через пробел уравнение (все знаки и числа через пробел)  \n \
            /Комплексное 2 + 3 j')

@bot.message_handler(commands=['Логи'])
def comands_message(message):
    global data
    with open('log.txt', 'rb') as file:
        data = file.read()
    bot.send_message(message.chat.id, data)

@bot.message_handler(content_types='text')
def check_message(message):
    global msg
    global var1
    if '/Комплексное' in message.text:
        msg = message.text
        msg = msg.split(' ')
        msg.pop(0)
        print(msg)
        var1 = msg
        transform_vvod()
        clean_vvod()
        goin_vvod()
        fin_var()
        print(var_fin)
        CompResult = Complex_calculator(var_fin)
        print(CompResult)
        bot.send_message(message.chat.id,CompResult)
        save_log(make_answer(var1, var_fin, False))

    elif '/Простое' in message.text:
        # bot.send_message(message.chat.id,'Удалили!')
        msg = message.text
        msg = msg.split(' ')
        msg.pop(0)
        print(msg)
        var1 = msg
        transform_vvod()
        clean_vvod()
        goin_vvod()
        fin_var()
        print(var_fin)
        CompResult = calculation(var_fin)
        print(CompResult)
        bot.send_message(message.chat.id,CompResult)
        save_log(make_answer(var1, var_fin, False))

bot.polling()

# quest = message.text.split()[1:]
#     qq=" ".join(quest)
#     data = { 'question_raw': [qq]}
#     try:
#         res = requests.post(API_URL,json=data,verify=False).json()
#         bot.send_message(message.chat.id, res)
#     except:
#         bot.send_message(message.chat.id, "Что-то я ничего не нашел :-(")
# API_URL='https://7012.deeppavlov.ai/model'

# def norm_zp(zp):
#   return zp/12*10000*75
#   df['median_income'] = df['median_income'].apply(norm_zp) затирают прошлые значения


