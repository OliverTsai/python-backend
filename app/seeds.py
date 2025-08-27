# app/seeds.py
from app import db
from app.models import ApiKey, Company, CompanyGov  # 添加 CompanyGov 導入
from datetime import datetime
import pandas as pd
import os
import gc  # 添加垃圾回收模組

def seed_data():
    """
    添加初始數據到數據庫
    """
    print("開始添加種子數據...")
    
    # 檢查是否已經有 API 密鑰，如果沒有則添加
    if ApiKey.query.count() == 0:
        print("添加默認 API 密鑰...")
        default_api_key = ApiKey(key='admin123', is_active=True)
        db.session.add(default_api_key)
        
    # 添加一些示例公司數據
    if Company.query.count() == 0:
        print("添加示例公司數據...")
        companies = [
            Company(
                business_no="12345678",
                company_name="示例科技有限公司",
                company_address="台北市信義區信義路五段7號",
                business_description="專注於人工智能和大數據分析的科技公司",
                capital_amount=10000000,
                employee_count=50,
                organization_type="有限公司"
            ),
            Company(
                business_no="87654321",
                company_name="未來電子股份有限公司",
                company_address="新北市板橋區縣民大道二段7號",
                business_description="電子零件製造與銷售",
                capital_amount=50000000,
                employee_count=200,
                organization_type="股份有限公司"
            )
        ]
        db.session.add_all(companies)
        db.session.commit()
    
    # --- CSV 文件路徑修正 ---
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # /app
    csv_path = os.path.join(BASE_DIR, "tests", "gov.csv")

    if os.path.exists(csv_path):
        print(f"正在讀取 {csv_path} 文件...")
        try:
            # 定義列名，根據您提供的資料結構
            column_names = [
                'company_address',         # 地址
                'business_no',             # 統一編號
                'head_office_business_no', # 總機構統一編號
                'company_name',            # 名稱
                'capital_amount',          # 資本額
                'create_date',             # 設立日期
                'organization_type',       # 組織名稱
                'use_business_invoice',    # 使用統一發票
                'industrial_code1',        # 行業代碼
                'industrial_name1',        # 行業名稱
                'industrial_code2',        # 行業代碼2
                'industrial_name2',        # 行業名稱2
                'industrial_code3',        # 行業代碼3
                'industrial_name3',        # 行業名稱3
                'industrial_code4',        # 行業代碼4
                'industrial_name4'         # 行業名稱4
            ]

            print("目前的數據庫中 CompanyGov 記錄數量:", CompanyGov.query.count())
            
            # 如果需要將 CSV 數據導入到數據庫
            if CompanyGov.query.count() == 0:
                print("從 CSV 文件添加政府公司資料...")
                
                # 批次處理參數
                batch_size = 1000  # 每批處理的記錄數
                total_imported = 0
                
                # 使用 chunksize 參數分批讀取 CSV 文件
                for chunk_df in pd.read_csv(csv_path, header=None, names=column_names, chunksize=batch_size):
                    print(f"正在處理第 {total_imported} 到 {total_imported + len(chunk_df)} 條記錄...")
                    
                    # 創建批次記錄
                    batch_records = []
                    for index, row in chunk_df.iterrows():
                        try:
                            # 使用當前時間作為資料創建和修改時間
                            current_time = datetime.utcnow()
                            # 從統一編號中提取公司名稱的一部分作為 company_name_part
                            company_name = row['company_name']
                            company_name_part = company_name[:3] if len(company_name) > 3 else company_name
                            
                            # 從地址中提取縣市部分作為 company_address_part
                            address = row['company_address']
                            address_parts = address.split('縣') if '縣' in address else address.split('市')
                            company_address_part = address_parts[0] + ('縣' if '縣' in address else '市') if len(address_parts) > 1 else address
                            
                            company_gov = CompanyGov(
                                _id=row['business_no'],
                                business_no=row['business_no'],
                                capital_amount=str(row['capital_amount']),
                                company_address=row['company_address'],
                                company_address_part=company_address_part,
                                company_name=row['company_name'],
                                company_name_part=company_name_part,
                                create_date=str(row['create_date']),
                                data_create_time=current_time,
                                data_last_modified_time=current_time,
                                head_office_business_no=row['head_office_business_no'] if pd.notna(row['head_office_business_no']) else "",
                                industrial_code1=str(row['industrial_code1']) if pd.notna(row['industrial_code1']) else "",
                                industrial_code2=str(row['industrial_code2']) if pd.notna(row['industrial_code2']) else "",
                                industrial_code3=str(row['industrial_code3']) if pd.notna(row['industrial_code3']) else "",
                                industrial_code4=str(row['industrial_code4']) if pd.notna(row['industrial_code4']) else "",
                                industrial_name1=str(row['industrial_name1']) if pd.notna(row['industrial_name1']) else "",
                                industrial_name2=str(row['industrial_name2']) if pd.notna(row['industrial_name2']) else "",
                                industrial_name3=str(row['industrial_name3']) if pd.notna(row['industrial_name3']) else "",
                                industrial_name4=str(row['industrial_name4']) if pd.notna(row['industrial_name4']) else "",
                                organization_type=row['organization_type'],
                                use_business_invoice=row['use_business_invoice']
                            )
                            batch_records.append(company_gov)
                        except Exception as e:
                            print(f"處理第 {index} 行時出錯: {e}")
                            continue
                    
                    # 批次添加記錄到數據庫
                    if batch_records:
                        try:
                            db.session.add_all(batch_records)
                            db.session.commit()
                            total_imported += len(batch_records)
                            print(f"成功導入 {len(batch_records)} 條記錄，總計: {total_imported}")
                        except Exception as e:
                            db.session.rollback()
                            print(f"批次提交時出錯: {e}")
                    
                    # 清理記憶體
                    del batch_records
                    gc.collect()
                
                print(f"已從 CSV 文件導入總計 {total_imported} 條記錄")
        except Exception as e:
            print(f"讀取 CSV 文件時出錯: {e}")
    else:
        print(f"找不到 CSV 文件: {csv_path}")
        
        # 如果找不到 CSV 文件，則添加一個示例政府公司資料
        if CompanyGov.query.count() == 0:
            print("添加示例政府公司資料...")
            company_govs = [
                CompanyGov(
                    _id="99995009",
                    business_no="99995009",
                    capital_amount="200000",
                    company_address="臺北市萬華區新起里漢中街１３５號地下",
                    company_address_part="臺北市",
                    company_name="灰姑娘舞蹈團體服裝行",
                    company_name_part="灰姑娘舞",
                    create_date="0940406",
                    data_create_time=datetime.fromisoformat("2025-06-05T02:33:02.540+08:00"),
                    data_last_modified_time=datetime.fromisoformat("2025-06-08T11:28:15.592+08:00"),
                    head_office_business_no="",
                    industrial_code1="455211",
                    industrial_code2="",
                    industrial_code3="",
                    industrial_code4="",
                    industrial_name1="服裝批發",
                    industrial_name2="",
                    industrial_name3="",
                    industrial_name4="",
                    organization_type="獨資",
                    use_business_invoice="Y"
                )
            ]
            db.session.add_all(company_govs)
            db.session.commit()

    print("種子數據添加完成！")