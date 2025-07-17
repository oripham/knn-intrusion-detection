from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import matplotlib.pyplot as plt
import joblib


from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

import warnings

warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.float_format', lambda x: '%.3f' % x)
plt.rcParams["figure.figsize"] = (10, 6)

# Load dataset
df_train = pd.read_csv("KDDTrain+.txt", header=None)
df_test = pd.read_csv("KDDTest+.txt", header=None)

# Define column names
columns = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land',
           'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised',
           'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
           'num_access_files', 'num_outbound_cmds', 'is_host_login', 'is_guest_login', 'count',
           'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
           'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
           'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
           'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
           'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate',
           'attack', 'level']
df_train.columns = columns
df_test.columns = columns

# Drop 'level' column as it's not needed
df_train.drop(columns=['level'], inplace=True)
df_test.drop(columns=['level'], inplace=True)

# Preprocessing improvements


def preprocess_data(df):
    # Convert attack labels to binary (normal vs attack)
    df['attack'] = df['attack'].apply(
        lambda x: 'normal' if x == 'normal' else 'attack')
    return df


df_train = preprocess_data(df_train)
df_test = preprocess_data(df_test)

# Separate features and target
X_train = df_train.drop(columns=['attack'])
y_train = df_train['attack']

X_test = df_test.drop(columns=['attack'])
y_test = df_test['attack']

encoder = LabelEncoder()
for col in ['protocol_type', 'service', 'flag']:
    X_train[col] = encoder.fit_transform(X_train[col])
    X_test[col] = encoder.transform(X_test[col])

# Enhanced feature selection

# Use Random Forest for feature importance
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
feature_importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': rf.feature_importances_
})
top_features = feature_importance.nlargest(20, 'importance')[
    'feature'].tolist()
X_train = X_train[top_features]
X_test = X_test[top_features]

# Improved scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


k = 6  # Adjust based on experimentation

# Try different distance metrics
# Options: 'euclidean', 'manhattan', 'minkowski', 'chebyshev'
distance_metric = 'chebyshev'

# Use weighted KNN
weighting = 'uniform'  # Options: 'uniform', 'distance'

model = KNeighborsClassifier(
    n_neighbors=k,
    metric=distance_metric,
    weights=weighting
)

model.fit(X_train, y_train)

# Lưu mô hình đã huấn luyện
joblib.dump(model, 'knn_model.pkl')

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
print(f"Improved Accuracy: {accuracy:.2%}")
