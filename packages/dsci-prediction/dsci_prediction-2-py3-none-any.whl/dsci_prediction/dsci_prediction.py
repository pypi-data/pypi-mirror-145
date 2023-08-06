
from sklearn.model_selection import train_test_split
import pandas as pd
import argparse
from sklearn.model_selection import cross_validate

import numpy as np
import matplotlib.pyplot as plt


from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.compose import make_column_transformer

import seaborn as sns

def load_data(input_path, output_path):
    
    '''
    Insert comment
    
    '''
    col_names = ["id", "clump", "unif_size", "unif_shape", "adhesion", "epi_size", "nuclei", "chromatin", "nucleoli", "mitoses", "class"]
    dataset = pd.read_csv(str(input_path), names=col_names, sep=",")
    
    return dataset.to_csv(str(output_path), index=False)


def clean_data(input_path, output_path_train, output_path_test):
    '''
    Insert comment
    '''
    
    #cleaning data
    
    df = pd.read_csv(str(input_path))
    df = df[(df != '?').all(axis=1)]
    df['nuclei'] = df['nuclei'].astype(int)
    df = df.drop(columns=["id"])
    
    #replace 2 -> 0 & 4 -> 1 in target class 
    df['class'] = df['class'].replace([2],0)
    df['class'] = df['class'].replace([4],1) 
    
    #split train/test data
    train_df, test_df = train_test_split(df, test_size=0.3, random_state=123)
    train_df.to_csv(str(output_path_train), index=False)
    test_df.to_csv(str(output_path_test), index=False)
    
    
def EDA_plot(train_df, hist_output, boxplot_output):
    
    '''
    Insert comment
    '''
    
    train_df = pd.read_csv(str(train_df))
    X_train = train_df.drop(columns=["class"])
    numeric_looking_columns = X_train.select_dtypes(
        include=np.number).columns.tolist()
    benign_cases = train_df[train_df["class"] == 0]
    malignant_cases = train_df[train_df["class"] == 1]
    
    #plot histogram
    fig = plot_hist_overlay(df0=benign_cases, df1=malignant_cases,
                            columns=numeric_looking_columns, 
                            labels=["0 - benign", "1 -malignant"],
                            fig_no="1")
    fig.savefig(str(hist_output), facecolor="white")
    
    #plot boxplot 
    fig2 = boxplot_plotting(3, 3, 20, 25, numeric_looking_columns, train_df, 2)
    fig2.savefig(str(boxplot_output), facecolor="white")
    
    
    
def build_test_model(train_df, test_df, cross_val_output, tuned_para_output,
                     classification_output, confusion_matrix_output):
    scoring = [
        "accuracy",
        "f1",
        "recall",
        "precision",]
    
    results = {}
    '''
    Insert comment
    '''
    
    
    np.random.seed(123)
    train_df = pd.read_csv(str(train_df))
    test_df = pd.read_csv(str(test_df))
    X_train = train_df.drop(columns=["class"])
    X_test = test_df.drop(columns=["class"])
    y_train = train_df["class"]
    y_test = test_df["class"]
    numeric_looking_columns = X_train.select_dtypes(include=np.number).columns.tolist()
    numeric_transformer = StandardScaler()
    ct = make_column_transformer((numeric_transformer, numeric_looking_columns))
    pipe_knn = make_pipeline(ct, KNeighborsClassifier(n_neighbors=5))
    pipe_dt = make_pipeline(ct, DecisionTreeClassifier(random_state=123))
    pipe_reg = make_pipeline(ct, LogisticRegression(max_iter=100000))
    classifiers = {
        "kNN": pipe_knn,
        "Decision Tree": pipe_dt,
        "Logistic Regression" : pipe_reg}
    
    #cross_val_scores_for_models
    for (name, model) in classifiers.items():
        results[name] = mean_cross_val_scores(
            model,
            X_train,
            y_train,
            return_train_score=True,
            scoring = scoring)
        cross_val_table = pd.DataFrame(results).T
        cross_val_table.to_csv(str(cross_val_output))
        
        #tune hyperparameters 
        np.random.seed(123)
        search = GridSearchCV(pipe_knn,
                              param_grid={'kneighborsclassifier__n_neighbors': range(1,50),
                                          'kneighborsclassifier__weights': ['uniform', 'distance']},
                              cv=10,
                              n_jobs=-1,
                              scoring="recall",
                              return_train_score=True)
        search.fit(X_train, y_train)
        best_score = search.best_score_.astype(type('float', (float,), {}))
        tuned_para = pd.DataFrame.from_dict(search.best_params_, orient='index')
        tuned_para = tuned_para.rename(columns = {0:"Value"})
        tuned_para = tuned_para.T
        tuned_para['knn_best_score'] = best_score
        tuned_para.to_csv(str(tuned_para_output))
        
        #model on test set 
        pipe_knn_tuned = make_pipeline(ct,KNeighborsClassifier(
            n_neighbors=search.best_params_['kneighborsclassifier__n_neighbors'],
            weights=search.best_params_['kneighborsclassifier__weights']))
        pipe_knn_tuned.fit(X_train, y_train)
        
        #classification report 
        report = classification_report(y_test, pipe_knn_tuned.predict(X_test),
                                       output_dict=True, target_names=["benign", "malignant"])
        report = pd.DataFrame(report).transpose()
        report.to_csv(str(classification_output))
        
        #confusion matrix 
        cm = confusion_matrix(y_test, pipe_knn_tuned.predict(X_test), labels=pipe_knn_tuned.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=pipe_knn_tuned.classes_)
        disp.plot()
        plt.savefig(str(confusion_matrix_output))
        from sklearn.model_selection import cross_validate
        

def mean_cross_val_scores(model, X_train, y_train, **kwargs):
    """
    Returns mean of cross validation of given model, X_train, y_train 
    Parameters
    -----------
    model :
        scikit-learn model
    X_train : numpy array or pandas DataFrame
        X in the training data
    y_train : numpy array or pandas DataFrame
        y in the training data
    Returns
    -----------
        pandas Series with mean scores from cross_validation
    """
    scores = cross_validate(model, X_train, y_train, **kwargs)
    mean_scores = pd.DataFrame(scores).mean()
    out_col = []

    for i in range(len(mean_scores)):
        out_col.append(mean_scores[i])

    return pd.Series(data=out_col, index=mean_scores.index)
    
    
def boxplot_plotting (num_rows,num_columns,width,height,variables,datafr,number):
    
    """
    A function which returns a given number of boxplots for different target  
    against each numerical feature. The returning objects are seaborn.boxplot types. 
    -------------------
    PARAMETERS:
    A dataframe containing the variables and their correspondent labels
    Variables: A list of each variable's name
    num_rows and num_columns: An integer and positive number for both num_rows and num_columns for the
    boxplot fig "canvas" object where our boxplots will go,
    width: A positive width measure 
    length: A positive length measure 
    A binary class label 
    A column array for managing variable names
    A training dataframe object
    Integer positive number for correct ordering  of graphs 
    -------------------
    REQUISITES:
    The target labels ("class label") must be within the data frame 
    The multiplication between num_rows and num_columns must return be equal to num_variables.
    It is possible for num_rows & num_columns to be values that when multiplied don't equal the "variables" numeric value,
    but that will create more boxplots which will be empty. 
    
    --------------------
    RETURNS:
    It returns a fixed number "num_variables" of boxplot objects. Each Boxplot represents both Target Class
    Labels according to a given Variable
    --------------------
    Examples
    datafr=train_df
    --------
    boxplot_plotting (3,3,20,25,numeric_column,datafr,number)
    """
    
    fig,ax= plt.subplots(num_rows,num_columns,figsize=(width,height))
    for idx, (var,subplot) in enumerate(zip(variables,ax.flatten())):
        a = sns.boxplot(x='class',y=var,data=datafr,ax=subplot).set_title (f"Figure {number}.{idx}:Boxplot of {var} for each target class label")
    return fig
         
         

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_hist_overlay(df0, df1, columns, labels, fig_no="1",alpha=0.7, bins=5, **kwargs):
    """
    A function that plot multiple histogram for a target
    classification label against each numerical features.
    The resulting histograms will be a grid layout contained in
    one single Figure object
    REQUIRED: target label are binary i.e 0 or 1, negative or positive
    Parameters
    -------
    df0:
        A pandas DataFrame that is corresponded to the label 0
    df1:
        A pandas DataFrame that is corresponded to the label 1
    columns:
        A list of column name
    labels: 
        A list of label for each of the histograms for each label
    fig_no: optional, default="1"
        A string denoting the figure number, in the case of multiple figures
    alpha: optional, default=0.7
        A float denotes the alpha value for the matplotlib hist function
    bin: optional, default=5
        An int denotes the number of bins for the matplotlib hist function
    **kwargs:
        Other parameters for the plotting function 
    Returns
    -------
    A matplotlib.figure.Figure object
    Examples
    -------
    benign_cases = train_df[train_df["class"] == 0]   # df0             
    malignant_cases = train_df[train_df["class"] == 1] # df1
    plot_hist_overlay(benign_cases, malignant_cases,["unif_size"], labels=["0 - benign", "1 - malignant"]
    
    """
    
    # To automatically calculating the size of dimension of the figures (Square shape)
    size = len(columns)
    dim = np.ceil(np.sqrt([size])).astype(int)[0]
    fig = plt.figure(1, figsize=(22,22))
         
    for idx, x in enumerate(columns):
        subplot=plt.subplot(dim, dim, idx+1)
        col_name = x.title().replace("_", " ")
        subplot.hist(df0[x], alpha=alpha, bins=bins, label=labels[0], **kwargs)
        subplot.hist(df1[x], alpha=alpha, bins=bins, label=labels[1], **kwargs)
        subplot.legend(loc="upper right")
        subplot.set_xlabel(col_name, fontsize=14)
        subplot.set_ylabel("Count", fontsize=14)
        subplot.set_title(f"Figure {fig_no}.{idx+1}: Histogram of {col_name} for each target class label", fontsize=14)
    
    #fig.suptitle(f"Figure {fig_no}: Distribution of the target class for each numeric feature", fontsize=20)
    return fig