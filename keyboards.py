from telebot import types


keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
btn1 = types.KeyboardButton('Да')
btn2 = types.KeyboardButton('Нет')
keyboard.add(btn1, btn2)

keyboard1 = types.ReplyKeyboardMarkup(one_time_keyboard=True)
bt = types.KeyboardButton('Python vol. 9')
bt1 = types.KeyboardButton('Python vol. 8')
bt2 = types.KeyboardButton('Python-9. Even')
bt4 = types.KeyboardButton('Python-8. Even')
bt5 = types.KeyboardButton('JavaScript vol. 9')
keyboard1.row(bt1, bt4)
keyboard1.row(bt, bt2)
keyboard1.row(bt5)
