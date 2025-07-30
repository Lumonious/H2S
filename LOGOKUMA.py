import re
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Gaussian çıktısını oku
filename = "sonn.log"  # Çıktı dosyasının ismini buraya girin
with open(filename, "r") as file:
    log_data = file.readlines()

# Enerji ve geometri verilerini ayıklamak için boş listeler
energies = []
bond_lengths = []
angles = []

# Regex kalıpları
energy_pattern = re.compile(r'SCF Done:\s+E\(.+?\)\s+=\s+(-?\d+\.\d+)')
bond_pattern = re.compile(r"R\(\d+,\d+\)\s+(\d+\.\d+)")
angle_pattern = re.compile(r"A\(\d+,\d+,\d+\)\s+(\d+\.\d+)")

# Her satırı tarayarak enerji ve geometri bilgilerini çıkar
for line in log_data:
    # Enerji değerini çek
    energy_match = energy_pattern.search(line)
    if energy_match:
        energies.append(float(energy_match.group(1)))
    
    # Bağ uzunluğunu çek
    bond_match = bond_pattern.search(line)
    if bond_match:
        bond_lengths.append(float(bond_match.group(1)))
    
    # Açıyı çek
    angle_match = angle_pattern.search(line)
    if angle_match:
        angles.append(float(angle_match.group(1)))

# Uzunlukları kontrol edin
print("Energies:", len(energies))
print("Bond Lengths:", len(bond_lengths))
print("Angles:", len(angles))

# En kısa listenin uzunluğunu bul
min_length = min(len(energies), len(bond_lengths), len(angles))

# Listeleri en kısa uzunluğa göre kırp
energies = energies[:min_length]
bond_lengths = bond_lengths[:min_length]
angles = angles[:min_length]

# Verileri bir Pandas DataFrame'e aktar
data = pd.DataFrame({
    'Energy (Hartree)': energies,
    'Bond Length (Å)': bond_lengths,
    'Angle (°)': angles
})

# Verileri kontrol et
print(data.head())

# Verileri bir txt dosyasına kaydet
data.to_csv("output.txt", sep="\t", index=False)

# 3D grafik çizimi
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(data['Bond Length (Å)'], data['Angle (°)'], data['Energy (Hartree)'], c=data['Energy (Hartree)'], cmap='viridis')

ax.set_xlabel('Bond Length (Å)')
ax.set_ylabel('Angle (°)')
ax.set_zlabel('Energy (Hartree)')
ax.set_title('3D Plot of Energy vs Bond Length and Angle')
fig.colorbar(sc, label='Energy (Hartree)')
plt.show()
