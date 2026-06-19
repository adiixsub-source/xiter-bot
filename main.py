import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import time as _time
from keep_alive import keep_alive

TOKEN = '8240347823:AAFuSBsYn-oa8UgzmVmRuxv4cRgKoFCyfSE'

ADMIN_ID = 6963083559

BINANCE_PAY_ID = "1045351326"
MIN_DEPOSIT = 30

LANGS = {
    "en": {
        "welcome": "Welcome to **XITER RESELLER BOT** 🛡️\n\nSelect a proxy plan or deposit funds to your account:",
        "btn_lang": "🇸🇦 العربية",
        "dep": "💰 Deposit Funds (Min $30)",
        "back_dep": "« Back to Deposit Menu",
        "back_main": "« Back to Menu",
        "dep_menu_title": "💳 **Deposit Funds**\n\n⚠️ Minimum deposit limit is **$30**.\nSelect your preferred payment method:",
        "out_of_stock": "❌ Out of stock! Please contact the admin.",
        "insufficient": "❌ Insufficient Balance! You need ${price} to buy this.",
        "purchase_ok": "✅ Purchase Successful!",
        "purchase_msg": "🎉 **Purchase Successful!**\n\n📦 Plan: **{days} PROXY PASS**\n🔑 Your Key: `{key}`\n\nThank you for trusting us!",
    },
    "ar": {
        "welcome": "أهلاً بك في **بوت XITER** 🛡️\n\nاختر باقة بروكسي أو أودع رصيداً في حسابك:",
        "btn_lang": "🇺🇸 English",
        "dep": "💰 إيداع رصيد (الحد الأدنى $30)",
        "back_dep": "« العودة لقائمة الإيداع",
        "back_main": "« العودة للقائمة",
        "dep_menu_title": "💳 **إيداع الرصيد**\n\n⚠️ الحد الأدنى للإيداع هو **$30**.\nاختر طريقة الدفع المفضلة:",
        "out_of_stock": "❌ المخزون فارغ! تواصل مع الآدمن.",
        "insufficient": "❌ رصيدك غير كافٍ! تحتاج ${price} لشراء هذه الباقة.",
        "purchase_ok": "✅ تمت عملية الشراء بنجاح!",
        "purchase_msg": "🎉 **تمت عملية الشراء بنجاح!**\n\n📦 الباقة: **{days} PROXY PASS**\n🔑 مفتاحك: `{key}`\n\nشكراً لثقتك بنا!",
    }
}

bot = telebot.TeleBot(TOKEN)

def init_db():
    conn = sqlite3.connect('xiter_database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, credits REAL DEFAULT 0.0, lang TEXT DEFAULT "en")')
    cursor.execute('CREATE TABLE IF NOT EXISTS keys (id INTEGER PRIMARY KEY AUTOINCREMENT, duration TEXT, key_val TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS deposit_admins (user_id INTEGER PRIMARY KEY)')
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN lang TEXT DEFAULT "en"')
    except:
        pass
    conn.commit()
    conn.close()

init_db()

def get_user_data(user_id):
    conn = sqlite3.connect('xiter_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT credits, lang FROM users WHERE user_id = ?', (user_id,))
    res = cursor.fetchone()
    conn.close()
    return res if res else (0.0, "en")

def update_user_balance(user_id, amount):
    conn = sqlite3.connect('xiter_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, credits, lang) VALUES (?, 0.0, "en")', (user_id,))
    cursor.execute('UPDATE users SET credits = credits + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

def set_lang(user_id, lang):
    conn = sqlite3.connect('xiter_database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET lang = ? WHERE user_id = ?', (lang, user_id))
    conn.commit()
    conn.close()

def is_deposit_admin(user_id):
    if user_id == ADMIN_ID:
        return True
    conn = sqlite3.connect('xiter_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM deposit_admins WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return bool(result)

def main_menu_keyboard(balance, lang):
    t = LANGS[lang]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(f"💳 Balance: ${balance}", callback_data="none"),
        InlineKeyboardButton(t["dep"], callback_data="menu_deposit"),
        InlineKeyboardButton("🔹 1 DAY PROXY PASS - $1", callback_data="buy_1"),
        InlineKeyboardButton("🔹 7 DAYS PROXY PASS - $3", callback_data="buy_3"),
        InlineKeyboardButton("🔹 31 DAYS PROXY PASS - $5", callback_data="buy_5"),
        InlineKeyboardButton(t["btn_lang"], callback_data="toggle_lang")
    )
    return markup

def deposit_menu_keyboard(lang):
    t = LANGS[lang]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🟡 Binance Pay", callback_data="dep_binance_pay"),
        InlineKeyboardButton("🎁 Binance Gift Card", callback_data="dep_gift_card"),
        InlineKeyboardButton("💬 Other Methods (Contact Owner)", callback_data="dep_other"),
        InlineKeyboardButton(t["back_main"], callback_data="menu_main")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('xiter_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, credits, lang) VALUES (?, 0.0, "en")', (user_id,))
    conn.commit()
    conn.close()

    balance, lang = get_user_data(user_id)
    bot.send_message(message.chat.id, LANGS[lang]["welcome"], reply_markup=main_menu_keyboard(balance, lang), parse_mode="Markdown")

@bot.message_handler(commands=['adm'])
def add_deposit_admin(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        new_adm = int(message.text.split()[1])
        conn = sqlite3.connect('xiter_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO deposit_admins (user_id) VALUES (?)', (new_adm,))
        conn.commit()
        conn.close()
        bot.reply_to(message, f"✅ تم تعيين `{new_adm}` كمساعد إيداع.", parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ **طريقة الاستخدام:**\n`/adm [ID]`", parse_mode="Markdown")

@bot.message_handler(commands=['ship'])
def admin_ship(message):
    if not is_deposit_admin(message.from_user.id):
        return
    try:
        args = message.text.split()
        player_id = int(args[1])
        amount = float(args[2])
        update_user_balance(player_id, amount)
        bot.reply_to(message, f"✅ **SUCCESS!**\n👤 User: `{player_id}`\n💵 Added: `${amount}`", parse_mode="Markdown")
        try:
            bot.send_message(player_id, f"🎉 **Deposit Successful!**\nYour account has been credited with `${amount}`.\nUse /start to view your updated balance.", parse_mode="Markdown")
        except:
            pass
    except:
        bot.reply_to(message, "⚠️ **Correct Usage:**\n`/ship [User_ID] [Amount]`", parse_mode="Markdown")

@bot.message_handler(commands=['users'])
def admin_users(message):
    if message.from_user.id != ADMIN_ID:
        return
    conn = sqlite3.connect('xiter_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, credits FROM users')
    users = cursor.fetchall()
    conn.close()

    text = f"👥 **Total Registered Users:** {len(users)}\n\n"
    for u in users:
        text += f"ID: `{u[0]}` | Balance: `${u[1]}`\n"
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['1d', '7d', '31d'])
def add_stock(message):
    if not is_deposit_admin(message.from_user.id):
        return
    try:
        command = message.text.split()[0].replace('/', '')
        key_value = message.text.split(maxsplit=1)[1]
        conn = sqlite3.connect('xiter_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO keys (duration, key_val) VALUES (?, ?)', (command, key_value))
        conn.commit()
        conn.close()
        bot.reply_to(message, f"✅ **تم إضافة المفتاح بنجاح!**\n📦 القسم: `{command}`\n🔑 المفتاح: `{key_value}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ **طريقة الاستخدام:**\n`/1d [المفتاح]`\n`/7d [المفتاح]`\n`/31d [المفتاح]`", parse_mode="Markdown")

@bot.message_handler(commands=['key'])
def show_stock(message):
    if not is_deposit_admin(message.from_user.id):
        return
    conn = sqlite3.connect('xiter_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT duration, key_val FROM keys')
    keys = cursor.fetchall()
    conn.close()

    if not keys:
        bot.reply_to(message, "📦 **المخزون فارغ تماماً حالياً.**", parse_mode="Markdown")
        return

    text = "📦 **المخزون الحالي للمفاتيح:**\n\n"
    for k in keys:
        text += f"▪️ فئة: `{k[0]}` | 🔑 `{k[1]}`\n"
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    balance, lang = get_user_data(user_id)
    t = LANGS[lang]

    if call.data == "none":
        bot.answer_callback_query(call.id)

    elif call.data == "toggle_lang":
        new_lang = "ar" if lang == "en" else "en"
        set_lang(user_id, new_lang)
        balance, new_lang = get_user_data(user_id)
        bot.edit_message_text(
            LANGS[new_lang]["welcome"], chat_id, msg_id,
            reply_markup=main_menu_keyboard(balance, new_lang),
            parse_mode="Markdown"
        )

    elif call.data == "menu_main":
        bot.edit_message_text(
            t["welcome"], chat_id, msg_id,
            reply_markup=main_menu_keyboard(balance, lang),
            parse_mode="Markdown"
        )

    elif call.data == "menu_deposit":
        bot.edit_message_text(
            t["dep_menu_title"], chat_id, msg_id,
            reply_markup=deposit_menu_keyboard(lang),
            parse_mode="Markdown"
        )

    elif call.data == "dep_binance_pay":
        back_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(t["back_dep"], callback_data="menu_deposit"))
        text = (
            f"🟡 **Binance Pay Instructions**\n\n"
            f"1. Open Binance App.\n"
            f"2. Send funds to Binance ID: `{BINANCE_PAY_ID}`\n"
            f"3. ⚠️ Must send minimum **${MIN_DEPOSIT}**\n\n"
            f"After sending, copy your Telegram ID (`{user_id}`) and the receipt, then send them to the Owner."
        )
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=back_markup, parse_mode="Markdown")

    elif call.data == "dep_gift_card":
        back_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(t["back_dep"], callback_data="menu_deposit"))
        text = (
            f"🎁 **Binance Gift Card**\n\n"
            f"Create a Binance Gift card of minimum **${MIN_DEPOSIT}**.\n\n"
            f"Send the Gift Card Code along with your Telegram ID (`{user_id}`) directly to the Owner."
        )
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=back_markup, parse_mode="Markdown")

    elif call.data == "dep_other":
        back_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(t["back_dep"], callback_data="menu_deposit"))
        bot.edit_message_text(
            "💬 For other payment methods, please contact the bot owner directly.",
            chat_id, msg_id, reply_markup=back_markup
        )

    elif call.data.startswith("buy_"):
        price = float(call.data.split("_")[1])

        if price == 1:
            days_name, db_duration = "1 DAY", "1d"
        elif price == 3:
            days_name, db_duration = "7 DAYS", "7d"
        elif price == 5:
            days_name, db_duration = "31 DAYS", "31d"
        else:
            return

        conn = sqlite3.connect('xiter_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, key_val FROM keys WHERE duration = ? LIMIT 1', (db_duration,))
        key_data = cursor.fetchone()

        if not key_data:
            conn.close()
            bot.answer_callback_query(call.id, t["out_of_stock"], show_alert=True)
            return

        if balance >= price:
            key_id, the_key = key_data
            update_user_balance(user_id, -price)
            cursor.execute('DELETE FROM keys WHERE id = ?', (key_id,))
            conn.commit()
            conn.close()

            bot.answer_callback_query(call.id, t["purchase_ok"], show_alert=True)
            bot.send_message(chat_id, t["purchase_msg"].format(days=days_name, key=the_key), parse_mode="Markdown")

            new_balance, _ = get_user_data(user_id)
            bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=main_menu_keyboard(new_balance, lang))

            try:
                bot.send_message(
                    ADMIN_ID,
                    f"🛒 **New Sale!**\n👤 User: `{user_id}`\n📦 Plan: `{days_name}`\n💵 Price: `${price}`\n🔑 Delivered Key: `{the_key}`",
                    parse_mode="Markdown"
                )
            except:
                pass
        else:
            conn.close()
            bot.answer_callback_query(call.id, t["insufficient"].replace("${price}", str(price)), show_alert=True)

keep_alive()
print("XITER RESELLER BOT IS RUNNING SECURELY...")

while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Connection error: {e}. Reconnecting in 5 seconds...")
        _time.sleep(5)
