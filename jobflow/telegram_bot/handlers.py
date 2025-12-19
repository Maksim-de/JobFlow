from aiogram import Bot, Router, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from JobFlow.jobflow.telegram_bot.states import *
from JobFlow.jobflow.analysis_cv.api_handler import *
from aiogram.utils.markdown import hbold, hitalic, hunderline, text, code
import io
import asyncio
import json
import html
import re
from aiogram.utils.markdown import html_decoration as hd
from bs4 import BeautifulSoup
import re
from markdown import markdown
from JobFlow.config import *
import yookassa
from yookassa import Payment, Configuration

vacanciessss = {}
hr_vacanciess = {}
yookassa.Configuration.account_id = '1138549'
yookassa.Configuration.secret_key = 'test_XUnT2LyiO1DHyfNV9AInV6xPTeuuXxPyjXv41V7Hggk'

category_keywords = {
 "Аналитика": {
    "keywords": [
      "аналитик", 'systems_analyst', 'data_analyst', 'business_analyst', 'bi-аналитик', 'бизнес-аналитик', 'marketing_analyst', 
      'bi_developer', 'bi-аналитик, аналитик данных'
    ],
    "subcategories": {
      "Системный аналитик": [
        "системн", "systems_analyst",  "uml"
      ],
      "Бизнес аналитик": [
        "бизнес", "business", 'бизнес-аналитик'
      ],
      "Data аналитик и BI": [
        'data_analyst', 'bi-аналитик', "bi_developer", 'bi-аналитик, аналитик данных'
      ],
      "Продуктовый аналитик": [
        "продуктов", "product", "a/b", "ab test", "a/b test", 'продуктовый аналитик'
      ],
      "Аналитик DWH": [
        "data engineer", "dwh", "data warehouse", "airflow", "data lake",
        "databricks", "spark", "hadoop", 'sql'
      ],
      "Веб-аналитик": [
        "веб", "web",
      ],
      "Аналитика (Другое)": []
  }
},
 "Тестирование": {
    "keywords": [
      "тестировщик", "tester", "qa", "quality assurance", "тестировщик-автоматизатор",
      "qa engineer", "инженер по тестирован", "ручн тестирован", "автоматизирован тестирован",
      "мобильн тестирован", "веб тестирован", "гейм тестирован", "api тестирован",
      "безопасност тестирован", "производительност тестирован", "нагрузочн тестирован",
      "интеграцион тестирован", "регрессион тестирован", "smoke тестирован", "приемочн тестирован",
      "quality manager", "qa lead", "qa architect", 'manual_testing', 'test_automation', 'qa_engineer'
    ],
    "subcategories": {
      "Ручное тестирование": [
        "ручн тестировщик", 'ручное', 'ручного', 'manual_testing'
      ],
      "Автоматизированное тестирование": [
        "автоматизатор тестирован", "automation tester", "qa automation", "test_automation"
      ],
     "Тестирование (Другое)": []
    }
},
 "Разработка": {
    "keywords": [
      "frontend", "front-end", "front end", "javascript", "js",
      "react", "angular", "vue", "typescript", 'software',
      "backend", 'devops', 'mobileapp_developer', "data_engineer", 'database_developer', 
      "fullstack", "full-stack", "full stack", "DevOps-инженер"
    ],
    "subcategories": {
      "Frontend разработка": [
        "frontend", "front-end", "front end", "javascript", "js",
        "react", "angular", "vue", "typescript", "ui developer"
      ],
      "Backend разработка": [
        "backend", "back-end", "back end", "server", "api",
        "python", "java", "php", "node", "nodejs", "net", "ruby", "go", "golang"
      ],
      "Fullstack разработка": [
        "fullstack", "full-stack", "full stack", 
      ],
      "Мобильная разработка": [
        "mobile", "android", "ios", "flutter", "react",
        "котлин", "kotlin", "swift", "mobileapp_developer"
      ],
      "DevOps": [
        "devops", "DevOps-инженер"
      ], 
      "Data engineer": [
        "data_engineer", 'database_developer'
      ],
  "Разработка (Другое)": []
    }
},
 "ML/AI/DS": {
    "keywords": [ 
      "ml engineer", "ml-engineer", "mlops", 'data_scientist', 'ml', 'ai', 'промт', 'дата-сайентист'
    ],
    "subcategories": {
      "Data Science": [
        "data science", "анализ данн", "дата-сайентист", "data_scientist", 'дата-сайентист'
      ],
      "ML Engineering": [
        "ml engineer", "ml-engineer", "mlops", "model serving"
      ],
       "AI (Другое)": []
    }
},
 "Менеджмент": {
    "keywords": [
      'менеджер продукта', 'руководитель группы разработки', 'руководитель отдела аналитики', "руководитель проектов", 'project_manager',
      'project_director', 'product_manager', 'marketing_manager', 'account_manager'
    ],

    "subcategories": {
      "Продуктовый менеджмент": [
        "продуктов менеджер", "product manager", "PM", "product owner",
        "руководитель продукт", "head of product", 'product_manager'
      ],
      "Проектный менеджмент": [
        "проектн менеджер", "project manager", "PM", "руководитель проектов", 'project_manager', 'scrum_master', 'account_manager'
      ],
      "ИТ топ менеджмент": [
        'руководитель группы разработки',  'руководитель отдела аналитики', 'технический директор (сто)',  'project_director'
      ],

"Менеджмент (Другое)": []
 }
    }
}



from aiogram import F
from aiogram.types import Message, FSInputFile




router = Router()

users = {}

selected_subcategories = {}

selected_cities = {}

user_expierence = {}


user_subspecializations = {}

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.filters import Command
from aiogram import html as h
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Главное меню
main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Поиск вакансий")],
    [KeyboardButton(text="🎨 Настроить автоотклик"), KeyboardButton(text="AI ассистент")],
    [KeyboardButton(text="Подписка")],
    [KeyboardButton(text="Опубликовать вакансию"), KeyboardButton(text="Помощь")]
], resize_keyboard=True)

# Меню категорий вакансий
categories_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Аналитика"), KeyboardButton(text="Разработка")],
    [KeyboardButton(text="Тестирование"), KeyboardButton(text="ML/AI/DS")],
    [KeyboardButton(text="Менеджмент")],
    [KeyboardButton(text="Отписаться от рассылки вакансий")],
    [KeyboardButton(text="В главное меню"), KeyboardButton(text="Готово")]
], resize_keyboard=True)

expierence_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Нет опыта"), KeyboardButton(text="От 1 года до 3 лет")],
    [KeyboardButton(text="От 3 до 6 лет"), KeyboardButton(text="Более 6 лет")],
    [KeyboardButton(text="Назад в категории"),KeyboardButton(text="Готово")]
    
], resize_keyboard=True)


# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    # user_id = message.from_user.id
    user_id = str(message.from_user.id)
    await state.set_state(Form.user_id)
    await state.update_data(user_id=user_id) 
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку start")

    username = (
        message.from_user.username 
        if message.from_user.username 
        else f"id{message.from_user.id}"
    )

    await check_and_add_user(user_id, message.from_user.first_name, username)
    


    welcome_text = (
    "👋 <b>Привет, {name}!</b>\n\n"
    "Я твой персональный HR-ассистент, который поможет найти работу мечты!\n\n"
    "📌 <b>Что я умею:</b>\n\n"
    "🔍 Искать вакансии по твоим критериям\n"
    "📝 Анализировать твоё резюме и давать рекомендации\n"
    "📝 Мой канал: @mrJobHunter\n\n"
   
    "Для работы со мной просто используй кнопки меню ниже 👇\n\n"
    "<i>Если что-то пойдёт не так, ты всегда можешь перезапустить меня командой /start</i>\n\n"
    "Ваш feedback помогает нам становиться лучше! Ошибки и предложения принимаются через кнопку <b>Помощь</b>."
        ).format(name=message.from_user.first_name)


    await message.answer(welcome_text,  parse_mode="HTML", reply_markup=main_keyboard)
    logger.info(f"Пользователю {message.from_user.id} {message.from_user.username} отправлен welcome_text")





@router.message(lambda message: message.text == "Подписка")
async def auto_response(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} начал настройку подписки")

    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="/premium")],
            [KeyboardButton(text="В главное меню")]
        ]
    )
    url = "https://redirect-maksim-arkhipov.amvera.io/get_flag_prem"
    user_id =  str(message.from_user.id)

    params = {"user_id": user_id} 
    print(user_id)
    try:
        answ = requests.get(url, params=params)
        print(answ.json())
        prem_active_flag = answ.json()[0]['is_premium']
        prem_date = answ.json()[0]['premium_date']
        prem_date = datetime.strptime(prem_date, "%Y-%m-%dT%H:%M:%S.%f") # Формат может отличаться!
        current_date = datetime.now()
        print(prem_active_flag)
        print(prem_date)
        remaining_time = prem_date - current_date
        print(remaining_time)
    except Exception as e:
        prem_active_flag = None
        remaining_time = 0
        print(e)
    try:
        if prem_active_flag is True and remaining_time.seconds // 3600 > 0:
            print('зашли')
            mess = (
            "💎 <b>Подписка активна до:</b>\n"
            f"📅 {prem_date.strftime('%d.%m.%Y %H:%M')}\n"
            f"⏳ Осталось: {remaining_time.seconds // 3600} часов"
            )

            await message.answer(mess,
            reply_markup=markup,
            parse_mode="HTML"
            )
        else:
            mess = (
                "💎 <b>Премиум-подписка даст вам решающее преимущество:</b>\n\n"
                "🔹 <b>В 3 раза больше откликов</b>\n"
                "• Безлимитные автоотклики\n"
                "• Ваши заявки видны работодателям <u>первыми</u>\n\n"
                "🔹 <b>Экспертная прожарка резюме</b>\n"
                "• Неограниченный анализ AI-ассистентом\n"
                "• Точечные исправления для прохождения ATS\n\n"
                "🔥 <b>Спецпредложение:</b>\n"
                "• <i>90₽/день</i> — тестовый доступ ко всем функциям\n"
                "• <i>490₽/неделю</i> (выгода 63%) — оптимальный вариант\n\n"
                "👉 Нажмите /premium для мгновенного доступа"
            )

            await message.answer(mess,
                reply_markup=markup,
                parse_mode="HTML"
            )

    except:
        await message.answer(
            "Попробуйте чуть позже\n\n",
            reply_markup=categories_keyboard,
            parse_mode="Markdown"
        )

@router.message(Command("premium"))
async def auto_response(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} начал оплату подписки")

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 1 день - 90₽", callback_data="premium_1day")],
        [InlineKeyboardButton(text="🔥 1 неделя - 490₽ (Выгода 63%)", callback_data="premium_7days")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="premium_help")]
    ])
    

    try:

        mess =(
            "👉 Выберите тариф:"
        )

        await message.answer(mess, reply_markup=markup, parse_mode="HTML")

    except:
        await message.answer(
            "Попробуйте чуть позже\n\n",
            reply_markup=categories_keyboard,
            parse_mode="Markdown"
        )

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery




@router.callback_query(lambda c: c.data.startswith("premium_"))
async def process_premium_selection(callback: CallbackQuery):
    action = callback.data.split("_")[1]
    
    if action == "help":
        await callback.message.answer("📩 По вопросам подписки пишите @pirici_pip")
        return
    
    # Определяем тариф
    tariff = {
        "1day": {"price": 90.00, "days": 1},
        "7days": {"price": 490.00, "days": 7}
    }.get(action)
    
    if not tariff:
        await callback.answer("Неизвестный тариф")
        return
    
    # Создаем платеж @CharacterMind_bot
    try:
        payment = Payment.create({
            "amount": {"value": tariff["price"], "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": f"https://t.me/HrJobVacancy_Bot"
            },
            "capture": True,
            "description": f"Премиум подписка на {tariff['days']} дней",
            "metadata": {
                "user_id": callback.from_user.id,
                "tariff": action,
                "days": tariff["days"]
            }
        })

        try:
            payment_id = payment.id
            url = "https://redirect-maksim-arkhipov.amvera.io/send_payment_link"
            user_id =  str(callback.from_user.id)
            print(callback.message.from_user.id)
            params = {"user_id": user_id, "payment_id": payment_id} 
            print(user_id)

            answ = requests.get(url, params=params)

            print(answ)
            print(user_id)
       
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить", url=payment.confirmation.confirmation_url)],
                [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"check_{action}")]
            ])
            
            await callback.message.edit_text(
                f"🛒 Тариф: <b>{tariff['days']} день</b>\n"
                f"💵 Сумма: <b>{tariff['price']}₽</b>\n\n"
                "1. Нажмите «Оплатить»\n"
                "2. После оплаты — «Я оплатил»",
                reply_markup=markup,
                parse_mode="HTML"
            )
        except: 
            logger.error(f"Ошибка создания платежа: {e}")
            await callback.message.answer("Ошибка при создании платежа. Попробуйте позже.")


        
    except Exception as e:
        logger.error(f"Ошибка создания платежа: {e}")
        await callback.message.answer("Ошибка при создании платежа. Попробуйте позже.")


@router.callback_query(lambda c: c.data.startswith("check_"))
async def check_payment(callback: CallbackQuery):
    tariff = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    try:
        # Здесь должна быть проверка платежа через API ЮKassa
        # В реальном коде используйте Payment.find(payment_id)

        url = "https://redirect-maksim-arkhipov.amvera.io/get_payment_link"
        user_id =  str(callback.from_user.id)
        print(callback.message.from_user.id)
        params = {"user_id": user_id} 
        print(user_id)

        

        payment_id = requests.get(url, params=params)

        print(payment_id.json()['message'])
        payment_id = payment_id.json()['message']
        pay = Payment.find_one(payment_id)

        print(pay)
        print(pay.status)
        
        # Для примера - эмулируем успешную оплату
        payment_status = pay.status  # В реальном коде получаем от API
        
        if payment_status == "succeeded":
            days = 1 if tariff == "1day" else 7
            expiry_date = datetime.now() + timedelta(days=days)

            url_for_update = "https://redirect-maksim-arkhipov.amvera.io/update_flag_prem"
            
            try:
                params = {"user_id": user_id, 'premium_date': expiry_date} 
                udp = requests.get(url_for_update, params=params)
                print('все получилось')
                # Сохраняем в БД (пример для SQLite)
            except:
                print('ошибка обновлния')

            
            await callback.message.edit_text(
                f"✅ <b>Оплата подтверждена!</b>\n\n"
                f"Премиум-доступ активен до {expiry_date.strftime('%d.%m.%Y')}",
                parse_mode="HTML"
            )
        else:
            await callback.answer("Платеж не найден. Попробуйте позже.", show_alert=True)
            
    except Exception as e:
        logger.error(f"Ошибка проверки платежа: {e}")
        await callback.answer("Ошибка при проверке платежа", show_alert=True)

@router.message(lambda message: message.text == "🎨 Настроить автоотклик")
async def auto_response(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} начал настройку автооткликов")
    # await state.set_state(Form.auto)
    url = "https://redirect-maksim-arkhipov.amvera.io/generate_link"

    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Далее")],
            [KeyboardButton(text="Отключить автоотклик")],
            [KeyboardButton(text="В главное меню")]
        ]
    )
    params = {"user_id": message.from_user.id} 
    try:
        response = requests.post(url, params=params) 

        mess = (
            "👋 <b>Давайте настроим автоотклик на вакансии!</b>\n\n"
            "🛠 <b>Шаг 1 из 3:</b> Подключение аккаунта HH\n\n"
            "Для работы автоотклика нужно однократно авторизоваться:\n\n"
            "▫️ Если вы <b>уже авторизовались</b> ранее - просто нажмите <b>Далее</b>\n"
            "▫️ Если <b>ещё нет</b> - пройдите быструю авторизацию:\n\n"
            "1. Нажмите на ссылку ниже\n"
            "2. Разрешите доступ к вашему профилю HH\n"
            "3. Вернитесь в бот и нажмите <b>Далее</b>\n\n"
            f"🔗 <a href='{response.text[1:-1]}'>Перейти к авторизации</a>\n\n"
            "<i>Это безопасно - мы получаем только базовый доступ для работы с откликами</i>"
        )

        await message.answer(mess,
            reply_markup=markup,
            parse_mode="HTML"
        )

    except:
        await message.answer(
            "Попробуйте чуть позже\n\n",
            reply_markup=categories_keyboard,
            parse_mode="Markdown"
        )


@router.message(lambda message: message.text == "Отключить автоотклик")
async def auto_response(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} начал отключение автооткликов")
    # await state.set_state(Form.auto)
    url = "https://redirect-maksim-arkhipov.amvera.io/disable_auto"


    params = {"user_id": message.from_user.id} 
    try:
        response = requests.post(url, params=params) 

         
        success_message = (
            "✅ <b>Автоотклики успешно отключены!</b>\n\n"
            "Если захотите снова их включить - просто повторите те же действия, "
            "что и при первоначальной настройке.\n\n"
            "Хорошего дня! 😊"
        )

        await message.answer(success_message,
            reply_markup=main_keyboard,
            parse_mode="HTML"
        )

    except:
        await message.answer(
            "Попробуйте чуть позже\n\n",
            reply_markup=categories_keyboard,
            parse_mode="Markdown"
        )
    
    
    
# @router.message(lambda message: message.text == "Далее")
# async def resume(message: Message, state: FSMContext):
#     logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку Далее")
#     # await state.set_state(Form.auto)
#     url_access_token = "https://redirect-maksim-arkhipov.amvera.io/get_access_token_from_bd"
#     url = "https://redirect-maksim-arkhipov.amvera.io/get_resume"

#     params = {"user_id": message.from_user.id} 

#     markup = ReplyKeyboardMarkup(
#         resize_keyboard=True,
#         keyboard=[
#             [KeyboardButton(text="Все верно")],
#             [KeyboardButton(text="Другое резюме")],
#             [KeyboardButton(text="В главное меню")]
#         ]
#     )


#     try:
#         access_token = requests.get(url_access_token, params=params)

        

#         params = access_token.json()[0]

#         await state.update_data(access_token=access_token.json()[0]['access_token']) 

#         response = requests.get(url, params=params) 


#         resume = response.json()['items']

#         if resume[0]['total_experience']['months'] == 0:
#             exp = 'Нет опыта'
#         elif resume[0]['total_experience']['months'] < 36:
#             exp = 'От 1 года до 3 лет'
#         elif resume[0]['total_experience']['months'] < 72:
#             exp = 'От 3 до 6 лет'
        
#         mess = (
#             f"🔍 Ваше резюме!\n\n"
#             f"📌 Название: {resume[0]['title']}\n"
#             f"📌 Город: {resume[0]['area']['name']}\n"
#             f"📌 Опыт работы: {exp}/ {resume[0]['total_experience']['months']} месяцев\n"
#             "──────────────────\n"
#             f"Если это верное резюме нажмите <b>Все верно</b>\n"
#         )

#         await state.update_data(resume_id=resume[0]['id']) 

#         await message.answer(mess,
#             reply_markup=markup,
#             parse_mode="HTML"
#         )


#     except:
#         await message.answer(
#             "Попробуйте чуть позже\n\n",
#             reply_markup=categories_keyboard,
#             parse_mode="Markdown"
#         )

@router.message(lambda message: message.text == "Далее")
async def resume(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку Далее")
    await show_resume(message, state, resume_index=0)

@router.message(lambda message: message.text == "🔄 Другое резюме")
async def another_resume(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} запросил другое резюме")
    data = await state.get_data()
    current_index = data.get('resume_index', 0)
    await show_resume(message, state, resume_index=current_index + 1)

async def show_resume(message: Message, state: FSMContext, resume_index: int):
    url_access_token = "https://redirect-maksim-arkhipov.amvera.io/get_access_token_from_bd"
    url = "https://redirect-maksim-arkhipov.amvera.io/get_resume"

    params = {"user_id": message.from_user.id} 

    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="✅ Все верно")],
            [KeyboardButton(text="🔄 Другое резюме")],
            [KeyboardButton(text="В главное меню")]
        ]
    )

    try:
        access_token = requests.get(url_access_token, params=params)
        params = access_token.json()[0]
        await state.update_data(access_token=access_token.json()[0]['access_token']) 

        response = requests.get(url, params=params) 
        resumes = response.json()['items']

        print(resumes)
        print(len(resumes))

        # Сохраняем текущий индекс резюме
        await state.update_data(resume_index=resume_index)
        
        # Проверяем, есть ли резюме с таким индексом
        if resume_index >= len(resumes):
            await message.answer("🔁 Вы просмотрели все резюме. Показываю первое.", reply_markup=markup)
            resume_index = 0
            await state.update_data(resume_index=0)

        resume = resumes[resume_index]

        if resume['total_experience'] is None:
            exp = 'Нет опыта'
        elif resume['total_experience']['months'] == 0:
            exp = 'Нет опыта'
        elif resume['total_experience']['months'] < 36:
            exp = 'От 1 года до 3 лет'
        elif resume['total_experience']['months'] < 72:
            exp = 'От 3 до 6 лет'
        else:
            exp = 'Более 6 лет'
        
        if resume['title'] is None:
            resume['title'] = 'Не определено'
        if resume['area']['name'] is None:
            resume['area']['name'] = 'Не определено'
        
        mess = (
            f"📄 <b>Ваше резюме #{resume_index + 1}</b>\n\n"
            f"🏷 <b>Название:</b> {resume['title']}\n"
            f"🌆 <b>Город:</b> {resume['area']['name']}\n"
            f"⏳ <b>Опыт работы:</b> {exp}\n\n"
            "────────────────────\n"
            "Это ваше актуальное резюме?\n"
            "• Да - <b>✅ Все верно</b>\n"
            "• Нет - <b>🔄 Другое резюме</b>"
        )


        await state.update_data(resume_id=resume['id']) 

        await message.answer(mess,
            reply_markup=markup,
            parse_mode="HTML"
        )

    except Exception as e:
        logger.error(f"Ошибка при получении резюме: {e}")
        await message.answer(
            "😕 Не удалось загрузить резюме. Пожалуйста, попробуйте позже.\n"
            "Если проблема повторяется, обратитесь в поддержку.",
            reply_markup=categories_keyboard,
            parse_mode="Markdown"
        )


    # Тут
    
@router.message(lambda message: message.text == "✅ Все верно")
async def handle_correct_resume(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    logger.info(f"Пользователь {user_id} подтвердил резюме")
    
    # Инициализируем выбор подкатегорий
    if user_id not in user_subspecializations:
        user_subspecializations[user_id] = set()

    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Аналитика"), KeyboardButton(text="Разработка")],
            [KeyboardButton(text="Тестирование"), KeyboardButton(text="ML/AI/DS")],
            [KeyboardButton(text="Менеджмент")],
            [KeyboardButton(text="В главное меню")]
        ]
    )
    
    await message.answer(
        "📌 Отлично! Теперь выбери специализацию",
        reply_markup=markup
    )
    await state.set_state(Form.waiting_for_specialization)


@router.message(Form.waiting_for_specialization, lambda message: message.text in category_keywords.keys())
async def handle_specialization_selection(message: Message, state: FSMContext):
    specialization = message.text
    user_id = str(message.from_user.id)
    
    # Сохраняем выбор специализации
    await state.update_data(specialization=specialization)
    
    # Инициализируем пустое множество для выбранных подспециализаций
    await state.update_data(selected_subspecializations=set())
    
    await message.answer(
        f"📌 Ты выбрал специализацию: <b>{specialization}</b>\n\n"
        "Теперь укажи конкретные направления (можно выбрать несколько):",
        reply_markup= await get_subspecializations_keyboard(specialization, state),
        parse_mode="HTML"
    )
    await state.set_state(Form.waiting_for_subspecialization)



async def get_subspecializations_keyboard(specialization: str, user_id: str = None) -> ReplyKeyboardMarkup:
    """Создает клавиатуру подкатегорий с галочками"""
    builder = ReplyKeyboardBuilder()
    
    # Получаем подкатегории для выбранной специализации
    subspecializations = category_keywords[specialization]["subcategories"].keys()
    
    # Добавляем кнопки с галочками для выбранных
    for subspec in subspecializations:
        if user_id and user_id in user_subspecializations and subspec in user_subspecializations[user_id]:
            text = f"✅ {subspec}"
        else:
            text = subspec
        builder.add(KeyboardButton(text=text))
    
    builder.adjust(2)
    
    # Кнопки управления
    builder.row(
        KeyboardButton(text="Назад в категории"),
        KeyboardButton(text="Готово")
    )
    
    return builder.as_markup(resize_keyboard=True)

@router.message(Form.waiting_for_subspecialization, lambda message: message.text == "Назад в категории")
async def handle_back_to_categories(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    logger.info(f"Пользователь {user_id} вернулся к выбору категорий")
    
    # Очищаем выбранные подкатегории при возврате
    # if user_id in user_subspecializations:
    #     user_subspecializations[user_id].clear()
    
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Аналитика"), KeyboardButton(text="Разработка")],
            [KeyboardButton(text="Тестирование"), KeyboardButton(text="ML/AI/DS")],
            [KeyboardButton(text="Менеджмент")],
            [KeyboardButton(text="В главное меню")]
        ]
    )
    
    await message.answer(
        "🔙 Возвращаемся к выбору категории\n\n",
        reply_markup=markup
    )
    await state.set_state(Form.waiting_for_specialization)



@router.message(
    Form.waiting_for_subspecialization,
    lambda message: any(
        message.text.replace("✅ ", "") in subcats 
        for cat in category_keywords.values() 
        for subcats in cat["subcategories"].keys()
    )
)
async def handle_subspecialization_selection(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    subspecialization = message.text.replace("✅ ", "")
    
    # Получаем выбранную специализацию
    data = await state.get_data()
    specialization = data['specialization']
    
    # Добавляем или удаляем подкатегорию
    if subspecialization in user_subspecializations.get(user_id, set()):
        user_subspecializations[user_id].remove(subspecialization)
        action = "❌ Убрано из выбора"
    else:
        user_subspecializations[user_id].add(subspecialization)
        action = "✅ Добавлено к выбору"
    
    # Формируем текущий выбор
    selected = "\n".join(f"✅ {subspec}" for subspec in user_subspecializations.get(user_id, []))
    if not selected:
        selected = "Пока ничего не выбрано"
    
    await message.answer(
        f"{action}: <b>{subspecialization}</b>\n\n"
        f"<b>Твой текущий выбор:</b>\n\n{selected}\n\n"
        "Можешь продолжить выбирать или нажать <b>«Готово»</b>",
        reply_markup=await get_subspecializations_keyboard(specialization, user_id),
        parse_mode="HTML"
    )


@router.message(Form.waiting_for_subspecialization, lambda message: message.text == "Готово")
async def handle_subspecialization_done(message: Message, state: FSMContext, bot: Bot):
    user_id = str(message.from_user.id)
    data = await state.get_data()
    specialization = data['specialization']
    
    if not user_subspecializations.get(user_id):
        await message.answer("⚠️ Ты не выбрал ни одного направления.\n\n"
                           "Пожалуйста, выбери хотя бы один вариант.")
        return
    
    # Получаем город из резюме (аналогично функции resume)
    url_access_token = "https://redirect-maksim-arkhipov.amvera.io/get_access_token_from_bd"
    url_resume = "https://redirect-maksim-arkhipov.amvera.io/get_resume"
    
    try:
        # Получаем токен и резюме
        access_token = requests.get(url_access_token, params={"user_id": message.from_user.id})
        params = access_token.json()[0]
        response = requests.get(url_resume, params=params)
        resume_data = response.json()['items'][0]
        
        city = resume_data['area']['name']
        
        # Сохраняем город в состоянии
        await state.update_data(resume_city=city)
        
        # Клавиатура для подтверждения города
        city_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Оставить как в резюме")],
                [KeyboardButton(text="Изменить город")],
                [KeyboardButton(text="В главное меню")]
            ],
            resize_keyboard=True
        )
        
        await message.answer(
            "🛠 <b>Шаг 2 из 3:</b> Выбери город\n\n"
            f"📍 Твой город в резюме: <b>{city}</b>\n\n"
            "Хочешь оставить этот город или изменить?",
            reply_markup=city_keyboard,
            parse_mode="HTML"
        )
        
        # Переходим в состояние ожидания выбора по городу
        await state.set_state(Form.waiting_for_city_confirmation)
        
    except Exception as e:
        logger.error(f"Ошибка при получении резюме: {e}")
        await message.answer(
            "⚠️ Не удалось получить информацию о городе из резюме.\n"
            "Попробуйте позже или укажите город вручную.",
            reply_markup=main_keyboard
        )
        await state.clear()


selected_cities_auto = {}

def get_cities_keyboard_auto(user_id: int = None) -> ReplyKeyboardMarkup:
    """Клавиатура выбора городов ТОЛЬКО для автоотклика"""
    builder = ReplyKeyboardBuilder()
    
    # Кнопки управления
    builder.row(KeyboardButton(text="Назад"))
    builder.row(KeyboardButton(text="Готово"))
    
    # Приоритетные города
    priority_cities = [
        "Москва", "Санкт-Петербург", "Казань", "Новосибирск", 
        "Екатеринбург", "Красноярск", "Нижний Новгород", "Челябинск", 
        "Уфа", "Самара", "Ростов-на-Дону", "Краснодар", "Омск", 
        "Воронеж", "Пермь", "Волгоград"
    ]

    for city in priority_cities:
        if user_id and user_id in selected_cities_auto and city in selected_cities_auto[user_id]:
            text_button = f"✅ {city}"
        else:
            text_button = city
        builder.add(KeyboardButton(text=text_button))
    
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)




@router.message(
    Form.waiting_for_cities_auto, 
    lambda message: message.text.replace("✅ ", "") in [
        "Москва", "Санкт-Петербург", "Казань", "Новосибирск",
        "Екатеринбург", "Красноярск", "Нижний Новгород", "Челябинск",
        "Уфа", "Самара", "Ростов-на-Дону", "Краснодар", "Омск",
        "Воронеж", "Пермь", "Волгоград"
    ]
)
async def handle_city_selection_auto(message: Message):
    user_id = str(message.from_user.id)
    city = message.text.replace("✅ ", "")
    
    if user_id not in selected_cities_auto:
        selected_cities_auto[user_id] = set()
    
    if city in selected_cities_auto[user_id]:
        selected_cities_auto[user_id].remove(city)
        action = "❌ Убрано из выбора"
    else:
        selected_cities_auto[user_id].add(city)
        action = "✅ Добавлено к выбору"
    
    selected = "\n".join(selected_cities_auto.get(user_id, ["Пока ничего не выбрано"]))
    
    await message.answer(
        f"{action}: {city}\n\n"
        f"Текущий выбор:\n{selected}\n\n"
        "Продолжайте выбирать или нажмите «Готово»",
        reply_markup=get_cities_keyboard_auto(user_id)
    )


@router.message(Form.waiting_for_city_confirmation, lambda message: message.text == "Оставить как в резюме")
async def handle_keep_city_as_in_resume(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    
    # Получаем город из сохраненных данных состояния
    data = await state.get_data()
    city = data.get('resume_city')
    
    if not city:
        await message.answer(
            "⚠️ Не удалось определить город из резюме. Пожалуйста, выберите город вручную.",
            reply_markup=get_cities_keyboard_auto(user_id)
        )
        await state.set_state(Form.waiting_for_cities_auto)
        return
    
    # Сохраняем выбранный город
    if user_id not in selected_cities_auto:
        selected_cities_auto[user_id] = set()
    selected_cities_auto[user_id].add(city)
    
    # Сохраняем город в состоянии
    await state.update_data(city=city)
    
    # Переходим к выбору опыта работы
    await message.answer(
        f"📍 Город сохранен: <b>{city}</b>\n\n"
        "🛠 <b>Шаг 3 из 3:</b> Критерии опыта работы\n\n"
        "Пожалуйста, укажите, на вакансии с каким опытом работы "
        "вы хотите получать автоотклики:\n\n"
        "📌 Можно выбрать несколько вариантов - просто нажмите на них.",
        reply_markup=get_experience_keyboard_auto(user_id),
        parse_mode="HTML"
    )
    await state.set_state(Form.waiting_for_experience_auto_response)



def get_experience_keyboard_auto(user_id: str = None) -> ReplyKeyboardMarkup:
    """Создает клавиатуру выбора опыта с галочками для выбранных вариантов"""
    builder = ReplyKeyboardBuilder()
    
    # Варианты опыта
    experience_options = [
        "Нет опыта", 
        "От 1 года до 3 лет",
        "От 3 до 6 лет", 
        "Более 6 лет"
    ]
    
    # Добавляем кнопки с учетом выбранных вариантов
    for option in experience_options:
        if user_id and user_id in user_expierence and option in user_expierence[user_id]:
            text = f"✅ {option}"
        else:
            text = option
        builder.add(KeyboardButton(text=text))
    
    builder.adjust(2)
    
    # Добавляем кнопки управления
    builder.row(
        KeyboardButton(text="Назад в категории"),
        KeyboardButton(text="Готово")
    )
    
    return builder.as_markup(resize_keyboard=True)



@router.message(Form.waiting_for_city_confirmation, lambda message: message.text == "Изменить город")
async def handle_change_city(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    await message.answer(
        "Выбери города для поиска:",
        reply_markup=get_cities_keyboard_auto(user_id)
    )
    await state.set_state(Form.waiting_for_cities_auto)


@router.message(Form.waiting_for_cities_auto, lambda message: message.text == "Готово")
async def handle_cities_done_auto(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    
    if not selected_cities_auto.get(user_id):
        await message.answer(
            "⚠️ Вы не выбрали ни одного города!",
            reply_markup=get_cities_keyboard_auto(user_id)
        )
        return
    
    await message.answer(
        "📌 Теперь укажи требуемый опыт работы:",
        reply_markup=get_experience_keyboard_auto(user_id)
    )
    await state.set_state(Form.waiting_for_experience_auto_response)


@router.message(
    Form.waiting_for_experience_auto_response,
    lambda message: message.text.replace("✅ ", "") in [
        "Нет опыта", 
        "От 1 года до 3 лет",
        "От 3 до 6 лет", 
        "Более 6 лет"
    ]
)
async def handle_experience_selection_auto(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    experience = message.text.replace("✅ ", "")
    
    # Инициализируем множество для пользователя, если его нет
    if user_id not in user_expierence:
        user_expierence[user_id] = set()
    
    # Добавляем или удаляем опыт
    if experience in user_expierence[user_id]:
        user_expierence[user_id].remove(experience)
        action = "❌ Убрано из выбора"
    else:
        user_expierence[user_id].add(experience)
        action = "✅ Добавлено к выбору"
    
    # Обновляем клавиатуру
    await message.answer(
        f"{action}: <b>{experience}</b>\n\n"
        "Можешь продолжить выбирать или нажать <b>«Готово»</b>",
        reply_markup=get_experience_keyboard_auto(user_id),
        parse_mode="HTML"
    )
@router.message(Form.waiting_for_experience_auto_response, lambda message: message.text == "Назад в категории")
async def back_from_experience_to_categories(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    logger.info(f"Пользователь {user_id} вернулся к выбору категорий")
    
    # Полностью очищаем состояние
    await state.clear()
    
    # Создаем клавиатуру категорий
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Аналитика"), KeyboardButton(text="Разработка")],
            [KeyboardButton(text="Тестирование"), KeyboardButton(text="ML/AI/DS")],
            [KeyboardButton(text="Менеджмент")],
            [KeyboardButton(text="В главное меню")]
        ]
    )
    
    await message.answer(
        "🔙 Возвращаемся к выбору категории\n\n"
        "Выберите специализацию:",
        reply_markup=markup
    )
    await state.set_state(Form.waiting_for_specialization)

@router.message(Form.waiting_for_experience_auto_response, lambda message: message.text == "Готово")
async def handle_experience_done_auto(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)

    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Включить автоотклик")],
            [KeyboardButton(text="В главное меню")]
        ]
    )
    
    if not user_expierence.get(user_id):
        await message.answer("⚠️ Ты не выбрал ни одного варианта опыта.\n\n"
                           "Пожалуйста, выбери хотя бы один вариант.")
        return
    
    # Получаем все выбранные настройки
    data = await state.get_data()
    resume_id = data.get('resume_id')
    print(resume_id)
    city = data.get('city', ", ".join(selected_cities.get(user_id, [])))
    selected_subspecs = "\n".join(f"• {subspec}" for subspec in user_subspecializations.get(user_id, []))
    selected_experience = "\n".join(f"• {exp}" for exp in user_expierence.get(user_id, []))
    
    # Формируем итоговое сообщение
    await message.answer(
        "🎉 <b>Автоотклик успешно настроен!</b>\n\n"
    "📋 <b>Ваши параметры поиска:</b>\n"
    f"├ <b>Специализации:</b>\n{selected_subspecs}\n"
    f"├ <b>Локация:</b> {city}\n"
    f"└ <b>Опыт работы:</b>\n{selected_experience}\n\n"
    "🚀 <b>Теперь вы можете:</b>\n"
    "• Нажать <b>'Включить автоотклик'</b> для автоматической рассылки\n"
    "• Или вернуться в меню для корректировки параметров\n\n"
    "ℹ️ <i>Лимит: 30 автооткликов в сутки</i>",
        reply_markup=markup,
        parse_mode="HTML"
    )
    
    # Здесь можно сохранить все настройки в базу
    # await state.clear()

@router.message(lambda message: message.text == "Включить автоотклик")
async def handle_experience_done_auto(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    url = "https://redirect-maksim-arkhipov.amvera.io/send_vacansy"

    
    # Получаем все выбранные настройки
    data = await state.get_data()
    resume_id = data.get('resume_id')
    print(resume_id)
    location = data.get('city', ", ".join(selected_cities.get(user_id, [])))
    print(location)
    vacancy_category = "\n".join(f"{subspec}" for subspec in user_subspecializations.get(user_id, []))
    experience = "\n".join(f"{exp}" for exp in user_expierence.get(user_id, []))

    access_token = data.get('access_token')
    
    params = {"vacancy_category": vacancy_category, "location": location, 'experience': experience, 'access_token': access_token, 'resume_id': resume_id} 
    try:
        print(params)
        await message.answer('Начинаем рассылать ваше резюме',
            reply_markup=main_keyboard,
            parse_mode="HTML"
        )
        response = requests.post(url, params=params) 

        print(response)
        print(response.json()['send'])

        markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="/premium")],
            [KeyboardButton(text="В главное меню")]
        ]
    )

        mess = (
            f"🚀 <b>Автоотклик успешно отправлен!</b>\n\n"
            f"📌 Вы использовали <b>{response.json()['send']} из 15</b> дневных откликов\n\n"
            "💎 <b>Премиум-подписка даст вам решающее преимущество:</b>\n\n"
            "🔹 <b>В 3 раза больше откликов</b>\n"
            "• Безлимитные автоотклики\n"
            "• Ваши заявки видны работодателям <u>первыми</u>\n\n"
            "🔹 <b>Экспертная прожарка резюме</b>\n"
            "• Неограниченный анализ AI-ассистентом\n"
            "• Точечные исправления для прохождения ATS\n\n"
            "🔥 <b>Спецпредложение:</b>\n"
            "• <i>90₽/день</i> — тестовый доступ ко всем функциям\n"
            "• <i>490₽/неделю</i> (выгода 63%) — оптимальный вариант\n\n"
            "📢 <b>Сейчас лучший момент подключить подписку</b> — ваше резюме уже в системе!\n\n"
            "👉 Нажмите /premium для мгновенного доступа"
        )

        await message.answer(mess,
            reply_markup=markup,
            parse_mode="HTML"
        )

    except:
        await message.answer(
            "Попробуйте чуть позже\n\n",
            reply_markup=categories_keyboard,
            parse_mode="Markdown"
        )



@router.message(Form.waiting_for_experience_auto_response, lambda message: message.text == "Назад")
async def back_from_experience_auto(message: Message, state: FSMContext):
    # Возвращаемся к выбору города
    data = await state.get_data()
    if 'resume_city' in data:
        city_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Оставить как в резюме")],
                [KeyboardButton(text="Изменить город")],
                [KeyboardButton(text="В главное меню")]
            ],
            resize_keyboard=True
        )
        
        await message.answer(
            "🛠 <b>Шаг 2 из 3:</b> Выбери город\n\n"
            f"📍 Твой город в резюме: <b>{data['resume_city']}</b>\n\n"
            "Хочешь оставить этот город или изменить?",
            reply_markup=city_keyboard,
            parse_mode="HTML"
        )
        await state.set_state(Form.waiting_for_city_confirmation)
    else:
        await message.answer(
            "Выбери города для поиска. Не рекомендуем выбирать только 'Удаленная работа' - таких вакансий мало.",
            reply_markup=get_cities_keyboard_auto(all_cities, str(message.from_user.id))
        )
        await state.set_state(Form.waiting_for_cities)


# Обработчик кнопки "Поиск вакансий"
@router.message(lambda message: message.text == "Поиск вакансий")
async def search_vacancies(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} начал поиск вакансий")
    await state.set_state(Form.category)
    await message.answer(
        "🔍 Давай подберем для тебя лучшие вакансии!\n"
        "Выбери категорию из списка:",
        reply_markup=categories_keyboard
        )
    
@router.message(lambda message: message.text == "Отписаться от рассылки вакансий")
async def otpiska(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} отписывается от всех вакансий")
    user_id = str(message.from_user.id)
    selected_subcategories[user_id] = set()
    
    await message.answer(
        "🔍 Вы успешно отписались от всех вакансий\n",
        reply_markup=main_keyboard
        )


@router.message(Form.category, lambda message: message.text in category_keywords.keys())
async def handle_category(message: Message, state: FSMContext):
    category = message.text
    user_id = str(message.from_user.id)
    
    await state.update_data(current_category=category)
    
    # Инициализируем пустой набор подкатегорий для пользователя, если еще нет
    if user_id not in selected_subcategories:
        selected_subcategories[user_id] = set()
    

    await message.answer(
        f"📌 Ты выбрал категорию: <b>{category}</b>\n\n"
        "Теперь укажи подкатегории (можно выбрать несколько):",
        reply_markup=get_subcategories_keyboard(category, user_id),
        parse_mode="HTML"
    )


# Функция для создания клавиатуры подкатегорий
def get_subcategories_keyboard(category: str, user_id: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    subcategories = category_keywords[category]["subcategories"].keys()
    
    # Добавляем кнопки подкатегорий (по 2 в ряд)
    for subcategory in subcategories:
        # Проверяем, выбрана ли подкатегория для этого пользователя
        is_selected = user_id in selected_subcategories and subcategory in selected_subcategories[user_id]
        text_button = f"✅ {subcategory}" if is_selected else subcategory
        builder.add(KeyboardButton(text=text_button))
    
    builder.adjust(2)
    
    # Добавляем кнопки управления
    builder.row(
        KeyboardButton(text="Назад в категории"),
        KeyboardButton(text="Готово")
    )
    
    return builder.as_markup(resize_keyboard=True)

# Обработчик выбора подкатегорий
@router.message(
    Form.category,
    lambda message: any(
        message.text.replace("✅ ", "") in subcats 
        for cat in category_keywords.values() 
        for subcats in cat["subcategories"].keys()
    )
)
async def handle_subcategory(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    subcategory = message.text.replace("✅ ", "") 
    
    # Инициализируем множество подкатегорий для пользователя, если еще нет
    if user_id not in selected_subcategories:
        selected_subcategories[user_id] = set()
    
    # Добавляем или удаляем подкатегорию
    if subcategory in selected_subcategories[user_id]:
        selected_subcategories[user_id].remove(subcategory)
        action = "❌ Убрано из выбора"
    else:
        selected_subcategories[user_id].add(subcategory)
        action = "✅ Добавлено к выбору"
    
    # Получаем текущую категорию для обновления клавиатуры
    data = await state.get_data()
    current_category = data.get('current_category')
    
    selected = "\n".join(selected_subcategories.get(user_id, ["Пока ничего не выбрано"]))

    
    await message.answer(
        f"{action}: <b>{subcategory}</b>\n\n"
        f"<b>Твой текущий выбор:</b>\n\n{selected}\n\n"
        "Можешь продолжить выбирать или нажать <b>«Готово»</b>",
        reply_markup=get_subcategories_keyboard(current_category, user_id),
        parse_mode="HTML"
    )


@router.message(Form.category, lambda message: message.text == "Готово")
async def handle_subcategories_done(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    
    if user_id not in selected_subcategories or not selected_subcategories[user_id]:
        await message.answer("⚠️ Ты не выбрал ни одной специализации.\n\n"
            "Пожалуйста, выбери хотя бы один вариант.")
        return
    
    selected = "\n".join(selected_subcategories[user_id])
   
    await message.answer(
        "📋 <b>Отлично! Твой выбор:</b>\n\n"
        f"{selected}\n\n"
        "Теперь укажи свой опыт работы:",
        reply_markup=get_experience_keyboard(user_id),  # Используем новую функцию
        parse_mode="HTML"
    )

    await state.set_state(Form.waiting_for_experience)


def get_experience_keyboard(user_id: str = None) -> ReplyKeyboardMarkup:
    """Создает клавиатуру выбора опыта с галочками для выбранных вариантов"""
    builder = ReplyKeyboardBuilder()
    
    # Варианты опыта
    experience_options = [
        "Нет опыта", 
        "От 1 года до 3 лет",
        "От 3 до 6 лет", 
        "Более 6 лет"
    ]
    
    # Добавляем кнопки с учетом выбранных вариантов
    for option in experience_options:
        if user_id and user_id in user_expierence and option in user_expierence[user_id]:
            text = f"✅ {option}"
        else:
            text = option
        builder.add(KeyboardButton(text=text))
    
    builder.adjust(2)
    
    # Добавляем кнопки управления
    builder.row(
        KeyboardButton(text="Назад в категории"),
        KeyboardButton(text="Готово")
    )
    
    return builder.as_markup(resize_keyboard=True)


@router.message(Form.waiting_for_experience)
async def handle_experience_selection(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    
    # Инициализируем множество для пользователя, если его нет
    if user_id not in user_expierence:
        user_expierence[user_id] = set()
    
    if message.text == "Назад в категории":
        await state.set_state(Form.category)
        await message.answer("Возвращаемся к выбору категорий", reply_markup=categories_keyboard)
        return
    
    if message.text == "Готово":
        if not user_expierence.get(user_id):
            await message.answer("⚠️ Ты не выбрал ни одного варианта опыта.\n\n"
                               "Пожалуйста, выбери хотя бы один вариант или нажми «Назад в категории».")
            return
            
        selected = "\n".join(f"• {exp}" for exp in user_expierence[user_id])
        await message.answer(
            "📋 <b>Отлично! Твой выбор опыта:</b>\n\n"
            f"{selected}\n\n"
            "Теперь укажи города для поиска:",
            reply_markup=get_cities_keyboard(all_cities, user_id),
            parse_mode="HTML"
        )
        await state.set_state(Form.waiting_for_cities)
        return
    
    # Обрабатываем выбор опыта (удаляем галочку если есть)
    exp = message.text.replace("✅ ", "").strip()
    
    # Добавляем или удаляем опыт
    if exp in user_expierence[user_id]:
        user_expierence[user_id].remove(exp)
        action = "❌ Убрано из выбора"
    else:
        user_expierence[user_id].add(exp)
        action = "✅ Добавлено к выбору"
    
    # Формируем текст с выбранными вариантами (с галочками)
    selected = "\n".join(f"✅ {exp}" for exp in user_expierence.get(user_id, []))
    if not selected:
        selected = "Пока ничего не выбрано"
    
    # Получаем обновленную клавиатуру с галочками
    updated_keyboard = get_experience_keyboard(user_id)
    
    await message.answer(
        f"{action}: <b>{exp}</b>\n\n"
        f"<b>Твой текущий выбор:</b>\n\n{selected}\n\n"
        "Можешь продолжить выбирать или нажать <b>«Готово»</b>",
        reply_markup=updated_keyboard,
        parse_mode="HTML"
    )
# Общий обработчик для кнопки "Назад в категории"
async def back_to_categories_common(message: Message, state: FSMContext):
    # Всегда переходим к выбору категорий
    await state.set_state(Form.category)
    await message.answer("Выберите категорию:", reply_markup=categories_keyboard)

# Обработчики для разных состояний
@router.message(Form.waiting_for_experience, lambda message: message.text == "Назад в категории")
async def back_to_categories_from_experience(message: Message, state: FSMContext):
    await back_to_categories_common(message, state)

# @router.message(Form.waiting_for_cities, lambda message: message.text == "Назад в категории")
# async def back_to_categories_from_cities(message: Message, state: FSMContext):
#     await back_to_categories_common(message, state)

@router.message(Form.waiting_for_cities, lambda message: message.text == "Назад в категории")
async def back_to_categories_from_cities(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    # Сохраняем выбранные города перед возвратом
    await state.update_data(selected_cities=selected_cities.get(user_id, set()))
    await back_to_categories_common(message, state)

@router.message(Form.category, lambda message: message.text == "Назад в категории")
async def back_to_categories_from_category(message: Message, state: FSMContext):
    await back_to_categories_common(message, state)
    
def get_cities_keyboard(all_cities,user_id: int = None) -> ReplyKeyboardMarkup:
    # builder = ReplyKeyboardBuilder()
    # builder.row(KeyboardButton(text="Назад в категории"))
    # builder.row(KeyboardButton(text="Начать поиск вакансий"))
    # builder.adjust(1)
    
    builder = ReplyKeyboardBuilder()
    
    # Кнопки управления
    builder.row(KeyboardButton(text="Назад в категории"))
    builder.row(KeyboardButton(text="Начать поиск вакансий"))
    
    # Добавляем кнопку "Удаленка" отдельной строкой
    remote_text = "✅ Удаленная работа" if (user_id and str(user_id) in selected_cities and "Удаленная работа" in selected_cities[str(user_id)]) else "Удаленная работа"

    builder.row(KeyboardButton(text=remote_text))
    
    # Полный список городов России (пример)
    all_cities_now = all_cities
    
    # Приоритетные города (должны быть в начале)
    priority_cities = ["Москва", "Санкт-Петербург", "Казань", "Новосибирск", "Екатеринбург", 'Красноярск', 
                       "Нижний Новгород", 'Челябинск', 'Уфа',
                       "Самара", "Ростов-на-Дону", 'Краснодар', "Омск", 'Воронеж', 'Пермь', 'Волгоград']
    

    sorted_cities = priority_cities # + sorted(

    for city in sorted_cities:
        if user_id and str(user_id) in selected_cities and city in selected_cities[str(user_id)]:
            text_button = f"✅ {city}"
        else:
            text_button = city
        builder.add(KeyboardButton(text=text_button))
    
    builder.adjust(2)
    
    # Добавляем кнопки управления

    return builder.as_markup(resize_keyboard=True)



@router.message(Form.waiting_for_cities, F.text, lambda message: message.text.replace("✅ ", "") in all_cities or message.text.replace("✅ ", "") == "Удаленная работа")
async def handle_city_selection(message: Message):
    user_id = str(message.from_user.id)
    city = message.text.replace("✅ ", "")  # Удаляем эмодзи если есть

   
    
    # Инициализируем множество для пользователя, если его нет
    if user_id not in selected_cities:
        selected_cities[user_id] = set()
    
    # Добавляем или удаляем город
    if city in selected_cities[user_id]:
        selected_cities[user_id].remove(city)
        action = "❌ Убрано из выбора"
    else:
        selected_cities[user_id].add(city)
        action = "✅ Добавлено к выбору"
    
    # Формируем список выбранных городов
    selected = "\n".join(selected_cities.get(user_id, ["Пока ничего не выбрано"]))

    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} выбрал {selected}")
    # Обновляем клавиатуру
    await message.answer(
        f"{action}: {city}\n\n"
        f"Текущий выбор:\n{selected}\n\n"
        "Продолжайте выбирать или нажмите «Начать поиск»",
        reply_markup=get_cities_keyboard(all_cities, user_id)
    )


@router.message(F.text == "Начать поиск вакансий")
async def handle_vacancy_search(message: Message, state: FSMContext, bot: Bot):
    user_id = str(message.from_user.id)
    
    # Проверяем, что пользователь выбрал города
    if not selected_cities.get(user_id):
        await message.answer(
            "⚠️ <b>Ой!</b>\n"
            "Ты не выбрал ни одного города для поиска.\n"
            "Пожалуйста, укажи хотя бы один город или выбери удаленную работу.\n",
            parse_mode="HTML", 
            reply_markup=get_cities_keyboard(all_cities, user_id)
        )
        return
    
    try:

        category = selected_subcategories[user_id]

        category_text =  "\n".join(f"• {category}" for category in selected_subcategories[user_id])
        
        # Формируем текст с выбранными городами
        cities_text = "\n".join(f"• {city}" for city in selected_cities[user_id])


        await message.answer(
            "🔍 <b>Начинаю поиск вакансий...</b>\n\n"
            f"<b>Категория:</b>\n{category_text}\n\n"
            # f"<b>Опыт работы:</b>\n{user_exp}\n\n"
            f"<b>Города:</b>\n{cities_text}\n\n"
            "Как только найду подходящие вакансии - сразу пришлю их тебе!\n\n"
            "⏳ <i>Внимание:</i> я не умею рассылать чаще, чем раз в 10 минут",
            parse_mode="HTML", 
            reply_markup=main_keyboard
        )
        
        await send_personalized_vacancies(bot)  
        logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} окончил настройку поиска вакансий")

    except:
         await message.answer(
            "😕 <b>Упс, что-то пошло не так</b>\n"
            "Попробуй начать поиск заново через меню."
            "Ошибка блин блинский\n",
            "Если меню не работает, отправь /start",
            parse_mode="HTML", reply_markup=main_keyboard
        )
         logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} столкнулся с ошибкой")
        
    
# Обработчик кнопки "В главное меню"
@router.message(lambda message: message.text == "В главное меню")
async def back_to_main(message: Message):
    user_id = message.from_user.id
    await message.answer("Возвращаемся в главное меню", reply_markup=main_keyboard)

@router.message(lambda message: message.text == "AI ассистент")
async def update_resume(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку AI ассистент")
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="🔥 Прожарка резюме на основе вакансий")],
            [KeyboardButton(text="🎯 Общая оценка резюме")],
            [KeyboardButton(text="В главное меню")]
        ]
    )

    await message.answer(
    text=(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я — твой AI помощник по карьере.\n\n"
        "✨ Я стараюсь быть максимально точным и опираюсь на реальные вакансии, "
        "но иногда могу ошибаться — если что-то покажется странным, "
        "сообщи пожалуйста по кнопке 'Помощь'!\n\n"
        "С чего начнём?"
    ),
    reply_markup=markup,
    parse_mode="HTML"
)



def escape_html(text):
    return markdown(text, extensions=['fenced_code'])


def clean_and_format(text: str) -> str:

    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  
    text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)
    text = text.replace("<think>", "").replace("</think>", "")
    return text




@router.message(lambda message: message.text == "🎯 Общая оценка резюме")
async def general_resume_review(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку Общая оценка резюме")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В главное меню")]],
        resize_keyboard=True
    )
    await message.answer(
        text="📌 Отлично! Пришлите резюме в формате PDF для комплексной оценки",
        reply_markup=keyboard
    )
    await state.set_state(ResumeAnalysisStates.waiting_for_resume_total)
    logger.info(f"Пользователь {message.from_user.id} начал общую оценку резюме")



# @router.message(F.document, ResumeAnalysisStates.waiting_for_resume_total)
# async def handle_general_resume(message: Message, state: FSMContext):
#     try:
#         if not message.document.file_name.lower().endswith('.pdf'):
#             await message.answer("❌ Файл должен быть в формате PDF!")
#             return

#         logger.info(f"Получен документ: {message.document.file_name}")
#         await message.answer("🔍 Анализирую резюме... Обычно это занимает 3-5 минут")

#         # Скачиваем и обрабатываем файл
#         file = await message.bot.download(message.document.file_id)
#         pdf_bytes = file.read()
        
#         # Извлекаем текст и сохраняем в state
#         extracted_text = extract_text_from_pdf(pdf_bytes)
#         if not extracted_text:
#             await message.answer("❌ Не удалось извлечь текст. Убедитесь, что файл не сканированный.")
#             await state.clear()
#             return
            
#         await state.update_data(resume_text=extracted_text)
#         await state.set_state(ResumeAnalysisStates.resume_text_stored)

#         # Вызываем hot_resume для общей оценки
#         analysis_result = await generating_answer_without_vacancy(extracted_text)  
#         formatted_result = clean_and_format(analysis_result)

#         logger.info(f"Пользователь {message.from_user.id} получил анализ {formatted_result}")
        
#         await message.answer(formatted_result, parse_mode="HTML")
#         await message.answer(
#             "✅ Анализ завершен. Буду рад если вы поделитесь фидбеком о моей работе через кнопку 'Помощь'",
#             reply_markup=ReplyKeyboardMarkup(
#                 keyboard=[
#                     [KeyboardButton(text="В главное меню")]
#                 ],
#                 resize_keyboard=True
#             )
#         )

#     except Exception as e:
#         logger.error(f"Ошибка при обработке резюме: {e}", exc_info=True)
#         await message.answer("⚠️ Произошла ошибка анализа. Попробуйте другой файл.",
#             reply_markup=ReplyKeyboardMarkup(
#                 keyboard=[
#                     [KeyboardButton(text="В главное меню")]
#                 ],
#                 resize_keyboard=True
#             )
#         )
#         await state.clear()


@router.message(F.document, ResumeAnalysisStates.waiting_for_resume_total)
async def handle_general_resume(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В главное меню")]],
        resize_keyboard=True
    )
    
    async def perform_analysis_with_retries():
        MAX_RETRIES = 3
        RETRY_DELAY = 2
        
        for attempt in range(MAX_RETRIES):
            try:
                # Проверка формата файла
                if not message.document.file_name.lower().endswith('.pdf'):
                    await message.answer("❌ Файл должен быть в формате PDF!", reply_markup=keyboard)
                    return None

                logger.info(f"Попытка {attempt + 1}/{MAX_RETRIES} для пользователя {message.from_user.id}")

                await message.answer(f"🔍 Анализирую резюме... Попытка {attempt + 1} из {MAX_RETRIES}")

                # Скачивание и обработка файла
                file = await message.bot.download(message.document.file_id)
                pdf_bytes = file.read()
                
                # Извлечение текста
                extracted_text = extract_text_from_pdf(pdf_bytes)
                if not extracted_text:
                    await message.answer("❌ Не удалось извлечь текст. Убедитесь, что файл не сканированный.", reply_markup=keyboard)
                    return None
                    
                await state.update_data(resume_text=extracted_text)
                await state.set_state(ResumeAnalysisStates.resume_text_stored)

                # Генерация анализа
                analysis_result = await generating_answer_without_vacancy(extracted_text)
                formatted_result = clean_and_format(analysis_result)

                # Попытка отправки результата
                try:
                    await message.answer(formatted_result, parse_mode="HTML")
                    await message.answer(
                        "✅ Анализ завершен. Буду рад если вы поделитесь фидбеком о моей работе через кнопку 'Помощь'",
                        reply_markup=keyboard
                    )
                    return True
                except Exception as send_error:
                    logger.error(f"Ошибка отправки (попытка {attempt + 1}): {send_error}")
                    if attempt < MAX_RETRIES - 1:
                        await asyncio.sleep(RETRY_DELAY)
                    continue

            except Exception as e:
                logger.error(f"Ошибка анализа (попытка {attempt + 1}): {e}")
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY)
                continue
        
        return False

    try:
        success = await perform_analysis_with_retries()
        
        if not success:
            logger.error(f"Все попытки анализа провалились для пользователя {message.from_user.id}")
            await message.answer(
                "😔 Не удалось проанализировать резюме после нескольких попыток. Пожалуйста:\n"
                '1. Проверьте, что файл в формате PDF\n'
                '2. Убедитесь, что файл не повреждён\n'
                '3. Попробуйте сократить объём текста в резюме\n'
                '4. Повторите попытку позже',
                reply_markup=keyboard
            )
            
    except Exception as e:
        logger.critical(f"Критическая ошибка обработчика: {e}")
        await message.answer(
            "⚠️ Произошла непредвиденная ошибка. Мы уже работаем над её устранением.",
            reply_markup=keyboard
        )
    finally:
        await state.clear()




@router.message(F.text, lambda message: message.text == "🔥 Прожарка резюме на основе вакансий")
async def start_resume_roast_from_existing(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку Прожарка резюме на основе вакансий")
    await state.set_state(ResumeAnalysisStates.waiting_for_category)
    await message.answer(
        "🔍 Выберите категорию вакансий для анализа резюме:",
        reply_markup=get_roast_categories_keyboard()
    )

def get_roast_categories_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔥 Аналитика"), KeyboardButton(text="🔥 Разработка")],
            [KeyboardButton(text="🔥 Тестирование"), KeyboardButton(text="🔥 ML/AI/DS")],
            [KeyboardButton(text="🔥 Менеджмент")],
            [KeyboardButton(text="В главное меню")]
        ],
        resize_keyboard=True

    )

@router.message(F.text, lambda message: message.text[2:] in category_keywords.keys())
async def handle_roast_category(message: Message, state: FSMContext):
    """🔥 Обработчик выбора категории для прожарки"""
    category = message.text[2:]
    await state.update_data(roast_category=category)
    await state.set_state(ResumeAnalysisStates.waiting_for_subcategory)
    
    await message.answer(
        f"🔥 Выберите <b>ОДНУ</b> специализацию в категории <b>{category}</b>:\n"
        "Нажмите на нужную подкатегорию ниже 👇",
        reply_markup=get_roast_subcategories_keyboard(category),
        parse_mode="HTML"
    )

def get_roast_subcategories_keyboard(category: str) -> ReplyKeyboardMarkup:
    """🔥 Клавиатура подкатегорий для прожарки"""
    builder = ReplyKeyboardBuilder()
    
    # Добавляем подкатегории с emoji
    for subcategory in category_keywords[category]["subcategories"].keys():
        builder.add(KeyboardButton(text=f"🔥 {subcategory}"))  
    
    builder.adjust(2)
    
    # Управляющие кнопки тоже с emoji
    builder.row(
        KeyboardButton(text="В главное меню")
    )
    
    return builder.as_markup(resize_keyboard=True)


hair_user = {}
@router.message(F.text, 
    ResumeAnalysisStates.waiting_for_subcategory,
    lambda message: any(
        message.text[2:] in subcats
        for cat in category_keywords.values()
        for subcats in cat["subcategories"].keys()
    )
)
async def handle_roast_subcategory_selection(message: Message, state: FSMContext):
    """🔥 Обработчик выбора подкатегории"""
    hair_user[message.from_user.id] = message.text[2:] 
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В главное меню")]],
        resize_keyboard=True
    )
    await message.answer(
        text="📌 Отлично! Пришлите резюме в формате PDF для комплексной оценки",
        reply_markup=keyboard
    )
    await state.set_state(ResumeAnalysisStates.waiting_for_resume_fair)
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} начал прожарку резюме")


@router.message(F.document, ResumeAnalysisStates.waiting_for_resume_fair)
async def handle_general_resume(message: Message, state: FSMContext, bot):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В главное меню")]],
        resize_keyboard=True
    )
    
    async def try_analyze(attempts=3):
        for attempt in range(attempts):
            try:
                if not message.document.file_name.lower().endswith('.pdf'):
                    await message.answer("❌ Файл должен быть в формате PDF!",
                        reply_markup=keyboard)
                    return None

                logger.info(f"Получен документ: {message.document.file_name} (попытка {attempt + 1})")
                await message.answer(f"🔍 Анализирую резюме... Попытка {attempt + 1} из {attempts}")

                # Скачиваем и обрабатываем файл
                file = await message.bot.download(message.document.file_id)
                pdf_bytes = file.read()
                
                # Извлекаем текст
                extracted_text = extract_text_from_pdf(pdf_bytes)

                # Пробуем получить анализ
                analysis_result = await hot_resume(extracted_text, hair_user[message.from_user.id])
                formatted_result = clean_and_format(analysis_result)
                
                # Пробуем отправить результат
                try:
                    await message.answer(
                        formatted_result,
                        parse_mode="HTML",
                        reply_markup=keyboard
                    )
                    return True  # Успех и анализ и отправка
                except Exception as send_error:
                    logger.error(f"Ошибка отправки результата (попытка {attempt + 1}): {str(send_error)}")
                    if attempt < attempts - 1:
                        await asyncio.sleep(2)
                    continue

            except Exception as e:
                logger.error(f"Ошибка анализа (попытка {attempt + 1}): {str(e)}")
                if attempt < attempts - 1:
                    await asyncio.sleep(2)
                continue
        
        return False  # Все попытки провалились

    try:
        success = await try_analyze()
        
        if not success:
            logger.error(f"Все попытки провалились для пользователя {message.from_user.id}")
            await message.answer(
                '😔 Не удалось проанализировать резюме после нескольких попыток. Пожалуйста:\n'
                '1. Проверьте, что файл в формате PDF\n'
                '2. Убедитесь, что файл не повреждён\n'
                '3. Попробуйте сократить объём текста в резюме\n'
                '4. Повторите попытку позже',
                parse_mode="HTML",
                reply_markup=keyboard
            )
            
    except Exception as e:
        logger.critical(f"Критическая ошибка обработчика: {str(e)}")
        await message.answer(
            '⚠️ Произошла непредвиденная ошибка. Мы уже работаем над её устранением.\n'
            'Пожалуйста, попробуйте отправить резюме ещё раз через несколько минут.',
            parse_mode="HTML",
            reply_markup=keyboard
        )
    


@router.message(F.text == "Опубликовать вакансию")
async def handle_vacancy_search(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал на кнопку Опубликовать вакансию")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В главное меню")]],
        resize_keyboard=True
    )
    
    await message.answer(
    "🌿 <b>Добрый день!</b>\n\n"
    "Мы рады, что вы решили разместить вакансию в нашем сервисе!\n\n"
    "📝 <b>Пожалуйста, напишите в чат с ботом следующую информацию:</b>\n\n"
    "• Наименование вакансии\n"
    "• Описание вакансии\n"
    "• Компания\n"
    "• Требуемые навыки\n"
    "• Опыт работы\n"
    "• Уровень зарплаты (по желанию)\n"
    "• Локация/удаленная работа\n"
    "• Ссылка на вакансию (если есть)\n\n"
    "💼 Наш менеджер рассмотрит вашу заявку и свяжется с вами в ближайшее время "
    "для уточнения деталей и публикации вакансии.\n\n"
    "<i>Благодарим за сотрудничество!</i>",
    parse_mode="HTML",
    reply_markup=keyboard
)


    await state.set_state(Form.waiting_for_description)

@router.message(Form.waiting_for_description)
async def process_vacancy_description(message: Message, state: FSMContext):
    if message.text == "В главное меню":
        await state.clear()
        await message.answer("Создание вакансии отменено", reply_markup=main_keyboard)
        return
    
    # Сохраняем данные (можно добавить в FSM storage)
    await state.update_data(vacancy_description=message.text)

    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} отправил текст вакансии")
    
    # Подтверждение получения
    await message.reply(
        "✅ <b>Вакансия получена!</b>\n\n"
        "Менеджер проверит информацию и свяжется с вами в течение 24 часов.\n"
        "Спасибо за доверие!",
        parse_mode="HTML",
        reply_markup=main_keyboard  # Убираем спец. клавиатуру
    )
    
    # Здесь можно добавить отправку уведомления менеджеру
    await forward_to_manager(message)
    
    await state.clear()

    
@router.message(Command("forward_vacancy"))  # Можно привязать к команде или другому фильтру
async def forward_to_manager(message: Message):
    MANAGER_CHAT_ID = -4959512272  # Замените на реальный ID чата/группы
    
    try:
        # 1. Пересылаем сообщение менеджеру
        forwarded_msg = await message.forward(
            chat_id=MANAGER_CHAT_ID
        )
        
        # 2. Отправляем поясняющее сообщение (привязанное к пересланному)
        await message.bot.send_message(
            chat_id=MANAGER_CHAT_ID,
            text=f"🚀 Новая вакансия от @{message.from_user.username}",
            reply_to_message_id=forwarded_msg.message_id  # Ответ именно на пересланное сообщение
        )
        
        # 3. Подтверждаем пользователю
        await message.reply("✅ Вакансия отправлена менеджеру!")
        logger.info(f"Вакансия отправлена в наш чат")
        
    except Exception as e:
        logger.info(f"Ошибка пересылки: {e}")
        await message.answer("⚠️ Не удалось отправить вакансию. Попробуйте позже.")
 

@router.message(F.text == "Помощь")
async def handle_trable(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку Помощь")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В главное меню")]],
        resize_keyboard=True
    )
    
    await message.answer(
    "🛎 <b>Служба поддержки</b>\n\n"
        "Расскажите, с какой проблемой вы столкнулись?\n"
        "Опишите её как можно подробнее, и мы обязательно поможем!\n\n",
    parse_mode="HTML",
    reply_markup=keyboard
    )


    await state.set_state(Form.waiting_for_trable)

@router.message(Form.waiting_for_trable)
async def process_vacancy_description(message: Message, state: FSMContext):
    if message.text == "В главное меню":
        await state.clear()
        await message.answer("✅ Запрос в поддержку отменен)", reply_markup=main_keyboard)
        return
    
    # Сохраняем данные (можно добавить в FSM storage)
    await state.update_data(trable=message.text)
    
    # Подтверждение получения
    await message.reply(
        "💌 <b>Спасибо за обращение!</b>\n\n"
        "Ваше сообщение получено и передано в поддержку.\n"
        "Мы ответим вам в ближайшее время.\n",
        parse_mode="HTML",
        reply_markup=main_keyboard  # Убираем спец. клавиатуру
    )

    await forward_to_manager_trable(message)
    
    await state.clear()

@router.message(Command("forward_to_manager_trable"))  # Можно привязать к команде или другому фильтру
async def forward_to_manager_trable(message: Message):
    MANAGER_CHAT_ID = -4959512272  # Замените на реальный ID чата/группы
    
    try:
        # 1. Пересылаем сообщение менеджеру
        forwarded_msg = await message.forward(
            chat_id=MANAGER_CHAT_ID
        )
        
            
           
        # 2. Отправляем поясняющее сообщение (привязанное к пересланному)
        await message.bot.send_message(
            chat_id=MANAGER_CHAT_ID,
            text= (f"🆘 <b>Новый запрос в поддержку</b>\n\n"
                 f"🚀 Проблема у @{message.from_user.username}"
                 f"🆔 <b>ID:</b> {message.from_user.id}\n"
                f"📅 <b>Время:</b> {message.date.strftime('%d.%m %H:%M')}\n\n"
             # Ответ именно на пересланное сообщение
            ),
            parse_mode="HTML",
            reply_to_message_id=forwarded_msg.message_id 
        )
        logger.info(f"Проблема отправлена в наш чат")
        # 3. Подтверждаем пользователю
        await message.reply("✅ Ваша проблема отправлена менеджеру!")
        
    except Exception as e:
        logger.info(f"Ошибка пересылки: {e}")
        await message.answer("Упс... что-то пошло не так.")
 




# Бд ниже

async def hourly_db_update(bot: Bot):
    """Ежечасное обновление БД"""
    global vacanciessss
    global hr_vacanciess
    while True:
        logger.info(f"[{datetime.now()}] Запуск обновления БД...")

        vacanciessss, hr_vacanciess = await load_and_cache_vacancies()
        logger.info(f"[{datetime.now()}] Вакансии загружены")
        await send_personalized_vacancies(bot)  
        logger.info(f"[{datetime.now()}] Рассылка отправлена")
        await asyncio.sleep(3600)  # 1 час
    

async def hourly_db_save(bot: Bot):
    """Ежечасное сохранение в БД"""
    global vacanciessss
    global hr_vacanciess
    while True:
        logger.info(f"[{datetime.now()}] Запуск сохранения БД...")
        await save_selected_subcategories()
        logger.info(f"[{datetime.now()}] Сохранение в БД завершено")
        await asyncio.sleep(3600)  # 1 час
        

async def start_background_tasks(bot: Bot):
    """Запуск фоновых задач при старте"""
    global selected_subcategories
    global selected_cities
    global all_cities
    global user_expierence

    loaded_data, all_cities, selected_cities, user_expierence = await load_selected_subcategories()
    # vacanciessss = await load_and_cache_vacancxies()
    selected_subcategories.update(loaded_data)
    logger.info(f"[{datetime.now()}] Загружено {len(loaded_data)} пользовательских выборов из БД")
    asyncio.create_task(hourly_db_update(bot))
    asyncio.create_task(hourly_db_save(bot))
    asyncio.create_task(cleanup_memory(bot))


async def cleanup_memory(bot: Bot):
    """Раз в 2 дня чистим кеш"""
    global last_send_time, send_vacancies
    while True:
        await asyncio.sleep(172800) 
        logger.info(f"[{datetime.now()}] Запуск очистки last_send_time, send_vacancies")
        try:
            now = datetime.now()
            last_send_time = {k: v for k, v in last_send_time.items() if now - v < timedelta(days=3)}
            send_vacancies = {k: v for k, v in send_vacancies.items() if now - v[-1]['date'] < timedelta(days=3)}
        except Exception as e:
            logger.info(f"[{datetime.now()}] Cleanup error: {e}")
   


async def save_selected_subcategories():
    if not selected_subcategories:
        return
    
    conn = None
    try:
        conn = await asyncpg.connect(
            host= host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        # Создаем копии словарей для безопасной итерации
        users_to_update = selected_subcategories.copy()
        cities_to_update = selected_cities.copy()
        exp_to_update = user_expierence.copy()

        async with conn.transaction():
            # Обновляем подкатегории
            for user_id, subcategories in users_to_update.items():
                await conn.execute(
                    "UPDATE users SET new_category = $1 WHERE user_id = $2",
                    json.dumps(list(subcategories), ensure_ascii=False),
                    str(user_id)
                )

            # Обновляем города
            for user_id, cities in cities_to_update.items():
                await conn.execute(
                    "UPDATE users SET cities = $1 WHERE user_id = $2",
                    json.dumps(list(cities), ensure_ascii=False),
                    str(user_id)
                )

            # Обновляем опыт
            for user_id, exp in exp_to_update.items():
                await conn.execute(
                    "UPDATE users SET experience = $1 WHERE user_id = $2",
                    json.dumps(list(exp), ensure_ascii=False),
                    str(user_id)
                )
        
        logger.info(f"[{datetime.now()}] Успешно сохранены данные для {len(users_to_update)} пользователей")

    
    except ValueError as e:  # Заменили json.JSONEncodeError
        logger.info(f"[{datetime.now()}] Ошибка кодирования JSON: {e}")
    except asyncpg.PostgresError as e:
        logger.info(f"[{datetime.now()}] Ошибка базы данных:  {e}")
    except Exception as e:
        logger.info(f"[{datetime.now()}] Неожиданная ошибка:  {e}")
    finally:
        if conn:
            await conn.close()



# При перезапуске
async def load_selected_subcategories() -> dict:
    """
    Загружает сохраненные подкатегории из базы данных
    Возвращает словарь в формате {user_id: set(subcategories)}
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
        
        # Загружаем данные из базы
        records = await conn.fetch(
            "SELECT user_id, new_category FROM users WHERE new_category IS NOT NULL"
        )
        city_list = await conn.fetch(
            "SELECT distinct location FROM vacans"
        )


        city_list = [record['location'] for record in city_list]
        city_list = [city for city in city_list if city is not None]

        city_for_users = await conn.fetch(
            "SELECT user_id, cities FROM users WHERE cities IS NOT NULL"
        )

        expierence_for_users = await conn.fetch(
            "SELECT user_id, experience FROM users WHERE experience IS NOT NULL"
        )


        # Формируем словарь selected_subcategories
        loaded_data = {}
        for record in records:
            try:
                if record['new_category']:
                    # Декодируем JSON и преобразуем список в set
                    loaded_data[record['user_id']] = set(json.loads(record['new_category']))
            except json.JSONDecodeError as e:
                logger.info(f"[{datetime.now()}] Ошибка декодирования для user_id {record['user_id']}: {e}")
                continue
        logger.info(f"[{datetime.now()}] Успешно загружено пользователей {len(loaded_data)} записей из БД")

        loaded_data_city = {}
        for record in city_for_users:
            try:
                if record['cities']:
                    # Декодируем JSON и преобразуем список в set
                    loaded_data_city[record['user_id']] = set(json.loads(record['cities']))
            except json.JSONDecodeError as e:
                logger.info(f"[{datetime.now()}] Ошибка декодирования для user_id {record['user_id']}: {e}")
                continue
        logger.info(f"[{datetime.now()}] Успешно загружено городов {len(loaded_data_city)} записей из БД")
        user_expierence = {}
        for record in expierence_for_users:
            try:
                if record['experience']:
                    # Декодируем JSON и преобразуем список в set
                    user_expierence[record['user_id']] = set(json.loads(record['experience']))
                    # user_expierence[record['user_id']] = set((record['experience']))
                    # user_expierence[record['user_id']] = record['experience']
            except Exception as e:
                logger.info(f"[{datetime.now()}] Ошибка декодирования для user_id {record['user_id']}: {e}")
                continue
        logger.info(f"[{datetime.now()}] Успешно загружено опыта {len(user_expierence)} записей из БД")    
        
        return loaded_data, city_list, loaded_data_city, user_expierence
        
    except Exception as e:
        logger.info(f"[{datetime.now()}] Ошибка при загрузке из БД: {e}") 
        return {}
    finally:
        if conn:
            await conn.close()



# Загрузка актуальных вакансий

async def load_and_cache_vacancies():
    """
    Загружает обычные и HR-вакансии из БД,
    возвращает кортеж (vacancies_cache, hr_vacancies_cache)
    """
    conn = None
    logger.info(f"[{datetime.now()}] Начали кешировать вакансии") 
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        # 1. Загрузка обычных вакансий
        records = await conn.fetch(
            "SELECT id, title, company, skills, location, experience, new_category, date, link "
            "FROM vacans WHERE date >= CURRENT_DATE - INTERVAL '3 day' AND (is_hr != TRUE or is_hr is Null)" 
        )
        
        # Кэшируем обычные вакансии
        vacancies = {
            str(record['id']): {
                'title': record['title'],
                'company': record['company'],
                'skills': record['skills'],
                'location': record['location'],
                'experience': record['experience'],
                'categories': record['new_category'].split("|")[1],
                'date': record['date'],
                'link': record['link'],
                'is_hr': False
            }
            for record in records
        }
        
        # 2. Загрузка HR-вакансий
        hr_records = await conn.fetch(
            "SELECT id, title, company, skills, location, description, date, link, contact, experience, new_category "
            "FROM vacans WHERE date >= CURRENT_DATE - INTERVAL '3 day' AND is_hr = TRUE"
        )
        
        # Кэшируем HR-вакансии
        hr_vacancies = {
            str(record['id']): {
                'title': record['title'],
                'company': record['company'],
                'skills': record['skills'],
                'location': record['location'],
                'experience': record['experience'],
                'categories': record['new_category'].split("|")[1],
                'description': record['description'],
                'date': record['date'],
                'link': record['link'],
                'is_hr': True,
                'contact': record['contact']
            }
            for record in hr_records
        }
        logger.info(f"[{datetime.now()}] Вакансии успешно закешированы (обычные: {len(vacancies)}, HR: {len(hr_vacancies)})") 
        return vacancies, hr_vacancies
        
    except Exception as e:
        logger.info(f"[{datetime.now()}] Ошибка загрузки данных: {e}") 
        return {}, {}
    finally:
        if conn:
            await conn.close()



from datetime import datetime, timedelta



# Глобальный словарь для хранения времени последней рассылки
last_send_time = {}
send_vacancies = {}
vacancy_counter = {}


async def send_vacancies_to_user(bot: Bot, user_id: int, vacancies: list):
    """Отправляет вакансии пользователю с возможной задержкой"""
    message = ""
    if len(vacancies) < 3:
        for i, vac in enumerate(vacancies, 1):
            message = (
                f"🏢 <b>Должность:</b> {vac['title']}\n"
                f"🏛 <b>Компания:</b> <i>{vac['company']}</i>\n\n"
                
                "📍 <b>Локация:</b> {location}\n"
                "📅 <b>Требуемый опыт:</b> {experience}\n\n"
                
                
                "🔗 <a href='{link}'>Посмотреть вакансию</a>\n"
                "──────────────────"
            ).format(
                location=vac.get('location', 'Не указано'),
                experience=vac.get('experience', 'Не указан'),
                link=vac['link']
            )
            await bot.send_message(
            chat_id=user_id,
            text="".join(message),
            parse_mode="HTML"
            )
    else:

        for i, vac in enumerate(vacancies, 1):

            message += (
                f"🏢 <b>Должность:</b> {vac['title']}\n"
                f"🏛 <b>Компания:</b> <i>{vac['company']}</i>\n\n"
                
                "📍 <b>Локация:</b> {location}\n"
                "📅 <b>Требуемый опыт:</b> {experience}\n\n"
                
                
                "🔗 <a href='{link}'>Посмотреть вакансию</a>\n"
                "──────────────────"
            ).format(
                location=vac.get('location', 'Не указано'),
                experience=vac.get('experience', 'Не указан'),
                link=vac['link']
            )

            # Если пользователь в списке для задержки и это каждая 3-я вакансия
            if i % 3 == 0:
                await bot.send_message(
                chat_id=user_id,
                text="".join(message),
                parse_mode="HTML"
                )
                message = ""
                logger.info(f"[{datetime.now()}] ⏳ Отправлено 3 вакансии, пауза 10 минут для пользователя {user_id}..") 
                await asyncio.sleep(2400)  # Задержка только для этого пользователя, было 600

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



async def send_hr_vacancies_to_user(bot: Bot, user_id: int, vacancies: list):
    """Отправляет HR-вакансии пользователю с возможной задержкой"""

    for i, vac in enumerate(vacancies, 1):
        # message = [
        #     "🔔 <b>Специальные HR-вакансии:</b>\n",
        #     f"✨ <b>{vac['title']}</b>\n",
        #     f"🏛 <i>{vac['company']}</i>\n\n",
        #     f"🌍 <b>Локация:</b> {vac['location']}\n",
        #     f"💼 <b>Навыки:</b> {vac['skills'][:150]}\n",
        #     f"📝 <b>Описание:</b> {vac['description'][:500]} ...\n\n",
        #     f"🔗 <b>Контакты для связи:</b> {vac['contact']}\n"
        # ]
        
        message = (
            "🌟 <b>Прямая вакансия от HR</b> 🌟\n"
            "══════════════════════\n"
            f"🎯 <b>Должность:</b> {vac['title']}\n"
            f"🏢 <b>Компания:</b> {vac['company']}\n"
            f"🌎 <b>Локация:</b> {vac.get('location', 'Не указана')}\n\n"
            
            "🔹 <b>Требуемые навыки:</b>\n"
            f"{(vac['skills'][:200])}\n\n"
            
            "📌 <b>Описание вакансии:</b>\n"
            f"{vac['description'][:600]}\n\n"
            
            "📞 <b>Контакты для отклика:</b>\n"
            f"   {vac['contact']}\n"

        )
        
        await bot.send_message(
            chat_id=user_id,
            text="".join(message),
            parse_mode="HTML"
        )
        await asyncio.sleep(1)

        print('Отправлена hr вакансия')
        
        if i % 3 == 0:
            logger.info(f"[{datetime.now()}] ⏳ Отправлено 3 HR-вакансии, пауза 10 минут для пользователя {user_id}..") 
            await asyncio.sleep(600)




async def send_personalized_vacancies(bot: Bot):
    """Рассылает только новые вакансии, появившиеся с последней проверки"""
    global vacancy_counter
    logger.info(f"[{datetime.now()}] Начало рассылки вакансий") 

    try:
        current_time = datetime.now()
        
        # 1. Фильтрация свежих вакансий
        fresh_vacancies = {}
        fresh_hr_vacancies = {}

        for vid, v in vacanciessss.items():
            try:
                try:
                    vacancy_date = datetime.strptime(str(v['date']), '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    vacancy_date = datetime.strptime(str(v['date']), '%Y-%m-%d %H:%M:%S')
                
                if vacancy_date >= current_time - timedelta(hours=24):
                    fresh_vacancies[vid] = v
            except Exception as e:
                logger.info(f"[{datetime.now()}] Ошибка парсинга даты для вакансии {vid}: {e}") 
                continue


        for vid, v in hr_vacanciess.items():
            try:
                try:
                    vacancy_date = datetime.strptime(str(v['date']), '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    vacancy_date = datetime.strptime(str(v['date']), '%Y-%m-%d %H:%M:%S')
                
                if vacancy_date >= current_time - timedelta(hours=24):
                    fresh_hr_vacancies[vid] = v
            except Exception as e:
                logger.info(f"[{datetime.now()}] Ошибка парсинга даты для вакансии {vid}: {e}") 
                continue
        
        

        if not fresh_vacancies and not fresh_hr_vacancies:
            logger.info(f"[{datetime.now()}]  Нет новых вакансий для рассылки") 
            return
            
        # 2. Создаем задачи для каждого пользователя
        tasks = []
        for user_id, user_categories in selected_subcategories.items():
            user_cities = selected_cities.get(user_id, set())
            
            # Фильтруем вакансии для пользователя
            # matched_vacancies = [
            # v for v in fresh_vacancies.values()
            # if (v.get('location') is not None and  # Проверяем, что location не None
            #     v['location'] in user_cities and
            #     any(cat in v['categories'] for cat in user_categories) and
            #     (v.get('experience') == user_expierence.get(user_id) or v.get('experience') == 'Не указано'))
            # ]

            matched_vacancies = [
                v for v in fresh_vacancies.values()
                if (v.get('location') is not None and
                v['location'] in user_cities and
                any(cat in v['categories'] for cat in user_categories) and
                (v.get('experience') in user_expierence.get(user_id, set()) or 
                v.get('experience') == 'Не указано'))
                ]

            matched_hr_vacancies = [
                v for v in fresh_hr_vacancies.values()
                if (v.get('location') is not None and  
                v['location'] in user_cities and
                any(cat in v['categories'] for cat in user_categories) and
                (v.get('experience') or user_expierence.get(user_id, set()) or v.get('experience') == 'Не указано'))
            ]
            

            # Исключаем уже отправленные
            previously_sent_links = {vac['link'] for vac in send_vacancies.get(user_id, [])}
            new_matched_vacancies = [vac for vac in matched_vacancies if vac['link'] not in previously_sent_links]

            new_matched_hr_vacancies = [vac for vac in matched_hr_vacancies if vac['link'] not in previously_sent_links]

            # Обновляем информацию об отправленных вакансиях
            
            if user_id in last_send_time:
                time_since_last_send = current_time - last_send_time[user_id]
                if time_since_last_send < timedelta(minutes=10):
                    logger.info(f"[{datetime.now()}] Пропускаем рассылку для {user_id} - не прошло 10 минут") 
                    continue
            

            if new_matched_hr_vacancies:
                task = asyncio.create_task(
                     send_hr_vacancies_to_user(bot, user_id, new_matched_hr_vacancies))
                tasks.append(task)

            if new_matched_vacancies:
                    # Запускаем асинхронную задачу отправки
                task = asyncio.create_task(
                    send_vacancies_to_user(bot, user_id, new_matched_vacancies)
                    )
                tasks.append(task)
                    
            

            if new_matched_vacancies or new_matched_hr_vacancies:
                if user_id not in send_vacancies:
                    send_vacancies[user_id] = []
                send_vacancies[user_id].extend(new_matched_vacancies + new_matched_hr_vacancies)
                last_send_time[user_id] = current_time

                
        # Ожидаем завершения всех задач
        await asyncio.gather(*tasks)
        
    except Exception as e:
        logger.info(f"[{datetime.now()}] Критическая ошибка в рассылке: {e}") 



