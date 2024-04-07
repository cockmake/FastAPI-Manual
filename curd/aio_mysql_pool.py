from typing import Union

import aiomysql

from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_POOL_SIZE


# 修改为异步
class MYSQLOP:
    def __init__(self):
        self.user_table = "user_table"  # 已经注册的用户表
        self.user_to_register_table = "user_to_register_table"  # 待审核的用户表
        self.data_center_table = "data_center_table"  # 数据中心表
        self.operation_log_table = "operation_log_table"  # 操作日志表
        self.data_drop_table = "data_drop_table"  # 数据删除表
        # 用户可以修改的字段、允许插入、删除的表
        self.user_fields_table = "user_fields_table"  # 用户可以修改的字段表 （还包括增、删两个权限）

        self.mysql_pool: Union[aiomysql.Pool, None] = None

    async def init_pool(self):
        self.mysql_pool = await aiomysql.create_pool(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DATABASE,
            minsize=MYSQL_POOL_SIZE // 2,
            maxsize=MYSQL_POOL_SIZE,
            cursorclass=aiomysql.cursors.DictCursor
        )
    async def query_user_info_from_username(self, username):
        # 根据用户名查询用户信息
        # 如果存在返回用户信息
        # 如果不存在返回None
        async with await self.mysql_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                sql = "SELECT * FROM %s WHERE username = '%s'" % (self.user_table, username)
                await cursor.execute(sql)
                result = await cursor.fetchone()
        return result

    async def get_user_privilege(self, username, name):
        # 获取用户权限
        async with self.mysql_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                sql = "SELECT * FROM %s WHERE username = '%s' AND name = '%s'" % (
                    self.user_fields_table, username, name)
                await cursor.execute(sql)
                result = await cursor.fetchone()
        return result

    async def write_operation_log(self, username, operation_type, operation_desc):
        # 插入操作日志表
        sql = "INSERT INTO %s (username, operation_type, operation_desc) VALUES ('%s', '%s', '%s')" % (
            self.operation_log_table, username, operation_type, operation_desc)
        try:
            async with self.mysql_pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(sql)
                    await conn.commit()
            return True
        except Exception as e:
            print(e)
            return False



aio_mysql_pool = MYSQLOP()
