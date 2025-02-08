import os
import requests
import math

def fetch_palettes_from_colorhunter(theme="sky", base_hex=None):
    """
    RapidAPI의 Color Hunter API를 호출하여 지정된 테마(theme)에 따른 팔레트 목록을 반환합니다.
    - theme: ColorHunt 웹사이트에서 제공하는 테마 (예: "sky", "vintage", "pastel", "retro", "monotone" 등)
    - base_hex: 옵션으로, 특정 기준 색상(hex 코드)을 넣으면 이 색상을 기준으로 팔레트를 필터링할 수도 있음
    """
    url = "https://color-hunter.p.rapidapi.com/palettes/" + theme
    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY"),   # 환경변수에 API 키 저장
        "X-RapidAPI-Host": "color-hunter.p.rapidapi.com"
    }
    
    params = {}
    if base_hex:
        params["hex"] = base_hex.lstrip('#')  # 필요에 따라 파라미터 구성

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()  # API 응답 형식에 따라 수정 필요 (예: 팔레트 목록)
    else:
        return None
    
def color_distance(hex1, hex2):
    """
    두 헥스 색상(hex 문자열, 예: "#FBF5DD") 사이의 유클리드 거리를 계산합니다.
    거리가 작을수록 색상이 비슷하다고 판단할 수 있습니다.
    """
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
    # 각 색상 성분 간의 차이를 제곱하여 합산한 후 제곱근을 구함
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)))

def select_palette_with_required_colors(required_colors, palettes, threshold=50):
    """
    required_colors: 리스트, 예: [user_face_color, outer_color]
    palettes: 외부 API나 더미 데이터로부터 가져온 팔레트 목록. 각 팔레트는 {"name": ..., "colors": [색상1, 색상2, ...]} 형식.
    threshold: 두 색상이 "유사하다"고 판단할 최대 색상 거리 (값은 실험을 통해 조정)
    
    각 팔레트에서, 모든 required_color와 팔레트 내 색상들 간의 최소 거리를 계산합니다.
    만약 모든 required_color의 최소 거리가 threshold 이하이면, 그 팔레트를 후보로 합니다.
    여러 후보가 있다면, 총 거리(유사도)의 합이 가장 작은 팔레트를 선택합니다.
    """
    best_palette = None
    best_score = float('inf')
    
    for palette in palettes:
        palette_colors = palette.get("colors", [])
        total_distance = 0
        meets_requirements = True
        for req_color in required_colors:
            distances = [color_distance(req_color, pal_color) for pal_color in palette_colors]
            min_distance = min(distances) if distances else float('inf')
            if min_distance > threshold:
                meets_requirements = False
                break
            total_distance += min_distance
        if meets_requirements and total_distance < best_score:
            best_score = total_distance
            best_palette = palette
    return best_palette

def extract_recommendation_colors(best_palette, exclude_colors, similarity_threshold=50):
    """
    best_palette: 선택된 팔레트 딕셔너리, 예: {"name": "...", "colors": [색상1, 색상2, ...]}
    exclude_colors: 리스트, 예: [user_face_color, outer_color]
    similarity_threshold: 제외할 색상과의 유사도 임계값
    
    best_palette의 색상들 중, exclude_colors와의 유사도(거리)가 similarity_threshold 미만이면 해당 색상은 추천 목록에서 제외하고,
    나머지 색상들을 추천 색상으로 반환합니다.
    """
    palette_colors = best_palette.get("colors", [])
    recommendation_colors = []
    for color in palette_colors:
        # exclude_colors 중 하나와의 거리가 similarity_threshold 미만이면 제외
        if any(color_distance(color, ex_color) < similarity_threshold for ex_color in exclude_colors):
            continue
        recommendation_colors.append(color)
    return recommendation_colors
