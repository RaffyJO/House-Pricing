# -*- coding: utf-8 -*-
"""UAS AI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jV7YHzx2NY4szKKxu7GaWOlEUIj_AVWR

# Exploring data
We will explore the data using pandas.

Take a note that pandas allows us to load data from xlsx Excel (HARGA RUMAH MALANG.xlsx)
"""

import pandas as pd
data = pd.read_excel('HARGA RUMAH MALANG.xlsx', sheet_name = 'Sheet1', skiprows = 1)

print(data)

pd.DataFrame(data['HARGA'].describe())

"""#  Data Preparation

- data.drop(columns='KOTA', inplace=True, axis=1), Operasi ini menghapus
kolom 'KOTA' dari DataFrame ‘data’ karena berisikan nilai yang sama.

- data.GRS = data.GRS.map({'ADA':1,'TIDAK ADA':0}), Operasi ini
mengganti nilai dalam kolom 'GRS' dengan 1 jika nilainya adalah 'ADA' dan
dengan 0 jika nilainya adalah 'TIDAK ADA'.

"""

data.drop(columns='KOTA', inplace=True, axis=1)

data.GRS = data.GRS.map({'ADA':1,'TIDAK ADA':0})

data.head()

"""#  Data Segregation

- Menghapus nilai-nilai di luar kisaran persentil 1 hingga 99 (1%
hingga 99%) dari setiap kolom yang tercantum dalam dataset data untuk
memperbaiki distribusi data dan menghilangkan nilai-nilai yang ekstrem.

"""

data = data[(data.LT>data.LT.quantile(0.01))&(data.LT<data.LT.quantile(0.99))]
data = data[(data.LB>data.LB.quantile(0.01))&(data.LB<data.LB.quantile(0.99))]
data = data[(data.JKT>data.JKT.quantile(0.01))&(data.JKT<data.JKT.quantile(0.99))]
data = data[(data.JKM>data.JKM.quantile(0.01))&(data.JKM<data.JKM.quantile(0.99))]
data = data[(data.HARGA>data.HARGA.quantile(0.01))&(data.HARGA<data.HARGA.quantile(0.99))]

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

X = data.iloc[:,1:]
X

y = data.iloc[:,0]
y

"""# Split Data Into Training and Testing"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

X_train

y_train

"""# Perform Training

- Model machine learning yang digunakan adalah RandomForestRegressor. RandomForest adalah jenis model dalam kategori supervised learning yang dapat
digunakan untuk permasalahan regresi dan klasifikasi. Dalam konteks ini, digunakan
untuk memprediksi harga rumah (sebuah nilai numerik), maka itu merupakan masalah
regresi, dan RandomForestRegressor adalah model yang tepat untuk digunakan.
"""

model = RandomForestRegressor()
model.fit(X_train, y_train)
hasil = model.predict(X_test)

hasil

"""# Prediction"""

def prediksi(LT, LB, JKT, JKM, GRS):
    predict = pd.DataFrame()
    predict['LT'] = [LT]
    predict['LB'] = [LB]
    predict['JKT'] = [JKT]
    predict['JKM'] = [JKM]
    predict['GRS'] = [GRS]
    hasil = model.predict(predict)
    return hasil[0]  # Mengambil nilai prediksi dari array hasil

nilai = prediksi(500, 400, 4, 3, 1)
nilai_miliar = nilai / 1e9  # Konversi ke miliar

print(prediksi(500, 400, 4, 3, 1))
print("{:.2f} miliar".format(nilai_miliar))

"""# Model Evaluation

- Penggunaan Mean Squared Error (MSE) sebagai metrik evaluasi
model memberikan informasi mengenai seberapa baik model dapat memprediksi
harga.
"""

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

r2_score = r2_score(y_test, y_pred)
mae_score = mean_absolute_error(y_test, y_pred)
mse_score = mean_squared_error(y_test, y_pred)
rmse_score = mean_squared_error(y_test, y_pred, squared=True) # RMSE diaktifkan dengan parameter squared=True

print(f'Skor R2: {r2_score}')
print(f'Skor MAE: {mae_score}')
print(f'Skor MSE: {mse_score}')
print(f'Skor RMSE: {rmse_score}')