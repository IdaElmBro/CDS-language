import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def visualize(words, model):
# an empty list for vectors
    X = []
# get vectors for subset of words
    for word in words:
        X.append(model[word])

# Use PCA for dimensionality reduction to 2D
    pca = PCA(n_components=2)
    result = pca.fit_transform(X)

# or try SVD - how are they different?
#svd = TruncatedSVD(n_components=2)
# fit_transform the initialized PCA model
#result = svd.fit_transform(X)

# create a scatter plot of the projection
    plot = plt.scatter(result[:, 0], result[:, 1])


# for each word in the list of words
    for i, word in enumerate(words):
        plt.annotate(word, xy=(result[i, 0], result[i, 1]))

    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
 
# displaying the title
    plt.title("Dimensionality reduction")
 
    return plot