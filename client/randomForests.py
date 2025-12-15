#####################################################################
#
# Random forest code explained and teached with
# accelometer data
#
# Key issues to understand
# 1. Bootstrap sampling = Training data for each tree is different
# 2. Only subset of features are used when training a tree. Features with
#    accelometer data are X,Y,Z values
# 3. 1 and 2 together makes trees to look the problem from different perspective
# 4. Gini impurity is used to search for optimal threshold for a feature
# 5. Leaf (lehti)= end of tree branch and always has a prediction value
# 6. Node (solmu) = divides tree to left and righ branch with certain
#    feature and learned threshold
####################################################################

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


# =======================================
# 1. Gini impurity
# =======================================
def gini_impurity(y):
    counts = Counter(y)       # how many times labels 0,1,2,3,4,5 occur
    total = len(y)
                              # count / total is for examle 100/600
                              # if all the labels are the same, gini = 0
                              # if all the labels are equaly likely
                              # gini = (C-1)/C, where C = number of labels
                              # gini approaches 1, whem labels>>1


    return 1 - sum((count / total) ** 2 for count in counts.values())


# =======================================
# 2. Let's find best split for a one feature
# =======================================
def find_best_split(X_column, y):

    # Sort according to values (makes it easier to find split position)
    sorted_idx = X_column.argsort()
    X_sorted = X_column[sorted_idx]
    y_sorted = y[sorted_idx]

    best_gain = 0
    best_threshold = None

    parent_gini = gini_impurity(y)

    for i in range(1, len(y)):
        if X_sorted[i] == X_sorted[i - 1]:  # looking for position where
            continue                        # consecutive values are not
                                            # the same

        threshold = (X_sorted[i] + X_sorted[i - 1]) / 2

        left_y = y_sorted[:i]
        right_y = y_sorted[i:]

        g_left = gini_impurity(left_y)
        g_right = gini_impurity(right_y)

        n = len(y)
        # weighted gini calculated at child nodes
        gain = parent_gini - (len(left_y)/n)*g_left - (len(right_y)/n)*g_right

        if gain > best_gain:
            best_gain = gain
            best_threshold = threshold

    return best_threshold, best_gain


# =======================================
# 3. Decision Tree Node
# =======================================
class TreeNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, prediction=None):
        self.feature = feature        # features in our example are (X,Y,Z)
        self.threshold = threshold    # splitting threshold
        self.left = left
        self.right = right
        self.prediction = prediction  # Will have value only if leaf node


# =======================================
# 4. Decision Tree
# =======================================
class DecisionTree:
    def __init__(self, max_depth=3, feature_subsample=2):
        self.max_depth = max_depth
        self.feature_subsample = feature_subsample  # using only 2 features
        self.root = None                            # othervice trees are
                                                    # too similar

    def fit(self, X, y, depth=0):
        if depth >= self.max_depth or len(set(y)) == 1:   # max depth or all
                                                          # values have same
                                                          # label
            prediction = Counter(y).most_common(1)[0][0]  # calculates the most
            return TreeNode(prediction=prediction)        # common label

        n_features = X.shape[1]         # X,Y,Z data case n_features = 3
                                        # as our data X.shape = 600,3

        # Random feature selected from 2 feature set
        feature_indices = np.random.choice(n_features, self.feature_subsample, replace=False)

        best_feature = None
        best_threshold = None
        best_gain = 0

        # Find best split from selected features
        for f in feature_indices:
            threshold, gain = find_best_split(X[:, f], y)
            if gain > best_gain:
                best_gain = gain
                best_feature = f
                best_threshold = threshold

        # if there is no gain → make a leaf
        if best_gain == 0 or best_threshold is None:
            prediction = Counter(y).most_common(1)[0][0]
            return TreeNode(prediction=prediction)

        # split based on searhed best feature and threshold
        left_idx = X[:, best_feature] < best_threshold
        right_idx = ~left_idx
        # fit function is called recursively until we end up to leaf

        left_child = self.fit(X[left_idx], y[left_idx], depth+1)
        right_child = self.fit(X[right_idx], y[right_idx], depth+1)

        node = TreeNode(
            feature=best_feature,
            threshold=best_threshold,
            left=left_child,
            right=right_child
        )

        if depth == 0:
            self.root = node

        return node

    def predict_one(self, x):
        node = self.root
        while node.prediction is None:
            if x[node.feature] < node.threshold:
                node = node.left
            else:
                node = node.right
        return node.prediction

    def predict(self, X):
        return np.array([self.predict_one(x) for x in X])

    def print_tree(self, node=None, depth=0):
        if node is None:
            node = self.root

        indent = "  " * depth
        if node.prediction is not None:
            print(f"{indent}Leaf: predict={node.prediction} if branc {node}")


        else:
            print(f"{indent}Node: feature={node.feature}, threshold={node.threshold:.3f} else branch {node}")


            self.print_tree(node.left, depth + 1)
            self.print_tree(node.right, depth + 1)

# =======================================
# 5. Random Forest
# =======================================
class RandomForest:
    def __init__(self, n_estimators=10, max_depth=3, feature_subsample=2):
        self.n_estimators = n_estimators
        self.trees = []
        self.max_depth = max_depth
        self.feature_subsample = feature_subsample

    def fit(self, X, y):
        n = len(y)
        for _ in range(self.n_estimators):

            idx = np.random.choice(n, n, replace=True)
            X_sample = X[idx]
            y_sample = y[idx]

            tree = DecisionTree(
                max_depth=self.max_depth,
                feature_subsample=self.feature_subsample
            )
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)

    def predict(self, X):
        tree_preds = np.array([tree.predict(X) for tree in self.trees])
        # Äänestys
        preds = []
        for col in tree_preds.T:
            preds.append(Counter(col).most_common(1)[0][0])
        return np.array(preds)


# =======================================
# 6. LET'S GENERATE ACCELOMETER DATA
# =======================================
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

y_data = data[:,3]

X_data = data[:,0:3]

N=600

# Train/test
idx = int(0.7 * N)
X_train, X_test = X_data[:idx], X_data[idx:]
y_train, y_test = y_data[:idx], y_data[idx:]


# =======================================
# 7. OPETETAAN OMA RANDOM FOREST
# =======================================
forest = RandomForest(n_estimators=20, max_depth=4, feature_subsample=2)
forest.fit(X_train, y_train)

print("Random Forest teached!\n")


# =======================================
# 8. INFERENCE = PREDICTING WITH THE MODEL
# =======================================
# X_data[0,:] ~ 1800, 1500, 1500
# X_data[101,:] ~ 1200, 1500, 1500
# X_data[201,:] ~ 1500, 1800, 1500
new_samples = np.array([X_data[0,:], X_data[101,:], X_data[201,:]])

pred = forest.predict(new_samples)

print("Predictions:\n")
for i, p in enumerate(pred):
    print(f"  Measurement {i+1}: label {p}")
    
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(data[:,0], data[:,1], data[:,2],color='red')

# Akselien nimet
ax.set_xlabel('X-akseli')
ax.set_ylabel('Y-akseli')
ax.set_zlabel('Z-akseli')

plt.show()



tree = DecisionTree(max_depth=3)
tree.fit(X_data, y_data)
tree.print_tree()

print("")

tree = DecisionTree(max_depth=3)
tree.fit(X_data, y_data)
tree.print_tree()

