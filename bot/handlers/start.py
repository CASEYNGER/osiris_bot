"""Хэндлеры (обработчики)."""
from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from constants.templates import ADMIN, NOT_ADMIN

from utils.check_funcs import contains_bad_words

from db.db_work import (
    register_user, is_registered, make_admin, is_admin,
    get_users
)

from kbs.all_kbs import main_kb
from kbs.inline_kbs import (
    main_ikb, about_ikb, pages_ikb, soft_skills,
    hard_skills, portfolio_ikb
    )

from about_me import info

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обработчик команды /start.

    Автоматически добавляет пользователя в БД
    и отправляет приветственное сообщение в зависимости
    от статуса пользователя.

    :message: сообщение (class Message).
    """
    user_id = message.from_user.id
    username = message.from_user.username or "None"
    full_name = message.from_user.full_name

    if await is_registered(user_id):
        await message.answer(
            f"Рад тебя видеть снова, <b>{full_name}</b>! 👋\n\n"
            "Я <b>Осирис</b>, твой виртуальный ассистент в мире "
            "технологий.\n\n"
            "Готов помочь тебе узнать больше о моем создателе. Я собрал "
            "самую актуальную информацию и готов с тобой поделиться.\n\n"
            "Просто <i>выбери пункт</i> из меню, чтобы начать работу!",
            reply_markup=main_kb(
                user_telegram_id=message.from_user.id
            )
        )
    else:
        await register_user(user_id, username, full_name)
        await message.answer(
            f"Добро пожаловать, {username}! 👋\n\n"
            "Меня зовут Осирис, и ты только что стал частью моего"
            "маленького технологичного мира. Я создан для того, чтобы "
            "помочь тебе узнать больше о моем создателе и всех проектах "
            "которыми мы занимаемся.\n\n"
            "Все, что тебе нужно - это <i>выбрать пункт</i> в меню, и я "
            "проведу тебя по всем возможностям!",
            reply_markup=main_kb(
                user_telegram_id=message.from_user.id
            )
        )


@start_router.message(Command("status"))
async def get_status(message: Message):
    """
    Обработчик команды /status.

    Отправка приватной информации (только для
    авторизированных пользователей)

    :message: сообщение (class Message).
    """
    user_id = message.from_user.id
    username = message.from_user.username

    if not await is_registered(user_id):
        await message.answer(
            f"⛔ {username}, вы не авторизованы.\n\n"
            "Используйте /start для регистрации."
        )
        return

    await message.answer(
        f"<b>Статус пользователя:</b> {message.from_user.full_name}\n\n"
        f"<b>ID:</b> {message.from_user.id}\n"
        f"<b>Никнейм:</b> {username}\n"
        f"<b>Имя:</b> {message.from_user.first_name}\n"
        f"<b>Фамилия:</b> {message.from_user.last_name}\n"
    )


@start_router.message(Command("get_users"))
async def send_users_list(message: Message):
    """
    Обработчик команды /get_users.

    Отправляет список пользователей (только для админов).

    :message: сообщение (class Message).
    """
    users = await get_users()
    if not await is_admin(message.from_user.id):
        await message.answer(NOT_ADMIN)
        return
    if not users:
        await message.answer("База данных пуста.")
        return
    text = "\n".join(
        [f"- {user[0]}, @{user[1]}, {user[2]};" for user in users]
    )
    await message.answer(f"<b>Список пользователей:</b>\n\n{text}")


@start_router.message(Command("make_admin"))
async def make_admin_command(message: Message):
    """
    Обработчик команды /make_admin.

    Делает пользователя администратором (только для админов).

    :message: сообщение (class Message).
    """
    if not await is_admin(message.from_user.id):
        await message.answer(NOT_ADMIN)
        return

    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("⚠ Использование: /make_admin <user_id>")
        return

    user_id = int(args[1])
    await make_admin(user_id)
    await message.answer(f"✅ Пользователь {user_id} теперь администратор!")


@start_router.message(Command("admin_panel"))
async def admin_panel(message: Message):
    """
    Обработчик команды /admin_panel.

    Панель администратора (доступ только у админов).

    :message: сообщение (class Message).
    """
    if not await is_admin(message.from_user.id):
        await message.answer(NOT_ADMIN)
        return

    await message.answer(
        "🔧 <b>Добро пожаловать в панель администратора!</b>\n\n"
        "<b>Доступные команды:</b>\n\n"
        "/status - узнать статус пользователя;\n"
        "/get_users - получить список пользователей;\n"
    )


@start_router.message(F.text == "⚙️ Настройки")
async def get_settings(message: Message):
    """
    Обработчик текста "⚙️ Настройки".

    Вызывает меню настроек.

    :message: сообщение (class Message).
    """
    await message.answer(
        "<b>Настройки</b>\n\n"
        "Это раздел с общими настройками виртуального помощника, "
        "где вы можете <i>(в разработке...)</i> ...\n\n"
        "Посмотреть информацию о себе возможно командой /status"
    )


@start_router.message(F.text == "О разработчике")
async def post_info(message: Message):
    """
    Обработчик текста "О разработчике".

    Вызывает информацию о разработчике и inline_menu.

    :message: сообщение (class Message).
    """
    await message.answer(
        "<b>О разработчике</b>\n\n"
        f"<b>ФИО:</b> {info[0]}\n"
        f"<b>Дата рождения:</b> {info[1]}\n"
        f"<b>Место рождения:</b> {info[2]}\n"
        f"<b>Уровень образования:</b> {info[3]}\n"
        "\nJunior backend-разработчик с энтузиазмом к созданию "
        "качественного кода и обучению новым технологиям. "
        "Имею опыт в разработке на языке Python"
        " и знаком с популярными фреймворками,"
        " такими как Aiogram для создания"
        " ботов и Django для веб-разработки. "
        "Стремлюсь к постоянному совершенствованию"
        " своих навыков и решению реальных задач с использованием современных"
        " инструментов разработки.\n\n"
        "Мой путь в программировании только начинается, но я уже успел"
        " поработать с различными проектами, которые помогли мне освоить"
        " основы разработки и повысить уровень знаний. Я открыт к новым"
        " вызовам и всегда готов учиться, чтобы развиваться как специалист"
        " в области технологий.",
        reply_markup=about_ikb()
    )


@start_router.callback_query(F.data == "start")
async def go_home_handler(callback: CallbackQuery):
    """
    Обработчик сallback_query "start".

    Вызывает основное inline-меню.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        "<b>Главное меню</b>",
        reply_markup=main_ikb()
    )
    await callback.answer()


# Хэндлер на callback "Ссылки"
@start_router.callback_query(F.data == "pages")
async def send_pages(callback: CallbackQuery):
    """
    Обработчик сallback_query "pages".

    Вызывает inline-меню с ссылками на
    социальные сети.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        "<b>Ссылки на социальные сети</b>",
        reply_markup=pages_ikb()
    )
    await callback.answer()


@start_router.callback_query(F.data == "soft_skills")
async def get_soft_skills(callback: CallbackQuery):
    """
    Обработчик сallback_query "soft_skills".

    Вызывает страницу с информацией о софт-скиллах.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        "<b>Софт-скиллы</b>\n\n"
        "<b>Командная работа и коммуникабельность</b>\n"
        "Легко нахожу общий язык с коллегами и людьми, "
        "умею работать в команде.\n\n"
        "<b>Ответственность</b>\n"
        "Знаю ценность своей работы и цену ее результатов.\n\n"
        "<b>Внимательность</b>\n"
        "Стремлюсь к качеству и точности продукта, изучаю требования"
        " и спецификации.\n\n"
        "<b>Адаптивность</b>\n"
        "Быстро осваиваю новые инструменты и технологии.\n\n"
        "<b>Навыки критического мышления</b>\n"
        "Умею анализировать проблемы, находить оптимальные решения "
        "и обосновывать их.\n\n"
        "<b>Эмоциональный интеллект</b>\n"
        "Способен понимать эмоции людей, реагировать на них с уважением "
        "и учитывать их, как в жизни, так и в работе.\n\n"
        "<b>Гибкость</b>\n"
        "Легко приспосабливаюсь к изменениям, не боюсь пробовать новое.\n\n"
        "<b>Решение конфликтов</b>\n"
        "Нахожу пути для урегулирования разногласий, добиваюсь "
        "конструктивного взаимодействия.",
        reply_markup=soft_skills()
    )
    await callback.answer()


@start_router.callback_query(F.data == "hard_skills")
async def get_hard_skills(callback: CallbackQuery):
    """
    Обработчик сallback_query "hard_skills".

    Вызывает страницу с информацией о хард-скиллах.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        "<b>Хард-скиллы</b>\n\n"
        "<b>Языки программирования:</b>\n"
        "- Python\n\n"
        "<b>Языки разметки и форматирования:</b>\n"
        "- HTML\n- CSS\n\n"
        "<b>Фреймворки:</b>\n"
        "- Django\n- Aiogram\n- Requests\n\n"
        "<b>Базы данных:</b>\n"
        "- SQL (PostgreSQL)\n- ORM (SQLAlchemy, SQLite)\n\n"
        "<b>API и веб-сервисы:</b>\n"
        "- <i>В процессе изучения...</i>\n\n"
        "<b>Тестирование:</b>\n"
        "- PyTest, Unittest\n\n"
        "<b>Системы контроля версий:</b>\n"
        "- Git (GitHub)\n\n"
        "<b>Контейнеризация и DevOps:</b>\n"
        "- Docker (<i>В процессе изучения...</i>)\n"
        "- CI/CD (<i>В процессе изучения...</i>)\n\n"
        "<b>Безопасность:</b>\n"
        "- Основы безопасности приложений, шифрование данных "
        "и защита от SQL-инъекций, XSS, CSRF.",
        reply_markup=hard_skills()
    )
    await callback.answer()


@start_router.callback_query(F.data == "about")
async def get_about_info(callback: CallbackQuery):
    """
    Обработчик сallback_query "about".

    Вызывает страницу с информацией о разработчике.

    :callback: вызов (class CallbackQuery).
    """
    about_text = (
        "<b>О разработчике</b>\n\n"
        f"<b>ФИО:</b> {info[0]}\n"
        f"<b>Дата рождения:</b> {info[1]}\n"
        f"<b>Место рождения:</b> {info[2]}\n"
        f"<b>Уровень образования:</b> {info[3]}\n\n"
        "Junior backend-разработчик с энтузиазмом к созданию"
        "качественного кода и обучению новым технологиям. "
        "Имею опыт в разработке на языке Python"
        " и знаком с популярными фреймворками,"
        " такими как Aiogram для создания"
        " ботов и Django для веб-разработки. "
        "Стремлюсь к постоянному совершенствованию"
        " своих навыков и решению реальных задач с использованием современных"
        " инструментов разработки.\n\n"
        "Мой путь в программировании только начинается, но я уже успел"
        " поработать с различными проектами, которые помогли мне освоить"
        " основы разработки и повысить уровень знаний. Я открыт к новым"
        " вызовам и всегда готов учиться, чтобы развиваться как специалист"
        " в области технологий."
    )
    await callback.message.edit_text(
        about_text,
        reply_markup=about_ikb()
    )
    await callback.answer()


@start_router.callback_query(F.data == "portfolio")
async def post_portfolio(callback: CallbackQuery):
    """
    Обработчик сallback_query "portfolio".

    Вызывает страницу с портфолио.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        "<b>Портфолио</b>\n\n"
        "<i>(В разработке...)</i>",
        reply_markup=portfolio_ikb()
    )


@start_router.callback_query(F.data == "contact")
async def contact_button(callback: CallbackQuery):
    """
    Обработчик сallback_query "contact".

    Вызывает сообщение для редиректа.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        "<b>Связь с разработчиком</b>\n\n"
        "Для <b>возможности</b> дальнейшей коммуникации "
        "используйте корректный формат обращения:\n\n"
        "<b>Пример:</b> #связь <i>Привет, я юзер!...</i>\n\n"
        "Напишите ваше сообщение и я передам его!"
    )
    await callback.answer()


@start_router.message(F.text.startswith("#связь "))
async def send_user_message_to_admin(message: Message, bot: Bot):
    """Редирект сообщений пользователей администратору."""
    user_id = message.from_user.id

    if not await is_registered(user_id):
        await message.answer(
            "⛔ Вам нужно зарегистрироваться, чтобы написать админу."
        )

    text = message.text.replace("#связь ", "").strip()

    if not text:
        await message.answer(
            "Пожалуйста, соблюдайте <b>формат</b> обращения!\n\n"
            "<b>Пример:</b> #связь <i>Привет, я юзер!...</i>\n\n"
        )
        return

    if contains_bad_words(text):
        await message.answer(
            "❌ <b>Сообщение не отправлено.</b>\n\n"
            "Ваше сообщение содержит запрещенные слова и может "
            "быть оскорбительным и унижающим достоинство других "
            "людей."
            )
        return

    admin_id = ADMIN
    await bot.send_message(
        admin_id,
        f"📩 <b>Сообщение от @{message.from_user.username}:</b>\n\n{text}"
    )
    await message.answer(
        "✅ <b>Сообщение успешно отправлено.</b>\n\n"
        "В ближайшее время мой создатель обязательно его прочитает."
        )
