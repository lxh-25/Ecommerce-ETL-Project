import pandas as pd
from sqlalchemy import create_engine

# 1. 准备假数据
data = {
    'order_id': [1, 2, 3],
    'name': ['张三', '李四', '王五']
}
df = pd.DataFrame(data)

# 2. 连接数据库 (注意修改这里的密码！)
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/etl_project')

# 3. 写入数据
df.to_sql('test_table', con=engine, if_exists='replace', index=False)

print("数据成功写入数据库！")