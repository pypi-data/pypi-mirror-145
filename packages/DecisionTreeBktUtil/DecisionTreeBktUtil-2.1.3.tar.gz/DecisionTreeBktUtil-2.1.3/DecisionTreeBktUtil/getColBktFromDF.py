# python环境
# %matplotlib  inline
import pandas as pd
import sys
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import *
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import matplotlib.pyplot as plt

# 模型
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree._export import _BaseTreeExporter
import graphviz
from sklearn.tree import export_text



# 决策树版本
# @column: 特征列
# @label: 标签列
#@return： 返回特征名的分桶点
def getFeatureBkt_DT(DF, featureCol, labelCol):

    # 输入打印的字符串，返回分桶值
    def get_bkt_from_export_text(export_text):
        bkt_list = []
        result = []
        # 先写入
        with open("tep.txt", 'w', encoding='utf-8') as w:
            w.write(export_text)
        # 再读取
        with open("tep.txt", 'r') as source:
            txt = source.readlines()
            for i in range(0, len(txt)):
                bkt_value = float(txt[i].split(" ")[-1].replace("\n", ""))
                bkt_list.append(bkt_value)
            # print(sorted(set(bkt_list)))
        return sorted(set(bkt_list))

    DF = DF.fillna(0)
    # 取出单特征和标签
    x, y = DF[featureCol].values, DF[labelCol].values
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    # 开始训练
    clf = DecisionTreeClassifier(max_depth=10)
    clf=clf.fit(x_train.reshape(-1, 1), y_train.reshape(-1, 1))
    # 方法1 ： plot_tree
    tree.plot_tree(clf)
    # 方法2 ： graphviz
    # 方法3 ： export_text
    r = export_text(clf, feature_names=[featureCol]) # 返回值 str类型
    # 输入打印的结果，返回分桶值
    bkt_list = get_bkt_from_export_text(r)
    print("'%s': %s" %(featureCol, bkt_list))

# GBDT版本
def getFeatureBkt_GBDT(DF, featureCol, labelCol):
    DF = DF.fillna(0)
    # 取出单特征和标签
    x, y = DF[featureCol].values, DF[labelCol].values
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    # 开始训练
    clf = GradientBoostingRegressor(n_estimators=3, learning_rate=1.0,max_depth=2, random_state=0)
    clsf = clf.fit(x_train.reshape(-1, 1), y_train)
    n_estimators=clsf.n_estimators_
#     tree.plot_tree(clf.estimators_[0][0])
#     tree.plot_tree(clf.estimators_[1][0])
    tree.plot_tree(clf.estimators_[2][0])
    r = export_text(clf, feature_names=[featureCol])
    print(r)
