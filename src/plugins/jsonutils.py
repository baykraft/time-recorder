def strip_to_none(json, key: str):
    """
    JSONオブジェクトからkeyに対する値を取得します。
    JSONオブジェクトにkeyが含まれていない場合はNoneを返却します。

    :param json: JSONオブジェクト
    :type json: dict
    :param key: キー
    :type key: str
    :return: keyに対する値、keyがJSONオブジェクトに含まれていない場合はNone
    :rtype: Any or None
    """
    return json[key] if key in json else None
