import telegram

TOKEN= "6137784963:AAE5gShzTjlruzEvLkbJkIqzQs-tpWf0sjY"
url = "https://Davron0703qwerty1234.pythonanywhere.com/webhook"
bot = telegram.Bot(TOKEN)

print(bot.set_webhook(url))