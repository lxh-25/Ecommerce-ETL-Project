import pandas as pd
import numpy as np
import random

n = 1000
data = {
    'order_id': [f'ORD{i:05d}' for i in range(1, n+1)],
    'customer_id': [f'C{random.randint(100, 200)}' for _ in range(n)],
    'order_date': pd.date_range(start='2023-01-01', periods=n, freq='h').astype(str).tolist(),
    'amount': [round(random.uniform(10, 500), 2) for _ in range(n)],
    'status': [random.choice(['Completed', 'Cancelled', 'Pending']) for _ in range(n)]
}

df = pd.DataFrame(data)

# 1. 强行改成万能类型 object，再混入“元”字
df['amount'] = df['amount'].astype(object)
df.loc[random.sample(range(n), 50), 'amount'] = df['amount'].astype(str) + '元'

# 2. 随机弄乱一些日期的格式
df.loc[random.sample(range(n), 50), 'order_date'] = '2023/01/01'

# 3. 随机制造一些空值 (NaN)
df.loc[random.sample(range(n), 30), 'customer_id'] = np.nan

# 4. 故意加入重复行
df = pd.concat([df, df.iloc[10:20]], ignore_index=True)

# 保存为 CSV
df.to_csv('dirty_orders.csv', index=False, encoding='utf-8-sig')
print("1000行带有脏数据的 dirty_orders.csv 已成功生成！")