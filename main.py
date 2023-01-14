from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import admin, site, register, user, install
import models, database
from fastapi_sqlalchemy import DBSessionMiddleware, db
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse

middleware = [
 Middleware(SessionMiddleware, secret_key="super-secret")
]


app = FastAPI(middleware=middleware, docs_url=None, redoc_url=None)

app.add_middleware(DBSessionMiddleware, db_url=database.SQLALCHEMY_DATABASE_URL)


app.mount("/static/", StaticFiles(directory='static', html=True), name="static")

models.Base.metadata.create_all(database.engine)


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return RedirectResponse("/")

app.include_router(install.installer)
app.include_router(admin.dashboard)
app.include_router(site.main)
app.include_router(register.register)
app.include_router(user.user)