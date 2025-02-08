# recommendation/utils_palette.py
import os
import requests

def get_palette_from_colorhunt(base_color):
    """
    base_color를 기준으로 컬러 헌트 API를 호출하여 추천 팔레트를 반환합니다.
    실제 API 키와 엔드포인트가 있다면 아래 코드를 수정합니다.
    """
    api_key = os.environ.get("COLORHUNT_API_KEY")  # 또는 Django settings에서 불러오기
    if api_key:
        url = "https://example-rapidapi-endpoint.com/getPalettes"  # 실제 API 엔드포인트로 수정 필요
        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "color-hunter.p.rapidapi.com"
        }
        params = {"color": base_color}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()  # API 문서에 따라 필요한 데이터 파싱
        else:
            return {"error": "API 호출 실패", "status_code": response.status_code}
    else:
        # 더미 팔레트 (실제 API 키가 없을 경우)
        dummy_palette = {
            "base_color": base_color,
            "palettes": [
                ["#FF5733", "#33FFCE", "#335BFF", "#9D33FF", "#FF33A8"],
                ["#FBF5DD", "#D4A5A5", "#A3C6C4", "#F7D6BF", "#FFE1A8"]
            ]
        }
        return dummy_palette
