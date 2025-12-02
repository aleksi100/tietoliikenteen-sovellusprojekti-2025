import numpy as np
import matplotlib.pyplot as plt
''''

data = np.genfromtxt(
    "sensordata.csv",
    delimiter=",",
    usecols=[4,5,6],
    skip_header=1,
)

X = data[:, 0]
Y = data[:, 1]
Z = data[:, 2]
'''

np.random.seed(0)
# There are 6 classes:
# X direction down => X = 1800, label = 0
# X direction up => X = 1200, label = 1
# etc.
data = np.zeros((600,4))
data[0:100,:] = np.array([1800,1500,1500,0])
data[100:200,:] = np.array([1200,1500,1500,1])
data[200:300,:] = np.array([1500,1800,1500,2])
data[300:400,:] = np.array([1500,1200,1500,3])
data[400:500,:] = np.array([1500,1500,1800,4])
data[500:600,:] = np.array([1500,1500,1200,5])
data[:,0:3] = data[:,0:3] + 70*np.random.rand(600, 3)


Y = data[:,3]
X = data[:,0:3]
Z = data[:, 2]

center_points = data[np.random.choice(len(data), 6, replace=False)]
print("Alkuperäiset")
print(center_points)
print("----------------")

centerPointCumulativeSum = np.zeros((6,3))
Counts = np.zeros(6)

for i in range(data.shape[0]):
    point = data[i]
    distance = np.zeros(6)

    for c in range(6):
        distance[c] = np.linalg.norm(point[0:3] - center_points[c,0:3])

    smallest_idx = np.argmin(distance)
    Counts[smallest_idx] += 1
    centerPointCumulativeSum[smallest_idx] += point[0:3]


updated_centers = centerPointCumulativeSum / Counts[:, None]

print("Siirretyt")
print(updated_centers)


from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot all points
#ax.scatter(X, Y, Z, c='blue', s=5, alpha=0.5, label='Data Points')

ax.scatter(X[:,0], X[:,1], X[:,2], c='blue', s=5, alpha=0.5, label='Data Points')

# Plot initial cluster centers
ax.scatter(
    center_points[:,0],
    center_points[:,1],
    center_points[:,2],
    c='red',
    s=80,
    marker='X',
    label='Center Points'
    
)

ax.scatter(
    updated_centers[:,0],
    updated_centers[:,1],
    updated_centers[:,2],
    c='green',
    s=100,
    marker='D',
    label='Updated Cluster Centers'
)


ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Sensor Data with Random Initial Cluster Centers')
ax.legend()

plt.show()

# Oletetaan, että updated_centers on muotoa (6,3)
# ja sisältää keskipisteiden koordinaatit kokonaislukuina

# Muunna float -> int, jos haluat kokonaisarvot
CP = updated_centers.astype(int)

# Luo tiedosto
with open("keskipisteet.h", "w") as f:
    f.write("int CP[6][3] = {\n")
    for i, row in enumerate(CP):
        f.write(f"    {{{row[0]}, {row[1]}, {row[2]}}}")
        if i < len(CP)-1:
            f.write(",  // Keskipiste {}\n".format(i+1))
        else:
            f.write("   // Keskipiste {}\n".format(i+1))
    f.write("};\n")

print("Tiedosto 'keskipisteet.h' luotu onnistuneesti!")










'''''
for o in range(scaled_points.shape[0]):
    for i in range(data.shape[0]):
        point1 = data[i]
        point2 = scaled_points[o]
        lyhyin = np.linalg.norm(point1-point2)
        




fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X, Y, Z)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.scatter(center_points[:,0], center_points[:,1], center_points[:,2],
           color='red', s=100, marker='X', label='Center Points')

plt.show()

'''
