"""
EXIF Reader Module
画像のEXIFデータから情報を取得する機能を提供
"""

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
