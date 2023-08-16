# 训练数据
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"]="SimHei"

# 设置正常显示字符
plt.rcParams["axes.unicode_minus"]=False
plt.rcParams["font.size"]=12

#设置随机种子，保证随机数可复现
np.random.seed(0)
#生成样本数据
X = np.random.randint(70,100,size=(50,2))

plt.scatter(X[:,0],X[:,1])
plt.xlabel("语文")
plt.ylabel("数学")

# n_clusters ：簇的数量  即k值
kmeans = KMeans(n_clusters=4)
kmeans.fit(X)

#获取聚类后质心
print("质心",kmeans.cluster_centers_)

#获取每个样本所属的簇。标签的数值对应所属簇的索引
print("标签",kmeans.labels_)

#获取 SSE（簇惯性）
print("SSE",kmeans.inertia_)

#获取迭代次数
print("迭代次数",kmeans.n_iter_)
#聚类的分值，分值越大，效果越好
print("分值",kmeans.score(X))