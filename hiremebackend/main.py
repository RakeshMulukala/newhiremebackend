from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from hiremebackend.database_module import Base, engine
from hiremebackend.routers import users, deliveries, coupons, recipes, notifications
from hiremebackend.routers import auth_router

# Auto-create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hire Me API", version="1.0.0")

# ✅ CORS config — allow your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://glittery-liger-d83c39.netlify.app",  # ✅ your deployed frontend
        "http://localhost:3000",                      # ✅ local development (optional)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Swagger JWT Auth Setup
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Hire Me API",
        version="1.0.0",
        description="API for the Hire Me App with JWT Authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ✅ Include All Routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(deliveries.router, prefix="/deliveries", tags=["Deliveries"])
app.include_router(coupons.router, prefix="/coupons", tags=["Coupons"])
app.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])


# ✅ Root test
@app.get("/")
async def root(request: Request):
    return {"message": "Hire Me API is live and connected!"}


