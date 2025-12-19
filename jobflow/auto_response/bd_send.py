import psycopg2
from fastapi import HTTPException
import asyncio
from openai import OpenAI
import asyncpg
import requests
from JobFlow.config import *



async def load_vacancies_for_send(vacancy_categories, locations, experiences):
    """
    Загружает вакансии по нескольким категориям, локациям и уровням опыта
    Args:
        vacancy_categories: список или строка категорий (разделенных запятыми)
        locations: список или строка локаций (разделенных запятыми)
        experiences: список или строка уровней опыта (разделенных запятыми)
    Returns:
        Список словарей с вакансиями
    """
    def prepare_input(param):
        """Преобразует входной параметр в список"""
        if isinstance(param, str):
            return [item.strip() for item in param.split('\n')]
        elif isinstance(param, (list, tuple)):
            return list(param)
        return [str(param)]
    

    categories = vacancy_categories.split('\n')
    locations_list = prepare_input(locations)
    exp_levels = prepare_input(experiences)
    
    conn = None
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        # Формируем условия для SQL запроса
        category_conditions = " OR ".join([f"new_category LIKE '%{cat}%'" for cat in categories])
        location_conditions = " OR ".join([f"location LIKE '%{loc}%'" for loc in locations_list])
        experience_conditions = " OR ".join([f"experience LIKE '%{exp}%'" for exp in exp_levels])
        
        query = f"""
        SELECT link 
        FROM vacans 
        WHERE ({category_conditions})
          AND ({location_conditions})
          AND ({experience_conditions})
          AND date >= CURRENT_DATE - INTERVAL '4 day'
          AND source LIKE 'hh'
        """

        print(query)
        
        records = await conn.fetch(query)
        return [dict(record) for record in records]
        
    except Exception as e:
        print(f"Ошибка при загрузке вакансий: {e}")
        return []
    finally:
        if conn:
            await conn.close()


async def get_access_token_from_bd(user_id):
    """
    Загружает вакансии и пользовательские выборки из БД,
    возвращает кортеж (vacancies_cache, user_selections)
    """
    conn = None
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        records = await conn.fetch(
            f"SELECT access_token FROM users WHERE user_id like '{user_id}'"
        )
        
        return records
        
    except Exception as e:
       
        return {}
    finally:
        if conn:
            await conn.close()








async def send_vacanc(access_token, resume_id, vacancy_id):

    url = "https://api.hh.ru/negotiations"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mr.JobHunter/1.0 (maksim.arkhipov.020@mail.ru)"
    }

    # Теперь используем multipart/form-data вместо JSON
    files = {
        'vacancy_id': (None, str(vacancy_id)),
        'resume_id': (None, str(resume_id)),
        'message': (None, 'Добрый день, заинтересовала вакансия. Предлагаю обсудить детали!')
    }

    response = requests.post(url, headers=headers, files=files)
    return response



async def update_users(access_token, refresh_token, expires_in, state) -> tuple:
    """
    Обновляет access_token, refresh_token, expires_in, state
    возвращает кортеж (vacancies_cache, user_selections)
    """
    conn = None
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        # 1. Обновляем токены пользователя
        await conn.execute(
            "UPDATE users SET access_token = $1, refresh_token = $2, expires_in = $3 WHERE user_id = $4",
            str(access_token), str(refresh_token), str(expires_in), str(state)
        )
        
       
       
        return {'message': "ok"}
        
    except Exception as e:
        print(f"Error in update_users: {e}")
        return {'message': f"{e}"}
    finally:
        if conn:
            await conn.close()



async def update_users_resume(resume_id, count, access_token, new_category_auto, location_auto, experience_auto) -> tuple:
    conn = None
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        # 1. Получаем текущее значение count из базы данных
        current_count = await conn.fetchval(
            "SELECT count FROM users WHERE access_token = $1",
            str(access_token)
        )
        
        # Если записи нет, current_count будет None, тогда устанавливаем 0
        if current_count is None:
            current_count = 0
        
        # 2. Вычисляем новое значение
        new_count = current_count + int(count)
        
        # 3. Обновляем запись в базе данных
        await conn.execute(
            "UPDATE users SET resume_id = $1, count = $2,new_category_auto = $3, location_auto = $4, experience_auto = $5, is_active_auto = True  WHERE access_token = $6",
            str(resume_id), new_count, str(new_category_auto.split("\n")), str(location_auto.split("\n")), str(experience_auto.split("\n")), str(access_token)
        )
        return {'message': "ok"}

    except Exception as e:
        print(f"Error in update_users: {e}")
        return {'message': f"{e}"}
    finally:
        if conn:
            await conn.close()


async def update_users_premium(user_id, payment_id) -> tuple:
    conn = None
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        await conn.execute(
            "UPDATE users SET payment_id = $1 WHERE user_id = $2",
            str(payment_id), str(user_id)
        )
        return {'message': "ok"}

    except Exception as e:
        print(f"Error in update_users: {e}")
        return {'message': f"{e}"}
    finally:
        if conn:
            await conn.close()

async def get_user_premium(user_id) -> tuple:
    conn = None
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        payment_id = await conn.fetchval(
            "SELECT payment_id FROM users WHERE user_id = $1",
            str(user_id)
        )
        return {'message': payment_id}

    except Exception as e:
        print(f"Error in update_users: {e}")
        return {'message': f"{e}"}
    finally:
        if conn:
            await conn.close()


async def update_flag_premium(user_id, premium_date) -> tuple:
    conn = None
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        # is_premium
        await conn.execute(
            "UPDATE users SET is_premium = True, premium_date =$1  WHERE user_id = $2",
            premium_date, str(user_id)
        )
        return {'message': "ok"}
    

    except Exception as e:
        print(f"Error in update_users: {e}")
        return {'message': f"{e}"}
    finally:
        if conn:
            await conn.close()



async def get_flag_premium(user_id):
    """
    Загружает вакансии и пользовательские выборки из БД,
    возвращает кортеж (vacancies_cache, user_selections)
    """
    conn = None
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        records = await conn.fetch(
            f"SELECT is_premium, premium_date FROM users WHERE user_id like '{user_id}'"
        )
        
        return records
        
    except Exception as e:
       
        return {}
    finally:
        if conn:
            await conn.close()



async def disable_auto_for_user(user_id):
    """
    Отключаем автоотклики
    """
    conn = None
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        await conn.execute(
            "UPDATE users SET is_active_auto = False WHERE user_id = $1",
            str(user_id)
        )
        return {'message': "ok"}
        
        return records
        
    except Exception as e:
       
        return {}
    finally:
        if conn:
            await conn.close()


async def get_payment_token(user_id):
    """
    Загружает вакансии и пользовательские выборки из БД,
    возвращает кортеж (vacancies_cache, user_selections)
    """
    conn = None
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        records = await conn.fetch(
            f"SELECT payment_id FROM users WHERE user_id like '{user_id}'"
        )
        
        return records
        
    except Exception as e:
       
        return {}
    finally:
        if conn:
            await conn.close()