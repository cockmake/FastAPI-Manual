from fastapi import APIRouter

from ObjectModel.data import User

users_route = APIRouter(prefix='/users', tags=["users"])


@users_route.post(
    '/create',
    response_model=User,
    response_model_exclude_none=True,  # 不返回None值
    # response_model_exclude_unset=True,  # 不返回默认值 如果请求中有传入则返回
    response_model_exclude_defaults=True,  # 不返回默认值 如果传入了值与默认值相同也不返回
    response_model_exclude={"password"}
)
async def create_user(user: User):
    return user
