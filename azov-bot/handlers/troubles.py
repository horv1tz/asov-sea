import json
import os

import aiohttp
from aiogram import Router, types, F
from aiogram.filters import StateFilter, Command, or_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import requests as rq
from dotenv import load_dotenv, find_dotenv

user_private_router = Router()

load_dotenv(find_dotenv())

categories_response = rq.get("http://localhost:8000/troubles/get_all_categories")
categories_data = json.loads(categories_response.text)

headers = {
    "Authorization": f"Bearer {os.getenv('BEARER_TOKEN')}"
}


async def upload_photo_to_fastapi(file_id: str, trouble_id: int):
    async with aiohttp.ClientSession() as session:
        # Получаем информацию о файле от Telegram
        telegram_file_path_url = f"https://api.telegram.org/bot{os.getenv('TOKEN')}/getFile?file_id={file_id}"
        async with session.get(telegram_file_path_url) as response:
            file_path_data = await response.json()
            file_path = file_path_data['result']['file_path']

        # Скачиваем файл
        file_url = f"https://api.telegram.org/file/bot{os.getenv('TOKEN')}/{file_path}"
        async with session.get(file_url) as response:
            if response.status == 200:
                file_content = await response.read()
                # Здесь file_content - это бинарное содержимое файла

                # Создаем FormData и отправляем файл на FastAPI сервер
                data = aiohttp.FormData()
                data.add_field('file',
                               file_content,
                               filename='trouble_photo.jpg',
                               content_type='image/jpeg')

                upload_url = f"http://127.0.0.1:8000/troubles/uploadfile/avatar/{trouble_id}"
                async with session.post(upload_url, headers=headers, data=data) as upload_response:
                    if upload_response.status == 200:
                        # Фотография успешно загружена на ваш сервер
                        return True
                    else:
                        # Обработка ошибок при загрузке
                        return False
            else:
                # Обработка ошибок при скачивании файла
                return False


class AddTrouble(StatesGroup):
    category_id = State()
    name = State()
    description = State()
    location = State()
    photo = State()

# Вспомогательная функция для создания сообщения со списком категорий
def create_categories_message(categories):
    message_text = "Выберите категорию проблемы:\n"
    for key, value in categories.items():
        message_text += f"{value['id']}) {value['name']}\n"
    return message_text

@user_private_router.message(or_f(Command("send"), (F.text.lower() == "Сообщить о проблеме") | (F.text.lower().contains("проблем") )))
async def start_trouble_reporting(message: types.Message, state: FSMContext):
    await message.answer(create_categories_message(categories_data))
    await state.set_state(AddTrouble.category_id)


@user_private_router.message(StateFilter('*'), Command("отмена"))
@user_private_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены")

#Вернутся на шаг назад (на прошлое состояние)
@user_private_router.message(StateFilter('*'), Command("назад"))
@user_private_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddTrouble.name:
        await message.answer('Предыдущего шага нет, или введите название товара или напишите "отмена"')
        return

    previous = None
    for step in AddTrouble.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AddTrouble.texts[previous.state]}")
            return
        previous = step


@user_private_router.message(AddTrouble.category_id, F.text)
async def process_category_id(message: types.Message, state: FSMContext):
    # Здесь можно добавить проверку на валидность введенной категории
    await state.update_data(category_id=message.text)
    await message.answer("Введите название:")
    await state.set_state(AddTrouble.name)

@user_private_router.message(AddTrouble.name, F.text)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание проблемы:")
    await state.set_state(AddTrouble.description)

@user_private_router.message(AddTrouble.description, F.text)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Отправьте местоположение:")
    await state.set_state(AddTrouble.location)

@user_private_router.message(AddTrouble.location, F.location)
async def process_location(message: types.Message, state: FSMContext):
    location_data = f"{message.location.latitude}, {message.location.longitude}"
    await state.update_data(location=location_data)
    await message.answer("Теперь отправьте фотографию проблемы:")
    await state.set_state(AddTrouble.photo)

@user_private_router.message(AddTrouble.location)
async def process_location_error(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте местоположение используя функцию отправки локации в Telegram.")


@user_private_router.message(AddTrouble.photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)

    data = await state.get_data()

    trouble_data = {
        "name": data['name'],
        "description": data['description'],
        "priority": "Низкий",
        "latitude": float(data['location'].split(', ')[0]),
        "longitude": float(data['location'].split(', ')[1]),
        "category_id": int(data['category_id']),
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8000/troubles/add_new", json=trouble_data,
                                headers=headers) as response:
            if response.status == 200:
                await message.answer("Ваша проблема зарегистрирована, спасибо за обращение.")
                response_json = await response.json()
                trouble_id = response_json.get("trouble_id")
                await upload_photo_to_fastapi(message.photo[-1].file_id, trouble_id=trouble_id)
            else:
                await message.answer("Произошла ошибка при регистрации проблемы.")

    await state.clear()

@user_private_router.message(AddTrouble.photo)
async def process_photo_error(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте фотографию проблемы.")