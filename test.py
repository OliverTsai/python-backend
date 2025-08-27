# test.py
import psycopg2
import sys

# 資料庫連線設定
DB_CONFIG = {
    'dbname': 'company_search',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',  # 如果在容器外執行，使用 localhost
    'port': '5433'        # 對應 docker-compose 中映射的外部端口
}

def search_company_by_address():
    """
    查詢公司地址中包含"台中"的記錄
    """
    try:
        # 連接到資料庫
        print("正在連接到資料庫...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 查詢地址中包含"台中"的記錄
        address_query = """
        SELECT business_no, company_name, company_address, capital_amount, 
               organization_type, create_date, industrial_code1, industrial_name1
        FROM company_govs
        WHERE company_address LIKE %s
        LIMIT 20  -- 限制返回記錄數量，避免結果過多
        """
        cursor.execute(address_query, ("%台中%",))
        address_results = cursor.fetchall()
        
        print("\n===== 地址包含「台中」的查詢結果 =====")
        if address_results:
            print(f"找到 {len(address_results)} 條匹配記錄 (限制顯示20條):")
            for record in address_results:
                print_company_info(record)
                
            # 查詢符合條件的總記錄數
            count_query = """
            SELECT COUNT(*)
            FROM company_govs
            WHERE company_address LIKE %s
            """
            cursor.execute(count_query, ("%台中%",))
            total_matching = cursor.fetchone()[0]
            print(f"\n資料庫中共有 {total_matching} 條地址包含「台中」的記錄")
        else:
            print("未找到地址包含「台中」的記錄")
            
            # 查詢資料庫中的總記錄數
            cursor.execute("SELECT COUNT(*) FROM company_govs")
            total_records = cursor.fetchone()[0]
            print(f"\n資料庫中 company_govs 表共有 {total_records} 條記錄")
            
            # 如果有記錄，隨機顯示一條作為參考
            if total_records > 0:
                cursor.execute("""
                SELECT business_no, company_name, company_address, capital_amount, 
                       organization_type, create_date, industrial_code1, industrial_name1
                FROM company_govs
                LIMIT 1
                """)
                sample_record = cursor.fetchone()
                print("\n資料庫中的樣本記錄:")
                print_company_info(sample_record)
                
                # 檢查是否有任何地址欄位包含中文字符
                cursor.execute("""
                SELECT COUNT(*)
                FROM company_govs
                WHERE company_address ~ '[一-龥]'
                """)
                chinese_count = cursor.fetchone()[0]
                print(f"\n資料庫中有 {chinese_count} 條記錄的地址包含中文字符")
        
        # 關閉資料庫連接
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"查詢過程中發生錯誤: {e}")
        return 1
    
    return 0

def print_company_info(record):
    """
    打印公司信息的輔助函數
    """
    # 根據查詢結果的順序解析記錄
    business_no, company_name, company_address, capital_amount, organization_type, create_date, industrial_code1, industrial_name1 = record
    
    print(f"統一編號: {business_no}")
    print(f"公司名稱: {company_name}")
    print(f"公司地址: {company_address}")
    print(f"資本額: {capital_amount}")
    print(f"組織類型: {organization_type}")
    print(f"成立日期: {create_date}")
    print(f"行業代碼1: {industrial_code1}")
    print(f"行業名稱1: {industrial_name1}")
    print("-" * 50)

if __name__ == "__main__":
    sys.exit(search_company_by_address())