from PIL import Image
import sys
import os

def convert_jfif_to_jpeg(input_file, output_file):
    with Image.open(input_file) as img:
        img = img.convert("RGB")
        img.save(output_file, "JPEG")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python convert_jfif.py <input.jfif>")
        sys.exit(1)
    input_file = sys.argv[1]
    base, _ = os.path.splitext(input_file)
    output_file = base + ".jpg"
    convert_jfif_to_jpeg(input_file, output_file)
    print(f"{input_file} を {output_file} に変換しました。")