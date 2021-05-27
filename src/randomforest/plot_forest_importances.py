import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics

from CombinedScrapper.generator import poke_data_set
from sklearn.inspection import permutation_importance

# %%
# Data generation and model fitting
# ---------------------------------
# We generate a synthetic dataset with only 3 informative features. We will
# explicitly not shuffle the dataset to ensure that the informative features
# will correspond to the three first columns of X. In addition, we will split
# our dataset into training and testing subsets.
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
ds = poke_data_set()
X, y, feature_names = ds.data, ds.target, ds.feature_names
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.30, random_state=42)

# %%
# A random forest classifier will be fitted to compute the feature importances.
from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(random_state=0, criterion="entropy", max_depth=10)
forest.fit(X_train, y_train)
y_pred = forest.predict(X_test)
print(y_pred)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
start_time = time.time()
importances = forest.feature_importances_
std = np.std([
    tree.feature_importances_ for tree in forest.estimators_], axis=0)
elapsed_time = time.time() - start_time

print(f"Elapsed time to compute the importances: "
      f"{elapsed_time:.3f} seconds")

# %%
# Let's plot the impurity-based importance.

forest_importances = pd.Series(importances, index=feature_names)

fig, ax = plt.subplots()
forest_importances.plot.bar(yerr=std, ax=ax)
ax.set_title("Feature importances using MDI")
ax.set_ylabel("Mean decrease in impurity")
fig.tight_layout()

# %%
# We observe that, as expected, the three first features are found important.
#
# Feature importance based on feature permutation
# -----------------------------------------------
# Permutation feature importance overcomes limitations of the impurity-based
# feature importance: they do not have a bias toward high-cardinality features
# and can be computed on a left-out test set.


start_time = time.time()
result = permutation_importance(
    forest, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2)
elapsed_time = time.time() - start_time
print(f"Elapsed time to compute the importances: "
      f"{elapsed_time:.3f} seconds")

forest_importances = pd.Series(result.importances_mean, index=feature_names)

# %%
# The computation for full permutation importance is more costly. Features are
# shuffled n times and the model refitted to estimate the importance of it.
# Please see :ref:`permutation_importance` for more details. We can now plot
# the importance ranking.

fig, ax = plt.subplots()
forest_importances.plot.bar(yerr=result.importances_std, ax=ax)
ax.set_title("Feature importances using permutation on full model")
ax.set_ylabel("Mean accuracy decrease")
fig.tight_layout()
plt.show()

# %%
# The same features are detected as most important using both methods. Although
# the relative importances vary. As seen on the plots, MDI is less likely than
# permutation importance to fully omit a feature.
