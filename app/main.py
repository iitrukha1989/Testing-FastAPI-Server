##########################################
#
#   Основной модуль FastAPI приложения
#
##########################################

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.auth import router as auth_router
from app.routers.category import router as category_router
from app.routers.products import router as product_router
from app.routers.permission import router as permission_router
from app.routers.review import router as review_router

app = FastAPI(title="test project")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(permission_router)
app.include_router(review_router)
