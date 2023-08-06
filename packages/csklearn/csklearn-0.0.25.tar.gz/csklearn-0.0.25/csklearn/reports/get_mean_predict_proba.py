import pandas as pd
import numpy as np


def get_mean_predict_proba(pipe, X_test):

    # Predict
    y_pred = pipe.predict(X_test)

    # Get proba
    y_prob = pipe.predict_proba(X_test)
    y_prob = pd.Series(y_prob.tolist())
    df_1 = pd.DataFrame(y_pred, columns = ["y_pred"])
    df_1["y_prob"] = y_prob

    # sort
    lst_L2 = sorted(np.unique(y_pred))
    lst_prob = []
    for i in range(len(lst_L2)):
        value = lst_L2[i]
        df_aux = df_1.loc[df_1["y_pred"] == value]
        probabilities = []
        for j in range(len(df_aux)):
            arr = df_aux["y_prob"].iloc[j]
            probabilities.append(arr[i])
        lst_prob.append(np.mean(probabilities))

    df_2 = pd.DataFrame(lst_L2, columns = ["modo de fallo"])
    df_2["predict_proba"] = lst_prob
    return df_2