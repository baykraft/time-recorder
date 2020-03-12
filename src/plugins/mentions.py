from slackbot.bot import listen_to
from slackbot.dispatcher import Message
from sqlalchemy import desc

from plugins import dateutils, stringutils
from plugins.models import Session, TimeRecord, User
import re
import logging


@listen_to(r'(モ[ー〜]+ニン|も[ー〜]+にん|おっは|おは|へろ|はろ|ヘロ|ハロ|hi|hello|morning|出勤)')
def sign_in(message: Message, *something):
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
    :type message: Message
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
    try:
        # ユーザ情報を登録
        user_record: User = session.query(User).filter(
            User.user == user
        ).first()
        if user_record:
            user_record.real_name = message.user['real_name']
        else:
            session.add(User(user, message.user['real_name']))

        # 勤怠記録を登録
        filtered: TimeRecord = session.query(TimeRecord).filter(
            TimeRecord.user == user,
            TimeRecord.date == date).first()
        if filtered:
            filtered.start_time = time
        else:
            record: TimeRecord = TimeRecord(user, date)
            latest: TimeRecord = session.query(TimeRecord).filter(
                TimeRecord.user == user
            ).order_by(desc(TimeRecord.date)).first()
            if latest:
                record.customer = latest.customer
            record.start_time = time
            session.add(record)

        now = "{0:%Y/%m/%d %H:%M}".format(date_time)
        message.reply(f'おはようございます ({now})')

    except Exception as e:
        session.rollback()
        logging.error(e)
    finally:
        if session.is_active:
            session.commit()
        session.close()


@listen_to(r'(バ[ー〜ァ]*イ|ば[ー〜ぁ]*い|おやすみ|お[つっ]ー|おつ|さらば|お先|お疲|帰|乙|bye|night|(c|see)\s*(u|you)|退勤|ごきげんよ|グ[ッ]?バイ|さようなら)')
def sign_out(message: Message, *something):
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
    :type message: Message
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
    try:
        # ユーザ情報を登録
        user_record: User = session.query(User).filter(
            User.user == user
        ).first()
        if user_record:
            user_record.real_name = message.user['real_name']
        else:
            session.add(User(user, message.user['real_name']))

        # 勤怠記録を登録
        filtered: TimeRecord = session.query(TimeRecord).filter(
            TimeRecord.user == user,
            TimeRecord.date == date).first()
        if filtered:
            filtered.end_time = time
        else:
            record: TimeRecord = TimeRecord(user, date)
            latest: TimeRecord = session.query(TimeRecord).filter(
                TimeRecord.user == user
            ).order_by(desc(TimeRecord.date)).first()
            if latest:
                record.customer = latest.customer
            record.end_time = time
            session.add(record)

        now = "{0:%Y/%m/%d %H:%M}".format(date_time)
        message.reply(f'お疲れ様でした ({now})')

    except Exception as e:
        session.rollback()
        logging.error(e)
    finally:
        if session.is_active:
            session.commit()
        session.close()


@listen_to(r'(休|やす(ま|み|む)|休暇)')
def off(message: Message, *something):
    """
    休暇メッセージ受信サービスです。
    以下のようなメッセージに反応します。

        * 休
        * やすま
        * やすみ
        * やすむ
        * 休暇

    メッセージには日付を指定することが可能です。日付を指定しない場合は現在日付で記録されます。
    「有休」として記録されます。

        休み 2020/1/29
        休み 1/29
        休み

    メッセージには午前および午後を指定することも可能です。
    午前が指定された場合は「有休(AM)」、午後が指定された場合は「有休(PM)」として記録されます。

        午前休み
        午後休み
        am休み
        pm休み

    また、シングルクォートで文字列を括ることでメモ情報を記録することができます。

        休み 1/30 "ここがメモとして記録される"
        休み "ここがメモとして記録される"

    :param message: メッセージオブジェクト
    :type message: Message
    :param something: メッセージタプル
    :type something: tuple
    :return: なし
    :rtype: None
    """
    text = message.body['text']
    date_time = dateutils.normalize_datetime(text)
    date = date_time.date()
    user = message.body['user']

    # 勤休を判定
    # テキストに午前が含まれている場合は「有休（AM)」、
    # 午後が含まれている場合は「有休（PM)」、
    # それ以外は「有休」とする。
    kind = 10
    if dateutils.is_am(text):
        kind = 11
    elif dateutils.is_pm(text):
        kind = 12

    note = text
    pattern = re.compile('"(.+)"')
    matches = pattern.search(stringutils.translate2han(text))
    if matches:
        groups = matches.groups()
        note = groups[0]

    session = Session()
    try:
        # ユーザ情報を登録
        user_record: User = session.query(User).filter(
            User.user == user
        ).first()
        if user_record:
            user_record.real_name = message.user['real_name']
        else:
            session.add(User(user, message.user['real_name']))

        # 勤怠記録を登録
        filtered: TimeRecord = session.query(TimeRecord).filter(
            TimeRecord.user == user,
            TimeRecord.date == date).first()
        if filtered:
            filtered.start_time = None
            filtered.end_time = None
            filtered.kind = kind
            filtered.note = note
        else:
            record: TimeRecord = TimeRecord(user, date)
            latest: TimeRecord = session.query(TimeRecord).filter(
                TimeRecord.user == user
            ).order_by(desc(TimeRecord.date)).first()
            if latest:
                record.customer = latest.customer
            record.start_time = None
            record.end_time = None
            record.kind = kind
            record.note = note
            session.add(record)

        now = "{0:%Y/%m/%d}".format(date_time)
        if 11 == kind:
            message.reply(f'{now} を有休(AM)として登録しました')
        elif 12 == kind:
            message.reply(f'{now} を有休(PM)として登録しました')
        else:
            message.reply(f'{now} を有休として登録しました')

    except Exception as e:
        session.rollback()
        logging.error(e)
    finally:
        if session.is_active:
            session.commit()
        session.close()
