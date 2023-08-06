import pandas as pd
import numpy as np
from sklearn.metrics import classification_report


def get_accuracy_matrix(y_test, y_pred):
    # precision
    df_preds = pd.DataFrame({'y':y_test.tolist()})
    df_preds['y_pred'] = y_pred.tolist()
    df_preds['ok'] = (df_preds['y'] == df_preds['y_pred'])*1
    df_preds['accuracy'] = (df_preds['y'] == df_preds['y_pred'])*1
    df_preds['nok'] = (df_preds['y'] != df_preds['y_pred'])*1  
    df_acc = df_preds.groupby('y_pred').agg({'accuracy':lambda x: np.sum(x)/len(x),\
        'ok':lambda x: np.sum(x), 'nok':lambda x: np.sum(x)}).\
        sort_values('ok', ascending=False)
    df_acc['precision'] = df_acc.ok / (df_acc.ok + df_acc.nok)
    df_acc.reset_index(inplace=True)

    # sensitivity
    df_sen = df_preds.groupby('y').agg({'ok':lambda x: np.sum(x), 
                                        'nok':lambda x: np.sum(x),
             'y_pred': lambda x: '||||'.join([str(a)+' ('+str(b)+')' 
                         for a,b in zip(np.unique(x, return_counts=True)[0], 
                         np.unique(x, return_counts=True)[1])]),}).\
        sort_values('ok', ascending=False)
    df_sen['sensitivity'] = df_sen.ok / (df_sen.ok + df_sen.nok)
    df_sen.reset_index(inplace=True)

    # merge sensitivity and precision
    df_merge = df_acc.merge(df_sen, how='left', left_on='y_pred', right_on='y')
    df_merge.sort_values('sensitivity', ascending=False, inplace=True)

    return df_merge


def get_preds_matrix(y_test, y_pred):
    df_preds = pd.DataFrame({'y':y_test})
    df_preds['y_pred'] = y_pred
    df_preds['ok'] = (df_preds['y'] == df_preds['y_pred'])*1
    df_preds['county'] = df_preds['y']
    df_miss = df_preds.groupby('y_pred', as_index=False).\
            agg({'county':'count',
                    'y': lambda x: '||||'.join([str(a)+' ('+str(b)+')' 
                        for a,b in zip(np.unique(x, return_counts=True)[0], 
                        np.unique(x, return_counts=True)[1])]),
                    'ok':'sum'}).\
            rename(columns={'county':'preds_count', 'ok':'correct_class'})

    df_miss['y'] = df_miss['y'].apply(lambda x: x.split('||||'))
    df_preds.drop('county', axis=1, inplace=True)
                            

    df_miss['accuracy'] = round(df_miss['correct_class']/
                                df_miss['preds_count'], 3)
    df_miss = df_miss.sort_values('accuracy', ascending=False)

    return df_miss


def get_classification_report(y_test, y_pred):
    df_report = pd.DataFrame(classification_report(y_test, y_pred, 
                                                    output_dict=True)).\
                            transpose()
    # df_report = df_report.drop(columns=['f1-score', 'support'])
    df_report.sort_values('precision', ascending=False, inplace=True)

    df_acc = get_accuracy_matrix(y_test, y_pred)
    df_acc = df_acc.drop(columns=['accuracy','precision','sensitivity'])
    df_acc = df_acc.set_index('y')

    df_merge = df_report.merge(df_acc, left_index=True, right_on='y')
    df_merge = df_merge.drop(columns=['y_pred_x','ok_y'])
    df_merge.rename({'ok_x':'TP','nok_x':'FP','nok_y':'FN',
                    'y_pred_y':'predictions'}, axis=1, inplace=True)

    df_merge.reset_index(inplace = True)

    return df_merge
