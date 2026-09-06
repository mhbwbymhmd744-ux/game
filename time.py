import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

player_data = {}

# فایل‌آیدی‌های تصاویر ربات
MOBAD_PHOTO = "AgACAgQAAxkBAAEiVp5qnLahWfxLm0jny5nj20ZGVEdeawACgBRrGzUC6FAkjIeRSJM85wEAAwIAA3kAAz0E"
IRANVIJ_PHOTO = "AgACAgQAAxkBAAEiVqhqnLnQqRs0KZ0MccGx__HEiErXggAChxRrGzUC6FBLCpwR2N9qiQEAAwIAA3kAAz0E"

WEAPONS = [
    {
        "id": "bow",
        "name": "کمان کهنه",
        "rank": "رایج",
        "element": "آب",
        "stats": "توان حمله: +5 | سرعت: +4",
        "desc": "کمانی چوبی و به یادگار مانده از روزگارانِ پیشین؛ زهِ آن کمی سست شده اما همچنان در رزمِ دوربرد یارای توست.",
        "file_id": "AgACAgQAAxkBAAEiVqBqnLbbsidzJdoP8MZ5I_H7c7HoLwACgRRrGzUC6FC8ekEeWM0ligEAAwIAA3kAAz0E"
    },
    {
        "id": "axe",
        "name": "تبرِ سنگینِ آهنگر",
        "rank": "رایج",
        "element": "آتش",
        "stats": "توان حمله: +7 | دفاع: +3",
        "desc": "تبری زنگارگرفته از کوره‌های خاموشِ باستانی که با ضرباتِ سنگینش، استخوانِ دشمن را خرد می‌کند.",
        "file_id": "AgACAgQAAxkBAAEiVqNqnLcJ-3SKzGo3TrIvmCllYLnUggACgxRrGzUC6FDuuq1jLUqgWAEAAwIAA3kAAz0E"
    },
    {
        "id": "sword",
        "name": "شمشیرِ مه‌آلود",
        "rank": "رایج",
        "element": "باد",
        "stats": "توان حمله: +6 | حداکثر انرژی: +5",
        "desc": "شمشیری قدیمی که تیغه‌ی آن در میانِ غبار و باد می‌رقصد؛ سبک‌بار است و توانِ تنفس در نبرد را فزونی بخشد.",
        "file_id": "BQACAgQAAxkBAAEiVpxqnLYeNqzS-OqXojOlyWTWKmzenAAC4SEAAjUC6FCnxLo5EQ4bDz0"
    },
    {
        "id": "mace",
        "name": "گرزِ خاکی",
        "rank": "رایج",
        "element": "خاک",
        "stats": "توان حمله: +6 | میزان جان: +10",
        "desc": "گرزی استوار از سنگِ تیره که ریشه‌اش به صخره‌های سخت پیوند خورده و پایداریِ تن را در برابرِ ضربات بالا می‌برد.",
        "file_id": "AgACAgQAAxkBAAEiVqJqnLcJwCmTkdwyXk6tPVCaCkWO8AACghRrGzUC6FB547ssmEg0OQEAAwIAA3kAAz0E"
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player_data[user_id] = {"step": "waiting_for_name"}
    
    mobad_text = (
        "*(مردی سالخورده با ردای قهوه‌رنگ و محاسن و موهای بلندِ سفید، چوب‌دست‌به‌دست به تو نزدیک می‌شود؛ در کنارش آتشدانی کوچک شعله می‌کشد...)*\n\n"
        "درود بر تو ای جوانمردِ پاک‌سرشت و جویای نام! گام نهادنت را به این خاکِ تاریک و بلازده، ارج می‌نهم. "
        "من «موبدِ پیر»، دیده‌بانِ این مرز و بوم، چشم به راهِ کسی چون تو بودم تا رازِ این تاریکیِ بی‌انتها را بازگو کنم.\n\n"
        "گوش فرادار به داستانی که ریشه‌اش در آغازین روزهای آفرینش و زمانِ بیکران نهفته است... "
        "روزگارانی دراز پیش از این، خدای زمان — **زروان** — هزار سال تمام نیایش و قربانی کرد تا فرزندی به نام **اهورامزدا** بیافریند...\n\n"
        "اکنون اهریمن این سرزمین را به کانون آشوب بدل ساخته است. هدفت گذر از رنج‌ها و به زانو درآوردنِ تاریکی است.\n\n"
        "اکنون، پیش از آنکه راهِ پرشکوهِ خود را آغاز کنی، مرا بگوی که نامِ بلندِ تو چیست و به چه نامی در طومارِ دلاوران شناخته خواهی شد؟"
    )
    
    await update.message.reply_photo(
        photo=MOBAD_PHOTO,
        caption=mobad_text,
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in player_data:
        await start(update, context)
        return

    state = player_data[user_id].get("step")

    if state == "waiting_for_name":
        name = update.message.text
        player_data[user_id]["name"] = name
        player_data[user_id]["step"] = "choosing_weapon"
        player_data[user_id]["weapon_index"] = 0

        await update.message.reply_text(
            f"پذیرفتیم ای {name}! نامت در طومارِ دلاوران ثبت شد.\n\nاکنون ورق بزن و سلاحِ خویش را انتخاب کن:",
            parse_mode="Markdown"
        )
        await send_weapon_page(update.effective_chat.id, user_id, context, edit=False)

async def send_weapon_page(chat_id, user_id, context, edit=False, message_id=None):
    idx = player_data[user_id]["weapon_index"]
    w = WEAPONS[idx]
    
    text = (
        f"📖 **طومارِ افزارها و سلاح‌های کهن** (برگه {idx + 1} از {len(WEAPONS)})\n\n"
        f"⚔️ **نام:** {w['name']}\n"
        f"🔹 **درجه:** {w['rank']}\n"
        f"🔥 **عنصر:** {w['element']}\n"
        f"📊 **ویژگی‌ها:** {w['stats']}\n\n"
        f"📜 *{w['desc']}*\n\n"
        "برای دیدنِ دیگر افزارها، برگه‌ها را ورق بزن یا همین سلاح را برگزین:"
    )

    keyboard = [
        [
            InlineKeyboardButton("◀ برگه پیشین", callback_data="prev_weapon"),
            InlineKeyboardButton("برگه بعدی ▶", callback_data="next_weapon")
        ],
        [
            InlineKeyboardButton(f"✨ گزینشِ این سلاح ({w['name']})", callback_data=f"select_{w['id']}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if edit and message_id:
        await context.bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=InputMediaPhoto(media=w['file_id'], caption=text, parse_mode="Markdown"),
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=w['file_id'],
            caption=text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in player_data:
        return

    data = query.data

    if data == "next_weapon":
        player_data[user_id]["weapon_index"] = (player_data[user_id]["weapon_index"] + 1) % len(WEAPONS)
        await send_weapon_page(query.message.chat_id, user_id, context, edit=True, message_id=query.message.message_id)
        
    elif data == "prev_weapon":
        player_data[user_id]["weapon_index"] = (player_data[user_id]["weapon_index"] - 1) % len(WEAPONS)
        await send_weapon_page(query.message.chat_id, user_id, context, edit=True, message_id=query.message.message_id)
        
    elif data.startswith("select_"):
        weapon_id = data.split("_")[1]
        selected_weapon = next(w for w in WEAPONS if w["id"] == weapon_id)
        player_data[user_id]["weapon"] = selected_weapon
        player_data[user_id]["step"] = "in_iranvij"

        player_name = player_data[user_id]["name"]

        spawn_text = (
            f"پهلوان {player_name}، **{selected_weapon['name']}** ({selected_weapon['rank']}) با عنصرِ **{selected_weapon['element']}** را با خود همراه ساخت.\n\n"
            "*(با در دست داشتن این افزار، گام در گذرگاهی مه‌آلود می‌گذاری... هوا خنک می‌شود و در پسِ غبار، دیوارهای بلند و سنگیِ شهری باستانی پدیدار می‌گردند.)*\n\n"
            "به **«ایران‌ویج»** — گهواره‌ی اساطیری و پناهگاهِ بازماندگانِ این مرز و بوم — خوش آمدی!\n\n"
            "این‌جا نقطه‌ی آغازِ نبردِ توست. کوچه‌های خلوت و آتشدان‌های خاموشِ شهر چشم به راهِ گام‌های استوارِ تویند تا دوباره نور و زندگی را بازگردانند."
        )

        # ارسال عکس ایران‌ویج به همراه متن ورود به شهر
        await query.message.delete()
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=IRANVIJ_PHOTO,
            caption=spawn_text,
            parse_mode="Markdown"
        )

def main():
    TOKEN = "8717208912:AAHGgwn_7rURyL9C-D9PrJSsUlwdcizmfdE"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("ربات میراث زمان با موفقیت روشن شد و آماده‌ی نبرد است...")
    app.run_polling()

if __name__ == "__main__":
    main()