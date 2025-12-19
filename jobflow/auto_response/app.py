import pandas as pd
from fastapi import FastAPI, UploadFile, File, WebSocket
from pydantic import BaseModel, Field

from typing import List
from fastapi.encoders import jsonable_encoder
import io
import numpy as np
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket, WebSocketDisconnect, Query
import json
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode, quote

from bd_send import *
import uvicorn


app = FastAPI()
CLIENT_ID = "G7D40HO7QR5FCQ78VQB1UKI95CNJMR2H2GM7VKIST1HFB8NB4SM36VG7T71O77M3"
CLIENT_SECRET = "ID3JTVQOJJA4HFQ7F7VAD88MQQRTD4DIRIS0TOIBANHRJKOH4QNDIKU9UMSPN0RR"
REDIRECT_URI = "https://redirect-maksim-arkhipov.amvera.io/code"


@app.post("/send_vacansy")
async def send_vacansy(vacancy_category, location, experience, access_token, resume_id): 
    try:
        result = await load_vacancies_for_send(vacancy_category, location, experience)
        count = 0
        print('вакансии загрузили')
        for i in result[0:15]:
            print(i['link'])
            try: 
                a = await send_vacanc(access_token, resume_id, i['link'].split('/')[-1])
                await asyncio.sleep(1) 
                print("Выполнили")
                count+=1
            except:
                print(i, 'error')
        
        update_res= await update_users_resume(resume_id,count, access_token, vacancy_category, location, experience)

      # Now it's a regular function call
        
        return {'send' : count}
    except Exception as e:
        print(f"Full error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    



@app.get("/get_vacanc")
async def get_item(vacancy_category, location, experience):
    try:
        print("Зашли")
        result = await load_vacancies_for_send(vacancy_category, location, experience)
        print(result)
        print("Выполнили")
        return result
    except Exception as e:
        print(f"Full error: {e}")  # Логируем полную ошибку
        raise HTTPException(status_code=400, detail=str(e))

async def get_access_token(auth_code, state):
    url = "https://hh.ru/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": auth_code
    }
    response = requests.post(url, data=data)
    response_data = response.json()
    response_data['state'] = state
    return response_data


@app.get("/code")
async def get_item(code, state):
    redirect_url = f"https://t.me/HrJobVacancy_Bot"
    try:
        print("зашлиии")
        a =  await get_access_token(code, state)
        b = await update_users(a['access_token'], a['refresh_token'], a['expires_in'], state)
        return RedirectResponse(redirect_url)
    except Exception as e:
        print(f"Full error: {e}")  # Логируем полную ошибку
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_resume")
async def get_resume(access_token):
    url = "https://api.hh.ru/resumes/mine"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return {'message': e}


@app.get("/get_access_token_from_bd")
async def get_access_token_in_bd(user_id):
    try:
        response = await get_access_token_from_bd(user_id)
        return response
    except Exception as e:
        return {'message': e}



@app.post("/generate_link")
async def predict_item(user_id): 

    STATE = user_id

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": STATE # Защита от CSRF
    }
    return f"https://hh.ru/oauth/authorize?{urlencode(params)}"


@app.get("/send_payment_link")
async def payment_link(user_id, payment_id):
    try:
        print("send_payment_link")
        a =  await update_users_premium(user_id, payment_id)
        return a
    except Exception as e:
        print(f"Full error: {e}")  # Логируем полную ошибку
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/get_payment_link")
async def get_payment(user_id):
    try:
        print("get_payment_link")
        a =  await get_user_premium(user_id)
        return a
    except Exception as e:
        print(f"Full error: {e}")  # Логируем полную ошибку
        raise HTTPException(status_code=400, detail=str(e))

from datetime import datetime

@app.get("/update_flag_prem")
async def update_flag_prem(user_id, premium_date):
    try:
        print("update_flag_prem")
        premium_date = datetime.strptime(premium_date, '%Y-%m-%d %H:%M:%S.%f')
        a =  await update_flag_premium(user_id, premium_date)
        return a
    except Exception as e:
        print(f"Full error: {e}")  # Логируем полную ошибку
        raise HTTPException(status_code=400, detail=str(e))
    



@app.get("/get_flag_prem")
async def get_flag_prem(user_id):
    try:
        print("get_flag_prem")
        a =  await get_flag_premium(user_id)
        return a
    except Exception as e:
        print(f"Full error: {e}")  # Логируем полную ошибку
        raise HTTPException(status_code=400, detail=str(e))
    


@app.post("/disable_auto")
async def disable_auto(user_id):
    try:
        print("disable_auto")
        a =  await disable_auto_for_user(user_id)
        return a
    except Exception as e:
        print(f"Full error: {e}")  # Логируем полную ошибку
        raise HTTPException(status_code=400, detail=str(e))
   

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или список ["http://localhost", "https://example.com"]
    allow_credentials=True,  # Разрешить куки (если нужно)
    allow_methods=["*"],     # Разрешить все методы (GET, POST, PUT и т. д.)
    allow_headers=["*"],     # Разрешить все заголовки
)


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, port=80, host="0.0.0.0", log_level="info")

# uvicorn app:app --reload --port 8000
# app - приложение FastAPI()
# main - название файла
