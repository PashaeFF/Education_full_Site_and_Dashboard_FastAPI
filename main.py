from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from routers import admin, site, register, user
from starlette.templating import Jinja2Templates
from fastapi_pagination import add_pagination
import models, database
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

middleware = [
 Middleware(SessionMiddleware, secret_key="super-secret")
]
app = FastAPI(middleware=middleware)

app.mount("/static/", StaticFiles(directory='static', html=True), name="static")

models.Base.metadata.create_all(database.engine)

add_pagination(app)

app.include_router(admin.dashboard)
app.include_router(site.main)
app.include_router(register.register)
app.include_router(user.user)