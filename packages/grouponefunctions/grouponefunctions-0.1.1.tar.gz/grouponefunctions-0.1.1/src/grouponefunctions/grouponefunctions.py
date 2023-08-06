import numpy as np
import pandas as pd
import warnings as wa
import matplotlib.pyplot as plt

def split_xy(df, desiredfeatures, target):
    # Split data into target and desired features
    #
    # Takes in a dataframe and extracts the desired features used
    # to predict a specified target variable
    #
    # @param df A data frame.
    # @param desiredfeatures Target feature(s) you desire for your analysis in list or string form
    # @param target The target variable(s) you desire for your analysis in list or string form
    #
    # @return Two data frames or series each with number of columns equal to the number of variables passed in
    # as desiredfeatures and target. Whether it's a dataframe or pd.series depends on number of variables passed into
    # the arguments for desiredfeatures and target. If either passes in a list, it will return a dataframe.
    # If either passes in a single string, it will return a pd.series.
    # The dataframe/series (named X_df) contains only the columns listed in desiredfeatures from the input data frame.
    # The second dataframe/series (named y_df) contains only the columns listed in target from the input data frame.
    #
    # @examples
    # X_train, y_train = split_xy(train_df, ["feature1", "feature2", "feature3"], "G3")
    # X_train, y_train = split_xy(train_df, "G3", ["feature1", "feature2", "feature3"])
    
    X_df = None
    y_df = None
    
    if isinstance(desiredfeatures, str) and isinstance(target, str):
        if target == desiredfeatures:
            wa.warn("Desiredfeatures and target have features in common. Are you sure?", UserWarning)
    elif any(item in desiredfeatures for item in target) or any(item in target for item in desiredfeatures):
        list1 = set(desiredfeatures)
        both = list1.intersection(target)
        wa.warn("Desiredfeatures and target have features in common. Are you sure?", UserWarning)
    
    if isinstance(df, pd.DataFrame):
        if isinstance(desiredfeatures, str) or isinstance(desiredfeatures, list):
            X_df = df[desiredfeatures]
        else:
            raise TypeError("desiredfeatures is not a list or string")

        if isinstance(target, str) or isinstance(target, list):
            y_df = df[target]
        else:
            raise TypeError("target is not a list or string")
    else:
        raise TypeError("First argument is not a dataframe")
        
    return X_df, y_df


def plot_square_data(x_df, y_df, desiredFeatures, titles, txt):
    # Create plots to display in a square manner ( tiles of plots in 2x2, 3x3 or (n)by(n-1) configuration
    #
    # Takes in the required x and y dataframes that will be used to display the desired features in x_df 
    # alongside the data in y_df and the respective titles 
    #
    # @param x_df dataframe containing dependent variables
    # @param y_df dataframe containing independent variables
    # @param desiredFeatures Target feature(s) in x_df you desire for your analysis in list form
    # @param titles The respective titles(s) desired for your plot(s) in list form
    # @param txt the text to display as a string over the plot
    #
    # @return axy for testing purposes on the features of the plot
    # @return fig which is a copy of the plot able to be used in other functions
    #
    # @examples
    # plot_square_data(X_train, y_train, ["feature1", "feature2", "feature3"], ["title1", "title2", "title3], "This is Plot 1")
    # plot_square_data(dependent, independednts, ["income"], ["retirement_age"], "Income and Retirement Age Relation")
    

    if not (isinstance(x_df, pd.DataFrame) and isinstance(y_df, pd.Series) and x_df.shape[0] == y_df.shape[0]):
        raise TypeError("The first two arguments are not dataframes of equal length")
    if not (isinstance(desiredFeatures, list) and len(desiredFeatures) > 0 and isinstance(desiredFeatures[0], str)):
        raise TypeError("desiredFeatures is not a list of strings length at least 1")
    if not (isinstance(titles, list) and len(titles) > 0 and isinstance(titles[0], str) and len(titles) == len(desiredFeatures)):
        raise TypeError("titles is not a list of strings of length equal to desiredFeatures")
    if not isinstance(txt, str):
        raise TypeError("The last argument is not a string")


    # This will form a minimum sized box for the plots to go in, preferring horizontal boxes
    # will aways preffer to create a box rather than make vertical spanning blocks if there are many
    side_length_x = int(len(titles)**(1/2))
    side_length_y = int(len(titles)**(1/2))
    if side_length_x * side_length_y < len(titles):
        side_length_x += 1
        if side_length_x * side_length_y < len(titles):
            side_length_y += 1


    fig, axs = plt.subplots(side_length_y, side_length_x, figsize=(10,10))

    x = 0
    y = 0
    try:
        for i, feature in enumerate(desiredFeatures):
            #print(desiredFeatures[i])
            axs[y, x].scatter(x_df[desiredFeatures[i]], y_df)
            axs[y, x].set_title(titles[i])
            x += 1
            if x >= side_length_x:
                x = 0
                y += 1
    except:
        raise TypeError("desiredFeature is not in dependent dataframe")


    # plt.figtext(0.5, 0.05, txt, wrap=True, horizontalalignment='center', fontsize=12)
    fig1 = plt.gcf()
    # plt.show()

    return axs,fig1

def list_abs(pre, transformers, steps, features):
    # This is the abstract function for list, used in Results part of the notebook
    # @param pre is the preprocessor we're working w ith
    # @param transformers is the name of the transformers for pre
    # @param steps is the steps name for pre
    # @param features is the category of features we're focusing on
    #
    # @return a list containing all the features listed under the category (passed in as input "features")
    #
    # @examples
    # list_abs(preprocessor, "pipeline-2", "onehotencoder", categorical_features)
    
    #See if transformers and steps are Strings
    if (not isinstance(transformers, str)) or (not isinstance(steps, str)):
        raise TypeError("Transformers and Steps need to be strings")
        
    #See if features is a list of Strings
    if (not isinstance(features, list)):
        raise TypeError("features need to be a list")
        
    #If both tests are passed: we generate the outcome and return
    else:
        ret = list(
        pre.named_transformers_[transformers]
        .named_steps[steps]
        .get_feature_names_out(features)
        )
    
    return ret