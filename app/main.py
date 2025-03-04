##########################################
#
#   Основной модуль FastAPI приложения
#
##########################################

from fastapi import FastAPI

from app.auth import router as auth_router
from app.routers.category import router as category_router
from app.routers.products import router as product_router
from app.routers.permission import router as permission_router
from app.routers.review import router as review_router

app = FastAPI(title="test project")

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(permission_router)
app.include_router(review_router)
