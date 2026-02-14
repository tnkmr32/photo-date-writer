#!/usr/bin/env python3
"""
Photo Date Writer - MVP版
JPGファイルのEXIFから撮影日時を読み取り、画像右下に日付を印字するシンプルなツール
"""

import sys
import os

from image_processor import add_date_to_image
from file_handler import collect_jpg_files, process_multiple_images


def main():
    """メイン関数"""
    # コマンドライン引数のチェック
    if len(sys.argv) != 3:
        print("使い方:")
        print("  単一ファイル: python main.py <入力ファイル.jpg> <出力ファイル.jpg>")
        print("  フォルダ処理: python main.py <入力フォルダ> <出力フォルダ>")
        print("例:")
        print("  python main.py input.jpg output.jpg")
        print("  python main.py ./input_folder ./output_folder")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # 入力パスの存在チェック
    if not os.path.exists(input_path):
        print(f"エラー: 入力パスが存在しません: {input_path}")
        sys.exit(1)
    
    # 入力がファイルかフォルダかを判定
    if os.path.isfile(input_path):
        # 単一ファイル処理
        try:
            add_date_to_image(input_path, output_path)
        except Exception as e:
            print(f"エラー: {e}")
            sys.exit(1)
    
    elif os.path.isdir(input_path):
        # フォルダ処理
        # 出力先もフォルダであることを確認
        if os.path.exists(output_path) and not os.path.isdir(output_path):
            print(f"エラー: 出力先がフォルダではありません: {output_path}")
            sys.exit(1)
        
        # 出力フォルダが存在しない場合は作成
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
                print(f"出力フォルダを作成しました: {output_path}\n")
            except Exception as e:
                print(f"エラー: 出力フォルダの作成に失敗しました: {e}")
                sys.exit(1)
        
        # JPGファイルを収集
        jpg_files = collect_jpg_files(input_path)
        
        if not jpg_files:
            print(f"エラー: 入力フォルダにJPGファイルが見つかりません: {input_path}")
            sys.exit(1)
        
        print(f"入力フォルダ: {input_path}")
        print(f"出力フォルダ: {output_path}")
        
        # バッチ処理を実行
        process_multiple_images(jpg_files, output_path)
    
    else:
        print(f"エラー: 入力パスが不正です: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
