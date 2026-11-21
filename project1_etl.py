import pandas as pd
from sqlalchemy import create_engine
import logging

# ==========================================
# 1. 配置日志记录 (把信息存到 etl.log 文件里)
# ==========================================
logging.basicConfig(
    filename='etl.log',               # 日志文件名
    level=logging.INFO,               # 记录 INFO 及以上级别的信息
    format='%(asctime)s - %(levelname)s - %(message)s', # 时间 - 级别 - 信息
    encoding='utf-8'
)

def run_etl():
    logging.info("=== ETL 任务开始 ===")
    print("正在执行 ETL，请查看 etl.log 文件...")
    
    try:
        # 2. 提取数据 (Extract)
        logging.info("开始读取 CSV 文件...")
        df = pd.read_csv('dirty_orders.csv', encoding='utf-8-sig')
        logging.info(f"读取成功，共 {len(df)} 行数据。")

        # 3. 清洗数据 (Transform)
        logging.info("开始清洗数据...")
        df = df.drop_duplicates()
        df = df.dropna(subset=['customer_id'])
        df['amount'] = df['amount'].astype(str).str.replace('元', '').astype(float)
        df['order_date'] = pd.to_datetime(df['order_date'], format='mixed')
        logging.info(f"清洗完成，剩余 {len(df)} 行干净数据。")

        # 4. 加载数据 (Load)
        logging.info("开始连接 MySQL 并写入数据...")
        engine = create_engine('mysql+pymysql://root:123456@172.31.224.1:3306/etl_project')
        df.to_sql('clean_orders', con=engine, if_exists='replace', index=False)
        logging.info("数据成功写入数据库！")

    except FileNotFoundError:
        # 如果文件找不到了，会触发这里
        logging.error("找不到 dirty_orders.csv 文件，请检查文件是否存在！")
        print("❌ 错误：文件不存在！")
        
    except Exception as e:
        # 捕获其他所有未知错误（比如数据库密码错了、断网了）
        logging.error(f"ETL 任务失败，发生异常：{e}")
        print(f"❌ 错误：{e}")
        
    finally:
        # 无论成功还是失败，最后都会执行这里
        logging.info("=== ETL 任务结束 ===")

# 执行函数
if __name__ == "__main__":
    run_etl()