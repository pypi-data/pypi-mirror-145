# -*- coding: utf-8 -*-
# @Time   : 2021/4/22 下午3:08
# @Author : wu

"""
pip install sqlalchemy
"""

# 导入:
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建对象的基类:
Base = declarative_base()

DBS = {
    "local": "mysql+pymysql://root:root@localhost:3306",
    "42": "mysql+pymysql://root:123456@192.168.1.42:3306",
}


class SqlAlchemy:
    def __init__(self, db_dns=DBS["42"], db="device"):
        # 初始化数据库连接，echo=True是开启调试，这样当我们执行文件的时候会提示相应的文字。
        db_dns = f"{db_dns}/{db}"
        self.engine = create_engine(db_dns, echo=False)
        self.session = self.create_session()

    def create_table(self, _Base=None):
        """创建表"""
        if not _Base:
            _Base = Base
        _Base.metadata.create_all(self.engine)

    def create_session(self):
        """
        创建 session
        获取session，然后把对象添加到session，最后提交并关闭。DBSession对象可视为当前数据库连接。
        Returns:

        """
        # 创建DBSession类型:
        DB_Session = sessionmaker(bind=self.engine)
        # 创建session对象:
        session = DB_Session()
        return session

    def add_new(self, data: dict or list = None):
        """
        如果存在相同的主键则抛出异常
        :param data:
        :return:
        """
        data = data if isinstance(data, list) else [data]
        self.session.add_all(data)  # 添加多个
        # 提交即保存到数据库:
        self.session.commit()
        # 关闭session:
        self.session.close()

    def query_one(self, table, condition=None):
        result = self.session.query(table).filter(condition).one_or_none()
        return result.to_dict() if result else None

    def query_all(self, table, condition=None):
        if condition is None:
            result = self.session.query(table).all()
        else:
            result = self.session.query(table).filter(condition).all()
        res_list = [i.to_dict() for i in result]
        return res_list

    def insert(self, table: declarative_base, data=None):
        if not data:
            logger.warning(f"Data is None: {data}")
            return
        insert_stmt = insert(table).values(**data)

        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**data)
        self.session.execute(on_duplicate_key_stmt)
        self.session.commit()

    def del_data(self, table: declarative_base, condition=None):
        users = self.query_all(table, condition)
        [self.session.delete(u) for u in users]
        self.session.commit()

    def is_exist_table(self, table_name: str):
        ret = self.engine.dialect.has_table(self.engine, table_name)
        if ret:
            logger.info(f'Yes! Table "machine_devices" does exist')
        else:
            logger.info(f'No! Table "machine_devices" does not exist')
        return ret


if __name__ == "__main__":
    obj = SqlAlchemy()
    obj.create_table()
    # obj.insert()
