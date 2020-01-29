import sqlalchemy as sa
import os
import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = sa.create_engine(os.environ.get('DATABASE_URL'))


class Timesheet(Base):
    __tablename__ = 'timesheet'
    __table_args__ = (sa.UniqueConstraint("user", "date"), {})
    timesheetid = sa.Column('timesheetid', sa.Integer, primary_key=True, autoincrement=True)
    user: str = sa.Column('user', sa.String(9), nullable=False)
    date: datetime.date = sa.Column('date', sa.DATE, nullable=False)
    start_time: datetime.time = sa.Column('start_time', sa.TIME, nullable=True)
    end_time: datetime.time = sa.Column('end_time', sa.TIME, nullable=True)
    note: str = sa.Column('note', sa.String, nullable=True)

    def __init__(self, user, date, start_time, end_time, note):
        self.user = user
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.note = note

    def __repr__(self):
        return '<Timesheet({}, {}, {}, {}, {}, {})>'.format(
            self.timesheetid, self.user, self.date, self.start_time, self.end_time, self.note)


Base.metadata.create_all(engine)
