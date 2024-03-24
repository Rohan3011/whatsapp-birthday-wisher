from typing import Union
from fastapi import FastAPI
from fastapi_utilities import repeat_at
from birthday import check_for_birthdays

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


EVERY_MINUTE="* * * * *"
EVERY_DAY = "0 0 * * *"

@app.on_event("startup")
@repeat_at(cron=EVERY_DAY)
async def brithday_wishes():
    check_for_birthdays()

