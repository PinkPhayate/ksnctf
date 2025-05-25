from PIL import Image

def convert_jfif_to_jpeg(input_file, output_file):
    # JFIFファイルを開く
    with Image.open(input_file) as img:
        # RGB形式に変換（必要に応じて）
        img = img.convert("RGB")
        
        # JPEG形式で保存
        img.save(output_file, "JPEG")

convert_jfif_to_jpeg("39.jfif", "39.jpg")
convert_jfif_to_jpeg("40.jfif", "40.jpg")