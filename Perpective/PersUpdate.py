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


# Dörtgen bulma fonksiyonu
def find_quadrilaterals(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    quadrilaterals = []

    for contour in contours:
        # Konturun alanını hesapla
        area = cv2.contourArea(contour)
        if area < 100:  # Küçük alanları atla
            continue

        # Konturu dört kenara dönüştür
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # Dört kenar varsa kaydet
        if len(approx) == 4:
            quadrilaterals.append(approx)

    return quadrilaterals


# Uzaklıkları hesaplama fonksiyonu
def calculate_distances(quadrilaterals, origin):
    distances = []
    for quadrilateral in quadrilaterals:
        # Dörtgenin merkezini hesapla
        M = cv2.moments(quadrilateral)
        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
            # Uzaklığı hesapla
            distance_x = cX - origin[0]
            distance_y = origin[1] - cY  # Y'yi düzelt
            distances.append((distance_x, distance_y, (cX, cY)))  # Merkez koordinatını ekle
    return distances


# Resmi yükle
image = cv2.imread('pers.jpg')
if image is None:
    print("Resim yüklenemedi. Lütfen dosya yolunu kontrol edin.")
    exit()

image = cv2.resize(image, (800, 600))  # Resmi boyutlandır
cv2.imshow('Original Image', image)

# Fare olayı için pencereyi ayarla
cv2.setMouseCallback('Original Image', select_point)

# Kullanıcının tıklamasını bekle
cv2.waitKey(0)

# Dört köşe noktası (tıklanan noktalar)
if len(points) == 4:
    # Kullanıcıdan cm cinsinden koordinatları al
    for i in range(4):
        cm_x = float(input(f"{i + 1}. noktanın X koordinatını (cm cinsinden) girin: "))
        cm_y = float(input(f"{i + 1}. noktanın Y koordinatını (cm cinsinden) girin: "))
        cm_coordinates.append((cm_x, cm_y))

    pts1 = np.float32(points)  # Tıklanan dört noktayı al
    # Dönüştürülecek yeni köşe noktaları
    width, height = 280, 110  # İstediğiniz boyut
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])  # Düzgün bir sıralama

    # Perspektif dönüşüm matrisini hesapla
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(image, matrix, (width, height))

    # Dönüştürülmüş görüntüde kareleri bul
    quadrilaterals = find_quadrilaterals(result)

    # Bulunan kareleri çiz ve isimlerini yazdır
    for i, quadrilateral in enumerate(quadrilaterals):
        cv2.drawContours(result, [quadrilateral], -1, (0, 255, 0), 2)  # Dörtgeni yeşil ile çiz
        # Dörtgenin merkezini hesapla
        M = cv2.moments(quadrilateral)
        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
            # Kare ismini yazdır
            cv2.putText(result, f'Kare {i + 1}', (cX - 20, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Başlangıç noktası (ilk tıklanan nokta)
    origin = points[0]

    # Uzaklıkları hesapla
    distances = calculate_distances(quadrilaterals, origin)

    # Uzaklıkları ekrana yazdır
    for i, distance in enumerate(distances):
        print(f"Kare {i + 1} uzaklıkları (cm): X: {distance[0]}, Y: {distance[1]}")

    # Sonucu göster
    cv2.imshow('Warped Image with Detected Quadrilaterals', result)
else:
    print("Lütfen dört nokta seçin.")

cv2.waitKey(0)
cv2.destroyAllWindows()