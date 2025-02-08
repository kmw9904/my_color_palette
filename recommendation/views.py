# recommendation/views.py
import colorsys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils_palette import (
    fetch_palettes_from_colorhunter,
    select_palette_with_required_colors,
    extract_recommendation_colors
)
class PaletteBasedRecommendationView(APIView):
    """
    사용자로부터 피부톤, 아우터 색상, 그리고 원하는 스타일을 받아서,
    Color Hunter API를 통해 팔레트를 가져온 후, 
    두 색상(피부톤과 아우터 색상)이 포함(혹은 유사)된 팔레트를 선택하고,
    해당 팔레트에서 이 두 색상을 제외한 나머지 색상들을 추천하는 API.
    """
    def post(self, request):
        skin_tone = request.data.get("skin_tone")
        outer_color = request.data.get("outer_color") or skin_tone
        style = request.data.get("style", "빈티지")
        
        if not skin_tone:
            return Response({"error": "skin_tone is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 필수 색상 목록 생성
        required_colors = [skin_tone, outer_color]
        
        # RapidAPI의 Color Hunter API에서 해당 스타일의 팔레트들을 가져옴
        palettes_data = fetch_palettes_from_colorhunter(theme=style)
        if not palettes_data:
            return Response({"error": "Failed to fetch palettes from API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # API 응답 구조에 따라 팔레트 리스트 추출 (예시: palettes_data["palettes"])
        palettes = palettes_data.get("palettes", [])
        if not palettes:
            return Response({"error": "No palettes found for the given style"}, status=status.HTTP_404_NOT_FOUND)
        
        # 필수 색상을 포함하는 최적의 팔레트 선택
        best_palette = select_palette_with_required_colors(required_colors, palettes)
        if not best_palette:
            return Response({"error": "No suitable palette found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 선택된 팔레트에서 추천 색상 추출 (필수 색상과 유사한 색상은 제외)
        recommended_colors = extract_recommendation_colors(best_palette, exclude_colors=required_colors)
        
        result = {
            "selected_palette": best_palette,
            "recommended_colors": recommended_colors
        }
        return Response(result, status=status.HTTP_200_OK)

def complementary_color(hex_color):
    """
    입력된 HEX 색상에 대해 보색을 계산합니다.
    """
    # '#' 제거 후 RGB 값으로 변환
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # 0~1 범위로 스케일 조정
    r_, g_, b_ = r/255.0, g/255.0, b/255.0
    # HSV로 변환 (색상, 채도, 명도)
    h, s, v = colorsys.rgb_to_hsv(r_, g_, b_)
    # 색상(hue)을 180도(0.5)를 더해 보색 계산 (모듈로 1.0)
    h = (h + 0.5) % 1.0
    # 다시 RGB로 변환
    r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
    r2, g2, b2 = int(r2 * 255), int(g2 * 255), int(b2 * 255)
    return '#{:02X}{:02X}{:02X}'.format(r2, g2, b2)

def analogous_colors(hex_color, num=2):
    """
    입력된 HEX 색상에 대해 좌우로 약간의 Hue 변화를 주어
    유사색을 계산합니다.
    num: 반환할 유사색 개수 (기본 2개)
    """
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r_, g_, b_ = r/255.0, g/255.0, b/255.0
    h, s, v = colorsys.rgb_to_hsv(r_, g_, b_)
    
    colors = []
    # 유사색은 색상(hue)을 약 ±0.1 정도 이동한 색상으로 계산
    shifts = [-0.1, 0.1]
    for shift in shifts[:num]:
        new_h = (h + shift) % 1.0
        r2, g2, b2 = colorsys.hsv_to_rgb(new_h, s, v)
        colors.append('#{:02X}{:02X}{:02X}'.format(int(r2*255), int(g2*255), int(b2*255)))
    return colors

class RecommendationView(APIView):
    """
    POST 요청을 받아 사용자가 입력한 base_color(HEX 문자열)와 장르(옵션)를 기반으로
    추천 색상을 반환하는 API입니다.
    """
    def post(self, request):
        data = request.data
        base_color = data.get('base_color')
        genre = data.get('genre', 'default')  # 장르를 나중에 알고리즘에 반영할 수 있음
        
        if not base_color:
            return Response({"error": "base_color is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 기본 추천 로직: 보색과 유사색 계산
        comp_color = complementary_color(base_color)
        analo_colors = analogous_colors(base_color)
        
        recommendations = {
            "base_color": base_color,
            "complementary": comp_color,
            "analogous": analo_colors,
            "genre": genre,
            # 향후 장르에 따른 추가 필터링이나 다른 추천 알고리즘 추가 가능
        }
        
        return Response(recommendations, status=status.HTTP_200_OK)

class PaletteRecommendationView(APIView):
    """
    POST 요청으로 base_color를 전달받아 추천 팔레트를 반환하는 API입니다.
    """
    def post(self, request):
        data = request.data
        base_color = data.get('base_color')
        if not base_color:
            return Response({"error": "base_color is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        palette_data = fetch_palettes_from_colorhunter(base_color)
        return Response(palette_data, status=status.HTTP_200_OK)