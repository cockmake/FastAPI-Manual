import time

import jwt

from settings import SECRET_KEY

def format_current_time():
    # 格式化当前时间
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def generate_token(username, cur_t, alive_time, user_type='user'):
    # alive_time单位为秒
    # 使用jwt 根据secret_key生成token
    # token中包含用户名、当前时间戳和过期时间戳。
    encode_info = {
        'username': username,
        'login_time': cur_t,
        'expire_time': cur_t + alive_time,
        'user_type': user_type
    }
    encoded_jwt = jwt.encode(encode_info, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def get_operation_description(username, operation_type, affected_ids):
    """
    根据操作类型和受影响的id列表生成操作描述
    :param username: str
    :param operation_type: 增、删、批量增、登录、注销
    :param affected_ids: type: list、int
    :return: str
    """
    if operation_type in ["增", "删"]:
        return f"{format_current_time()}：\n用户{username}{operation_type}了\n序号为：{affected_ids}的数据".replace('\'',
                                                                                                                  '')
    elif operation_type == "批量增":
        return f"{format_current_time()}：\n用户{username}批量增加了\n序号为：{affected_ids[0]} -- {affected_ids[1]}的数据".replace(
            '\'', '')
    elif operation_type == "登录":
        return f"{format_current_time()}：\n用户{username}登录了系统"
    elif operation_type == "注销":
        return f"{format_current_time()}：\n用户{username}退出了系统"
    else:
        return "未知操作类型"