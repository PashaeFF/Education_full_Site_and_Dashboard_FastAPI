from fastapi import APIRouter, Request, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import desc
import models, database, paginate, time_calculate
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates
from configurations.token import verify_token

messages_panel = APIRouter(
    tags=['Dashboard / Messages'],
)

@messages_panel.get("/inbox")
def inbox(request: Request, db:Session = Depends(database.get_db), page: int = 1, page_size: int = 10):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            m_data = db.query(models.AdminMessages).order_by(models.AdminMessages.created_at.desc()).all()
            unread = db.query(models.AdminMessages).filter_by(readed=0).order_by(models.AdminMessages.created_at.desc()).all()
            data_length = len(m_data)
            messages = paginate.paginate(data=m_data, data_length=data_length,page=page, page_size=page_size)
            #mesajin gelme zamanini hesablayir
            messages_time = time_calculate.messages_time()
            ########## flash message
            _flash_message = ""
            if request.session.get("flash_messsage"):
                _flash_message = request.session.get("flash_messsage")
                request.session.pop("flash_messsage") if "flash_messsage" in request.session else []
            return templates.TemplateResponse("dashboard/messages.html",{"request":request, "m_data":m_data, "messages":messages, "flash":_flash_message,
                                                                            "unread":unread, "messages_time": messages_time, "user":user})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@messages_panel.get("/inbox/delete_all")
async def delete_all_messages(request: Request, response: Response, db: Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            messages_all = db.query(models.AdminMessages)
            print(messages_all)
            messages_all.delete()
            db.commit()
            request.session["flash_messsage"] = []
            request.session["flash_messsage"].append({"message": "Mesajlar silindi", "category": "success"})
            request = RedirectResponse(url="/admin/inbox", status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@messages_panel.get("/inbox/{id}")
def read_message(id: int, request: Request, db: Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            unread = db.query(models.AdminMessages).filter_by(readed=0).all()
            message = db.query(models.AdminMessages).filter_by(id=id).first()
            message_id = db.query(models.AdminMessages).filter_by(id=id)
            #mesajin gelme zamanini hesablayir
            messages_time = time_calculate.messages_time()
            #mesaj achilan kimi oxunmush kimi qeyd etmek uchun
            message_id.update({"readed":1})
            db.commit()
            return templates.TemplateResponse("dashboard/get_message.html",{"request":request,"message":message, "user":user,
                                                                            "unread":unread, "messages_time": messages_time})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
        

@messages_panel.get("/inbox/{id}/delete")
def delete_message(id: int, request: Request, db: Session = Depends(database.get_db)):
    ######## user_check #########
    access_token = request.cookies.get("access_token")
    current_user = verify_token(access_token)
    user = db.query(models.User).filter_by(id=current_user).first()
    #######     end    ##########
    if user:
        if user.admin_user == True or user.super_user == True:
            message = db.query(models.AdminMessages).filter_by(id=id)
            message.delete()
            db.commit()
            request.session["flash_messsage"] = []
            request.session["flash_messsage"].append({"message": "Mesajlar silindi", "category": "success"})
            request = RedirectResponse(url="/admin/inbox", status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)



