from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from configurations import models, database
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utils.helper import templates, check_user, default_variables
from utils import paginate


messages_panel = APIRouter(
    tags=['Dashboard / Messages'],
)

@messages_panel.get("/inbox")
def inbox(request: Request, page: int = 1, page_size: int = 10):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            variables = default_variables(request)
            page_title = 'Admin mesajları'
            messages = paginate.paginate(data=variables['messages_data'], data_length=len(variables['messages_data']),page=page, page_size=page_size)
            return templates.TemplateResponse("dashboard/messages.html",{"request":request, "m_data":variables['messages_data'], "messages":messages, "flash":variables['_flash_message'],
                                                                            "unread":variables['unread_messages_data'], "messages_time": variables['messages_time'], "user":check['user'],
                                                                            "page_title":page_title})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@messages_panel.get("/inbox/delete_all")
async def delete_all_messages(request: Request, db: Session = Depends(database.get_db)):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            messages_all = db.query(models.AdminMessages)
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
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            variables = default_variables(request)
            page_title = 'Admin mesajları'
            message = db.query(models.AdminMessages).filter_by(id=id).first()
            message_id = db.query(models.AdminMessages).filter_by(id=id)
            message_id.update({"readed":1})
            db.commit()
            return templates.TemplateResponse("dashboard/get_message.html",{"request":request,"message":message, "user":check['user'],
                                                                            "unread":variables['unread'], "messages_time": variables['messages_time'],
                                                                            "page_title":page_title})
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
        

@messages_panel.get("/inbox/{id}/delete")
def delete_message(id: int, request: Request, db: Session = Depends(database.get_db)):
    check = check_user(request)
    if check['user']:
        if check['user'].admin_user == True or check['user'].super_user == True:
            message = db.query(models.AdminMessages).filter_by(id=id)
            message.delete()
            db.commit()
            request.session["flash_messsage"] = []
            request.session["flash_messsage"].append({"message": "Mesaj silindi", "category": "success"})
            request = RedirectResponse(url="/admin/inbox", status_code=HTTP_303_SEE_OTHER)
            return request
        else:
            return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)



