import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Состояния диалога для бронирования
SELECT_DAY, SELECT_TIME, ENTER_NAME, ENTER_PHONE = range(4)


def get_admin_chat_id() -> int:
    admin_chat = os.getenv("ADMIN_CHAT_ID")
    if admin_chat:
        try:
            return int(admin_chat)
        except ValueError:
            pass
    admin_ids = os.getenv("ADMIN_IDS", "")
    if admin_ids:
        first = admin_ids.split(",")[0].strip()
        try:
            return int(first)
        except ValueError:
            pass
    return 0


ADMIN_CHAT_ID = get_admin_chat_id()

# Тексты шагов воронки
TEXT_STEPS = [
    (
        "♣️ То, что я тебе сейчас предложу - закроет все твои финансовые дыры, "
        "и заставит почувствовать себя не просто человеком, а человеком с деньгами, "
        "с конкретной целью, человеком с возможностями."
    ),
    (
        "♥️ ЕСЛИ ТЫ ТУТ, то ты прошел уже многое в жизни, и понял, что нет ничего благородного в бедности.\n\n"
        "Лично я уже была бедной! Хватит! Я выбрала богатство! Ведь когда у богатого человека проблемы, "
        "он решает их в своей крутой машине, в дорогой одежде, с дорогими часами на руках.\n\n"
        "Я тебе предлагаю не просто проект, я предлагаю тебе РЕШЕНИЕ, которое даст финансовую свободу, "
        "чувство уверенности, даст богатство и наконец-то исполнит твою самую смелую мечту."
    ),
    (
        "Ответь себе честно на следующие вопросы:\n\n"
        "👉 У тебя есть висяки по кредитам?\n\n"
        "👉 Тебя выгоняют со съёмной квартиры или поднимают плату?\n\n"
        "👉 Хочешь насобирать на квартиру, но собираешь уже лет 10?\n\n"
        "👉 Твои дети растут, но за какие деньги их учить?\n\n"
        "👉 Хочешь отдыхать в самых лучших местах этой планеты, но даже боишься мечтать об этом?\n\n"
        "👉 Хочешь машину с салона, но пока что можешь позволить себе только перекупных перекупов?\n\n"
        "Если у тебя хотя бы одно «Да», это круто 🙌 Ты попал в нужное место. Жми «Продолжить»."
    ),
    (
        "♦️ Предлагаю твоему вниманию CIB INCEPTION — проект, который дарит финансовые крылья. 🪽\n\n"
        "Быстрее узнавай, как он работает 👇"
    ),
    (
        "♠️ Инвестиционный проект Crypto Invest Bank INCEPTION — надёжный инновационный финансовый сервис, "
        "который делает инвестиции доступными и выгодными.\n\n"
        "Вы размещаете свой капитал и получаете стабильный доход просто и без скрытых комиссий."
    ),
    (
        "♣️ Сегодня криптовалюта приносит прибыль уже всем, но только не тебе.\n\n"
        "Нужно не упустить свою возможность тоже зарабатывать на криптовалюте и получить свой «кусок пирога»."
    ),
    (
        "♥️ Размещая свой капитал у нас, ты получаешь самые выгодные и надёжные условия инвестирования, "
        "так как твой капитал управляется профессиональными трейдерами, у которых больше 10 лет опыта "
        "торговли на рынке криптовалюты."
    ),
    (
        "Теперь задай главный вопрос: «Сколько я заработаю?» 🤑🫰"
    ),
    (
        "С 500$ за год 1500$\n"
        "С 1000$ за год 3000$\n"
        "С 5000$ за год 15000$\n"
        "С 10000$ за год 31000$"
    ),
    (
        "Ты ещё тут? Или понял, что богатство не для тебя?"
    ),
    (
        "Если тебе эта информация не откликается, тебе не сюда! Дальше не переходи, не отнимай время!\n\n"
        "Возвращайся на свою работу и забудь всё, что тут услышал!\n\n"
        "Но, прежде чем ты покинешь клуб победителей, подумай про соседа, который, возможно, "
        "именно в эту же секунду нажимает кнопку «Продолжить», и в каком-то недалёком будущем, "
        "когда ты тормознёшь на красный на своей старой машине или вообще будешь стоять на пешеходном, "
        "а твой сосед остановится рядом с тобой на шикарной новой машине с салона, то НЕ ЗАВИДУЙ ЧЁРНОЙ ЗАВИСТЬЮ, "
        "просто СЕГОДНЯ он решился, а ты дал заднюю."
    ),
    (
        "ВСЁ ЗАВИСИТ ОТ КАЖДОГО ИЗ НАС. Ты не должен терпеть отказ от Вселенной!\n\n"
        "Вселенная говорит тебе «Да» на все твои желания — самые смелые, самые неисполнимые, самые сокровенные!\n\n"
        "Поверь, сегодня Вселенная выбрала тебя, и именно СЕГОДНЯ она говорит тебе: «Даааа»."
    ),
    (
        "Решай свои проблемы, пока твои финансы растут.\n\n"
        "А для этого тебе нужно только одно: забронируй онлайн-созвон с ТОПовым Агентом, который поможет сделать "
        "твой первый вклад и сделает тебя Инвестором."
    ),
]


def continue_keyboard(next_index: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Продолжить", callback_data=f"next_{next_index}")]]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = TEXT_STEPS[0]
    keyboard = continue_keyboard(1)
    await update.message.reply_text(text, reply_markup=keyboard)


async def handle_next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    try:
        _, idx_str = data.split("_", 1)
        idx = int(idx_str)
    except Exception:
        return

    if idx < 0 or idx >= len(TEXT_STEPS):
        return

    text = TEXT_STEPS[idx]

    if idx < len(TEXT_STEPS) - 1:
        keyboard = continue_keyboard(idx + 1)
        await query.message.reply_text(text, reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Забронировать", callback_data="book_start")]]
        )
        await query.message.reply_text(text, reply_markup=keyboard)


async def book_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Пн", callback_data="day_Пн"),
            InlineKeyboardButton("Вт", callback_data="day_Вт"),
            InlineKeyboardButton("Ср", callback_data="day_Ср"),
        ],
        [
            InlineKeyboardButton("Чт", callback_data="day_Чт"),
            InlineKeyboardButton("Пт", callback_data="day_Пт"),
        ],
        [
            InlineKeyboardButton("Сб", callback_data="day_Сб"),
            InlineKeyboardButton("Вс", callback_data="day_Вс"),
        ],
    ])
    await query.message.reply_text(
        "Выберите удобный день недели для созвона:",
        reply_markup=keyboard,
    )
    return SELECT_DAY


async def select_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, day = query.data.split("_", 1)
    context.user_data["day"] = day

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("10:00", callback_data="time_10:00"),
            InlineKeyboardButton("12:00", callback_data="time_12:00"),
        ],
        [
            InlineKeyboardButton("15:00", callback_data="time_15:00"),
            InlineKeyboardButton("18:00", callback_data="time_18:00"),
        ],
    ])
    await query.message.reply_text(
        f"Отлично, день: {day}\n\nТеперь выберите удобное время:",
        reply_markup=keyboard,
    )
    return SELECT_TIME


async def select_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, time = query.data.split("_", 1)
    context.user_data["time"] = time

    await query.message.reply_text(
        "Напишите, пожалуйста, ваше имя:"
    )
    return ENTER_NAME


async def enter_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    context.user_data["name"] = name

    await update.message.reply_text(
        "Теперь укажите, пожалуйста, ваш номер телефона:"
    )
    return ENTER_PHONE


async def enter_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    context.user_data["phone"] = phone

    user = update.effective_user
    day = context.user_data.get("day")
    time = context.user_data.get("time")
    name = context.user_data.get("name")

    await update.message.reply_text(
        "Спасибо! Ваша заявка на созвон с ТОПовым Агентом принята. "
        "Мы свяжемся с вами в ближайшее время. 💛"
    )

    if ADMIN_CHAT_ID:
        text = (
            "📩 Новая заявка на созвон CIB INCEPTION\n\n"
            f"👤 Имя: {name}\n"
            f"📞 Телефон: {phone}\n"
            f"📅 День: {day}\n"
            f"⏰ Время: {time}\n\n"
            f"Telegram: @{user.username if user and user.username else 'без username'}\n"
            f"ID: {user.id if user else 'неизвестно'}"
        )
        try:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
        except Exception:
            pass

    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бронирование отменено.")
    context.user_data.clear()
    return ConversationHandler.END


def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Не задан BOT_TOKEN в переменных окружения.")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_next, pattern=r"^next_\d+$"))

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(book_start, pattern=r"^book_start$")],
        states={
            SELECT_DAY: [CallbackQueryHandler(select_day, pattern=r"^day_.+")],
            SELECT_TIME: [CallbackQueryHandler(select_time, pattern=r"^time_.+")],
            ENTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_name)],
            ENTER_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)

    print("✅ Бот запущен. Открой своего бота и набери /start.")
    app.run_polling()


if __name__ == "__main__":
    main()
