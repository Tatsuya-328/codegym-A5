# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
load_dotenv()

# 環境変数を参照
import os

# google map API keyの設定
GOOGLE_MAP_API_KEY = os.getenv('GOOGLE_MAP_API_KEY')
