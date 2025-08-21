from app import db
from datetime import datetime

class ApiKey(db.Model):
    __tablename__ = 'api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ApiKey {self.id}>'

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    business_no = db.Column(db.String(20), unique=True, nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    company_address = db.Column(db.String(500))
    business_description = db.Column(db.Text)
    introduction = db.Column(db.Text)
    capital_amount = db.Column(db.String(50))
    employee_count = db.Column(db.Integer, default=0)
    organization_type = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯
    industrials = db.relationship('Industrial', backref='company', lazy=True, cascade="all, delete-orphan")
    contacts = db.relationship('Contact', backref='company', lazy=True, cascade="all, delete-orphan")
    telephones = db.relationship('Telephone', backref='company', lazy=True, cascade="all, delete-orphan")
    faxes = db.relationship('Fax', backref='company', lazy=True, cascade="all, delete-orphan")
    emails = db.relationship('Email', backref='company', lazy=True, cascade="all, delete-orphan")
    websites = db.relationship('Website', backref='company', lazy=True, cascade="all, delete-orphan")
    factory_infos = db.relationship('FactoryInfo', backref='company', lazy=True, cascade="all, delete-orphan")
    use_keywords = db.relationship('UseKeyword', backref='company', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Company {self.business_no}>'
    
    def to_dict(self):
        return {
            'Id': str(self.id),
            'BusinessNo': self.business_no,
            'CompanyName': self.company_name,
            'CompanyAddress': self.company_address,
            'BusinessDescription': self.business_description,
            'Introduction': self.introduction,
            'CapitalAmount': self.capital_amount,
            'EmployeeCount': self.employee_count,
            'OrganizationType': self.organization_type,
            'Industrials': [i.name for i in self.industrials],
            'Contacts': [c.name for c in self.contacts],
            'Telephones': [t.number for t in self.telephones],
            'Faxes': [f.number for f in self.faxes],
            'Emails': [e.address for e in self.emails],
            'Websites': [w.url for w in self.websites],
            'FactoryInfos': [f.to_dict() for f in self.factory_infos],
            'UseKeywords': [k.keyword for k in self.use_keywords],
            'UseSource': ["1", "2"],  # 示例來源代碼
            'DataCreateTime': self.created_at.isoformat(),
            'DataLastModifiedTime': self.updated_at.isoformat()
        }

class Industrial(db.Model):
    __tablename__ = 'industrials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    def __repr__(self):
        return f'<Industrial {self.name}>'

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    def __repr__(self):
        return f'<Contact {self.name}>'

class Telephone(db.Model):
    __tablename__ = 'telephones'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    def __repr__(self):
        return f'<Telephone {self.number}>'

class Fax(db.Model):
    __tablename__ = 'faxes'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    def __repr__(self):
        return f'<Fax {self.number}>'

class Email(db.Model):
    __tablename__ = 'emails'
    
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    def __repr__(self):
        return f'<Email {self.address}>'

class Website(db.Model):
    __tablename__ = 'websites'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    def __repr__(self):
        return f'<Website {self.url}>'

class FactoryInfo(db.Model):
    __tablename__ = 'factory_infos'
    
    id = db.Column(db.Integer, primary_key=True)
    regi_id = db.Column(db.String(50), nullable=False)
    factory_name = db.Column(db.String(200), nullable=False)
    factory_address = db.Column(db.String(500))
    contact = db.Column(db.String(100))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    # 關聯
    products = db.relationship('Product', backref='factory_info', lazy=True, cascade="all, delete-orphan")
    used_materials = db.relationship('UsedMaterial', backref='factory_info', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<FactoryInfo {self.factory_name}>'
    
    def to_dict(self):
        return {
            'RegiID': self.regi_id,
            'FactoryName': self.factory_name,
            'FactoryAddress': self.factory_address,
            'Contact': self.contact,
            'Products': [p.name for p in self.products],
            'UsedMaterials': [m.name for m in self.used_materials]
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    factory_info_id = db.Column(db.Integer, db.ForeignKey('factory_infos.id'), nullable=False)
    
    def __repr__(self):
        return f'<Product {self.name}>'

class UsedMaterial(db.Model):
    __tablename__ = 'used_materials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    factory_info_id = db.Column(db.Integer, db.ForeignKey('factory_infos.id'), nullable=False)
    
    def __repr__(self):
        return f'<UsedMaterial {self.name}>'

class UseKeyword(db.Model):
    __tablename__ = 'use_keywords'
    
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    def __repr__(self):
        return f'<UseKeyword {self.keyword}>'

class SearchCursor(db.Model):
    __tablename__ = 'search_cursors'
    
    id = db.Column(db.Integer, primary_key=True)
    cursor_id = db.Column(db.String(36), unique=True, nullable=False)
    keywords = db.Column(db.Text, nullable=False)  # 存儲為JSON字符串
    result_ids = db.Column(db.Text, nullable=False)  # 存儲為JSON字符串
    total_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<SearchCursor {self.cursor_id}>'