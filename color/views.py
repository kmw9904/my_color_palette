# color/views.py
import cv2
import numpy as np
from PIL import Image
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ColorExtraction
from .serializers import ColorExtractionSerializer

def extract_skin_color(image_field):
    """
    업로드된 이미지에서 얼굴을 검출한 후, 얼굴 영역 내에서
    YCrCb 색 공간 기반 스킨 컬러 범위를 활용하여 피부 영역을
    추출하고, 해당 영역의 평균 색상을 HEX 코드로 반환합니다.
    """
    try:
        # Pillow를 사용해 이미지를 RGB 모드로 엽니다.
        pil_image = Image.open(image_field).convert('RGB')
    except Exception as e:
        print("이미지 열기 오류:", e)
        return "#000000"  # 오류 시 검정색 반환

    # Pillow 이미지 -> NumPy 배열 (RGB 순서)
    cv_image = np.array(pil_image)

    # 그레이스케일 이미지 생성 (얼굴 검출을 위해)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)

    # Haar Cascade를 사용해 얼굴 검출
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        # 얼굴이 검출되지 않으면 전체 이미지의 평균 색상(혹은 기본 색상)을 반환
        return "#000000"

    # 검출된 얼굴 중 첫 번째 얼굴 영역 선택 (더 정교하게는 가장 큰 영역 선택 가능)
    (x, y, w, h) = faces[0]
    face_region = cv_image[y:y+h, x:x+w]

    # 얼굴 영역을 YCrCb 색 공간으로 변환 (피부 컬러 검출에 유리)
    face_ycrcb = cv2.cvtColor(face_region, cv2.COLOR_RGB2YCrCb)

    # 피부 색상의 일반적인 범위 (Y는 전체, Cr, Cb는 특정 범위)
    lower = np.array([0, 133, 77], dtype=np.uint8)
    upper = np.array([255, 173, 127], dtype=np.uint8)

    # 범위 내의 픽셀을 흰색(255), 나머지는 검정(0)으로 하는 마스크 생성
    skin_mask = cv2.inRange(face_ycrcb, lower, upper)

    # 모폴로지 연산: 노이즈 제거를 위해 침식과 팽창 적용
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    skin_mask = cv2.erode(skin_mask, kernel, iterations=1)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=1)

    # 마스크가 적용된 영역의 평균 색상 계산
    # cv2.mean는 마스크 영역 내에서 각 채널의 평균을 계산합니다.
    mean_color = cv2.mean(face_region, mask=skin_mask)  # (R, G, B, alpha)
    avg_color = mean_color[:3]  # RGB 채널만 사용

    # 만약 마스크로 인해 피부 픽셀이 전혀 검출되지 않았다면,
    # 얼굴 전체 영역의 평균 색상을 사용하도록 합니다.
    if cv2.countNonZero(skin_mask) == 0:
        avg_color_per_row = np.average(face_region, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)

    # 각 채널을 정수로 변환
    avg_color = tuple(int(c) for c in avg_color)

    # HEX 코드로 변환 (예: (251, 245, 221) -> "#FBF5DD")
    hex_color = '#{:02X}{:02X}{:02X}'.format(*avg_color)
    return hex_color

class ColorExtractionView(APIView):
    def post(self, request):
        serializer = ColorExtractionSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user if request.user.is_authenticated else None
            # 모델 저장 (이미지 업로드)
            color_extraction = serializer.save(user=user)
            
            # 실제 이미지 처리 로직 실행
            extracted_color = extract_skin_color(color_extraction.image)
            
            # 추출된 색상을 모델에 저장 및 업데이트
            color_extraction.extracted_color = extracted_color
            color_extraction.save()
            
            return Response(ColorExtractionSerializer(color_extraction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
