#!/usr/bin/env python3
"""
Photo Date Writer - MVP版
JPGファイルのEXIFから撮影日時を読み取り、画像右下に日付を印字するシンプルなツール
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
from datetime import datetime
import numpy as np


def apply_dodge_effect(base_img, text_mask, color=(255, 150, 80), intensity=0.7):
    """
    覆い焼き（Dodge）効果でテキストを合成する
    
    Args:
        base_img: PIL Image（ベース画像、RGBモード）
        text_mask: PIL Image（テキストマスク、Lモード。白い部分がテキスト）
        color: tuple（覆い焼きに使用する色のRGB値）
        intensity: float（効果の強度 0.0-1.0）
    
    Returns:
        PIL Image: 覆い焼き効果を適用した画像
    """
    # PIL ImageをNumPy配列に変換
    base_array = np.array(base_img, dtype=np.float32)
    mask_array = np.array(text_mask, dtype=np.float32) / 255.0  # 0.0-1.0に正規化
    
    # カラー値を0.0-1.0に正規化
    color_normalized = np.array(color, dtype=np.float32) / 255.0
    
    # 覆い焼き効果を適用
    # Dodge formula: Result = Base / (1 - Blend)
    # ただし、安全な実装として: Result = Base / (1 - Blend * intensity)
    result = base_array.copy()
    
    for i in range(3):  # RGB各チャンネルに対して
        # ブレンド値（マスク × カラー × 強度）
        blend = mask_array * color_normalized[i] * intensity
        
        # ゼロ除算を避けるため、blend が 1.0 に近い場合は最大値に
        # 覆い焼き計算: base / (1 - blend)
        denominator = 1.0 - blend
        denominator = np.maximum(denominator, 0.001)  # 最小値を設定してゼロ除算回避
        
        channel_result = base_array[:, :, i] / denominator
        
        # 255でクリップ
        result[:, :, i] = np.minimum(channel_result, 255.0)
    
    # NumPy配列をPIL Imageに変換
    result_img = Image.fromarray(result.astype(np.uint8))
    
    return result_img


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


def is_grayscale_image(img):
    """
    画像がモノクロ（グレースケール）かどうかを判定する

    Args:
        img: PIL Imageオブジェクト

    Returns:
        bool: モノクロの場合True、カラーの場合False
    """
    # 1. 画像モードで判定
    if img.mode in ('L', 'LA', '1'):
        return True

    # 2. RGB画像の場合、ピクセルをサンプリングして判定
    if img.mode in ('RGB', 'RGBA'):
        # 効率化のため、画像を縮小してサンプリング
        sample = img.resize((100, 100))
        pixels = np.array(sample)

        # R, G, Bチャンネルを取得
        r, g, b = pixels[:,:,0], pixels[:,:,1], pixels[:,:,2]

        # R=G=Bのピクセルの割合を計算
        grayscale_pixels = np.sum((r == g) & (g == b))
        total_pixels = r.size

        # 95%以上がグレースケールならモノクロと判定
        return (grayscale_pixels / total_pixels) > 0.95

    return False


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
        
        # 日付を `YY    MM    DD` 形式にフォーマット（フィルムカメラ風・7セグメント）
        date_str = date.strftime('%y    %m    %d')
        
        # RGB モードに変換（必要に応じて）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # モノクロ画像かどうかを判定
        is_grayscale = is_grayscale_image(img)
        
        # 印字色と強度を選択
        if is_grayscale:
            text_color = (255, 255, 255)  # 白
            dodge_intensity = 0.9
        else:
            text_color = (255, 150, 80)   # オレンジ
            dodge_intensity = 0.7
        
        # 描画用オブジェクトを作成
        draw = ImageDraw.Draw(img)
        
        # 画像サイズを取得
        img_width, img_height = img.size
        
        # フォント設定（7セグメントディスプレイ風フォント）
        # 画像の幅に対して2%のサイズに設定（高解像度画像に対応）
        font_size = int(img_width * 0.02)
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "DSEG7ClassicMini-BoldItalic.ttf")
        
        try:
            # プロジェクトの7セグメントフォント
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
            else:
                raise FileNotFoundError("7セグメントフォントが見つかりません")
        except:
            try:
                # フォールバック: Courier New Bold
                font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", font_size)
            except:
                try:
                    # Windows - Courier Bold
                    font = ImageFont.truetype("courbd.ttf", font_size)
                except:
                    try:
                        # Linux - Liberation Mono Bold
                        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", font_size)
                    except:
                        # 通常のCourier Newにフォールバック
                        try:
                            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New.ttf", font_size)
                        except:
                            # デフォルトフォントを使用
                            font = ImageFont.load_default()
                            print("警告: システムフォントが見つかりません。デフォルトフォントを使用します")
        
        # テキストのバウンディングボックスを取得
        bbox = draw.textbbox((0, 0), date_str, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 右下の位置を計算（マージンを水平・垂直で分離）
        horizontal_margin = int(img_width * 0.04)  # 右端からのマージン
        vertical_margin = int(img_width * 0.02)    # 下端からのマージン
        x = img_width - text_width - horizontal_margin
        y = img_height - text_height - vertical_margin
        
        # テキストマスクを作成（覆い焼き効果用）
        text_mask = Image.new('L', (img_width, img_height), 0)
        mask_draw = ImageDraw.Draw(text_mask)
        mask_draw.text((x, y), date_str, font=font, fill=255)
        
        # 覆い焼き効果を適用してテキストを合成（選択した色と強度を使用）
        img = apply_dodge_effect(img, text_mask, color=text_color, intensity=dodge_intensity)
        
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
