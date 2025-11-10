from scipy.stats import randint, uniform

LIGHTGBM_PARAMS = {
    'n_estimators' : randint(100, 300),
    'learning_rate' : uniform(0.03, 0.15),
    'num_leaves' : randint(20, 60),
    'max_depth' : randint(5, 20),
    'boosting_type' : ['gbdt']
}


RANDOM_SEARCH_PARAMS = {
    'n_iter' : 2,
    'cv' : 2,
    'verbose' : 1,
    'n_jobs' : -1,
    'random_state' : 42,
    'scoring' : 'accuracy'
}