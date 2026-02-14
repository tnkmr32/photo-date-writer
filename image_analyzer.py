"""
Image Analyzer Module
画像の特性を分析する機能を提供
"""

import numpy as np


def is_portrait(img):
    """
    画像がportrait（縦向き）かどうかを判定する

    Args:
        img: PIL Imageオブジェクト

    Returns:
        bool: portraitの場合True、landscapeの場合False
    """
    return img.height > img.width


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


def check_aspect_ratio(img, tolerance=0.02):
    """
    画像のアスペクト比が3:2（または2:3）かを判定する
    
    Args:
        img: PIL Imageオブジェクト
        tolerance: 許容誤差（デフォルト: 0.02 = 2%）
    
    Returns:
        bool: 範囲内の場合True、範囲外の場合False
    """
    width, height = img.size
    ratio = width / height
    
    # 3:2 (landscape) の場合: ratio ≈ 1.5
    expected_landscape = 3.0 / 2.0  # 1.5
    
    # 2:3 (portrait) の場合: ratio ≈ 0.667
    expected_portrait = 2.0 / 3.0  # 0.667
    
    # tolerance範囲内かチェック
    is_landscape = abs(ratio - expected_landscape) <= (expected_landscape * tolerance)
    is_portrait = abs(ratio - expected_portrait) <= (expected_portrait * tolerance)
    
    return is_landscape or is_portrait
