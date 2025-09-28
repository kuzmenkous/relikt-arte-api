from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


# @router.post("/", response_model=UserCreate)
# async def create_user(user: UserCreate):
#     return user


# @router.put("/{user_id}", response_model=UserUpdate)
# async def update_user(user_id: int, user: UserUpdate):
#     return user
