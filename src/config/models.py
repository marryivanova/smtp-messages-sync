from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


class UserDiscounts(BaseModel):
    user_id: int
    promo_code: str
    sale_id: int


class EmailRequest(BaseModel):
    recipient: str
    subject: str
    body: str


class Sale(BaseModel):
    sale_id: int
    sale_description: str
