import cv2
import numpy as np

# Global değişkenler
points = []
cm_coordinates = []

# Fare ile tıklama olayı için fonksiyon
def select_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:  # Sadece dört nokta seçilmesine izin ver
            points.append((x, y))
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # Yeşil nokta ekle
            cv2.imshow('Image', image)

# Koordinatları ekrana yazdırma
def add_coordinates(image, coords):
    for i, coord in enumerate(coords):
        # Hem tıklanan noktanın koordinatını hem de cm cinsinden koordinatları yaz
        text = f"({coord[0]}, {coord[1]})"
        cv2.putText(image, text, (int(points[i][0]), int(points[i][1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        # Tıklanan noktanın koordinatını da göster
        point_text = f"Point {i+1}: ({points[i][0]}, {points[i][1]})"
        cv2.putText(image, point_text, (int(points[i][0]), int(points[i][1] + 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# Resmi yükle
image = cv2.imread('pers.jpg')
if image is None:
    print("Resim yüklenemedi. Lütfen dosya yolunu kontrol edin.")
    exit()

image = cv2.resize(image, (800, 600))  # Resmi boyutlandır
cv2.imshow('Image', image)

# Fare olayı için pencereyi ayarla
cv2.setMouseCallback('Image', select_point)

# Kullanıcının tıklamasını bekle
cv2.waitKey(0)

# Dört köşe noktası (tıklanan noktalar)
if len(points) == 4:
    # Kullanıcıdan cm cinsinden koordinatları al
    for i in range(4):
        cm_x = float(input(f"{i+1}. noktanın X koordinatını (cm cinsinden) girin: "))
        cm_y = float(input(f"{i+1}. noktanın Y koordinatını (cm cinsinden) girin: "))
        cm_coordinates.append((cm_x, cm_y))

    pts1 = np.float32(points)  # Tıklanan dört noktayı al
    # Dönüştürülecek yeni köşe noktaları
    width, height = 280, 110  # İstediğiniz boyut
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])  # Düzgün bir sıralama

    # Perspektif dönüşüm matrisini hesapla
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(image, matrix, (width, height))

    # Sonucu göster
    add_coordinates(result, cm_coordinates)  # Koordinatları ekle
    cv2.imshow('Warped Image with Coordinates', result)
else:
    print("Lütfen dört nokta seçin.")

cv2.waitKey(0)
cv2.destroyAllWindows()