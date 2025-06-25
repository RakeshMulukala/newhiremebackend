# init_db.py
from hiremebackend.database_module import engine
from hiremebackend import models

print("Dropping and recreating all tables...")
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
