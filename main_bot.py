import telebot
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telebot import types
from fractions import Fraction
bot = telebot.TeleBot('YOUR TOKEN')
storage = {}

def init_storage(user_id):
  storage[user_id] = dict(first_number=None, second_number=None)

def store_number(user_id, key, value):
  storage[user_id][key] = dict(value=value)

def get_number(user_id, key):
  return storage[user_id][key].get('value')

@bot.message_handler(func=lambda m: True)
def start(message):

    init_storage(message.from_user.id)
    bot.reply_to(message, f"Привет я бот - калькулятор комплексных и рациональных чисел, чтобы запустить нажми 1")
    bot.register_next_step_handler(message, numbers)

def numbers(message):
      if message.text == "1":
         bot.reply_to(message,"Введите 1е число: ")
         bot.register_next_step_handler(message, plus_one)
      else:
         bot.reply_to(message, "Введите + чтобы прибавить два числа ")
         bot.register_next_step_handler(message, plus_one)

def plus_one(message):
        first_number = message.text

        if not first_number.isdigit():
            msg = bot.reply_to(message, 'Enter only digits!')
            bot.register_next_step_handler(message, plus_one)
            return

        store_number(message.from_user.id, "first_number", first_number)
        bot.reply_to(message, "Введите 2е число: ")
        bot.register_next_step_handler(message, plus_two)

def plus_two(message):
       second_number = message.text

       if not second_number.isdigit():
            msg = bot.reply_to(message, 'Enter only digits!')
            bot.register_next_step_handler(message, plus_two)
            return

       store_number(message.from_user.id, "second_number", second_number)
       bot.reply_to(message, "Введите 3е число: ")
       bot.register_next_step_handler(message, plus_third)



def plus_third(message):
    third_number = message.text

    if not third_number.isdigit():
        msg = bot.reply_to(message, 'Enter only digits!')
        bot.register_next_step_handler(message, plus_third)
        return


    store_number(message.from_user.id, "third_number", third_number)
    bot.reply_to(message, "Введите 4ое число: ")
    bot.register_next_step_handler(message, plus_four)


def plus_four(message):
    four_number = message.text

    if not four_number.isdigit():
        msg = bot.reply_to(message, 'Enter only digits!')
        bot.register_next_step_handler(message, plus_third)
        return

    store_number(message.from_user.id, "four_number", four_number)
    bot.reply_to(message, "Введите знак +,-,*,/: ")
    bot.register_next_step_handler(message, znak)
def znak(message):
    znak=message.text
    store_number(message.from_user.id, "znak", znak)


    bot.reply_to(message, "Какие числа будем вычислять -\n если комплексные нажми 1\n если рациональные нажми 2 ")
    bot.register_next_step_handler(message,enter)

def enter(message):
    number_1 = get_number(message.from_user.id, "first_number")
    number_2 = get_number(message.from_user.id, "second_number")
    number_3 = get_number(message.from_user.id, "third_number")
    number_4 = get_number(message.from_user.id, "four_number")
    znak = get_number(message.from_user.id, "znak")
    if message.text == "1":
     result_comp1=complex(int(number_1),int(number_2))
     result_comp2=complex(int(number_3),int(number_4))
     if znak == "+":
      res=result_comp1+result_comp2
      bot.reply_to(message, f"Ответ: {result_comp1}+{result_comp2}={res}")
     if znak == "-":
      res=result_comp1 - result_comp2
      bot.reply_to(message, f"Ответ: {result_comp1}-{result_comp2}={res}")
     if znak == "*":
      res = result_comp1 * result_comp2
      bot.reply_to(message, f"Ответ: {result_comp1}*{result_comp2}={res}")
     if znak == "/":
      res = result_comp1 / result_comp2
      bot.reply_to(message, f"Ответ: {result_comp1}/{result_comp2}={res}")
     with open('log_comp.csv', 'a', encoding='utf-8') as file:
         file.write(f'{result_comp1}{znak}{result_comp2}={res},\n')


    if message.text == "2":
     result_rat1=Fraction(int(number_1),int(number_2))
     result_rat2= Fraction(int(number_3), int(number_4))
     if znak == "+":
      res = result_rat1 + result_rat2
      bot.reply_to(message, f"Ответ: {result_rat1}+{result_rat2}={res}")
     if znak == "-":
      res = result_rat1 - result_rat2
      bot.reply_to(message, f"Ответ: {result_rat1}-{result_rat2}={res}")
     if znak == "*":
      res = result_rat1 * result_rat2
      bot.reply_to(message, f"Ответ: {result_rat1}*{result_rat2}={res}")
     if znak == "/":
      res = result_rat1 / result_rat2
      bot.reply_to(message, f"Ответ: {result_rat1}/{result_rat2}={res}")
     with open('log_rat.csv', 'a', encoding='utf-8') as file:
         file.write(f'{result_rat1}{znak}{result_rat2}={res},\n')





if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
 

