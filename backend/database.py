from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. SQLite Database URL Define karein
# Yeh local directory me 'taskflow.db' naam ki file bana dega
SQLALCHEMY_DATABASE_URL = "sqlite:///./taskflow.db"

# 2. Engine Create karein (SQLite ke liye connect_args zaroori hai)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 3. SessionLocal class banayein
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base Class (Models isse inherit karenge)
Base = declarative_base()