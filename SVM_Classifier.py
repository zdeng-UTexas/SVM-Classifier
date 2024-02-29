from data_preprocessing import read_csv
import numpy as np
import pandas as pd

from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
# from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

labels, features = read_csv('/Users/zhiyunjerrydeng/AEROPlan/embeddings_256_training.csv')

print(labels)
print(features.shape)


## SVM Classifier

X_train = features
y_train = labels

# Scale features
scaler = StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)

# Define parameter range for grid search
param_grid = {
    'C': [0.1, 1, 10, 100], 
    'gamma': ['scale', 'auto', 0.01, 0.1, 1],
    'kernel': ['linear', 'rbf', 'poly']
}

# Grid search for best parameters
grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=2)
grid.fit(X_train_scaled, y_train)

# View the best parameters
# print("Best parameters found: ", grid.best_params_)

# Use the best estimator for predictions
clf_best = grid.best_estimator_

## Predicting

temp, X_new = read_csv('/Users/zhiyunjerrydeng/AEROPlan/embeddings_256_testing.csv')
# print(temp)

# Preprocess the new dataset (e.g., feature scaling)
X_new_scaled = scaler.transform(X_new)

# Step 2: Make predictions
y_pred = clf_best.predict(X_new_scaled)

# y_pred is now your prediction vector, matching the shape of y_train
# (assuming the number of samples is the same)

print(y_pred.shape)

# print(y_pred)
y_pred_df = pd.DataFrame(y_pred, columns=['Predicted'])
# Save to CSV
y_pred_df.to_csv('/Users/zhiyunjerrydeng/AEROPlan/embeddings_256_predictive_class.csv', header=False, index=False)


## Assign cost 
class_to_number = {
    'dry_grass': 1,
    'fresh_grass': 1,
    'shrubbery': 3,
    'smooth_concrete': 0,
    'tree': 2
}

y_pred_cost = [class_to_number[label] for label in y_pred]
y_pred_cost_df = pd.DataFrame(y_pred_cost, columns=['Cost'])
y_pred_cost_df.to_csv('/Users/zhiyunjerrydeng/AEROPlan/embeddings_256_predictive_cost.csv', header=False, index=False)
