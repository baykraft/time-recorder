import sqlalchemy as sa
import os
import datetime
from sqlalchemy import exc, event
from sqlalchemy.pool import Pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = sa.create_engine(os.environ.get('DATABASE_URL'))
Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)


@event.listens_for(Pool, 'checkout')
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    """
    プールされているコネクションが有効かどうか判定します。

    :param dbapi_connection: DBAPI connection
    :param connection_record: connection record
    :param connection_proxy: connection proxy
    :return: None
    """
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute('SELECT 1')
    except Exception as e:
        raise exc.DisconnectionError(e)
    finally:
        cursor.close()


class TimeRecord(Base):
    """
    勤怠記録
    """
    __tablename__ = 'time_records'
    __table_args__ = (sa.UniqueConstraint('user', 'date'), {})
    time_record_id: int = sa.Column('time_record_id', sa.Integer, primary_key=True, autoincrement=True)
    user: str = sa.Column('user', sa.String(9), nullable=False)
    date: datetime.date = sa.Column('date', sa.DATE, nullable=False)
    start_time: datetime.time = sa.Column('start_time', sa.TIME, nullable=True)
    end_time: datetime.time = sa.Column('end_time', sa.TIME, nullable=True)
    note: str = sa.Column('note', sa.String, nullable=True)
    kind: int = sa.Column('kind', sa.Integer, nullable=False, default=0)
    customer: str = sa.Column('customer', sa.String, nullable=True)

    def __init__(self, user: str, date: datetime.date):
        self.user = user
        self.date = date

    def __repr__(self):
        return '<TimeRecord({}, {}, {}, {}, {}, {}, {}, {})>'.format(
            self.time_record_id,
            self.user, self.date, self.start_time, self.end_time, self.note, self.kind, self.customer)


class BreakTime(Base):
    """
    休憩時間
    """
    __tablename__ = 'break_times'
    break_time_id: int = sa.Column('break_time_id', sa.Integer, primary_key=True, autoincrement=True)
    user: str = sa.Column('user', sa.String(9), nullable=False)
    year: int = sa.Column('year', sa.Integer, nullable=False)
    month: int = sa.Column('month', sa.Integer, nullable=False)
    customer: str = sa.Column('customer', sa.String, nullable=False)
    start_time: datetime.time = sa.Column('start_time', sa.TIME, nullable=False)
    end_time: datetime.time = sa.Column('end_time', sa.TIME, nullable=False)

    def __init__(self,
                 user: str,
                 year: int,
                 month: int,
                 customer: str,
                 start_time: datetime.time,
                 end_time: datetime.time):
        self.user = user
        self.year = year
        self.month = month
        self.customer = customer
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<BreakTime({}, {}, {}, {}, {}, {}, {})>'.format(
            self.break_time_id, self.user, self.year, self.month, self.customer, self.start_time, self.end_time)


class FixedTime(Base):
    """
    所定時間
    """
    __tablename__ = 'fixed_times'
    fixed_time_id: int = sa.Column('fixed_time_id', sa.Integer, primary_key=True, autoincrement=True)
    user: str = sa.Column('user', sa.String(9), nullable=False)
    year: int = sa.Column('year', sa.Integer, nullable=False)
    month: int = sa.Column('month', sa.Integer, nullable=False)
    customer: str = sa.Column('customer', sa.String, nullable=False)
    start_time: datetime.time = sa.Column('start_time', sa.TIME, nullable=False)
    end_time: datetime.time = sa.Column('end_time', sa.TIME, nullable=False)

    def __init__(self,
                 user: str,
                 year: int,
                 month: int,
                 customer: str,
                 start_time: datetime.time,
                 end_time: datetime.time):
        self.user = user
        self.year = year
        self.month = month
        self.customer = customer
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<FixedTime({}, {}, {}, {}, {}, {}, {})>'.format(
            self.fixed_time_id, self.user, self.year, self.month, self.customer, self.start_time, self.end_time)


Base.metadata.create_all(engine)
