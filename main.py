from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, 
    Dispatcher, 
    CallbackContext, 
    Filters, 
    MessageHandler, 
    CommandHandler, 
    CallbackQueryHandler)
import os
import json
from db import DB
from cartdb import Cart
from tinydb import TinyDB, Query

TOKEN="6137784963:AAE5gShzTjlruzEvLkbJkIqzQs-tpWf0sjY"
db = DB('db.json')
# updater = Updater(TOKEN)
get_product_data=Cart('cartdb.json')


def start(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = str(update.message.chat.id)
    button1 = InlineKeyboardButton(text = "🛍 View Products", callback_data="View Products")
    button2 = InlineKeyboardButton(text = "📦 View Cart", callback_data="View Cart")
    button3 = InlineKeyboardButton(text = "📞 Contact Us", callback_data="Contact Us")
    button4 = InlineKeyboardButton(text = "📝 About Us", callback_data="About Us")
    keyboard = InlineKeyboardMarkup([[button1, button2],[button3, button4]])
    bot.sendMessage(chat_id=chat_id, text="Assalomu alaykum! Xush kelipsiz.\nQuyidagi menyudan kerakli tugmani bosing", reply_markup=keyboard)



def menu(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
   
    button1 = InlineKeyboardButton(text = "🛍 View Products", callback_data="View Products")
    button2 = InlineKeyboardButton(text = "📦 View Cart", callback_data="View Cart")
    button3 = InlineKeyboardButton(text = "📞 Contact Us", callback_data="Contact Us")
    button4 = InlineKeyboardButton(text = "📝 About Us", callback_data="About Us")
    keyboard = InlineKeyboardMarkup([[button1, button2],[button3, button4]])
    query.edit_message_text(text='Bosh menu:', reply_markup=keyboard)
   
   
 # 1-bo`lim ///////////////////////////////////////////////////////////////////////////////////////////////////////  
   
def view_products(update: Update, context: CallbackContext)-> None:
    query = update.callback_query

    brends = db.get_tables()
    keyboard = []
    for brend in brends:
        btn = InlineKeyboardButton(
            text = brend.capitalize(),
            callback_data=f"brend_{brend}"
        )
        keyboard.append([btn])
    btn1 = InlineKeyboardButton(text="🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard.append([btn1])

    keyboard = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Quyidagi brandlardan birini tanlang!", reply_markup=keyboard)



def get_product(update: Update, context: CallbackContext) -> None:
    bot = context.bot
    query = update.callback_query

    chat_id = query.message.chat.id
   # doc_id=db1.get(doc_id=1)[f'{chat_id}']['count']
    data = query.data
    brend = data.split('_')[-1]
    products=db.get_phone_list(brend)
    #create key
    keyboard=[[],[]]
    phone_text=f"1-10/{len(products)}\n\n"
    pr_range = 10
    for i, phone in enumerate(products[:pr_range], 1):
        phone_text += f"{i}. {phone['name']} {phone['memory']}\n"
        # create button
        btn = InlineKeyboardButton(
            text = str(i), 
            callback_data=f"product_{brend}_{phone.doc_id}"
            )
        if i < 6:
            # 1 2 3 4 5
            keyboard[0].append(btn)
        else:
            # 6 7 8 9 10
            keyboard[1].append(btn)
    btn2 = InlineKeyboardButton(text="➡️", callback_data=f'nextright_{brend}_{pr_range}')
    keyboard.append([btn2])

    btn3 = InlineKeyboardButton(text="Brend", callback_data="view_products")
    keyboard.append([btn3])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(phone_text, reply_markup=reply_markup)





def next_product(update, context):
    query = update.callback_query
    data = query.data.split('_')
    text, brend, pr_range = data

    pr_range = int(pr_range)
    products = db.get_phone_list(brend)

    if len(products) < pr_range:
        pr_range = 0

    print(len(products), pr_range)
    keyboard = [[], []]
    phone_text = f"{pr_range}-{pr_range+10}/{len(products)}\n\n"

    for i, phone in enumerate(products[pr_range:pr_range+10], 1):
        phone_text += f"{i}. {phone['name']} {phone['memory']}\n"
        # create button
        btn = InlineKeyboardButton(
            text = str(i),
            callback_data=f"product_{brend}_{phone.doc_id}"
        )
        if i < 6:
            # 1 2 3 4 5
            keyboard[0].append(btn)
        else:
            # 6 7 8 9 10
            keyboard[1].append(btn)
    pr_range += 10
    btn2 = InlineKeyboardButton(text="➡️", callback_data=f'nextright_{brend}_{pr_range}')
    keyboard.append([btn2])

    btn3 = InlineKeyboardButton(text="Brend", callback_data="view_products")
    keyboard.append([btn3])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(phone_text, reply_markup=reply_markup)

    query.answer("Next")
def get_phone(update, context):
    bot  = context.bot
    query = update.callback_query
    data = query.data.split('_')
    text, brend, doc_id = data
    print(data)
    phone = db.getPhone(brend, int(doc_id))
    print(phone)
    price = phone['price']
    ram = phone['RAM']
    memory = phone['memory']
    name = phone['name']
    color = phone['color']
    img = phone['img_url']
    text = f"📲{name}\n\n🎨{color}\n💾{ram}/{memory}\n💰{price}\n\n@telefonBozor"
    btn1 = InlineKeyboardButton(text="Add Card", callback_data=f'addcard_{brend}_{doc_id}')
    btn2 = InlineKeyboardButton(text="❌", callback_data='removeproduct')
    keyboard = InlineKeyboardMarkup([ [btn1, btn2] ])
    bot.send_photo(chat_id=query.message.chat.id, photo=img, caption=text, reply_markup=keyboard)
def add_card(update, context):
    query = update.callback_query
    data = query.data.split('_')
    chat_id = query.message.chat.id
    textt,brend,doc_id=data
    # print(chat_id)
    # print(brend)
    # print(doc_id)
    phone = db.getPhone(brend, int(doc_id))
    # print(phone)
    get_product_data.add(brend=brend,doc_id=doc_id,chat_id=chat_id)
    query.answer("Done✅")

def remove_product(update, context):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)
    query.answer('deleted')



# 2-bo`lim ////////////////////////////////////////////////////////////////////////////////////

def View_Cart(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    button1 = InlineKeyboardButton(text = "🛒 Cart", callback_data="Cart")
    button2 = InlineKeyboardButton(text = "📦 Order", callback_data="Order")
    button3 = InlineKeyboardButton(text = " 📝 Clear cart", callback_data="Clear cart")
    button4 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard = InlineKeyboardMarkup([[button1,button2],[button3,button4]])
    query.edit_message_text(text='Cart menu:', reply_markup=keyboard)

def see_products(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    products=get_product_data.get_cart(chat_id=chat_id)
    if products!=[]:
        Total=0
        k=0
        text='🛒Xaridlar:\n'
        for i in products:
            k+=1
            brand=i['brand']
            doc_id=i['doc_id']
            phone=db.getPhone(brend=brand,idx=doc_id)
            Total+=int(phone['price'])
            text+=f"{k}. {phone['name']}  Narxi: {phone['price']}\n"
        text+=f"Jami: {Total}"    
        chat_id = query.message.chat.id
        button4 = InlineKeyboardButton(text = "Orqaga", callback_data="bosh_view")
        keyboard=InlineKeyboardMarkup([[button4]])
        bot.sendMessage(chat_id=chat_id, text=text,reply_markup=keyboard)
    else:
        button4 = InlineKeyboardButton(text = "Orqaga", callback_data="bosh_view")
        keyboard=InlineKeyboardMarkup([[button4]])
        bot.sendMessage(chat_id=chat_id, text='Savat Bo`sh\n',reply_markup=keyboard)
def order(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    query.answer('Buyurtmangiz yuborildi🚀')
def clear_cart(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    get_product_data.remove(chat_id=chat_id)
    query.answer('Cart tozalandi')

# 3-bo`lim ///////////////////////////////////////////////////////////////////////////////////

def Contact_Us(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    button1 = InlineKeyboardButton(text = "📞 Phone number", callback_data="Phone number")
    button2 = InlineKeyboardButton(text = "📌 Address", callback_data="Address")
    button3 = InlineKeyboardButton(text = "📍 Location", callback_data="Location")
    button4 = InlineKeyboardButton(text = "📧 Email", callback_data="Email")
    button5 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard = InlineKeyboardMarkup([[button1, button2],[button3, button4],[button5]])
    query.edit_message_text(text='Contact Us', reply_markup=keyboard)
def phone_num(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    button4 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard=InlineKeyboardMarkup([[button4]])
    bot.sendMessage(chat_id=chat_id, text='Murojat uchun:\n📞 +998 99 755 07 33\n📞 +998 94 665 07 33\n@telefonBozor',reply_markup=keyboard)
def address(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    button4 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard=InlineKeyboardMarkup([[button4]])
    bot.sendMessage(chat_id, text='📌Address:\n Samarqand viloyati\nQo`shrabot tumani\nbozorjoy maxallsi 312-uy\n@telefonBozor')
def location(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    bot.sendLocation(chat_id=chat_id,latitude=40.26834059511894,longitude=66.68811723628676)
def email(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    button4 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard=InlineKeyboardMarkup([[button4]])
    bot.sendMessage(chat_id=chat_id, text='📧 Email:\ndostqobilovdavron885@gmail.com\n@telefonBozor',reply_markup=keyboard)
# 4-b0`lim /////////////////////////////////////////////////////////////////////////////////////40.26834059511894, 66.68811723628676

def About_Us(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    button1 = InlineKeyboardButton(text = "📝 Company Information", callback_data="Company Information")
    button2 = InlineKeyboardButton(text = "📝 Shipping & Returns", callback_data="Shipping & Returns")
    button3 = InlineKeyboardButton(text = " 📝 Privacy Policy", callback_data="Privacy Policy")
    button4 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard = InlineKeyboardMarkup([[button1],[button2],[button3],[button4]])
    query.edit_message_text(text='About menu:', reply_markup=keyboard)
def Company_Information(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    text="""
    Telefon savdo botimizga tushunmagan joylaringizga quidagi textda javob topasiz
    lhjkmnhfdsfh,mnhbgfdsa
    dfbfgbdghngh
    hgdhn
    dghngh
    nghndgh
    nhgddddddddd edj greeeeeeeeeeeeeeeee gergerg erg argekrga
    gergghaergaerghuaerguaergiuaergbrg
    gergaegrghlaegargbgrg
    ergjaeora;geragregrghrg
    """
    button4 = InlineKeyboardButton(text ="Orqaga", callback_data="Orqaga")
    keyboard=InlineKeyboardMarkup([[button4]])
    bot.sendMessage(chat_id=chat_id, text=text,reply_markup=keyboard)

updater = Updater(token=TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
# 1
dp.add_handler(CallbackQueryHandler(view_products, pattern="View Products"))
dp.add_handler(CallbackQueryHandler(get_product, pattern="brend_"))
dp.add_handler(CallbackQueryHandler(next_product, pattern="nextright"))
dp.add_handler(CallbackQueryHandler(view_products, pattern="view_products"))
dp.add_handler(CallbackQueryHandler(add_card, pattern="addcard_"))
dp.add_handler(CallbackQueryHandler(get_phone, pattern="product_"))
dp.add_handler(CallbackQueryHandler(remove_product, pattern="removeproduct"))


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
dp.add_handler(CallbackQueryHandler(Company_Information, pattern="Company Information"))
dp.add_handler(CallbackQueryHandler(About_Us, pattern="Orqaga"))

updater.start_polling()
updater.idle()