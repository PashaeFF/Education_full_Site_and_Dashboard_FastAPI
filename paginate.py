import models, database
from sqlalchemy.orm import Session
from fastapi import Depends

def paginate(data, data_length, page,page_size):
    start = (page - 1) * page_size
    end = start + page_size
    response = {
        "data": data[start:end],
        "total": data_length,
        "count": page_size,
        "pagination": {}
    }

    if end >= data_length:
        response["pagination"]["next"] = None
        if page > 1:
            response["pagination"]["previous"] = f"/?page={page - 1}"
        else:
            response["pagination"]["previous"] = None
    else:
        if page > 1:
            response["pagination"]["previous"] = f"/?page={page- 1}"
        else:
            response["pagination"]["previous"] = None
        response["pagination"]["next"] = f"/?page={page + 1}"


    return response
            
