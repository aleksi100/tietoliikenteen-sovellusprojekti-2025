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

K = 6
max_iters = 30

dmax = np.max(data)
dmin = np.min(1200)
center_points = np.random.randint(dmin,dmax,size=(6,3))
center_points = np.random.randint(dmin,dmax,size=(6,3))
print(dmin)
print(dmax)
print("Initial centers:\n", center_points, "\n")

for iteration in range(max_iters):
    distances = np.linalg.norm(X[:, None, :] - center_points[None, :, :], axis=2)
    print("Distances shape: ", distances.shape)
    
    cluster_id = np.argmin(distances, axis=1)

    
    new_centers = np.array([
        X[cluster_id == k].mean(axis=0) if np.any(cluster_id == k) else np.random.randint(dmin,dmax,size=(3))
        for k in range(K)
    ])

    
    if np.allclose(center_points, new_centers):
        print(f"Converged after {iteration+1} iterations.\n")
        #break

    center_points = new_centers

print("Final centers:\n", center_points)



from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')


ax.scatter(X[:,0], X[:,1], X[:,2], c='blue', s=5, alpha=0.5, label='Data Points')

# Plot initial cluster centers
ax.scatter(
    center_points[:,0],
    center_points[:,1],
    center_points[:,2],
    c='red',
    s=180,
    marker='X',
    label='Center Points'
    
)


ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Sensor Data with Random Initial Cluster Centers')
ax.legend()

plt.show()


CP = center_points.astype(int)

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







