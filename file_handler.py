"""
File Handler Module
ファイルやフォルダの操作、複数ファイルの一括処理機能を提供
"""

import os
import glob

from image_processor import add_date_to_image


def collect_jpg_files(folder_path):
    """
    フォルダ内のJPGファイルを収集する
    
    Args:
        folder_path: 検索するフォルダのパス
        
    Returns:
        list: JPGファイルのパスのリスト（ソート済み）
    """
    jpg_files = []
    
    # 様々な拡張子パターンに対応
    patterns = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']
    
    for pattern in patterns:
        jpg_files.extend(glob.glob(os.path.join(folder_path, pattern)))
    
    # 重複を削除してソート
    jpg_files = sorted(list(set(jpg_files)))
    
    return jpg_files


def process_multiple_images(input_files, output_folder):
    """
    複数の画像ファイルを一括処理する
    
    Args:
        input_files: 入力ファイルのパスのリスト
        output_folder: 出力先フォルダのパス
    """
    total = len(input_files)
    success_count = 0
    failed_files = []  # (ファイル名, エラーメッセージ)のリスト
    
    print(f"処理を開始します...")
    print(f"対象ファイル数: {total}件\n")
    
    for i, input_path in enumerate(input_files, 1):
        filename = os.path.basename(input_path)
        output_path = os.path.join(output_folder, filename)
        
        print(f"[{i}/{total}] 処理中: {filename}")
        
        try:
            add_date_to_image(input_path, output_path)
            success_count += 1
        except Exception as e:
            error_msg = str(e)
            failed_files.append((filename, error_msg))
            print(f"エラー: {error_msg}")
        
        print()  # 空行
    
    # 処理結果のサマリーを表示
    print("=" * 40)
    print("処理完了")
    print(f"成功: {success_count}件")
    print(f"失敗: {len(failed_files)}件")
    
    if failed_files:
        print("\n失敗したファイル:")
        for filename, error_msg in failed_files:
            print(f"  - {filename}: {error_msg}")
