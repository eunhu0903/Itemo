from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.session import Base, engine
from api.auth import auth, profile
from api.shipping import shipping
from api.product import product

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(shipping.router)
app.include_router(product.router)