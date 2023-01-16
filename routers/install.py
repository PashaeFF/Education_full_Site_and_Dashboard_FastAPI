from fastapi import APIRouter, Request, Depends, Response
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.orm import Session
import configurations.models as models, configurations.database as database
from starlette.status import HTTP_303_SEE_OTHER, HTTP_201_CREATED
from utils.helper import templates
from utils.hashing import Hasher
from configurations.token import create_access_token

installer = APIRouter(
    prefix= ("/install")
)

@installer.get("/")
def installer_page(request: Request, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        return RedirectResponse("/")
    else:
        _flash_message = ""
        if request.session.get("flash_messsage"):
            _flash_message = request.session.get("flash_messsage")
            request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
        return templates.TemplateResponse("installation_page.html", {"request":request, "flash":_flash_message})

@installer.post("/")
async def post_installer_page(request: Request, response: Response, db: Session = Depends(database.get_db)):
    site_settings = db.query(models.SiteSettings).filter_by(id=1).first()
    if site_settings:
        return RedirectResponse("/")
    else:
        form = await request.form()
        email = form.get("email")
        password = form.get("password")
        site_url = form.get("site_url")
        site_title = form.get("site_title")
        site_logo = form.get("site_logo")
        site_slogan = form.get("site_slogan")
        request.session["flash_messsage"] = []
        if "@" not in email:
            request.session["flash_messsage"].append({"message": "Emaili düzgün qeyd edin", "category": "error"})
            request = RedirectResponse(url="/install",status_code=HTTP_303_SEE_OTHER)
            return request
        if len(password) < 8:
            request.session["flash_messsage"].append({"message": "Parol minimum 8 simvol olmalıdır", "category": "error"})
            response = RedirectResponse(url="/install",status_code=HTTP_303_SEE_OTHER)
            return response
        user = models.User(
            email=email,
            password=Hasher.get_hash_password(password),
            super_user=True
            )
        site = models.SiteSettings(site_url=site_url, site_title=site_title, site_logo=site_logo, site_slogan=site_slogan)
        db.add(user)
        db.add(site)
        db.commit()
        db.refresh(user)
        db.refresh(site)
        data = {
                "sub": email,
                "id": user.id,
            }
        request.session["flash_messsage"].append({"message": "Sayt istifadəyə hazırdır ;)", "category": "success"})
        response = RedirectResponse(url=f"/admin",status_code=HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=f"Bearer {create_access_token(data=data)}", httponly=True)
        return response