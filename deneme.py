import matplotlib.pyplot as plt

# İlk veri seti
x1 = [0, 1, 2, 3, 4]
y1 = [0, 1, 4, 9, 16]

# İkinci veri seti
x2 = [0, 1, 2, 3, 4]
y2 = [0, 2, 3, 8, 12]

# Grafik oluşturma
plt.plot(x1, y1, label='Çizgi 1', color='b')  # İlk çizgi
plt.plot(x2, y2, label='Çizgi 2', color='r')  # İkinci çizgi

# Eksen başlıkları ve grafik başlığı
plt.xlabel('X Ekseni')
plt.ylabel('Y Ekseni')
plt.title('İki Ayrı Çizgi Gösterimi')

# Lejant (legend) ekleme
plt.legend()

# Grafiği gösterme
plt.show()
