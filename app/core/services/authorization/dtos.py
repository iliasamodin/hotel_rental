from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    email: str
    phone: str
    password: str
    first_name: str
    last_name: str
    is_admin: bool = False

    class Config:
        from_attributes = True
