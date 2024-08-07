import pandas as pd
import matplotlib.pyplot as plt

# Membaca file CSV
df = pd.read_csv('/home/pambudi/Yolov8/Data/Data3/General3/datatanpab3_15:56_31Jul.csv')

# Membuat grafik Error
plt.figure(figsize=(14, 7))
plt.plot(df['Error'], label='Error')
# plt.plot(df['Timestamp'], df['Delta Error'], label='Delta Error')

plt.axhline(y=0, color='r', linestyle='--', label='Set Point (0)')

# Memberi judul dan label pada grafik
plt.title('Error terhadap Waktu')
plt.xlabel('Waktu (s)')
plt.ylabel('Nilai Error')
plt.legend()
plt.grid(True)

# Membatasi rentang nilai error antara -20 hingga 20
plt.ylim(-100, 100)
# Membatasi rentang nilai waktu (disesuaikan dengan data)
plt.xlim(df.index.min(), df.index.max())

# Menampilkan grafik
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
