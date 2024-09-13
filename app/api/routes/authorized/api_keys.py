from fastapi import APIRouter

from app.database.models import ApiKey
from app.schemas import ApiKey as ApiKeySchema
from app.schemas import CreateApiKeyForm

from ._dependencies import AdminRules


api_keys_routes = APIRouter(prefix="/api_key")


@api_keys_routes.post("/create", dependencies=[AdminRules])
async def create_api_key(form: CreateApiKeyForm):
    ApiKey.exists(form.name)
    ApiKey(form).create()


@api_keys_routes.get("", dependencies=[AdminRules])
async def get_api_keys():
    return [
        ApiKeySchema(name=api_key.name)
        for api_key in ApiKey.select_where(all=True)
    ]


@api_keys_routes.delete("/{name}", dependencies=[AdminRules])
async def get_apikey(name: str):
    api_key = ApiKey.select_where(ApiKey.name == name)
    api_key.delete()


@api_keys_routes.get("/{name}", dependencies=[AdminRules])
async def delete_apikey(name: str):
    api_key = ApiKey.select_where(ApiKey.name == name)
    return api_key.key
