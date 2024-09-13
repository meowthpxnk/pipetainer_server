from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Config, Server
from uvicorn.protocols.utils import get_client_addr, get_path_with_query_string
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app import settings, logger

api = FastAPI()


# api.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@api.exception_handler(Exception)
async def default_exc_handler(request: Request, exc):
    scope = request.scope
    error = str(exc)
    addr = get_client_addr(scope)
    path = get_path_with_query_string(scope)
    method = scope["method"]
    version = scope["http_version"]
    logger.error(f'{addr} - "{method} {path} {version}", reason: {error}')
    # raise HTTPException(
    #     status_code=400, detail="There was an error parsing the body"
    # )
    return JSONResponse(
        {"error": error}, status_code=status.HTTP_400_BAD_REQUEST
    )


config = Config(
    app=CORSMiddleware(
        api,
        allow_origins=[
            "http://localhost:3000",
            "https://connector-front.meowthland.ru",
            "http://localhost:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    host=settings.api.host,
    port=settings.api.port,
    log_config=None,
)

server = Server(config)
