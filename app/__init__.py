from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
from flask_cors import CORS

# 初始化擴展
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# 創建 CORS 實例
cors = CORS()

def create_app():
    app = Flask(__name__)
    
    # 配置
    app.config.from_object('app.config.Config')
    
    # 初始化擴展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    cors.init_app(app, resources={r"/*": {"origins": "http://localhost:8080"}})
    
    # 註冊藍圖
    from app.routes import main_bp
    from app.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    # 創建數據表
    with app.app_context():
        db.create_all()

        # 導入並運行種子數據函數
        from app.seeds import seed_data
        seed_data()
        
        # 如果沒有API密鑰，創建一個默認的
        # from app.models import ApiKey
        # if not ApiKey.query.first():
        #     default_key = ApiKey(key="admin123", is_active=True, description="Default API Key")
        #     db.session.add(default_key)
        #     db.session.commit()
    
    return app

# 確保可以被 gunicorn 導入
app = create_app()