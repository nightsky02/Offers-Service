from fastapi import FastAPI, UploadFile, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.excel.procedure import parse_file
from app.excel.exceptions import UniqueOfferExpection, FileStructureError
from app.database import api
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.add_middleware(CORSMiddleware,
        allow_origins="*",
        allow_methods=["POST", "GET"],
        allow_headers="*")


@app.exception_handler(RequestValidationError)
async def handle_validation_exception(request: Request, err: RequestValidationError):
    response_dict = {}
    
    for error_body in err.errors():
        property_name = error_body["loc"][1]
        response_dict[property_name] = error_body["msg"]
    
    return JSONResponse(
        status_code=422,
        content=response_dict
    )

@app.post("/upload/")
def upload_excel_file(request: Request, file: UploadFile, user_id: int = Query(ge=0)):
    if not file.filename.endswith(".xlsx"):
        return {"status" : "error", "msg" : "service accepts only excel files"}
    
    try:
        result = parse_file(file.file)
    except UniqueOfferExpection as err:
        return {
            "msg" : "The offer with this id already exists in the file",
            "offer_id" : err.offer_id,
            "offer_name" : err.offer_name
        }
    except FileStructureError:
        return {"msg" : "Invalid structure of the file. It must contain 5 cells"}
    
    process_result = api.process_offers(user_id, result.correct_offers)

    return templates.TemplateResponse(request, "upload_results.html", context={
        "correct_offers" : result.correct_offers,
        "wrong_offers" : result.wrong_offers,
        "created_count" : process_result.success_count,
        "deleted_count" : process_result.deleted_count,
        "updated_count" : process_result.updated_count
    })

@app.get("/offers/")
def get_offers(request: Request, 
               seller_id: Annotated[int | None, Query(ge=0)] = None, 
               offer_id: Annotated[int | None, Query(ge=0)] = None,
                substr: Annotated[str | None, Query(max_length=10)] = None):
    
    offers = api.select_offers(seller_id, offer_id, substr)

    return templates.TemplateResponse(request, "search_result.html", context={
        "offers" : offers,
        "seller_id" : seller_id,
        "offer_id" : offer_id,
        "substr" : substr
    })



if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)