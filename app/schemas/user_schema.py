from pydantic import BaseModel, EmailStr, Field


class UserCreateInput(BaseModel):
    username: str = Field(min_length=3, max_length=255)
    email: EmailStr = Field()
    password: str = Field(min_length=8, max_length=255)


class UserUpdateInput(BaseModel):
    username: str | None = Field(min_length=3, max_length=255)
    email: EmailStr | None = Field()
    password: str | None = Field(min_length=8, max_length=255)


class UserLoginInput(BaseModel):
    email: EmailStr = Field()
    password: str = Field()


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
