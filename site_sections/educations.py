from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from configurations import models, database
from utils.helper import templates, check_user_in_site, site_default_variables
from utils import paginate


site_educations = APIRouter(
    tags=['Site/Educations']
)

@site_educations.get("/educations")
def get_all_educations(request: Request, page: int = 1, page_size: int = 6):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            page_title = check_site_user['site_settings'].site_title+" - "+lang.educations_page_title
            response = paginate.paginate(data=variables['educations'], data_length=len(variables['educations']), page=page, page_size=page_size)
            return templates.TemplateResponse("site/route/educations-page.html", {"request": request, "response":response,
                                                "page_title":page_title, "site_settings":check_site_user['site_settings'], 
                                                "categories":variables['categories'], "news_category":variables['news_category'],
                                                "user":check_site_user['user'], "current_user":check_site_user['current_user'],
                                                "language":lang})


@site_educations.get("/educations/{name}")
def get_category(name: str, request: Request, db: Session = Depends(database.get_db), page: int = 1, page_size: int = 6):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            category_name = db.query(models.EduCategory).filter_by(name=name).first()
            education = db.query(models.Education).filter_by(education_type=name).all()
            page_title = check_site_user['site_settings'].site_title+" - "+category_name.name
            response = paginate.paginate(data=education, data_length=len(education), page=page, page_size=page_size)
            return templates.TemplateResponse("site/route/educations-page.html", {"request": request,"category_name":category_name,
                                                                                    "page_title":page_title, "response":response, "site_settings":check_site_user['site_settings'], "categories":variables['categories'],
                                                                                    "news_category":variables['news_category'], "user":check_site_user['user'], "current_user":check_site_user['current_user'],
                                                                                    "language":lang})


@site_educations.get("/educations/{education_type}/{id}")
def educations(education_type: str, id: int, request: Request, db: Session = Depends(database.get_db)):
    check_site_user = check_user_in_site(request)
    lang = check_user_in_site(request)['site_language']
    if check_site_user['site_settings']:
        if check_site_user['site_settings'].is_active is None:
            return templates.TemplateResponse("site/closed.html", {"request":request})
        else:
            variables = site_default_variables(request)
            education = db.query(models.Education).filter_by(id=id).first()
            page_title = check_site_user['site_settings'].site_title+" - "+education.name
            return templates.TemplateResponse("site/route/education_details.html", {"request": request,"education":education, "site_settings":check_site_user['site_settings'],
                                                "page_title":page_title, "categories":variables['categories'],"news_category":variables['news_category'], "user":check_site_user['user'],
                                                "current_user":check_site_user['current_user'], "language":lang})
