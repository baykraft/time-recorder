from slackbot.bot import listen_to

from plugins import dateutils, stringutils
from plugins.models import engine, Timesheet
from sqlalchemy.orm import sessionmaker
import re

Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)


@listen_to(r'(モ[ー〜]+ニン|も[ー〜]+にん|おっは|おは|へろ|はろ|ヘロ|ハロ|hi|hello|morning|出勤)')
def sign_in(message, *something):
    """
    出勤メッセージ受信サービスです。
    以下のようなメッセージに反応します。

        * モーニング
        * モ〜ニング
        * もーにんぐ
        * も〜にんぐ
        * おっは
        * おはよう
        * へろ
        * はろ
        * ヘロ
        * ハロ
        * hi
        * hello
        * morning
        * 出勤

    メッセージには日時を指定することが可能です。日時を指定しない場合は現在日時で記録されます。

        おはようございます 2020/1/29 9:00
        おはようございます 1/29 9:00
        おはようございます 1/29
        おはようございます

    :param message: メッセージオブジェクト
    :type message: slackbot.dispatcher.Message
    :param something: メッセージタプル
    :type something: tuple
    :return: なし
    :rtype: None
    """
    date_time = dateutils.normalize_datetime(message.body['text'])
    date = date_time.date()
    time = date_time.time()
    user = message.body['user']

    session = Session()
    filtered: Timesheet = session.query(Timesheet).filter(Timesheet.user == user, Timesheet.date == date).first()
    if filtered:
        filtered.start_time = time
    else:
        timesheet: Timesheet = Timesheet(user, date)
        timesheet.start_time = time
        session.add(timesheet)
    session.commit()
    session.close()

    now = "{0:%Y/%m/%d %H:%M}".format(date_time)
    message.reply(f'おはようございます ({now})')


@listen_to(r'(バ[ー〜ァ]*イ|ば[ー〜ぁ]*い|おやすみ|お[つっ]ー|おつ|さらば|お先|お疲|帰|乙|bye|night|(c|see)\s*(u|you)|退勤|ごきげんよ|グ[ッ]?バイ|さようなら)')
def sign_out(message, *something):
    """
    退勤メッセージ受信サービスです。
    以下のようなメッセージに反応します。

        * バイ
        * バーイ
        * バ〜イ
        * バァイ
        * ばい
        * ばーい
        * ば〜い
        * ばぁい
        * おやすみ
        * おつー
        * おっー
        * おつ
        * さらば
        * お先
        * お疲
        * 帰
        * 乙
        * bye
        * night
        * cu
        * c u
        * cyou
        * c you
        * seeu
        * see u
        * seeyou
        * see you
        * 退勤
        * ごきげんよ
        * グッバイ
        * グバイ
        * さようなら

    メッセージには日時を指定することが可能です。日時を指定しない場合は現在日時で記録されます。

        お疲れ様でした 2020/1/29 17:30
        お疲れ様でした 1/29 17:30
        お疲れ様でした 1/29
        お疲れ様でした

    :param message: メッセージオブジェクト
    :type message: slackbot.dispatcher.Message
    :param something: メッセージタプル
    :type something: tuple
    :return: なし
    :rtype: None
    """
    date_time = dateutils.normalize_datetime(message.body['text'])
    date = date_time.date()
    time = date_time.time()
    user = message.body['user']

    session = Session()
    filtered: Timesheet = session.query(Timesheet).filter(Timesheet.user == user, Timesheet.date == date).first()
    if filtered:
        filtered.end_time = time
    else:
        timesheet: Timesheet = Timesheet(user, date)
        timesheet.end_time = time
        session.add(timesheet)
    session.commit()
    session.close()

    now = "{0:%Y/%m/%d %H:%M}".format(date_time)
    message.reply(f'お疲れ様でした ({now})')


@listen_to(r'(休|やす(ま|み|む)|休暇)')
def off(message, *something):
    """
    休暇メッセージ受信サービスです。
    以下のようなメッセージに反応します。

        * 休
        * やすま
        * やすみ
        * やすむ
        * 休暇

    メッセージには日時を指定することが可能です。日時を指定しない場合は現在日時で記録されます。

        休み 2020/1/29 17:30
        休み 1/29 17:30
        休み 1/29
        休み

    また、シングルクォートで文字列を括ることでメモ情報を記録することができます。

        休み 1/30 "ここがメモとして記録される"
        休み "ここがメモとして記録される"

    :param message: メッセージオブジェクト
    :type message: slackbot.dispatcher.Message
    :param something: メッセージタプル
    :type something: tuple
    :return: なし
    :rtype: None
    """
    text = message.body['text']
    date_time = dateutils.normalize_datetime(text)
    date = date_time.date()
    user = message.body['user']

    note = text
    pattern = re.compile('"(.+)"')
    matches = pattern.search(stringutils.translate2han(text))
    if matches:
        groups = matches.groups()
        note = groups[0]

    session = Session()
    filtered: Timesheet = session.query(Timesheet).filter(Timesheet.user == user, Timesheet.date == date).first()
    if filtered:
        filtered.start_time = None
        filtered.end_time = None
        filtered.kind = 10  # 有休
        filtered.note = note
    else:
        timesheet: Timesheet = Timesheet(user, date)
        timesheet.start_time = None
        timesheet.end_time = None
        timesheet.kind = 10  # 有休
        timesheet.note = note
        session.add(timesheet)
    session.commit()
    session.close()

    now = "{0:%Y/%m/%d}".format(date_time)
    message.reply(f'{now} を休暇として登録しました')
