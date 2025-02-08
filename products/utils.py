# products/utils.py
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def extract_dominant_colors(image_path, num_colors=5):
    """
    주어진 이미지 파일에서 대표 색상들을 추출합니다.
    - image_path: 이미지 파일 경로
    - num_colors: 추출할 대표 색상 개수
    반환: 헥스 코드 목록 (예: ['#FBF5DD', '#123456', ...])
    """
    image = Image.open(image_path).convert("RGB")
    # 처리 속도 향상을 위해 이미지 크기 리사이즈 (옵션)
    image = image.resize((150, 150))
    np_image = np.array(image)
    pixels = np_image.reshape((-1, 3))
    
    kmeans = KMeans(n_clusters=num_colors, random_state=0).fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    
    # RGB를 헥스 코드로 변환
    hex_colors = ['#{:02X}{:02X}{:02X}'.format(*color) for color in colors]
    return hex_colors
