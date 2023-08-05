import numpy as np
import pandas as pd

#make function to return best sklearn regressor model for given dataframe 
def performance_modelli_regressione(df, lista_colonne_x, colonna_y):
    from sklearn.linear_model import LinearRegression
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import SVR
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.linear_model import ElasticNet
    from sklearn.linear_model import Lasso
    from sklearn.linear_model import Ridge
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.model_selection import cross_val_score
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    regressor = [
        LinearRegression(),
        LogisticRegression(),
        SVR(),
        RandomForestRegressor(),
        GradientBoostingRegressor(),
        ElasticNet(),
        Lasso(),
        Ridge(),
        DecisionTreeRegressor(),
        KNeighborsRegressor()
    ]
    scores = []
    for reg in regressor:
        scores.append(np.mean(cross_val_score(reg, X, Y, cv=5)))
    #add figure size 
    plt.figure(figsize=(15,10))
    plt.bar(range(len(regressor)), scores)
    plt.xticks(range(len(regressor)), [reg.__class__.__name__ for reg in regressor])
    plt.ylabel("Media CV Score")
    plt.title("Comparazione Algoritmi di Regressione")
    plt.show()
    return regressor[np.argmax(scores)]

#make function to return best sklearn classification model for given dataframe 
def performance_modelli_classificazione(df, lista_colonne_x, colonna_y):    
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import cross_val_score
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    regressor = [
        LogisticRegression(),
        SVC(),
        RandomForestClassifier(),
        GradientBoostingClassifier(),
        DecisionTreeClassifier(),
        KNeighborsClassifier()
    ]
    scores = []
    for reg in regressor:
        scores.append(np.mean(cross_val_score(reg, X, Y, cv=5)))
    #add figure size 
    plt.figure(figsize=(15,10))
    plt.bar(range(len(regressor)), scores)
    plt.xticks(range(len(regressor)), [reg.__class__.__name__ for reg in regressor])
    plt.ylabel("Media CV Score")
    plt.title("Comparazione Algoritmi di Classificazione")
    plt.show()
    return regressor[np.argmax(scores)]   


#make funtion to return linear regression on multiple x columns
def regressione_lineare(df, lista_colonne_x, colonna_y):
    from sklearn.linear_model import LinearRegression
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    Y = df[colonna_y]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = Y.values.reshape(-1,1)
    reg = LinearRegression().fit(X, Y)
    #plot regression line
    plt.scatter(X, Y, color='black')
    return reg

#make funtion to return logistic regression on multiple x columns
def regressione_logistica(df, lista_colonne_x, colonna_y):
    from sklearn.linear_model import LogisticRegression
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = LogisticRegression().fit(X, Y)
    return reg

#make funtion to return SVR model on multiple x columns
def regressione_SVR(df, lista_colonne_x, colonna_y):
    from sklearn.svm import SVR
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = SVR().fit(X, Y)
    return reg

#make funtion to return support vector machine model on multiple x columns
def regressione_SVC(df, lista_colonne_x, colonna_y):
    from sklearn.svm import SVC
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = SVC().fit(X, Y)
    return reg

#make funtion to return random forest model on multiple x columns
def regressione_random_forest(df, lista_colonne_x, colonna_y):
    from sklearn.ensemble import RandomForestRegressor
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = RandomForestRegressor().fit(X, Y)
    return reg

#make funtion to return random forest classifier model on multiple x columns
def classificatore_random_forest(df, lista_colonne_x, colonna_y):
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = RandomForestClassifier().fit(X, Y)
    return reg

#make funtion to return gradient boosting model on multiple x columns
def regressione_gradient_boosting(df, lista_colonne_x, colonna_y):
    from sklearn.ensemble import GradientBoostingRegressor
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = GradientBoostingRegressor().fit(X, Y)
    return reg

#make funtion to return gradient boosting classifier model on multiple x columns
def classificatore_gradient_boosting(df, lista_colonne_x, colonna_y):
    from sklearn.ensemble import GradientBoostingClassifier
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = GradientBoostingClassifier().fit(X, Y)
    return reg

#make funtion to return decision tree model on multiple x columns
def regressione_decision_tree(df, lista_colonne_x, colonna_y):
    from sklearn.tree import DecisionTreeRegressor
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = DecisionTreeRegressor().fit(X, Y)
    return reg

#make funtion to return decision tree classifier model on multiple x columns
def classificatore_decision_tree(df, lista_colonne_x, colonna_y):
    from sklearn.tree import DecisionTreeClassifier
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = DecisionTreeClassifier().fit(X, Y)
    return reg

#make function to return KNN model on multiple x columns
def regressione_knn(df, lista_colonne_x, colonna_y):
    from sklearn.neighbors import KNeighborsRegressor
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = KNeighborsRegressor().fit(X, Y)
    return reg

#make function to return KNN classifier model on multiple x columns
def classificatore_knn(df, lista_colonne_x, colonna_y):
    from sklearn.neighbors import KNeighborsClassifier
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = KNeighborsClassifier().fit(X, Y)
    return reg

#make funtion to return elastic net classifier model on multiple x columns
def modello_elastic_net(df, lista_colonne_x, colonna_y):
    from sklearn.linear_model import ElasticNet
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = ElasticNet().fit(X, Y)
    return reg

#make funtion to return Lasso model on multiple x columns
def modello_lasso(df, lista_colonne_x, colonna_y):
    from sklearn.linear_model import Lasso
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = Lasso().fit(X, Y)
    return reg

#make funtion to return Ridge model on multiple x columns
def modello_ridge(df, lista_colonne_x, colonna_y):
    from sklearn.linear_model import Ridge
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    reg = Ridge().fit(X, Y)
    return reg


######################################################################################################

#make function to evaluate model with multiple metrics
# input: model, dataframe, list of columns to be used as x, column to be used as y
# output: dictionary with all metrics
def evaluazione_modello(reg, df, lista_colonne_x, colonna_y):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    y_pred = reg.predict(X)
    y_pred = np.round(y_pred)
    y_pred = y_pred.reshape(-1,1)
    y_pred = pd.DataFrame(y_pred)
    y_pred.columns = [colonna_y]
    df = pd.concat([df, y_pred], axis=1)
    df = df.dropna()
    y_pred = df[colonna_y]
    y_pred = y_pred.values.reshape(-1,1)
    y_pred = y_pred.reshape(-1,1)
    y_pred = y_pred.astype(int)
    y_true = df[colonna_y]
    y_true = y_true.values.reshape(-1,1)
    y_true = y_true.reshape(-1,1)
    y_true = y_true.astype(int)
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import mean_absolute_error
    from sklearn.metrics import r2_score
    from sklearn.metrics import accuracy_score
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import classification_report
    from sklearn.metrics import precision_score
    from sklearn.metrics import recall_score
    from sklearn.metrics import f1_score
    from sklearn.metrics import roc_auc_score
    from sklearn.metrics import roc_curve
    from sklearn.metrics import auc
    from sklearn.metrics import precision_recall_curve
    from sklearn.metrics import average_precision_score
    from sklearn.metrics import precision_recall_fscore_support
    
    #aplly all metrics to the model
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    accuracy = accuracy_score(y_true, y_pred)
    confusion = confusion_matrix(y_true, y_pred)
    report = classification_report(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    auc_roc = roc_auc_score(y_true, y_pred)
    precision_recall_curve = precision_recall_curve(y_true, y_pred)
    average_precision = average_precision_score(y_true, y_pred)
    precision_recall_fscore_support = precision_recall_fscore_support(y_true, y_pred)
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    return {'mse': mse, 'mae': mae, 'r2': r2, 'accuracy': accuracy, 'confusion': confusion, 'report': report, 'precision': precision, 'recall': recall, 'f1': f1, 'auc_roc': auc_roc, 'precision_recall_curve': precision_recall_curve, 'average_precision': average_precision, 'precision_recall_fscore_support': precision_recall_fscore_support, 'fpr': fpr, 'tpr': tpr, 'thresholds': thresholds, 'roc_auc': roc_auc}

#make function to return accuracy score of model on multiple x columns
def valutazione_modello(reg, df, lista_colonne_x, colonna_y):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df[lista_colonne_x]
    X = X.values.reshape(-1,len(lista_colonne_x))
    Y = df[colonna_y]
    Y = Y.values.reshape(-1,1)
    return reg.score(X, Y)

#make funtion to predict y values from x colums values
def predizione_y(reg, df):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    df = df.dropna()
    X = df
    X = X.values.reshape(-1,len(df.columns))
    Y = reg.predict(X)
    return Y

#make funtion to save model
def salva_modello(reg, nome_modello):
    import pickle
    pickle.dump(reg, open(nome_modello, 'wb'))

#make funtion to load model
def carica_modello(nome_modello):
    import pickle
    reg = pickle.load(open(nome_modello, 'rb'))
    return reg