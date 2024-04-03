import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from data_preprocessing_Unity import read_csv
import matplotlib.pyplot as plt

# Load your training data
labels, features = read_csv('/path/to/training/data.csv')

# Scale features
scaler = StandardScaler().fit(features)
features_scaled = scaler.transform(features)

# Initialize and train MLP
mlp = MLPClassifier(hidden_layer_sizes=(100,), max_iter=300, activation='relu', solver='adam', random_state=1)
mlp.fit(features_scaled, labels)

# Load testing data
_, X_new = read_csv('/path/to/testing/data.csv')
X_new_scaled = scaler.transform(X_new)

# Predict probabilities and calculate interpolated costs
probabilities = mlp.predict_proba(X_new_scaled)
costs_array = np.array([costs[class_label] for class_label in mlp.classes_])
interpolated_costs = np.dot(probabilities, costs_array)

# Saving the results
predicted_classes = mlp.classes_[np.argmax(probabilities, axis=1)]
results = pd.DataFrame({'Predicted_Class': predicted_classes, 'Interpolated_Cost': interpolated_costs})
results.to_csv('predicted_classes_and_costs.csv', index=False)

# Load the saved results (if necessary, or directly use the arrays)
results = pd.read_csv('predicted_classes_and_costs.csv')
interpolated_costs = results['Interpolated_Cost'].values

# Correctly reshape the costs array. Ensure these dimensions match your actual data's structure.
cost_map = interpolated_costs.reshape(correct_row_count, correct_column_count)

# If you need to swap the x and y axes (transpose the matrix)
cost_map_transposed = cost_map.T

# Visualization
plt.figure(figsize=(10, 7))
plt.imshow(cost_map_transposed, cmap='Greys', interpolation='nearest')
plt.colorbar(label='Interpolated Cost')
plt.title('Global Costmap of the Area')
plt.xlabel('Column Index')
plt.ylabel('Row Index')
plt.savefig('global_costmap_transposed.png')
