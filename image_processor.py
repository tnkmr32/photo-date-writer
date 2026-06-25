"""
Image Processor Module
画像に日付を印字するメイン処理を提供
"""

import os
from PIL import Image, ImageDraw, ImageFont

from exif_reader import get_date_from_exif
from image_analyzer import is_portrait, is_grayscale_image, check_aspect_ratio
from image_effects import apply_film_date_effect


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
        
        # アスペクト比をチェック
        if not check_aspect_ratio(img):
            width, height = img.size
            actual_ratio = width / height
            error_msg = f"画像のアスペクト比が3:2ではありません (サイズ: {width}x{height}, 比率: {actual_ratio:.3f})"
            raise ValueError(error_msg)
        
        # EXIFから日付を取得
        date = get_date_from_exif(img)
        if not date:
            raise ValueError("EXIFから撮影日時を取得できませんでした")
        
        # 日付を `YY    MM    DD` 形式にフォーマット（フィルムカメラ風・7セグメント）
        date_str = date.strftime('%y    %m    %d')
        
        # RGB モードに変換（必要に応じて）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Portrait画像かどうかを判定
        is_portrait_img = is_portrait(img)
        
        # Portrait画像の場合、左に90度回転（反時計回り）
        if is_portrait_img:
            img = img.rotate(90, expand=True)
        
        # モノクロ画像かどうかを判定
        is_grayscale = is_grayscale_image(img)
        
        # 印字色と強度を選択
        if is_grayscale:
            text_color = (255, 255, 255)  # 白
            film_intensity = 0.7
        else:
            text_color = (255, 150, 80)   # オレンジ
            film_intensity = 0.5
        
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
        horizontal_margin = int(img_width * 0.08)  # 右端からのマージン
        vertical_margin = int(img_width * 0.04)    # 下端からのマージン
        x = img_width - text_width - horizontal_margin
        y = img_height - text_height - vertical_margin
        
        # テキストマスクを作成（フィルム印字効果用）
        text_mask = Image.new('L', (img_width, img_height), 0)
        mask_draw = ImageDraw.Draw(text_mask)
        mask_draw.text((x, y), date_str, font=font, fill=255)
        
        # フィルム印字効果を適用してテキストを合成（選択した色と強度を使用）
        img = apply_film_date_effect(img, text_mask, color=text_color, intensity=film_intensity)
        
        # Portrait画像の場合、左に270度回転して元に戻す（反時計回り）
        if is_portrait_img:
            img = img.rotate(270, expand=True)
        
        # 画像を保存（品質95で保存）
        img.save(output_path, 'JPEG', quality=95)
        
        print(f"成功: 日付を印字した画像を保存しました → {output_path}")
        print(f"撮影日: {date_str}")
        
    except FileNotFoundError:
        raise FileNotFoundError(f"入力ファイルが見つかりません: {input_path}")
    except Exception as e:
        # 既に適切なメッセージを持つ例外はそのまま再raise
        if isinstance(e, (ValueError, FileNotFoundError)):
            raise
        # その他の例外は新しいメッセージでラップ
        raise Exception(f"画像処理エラー: {e}")
