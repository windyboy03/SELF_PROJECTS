from sklearn import datasets
iris = datasets.load_iris()
x = iris.data
y = iris.target
from sklearn.neighbors import KNeighborsClassifier
# k = 5
knn_5 = KNeighborsClassifier(n_neighbors= 5 )
knn_5.fit(x,y)
# k = 1
knn_1 = KNeighborsClassifier(n_neighbors= 1 )
knn_1.fit(x,y)

from sklearn.metrics import accuracy_score
# k = 5,result
y_pred = knn_5.predict(x)
print(accuracy_score(y,y_pred))
# k = 1，它的准确率
y_pred = knn_1.predict(x)
print(accuracy_score(y,y_pred))
