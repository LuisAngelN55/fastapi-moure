from fastapi import APIRouter

router = APIRouter (prefix="/products", tags=["products"], responses={404: {"message": "No encontrado"}})

products_list = ["Product1", "Product2", "Product3", "Product4", "Product5"] 

@router.get('/')
async def products():
    return products_list


@router.get('/{id}')
async def products(id: int):
    return products_list[id ]