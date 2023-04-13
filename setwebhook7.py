import telegram
import os

TOKEN= "6230194025:AAHTAoiyAjenRfBPEJ8fqcH2ssGZ9cIV5gs"
url = "https://Davron0703qwerty1234.pythonanywhere.com/webhook"
bot = telegram.Bot(TOKEN)

print(bot.set_webhook(url))