from slackbot.bot import listen_to

from plugins import dateutils, stringutils
from plugins.models import engine, Timesheet
from sqlalchemy.orm import sessionmaker
import re

Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)


@listen_to(r'(モ[ー〜]+ニン|も[ー〜]+にん|おっは|おは|へろ|はろ|ヘロ|ハロ|hi|hello|morning|出勤)')
def sign_in(message, *something):
    date_time = dateutils.normalize_datetime(message.body['text'])
    date = date_time.date()
    time = date_time.time()
    user = message.body['user']

    session = Session()
    filtered: Timesheet = session.query(Timesheet).filter(Timesheet.user == user, Timesheet.date == date).first()
    if filtered:
        filtered.start_time = time
    else:
        session.add(Timesheet(user, date, time, None, None))
    session.commit()
    session.close()

    now = "{0:%Y/%m/%d %H:%M}".format(date_time)
    message.reply(f'おはようございます ({now})')


@listen_to(r'(バ[ー〜ァ]*イ|ば[ー〜ぁ]*い|おやすみ|お[つっ]ー|おつ|さらば|お先|お疲|帰|乙|bye|night|(c|see)\s*(u|you)|退勤|ごきげんよ|グ[ッ]?バイ)')
def sign_out(message, *something):
    date_time = dateutils.normalize_datetime(message.body['text'])
    date = date_time.date()
    time = date_time.time()
    user = message.body['user']

    session = Session()
    filtered: Timesheet = session.query(Timesheet).filter(Timesheet.user == user, Timesheet.date == date).first()
    if filtered:
        filtered.end_time = time
    else:
        session.add(Timesheet(user, date, None, time, None))
    session.commit()
    session.close()

    now = "{0:%Y/%m/%d %H:%M}".format(date_time)
    message.reply(f'お疲れ様でした ({now})')


@listen_to(r'(休|やす(ま|み|む)|休暇)')
def off(message, *something):
    text = message.body['text']
    date_time = dateutils.normalize_datetime(text)
    date = date_time.date()
    user = message.body['user']

    note = text
    pattern = re.compile('"(.+)"')
    matches = pattern.search(stringutils.translate2han(text))
    if matches:
        groups = matches.groups()
        print(groups)
        note = groups[0]

    session = Session()
    filtered: Timesheet = session.query(Timesheet).filter(Timesheet.user == user, Timesheet.date == date).first()
    if filtered:
        filtered.start_time = None
        filtered.end_time = None
        filtered.note = note
    else:
        session.add(Timesheet(user, date, None, None, note))
    session.commit()
    session.close()

    now = "{0:%Y/%m/%d}".format(date_time)
    message.reply(f'{now} を休暇として登録しました')
