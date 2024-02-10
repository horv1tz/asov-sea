import os
from typing import Any

from sqlalchemy import select, text, or_, func
import shutil
from PIL import Image

from database import async_session_maker
from trouble.models import Trouble


# Базовая функция для сбора данных с БД
async def get_data(
    class_,
    filter,
    is_scalar: bool = False,
    order_by=None
):
    async with async_session_maker() as session:
        stmt = select(class_).where(filter)
        if is_scalar:
            res_query = await session.execute(stmt)
            res = res_query.scalar()
        else:
            if order_by:
                stmt = select(class_).where(filter).order_by(order_by)
            res_query = await session.execute(stmt)
            res = res_query.fetchall()
            res = [result[0] for result in res]
    return res


async def create_upload_avatar(
    object_id,
    file,
    class_,
    path: str,
):
    async with async_session_maker() as session:
        object = await session.get(class_, object_id)
        save_path = os.path.join(path, f"object{object.id}{file.filename}")

        with open(save_path, "wb") as new_file:
            shutil.copyfileobj(file.file, new_file)

        # Открываем изображение
        with Image.open(save_path) as img:
            # Изменяем размер изображения на 350x350
            img = img.resize((150, 150))
            # Создаем новый файл, преобразовывая изображение в формат WebP
            new_save_path = os.path.splitext(save_path)[0] + ".webp"
            img.save(new_save_path, "WEBP")

        # Удаляем старый файл
        os.remove(save_path)

        # Обновляем путь к файлу в объекте
        object.pathfile = new_save_path
        await session.commit()

    return new_save_path


def change_layout(text):
    conversion = {
        'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г',
        'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы',
        'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д',
        ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и',
        'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '`': 'ё',

        'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u',
        'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']', 'ф': 'a', 'ы': 's',
        'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l',
        'ж': ';', 'э': "'", 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b',
        'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.', 'ё': '`'
    }

    return ''.join([conversion.get(char, char) for char in text])


async def find_object(entity_class, entity_parameter, entity_mark: str, similarity: float = 0.3):
    async with async_session_maker() as session:
        await session.execute(text(f"SET pg_trgm.similarity_threshold = {similarity};"))
        entity_converted = change_layout(entity_mark)
        query = select(entity_class).where(
            or_(
                func.similarity(entity_parameter, entity_mark) > 0.3,
                func.similarity(entity_parameter, entity_converted) > 0.3
            )
        )
        result = (await session.execute(query)).unique().fetchall()

        # Исправленный код
        result = [getattr(entity[0], entity_parameter.key) for entity in result]

        return result if result else {"result": "not found"}


# async def fill_dict_user_info(user_dict: dict, user: User):
#     user_dict {
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "registered_at": user.registered_at,
#         "id": user.id,
#     }


async def get_object_images(
    class_: Any,
    object_ids: str,
):
    async with async_session_maker() as session:
        object_ids = object_ids.split(",")
        object_ids = list(map(lambda x: int(x), object_ids))
        images = {
            f"{(class_.__name__).lower()}{object_id}":
                (await session.get(class_, object_id))
                .pathfile for object_id in object_ids
        }
        return images


async def trouble_to_dict(
    trouble: Trouble
):
    return {
        "id": trouble.id,
        "name": trouble.name,
    }


async def trouble_on_map(
    trouble: Trouble
):
    return {
        "id": trouble.id,
        "latitude": trouble.latitude,
        "longtitude": trouble.longitude,
        "priority": trouble.priority
    }


async def detailed_info_trouble(trouble: Trouble):
    trouble_dict = trouble.__dict__
    info = {key: value for key, value in trouble_dict.items() if key not in ['reporter_id', 'id']}
    return info


async def main_info_trouble(trouble: Trouble):
    return {
        "name": trouble.name,
        "description": trouble.description,
        "category": trouble.category.name,
        "status": trouble.solved,
        "priority": trouble.priority
    }
