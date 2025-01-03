from passlib.hash import sha512_crypt

def solve_password(password_hash: str) -> str:
    salt = password_hash.split('$')[2]
    # パスワード候補を1つずつ取り出し、ソルトを付加してハッシュ化する
    pass_dictionary = open('dictionary.txt', 'r')
    cnt = 0
    for password in pass_dictionary:
        password = password.rstrip('\n')

        # Modular Crypt Format のハッシュ値を生成
        # hashlib, cryptモジュールでハッシュ値を生成すると、問題文のハッシュ値フォーマットと異なるため、passlibモジュールを使用する
        hashed = sha512_crypt.hash(password, rounds=5000, salt=salt)

        if hashed == password_hash:
            return password
    return None

if __name__ == '__main__':    
    # ./problem.txtファイルを読み込み、1行ずつハッシュ値からパスワードを推測する
    file = open('problem.txt', 'r')
    for line in file:
        username = line.split(':')[0]
        password_hash = line.split(':')[1]

        # ハッシュ値が一致するパスワードを探す
        password = solve_password(password_hash)
        print(username, password)



