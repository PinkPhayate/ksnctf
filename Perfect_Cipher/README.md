# Perfect Cipher

## 問題理解
問題に添付されているZIPファイルを解凍すると、以下のファイルが出てきた。
```
% ls
encrypt.cpp	encrypt.enc	flag.enc	mt19937ar.cpp	mt19937ar.h
```

encrypt.cppを読むと、ファイルを暗号化する関数と復号する関数が用意されている。
プログラムを読んだところ、seedファイルが必要だとわかったため、コマンドでseedファイルを作成し、`encrypt.cpp`を実行できることを確認。


```
# seed作成コマンド
└─# dd if=/dev/urandom of=seed bs=4 count=1024
1024+0 records in
1024+0 records out
4096 bytes (4.1 kB, 4.0 KiB) copied, 0.0456472 s, 89.7 kB/s

# プログラムをコンパイルして実行
└─# g++ -O2 -o encrypt.exe encrypt.cpp mt19937ar.cpp

└─# ./encrypt.exe

└─# ls -ltr
total 272
-rw-r--r-- 1 root root  2928 Apr 26  2005 mt19937ar.h
-rw-r--r-- 1 root root  5996 Apr 26  2005 mt19937ar.cpp
-rw-r--r-- 1 root root 78560 Jun  3  2012 flag.enc
-rw-r--r-- 1 root root 86165 Jan 13 11:39 encrypt.zip
-rw-r--r-- 1 root root  2600 Jan 18 12:31 encrypt.cpp
-rwxr-xr-x 1 root root 71624 Jan 18 12:31 encrypt.exe
-rw-r--r-- 1 root root  4096 Jan 18 12:39 seed
-rw-r--r-- 1 root root  2604 Jan 18 12:39 encrypt.enc
-rw-r--r-- 1 root root  2600 Jan 18 12:39 encrypt.key
-rw-r--r-- 1 root root  2600 Jan 18 12:39 encrypt_dec.cpp

# 差分がないので復元できたっぽい。
└─# diff -u encrypt.cpp encrypt_dec.cpp

```
復元できたことから、encrypt.cppは暗号化,復号する関数が用意されたプログラムと断定。  
プログラム自体には問題はなさそう。


## 本題

encrpt.cppプログラムを読んだところ以下のことがわかた。
1. encrypt.cppを乱数(mt19937)を使ってencrypt.encというファイルに暗号化、利用した乱数はencrypt.keyに保存  
`encrypt("encrypt.cpp", "encrypt.enc", "encrypt.key");`
2. encrypt.encというファイルを利用した乱数が記録されているencrypt.keyを使って復号し、encrypt_dec.cppというファイルに保存  
`decrypt("encrypt_dec.cpp", "encrypt.enc", "encrypt.key");`

cppプログラムを読んでいくと、暗号化・復号ともに、対象ファイルと生成した乱数を4byteずつXORしていることがわかった。すなわち、
- cppプログラムを使わなくても、対象ファイルと乱数ファイル(.key)があれば、XORして暗号化ファイル(.enc)は作れる。
- 対象ファイルと暗号化ファイル(.enc)から、暗号化に使用した乱数ファイル(.key)を生成できる。


上記より、以下を推測。
- encrypt.cppとencrypt.encから暗号化の際に利用した乱数一覧(encrypt.key)を生成できる
- flag.encとflag.keyという2つのファイルがあれば、flag.jpgは生成できる(そこにフラグがありそう)

## mt19937には脆弱性がある
mt19937には脆弱性があり、「randcrack」というpythonのモジュールで、これまで出力された乱数を元に、その先に出力されるであろう乱数を予測できるらしい。
```
apt install python3 python3-pip -y
```

### 補足
問題を解く際には、KaliLinuxイメージ上で行うようにしている。
pythonパッケージのインストールが、　普段Macでいつもやっているようにはインストールできなかったのでメモ。
```
// 以下コマンドはいずれもうまくいかなかった。
# pip3 install randcrack
# pip3 install python3-randcrack
```
上記コマンドを実行した時に、venvを使ってみろよ、というメッセージのことだったので使ってみたらインストールできた。

> If you wish to install a non-Kali-packaged Python package,
create a virtual environment using python3 -m venv path/to/venv.
Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
sure you have pypy3-venv installed.

```
└─# python3 --version
Python 3.12.8
$ python3 -m venv venv 
$ source venv/bin/activate


└─# pip install randcrack
Collecting randcrack
  Downloading randcrack-0.2.0-py3-none-any.whl.metadata (3.9 kB)
Downloading randcrack-0.2.0-py3-none-any.whl (5.7 kB)
Installing collected packages: randcrack
Successfully installed randcrack-0.2.0
```




## encrypt.keyを生成する
```python
def remove_first_4bits(input_file, output_file):
    with open(input_file, "rb") as f:
        data = f.read()
    
    if len(data) == 0:
        print("Error: File is empty.")
        return
    
    # 先頭バイトの下位4ビットのみ残す
    remaining_data = data[4:]  # 残りのデータ
        
    with open(output_file, "wb") as f:
        f.write(remaining_data)
    
    print(f"Processed file saved as {output_file}")

def xor_binary_files(file1, file2, output_file):
    with open(file1, "rb") as f1, open(file2, "rb") as f2, open(output_file, "wb") as out:
        while True:
            b1 = f1.read()
            b2 = f2.read()
            if not b1 or not b2:
                break
            xor_result = bytes(a ^ b for a, b in zip(b1, b2))
            out.write(xor_result)

# encrypt.keyを作成する
remove_first_4bits("encrypt.enc", "encrypt_minus4.enc")
xor_binary_files("encrypt_minus4.enc", "encrypt.cpp", "encrypt.key")

```

## flag.keyを生成するプログラム設計


cppプログラム中の`fwrite(&k, 4, 1, fk);`というメソッドで4byteずつ乱数を書き込んでいて、694回乱数が書かれている。(2776/4)。  
694の整数があれば、その先の乱数も予測できるはず.
```
└─# wc --bytes encrypt.key
2776 encrypt.key

# 先頭から20byte表示する
└─# od -N20 encrypt.key
0000000 101653 132274 075666 141253 161236 116476 000016 043026
0000020 137534 022501
0000024

# 16進数で表示すると1山が4byteになるっぽい。
└─# od -t x -N 20 encrypt.key
0000000 b4bc83ab c2ab7bb6 9d3ee29e 4616000e
0000020 2541bf5c
0000024
```

flag.encは78560byteで、先頭の4byteはファイルの長さを書いているはずなので、78556byte ->
19639個の乱数を生成して、バイナリファイルとして保存しするプログラムを用意。

```
# encrypt.keyを読み込み
data = []
with open('encrypt.key', 'rb') as f:
    for rand_bytes in iter(lambda: f.read(4), b''):
        # print(struct.unpack('I', rand_bytes)[0])
        data.append(struct.unpack('I', rand_bytes)[0])



# 乱数を予測するための学習材料として、encrypt.keyにある乱数624個を渡す
rc = RandCrack()
for i in range(624):
	rc.submit(data[i])

# encrypt.keyに記録されている乱数と予測した乱数が一致するか確認
for j in range(624, len(data)):
    predict_value = rc.predict_randrange(0, 4294967295)
    # fileから読み出した乱数と予測した乱数が一致するはず
    # print("Rand value in file: {}\nCracker result: {}"
    #     .format(data[j], predict_value))



# flag.keyを予測して作成する
with open("flag.key", "wb") as fk:
    for k in range(19639):
        predict_value = rc.predict_randrange(0, 4294967295)
        fk.write(struct.pack("I", predict_value))
        # 16進数に変換してflag.keyファイルに保存

# flag.encを4yte削ってflag.jpgを生成する
remove_first_4bits("flag.enc", "flag_minus4.enc")
xor_binary_files("flag.key", "flag_minus4.enc", "flag.jpg")
```


プログラム実行後、作成できることを確認。
flag.encの中にFLAGを発見(見つける方法難しかった)
```
└─# wc --byte flag.enc
78560 flag.enc
```





