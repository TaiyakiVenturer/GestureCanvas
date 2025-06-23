import os
import sys
import math
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from typing import cast, List, Union
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(parent_path)

from Models import _LoadSave as LoadSave
from ModelTraining.Testing.LiveTest_DataProcessing import LiveTest_DataProcessor as DataProcessor

ModelType = Union[SVC, RandomForestClassifier]

class GestureCanvas_Compare:
    def __init__(self):
        #模型串列
        self.models: List[ModelType] = []
        self.models.append(cast(SVC, LoadSave.load_model("SVC_1")))
        self.models.append(cast(RandomForestClassifier, LoadSave.load_model("RandomForest_100")))

        self.scalers: List[StandardScaler] = []
        self.scalers.append(cast(StandardScaler, LoadSave.load_scaler("SVC_1")))
        self.scalers.append(cast(StandardScaler, LoadSave.load_scaler("RandomForest_100")))
        
        self.models_name: List[str] = ["SVC1", "RF1"]
        self.results = {}

        print("Model loaded.")

    def load_data(self):
        self.X, self.y = LoadSave.load_dataset(1)
        self.unique_labels = np.unique(self.y)  #取得特徵
        
        #數據標準化
        self.X_flatten = self.X.reshape(self.X.shape[0], -1)
        scaler = StandardScaler()
        self.X_scaled = scaler.fit_transform(self.X_flatten)

    def evaluate_models(self):
        """
        評估所有模型
        """
        if self.X is None or self.y is None:
            raise ValueError("請先載入測試資料")
            
        if not self.models:
            raise ValueError("請先載入至少一個模型")
        
        print("Start evaluate...")
        
        count = 0
        for model in self.models:
            #預測
            y_pred = model.predict(self.X_scaled)
                
            #計算指標
            acc = accuracy_score(self.y, y_pred)
            f1 = f1_score(self.y, y_pred, average='weighted')
            cm = confusion_matrix(self.y, y_pred)
            
            #儲存結果
            self.results[count] = {
                'accuracy': acc,
                'f1_score': f1,
                'confusion_matrix': cm,
                'predictions': y_pred
            }
            
            print(f"{self.models_name[count]} 評估完成")
            count += 1

    def display_results(self):
        """
        顯示所有模型的性能結果
        """
        if not self.results:
            print("尚無評估結果，請先執行 evaluate_models()")
            return
        
        print("\n" + "="*60)
        print("模型性能比較結果")
        print("="*60)
        
        #創建結果表格
        results_df = pd.DataFrame(
            {
                'Model': name,
                'Accuracy': result['accuracy'],
                'F1 Score': result['f1_score']
            }for name, result in zip(self.models_name, self.results.values())
        )

        results_df = results_df.round(4)
        print("\n性能指標總覽:")
        print(results_df)
        
        #找出最佳模型
        best_acc_model = results_df['Accuracy'].idxmax()
        best_f1_model = results_df['F1 Score'].idxmax()
        
        print(f"\n最佳準確率模型: {self.models_name[int(results_df['Accuracy'].idxmax())]} ({results_df.loc[best_acc_model, 'Accuracy']:.4f})")
        print(f"最佳F1分數模型: {self.models_name[int(results_df['F1 Score'].idxmax())]} ({results_df.loc[best_f1_model, 'F1 Score']:.4f})")
    
    def display_com(self):
        #取得模型數量
        num_models = len(self.models_name)

        cols = math.ceil(math.sqrt(num_models))
        rows = math.ceil(num_models / cols)

        #建立子圖
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))

        #畫圖
        for idx, (name, result) in enumerate(zip(self.models_name, self.results.values())):
            row = idx // cols
            col = idx % cols

            # 如果只有 1 行 1 列，axes 會不是 2D，需要特判
            ax = axes[row][col] if rows > 1 else (axes[col] if num_models > 1 else axes)

            sns.heatmap(
                result['confusion_matrix'], 
                annot=True, 
                fmt='d', 
                cmap='Blues', 
                ax=ax,
                xticklabels=self.unique_labels.tolist(),
                yticklabels=self.unique_labels.tolist())
            
            ax.set_title(f"{name} - Confusion Matrix")
            ax.set_xlabel("Predicted")
            ax.set_ylabel("True")

        #如果圖不滿，要關掉空白子圖
        for idx in range(num_models, rows * cols):
            row = idx // cols
            col = idx % cols
            ax = axes[row][col] if rows > 1 else axes[col]
            ax.axis('off')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    canvas = GestureCanvas_Compare()
    canvas.load_data()
    canvas.evaluate_models()
    canvas.display_results()
    canvas.display_com()