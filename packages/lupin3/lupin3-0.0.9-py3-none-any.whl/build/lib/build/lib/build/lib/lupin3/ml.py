import datetime

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
import pickle
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from matplotlib import pyplot as plt
from xgboost import XGBClassifier,plot_importance
from sklearn.metrics import accuracy_score,recall_score,confusion_matrix



# def gen_filename():
#     filename = func.date2str(datetime.datetime.now().date())



def ML_LogisticRegression_train(data, labelcolname, size=0.25, penalty='l2', showcoef=False, showmatch=False,
                                savefilename='lg.pickle', **kwargs):
    X = data[[x for x in data.columns if x != labelcolname]]
    y = data[labelcolname]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size)

    # 标准化处理
    std = StandardScaler()
    X_train = std.fit_transform(X_train)
    X_test = std.transform(X_test)

    # 模型训练
    # 创建一个逻辑回归估计器
    lg = LogisticRegression(penalty=penalty, C=1.0)
    # 训练模型，进行机器学习
    lg.fit(X_train, y_train)
    # 得到模型，打印模型回归系数，即权重值

    with open(savefilename, 'wb') as fw:
        pickle.dump(lg, fw)

    if showcoef is True:
        print("logist回归系数为:\n", lg.coef_)
    else:
        pass
    # return estimator
    # 模型评估
    y_predict = lg.predict(X_test)
    y_proba = lg.predict_proba(X_test)
    y_proba = y_proba.max(axis=1)
    # print(y_proba.max(axis = 1))

    if showmatch is True:
        print("预测值为:\n", y_predict)
        print("真实值与预测值比对:\n", y_predict == y_test)
    else:
        pass
    rate = lg.score(X_test, y_test)
    print("直接计算准确率为:\n", rate)

    # 打印精确率、召回率、F1 系数以及该类占样本数
    labelsclass = list(set(y.tolist()))
    print(labelsclass)
    print("精确率与召回率为:\n", classification_report(y_test, y_predict, labels=labelsclass))

    # ###模型评估
    # #ROC曲线与AUC值
    print("AUCpredict值:\n", roc_auc_score(y_test, y_predict))
    print("AUCproba值:\n", roc_auc_score(y_test, y_proba))


def ML_predict(modelfile, dataset):
    with open(modelfile, 'rb') as fr:
        new_lg = pickle.load(fr)
        print(new_lg.predict([dataset]))


def ML_SVM_train(data,labelcolname,size= 0.25,savefilename='svm.pickle'):
    X = data[[x for x in data.columns if x != labelcolname]]
    y = data[labelcolname]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size)

    # 标准化处理
    std = StandardScaler()
    X_train = std.fit_transform(X_train)
    X_test = std.transform(X_test)



    from sklearn import svm
    predictor = svm.SVC(gamma='auto', C=1.0, decision_function_shape='ovr', kernel='rbf')
    predictor.fit(X_train, y_train)
    with open(savefilename, 'wb') as fw:
        pickle.dump(predictor, fw)
    # # 预测结果
    result = predictor.predict(X_test)
    # # 进行评估
    from sklearn.metrics import f1_score
    print("F-score: {0:.2f}".format(f1_score(result, y_test, average='micro')))

def ML_RandomForest_train(data,labelcolname,size= 0.25,savefilename='rf.pickle',showestimators=False,estimatornum = 100):
    X = data[[x for x in data.columns if x != labelcolname]]
    y = data[labelcolname]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size)



    clf = DecisionTreeClassifier(random_state=0)
    rfc = RandomForestClassifier(random_state=0)
    clf = clf.fit(X_train, y_train)
    rfc = rfc.fit(X_train, y_train)
    score_c = clf.score(X_test, y_test)
    score_r = rfc.score(X_test, y_test)

    with open(savefilename, 'wb') as fw:
        pickle.dump(rfc, fw)


    print("Single Tree:{}".format(score_c), "Random Forest:{}".format(score_r))

    rfc_l = []
    clf_l = []

    for i in range(10):
        rfc = RandomForestClassifier(n_estimators=25)
        rfc_s = cross_val_score(rfc, X, y, cv=10).mean()
        rfc_l.append(rfc_s)
        clf = DecisionTreeClassifier()
        clf_s = cross_val_score(clf, X, y, cv=10).mean()
        clf_l.append(clf_s)

    plt.plot(range(1, 11), rfc_l, label="Random Forest")
    plt.plot(range(1, 11), clf_l, label="Decision Tree")
    plt.legend()
    plt.show()


    if showestimators == False:
        pass
    else:

        superpa = []
        for i in range(estimatornum):
            rfc = RandomForestClassifier(n_estimators=i + 1, n_jobs=-1)
            rfc_s = cross_val_score(rfc, X, y, cv=10).mean()
            superpa.append(rfc_s)
        print(max(superpa), superpa.index(max(superpa)))
        plt.figure(figsize=[20, 5])
        plt.plot(range(1, estimatornum + 1), superpa)
        plt.show()

        rfc = RandomForestClassifier(n_estimators=25)
        rfc = rfc.fit(X_train, y_train)
        rfc.score(X_test, y_test)

        rfc.feature_importances_
        rfc.apply(X_test)
        rfc.predict(X_test)
        rfc.predict_proba(X_test)

def ML_XGBoost_train(data,labelcolname,size = 0.25,savefilename = 'xgb.pickle',max_depth_num = 5,gamma = 0.01,objective ="binary:logistic", eta=0.1,roundnum = 2000):

    X = data[[x for x in data.columns if x != labelcolname]]
    y = data[labelcolname]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size)
    # 重要参数：
    xgb_model = XGBClassifier(max_depth=max_depth_num,
                              eta=eta,
                              gamma=gamma,
                              min_child_weight=6,
                              objective=objective,
                              num_round=roundnum
                              )

    xgb_model.fit(
        X_train,
        y_train,
        eval_set=None,
        eval_metric='mlogloss',  # 评估函数，字符串类型，例如：'mlogloss'
        early_stopping_rounds=None,
        verbose=True,  # 间隔多少次迭代输出一次信息
        xgb_model=None
    )

    with open(savefilename, 'wb') as fw:
        pickle.dump(xgb_model, fw)

    y_pred = xgb_model.predict(X_test)  # 返回各个样本属于各个类别的概率

    accuracy = accuracy_score(y_test, y_pred)
    print('accuracy:%2.f%%' % (accuracy * 100))
    recall = recall_score(y_test, y_pred)
    print('recall:%2.f%%' % (recall * 100))

    confusion_matrix(y_test, y_pred)
    plot_importance(xgb_model)

