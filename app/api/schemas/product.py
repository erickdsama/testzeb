from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    summary: str
    sku: str
    summary: str
    photo: str
    brand: str
    long_description: str

    class Config:
        orm_mode = True
