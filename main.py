import uvicorn
from fastapi import FastAPI

from api.routers import groups, students

app = FastAPI()

app.include_router(groups.router)
app.include_router(students.router)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='127.0.0.1', reload=True)
