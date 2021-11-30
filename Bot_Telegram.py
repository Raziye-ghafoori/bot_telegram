from telebot import types
import telebot
from khayyam import JalaliDatetime
from gtts import gTTS
import random
import qrcode

bot= telebot.TeleBot("2116443669:AAF8TaVS_hJhAMViMUhkIBFtHPxhHZPYxh4")

@bot.message_handler(commands=['start'])
def wellcom(message):
    bot.reply_to(message,"wellcom "+(message.chat.first_name))
    bot.send_message(message.chat.id,"please enter /help for more information")

@bot.message_handler(commands=['age'])
def user_age(message):
    message_age=bot.send_message(message.chat.id,'send me your age!! e.g.1390/4/16')
    bot.register_next_step_handler(message_age,age1)
def age1(message):
    userBirth = message.text.split('/')
    if len(userBirth)==3:
            num_day = JalaliDatetime.now() - JalaliDatetime(userBirth[0], userBirth[1], userBirth[2])
            bot.reply_to(message, 'You age is '+ str(num_day.days//365))
    else:
            bot.reply_to(message, ' !!wrong!! ')

@bot.message_handler(commands=['voice'])
def con_text2voi(message):
    text=bot.send_message(message.chat.id,'send me your text .pleas send english ,I only know english')
    bot.register_next_step_handler(text,text2voice)   
def text2voice(message):
    voice=gTTS(text=message.text,lang="en",slow=False)
    voice.save("voice.ogg")
    voice_sent=open("voice.ogg",'rb')
    bot.send_voice(message.chat.id,voice_sent)

box_game=types.ReplyKeyboardMarkup(row_width=2)
key_box1=types.KeyboardButton("🎮New Game🎮")
key_box2=types.KeyboardButton("Exit")
box_game.add(key_box1,key_box2)

@bot.message_handler(commands=['game'])
def game_handler(message):
    click=bot.send_message(message.chat.id,"click for start",reply_markup=box_game)
    bot.register_next_step_handler(message,Click)
def Click(message):
    if message.text=="🎮New Game🎮":
        message_key=bot.send_message(message.chat.id,"enter between 0 to 50",reply_markup=box_game)
        bot.register_next_step_handler(message_key,Game)
        global number_pc
        number_pc=random.randint(0,50)
    elif message.text=="Exit":
        bot.send_message(message.chat.id,"please enter /help for more information",reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
    else:
        bot.reply_to(message=message,text="what did you send? i do not understand😕")
def Game(message):
    try:         
        if int(message.text)==number_pc:
            bot.send_message(message.chat.id,"👏")
            bot.send_message(message.chat.id,"You Win",reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
                
        elif int(message.text) > number_pc:
            message_new=bot.send_message(message.chat.id,"lower")
            bot.register_next_step_handler(message_new,Game)
        elif int(message.text) < number_pc:
            message_new=bot.send_message(message.chat.id,"higher")
            bot.register_next_step_handler(message_new,Game)
        elif  0<int(message.text)<50:
            bot.send_message(message.chat.id,"🤦opss!! your number is not betweem 0 to 50 🤦")
                
    except:
        bot.reply_to(message=message,text="what did you send? i do not understand😕")

@bot.message_handler(commands=['qrcode'])
def send_Qrcode(message):
    Text=bot.send_message(message.chat.id,"send me your text:")
    bot.register_next_step_handler(Text,make_qrcode)
def make_qrcode(message):
    qc=qrcode.make(message.text)
    qc.save("qc_bot.png")
    pec=open("qc_bot.png","rb")
    bot.send_photo(message.chat.id,pec)

@bot.message_handler(commands=['help'])
def Help(message):
    bot.send_message(message.chat.id,"/start --> Start the bot \n /game --> Play  game with bot \n /age --> Calculate age \n /voice --> Convert text to voice \n /max --> Get max of arry \n /argmax --> Get argument max of arry \n /qrcode --> Convert text to qrcode")(commands=['max'])

@bot.message_handler(commands=['max'])
def Max_handler(message):
    text_user=bot.send_message(message.chat.id,"send me a array e.p.1,2,6,3 ")
    bot.register_next_step_handler(text_user,Max)
def Max(message):
    try:
        array=list(map(int,message.text.split(",")))
        bot.reply_to(message=message,text="Max is "+str(max(array)))
    except:
        bot.reply_to(message=message,text="what did you send? i do not understand😕")

@bot.message_handler(commands=['argmax'])
def argMax_handler(message):
    text_user=bot.send_message(message.chat.id,"send me a array e.p.1,2,6,3 ")
    bot.register_next_step_handler(text_user,argMax)
def argMax(message):
    try:
        array=list(map(int,message.text.split(",")))
        m=max(array)
        for i in range(len(array)):
            if array[i] == m:
                bot.reply_to(message=message,text="Argument of max is "+str(i))
                break
    except:
        bot.reply_to(message=message,text="what did you send? i do not understand😕")

@bot.message_handler(func= lambda message :True)
def other(message):
    bot.reply_to(message=message,text="what did you send? i do not understand😕")
    bot.send_message(message.chat.id,"please enter /help for more information")

bot.infinity_polling()