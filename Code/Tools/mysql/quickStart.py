# coding: utf-8
# Author: wanhui0729@gmail.com

import json
import logging
import MySQLdb
from DBUtils.PooledDB import PooledDB


class MySQLClient(object):
    """
    MySQL客户端封装。
    """

    def __init__(self, conf, pool_count=5):
        """
        Args:
            conf: 数据连接配制
            pool_count: 连接池连接数
        Returns:
            b: type
        """

        try:
            self._pool = PooledDB(MySQLdb, pool_count, **conf)
        except Exception as e:
            logging.exception(e)
            raise SystemError(e)

    def _get_connect_from_pool(self):
        return self._pool.connection()

    def execute(self, sql, data):
        """
        执行SQL
        Args:
            sql: 数组，元素是SQL字符串
        Returns:
            None
        """
        conn = self._get_connect_from_pool()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, data)
            conn.commit()
        except Exception as e:
            logging.exception(e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def executemany(self, sql, datas):
        """
        Args:
            sql: SQL语句
            datas: 数据
        Returns:
            None
        """
        conn = self._get_connect_from_pool()
        cursor = conn.cursor()
        try:
            cursor.executemany(sql, datas)
            conn.commit()
        except Exception as e:
            logging.exception(e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def fetchall(self, sql, data=()):
        """
        查询SQL，获取所有指定的列
        Args:
            sql: SQL语句
        Returns:
            结果集
        """
        results = []
        conn = self._get_connect_from_pool()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, data)
            results = cursor.fetchall()
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()
            conn.close()
        return results



# 数据库连接
conf = {
    'host': '172.16.0.111',
    'port': 3306,
    'user': 'root',
    'passwd': 'XA4ljMs4dqGFJb',
    'db': 'db_rock_ai_auto',
    'charset': 'utf8'
}

_db = MySQLClient(conf)
_logger = logging.getLogger(__name__)

def _to_list(x):
    if isinstance(x, list):
        return x
    elif isinstance(x, (str, )):
        return [a.strip() for a in x.split(',')]
    else:
        raise ValueError('不能转成list: %r' % x)

class DBClass(object):
    # 默认第一个为ID，后面为create_time, update_time, status
    table_name = None
    fields = ''
    field_parses = {}
    default_values = {}
    ignore_fields = ['create_time', 'update_time']

    def __init__(self, item=None, mapping=None):
        # item为可遍历的数组或者tuple
        # mapping为数组或者字符串，元素以逗号隔开
        super(DBClass, self).__init__()

        # 表名
        assert self.__class__.table_name is not None
        self._table_name = self.__class__.table_name

        # 所有字段
        self._fields = _to_list(self.__class__.fields)

        # 忽略字段
        self._ignore_fields = _to_list(self.__class__.ignore_fields)

        # ID名
        self._id_name = self._fields[0]  # 默认ID名为第一个字段
        assert 'id' in self._id_name

        # 数据默认内容
        self._datas = {}
        for field in self._fields:
            self._datas[field] = self.__class__.default_values.get(field, None)

        if item is not None:
            assert mapping is not None
            if isinstance(mapping, (str,)):
                mapping = map(lambda x: x.strip(), mapping.split(','))
            update_datas = dict(zip(mapping, list(item)))
            self.loads(update_datas)

    def dumps(self):
        names, values = self.get_names_values()
        value = dict(zip(names, values))
        return value

    def loads(self, data_dict):
        for name in self._fields:
            if name in data_dict:
                value = data_dict[name]
                if value is not None and name in self.__class__.field_parses:
                    parser = self.__class__.field_parses[name]
                    self._datas[name] = parser.loads(value)
                else:
                    self._datas[name] = value

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            assert name in self._fields
            self._datas[name] = value

    def __getattr__(self, name):
        if name.startswith('_'):
            return self.__dict__[name]
        else:
            assert name in self._fields
            return self._datas[name]

    def get_names(self, excludes=[]):
        if not isinstance(excludes, list):
            excludes = [excludes]
        return list(set(self._fields) - set(excludes))

    def get_values(self, names):
        # 所有names中的元素的值，且是通过转换后的
        values = []
        for name in names:
            value = self._datas[name]
            if value is not None and name in self.__class__.field_parses:
                value = self.__class__.field_parses[name].dumps(value)
            values.append(value)
        return values

    def get_names_values(self, excludes=[]):
        names = self.get_names(excludes)
        values = self.get_values(names)
        return names, values

    def __repr__(self):
        names, values = self.get_names_values()
        data = dict(zip(names, values))
        return json.dumps(data, indent=4)

    def insert(self):
        assert self._datas[self._id_name] is None
        names, values = self.get_names_values(excludes=self._ignore_fields + [self._id_name])
        sql = """
        INSERT INTO %s (%s)
        VALUES (%s)
        """ % (self._table_name, ', '.join(names), ', '.join(['%s'] * len(names)))
        insert_id = _db.execute(sql, tuple(values))
        self._datas[self._id_name] = insert_id
        return insert_id

    def update(self, names):
        assert self._datas[self._id_name] is not None
        names = _to_list(names)
        if len(names) == 0:
            names = self.get_names(excludes=self._ignore_fields + [self._id_name])
        values = self.get_values(names)
        set_str = ', '.join(['%s=%%s' % name for name in names])
        sql = '''
        UPDATE %s
        SET %s
        WHERE %s = %%s
        ''' % (self._table_name, set_str, self._id_name)
        datas = tuple(values + [self._datas[self._id_name]])
        _db.execute(sql, datas)
        return True

    def delete(self):
        self.status = 0
        self.update(names=['status'])

    def delete_clear(self):
        assert self._datas[self._id_name] is not None
        _logger.info('Warning: 完整的删除记录(只能用于单元测试): %r' % self._table_name)
        sql = """DELETE FROM %s WHERE %s = %%s""" % (self._table_name, self._id_name)
        _db.execute(sql, (self._datas[self._id_name],))

    @classmethod
    def delete_multi(cls, condition):
        keys = condition.keys()
        values = condition.values()
        _local_one = cls()
        for key in keys:
            assert key in _local_one._fields
        where_place = ' AND '.join(['%s = %%s' % key for key in keys])
        _logger.info('Warning: 完整的删除多条记录(只能用于单元测试): %r' % _local_one._table_name)
        sql = """DELETE FROM %s WHERE %s""" % (_local_one._table_name, where_place)
        _db.execute(sql, tuple(values))

    @classmethod
    def get_multi(cls, condition):
        keys = condition.keys()
        values = condition.values()
        _local_one = cls()
        for key in keys:
            assert key in _local_one._fields
        names = _local_one.get_names()
        where_place = ' AND '.join(['%s = %%s' % key for key in keys])
        sql = '''
        SELECT %s
        FROM %s
        WHERE %s
        ''' % (', '.join(names), _local_one._table_name, where_place)
        results = _db.fetchall(sql, tuple(values))
        if results is not None and len(results) > 0:
            return [cls(x, names) for x in results]
        else:
            return None

    @classmethod
    def get_one(cls, condition):
        results = cls.get_multi(condition)
        if results is None:
            return None
        else:
            return results[0]

class DBClassBaseLoad(object):
    @staticmethod
    def dumps(obj):
        return obj

    @staticmethod
    def loads(obj):
        return obj


class utf8_json(DBClassBaseLoad):
    @staticmethod
    def dumps(obj):
        return json.dumps(obj, ensure_ascii=False)

    @staticmethod
    def loads(obj):
        return json.loads(obj)


class str_load(DBClassBaseLoad):
    @staticmethod
    def loads(obj):
        return str(obj)

class Character(DBClass):
    """
    角色数据类
    """
    table_name = 't_character'
    fields = 'character_id, name, auth_apis, create_time, update_time, status'
    info_list = ['character_id', 'name', 'auth_apis']
    field_parses = {
        'create_time': str_load,
        'update_time': str_load,
    }

    default_values = {
        'status': 1,
    }


def get_character_by_name(name: str):
    return Character.get_one({'name': name, 'status': 1})


def get_character_by_id(character_id: int):
    return Character.get_one({'character_id': character_id, 'status': 1})


def get_all_character():
    return Character.get_multi({'status': 1})

if __name__ == '__main__':
    print(get_all_character())