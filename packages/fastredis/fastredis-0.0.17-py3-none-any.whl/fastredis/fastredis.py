#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import showlog
import redis
import envx


def make_con_info(
        env_file_name: str = 'local.redis.env'
):
    # ---------------- 固定设置 ----------------
    inner_env = envx.read(file_name=env_file_name)
    if inner_env is None or len(inner_env) == 0:
        showlog.warning('[%s]文件不存在或文件填写错误！' % env_file_name)
        exit()
    else:
        max_connections = inner_env.get('max_connections')
        if max_connections is not None:
            try:
                max_connections = int(max_connections)
            except:
                showlog.warning('max_connections必须是数字！')
        else:
            max_connections = None
        con_info = {
            "host": inner_env.get('host', 'localhost'),
            "port": int(inner_env.get('port', '6379')),
            "password": inner_env.get('password'),
            "max_connections": max_connections,
        }
        return con_info


class Basics:
    def __init__(
            self,
            con_info: dict = None,  # 连结信息，如果设置，将优先使用
            db: int = None,  # 需要连接的数据库，以数字为序号的，从0开始
            host=None,  # 连接的域名
            port=None,  # 连接的端口
            password=None,  # 连接的密码,
            max_connections=None
    ):
        # 初始化所有参数
        if con_info is not None:
            self.con_db = con_info.get('db', 0)
            self.host = con_info.get('host')
            self.port = con_info.get('port')
            self.pwd = con_info.get('password')
            self.max_connections = con_info.get('max_connections')
        else:
            if db is None:
                self.con_db = 0
            else:
                self.con_db = db
            self.host = host
            self.port = port
            self.pwd = password
            self.max_connections = max_connections
        self.pool = self.make_connect_pool()
        self.conn = self.connect()

    def make_connect_pool(
            self
    ):
        # 使用连接池连接，节省每次连接用的时间
        pool = redis.ConnectionPool(
            host=self.host,
            port=self.port,
            password=self.pwd,
            db=self.con_db,
            max_connections=self.max_connections
        )
        return pool

    def connect(
            self
    ):
        # 从连接池中拿出一个连接
        connection = redis.Redis(
            connection_pool=self.pool
        )
        return connection

    def get_db_key_list(
            self,
            auto_reconnect: bool = True  # 自动重连
    ):
        """
        读取指定数据库的键列表
        """
        while True:
            try:
                inner_keys = self.conn.keys()
                key_list = list()
                for key in inner_keys:
                    key_list.append(key.decode())
                return key_list
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def read_list_key_values_length(
            self,
            key,
            auto_reconnect: bool = True  # 自动重连
    ):
        """
        读取指定库的指定键的值列表元素数量
        """
        while True:
            try:
                values_count = self.conn.llen(key)  # 获取列表元素个数
                return values_count
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def read_list_key_values(
            self,
            key,
            auto_reconnect: bool = True  # 自动重连
    ):
        """
        读取指定库的指定键的所有值列表
        """
        while True:
            try:
                values_count = self.conn.llen(key)  # 获取列表元素个数
                values = list()
                for i in range(values_count):
                    while True:
                        try:
                            each_value = self.conn.lindex(key, i)
                            break
                        except:
                            showlog.error('获取失败，准备重连')
                            self.conn = self.connect()
                    if each_value is not None:
                        values.append(each_value.decode())
                return values
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def read_list_first_value(
            self,
            key,
            auto_reconnect: bool = True  # 自动重连
    ):
        """
        获取列表的第一个元素
        """
        while True:
            try:
                last_value = self.conn.lindex(key, 0)
                return last_value
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def read_list_last_value(
            self,
            key,
            auto_reconnect: bool = True  # 自动重连
    ):
        """
        获取列表的最后一个元素
        """
        while True:
            try:
                last_value = self.conn.lindex(key, -1)
                return last_value
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def list_add_l(
            self,
            key,
            value,
            auto_reconnect: bool = True  # 自动重连
    ):
        # 在list左侧添加值
        while True:
            try:
                return self.conn.lpush(key, value)
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def list_add_r(
            self,
            key,
            value,
            auto_reconnect: bool = True  # 自动重连
    ):
        # 在list右侧添加值
        while True:
            try:
                return self.conn.rpush(key, value)
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def list_pop_l(
            self,
            key,
            auto_reconnect: bool = True  # 自动重连
    ):
        # 从左侧出队列
        while True:
            try:
                return self.conn.lpop(key)
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def list_pop_r(
            self,
            key,
            auto_reconnect: bool = True  # 自动重连
    ):
        # 从右侧侧出队列
        while True:
            try:
                return self.conn.rpop(key)
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def set_string(
            self,
            name,
            value,
            ex=None,
            px=None,
            auto_reconnect: bool = True  # 自动重连
    ):
        # 设置键值，ex过期时间（秒），px过期时间（毫秒）
        while True:
            try:
                return self.conn.set(
                    name,
                    value,
                    ex=ex,
                    px=px,
                    nx=False,
                    xx=False
                )
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def get_string(
            self,
            name,
            auto_reconnect: bool = True  # 自动重连
    ):
        # 获取键值
        while True:
            try:
                return self.conn.get(name)
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def delete_string(
            self,
            name,
            auto_reconnect: bool = True  # 自动重连
    ):
        # 删除键值
        while True:
            try:
                return self.conn.delete(name)
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def count_set(
            self,
            key,
            value,
            auto_reconnect: bool = True  # 自动重连
    ):
        # 键 计数 设定值
        while True:
            try:
                return self.conn.set(name=key, value=value)
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def count_add(
            self,
            key,
            auto_reconnect: bool = True  # 自动重连
    ):
        # 键 计数 增加1
        while True:
            try:
                return self.conn.incr(key)
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def count_reduce(
            self,
            key,
            auto_reconnect: bool = True  # 自动重连
    ):
        # 键 计数 减少1
        while True:
            try:
                return self.conn.decr(key)
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return

    def count_get(
            self,
            key,
            auto_reconnect: bool = True  # 自动重连
    ):
        # 键 计数 获取值
        while True:
            try:
                count_value = self.conn.get(key)
                if count_value is None:
                    return
                else:
                    return count_value.decode()
            except:
                pass
            if auto_reconnect is True:
                showlog.error('获取失败，尝试重连...')
                self.conn = self.connect()
            else:
                return


def list_add_r(
        key,
        value,
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env'
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.list_add_r(
        key=key,
        value=value
    )


def list_pop_l(
        key,
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env'
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.list_pop_l(
        key=key
    )


def read_list_key_values(
        key,
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env'
):
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.read_list_key_values(
        key=key
    )


def keys(
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env'
):
    """
    获取键列表
    """
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.get_db_key_list()


def read_list_first_value(
        key,
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env'
):
    # 获取列表的第一个元素
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.read_list_first_value(
        key=key
    )


def read_list_last_value(
        key,
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env'
):
    # 获取列表的最后一个元素
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.read_list_last_value(
        key=key
    )


def count_set(
        key,
        value,
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env'
):
    # 键 计数 设定值
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.count_set(
        key=key,
        value=value
    )


def count_add(
        key,
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env'
):
    # 键 计数 增加1
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.count_add(
        key=key
    )


def count_reduce(
        key,
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env'
):
    # 键 计数 减少1
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.count_reduce(
        key=key
    )


def count_get(
        key,
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env'
):
    # 键 计数 获取值
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.count_get(
        key=key
    )


def read_list_key_values_length(
        key,
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env'
):
    # 键 获取列表元素数量
    # ---------------- 固定设置 ----------------
    if con_info is None:
        con_info = make_con_info(
            env_file_name=env_file_name
        )
    else:
        pass
    if db is None:
        db = 0
    else:
        pass
    con_info['db'] = db
    # ---------------- 固定设置 ----------------
    basics = Basics(
        con_info=con_info
    )
    return basics.read_list_key_values_length(
        key=key
    )
