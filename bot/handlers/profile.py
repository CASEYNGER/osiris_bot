import re

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from constants.templates import (
    NAME_REGEX, EMAIL_REGEX, PHONE_REGEX
)

from db.db_work import (
    get_user, update_name, update_surname, update_email,
    update_phone_number
)

from fsm.states import EditProfile

from kbs.inline_kbs import edit_profile_ikb, back_to_profile_ikb

from utils.check_funcs import contains_bad_words

profile_router = Router()


@profile_router.message(F.text == "Профиль")
async def get_profile(message: Message):
    """
    Обработчик текста "Профиль".

    Отправка данных профиля.

    :message: сообщение (class Message).
    """
    user_info = await get_user(message.from_user.id)

    await message.answer(
        f"<b>Профиль пользователя</b>\n\n"
        f"<b>ID:</b> {message.from_user.id}\n"
        f"<b>Имя:</b> {user_info[0]}\n"
        f"<b>Фамилия:</b> {user_info[1]}\n"
        f"<b>E-mail:</b> {user_info[2]}\n"
        f"<b>Номер телефона:</b> {user_info[3]}\n",
        reply_markup=edit_profile_ikb()
    )
    await message.answer()


@profile_router.callback_query(F.data == "go_to_profile")
async def get_profile_call(callback: CallbackQuery):
    """
    Обработчик callback_query "go_to_profile".

    Отправка данных профиля.

    :callback: вызов (class CallbackQuery).
    """
    user_info = await get_user(callback.from_user.id)

    await callback.message.edit_text(
        f"<b>Профиль пользователя</b>\n\n"
        f"<b>ID:</b> {callback.from_user.id}\n"
        f"<b>Имя:</b> {user_info[0]}\n"
        f"<b>Фамилия:</b> {user_info[1]}\n"
        f"<b>E-mail:</b> {user_info[2]}\n"
        f"<b>Номер телефона:</b> {user_info[3]}\n",
        reply_markup=edit_profile_ikb()
    )
    await callback.answer()


@profile_router.callback_query(F.data == "edit_profile_name")
async def edit_user_profile_name(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик callback_query "edit_profile_name".

    Вызывает FSM EditProfile и переводит в режим ожидания
    ввода от пользователя значения нового имени.

    :callback: вызов (class CallbackQuery);
    :state: хранит данные о текущем состоянии пользователя.
    """
    await callback.message.edit_text(
        "Введите ваше имя:"
    )
    await state.set_state(EditProfile.waiting_for_name)
    await callback.answer()


@profile_router.message(StateFilter(EditProfile.waiting_for_name))
async def process_name(message: Message, state: FSMContext):
    """
    Обработчик состояния "waiting_for_name".

    Проверка на валидность введенных данных и обновление
    name в БД.

    :message: сообщение (class Message);
    :state: хранит данные о текущем состоянии пользователя.

    """
    new_name = message.text

    if not re.match(NAME_REGEX, new_name):
        await message.answer(
            "Имя должно содержать только буквы и пробелы.\n\n"
            "Попробуйте еще раз."
        )
        return

    if not len(new_name) <= 15:
        await message.answer(
            "Имя не может быть длиннее 15 символов.\n\n"
            "Попробуйте еще раз."
        )
        return

    if contains_bad_words(new_name):
        await message.answer(
            "Имя не может содержать оскорбительное или "
            "унижающее человеческое достоинство слово.\n\n"
            "Попробуйте еще раз."
        )
        return

    user_id = message.from_user.id
    await update_name(user_id, new_name)
    await state.clear()
    await message.answer(
        f"✅ Ваше имя обновлено на: <b>{new_name}</b>",
        reply_markup=back_to_profile_ikb()
    )


@profile_router.callback_query(F.data == "edit_profile_surname")
async def edit_user_profile_surname(
    callback: CallbackQuery,
    state: FSMContext
):
    """
    Обработчик callback_query "edit_profile_surname".

    Вызывает FSM EditProfile и переводит в режим ожидания
    ввода от пользователя значения новой фамилии.

    :callback: вызов (class CallbackQuery);
    :state: хранит данные о текущем состоянии пользователя.
    """
    await callback.message.edit_text(
        "Введите вашу фамилию:"
    )
    await state.set_state(EditProfile.waiting_for_surname)
    await callback.answer()


@profile_router.message(StateFilter(EditProfile.waiting_for_surname))
async def process_surname(message: Message, state: FSMContext):
    """
    Обработчик состояния "waiting_for_surname".

    Проверка на валидность введенных данных и обновление
    surname в БД.

    :message: сообщение (class Message);
    :state: хранит данные о текущем состоянии пользователя.
    """
    new_surname = message.text

    if not re.match(NAME_REGEX, new_surname):
        await message.answer(
            "Фамилия должна содержать только буквы и пробелы.\n\n"
            "Попробуйте еще раз."
        )
        return

    if not len(new_surname) <= 20:
        await message.answer(
            "Фамилия не может быть длиннее 20 символов.\n\n"
            "Попробуйте еще раз."
        )
        return

    if contains_bad_words(new_surname):
        await message.answer(
            "Фамилия не может содержать оскорбительное или "
            "унижающее человеческое достоинство слово.\n\n"
            "Попробуйте еще раз."
        )
        return

    user_id = message.from_user.id
    await update_surname(user_id, new_surname)
    await state.clear()
    await message.answer(
        f"✅ Ваша фамилия обновлена на: <b>{new_surname}</b>",
        reply_markup=back_to_profile_ikb()
    )


@profile_router.callback_query(F.data == "edit_profile_email")
async def edit_user_profile_email(
    callback: CallbackQuery,
    state: FSMContext
):
    """
    Обработчик callback_query "edit_profile_email".

    Вызывает FSM EditProfile и переводит в режим ожидания
    ввода от пользователя значения нового адреса почты.

    :callback: вызов (class CallbackQuery);
    :state: хранит данные о текущем состоянии пользователя.
    """
    await callback.message.edit_text(
        "Введите вашу почту в следующем формате:\n\n"
        "<i>example@adress.com</i>"
    )
    await state.set_state(EditProfile.waiting_for_email)
    await callback.answer()


@profile_router.message(StateFilter(EditProfile.waiting_for_email))
async def process_email(message: Message, state: FSMContext):
    """
    Обработчик состояния "waiting_for_email".

    Проверка на валидность введенных данных и обновление
    email в БД.

    :message: сообщение (class Message);
    :state: хранит данные о текущем состоянии пользователя.
    """
    new_email = message.text
    if not re.match(EMAIL_REGEX, new_email):
        await message.answer(
            "Неверный формат электронной почты.\n\n"
            "Убедитесь, что введеный адрес электронной почты "
            "соответствует формату."
        )
        return

    if not len(new_email) <= 30:
        await message.answer(
            "Адрес электронной почты не может быть "
            " длиннее 30 символов.\n\n"
            "Попробуйте еще раз."
        )
        return

    if contains_bad_words(new_email):
        await message.answer(
            "Адрес электронной почты не может содержать оскорбительное или "
            "унижающее человеческое достоинство слово.\n\n"
            "Попробуйте еще раз."
        )
        return

    user_id = message.from_user.id
    await update_email(user_id, new_email)
    await state.clear()
    await message.answer(
        f"✅ Ваша почта обновлена на: <b>{new_email}</b>",
        reply_markup=back_to_profile_ikb()
    )


@profile_router.callback_query(F.data == "edit_profile_number")
async def edit_user_profile_number(
    callback: CallbackQuery,
    state: FSMContext
):
    """
    Обработчик callback_query "edit_profile_number".

    Вызывает FSM EditProfile и переводит в режим ожидания
    ввода от пользователя значения нового номера телефона.

    :callback: вызов (class CallbackQuery);
    :state: хранит данные о текущем состоянии пользователя.
    """
    await callback.message.edit_text(
        "Введите номер вашего мобильного телефона в следующем формате:\n\n"
        "<i>+79998887766</i>"
    )
    await state.set_state(EditProfile.waiting_for_phone_number)
    await callback.answer()


@profile_router.message(StateFilter(EditProfile.waiting_for_phone_number))
async def process_phone_number(message: Message, state: FSMContext):
    """
    Обработчик состояния "waiting_for_name".

    Проверка на валидность введенных данных и обновление
    email в БД.

    :message: сообщение (class Message);
    :state: хранит данные о текущем состоянии пользователя.
    """
    new_phone_number = message.text
    if not re.match(PHONE_REGEX, new_phone_number):
        await message.answer(
            "Неправильный формат номера телефона.\n\n"
            "Убедитесь, что введеный номер телефона "
            "соответствует формату."
        )
        return

    user_id = message.from_user.id
    await update_phone_number(user_id, new_phone_number)
    await state.clear()
    await message.answer(
        f"✅ Ваш мобильный номер обновлен на: <b>{new_phone_number}</b>",
        reply_markup=back_to_profile_ikb()
    )
