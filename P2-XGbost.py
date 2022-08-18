import numpy as np
from sklearn.model_selection import train_test_split
import xlrd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_validate, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.svm import SVR
import xgboost as xgb
from xgboost import plot_importance

X = np.transpose(np.load('data/data/GRA_deCor_DATA.npy'), (1, 0))
Y = np.load('pIC50.npy')
name = np.load('data/data/GRA_deCor_NAME.npy')

# X = preprocessing.StandardScaler().fit_transform(X)
min_max_scaler = preprocessing.MinMaxScaler()
Y = min_max_scaler.fit_transform(Y.reshape(-1, 1))


def getTest(name):
    ret_x = []
    Molecular_Descriptor = r'Molecular_Descriptor.xlsx'
    Molecular_Descriptor = xlrd.open_workbook(Molecular_Descriptor)
    test_Molecular_Descriptor = Molecular_Descriptor.sheet_by_name('test')

    for id in name:
        ret_x.append(test_Molecular_Descriptor.col_values(test_Molecular_Descriptor.row_values(0).index(id))[1:])
    return np.transpose(np.array(ret_x), (1, 0))


params = {
    'booster': 'gbtree',
    'objective': 'reg:gamma',
    'gamma': 0.1,
    'max_depth': 5,
    'lambda': 3,
    'subsample': 0.7,
    'colsample_bytree': 0.7,
    'min_child_weight': 3,
    'slient': 1,
    'eta': 0.1,
    'seed': 1000,
    'nthread': 4,
}

# model = KNeighborsRegressor(n_neighbors=32)
# model = RandomForestRegressor()
# model = GradientBoostingRegressor()
# model = DecisionTreeRegressor()
# model = GridSearchCV(SVR(kernel='poly',C=10,degree=2), cv=5,param_grid={"C": [1e0, 1e1, 1e2, 1e3],"gamma": np.logspace(-2, 2, 5)})
# model = SVR(kernel='rbf',C=10,degree=2)
# model = ExtraTreesRegressor()

import xlwt

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)


workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('1')
ret = []
dtrain = xgb.DMatrix(x_train, y_train)
model = xgb.XGBRegressor()
for i in range(100):
    x_train1, x_test1, y_train1, y_test1 = train_test_split(x_train, y_train, test_size=0.8)

    model.fit(X=x_train1, y=y_train1)
    prds = model.predict(x_test)
    ret.append(prds)
    print('MAE:%.4f MSE:%.4f RMSE:%.4f R2 Score:%.4f' % (mean_absolute_error(y_test, prds),
                                                         mean_squared_error(y_test, prds),
                                                         np.sqrt(mean_squared_error(y_test, prds)),
                                                         r2_score(y_test, prds)))
    # worksheet.write(i, 0, mean_absolute_error(y_test,prds))
    #
    # worksheet.write(i, 1, mean_absolute_error(y_test,prds))
    # # worksheet.write(j, 1, mean_squared_error(y_test,y_pred))
    # worksheet.write(i, 2, np.sqrt(mean_squared_error(y_test,prds)))
    # worksheet.write(i, 2, r2_score(y_test,prds))
print(np.array(ret).shape)
print(ret)

ret = np.array(ret)
print(ret.shape)
for i in range(x_test.shape[0]):
    worksheet.write(i, 0, float(y_test[i]))
    print(ret[:,i])
    worksheet.write(i, 1, float(np.min(ret[:,i])))
    worksheet.write(i, 2, float(np.max(ret[:,i])))
workbook.save('data/ret/wucha.xls')

# r = len(x_test) + 1
# plt.plot(np.arange(1, r), prds, 'go-', label="predict")
# plt.plot(np.arange(1, r), y_test, 'co-', label="real")
# plt.legend()
# plt.show()
