import struct
import random, time
from randcrack import RandCrack


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


# encrypt.keyに使われている乱数を4 byteリストに追加
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