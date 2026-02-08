# サンプル画像について

このディレクトリにテスト用のJPG画像を配置してください。

## 要件

- JPEG形式の画像ファイル
- EXIFデータ（特にDateTimeOriginalタグ）が含まれていること
- スマートフォンやデジタルカメラで撮影した写真が最適です

## テスト方法

```bash
# samplesディレクトリに画像を配置後
python main.py samples/your_photo.jpg samples/output.jpg
```

## EXIFデータの確認方法

macOSの場合:
```bash
mdls samples/your_photo.jpg | grep kMDItemContentCreationDate
```

Pillowを使う場合:
```python
from PIL import Image
img = Image.open('samples/your_photo.jpg')
print(img._getexif())
```
