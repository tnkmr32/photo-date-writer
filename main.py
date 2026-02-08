#!/usr/bin/env python3
"""
Photo Date Writer - MVP版
JPGファイルのEXIFから撮影日時を読み取り、画像右下に日付を印字するシンプルなツール
"""

import sys
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
from datetime import datetime


def get_date_from_exif(image):
    """
    画像のEXIFデータから撮影日時を取得する
    
    Args:
        image: PIL Imageオブジェクト
        
    Returns:
        datetime: 撮影日時（取得できない場合はNone）
    """
    try:
        exif_data = image._getexif()
        if not exif_data:
            return None
        
        # EXIFタグから撮影日時を探す
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name == 'DateTimeOriginal':
                # EXIF日時フォーマット: "YYYY:MM:DD HH:MM:SS"
                return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        
        return None
    except Exception as e:
        print(f"EXIF読み取りエラー: {e}")
        return None


def add_date_to_image(input_path, output_path):
    """
    画像に日付を印字して保存する
    
    Args:
        input_path: 入力画像のパス
        output_path: 出力画像のパス
    """
    try:
        # 画像を開く
        img = Image.open(input_path)
        
        # EXIFから日付を取得
        date = get_date_from_exif(img)
        if not date:
            print("エラー: EXIFから撮影日時を取得できませんでした")
            sys.exit(1)
        
        # 日付を YYYY/MM/DD 形式にフォーマット
        date_str = date.strftime('%Y/%m/%d')
        
        # RGB モードに変換（必要に応じて）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 描画用オブジェクトを作成
        draw = ImageDraw.Draw(img)
        
        # フォント設定
        font_size = 32
        try:
            # システムフォントを使用（macOS/Linux）
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            try:
                # Windowsの場合
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # デフォルトフォントを使用
                font = ImageFont.load_default()
                print("警告: システムフォントが見つかりません。デフォルトフォントを使用します")
        
        # テキストのバウンディングボックスを取得
        bbox = draw.textbbox((0, 0), date_str, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 画像サイズを取得
        img_width, img_height = img.size
        
        # 右下の位置を計算（マージン20px）
        margin = 20
        x = img_width - text_width - margin
        y = img_height - text_height - margin
        
        # 背景の半透明矩形を描画（可読性向上）
        padding = 10
        background_bbox = [
            x - padding,
            y - padding,
            x + text_width + padding,
            y + text_height + padding
        ]
        
        # 半透明の黒背景を作成
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(background_bbox, fill=(0, 0, 0, 128))
        
        # RGB画像をRGBAに変換して合成
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        img = img.convert('RGB')
        
        # 再度描画オブジェクトを作成
        draw = ImageDraw.Draw(img)
        
        # 白文字で日付を描画
        draw.text((x, y), date_str, font=font, fill=(255, 255, 255))
        
        # 画像を保存（品質95で保存）
        img.save(output_path, 'JPEG', quality=95)
        
        print(f"成功: 日付を印字した画像を保存しました → {output_path}")
        print(f"撮影日: {date_str}")
        
    except FileNotFoundError:
        print(f"エラー: 入力ファイルが見つかりません: {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)


def main():
    """メイン関数"""
    # コマンドライン引数のチェック
    if len(sys.argv) != 3:
        print("使い方: python main.py <入力ファイル.jpg> <出力ファイル.jpg>")
        print("例: python main.py input.jpg output.jpg")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # 日付印字処理を実行
    add_date_to_image(input_path, output_path)


if __name__ == "__main__":
    main()
