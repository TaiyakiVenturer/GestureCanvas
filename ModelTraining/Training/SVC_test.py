import os
import sys
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split, StratifiedKFold

parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(parent_path)
from Models import _LoadSave as LoadSave

dir_path = os.path.dirname(os.path.abspath(__file__))
np.set_printoptions(suppress=True)

X, y = LoadSave.load_dataset(1)

# 數據標準化
X_flatten = X.reshape(X.shape[0], -1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_flatten)

'''
# 資料分割
X_train, X_test, y_train_original, y_test_original = train_test_split(
    X_flatten, y, test_size=0.2, random_state=1, stratify=y
)
'''

# 數據標準化
X_flatten = X.reshape(X.shape[0], -1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_flatten)

# 進行網格搜索調優
c_gamma_range = [0.01, 0.1, 1.0, 10.0]

param_grid = [{'C': c_gamma_range,
               'kernel': ['linear']},
              {'C': c_gamma_range,
               'gamma': c_gamma_range,
               'kernel': ['rbf']}]


skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)
gs = GridSearchCV(estimator=SVC(random_state=1),
                  param_grid=param_grid,
                  scoring='f1',
                  cv=skf,  # 使用分層交叉驗證
                  n_jobs=-1,
                  verbose=0)  # 減少輸出的訊息

#gs = gs.fit(X_train, y_train)
gs = gs.fit(X_scaled, y)

# 使用最佳模型進行預測
SVC_model = gs.best_estimator_

num = 1
LoadSave.save_model(SVC_model, f"SVC_{num}")
LoadSave.save_scaler(scaler, f"SVC_{num}")