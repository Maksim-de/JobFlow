from openai import OpenAI
from PyPDF2 import PdfReader
import io
import asyncpg
from typing import List
import asyncio
from datetime import datetime
from JobFlow.config import *

import requests

count_requests_in_day = 0

def get_client():
    """Возвращает клиента OpenAI с нужным токеном в зависимости от количества запросов"""
    global count_requests_in_day
    if count_requests_in_day < 45:
        api_key = TOKEN_DEPS_FOUR
    elif count_requests_in_day < 90:
        api_key = TOKEN_DEPS_THREE
    elif count_requests_in_day < 135:
        api_key = TOKEN_DEPS_TWO
    elif count_requests_in_day < 180:
        api_key = TOKEN_DEPS_ONE
    else:
        # Сбрасываем счетчик, если достигли лимита всех токенов
        count_requests_in_day = 0
        api_key = TOKEN_DEPS_THREE
    
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

client = get_client()



def extract_text_from_pdf(file: bytes) -> str:
    """Принимает PDF как bytes, возвращает извлеченный текст."""
    reader = PdfReader(io.BytesIO(file))
    text = " ".join([page.extract_text() for page in reader.pages])
    return text



async def generating_answer_without_vacancy(pdf_file, temp = 0.8):
    global count_requests_in_day

    client = get_client()

    count_requests_in_day+=1

    logger.info(f"[{datetime.now()}] Число запросов за день: {count_requests_in_day}") 

    
    prompt = f"""
                Ты — HR-эксперт с 10+ лет опыта в подборе IT-специалистов. Проведи профессиональный аудит резюме кандидата.

        Твоя цель — помочь кандидату улучшить резюме для ИТ-рынка, избегая критики, домыслов и повторения текста резюме.

        Формат ответа:

        Стиль: Telegram-сообщение

        Объем: 2000–2500 символов

        Тон: профессиональный и дружелюбный

        Без Markdown, только жирный текст и emoji

        Используй одинаковый стиль оформления во всех разделах

        Каждый пункт — это конкретная рекомендация или вывод

        Не пиши от третьего лица (не "у кандидата", а просто по факту)

        Не делай обобщений и общих фраз ("нужно улучшить" и т.п.)

        ОБЯЗАТЕЛЬНО:

        Структура и порядок блоков всегда одинаковый

        Внутри разделов — списки с маркерами (•), максимум 3–5 пунктов

        Используй только эти emoji:
        🎓 Образование  
        📚 Курсы и сертификаты  
        💼 Опыт работы  
        🛠 Технические навыки  
        📊 Соответствие рынку  
        🌟 Итоговая оценка  
        Структура ответа (следовать строго):

        🎓 Образование
        • Релевантность для целевой позиции
        • Есть ли пробелы по домену/навыкам
        • Какие курсы/обучение стоит пройти

        📚 Курсы и сертификаты
        • Какие навыки подтверждены
        • Какие сертификаты стоит добавить
        • Что усилит резюме на рынке труда

        💼 Опыт работы
        • Конкретные достижения (в цифрах, в проектах)
        • Чего не хватает: метрики, роли, масштаб
        • Рост: как обозначить карьерную прогрессию

        🛠 Технические навыки
        • Какие технологии соответствуют позиции
        • Что критично добавить (например, BI, Kafka, API, etc.)
        • Баланс: hard и soft skills — что усилить

        📊 Соответствие рынку
        • Уровень (Junior/Middle/Senior) по опыту
        • Зарплатные ожидания — указаны ли, соответствуют ли
        • ТОП-3 ключевых пробела для вакансий

        🌟 Итоговая оценка
        • Общий балл (по 10-балльной шкале)
        • Потенциал роста (в чем сила)
        • 2–3 рекомендации: срочно и в перспективу

        Резюме для анализа:
        {pdf_file}
        """

    loop = asyncio.get_event_loop()
    completion = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
            extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
            "X-Title": "<YOUR_SITE_NAME>",      # Optional
            },
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp
        )
    )

    return completion.choices[0].message.content

def hh(vacancy_id):
    vacancy_id = vacancy_id.split('/')[-1]
    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    data = requests.get(url).json()
    return data['description']

async def get_db_connection():
    return await asyncpg.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

async def bd_user() -> List[str]:
    conn = await get_db_connection()
    try:
        records = await conn.fetch("SELECT user_id FROM users")
        return [str(record['user_id']) for record in records]
    finally:
        await conn.close()

async def bd_user_add(user_id: str, name: str, username: str):
    conn = await get_db_connection()
    try:
        await conn.execute(
            "INSERT INTO users (user_id, name, username) VALUES ($1, $2, $3)",
            user_id, name, username
        )
    finally:
        await conn.close()

async def check_and_add_user(user_id: str, name: str, username: str):
    try:
        users_list = await bd_user()
        print(f"User {user_id} exists: {user_id in users_list}")
        if user_id not in users_list:
            await bd_user_add(user_id, name, username)
            print(f"User {user_id} added to DB")
    except Exception as e:
        print(f"Error in check_and_add_user: {e}")
        raise

import asyncpg

async def load_vacancies_for_analysis(vacancy_category):
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
        
        # 1. Загрузка вакансий
        records = await conn.fetch(
            f"SELECT title, salary, skills, location, experience, link FROM vacans WHERE new_category like '%{vacancy_category}' and date >= CURRENT_DATE - INTERVAL '3 day'"
        )
        logger.info(f"[{datetime.now()}] Скачали последние вакансии для анализа в функции Прожарки резюме") 
        return records
        
    except Exception as e:
        logger.info(f"[{datetime.now()}] Ошибка загрузки данных: {e}") 
        return {}, {}
    finally:
        if conn:
            await conn.close()


async def hot_resume(pdf_text, vacancy_category,  temp = 0.8):
    global count_requests_in_day

    client = get_client()

    count_requests_in_day+=1

    logger.info(f"[{datetime.now()}] Число запросов за день: {count_requests_in_day}") 

    logger.info(f"[{datetime.now()}] Зашли в функцию hot_resume") 
    
    vacancies = await load_vacancies_for_analysis(vacancy_category)
    logger.info(f"[{datetime.now()}] Перешли к промту") 
    prompt = f"""
        Ты — HR-эксперт с 10+ лет опыта в IT-рекрутинге. 
        Проанализируй резюме для позиции {vacancy_category} и дай рекомендации, которые увеличат шансы на отклик на 50%. 

        **Жесткие правила:**
        1. Только факты из резюме (не додумывай)
        2. Сравнивай с вакансиями {vacancies[:25]}, Не используй в ответах тег <record>, используй только названия и ссылки
        3. Пиши как личный консультант
        4. Макс. 2500 символов
        5. Из тегов используй только <b> для выделения жирного текста, строго не используй курсив и теги <think>. Не используй в ответе '#'.
        6. Используй ссылки на вакансии только в пункте "Наиболее релевантные вакансии за последнюю неделю"

        **Структура ответа (Telegram-форматирование):**
        🎯 <b>Главная проблема</b>: 1-2 предложения
        📊 <b>Число подходящих вакансий</b>: "За последнюю неделю было X подходящих вашему описанию вакансий"
        💼 <b>Соответствие роли</b>: 3 пункта (совпадение/нехватка)
        🛠 <b>ТОП-3 исправления</b> (конкретные примеры):
        1. Заменить "фраза из резюме" → "оптимизированная версия"
        2. Добавить навык "самый частый skill из вакансий"
        3. Удалить "нерелевантный пункт"
        🔗 <b>Ресурсы</b>: Совет что необходимо выучить
        4. Наиболее релевантные вакансии за последнюю неделю: ссылки только из текстов вакансий, который тебе прислали.

        Резюме:
        {pdf_text}
        """

    loop = asyncio.get_event_loop()
    completion = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
            extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
            "X-Title": "<YOUR_SITE_NAME>",      # Optional
            },
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp
        )
    )
    text = completion.choices[0].message.content
    logger.info(f"[{datetime.now()}] Полученная генерация {text}") 

    return text