from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

#  Chuỗi kết nối MySQL với PyMySQL
sql = "mysql+pymysql://root:130404@localhost:3306/product-management"

#  Tạo engine kết nối
engine = create_engine(sql, echo=True)  # thêm echo=True để log SQL truy vấn

#  Tạo session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

#  Tạo Base class cho các model
Base = declarative_base()

#  Dependency cho FastAPI
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
