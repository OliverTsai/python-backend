from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import ApiKey
from app import db
import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/Token')

@auth_bp.route('/Login', methods=['POST'])
def login():
    """
    處理登入請求，驗證API密鑰
    """
    data = request.get_json()
    
    if not data or 'apiKey' not in data:
        return jsonify({'error': 'Missing API key'}), 400
    
    api_key = data['apiKey']
    
    # 查詢API密鑰
    key_record = ApiKey.query.filter_by(key=api_key, is_active=True).first()
    
    if not key_record:
        return jsonify({'error': 'Invalid API key'}), 401
    
    # 創建JWT令牌
    access_token = create_access_token(
        identity=str(key_record.id),
        expires_delta=datetime.timedelta(seconds=1209600)  # 14天
    )
    
    return jsonify({'token': access_token}), 200