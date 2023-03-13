# Import libraries
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, balanced_accuracy_score, auc , precision_recall_curve
from xgboost import XGBClassifier
import lightgbm as lgb

def callmodel(df, model, separatetestset=False, testsetdf=None, f1=False, precisionscore=False, recallscore=False, cm=False, aucpr=False, prauc=False, all=False):
    # Takes a dataframe and a model to fit

    # Prepares test and training set
    x = df.drop(columns=['label'])
    y = df["label"]
    if separatetestset == False:
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42, stratify=y)
    else:
        x_train = x 
        y_train = y
        x_test = testsetdf.drop(columns=['label'])
        y_test = testsetdf["label"]
    
    # Creates model, train and predicts on test set
    if model == 'randomforest':
        clf = RandomForestClassifier(random_state=1)

    if model =='xgboost':
        clf = XGBClassifier()

    if model =='svc':
        clf = SVC(kernel= 'rbf', random_state=1)

    if model == 'lgbm':
        clf = lgb.LGBMClassifier()

    if model == 'final':
        clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 2, min_samples_leaf= 4, max_depth = 30, bootstrap = True)

    return prediction(clf, x_train, x_test, y_train, y_test, f1=f1, precisionscore=precisionscore, recallscore=recallscore, cm=cm, aucpr=aucpr, prauc=prauc, all=all)

def prediction(model, x_train, x_test, y_train, y_test, f1, precisionscore, recallscore, cm, aucpr, prauc, all):
    # Fits model, predicts on test data and prints out statistics 
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    
    precision, recall, _ = precision_recall_curve(y_test, y_pred)
    auc_pr = auc(recall, precision)
    f1score = f1_score(y_test, y_pred)*100
    matrix = confusion_matrix(y_test, y_pred)
    
    if f1 == True:
        return f1score
    
    if precisionscore == True:
        return precision
    
    if recallscore == True:
        return recall
    
    if cm == True:
        matrix = matrix.flatten()
        return list(matrix)
    
    if aucpr == True:
       return auc_pr
    
    if prauc == True:
        return list(precision), list(recall), auc_pr
    
    if all ==True: 
        print('F1-score: ', f1score)
        print('Precision: ', precision[1]*100)
        print('Recall: ', recall[1]*100)
        print('AUC_PR: ', auc_pr)
        print('Confusion Matrix: ', list(matrix.flatten()))
        output = [matrix.flatten(), accuracy_score(y_test, y_pred)*100, f1_score(y_test, y_pred)*100 , balanced_accuracy_score(y_test, y_pred)*100, auc_pr , precision, recall ]    
        return output
