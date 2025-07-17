import pandas as pd
import joblib
import warnings
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

warnings.filterwarnings('ignore')
pd.set_option('display.float_format', lambda x: '%.3f' % x)
plt.rcParams["figure.figsize"] = (10, 6)

# 1. Tải dữ liệu
df_train = pd.read_csv("KDDTrain+.txt", header=None)
df_test = pd.read_csv("KDDTest+.txt", header=None)

# 2. Gán tên cột
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

df_train.drop(columns=['level'], inplace=True)
df_test.drop(columns=['level'], inplace=True)

# 3. Tiền xử lý
def preprocess(df):
    df = df.copy()
    df['attack'] = df['attack'].apply(lambda x: 'normal' if x == 'normal' else 'attack')
    return df

df_train = preprocess(df_train)
df_test = preprocess(df_test)

X_train = df_train.drop(columns=['attack'])
y_train = df_train['attack']
X_test = df_test.drop(columns=['attack'])
y_test = df_test['attack']

# 4. Encode các cột phân loại và lưu lại encoder
categorical_cols = ['protocol_type', 'service', 'flag']
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    X_train[col] = le.fit_transform(X_train[col])
    X_test[col] = le.transform(X_test[col])
    encoders[col] = le

# Lưu encoder
joblib.dump(encoders, "encoders.pkl")

# 5. Chọn các đặc trưng quan trọng
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
feature_importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': rf.feature_importances_
})
top_features = feature_importance.nlargest(20, 'importance')['feature'].tolist()

X_train_top = X_train[top_features]
X_test_top = X_test[top_features]

# 6. Chuẩn hóa
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_top)
X_test_scaled = scaler.transform(X_test_top)

joblib.dump(scaler, "scaler.pkl")

# 7. Huấn luyện mô hình
model = KNeighborsClassifier(n_neighbors=6, metric='chebyshev', weights='uniform')
model.fit(X_train_scaled, y_train)

# 8. Lưu model
joblib.dump(model, "knn_model.pkl")
joblib.dump(top_features, "top_features.pkl")

# 9. Đánh giá
y_pred = model.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, pos_label='attack')

print(f"Accuracy: {acc:.2%}")
print(f"F1 Score: {f1:.2%}")
