import os

API_KEY = (
    os.getenv("YUANDIAN_API_KEY")
    or os.getenv("YUANDIAN_API")
    or os.getenv("CHINESELAW_API_KEY")
    or ""
)
