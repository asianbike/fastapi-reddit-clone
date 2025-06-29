from app.database import engine
from app.models import Base  # 이제 models/__init__.py 덕분에 Base가 전체 모델 포함

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)