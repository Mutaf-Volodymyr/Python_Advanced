from datetime import date
from pydantic import BaseModel, EmailStr, Field, field_validator


class AddressModel(BaseModel):
    city: str = Field(..., pattern=r'^[a-zA-Z- ]{3,30}$')
    street: str = Field(None, pattern=r'^[a-zA-Z- ]{3,30}$')
    house_number: int = Field(None, ge=1)


class UserModel(BaseModel):
    name: str = Field(..., pattern=r'^[a-zA-Z]{2,10}$')
    birthday: date
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)
    is_employed: bool
    address: AddressModel

    @field_validator('is_employed')
    @classmethod
    def validate_is_employed(cls, is_employed: bool, info):
        birthday = info.data['birthday']
        today = date.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        if age < 18:
            raise ValueError("User must be at least 18 years old.")
        elif age > 65:
            raise ValueError("User must be at most 65 years old.")
        return is_employed
