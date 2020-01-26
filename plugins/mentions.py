from slackbot.bot import listen_to

from plugins import dateutils


@listen_to(r'(モ[ー〜]+ニン|も[ー〜]+にん|おっは|おは|へろ|はろ|ヘロ|ハロ|hi|hello|morning|出勤)')
def sign_in(message, *something):
    date_time = dateutils.normalize_datetime(message.body['text'])
    now = "{0:%Y/%m/%d %H:%M}".format(date_time)
    message.reply(f'おはようございます ({now})')


@listen_to(r'(バ[ー〜ァ]*イ|ば[ー〜ぁ]*い|おやすみ|お[つっ]ー|おつ|さらば|お先|お疲|帰|乙|bye|night|(c|see)\s*(u|you)|退勤|ごきげんよ|グ[ッ]?バイ)')
def sign_out(message, *something):
    date_time = dateutils.normalize_datetime(message.body['text'])
    now = "{0:%Y/%m/%d %H:%M}".format(date_time)
    message.reply(f'お疲れ様でした ({now})')


@listen_to(r'(休|やす(ま|み|む)|休暇)')
def off(message, *something):
    date_time = dateutils.normalize_datetime(message.body['text'])
    now = "{0:%Y/%m/%d}".format(date_time)
    message.reply(f'{now} を休暇として登録しました')
