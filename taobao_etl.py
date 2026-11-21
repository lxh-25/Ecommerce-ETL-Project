# 初步尝试
# import pandas as pd 

# file_path= './taobao_data.csv'
# df =pd.read_csv(file_path)
# # print(df.head())
# # print(df.columns)

# # print(df.shape)
# # print(df.info())
# cols_to_drop=[col for col in df.columns if 'Unnamed' in col]
# df =df.drop(columns=cols_to_drop)
# # print(df.info())
# print(df.head())
# df['price']=df['price'].round(2)
# df['invoice_date']=pd.to_datetime(df['invoice_date'],format='mixed')
# print(df.info())


# #链接数据库mysql
# from sqlalchemy import create_engine
# engine =create_engine('mysql+pymysql://root:123456@localhost:3306/etl_project')

# df.to_sql('taobao_clean_orders',con=engine,if_exists='replace',index=False)

# 少量数据
# import pandas as pd
# from sqlalchemy import create_engine   #为了连接mysql
# import logging  #引入日志 防止突发情况无法检查

# logging.basicConfig(
#     filename='etl_taobao.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     encoding='utf-8'

# )
# def run_etl():
#     logging.info("======etl任务开始======")
#     try:
#         df=pd.read_csv('./taobao_data.csv')
#         cols_to_drop = [col for col in df.columns if 'Unnamed' in col]
#         df = df.drop(columns=cols_to_drop)
#         df['price'] = df['price'].round(2)
#         df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='mixed')
#         logging.info(f"数据清洗完成，共 {len(df)} 行")
#         engine = create_engine('mysql+pymysql://root:123456@localhost:3306/etl_project')
#         df.to_sql('taobao_clean_orders', con=engine, if_exists='replace', index=False)
#         logging.info("数据成功写入数据库！")

#     except Exception as e:
#         logging.error(f"ETL 任务失败，异常信息：{e}")
#         print(f"❌ 出错了：{e}")
# if __name__ == "__main__":
#     run_etl()
import pandas as pd
from sqlalchemy import create_engine
import logging 

logging.basicConfig(filename='etl_chunk.log', level=logging.INFO,
                     format='%(asctime)s - %(levelname)s - %(message)s', 
                     encoding='utf-8')
        
def run_chunk_etl():
    logging.info("======分块任务开始======")
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/etl_project')
    try:
        chunk_iter=pd.read_csv('./taobao_data.csv',chunksize=20000)
        chunk_count= 0
        for chunk in chunk_iter:
            chunk_count+=1
            print(f"正在处理第{chunk_count}块数据...")
            cols_to_drop= [col for col in chunk.columns if 'Unnamed' in col]
            chunk = chunk.drop(columns = cols_to_drop)
            chunk['price']=chunk['price'].round(2)
            chunk['invoice_date'] = pd.to_datetime(chunk['invoice_date'], 
                                                   format='mixed')
            
            chunk.to_sql('taobao_clean_orders_chunked', con=engine, if_exists='append', index=False)
            
        print("🎉 所有分块处理完毕，入库成功！")
        logging.info(f"分块处理完成，共处理了 {chunk_count} 块数据")

    except Exception as e:
        logging.error(f"ETL 任务失败，异常信息：{e}")
        print(f"❌ 出错了：{e}")
if __name__ == "__main__":
    run_chunk_etl()

