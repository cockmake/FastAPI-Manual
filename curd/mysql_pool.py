import pymysql
from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor

from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_POOL_SIZE


class MYSQLOP:
    def __init__(self):
        self.mysql_pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            mincached=MYSQL_POOL_SIZE // 2,  # 初始化时，链接池中至少创建的链接，0表示不创建
            maxcached=MYSQL_POOL_SIZE,
            maxusage=100,  # 一个连接可以复用的次数
            ping=0,
            maxconnections=2000,  # 连接池允许的最大连接数 不要超过数据库的限制
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        self.user_table = "user_table"  # 已经注册的用户表
        self.user_to_register_table = "user_to_register_table"  # 待审核的用户表
        self.data_center_table = "data_center_table"  # 数据中心表
        self.operation_log_table = "operation_log_table"  # 操作日志表
        self.data_drop_table = "data_drop_table"  # 数据删除表
        # 用户可以修改的字段、允许插入、删除的表
        self.user_fields_table = "user_fields_table"  # 用户可以修改的字段表 （还包括增、删两个权限）

    def get_user_privilege(self, username, name):
        # 获取用户权限
        with self.mysql_pool.connection() as conn:
            with conn.cursor(cursor=DictCursor) as cursor:
                sql = "SELECT * FROM %s WHERE username = '%s' AND name = '%s'" % (
                    self.user_fields_table, username, name)
                cursor.execute(sql)
                result = cursor.fetchone()
        return result

    def query_user_info_from_username(self, username):
        # 根据用户名查询用户信息
        # 如果存在返回用户信息
        # 如果不存在返回None
        with self.mysql_pool.connection() as conn:
            with conn.cursor(cursor=DictCursor) as cursor:
                sql = "SELECT * FROM %s WHERE username = '%s'" % (self.user_table, username)
                cursor.execute(sql)
                result = cursor.fetchone()
                return result

    def write_operation_log(self, username, operation_type, operation_desc):
        # 插入操作日志表
        sql = "INSERT INTO %s (username, operation_type, operation_desc) VALUES ('%s', '%s', '%s')" % (
            self.operation_log_table, username, operation_type, operation_desc)
        try:
            with self.mysql_pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    conn.commit()
            return True
        except Exception as e:
            print(e)
            return False


mysql_pool = MYSQLOP()
