import telebot
from telebot import types
import requests

TOKEN = '1825027707:AAH3ed4JZf2Mq45APeI7wfh3RNpbqsQPBi4'

WEATHER_TOKEN = '71696acc811bae0ab8504bdb2b41638b'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help','profile','calc','weather'])
def start_bot(message):
    if message.text.lower() == '/start':
        keyboard = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Шутиечка',callback_data='joke')
    
   

        keyboard.add(btn)
    
     
        bot.send_message(message.chat.id,
                         'Всем привет!\n Я новый бот!Чем я могу вам помочь?',
                         reply_markup=keyboard)
    
    elif message.text.lower() == '/help':
        bot.send_message(message.chat.id, 'Вы в разделе помощь')
        
    elif message.text.lower() == '/profile':
        bot.send_message(message.chat.id, 'Вы вошли в профиль')
        bot.send_message(message.chat.id, 'Ведите ваше имя')
        bot.register_next_step_handler(message, enter_name)
        
    elif message.text.lower() == '/weather':
        bot.send_message(message.chat.id, 'Вы в разделе Погоды')
        bot.send_message(message.chat.id, 'Ведите название города')
        bot.register_next_step_handler(message, weather_menu)
        
    elif message.text.lower() =='/calc':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Сумма')
        btn2 = types.KeyboardButton('Минус')
        btn3 = types.KeyboardButton('Деление')
        btn4 = types.KeyboardButton('Умножение')
        keyboard.add(btn1)
        keyboard.add(btn2)
        keyboard.add(btn3)
        keyboard.add(btn4)
        
        bot.send_message(message.chat.id,
                         'Калькулятор! Выберите действие',
                         reply_markup=keyboard)
        
        bot.register_next_step_handler(message, calc_choose)
        
def calc_choose(message):
    if message.text.lower() == 'сумма':
        bot.send_message(message.chat.id, "Вы выбрали сумму.")
        bot.send_message(message.chat.id, "Введите числа через пробел")
        bot.register_next_step_handler(message, calc_result_sum)
        
    if message.text.lower() == 'минус':
        bot.send_message(message.chat.id, "Вы выбрали минус.")
        bot.send_message(message.chat.id, "Введите числа через пробел")
        bot.register_next_step_handler(message, calc_result_minus)
        
        
def calc_result_sum(message):
    nums = message.text.split()
    num1 = int (nums[0])
    num2 = int (nums[1])
    
    bot.send_message(message.chat.id, f"Результат {num1 + num2}")
                
def calc_result_minus(message):
    nums = message.text.split()
    num1 = int (nums[0])
    num2 = int (nums[1])
    
    bot.send_message(message.chat.id, f"Результат {num1 - num2}")

@bot.message_handler(content_type=['text'])
def enter_name(message):
    name = message.text
    bot.send_message(message.chat.id, f"Ваше имя: {name}")
    bot.send_message(message.chat.id, f"Ведите ваш возраст")
   

@bot.message_handler(content_type=['text'])
def enter_age(message):
    name = message.text
    bot.send_message(message.chat.id, f"Ваш возраст: {name}")
    bot.send_message(message.chat.id, f"Ведите ваш любимый фильм")
    bot.register_next_step_handler(message, enter_favorite_film)
    
@bot.message_handler(content_type=['text'])
def enter_favorite_film(message):
    name = message.text
    bot.send_message(message.chat.id, f"Ваш любимй фильм: {name}")
    bot.send_message(message.chat.id, f"Ведите ваш город")
    bot.register_next_step_handler(message, you_city)
    
@bot.message_handler(content_type=['text'])
def you_city(message):
    name = message.text
    bot.send_message(message.chat.id, f"Ваш город: {name}")
@bot.callback_query_handler(func=lambda x: x.data=='joke')
def joke_fn(message):
    bot.send_message(message.from_user.id,'колобок повесился')
    
def weather_menu(message):
    city = message.text
    API_URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_TOKEN}'
    r = requests.get(API_URL)
    w = r.json()
    bot.send_message(message.chat.id, f"В городе: {w['name']}")
    bot.send_message(message.chat.id, f"Температура: {w['main']['temp']-273.15}")
    
    

    
    
        
bot.polling()