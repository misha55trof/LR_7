
import psycopg2
import telebot
from telebot import types
from datetime import date

a=date.today()
b=int(a.strftime("%V"))
if b % 2!=0: 
    c=1
    
else: 
    c=0
    

conn = psycopg2.connect(database="ras_db",user="postgres",password="1",host="localhost",port="5432")
cursor = conn.cursor()

token = "5227472009:AAEPekrNIfg5VwRQCwMGfagYkeQsmCJwUkw"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['week'])
def start(message):
    if c==0:
        bot.send_message(message.chat.id,'Сейчас нижняя неделя')
    if c==1:
        bot.send_message(message.chat.id,'Сейчас верхняя неделя')

@bot.message_handler(commands=['mtuci'])
def start(message):
    bot.send_message(message.chat.id,'https://vk.com/memmtuci')

@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id,'Для получения рассписания на день, пришлите мне день недели. \n Если вы хотите узнать чётность недели, пришлите мне /week \n Если вы хотите, чтобы я вам скинул ссылку на мтуси, пишите /mtuci')

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Расписание на текущую неделю", "Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Здраствуйте, я ваш бот с расписанием, выберете день недели и я пришлю расписание на этот день! \n также можете нажать /help', reply_markup=keyboard)






@bot.message_handler(content_types=['text'])
def answer(message):
    weakDays = ['Понедельник', 'Вторник','Среда','Четверг','Пятница']
    if c==1:
        if message.text in weakDays:
    
            cursor.execute("select day, subject, room_numb,  start_time, full_name from timelable, teatcher where subject = subject1 and day = '" + message.text + "' order by timelable asc")
            records = list(cursor.fetchall())

        elif message.text == "Расписание на текущую неделю":
            cursor.execute("select day, subject, room_numb,  start_time, full_name from teatcher, timelable where subject = subject1 order by timelable asc ")
            records = list(cursor.fetchall())

        elif message.text == "Расписание на следующую неделю":
            cursor.execute("select day, subject, room_numb,  start_time, full_name from teatcher, timelable1 where subject = subject1 order by timelable1 asc ")
            records = list(cursor.fetchall())
    elif c==0:
        if message.text in weakDays:
    
            cursor.execute("select day, subject, room_numb,  start_time, full_name from timelable1, teatcher where subject = subject1 and day = '" + message.text + "'")
            records = list(cursor.fetchall())
        elif message.text == "Расписание на текущую неделю":
            cursor.execute("select day, subject, room_numb,  start_time, full_name from teatcher, timelable1 where subject = subject1 order by timelable1 asc ")
            records = list(cursor.fetchall())

        elif message.text == "Расписание на следующую неделю":
            cursor.execute("select day, subject, room_numb,  start_time, full_name from teatcher, timelable where subject = subject1 order by timelable asc ")
            records = list(cursor.fetchall())


    if (not message.text in weakDays) and message.text!="Расписание на следующую неделю" and message.text != "Расписание на текущую неделю" and message.text != "/help" and message.text != "/week" and message.text != "/start" and message.text != "/mtuci" :
        bot.send_message(message.chat.id,'Прошу прощения, но я не совсем вас понимаю, пользуйтесь кнопками или нажмите /help')
    else:
        d=records[0][0]
        bot.send_message(message.chat.id, d)
        f1=d
        for el in records:
            d=el[0]
            sub=el[1]
            n=el[2]
            s=el[3]
            f=el[4]
            if f1!=d:
                    f1=d
                    bot.send_message(message.chat.id, d) 
            t='Предмет: '+str(sub)+'\n'+'Аудитория: '+str(n)+'\n'+'Время начала: '+str(s)+'\n'+'Преподаватель: '+str(f)
            bot.send_message(message.chat.id, t)

    if (not message.text in weakDays) and message.text!="Расписание на следующую неделю" and message.text() == "Расписание на текущую неделю" and message.text() == "/help" and message.text() == "/week" and message.text() == "/start":
        bot.send_message(message.chat.id,'Прошу прощения, но я не совсем вас понимаю, пользуйтесь кнопками или нажмите /help')    
    






bot.infinity_polling()