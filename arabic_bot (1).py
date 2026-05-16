#!/usr/bin/env python3
"""
Arab tilini o'rgatuvchi Telegram Bot
O'rnatish: pip install python-telegram-bot
Ishga tushirish: python arabic_bot.py
"""

import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Logging sozlamasi
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot tokeningizni shu yerga kiriting
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# =====================
# MA'LUMOTLAR BAZASI
# =====================

HARFLAR = [
    {"harf": "ا", "ism": "Alif", "talaffuz": "A / Aa"},
    {"harf": "ب", "ism": "Ba", "talaffuz": "B"},
    {"harf": "ت", "ism": "Ta", "talaffuz": "T"},
    {"harf": "ث", "ism": "Sa", "talaffuz": "S (yumshoq)"},
    {"harf": "ج", "ism": "Jim", "talaffuz": "J"},
    {"harf": "ح", "ism": "Ha", "talaffuz": "H (tomoqdan)"},
    {"harf": "خ", "ism": "Xa", "talaffuz": "X"},
    {"harf": "د", "ism": "Dal", "talaffuz": "D"},
    {"harf": "ذ", "ism": "Zal", "talaffuz": "Z (til bilan)"},
    {"harf": "ر", "ism": "Ra", "talaffuz": "R"},
    {"harf": "ز", "ism": "Zayn", "talaffuz": "Z"},
    {"harf": "س", "ism": "Sin", "talaffuz": "S"},
    {"harf": "ش", "ism": "Shin", "talaffuz": "Sh"},
    {"harf": "ص", "ism": "Sod", "talaffuz": "S (og'ir)"},
    {"harf": "ض", "ism": "Dod", "talaffuz": "D (og'ir)"},
    {"harf": "ط", "ism": "To", "talaffuz": "T (og'ir)"},
    {"harf": "ظ", "ism": "Zo", "talaffuz": "Z (og'ir)"},
    {"harf": "ع", "ism": "Ayn", "talaffuz": "' (tomoqdan)"},
    {"harf": "غ", "ism": "G'ayn", "talaffuz": "G'"},
    {"harf": "ف", "ism": "Fa", "talaffuz": "F"},
    {"harf": "ق", "ism": "Qof", "talaffuz": "Q"},
    {"harf": "ك", "ism": "Kof", "talaffuz": "K"},
    {"harf": "ل", "ism": "Lom", "talaffuz": "L"},
    {"harf": "م", "ism": "Mim", "talaffuz": "M"},
    {"harf": "ن", "ism": "Nun", "talaffuz": "N"},
    {"harf": "ه", "ism": "Ha", "talaffuz": "H"},
    {"harf": "و", "ism": "Vov", "talaffuz": "V / U"},
    {"harf": "ي", "ism": "Ya", "talaffuz": "Y / I"},
]

SOZLAR = [
    {"arab": "مرحبا", "ozbek": "Salom", "transkripsiya": "Marhaba"},
    {"arab": "شكرا", "ozbek": "Rahmat", "transkripsiya": "Shukran"},
    {"arab": "نعم", "ozbek": "Ha", "transkripsiya": "Na'am"},
    {"arab": "لا", "ozbek": "Yo'q", "transkripsiya": "Laa"},
    {"arab": "ماء", "ozbek": "Suv", "transkripsiya": "Maa'"},
    {"arab": "خبز", "ozbek": "Non", "transkripsiya": "Xubz"},
    {"arab": "بيت", "ozbek": "Uy", "transkripsiya": "Bayt"},
    {"arab": "كتاب", "ozbek": "Kitob", "transkripsiya": "Kitaab"},
    {"arab": "قلم", "ozbek": "Qalam", "transkripsiya": "Qalam"},
    {"arab": "مدرسة", "ozbek": "Maktab", "transkripsiya": "Madrasa"},
    {"arab": "أب", "ozbek": "Ota", "transkripsiya": "Ab"},
    {"arab": "أم", "ozbek": "Ona", "transkripsiya": "Umm"},
    {"arab": "ولد", "ozbek": "O'g'il bola", "transkripsiya": "Walad"},
    {"arab": "بنت", "ozbek": "Qiz bola", "transkripsiya": "Bint"},
    {"arab": "شمس", "ozbek": "Quyosh", "transkripsiya": "Shams"},
    {"arab": "قمر", "ozbek": "Oy", "transkripsiya": "Qamar"},
    {"arab": "سماء", "ozbek": "Osmon", "transkripsiya": "Samaa'"},
    {"arab": "أرض", "ozbek": "Yer", "transkripsiya": "Ard"},
    {"arab": "ماشاءالله", "ozbek": "Ajoyib!", "transkripsiya": "MaashaaAllah"},
    {"arab": "بسم الله", "ozbek": "Alloh nomi bilan", "transkripsiya": "Bismillah"},
]

SALOMLASHUVLAR = [
    {"arab": "السلام عليكم", "ozbek": "Assalomu alaykum", "transkripsiya": "As-salaamu alaykum"},
    {"arab": "وعليكم السلام", "ozbek": "Va alaykum assalom", "transkripsiya": "Wa alaykum as-salaam"},
    {"arab": "كيف حالك؟", "ozbek": "Qandaysiz?", "transkripsiya": "Kayfa haaluk?"},
    {"arab": "بخير، شكرا", "ozbek": "Yaxshi, rahmat", "transkripsiya": "Bikhair, shukran"},
    {"arab": "ما اسمك؟", "ozbek": "Ismingiz nima?", "transkripsiya": "Maa ismuk?"},
    {"arab": "اسمي ...", "ozbek": "Mening ismim ...", "transkripsiya": "Ismii ..."},
    {"arab": "من أين أنت؟", "ozbek": "Qayerdansiz?", "transkripsiya": "Min ayna ant?"},
    {"arab": "أنا من أوزبكستان", "ozbek": "Men O'zbekistondan", "transkripsiya": "Ana min Uzbekistan"},
    {"arab": "مع السلامة", "ozbek": "Xayr (sog'lomlik bilan)", "transkripsiya": "Ma'a as-salama"},
    {"arab": "إلى اللقاء", "ozbek": "Ko'rishguncha", "transkripsiya": "Ilaa al-liqaa'"},
]

# Conversation states
QUIZ_STATE = 1

# =====================
# ASOSIY BUYRUQLAR
# =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot boshlanish menyusi"""
    keyboard = [
        [InlineKeyboardButton("📖 Alifbo", callback_data="alifbo"),
         InlineKeyboardButton("💬 So'zlar", callback_data="sozlar")],
        [InlineKeyboardButton("👋 Salomlashuvlar", callback_data="salom"),
         InlineKeyboardButton("🧠 Test", callback_data="test")],
        [InlineKeyboardButton("📚 Dars rejimi", callback_data="dars")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🌙 *Arab tili o'rgatuvchi botga xush kelibsiz!*\n\n"
        "Men sizga arab tilini o'rgataman:\n"
        "📖 Alifbo — 28 ta arab harfi\n"
        "💬 So'zlar — zarur so'zlar va tarjimasi\n"
        "👋 Salomlashuvlar — kundalik iboralar\n"
        "🧠 Test — bilimingizni sinab ko'ring\n"
        "📚 Dars — ketma-ket o'rganish\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 *Mavjud buyruqlar:*\n\n"
        "/start — Bosh menyu\n"
        "/alifbo — Arab alifbosi\n"
        "/sozlar — So'zlar ro'yxati\n"
        "/salom — Salomlashuvlar\n"
        "/test — Bilimni sinash\n"
        "/dars — Dars rejimi\n"
        "/help — Yordam",
        parse_mode="Markdown"
    )

# =====================
# ALIFBO
# =====================

async def alifbo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["harf_index"] = 0
    await yuborish_harf(update, context, yangi=True)

async def yuborish_harf(update, context, yangi=False):
    idx = context.user_data.get("harf_index", 0)
    harf_info = HARFLAR[idx]

    matn = (
        f"📖 *Arab alifbosi — {idx + 1}/{len(HARFLAR)}*\n\n"
        f"🔤 Harf: `{harf_info['harf']}`\n"
        f"📛 Ismi: *{harf_info['ism']}*\n"
        f"🗣️ Talaffuz: _{harf_info['talaffuz']}_"
    )

    keyboard = []
    nav = []
    if idx > 0:
        nav.append(InlineKeyboardButton("⬅️ Oldingi", callback_data="harf_oldin"))
    if idx < len(HARFLAR) - 1:
        nav.append(InlineKeyboardButton("Keyingi ➡️", callback_data="harf_keyin"))
    if nav:
        keyboard.append(nav)
    keyboard.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if yangi:
        if update.message:
            await update.message.reply_text(matn, parse_mode="Markdown", reply_markup=reply_markup)
        else:
            await update.callback_query.message.reply_text(matn, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(matn, parse_mode="Markdown", reply_markup=reply_markup)

# =====================
# SO'ZLAR
# =====================

async def sozlar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["soz_index"] = 0
    await yuborish_soz(update, context, yangi=True)

async def yuborish_soz(update, context, yangi=False):
    idx = context.user_data.get("soz_index", 0)
    soz = SOZLAR[idx]

    matn = (
        f"💬 *Arab so'zlari — {idx + 1}/{len(SOZLAR)}*\n\n"
        f"🔤 Arab: `{soz['arab']}`\n"
        f"🇺🇿 O'zbek: *{soz['ozbek']}*\n"
        f"🗣️ Transkripsiya: _{soz['transkripsiya']}_"
    )

    keyboard = []
    nav = []
    if idx > 0:
        nav.append(InlineKeyboardButton("⬅️ Oldingi", callback_data="soz_oldin"))
    if idx < len(SOZLAR) - 1:
        nav.append(InlineKeyboardButton("Keyingi ➡️", callback_data="soz_keyin"))
    if nav:
        keyboard.append(nav)
    keyboard.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if yangi:
        if update.message:
            await update.message.reply_text(matn, parse_mode="Markdown", reply_markup=reply_markup)
        else:
            await update.callback_query.message.reply_text(matn, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(matn, parse_mode="Markdown", reply_markup=reply_markup)

# =====================
# SALOMLASHUVLAR
# =====================

async def salom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = "👋 *Arabcha salomlashuvlar:*\n\n"
    for s in SALOMLASHUVLAR:
        matn += f"🔤 `{s['arab']}`\n🇺🇿 {s['ozbek']}\n🗣️ _{s['transkripsiya']}_\n\n"

    keyboard = [[InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")]]

    if update.message:
        await update.message.reply_text(matn, parse_mode="Markdown",
                                         reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.message.reply_text(matn, parse_mode="Markdown",
                                                        reply_markup=InlineKeyboardMarkup(keyboard))

# =====================
# TEST
# =====================

async def test_boshlash(update, context):
    """Tasodifiy so'z testi"""
    barcha = SOZLAR + [{"arab": s["arab"], "ozbek": s["ozbek"], "transkripsiya": s["transkripsiya"]}
                       for s in SALOMLASHUVLAR]
    savol = random.choice(barcha)
    context.user_data["test_javob"] = savol["ozbek"]

    # 3 ta noto'g'ri javob + 1 ta to'g'ri
    noto_g_ri = random.sample(
        [s["ozbek"] for s in barcha if s["ozbek"] != savol["ozbek"]], 3
    )
    javoblar = noto_g_ri + [savol["ozbek"]]
    random.shuffle(javoblar)

    keyboard = [
        [InlineKeyboardButton(j, callback_data=f"test_{j}")] for j in javoblar
    ]
    keyboard.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")])

    matn = f"🧠 *Test savoli:*\n\nQuyidagi arabcha so'z o'zbekcha nima?\n\n`{savol['arab']}`\n_{savol['transkripsiya']}_"

    if update.message:
        await update.message.reply_text(matn, parse_mode="Markdown",
                                         reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.message.reply_text(matn, parse_mode="Markdown",
                                                        reply_markup=InlineKeyboardMarkup(keyboard))

# =====================
# DARS REJIMI
# =====================

async def dars_rejimi(update, context):
    matn = (
        "📚 *Dars rejimi — bosqichlar:*\n\n"
        "1️⃣ Alifboni o'rganing\n"
        "   👉 /alifbo\n\n"
        "2️⃣ Asosiy so'zlarni yod oling\n"
        "   👉 /sozlar\n\n"
        "3️⃣ Salomlashuvlarni mashq qiling\n"
        "   👉 /salom\n\n"
        "4️⃣ Bilimingizni test bilan sinang\n"
        "   👉 /test\n\n"
        "💡 *Maslahat:* Har kuni 10 daqiqa mashq qilsangiz, 1 oyda arab tilida salomlasha olasiz!"
    )
    keyboard = [[InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")]]

    if update.message:
        await update.message.reply_text(matn, parse_mode="Markdown",
                                         reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.message.reply_text(matn, parse_mode="Markdown",
                                                        reply_markup=InlineKeyboardMarkup(keyboard))

# =====================
# CALLBACK HANDLER
# =====================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu":
        keyboard = [
            [InlineKeyboardButton("📖 Alifbo", callback_data="alifbo"),
             InlineKeyboardButton("💬 So'zlar", callback_data="sozlar")],
            [InlineKeyboardButton("👋 Salomlashuvlar", callback_data="salom"),
             InlineKeyboardButton("🧠 Test", callback_data="test")],
            [InlineKeyboardButton("📚 Dars rejimi", callback_data="dars")],
        ]
        await query.message.reply_text(
            "🏠 *Bosh menyu* — nimani o'rganmohchisiz?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "alifbo":
        context.user_data["harf_index"] = 0
        await yuborish_harf(update, context)

    elif data == "harf_keyin":
        context.user_data["harf_index"] = context.user_data.get("harf_index", 0) + 1
        await yuborish_harf(update, context)

    elif data == "harf_oldin":
        context.user_data["harf_index"] = max(0, context.user_data.get("harf_index", 0) - 1)
        await yuborish_harf(update, context)

    elif data == "sozlar":
        context.user_data["soz_index"] = 0
        await yuborish_soz(update, context)

    elif data == "soz_keyin":
        context.user_data["soz_index"] = context.user_data.get("soz_index", 0) + 1
        await yuborish_soz(update, context)

    elif data == "soz_oldin":
        context.user_data["soz_index"] = max(0, context.user_data.get("soz_index", 0) - 1)
        await yuborish_soz(update, context)

    elif data == "salom":
        await salom_command(update, context)

    elif data == "test":
        await test_boshlash(update, context)

    elif data.startswith("test_"):
        javob = data[5:]
        to_g_ri = context.user_data.get("test_javob", "")

        if javob == to_g_ri:
            matn = "✅ *To'g'ri javob!* Zo'r!\n\nYana bir savol?"
        else:
            matn = f"❌ *Noto'g'ri.* To'g'ri javob: *{to_g_ri}*\n\nYana sinab ko'rasizmi?"

        keyboard = [
            [InlineKeyboardButton("🔄 Yana test", callback_data="test")],
            [InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")],
        ]
        await query.edit_message_text(matn, parse_mode="Markdown",
                                       reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "dars":
        await dars_rejimi(update, context)

# =====================
# MAIN
# =====================

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Buyruqlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("alifbo", alifbo_command))
    app.add_handler(CommandHandler("sozlar", sozlar_command))
    app.add_handler(CommandHandler("salom", salom_command))
    app.add_handler(CommandHandler("test", test_boshlash))
    app.add_handler(CommandHandler("dars", dars_rejimi))

    # Callback handler
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
