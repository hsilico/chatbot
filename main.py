from fastapi import FastAPI
import requests
from datetime import datetime, timedelta

app = FastAPI()

def meal(mealcode, i):
    meal = {1: '조식', 2: '중식', 3: '석식'}.get(mealcode, '')
    schYmd = (datetime.now() + timedelta(days=i)).strftime('%Y%m%d')
    schYmd1 = (datetime.now() + timedelta(days=i)).strftime('%Y.%m.%d')
    day = (datetime.now() + timedelta(days=i)).weekday()
    yoil = ["일", "월", "화", "수", "목", "금", "토"]

    url = f'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=e77c8447cce64754b960a4c73244dcd1&Type=json&pIndex=1&pSize=10&ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7010115&MLSV_YMD={schYmd}'
    response = requests.get(url)
    text = response.text

    if meal in text:
        explode1 = text.split('"DDISH_NM":"')[1]
        meal1 = explode1.split('","ORPLC_INFO"')[0].replace('<br/>', '\n')
        return f'{schYmd1} ({yoil[day]}) {meal}\n{meal1}'
    else:
        return f'{schYmd1} ({yoil[day]}) {meal}\n급식이 없습니다.'

@app.get("/mealToday")
async def meal_today():
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {"title": "오늘 조식", "description": meal(1, 0)},
                            {"title": "오늘 중식", "description": meal(2, 0)},
                            {"title": "오늘 석식", "description": meal(3, 0)}
                        ]
                    }
                }
            ]
        }
    }

@app.get("/mealTomorrow")
async def meal_tomorrow():
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {"title": "내일 조식", "description": meal(1, 1)},
                            {"title": "내일 중식", "description": meal(2, 1)},
                            {"title": "내일 석식", "description": meal(3, 1)}
                        ]
                    }
                }
            ]
        }
    }
