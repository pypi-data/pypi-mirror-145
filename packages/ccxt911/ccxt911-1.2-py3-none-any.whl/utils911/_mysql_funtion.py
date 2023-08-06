
from sqlalchemy import create_engine        #数据库

def create_sqlalchemy_engine(user, password, host, database):
    """
    创建sqlalchemy 引擎
    :param user: 用户名
    :param password: 密码
    :param host: hostIP
    :param database: 数据库名
    :return:返回引擎
    """
    engine = create_engine("mysql+pymysql://%s:%s@%s:3306/%s?charset=utf8" % (user, password, host, database))
    return engine
