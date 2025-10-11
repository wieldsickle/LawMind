import os
import pymysql
from pymysql import Error
from dotenv import load_dotenv
from contextlib import contextmanager


# 加载环境变量
load_dotenv()

# 创建数据库连接,使用上下文管理器
@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER"),
            port=int(os.getenv("DB_PORT", 3306)),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
            connect_timeout=10,
            read_timeout=10,
            write_timeout=10,
        )
        # 强制设置本次连接使用 utf8mb4，避免 1366 错误
        try:
            with connection.cursor() as _c:
                _c.execute("SET NAMES utf8mb4")
                _c.execute("SET character_set_connection = utf8mb4")
                _c.execute("SET collation_connection = utf8mb4_unicode_ci")
        except Exception as _:
            pass
        print("成功连接到MySQL数据库")
        yield connection
    except Exception as e:
        print(f"数据库连接错误: {e}")
        if connection:
            connection.rollback()
        raise
    # finally:
    #     if connection and connection.open:
    #         connection.close()
    #         print("数据库连接已关闭")


# 测试连接
if __name__ == "__main__":
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("数据库可访问:", cursor.fetchone())
    except Exception as e:
        print("测试失败:", e)