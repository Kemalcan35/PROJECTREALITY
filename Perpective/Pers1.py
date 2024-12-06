import cv2
import numpy as np

# Global değişkenler
points = []

# Fare ile tıklama olayı için fonksiyon
def select_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:  # Sadece dört nokta seçilmesine izin ver
            points.append((x, y))
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # Yeşil nokta ekle
            cv2.imshow('Image', image)

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
    pts1 = np.float32(points)  # Tıklanan dört noktayı al
    # Dönüştürülecek yeni köşe noktaları
    width, height = 600, 400  # İstediğiniz boyut
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])  # Düzgün bir sıralama

    # Perspektif dönüşüm matrisini hesapla
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(image, matrix, (width, height))

    # Sonucu göster
    cv2.imshow('Warped Image', result)
else:
    print("Lütfen dört nokta seçin.")

cv2.waitKey(0)
cv2.destroyAllWindows()