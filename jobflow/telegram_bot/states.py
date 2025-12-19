from aiogram.fsm.state import State, StatesGroup


class User:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self._categories = set()
        self._cities = set()

        

class Form(StatesGroup):
    user_id = State()
    category = State()
    resume = State()
    vacancy = State()
    vacancy_list = State()
    waiting_for_experience = State()
    waiting_for_cities = State()
    waiting_for_description = State() 
    waiting_for_trable = State() 
    auto = State()
    waiting_for_specialization = State()
    waiting_for_subspecialization = State()
    waiting_for_city_confirmation = State()
    waiting_for_experience_auto_response = State()
    waiting_for_cities_auto = State()
    

class ResumeAnalysisStates(StatesGroup):
    waiting_for_resume_total = State()
    waiting_for_category = State()
    waiting_for_subcategory = State()
    waiting_for_resume_file = State()
    resume_text_stored = State()  # Новое состояние для хранения текста
    waiting_for_resume_fair = State()
    category_fair = State()