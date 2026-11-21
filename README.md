项目简介
本项目是一个基于 Python 的轻量级 ETL（Extract-Transform-Load）数据管道。模拟真实电商业务场景，对包含大量空值、重复项及乱码的脏数据进行自动化清洗，最终落库至 MySQL 并输出业务分析指标。

技术栈
语言：Python 3.12
数据处理：Pandas, Numpy
数据库：MySQL 9.7, SQLAlchemy (PyMySQL)
工程化：Logging (日志记录), Try-Except (异常捕获)

核心功能

数据生成：create_data.py 可自动生成 1000 条包含空值、日期格式混乱、金额带单位（如"元"）的脏数据。

数据清洗：project1_etl.py 实现了去重、剔除关键字段空值、字符串正则替换（金额转浮点数）、日期格式标准化。

日志与容错：引入 Logging 模块将执行过程记录至 etl.log，并通过异常捕获保障程序在文件缺失或数据库断连时优雅退出。

数据落库：清洗完成后，通过 SQLAlchemy 批量写入 MySQL 数据库表 clean_orders。

业务分析成果 (SQL)
Top 5 大客户挖掘：通过 GROUP BY 与聚合函数找出贡献销售额前 5 的客户。
订单流失率监控：统计发现，样本数据中已取消订单占比约为 33%，为业务优化提供数据支撑。

如何运行

克隆仓库：git clone https://github.com/lxh-25/Ecommerce-ETL-Project.git

安装依赖：pip install pandas sqlalchemy pymysql

修改 project1_etl.py 中的数据库连接密码

依次运行 create_data.py 和 project1_etl.py




# Ecommerce ETL Project (电商数据清洗与入库)

## 项目简介
基于 Python 构建的工业级轻量 ETL 管道。针对包含大量冗余空列、时间格式混乱、金额精度丢失的真实电商数据（近 10 万行），进行自动化流式清洗，并最终落库至 MySQL，为下游 BI 分析提供高质量数据源。

## 技术栈
- **语言**：Python 3.12
- **数据处理**：Pandas (Chunksize 分块流式处理)
- **数据库**：MySQL 9.7, SQLAlchemy
- **工程化**：Logging (日志追踪), Try-Except (异常捕获)

## 核心功能与亮点
1. **流式分块处理**：使用 Pandas `chunksize=20000` 进行迭代读取，彻底解决百万级大文件导致的内存溢出（OOM）问题。
2. **数据清洗**：自动识别并剔除无用空列；精准修复浮点数精度丢失（保留两位小数）；统一混合时间格式。
3. **增量入库**：采用 `append` 模式追加写入 MySQL，避免历史数据被覆盖。
4. **日志与容错**：引入 Logging 模块记录全链路执行状态，并在异常发生时优雅退出。

## 运行指南
1. 安装依赖：`pip install pandas sqlalchemy pymysql`
2. 配置数据库连接：在脚本中填入你的 MySQL 账号密码。
3. 执行任务：`python taobao_etl.py`
