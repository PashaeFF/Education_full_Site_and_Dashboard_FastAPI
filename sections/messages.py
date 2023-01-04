from fastapi import APIRouter, Request, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import desc
import models, database, paginate, time_calculate
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, flash, get_flashed_messages
from datetime import datetime

messages_panel = APIRouter(
    tags=['Dashboard / Messages'],
)

@messages_panel.get("/inbox")
def inbox(request: Request, db:Session = Depends(database.get_db), page: int = 1, page_size: int = 10):
    m_data = db.query(models.AdminMessages).order_by(models.AdminMessages.created_at.desc()).all()
    unread = db.query(models.AdminMessages).filter_by(readed=0).order_by(models.AdminMessages.created_at.desc()).all()
    data_length = len(m_data)
    messages = paginate.paginate(data=m_data, data_length=data_length,page=page, page_size=page_size)

    #mesajin gelme zamanini hesablayir
    messages_time = time_calculate.messages_time()
    return templates.TemplateResponse("dashboard/messages.html",{"request":request, "m_data":m_data, "messages":messages,
                                                                    "unread":unread, "messages_time": messages_time})

@messages_panel.get("/inbox/{id}")
def read_message(id: int, request: Request, db: Session = Depends(database.get_db)):
    unread = db.query(models.AdminMessages).filter_by(readed=0).all()
    message = db.query(models.AdminMessages).filter_by(id=id).first()
    message_id = db.query(models.AdminMessages).filter_by(id=id)

    #mesajin gelme zamanini hesablayir
    messages_time = time_calculate.messages_time()

    #mesaj achilan kimi oxunmush kimi qeyd etmek uchun
    message_id.update({"readed":1})
    db.commit()
    return templates.TemplateResponse("dashboard/get_message.html",{"request":request,"message":message,
                                                                    "unread":unread, "messages_time": messages_time})

@messages_panel.get("/inbox/{id}/delete")
def delete_message(id: int, request: Request, db: Session = Depends(database.get_db)):
    message = db.query(models.AdminMessages).filter_by(id=id)
    message.delete()
    db.commit()
    flash(request,"Mesaj silindi", "success")
    return RedirectResponse(url="/admin/inbox",status_code=HTTP_303_SEE_OTHER)