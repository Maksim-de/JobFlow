import requests
from datetime import datetime, timedelta
import pytz
import bs4
import psycopg2
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


category_keywords = {
 "Аналитика": {
    "keywords": [
      "аналитик", 'systems_analyst', 'data_analyst', 'business_analyst', 'bi-аналитик', 'бизнес-аналитик', 'marketing_analyst',
      'bi_developer', 'bi-аналитик, аналитик данных', 'cистемный аналитик', 'soc_analyst', 'product_analyst'
    ],
    "subcategories": {
      "Системный аналитик": [
        "системн", "systems_analyst",  "uml", 'cистемный аналитик', 'системный', 'systems'
      ],
      "Бизнес аналитик": [
        "бизнес", "business", 'бизнес-аналитик', 'business_analyst'
      ],
      "Data аналитик и BI": [
        'data_analyst', 'bi-аналитик', "bi_developer", 'bi-аналитик, аналитик данных'
      ],
      "Продуктовый аналитик": [
        "продуктов", "product", "a/b", "ab test", "a/b test", 'продуктовый аналитик', 'product_analyst'
      ],
      "Аналитик DWH": [
        "data engineer", "dwh", "data warehouse", "airflow", "data lake",
        "databricks", "spark", "hadoop", 'sql'
      ],
      "Веб-аналитик": [
        "веб", "web",
      ],
      "Аналитик (Другое)": []
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
      "fullstack", "full-stack", "full stack", "devops-инженер", 'database_architect', 'database_admin', 'баз данных', 'разработка'
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
        "котлин", "kotlin", "swift", "mobileapp_developer", 'мобильная'
      ],
      "DevOps": [
        "devops", "DevOps-инженер"
      ],
      "Data engineer": [
        "data_engineer", 'database_developer', 'database_architect', 'database_admin', 'баз данных'
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
      'project_director', 'product_manager', 'marketing_manager', 'account_manager', 'cio', 'технический директор (сто)', 'cto'
    ],

    "subcategories": {
      "Продуктовый менеджмент": [
        "продуктов менеджер", "product manager", "PM", "product owner",
        "руководитель продукт", "head of product", 'product_manager', 'менеджер продукта'
      ],
      "Проектный менеджмент": [
        "проектн менеджер", "project manager", "PM", "руководитель проектов", 'project_manager', 'scrum_master', 'account_manager'
      ],
      "ИТ топ менеджмент": [
        'руководитель группы разработки',  'руководитель отдела аналитики', 'технический директор (сто)',  'project_director', 'cio', 'технический', 'cto'
      ],

"Менеджмент (Другое)": []
 }
    }
}

category_keywords_work = {

    "Аналитика": {
        "keywords": ['product_analyst', "аналитик", "бизнес аналитик" "analyst", "аналитик данных", "data analyst", "бизнес-аналитик", "business analyst", "BI-аналитик", "BI analyst", "системный аналитик", "system analyst", "веб-аналитик", "web analyst"],
        "subcategories": {
            "Системный аналитик": ["системный", "system analyst", 'cистемный аналитик', 'systems', 'systems analyst', 'ystem'],
            "Бизнес аналитик": ["бизнес-аналитик", "business analyst", "аналитик процессов", "process analyst", "full stack", "бизнес"],
            "Data аналитик и BI": ["аналитик данных", "data", "данных", "bi", "аналитик отчетности", "data analytics specialist"],
            "Продуктовый аналитик": ["продуктовый аналитик", "product analyst", "продуктовый", 'product_analyst'],
            "Веб-аналитик": ["веб-аналитик", "web analyst", "google analytics analyst", "аналитик метрик", "аналитик трафика"],
            "Аналитик DWH": ["data engineer", "dwh", "data warehouse", "airflow", "data lake", "databricks", "spark", "hadoop", 'sql'],
            "Аналитик (Другое)": []
}
    },
    "Разработка": {
        "keywords": ["разработчик", "developer", "программист", "engineer", "dev", "software", "приложений", "application", "код", "code"],
        "subcategories": {
            "Frontend разработка": ["frontend", "front-end", "front end", "javascript", "js", "react", "angular", "vue", "typescript", "ui developer"],
            "Backend разработка": ["backend", "back-end", "back end", "server", "api", "python", "java", "php", "node", "nodejs", "net", ".net", "go", "golang"],
            "Fullstack разработка": ["fullstack", "full-stack", "full stack", "универсальный разработчик","full", "mean", "lamp"],
            "Мобильная разработка": ["mobile", "android", "ios", "flutter", "react", "котлин", "kotlin", "swift", "mobileapp_developer"],
            "DevOps": ["devops", "DevOps-инженер"],
            "Разработка (Другое)": []
}
},
     "Тестирование": {
        "keywords": ["тестировщик", "tester", "qa", "quality assurance", "manual_testing", "тест", "test", "qa engineer", "инженер по тестированию"],
        "subcategories": {
            "Ручное тестирование": ["ручной тестировщик", "manual tester", "qa manual", "тестировщик ручного тестирования", "manual qa engineer", 'manual_testing'],
            "Автоматизированное тестирование": ['test_automation', 'qa', "автоматизатор тестирования", "automation tester", "qa automation", "инженер по автоматизации тестирования", "automation qa engineer"],
            "Тестирование (Другое)": []
}
},
     "ML/AI/DS": {
        "keywords": ["ml", "ai", 'ds', "data science", "дата-сайентист", 'data'],
         "subcategories": {
            "Data Science": ["data science", "анализ данн", "дата-сайентист", "data_scientist", 'дата-сайентист', 'ds', 'дата', 'data'],
            "ML Engineering": ["engineer", "ml-engineer", "mlops", "model serving"],
       "AI (Другое)": []
}
},
 "Менеджмент": {
    "keywords": [
      'менеджер продукта', 'менеджер' 'руководитель группы разработки', 'руководитель отдела аналитики', "руководитель проектов", 'project_manager',
      'project_director', 'product_manager', 'marketing_manager', 'account_manager', 'cio', 'технический директор (сто)', 'cto'
    ],

    "subcategories": {
      "Продуктовый менеджмент": [
        "продуктов менеджер", "product manager", "PM", "product owner",
        "руководитель продукт", "head of product", 'product_manager', 'продукт','менеджер продукта'
      ],
      "Проектный менеджмент": [
        "проектн менеджер", "project manager", "PM", "руководитель проектов", 'project_manager', 'scrum_master', 'account_manager'
      ],
      "ИТ топ менеджмент": [
        'руководитель группы разработки',  'руководитель отдела аналитики', 'технический директор (сто)',  'project_director', 'cio', 'технический', 'cto'
      ],

"Менеджмент (Другое)": []
 }
    }
}


# Парсим с hh и хабра и грузим в базу данных

import requests
from datetime import datetime, timedelta
import pytz
from bs4 import BeautifulSoup
import json
import re



def hh_parsing():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    date_from = yesterday.strftime("%Y-%m-%dT00:00:00")
    date_to = today.strftime("%Y-%m-%dT23:59:59")

    a_list_link = ['1']

    # Разбиваем роли на 3 логические группы для балансировки нагрузки
    role_groups = [
        ['156', '148', '160', '10',  '150', '165'],  # IT и управление
        ['36', '73', '96', '164', '104', '157' ],  # Маркетинг и продажи
        [  '107', '124', '125'] #,  # Другие специалисты
        # ['12', '25', '34', '155', '112','113', '114', '116', '121', '126']
    ]
    
    priority_cities = ["Москва", "Санкт-Петербург", "Казань", "Новосибирск", "Екатеринбург", 'Красноярск', 
                       "Нижний Новгород", 'Челябинск', 'Уфа',
                       "Самара", "Ростов-на-Дону", 'Краснодар', "Омск", 'Воронеж', 'Пермь', 'Волгоград']


    all_vacancies = []
    
    for group in role_groups:
        page = 0
        while True:
            params = {
                'professional_role': group,
                'date_from': date_from,
                'date_to': date_to,
                'per_page': 25,
                'page': page
            }
            
            try:
                response = requests.get("https://api.hh.ru/vacancies", params=params)
                response.raise_for_status()
                data = response.json()
                
                if not data['items']:
                    break
                    
                for item in data['items']:
                    if (item['area']['name'] in priority_cities) and (item['alternate_url'] not in a_list_link) and ('1С' not in item['name']) and ('1C' not in item['name']):
                      vacancy = {
                          "title": item['name'],
                          "company": item['employer']['name'],
                          "date": item['published_at'],
                          "location": item['area']['name'],
                          "employment": item['employment']['name'],
                          "experience": item['experience']['name'],
                          "salary": item.get('salary'),
                          "skills": item['snippet']['requirement'],
                          "link": item['alternate_url'],
                          'source': 'hh',
                          'vacancy_type': item['professional_roles'][0]['name'],
                          'new_category': classify_vacancy(item['professional_roles'][0]['name'], item['name'])
                      }
                      all_vacancies.append(vacancy)
                      a_list_link.append(item['alternate_url'])
                
                # print(f"Группа {group[:3]}..., Страница {page}: {len(data['items'])} вакансий")
                page += 1
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Ошибка: {str(e)}")
                break
    
    return all_vacancies

def safe_find_text(element, selector, **kwargs):
    found = element.find(selector, **kwargs) if element else None
    return found.text.strip() if found else None


def classify_vacancy(vacancy_type, title):
    a_list = ['Аналитика', 'Тестирование', 'Разработка', 'ML/AI/DS', 'Менеджмент']
    vacancy_type = vacancy_type.lower()
    title = title.lower()
    
    # Сначала проверяем по заголовку, если тип вакансии подходящий
    if vacancy_type in ['аналитик', 'программист, разработчик', 'тестировщик', 'аналитика', 'разработка, программирование', 'системный аналитик', 'дата-сайентист']:
        # Проверяем категории по заголовку
        for category in a_list:
            for keyword in category_keywords_work[category]['keywords']:
                if keyword in title:
                    # Теперь проверяем подкатегории
                    for subcategory in category_keywords_work[category]['subcategories']:
                        for sub_keyword in category_keywords_work[category]['subcategories'][subcategory]:
                            if sub_keyword in title:
                                return f"{category} | {subcategory}"
                    # Если подкатегория не найдена
                    return f"{category} | {category} (Другое)"
    
    # Если тип вакансии не подошел, проверяем по vacancy_type
    for category in a_list:
        for keyword in category_keywords[category]['keywords']:
            if keyword in vacancy_type:
                # Проверяем подкатегории
                for subcategory in category_keywords[category]['subcategories']:
                    for sub_keyword in category_keywords[category]['subcategories'][subcategory]:
                        if sub_keyword in vacancy_type:
                            return f"{category} | {subcategory}"
                # Если подкатегория не найдена
                return f"{category} | {category} (Другое)"
    
    # Если ничего не найдено
    return "Не определено | Не определено"


def get_vacancy_categories(element):
    """Извлекает категории вакансий из ссылок /vacancies/spec/"""
    categories = []
    if element:
        spec_links = element.find_all('a', href=lambda x: x and '/vacancies/spec/' in x)
        for link in spec_links:
            # Извлекаем последнюю часть пути как название категории
            category = link['href'].split('/')[-1]
            categories.append(category)
    return ', '.join(categories) if categories else ''



def get_vacancy_level(element):
    """Извлекает уровень вакансии из текста рядом с /vacancies?qid"""
    if element:
        level_link = element.find('a', href=lambda x: x and '/vacancies?qid=' in x)
        if level_link:
            return level_link.text.strip()
    return None




def superjob_parsing():
    a_list = []
    pages_to_check = 5

    headers = {
        "X-Api-App-Id": "v3.r.139164433.23ffc5190afedc15a75557bfecf0d17712201794.e87743a3f683bb304e7389b40f1fc40b4a1cbefa"
    }

    # Ключи нужных подкатегорий: аналитика, разработка, тестирование, ML/AI/DS, менеджмент

    target_keys = {627, 628, 36, 37, 38, 503, 42, 604, 650, 47,48, 50,56, 613, 605, 630, 61}
    priority_cities = ["Москва", "Санкт-Петербург", "Казань", "Новосибирск", "Екатеринбург", 'Красноярск', 
                       "Нижний Новгород", 'Челябинск', 'Уфа',
                       "Самара", "Ростов-на-Дону", 'Краснодар', "Омск", 'Воронеж', 'Пермь', 'Волгоград']

    for page in range(pages_to_check):
        params = {
            "page": page,
            "count": 100,
            "catalogues": 33  # IT-вакансии
        }

        response = requests.get("https://api.superjob.ru/2.0/vacancies/", headers=headers, params=params)

        if response.status_code != 200:
            print("Ошибка запроса:", response.status_code)
            continue

        vacancies = response.json().get("objects", [])
        today = datetime.now()  # Теперь это datetime, а не date
        
    

        for vac in vacancies:
            
            pub_date = datetime.fromtimestamp(vac.get("date_published", 0))
            # Пропускаем вакансии старше 1 суток
            if today - pub_date > timedelta(days=1):
                continue

            # 🔽 Фильтрация по подкатегориям (positions.key)
            subcatalog_keys = {
                pos.get("key")
                for cat in vac.get("catalogues", [])
                for pos in cat.get("positions", [])
            }
            if not subcatalog_keys & target_keys:
                continue  # пропускаем, если ни одна подкатегория не совпадает

            # Обработка опыта
            experience_raw = vac.get("experience", {}).get("title", "").lower()
            if "без опыта" in experience_raw:
                experience = "Нет опыта"
            elif "1 год" in experience_raw:
                experience = "От 1 года до 3 лет"
            elif "3 лет" in experience_raw:
                experience = "От 3 до 6 лет"
            elif "6 лет" in experience_raw:
                experience = "Более 6 лет"
            else:
                experience = "Не указано"

            # Категории
            # categories = [pos["title"] for cat in vac.get("catalogues", []) for pos in cat.get("positions", [])]

            categories = vac.get('catalogues')[0]['positions'][0]['key']
            city = vac.get("town", {}).get("title", "Не указано")
            classify = vac.get('catalogues')[0]['positions'][0]['title']

            if (categories in target_keys) and  (city in priority_cities):

              vacancy_data = {
                  "title": vac.get("profession", "Не указано"),
                  "company": vac.get("firm_name", "Не указано"),
                  "date": pub_date.strftime('%Y-%m-%d %H:%M:%S'),
                  "location": city,
                  "source": "superJob",
                  "employment": vac.get("type_of_work", {}).get("title", "Не указано"),
                  "salary": f"{vac.get('payment_from', 0)} - {vac.get('payment_to', 0)} {vac.get('currency', '').upper()}",
                  "skills": vac.get("candidat", ""),
                  "link": vac.get("link"),
                  "new_category": classify_vacancy(classify, vac.get("profession", "Не указано")),
                  "vacancy_type": classify,
                  "experience": experience
              }

              a_list.append(vacancy_data)

        time.sleep(1)

    return a_list


def habr_parsing():
    a_list = []
    num_list = 25

    for j in range(num_list):
        j+=1
        data = requests.get(f'https://career.habr.com/vacancies?page={j}&type=all')
        soup = BeautifulSoup(data.content, 'html.parser')
        vacancy = soup.find_all('div', class_='vacancy-card')
        for i in vacancy:
            time_vac = safe_find_text(i, 'time', class_='basic-date')
            time_vac = parse_russian_date(time_vac)
            if datetime.now() - time_vac < timedelta(days=1):
                experience = get_vacancy_level(i)
                if experience is None:
                    experience = 'Не указано'
                elif (experience == 'Старший (Senior)') or (experience == 'Ведущий (Lead)') :
                    experience = "От 3 до 6 лет"
                elif experience == 'Стажёр (Intern)':
                    experience = "Нет опыта"
                elif (experience == 'Средний (Middle)') or (experience == 'Младший (Junior)'):
                    experience = "От 1 года до 3 лет"
                
                location = safe_find_text(i, 'a', href=lambda x: x and 'city_id=' in x)

                if location is None:
                    location = 'Удаленная работа'
                vacancy_list = {
                "title": safe_find_text(i, 'a', class_='vacancy-card__title-link'),
                "company": safe_find_text(i, 'a', class_='link-comp', href=lambda x: x and '/companies/' in x),
                "date": datetime.now(),
                "location": location,
                'source' : 'habr',
                "employment": safe_find_text(i, 'span', class_='preserve-line', string=lambda x: x and 'Полный рабочий день' in x),
                "salary": safe_find_text(i, 'div', class_='basic-salary'),
                "skills": ', '.join([skill.text for skill in i.find_all('a', class_='link-comp', href=lambda x: x and '/skills/' in x)]) if i.find_all('a', class_='link-comp', href=lambda x: x and '/skills/' in x) else '',
                "link": "https://career.habr.com" + i.find('a', class_='vacancy-card__title-link')['href'] 
                    if i.find('a', class_='vacancy-card__title-link') else None,
                "new_category" : classify_vacancy(get_vacancy_categories(i), safe_find_text(i, 'a', class_='vacancy-card__title-link')),
                "vacancy_type": get_vacancy_categories(i),  # Добавленные категории из /vacancies/spec/
                "experience": experience
                }

                a_list.append(vacancy_list)
            else:
                break
        time.sleep(1)
    return a_list

def parse_date(date_str):
    """Парсит дату из строки в формате '2025-06-25T13:02:24+0300'"""
    try:
    # Удаляем временную зону (+0300) для упрощения (можно сохранить отдельно если нужно)
        if isinstance(date_str, str) and 'T' in date_str:
            return datetime.strptime(date_str.split('+')[0], '%Y-%m-%dT%H:%M:%S')
        return date_str
    except Exception as e:
        print(f"Ошибка парсинга даты {date_str}: {e}")
    return None # или datetime.now() для подстановки текущей даты

def parse_russian_date(date_str):
    month_map = {
        'января': 1, 'февраля': 2, 'марта': 3,
        'апреля': 4, 'мая': 5, 'июня': 6,
        'июля': 7, 'августа': 8, 'сентября': 9,
        'октября': 10, 'ноября': 11, 'декабря': 12
    }
    
    # Извлекаем день и месяц
    match = re.match(r'(\d{1,2})\s+([а-я]+)', date_str.lower())
    if not match:
        return None
    
    day = int(match.group(1))
    month_ru = match.group(2)
    month = month_map.get(month_ru)
    
    if not month:
        return None
    
    # Берем текущий год (можно задать явно если нужно)
    year = datetime.now().year
    
    return datetime(year=year, month=month, day=day)

def loading_to_base(hh_list, habr_list, superjob_list):
    conn = psycopg2.connect(
        host="pg4.sweb.ru",
        port=5433,
        database="maksimarkh",
        user="maksimarkh",
        password="Maksim1232145!"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT distinct link FROM vacans")
    link_records = cursor.fetchall()
    link_list = [record[0] for record in link_records if record[0] is not None]

    cursor.execute("SELECT distinct link FROM vacans where date > CURRENT_DATE")
    link_records = cursor.fetchall()
    link_list_now = [record[0] for record in link_records if record[0] is not None]

    

    for i in habr_list:
        if i['link'] not in link_list_now:
            
            cursor.execute("""
                INSERT INTO vacans (title, company, date, employment, salary, skills, link, location, source, new_category, vacancy_type, experience) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,  %s,  %s, %s, %s)
            """, (
                i['title'], 
                i['company'], 
                i['date'], 
                i['employment'], 
                i['salary'], 
                i['skills'], 
                i['link'],
                i['location'],
                i['source'],
                i['new_category'],
                i['vacancy_type'],
                i['experience']
                
            ))

    for i in hh_list:
        if i['link'] not in link_list:
            date_value = parse_date(i['date'])

            cursor.execute("""
            INSERT INTO vacans (title, company, date, employment, salary, skills, link, location, source, vacancy_type, experience, new_category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            i['title'],
            i['company'],
            date_value,
            i['employment'],
            str(i['salary']),
            i['skills'],
            i['link'],
            i['location'],
            i['source'],
            i['vacancy_type'],
            i['experience'],
            i['new_category']

            ))

    for i in superjob_list:
        if i['link'] not in link_list:
            date_value = parse_date(i['date'])

            cursor.execute("""
            INSERT INTO vacans (title, company, date, employment, salary, skills, link, location, source, vacancy_type, experience, new_category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            i['title'],
            i['company'],
            date_value,
            i['employment'],
            str(i['salary']),
            i['skills'],
            i['link'],
            i['location'],
            i['source'],
            i['vacancy_type'],
            i['experience'],
            i['new_category']

            ))
    conn.commit()
    cursor.close()
    conn.close()


def main():
    try:
        logger.info("Запуск парсера...")
        hh_list = hh_parsing()
        logger.info("HH загрузило...")
        habr_list = habr_parsing()
        logger.info("Habr загрузило...")
        superjob_list = superjob_parsing()
        logger.info("Superjob загрузило...")

    
        
        if hh_list or habr_list or superjob_list:
            logger.info("Начало загрузки в базу данных")
            loading_to_base(hh_list, habr_list, superjob_list)
            
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)

if __name__ == "__main__":
    main()
