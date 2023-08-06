'''
A general test script that ensures PaCMAP can be successfully loaded.
'''

import pacmap
import numpy as np
import matplotlib.pyplot as plt


# Try initialize
pacmap.PaCMAP()
print("Instance initialized successfully.")
# print instance
print(pacmap.PaCMAP())
# Initialize sample data
sample_data = np.random.normal(size=(10000, 20))
b = pacmap.PaCMAP(random_state=10)
b_out = b.fit_transform(sample_data)
c = pacmap.PaCMAP(random_state=10)
c_out = c.fit_transform(sample_data)
d = pacmap.PaCMAP()
d_out = d.fit_transform(sample_data)
e = pacmap.PaCMAP()
e_out = e.fit_transform(sample_data)
print('Experiment on a standard dataset has been done successfully.')

sample_small_data = np.random.normal(size=(40, 60)) # dim > size
f = pacmap.PaCMAP(random_state=20)
f_out = f.fit_transform(sample_small_data)
print('Experiment on a small dataset has been done successfully.')


try:
    assert(np.sum(np.abs(b_out-c_out))<1e-8)
    print("The output is deterministic.")
except AssertionError:
    print("The output is not deterministic.")
    try:
        assert(np.sum(np.abs(b.pair_FP.astype(int)-c.pair_FP.astype(int)))<1e-8)
        assert(np.sum(np.abs(b.pair_MN.astype(int)-c.pair_MN.astype(int)))<1e-8)
    except AssertionError:
        print('The pairs are not deterministic')
        for i in range(5000):
            if np.sum(np.abs(b.pair_FP[i] - c.pair_FP[i])) > 1e-8:
                print("FP")
                print(i)
                print(b.pair_FP[i])
                print(c.pair_FP[i])
                break
        for i in range(5000):
            if np.sum(np.abs(b.pair_MN[i] - c.pair_MN[i])) > 1e-8:
                print('MN')
                print(i)
                print(b.pair_MN[i])
                print(c.pair_MN[i])
                break

# FMNIST
fmnist = np.load("/Users/hyhuang/Desktop/MNIST/fmnist_images.npy", allow_pickle=True)
fmnist = fmnist.reshape(fmnist.shape[0], -1)
labels = np.load("/Users/hyhuang/Desktop/MNIST/fmnist_labels.npy", allow_pickle=True)
reducer = pacmap.PaCMAP(n_dims=2, n_neighbors=10, MN_ratio=0.5, FP_ratio=2.0, random_state=20)
embedding = reducer.fit_transform(fmnist, init="pca")
plt.scatter(embedding[:, 0], embedding[:, 1], s=0.5, c=labels, cmap='Spectral')
plt.savefig("./test_output/test_fmnist_seed.png")

reducer = pacmap.PaCMAP(n_dims=2, n_neighbors=10, MN_ratio=0.5, FP_ratio=2.0)
embedding = reducer.fit_transform(fmnist, init="pca")
plt.scatter(embedding[:, 0], embedding[:, 1], s=0.5, c=labels, cmap='Spectral')
plt.savefig("./test_output/test_fmnist_noseed.png")

# MNIST
mnist = np.load("/Users/hyhuang/Desktop/MNIST/mnist_images.npy", allow_pickle=True)
mnist = fmnist.reshape(mnist.shape[0], -1)
labels = np.load("/Users/hyhuang/Desktop/MNIST/mnist_labels.npy", allow_pickle=True)
reducer = pacmap.PaCMAP(n_dims=2, n_neighbors=10, MN_ratio=0.5, FP_ratio=2.0, random_state=20)
embedding = reducer.fit_transform(mnist, init="pca")
plt.scatter(embedding[:, 0], embedding[:, 1], s=0.5, c=labels, cmap='Spectral')
plt.savefig("./test_output/test_mnist_seed.png")

reducer = pacmap.PaCMAP(n_dims=2, n_neighbors=10, MN_ratio=0.5, FP_ratio=2.0)
embedding = reducer.fit_transform(mnist, init="pca")
plt.scatter(embedding[:, 0], embedding[:, 1], s=0.5, c=labels, cmap='Spectral')
plt.savefig("./test_output/test_mnist_noseed.png")

print('Figures have been generated successfully.')
