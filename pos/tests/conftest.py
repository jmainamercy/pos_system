# import os
# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.pool import StaticPool

# os.environ["DATABASE_URL"] = "sqlite://"

# from database import Base, get_db
# from main import app

# from dependencies import get_current_user 

# engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
# TestingSessionLocal = sessionmaker(bind=engine)

# class MockUser:
#     id = 1
#     username = "John"
#     masked_password = "hashed_dummy_string"
#     full_name = "John Doe"
#     role = "admin"       
#     is_active = True    

# @pytest.fixture
# def client():
#     Base.metadata.create_all(bind=engine)

#     def override_get_db():
#         db = TestingSessionLocal()
#         try:
#             yield db
#         finally:
#             db.close()

#     app.dependency_overrides[get_db] = override_get_db

#     def override_get_current_user():
#         return MockUser()
        
#     app.dependency_overrides[get_current_user] = override_get_current_user

#     yield TestClient(app)

#     app.dependency_overrides.clear()
#     Base.metadata.drop_all(bind=engine)
import os
import pytest
from datetime import datetime  # Added to handle database timestamp fields
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"

from database import Base, get_db
from main import app
from dependencies import get_current_user 

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind=engine)

class MockUser:
    id = 1
    username = "John"
    masked_password = "hashed_dummy_string"
    full_name = "John Doe"
    role = "admin"
    is_active = True

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        categories_table = Base.metadata.tables['categories']
        suppliers_table = Base.metadata.tables['suppliers']

        cat_payload = {"id": 1}
        for col in categories_table.columns:
            if col.name == 'id':
                continue
            if isinstance(col.type, DateTime):
                cat_payload[col.name] = datetime.utcnow()
            else:
                cat_payload[col.name] = f"Test Category {col.name}"

        sup_payload = {"id": 5}
        for col in suppliers_table.columns:
            if col.name == 'id':
                continue
            if isinstance(col.type, DateTime):
                sup_payload[col.name] = datetime.utcnow()
            else:
                sup_payload[col.name] = f"Test Supplier {col.name}"

        db.execute(categories_table.insert().values(**cat_payload))
        db.execute(suppliers_table.insert().values(**sup_payload))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Intelligent Seeding failed: {e}")
    finally:
        db.close()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = lambda: MockUser()

    yield TestClient(app)

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
