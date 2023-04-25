from flask import Flask, request
from telegram import Update
from telegram.ext import Dispatcher, Updater, MessageHandler, CommandHandler, Filters,CallbackQueryHandler
import os
from db import DB
import telegram
from bot import start,menu,view_products,get_product,next_product,get_phone,add_card,remove_product,View_Cart,Contact_Us,phone_num,address,location,email,About_Us,see_products,order,clear_cart
TOKEN = "6137784963:AAE5gShzTjlruzEvLkbJkIqzQs-tpWf0sjY"

bot = telegram.Bot(TOKEN)
db = DB('SmartphoneBot/db.json')
app = Flask(__name__)
@app.route("/webhook", methods=["POST"])
def home():
    dp = Dispatcher(bot, None, workers=0)
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dp.add_handler(CommandHandler("start", start))
    # 1
    dp.add_handler(CallbackQueryHandler(view_products, pattern="View Products"))
    dp.add_handler(CallbackQueryHandler(get_product, pattern="brend_"))
    dp.add_handler(CallbackQueryHandler(next_product, pattern="nextright"))
    dp.add_handler(CallbackQueryHandler(view_products, pattern="view_products"))
    dp.add_handler(CallbackQueryHandler(add_card, pattern="addcard_"))
    dp.add_handler(CallbackQueryHandler(get_phone, pattern="product_"))


    # 2
    dp.add_handler(CallbackQueryHandler(View_Cart, pattern="View Cart"))
    dp.add_handler(CallbackQueryHandler(see_products, pattern="Cart"))
    dp.add_handler(CallbackQueryHandler(View_Cart, pattern="bosh_view"))
    dp.add_handler(CallbackQueryHandler(order, pattern="Order"))
    dp.add_handler(CallbackQueryHandler(clear_cart, pattern="Clear cart"))

    # 3
    dp.add_handler(CallbackQueryHandler(Contact_Us, pattern="Contact Us"))
    dp.add_handler(CallbackQueryHandler(phone_num, pattern="Phone number"))
    dp.add_handler(CallbackQueryHandler(address, pattern="Address"))
    dp.add_handler(CallbackQueryHandler(location, pattern="Location"))
    dp.add_handler(CallbackQueryHandler(email, pattern="Email"))
    # 4
    dp.add_handler(CallbackQueryHandler(About_Us, pattern="About Us"))
    dp.add_handler(CallbackQueryHandler(menu, pattern="bosh_menu"))
    dp.process_update(update)
    return 'ok'
if __name__ == "__main__":
    app.run(debug=True)