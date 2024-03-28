import telebot
from telebot import types
from config import token, admin

bot = telebot.TeleBot(token)
messages = {
    'welcome': 'Привет, {name}. Чем могу помочь?',
    'sec_welcome': 'Я могу помочь чем-то ещё?',
    'services': {
        'price_list': 'Прайс услуг:\nСоздание сайтов - от 3000 рублей за услугу\nНаписание телеграм ботов - от 500 рублей за услугу\nАренда выделенных серверов - от 5 рублей (за 12 часов)',
        'learn_request': 'Пожалуйста опишите, чему бы вы хотели научиться',
        'work_request': 'Пожалуйста опишите, что вас заинтересовало'
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    global name
    name = message.from_user.first_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Прайс услуг', 'Подать заявку на обучение', 'Заказать услугу', 'Сотрудничество']
    markup.add(*[types.KeyboardButton(text=button) for button in buttons])
    bot.send_message(message.chat.id, text=messages['welcome'].format(name=name), reply_markup=markup)
    bot.register_next_step_handler(message, funcs)

def p(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Прайс услуг', 'Подать заявку на обучение', 'Заказать услугу', 'Сотрудничество']
    markup.add(*[types.KeyboardButton(text=button) for button in buttons])
    bot.send_message(message.chat.id, text=messages['sec_welcome'], reply_markup=markup)
    bot.register_next_step_handler(message, funcs)

def funcs(message):
    if message.text == 'Прайс услуг':
        bot.send_message(message.chat.id, text=messages['services']['price_list'])
        p(message)
    elif message.text == 'Подать заявку на обучение':
        bot.send_message(message.chat.id, text=messages['services']['learn_request'])
        bot.register_next_step_handler(message, teach)
    elif message.text == 'Заказать услугу':
        bot.send_message(message.chat.id, text=messages['services']['work_request'])
        bot.register_next_step_handler(message, work)
    elif message.text == 'Сотрудничество':
        us = message.from_user.username
        bot.send_message(message.chat.id, text='Ваша заявка отправлена, в скором времени с вами свяжется наш представитель')
        bot.send_message(admin, text=f'Заявка на сотрудничество от @{us}')
        p(message)
    else:
        bot.send_message(message.chat.id, text='Пожалуйста, пользуйтесь навигационными кнопками')
        p(message)

def teach(message):
    text = message.text
    us = message.from_user.username
    bot.send_message(message.chat.id, text='Ваша заявка отправлена, в скором времени с вами свяжется наш представитель')
    bot.send_message(admin, text=f'Заявка на обучение от @{us}\nпожелания клиента: {text}')
    p(message)

def work(message):
    text = message.text
    us = message.from_user.username
    bot.send_message(message.chat.id, text='Ваша заявка отправлена, в скором времени с вами свяжется наш представитель')
    bot.send_message(admin, text=f'Заявка на работу от @{us}\nпожелания клиента: {text}')
    p(message)

bot.polling()