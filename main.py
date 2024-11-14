from domain.answer import answer_router
from domain.question import question_router
from domain.user import user_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# domain.나오면 .은 폴더를 의미 starleet 폴더의 middlewares의 폴더의 등등
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

origins = [
    "http://localhost:5173"
]
# fastapi가백엔드(가상에서 uvicorn.main:app --reload)
# svelte가 프론트엔드서버(npm run dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))
@app.get("/22")
def index():
    return FileResponse("frontend/dist/index.html")
