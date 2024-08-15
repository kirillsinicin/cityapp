from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers.cities import CityAppException, city_router

app = FastAPI()


@app.exception_handler(CityAppException)
def city_app_exception_handler(request: Request, exc: CityAppException):
    return exc.response


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": "Ошибка валидации"},
    )


app.include_router(city_router)
