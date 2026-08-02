from fastapi import FastAPI
from database import Base, engine
from pos.routers import product,sale,sale_item,customer,user,receipt,payment,supplier,auth,category
import pos.models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="POS API", version="1.0.0")

app.include_router(auth.router) 
app.include_router(user.router)
app.include_router(supplier.router)
app.include_router(category.router)
app.include_router(product.router)


app.include_router(customer.router)
app.include_router(sale.router)
app.include_router(sale_item.router)
app.include_router(payment.router)
app.include_router(receipt.router)

