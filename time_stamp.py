import json
import time
from datetime import datetime

FILE_PATH = "static/time_stamp.json"

def get_minutes_from_midnight(time_str_hhmm):
    """
    hh:mm形式の時刻文字列を深夜0時からの経過分数に変換します。
    """
    try:
        h, m = map(int, time_str_hhmm.split(':'))
        if not (0 <= h <= 23 and 0 <= m <= 59):
            # このエラーは通常、呼び出し前のバリデーションで捕捉されるべきです。
            raise ValueError("Time values are out of range (00-23 for hour, 00-59 for minute).")
        return h * 60 + m
    except ValueError as e:
        # hh:mm 形式でない場合や、数値変換に失敗した場
        print(f"Error parsing time string '{time_str_hhmm}': {e}")
        raise  # エラーを再送出して上位で処理させるか、デフォルト値を返す

def main():
    try:
        while True:
            time_data = {}
            # 1. time_stamp.jsonファイルを開き、変数time_dataにjsonデータを格納する。
            #    なければ空の辞書を格納する。
            try:
                with open(FILE_PATH, 'r', encoding='utf-8') as f:
                    time_data = json.load(f)

                # JSONデータのフォーマット検証
                if not isinstance(time_data, dict) or \
                    "time_stamp" not in time_data or not isinstance(time_data.get("time_stamp"), str) or \
                    "time_int" not in time_data or not isinstance(time_data.get("time_int"), int):
                    print(f"警告: {FILE_PATH} のデータ形式が不正か、型が間違っています。初期化します。")
                    time_data = {} # 初期化をトリガーするためにリセット
                else:
                    # time_stamp のフォーマット ("hh:mm") を厳密に検証
                    try:
                        h_check, m_check = map(int, time_data["time_stamp"].split(':'))
                        if not (0 <= h_check <= 23 and 0 <= m_check <= 59):
                            raise ValueError("時刻の値が範囲外です。")
                    except ValueError:
                        print(f"警告: {FILE_PATH} の time_stamp ('{time_data['time_stamp']}') の形式が不正です。初期化します。")
                        time_data = {} # 初期化をトリガーするためにリセット
            except FileNotFoundError:
                print(f"{FILE_PATH} が見つかりません。新規に作成します。")
                # time_data は {} のまま
            except json.JSONDecodeError:
                print(f"{FILE_PATH} のJSONデコードに失敗しました。初期化します。")
                # time_data は {} のまま

            current_dt = datetime.now()
            current_time_hhmm_str = current_dt.strftime("%H:%M")

            # 2. time_dataが空の場合、"time_stamp"に現在時刻、"time_int"に0を設定する。
            if not time_data: # ファイルが存在しない、JSONエラー、またはバリデーション失敗の場合
                time_data["time_stamp"] = current_time_hhmm_str
                time_data["time_int"] = 0
                print(f"データが初期化されました: {time_data}")
            # この時点で、time_data にはロードされた (そして検証された) データ、
            # または新しく初期化されたデータが含まれています。
            stored_time_str = time_data["time_stamp"]
            current_time_int_from_data = time_data["time_int"]

            # 3. "time_stamp"に保存されている時刻と現在時刻の差を10秒ごとに取得し、
            #    差があればその差を分単位の整数として"time_int"に加算する。
            try:
                stored_total_minutes = get_minutes_from_midnight(stored_time_str)
            except ValueError:
                # stored_time_str のパースに失敗した場合 (初期化直後や予期せぬエラー)
                # 安全のため、現在の時刻で再初期化する
                time_data["time_stamp"] = current_time_hhmm_str
                time_data["time_int"] = 0
                stored_total_minutes = get_minutes_from_midnight(current_time_hhmm_str)
                current_time_int_from_data = 0

            current_total_minutes = current_dt.hour * 60 + current_dt.minute

            minute_diff = current_total_minutes - stored_total_minutes

            new_time_int = current_time_int_from_data

            if minute_diff != 0: # 分単位での差がある場合のみ処理
                if minute_diff > 0:
                    new_time_int += minute_diff
                else: # minute_diff < 0 (現在時刻が保存時刻より前。日付変更や時刻の巻き戻しなど)
                    new_time_int += (24 * 60) + minute_diff # 1日の総分数を加算してから負の差分を加える

            # 4. time_intの値が256以上になった場合、255以下になるまで256を引き続ける。
            while new_time_int >= 256:
                new_time_int -= 256

            # 5. "time_stamp"と"time_int"の値を更新してtime_stamp.jsonファイルを更新する。
            time_data["time_stamp"] = current_time_hhmm_str # 次のサイクルのために現在時刻に更新
            time_data["time_int"] = new_time_int
            try:
                with open(FILE_PATH, 'w', encoding='utf-8') as f:
                    json.dump(time_data, f, indent=4, ensure_ascii=False)
                current_log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{current_log_time}] {FILE_PATH} が更新されました: {time_data}")
            except IOError as e:
                print(f"{FILE_PATH} への書き込みエラー: {e}")

            time.sleep(10)

    except KeyboardInterrupt:
        print("\nプログラムがユーザーによって終了されました (KeyboardInterrupt)。")

if __name__ == "__main__":
    main()

