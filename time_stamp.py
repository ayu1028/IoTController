import json
import datetime
import time
import os

# ファイル名
FILE_NAME = "static/time_stamp.json"

def load_time_data(file_path):
    """
    time_stamp.jsonファイルを開き、JSONデータを読み込む。
    ファイルが存在しないか、空の場合は空の辞書を返す。

    Args:
        file_path (str): JSONファイルのパス。

    Returns:
        dict: 読み込んだJSONデータまたは空の辞書。
    """
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # キーの存在とフォーマットを簡易チェック
            if "time_stamp" in data and "time_int" in data:
                 return data
            else:
                 return {} # フォーマットが不正なら空として扱う
    except json.JSONDecodeError:
        print(f"警告: {file_path} は有効なJSONファイルではありません。空のデータとして扱います。")
        return {}
    except Exception as e:
        print(f"ファイルの読み込み中にエラーが発生しました: {e}")
        return {}


def save_time_data(file_path, data):
    """
    指定されたデータをJSONファイルに保存する。

    Args:
        file_path (str): 保存するJSONファイルのパス。
        data (dict): 保存するデータ。
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"ファイルの保存中にエラーが発生しました: {e}")


def update_time_loop():
    """
    時刻を監視し、10秒ごとにtime_stamp.jsonを更新するメインループ。
    KeyboardInterruptで終了する。
    """
    time_data = load_time_data(FILE_NAME)

    # time_dataが空の場合、初期値を設定
    if not time_data:
        time_data = {"time_stamp": "00:00", "time_int": 0}
        print("初期データを設定しました:", time_data)
        save_time_data(FILE_NAME, time_data)

    print("時刻の監視を開始します。(Ctrl+Cで終了)")

    try:
        while True:
            # 現在時刻を取得
            now = datetime.datetime.now()
            current_time_str = now.strftime("%H:%M")
            
            # time_int を計算
            if current_time_str == "00:00":
                time_int = 0
            else:
                time_int = now.hour * 60 + now.minute

            # データが更新されたかチェック
            if time_data.get("time_stamp") != current_time_str or \
               time_data.get("time_int") != time_int:
                
                # time_dataを更新
                time_data["time_stamp"] = current_time_str
                time_data["time_int"] = time_int

                # time_stamp.jsonを更新
                save_time_data(FILE_NAME, time_data)
                print(f"ファイルを更新しました: {time_data}")
            else:
                print(f"時刻 {current_time_str} - 変更なし")

            # 10秒待機
            time.sleep(10)

    except KeyboardInterrupt:
        print("\nプログラムを終了します。")

# メインプログラムの実行
if __name__ == "__main__":
    update_time_loop()