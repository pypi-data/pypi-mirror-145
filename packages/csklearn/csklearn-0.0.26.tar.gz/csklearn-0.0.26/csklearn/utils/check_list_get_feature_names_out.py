def check_list_get_feature_names_out(ls_obj:list):
    """Check whether a list of objects have attribute 
        "get_feature_names_out"

    Args:
        ls_obj (list): list of sklearn transformers
    """
    ls_neg = [obj for obj in ls_obj if 
                                hasattr(obj, 'get_feature_names_out') is False]
    if len(ls_neg) > 0:
        raise Exception('The following objects has not method "get_feature_names_out": \n{}'.\
                format(ls_neg))
        