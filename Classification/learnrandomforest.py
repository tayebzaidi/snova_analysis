from sklearn import datasets
iris = datasets.load_iris()
print iris.keys()

X=iris.data
y=iris.target

print X.shape
print y.shape
