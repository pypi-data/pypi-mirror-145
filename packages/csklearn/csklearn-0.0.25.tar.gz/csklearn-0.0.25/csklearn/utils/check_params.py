from sklearn.pipeline import Pipeline

def check_params(pipe:Pipeline, d_search_space:dict):
    """Function to check if all hyperparameters are well defined

    Args:
        pipe (Pipeline): sklearn Pipeline object
        d_search_space (dict): dictionary with params format

    Raises:
        Exception: if hyperparameters are not well defined
    """
    aux = [x for x in d_search_space.keys() if x not in pipe.get_params()]
    if len(aux) > 0:
        raise Exception("The following params don't exists: {}".format(aux))