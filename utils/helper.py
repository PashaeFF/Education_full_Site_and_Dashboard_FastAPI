from starlette.templating import Jinja2Templates

def closed(request, site_settings):
    return templates.TemplateResponse("site/closed.html", {"request":request, "site_settings":site_settings})


templates = Jinja2Templates(directory="templates")


