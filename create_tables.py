from hiremebackend.database_module import engine
from hiremebackend import models

print("⏳ Creating tables...")
models.Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
