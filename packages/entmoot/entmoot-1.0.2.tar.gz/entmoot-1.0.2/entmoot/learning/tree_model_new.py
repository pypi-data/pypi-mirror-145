class TreeEnsemble:

    def __init__(self,
                 space,
                 training_params=None,
                 tune_params=False,
                 random_state=100):
        self._space = space
        self._training_params = training_params
        self._tune_params = tune_params
        self._random_state = random_state

    def fit(self, X, y):
        import lightgbm as lgb

        # train with fixed hyperparameters
        if not self._tune_params:
            DEFAULT_PARAMS = {
                'objective': 'regression',
                'metric': 'rmse',
                'boosting': 'gbdt',
                'num_boost_round': 5,
                'max_depth': 3,
                'min_data_in_leaf': 2,
                'min_data_per_group': 2,
                'random_state': self._random_state,
                'verbose': -1
            }
            # if there are categorical vars
            train_data = lgb.Dataset(X, label=y,
                                     categorical_feature=self._space.cat_idx,
                                     free_raw_data=False,
                                     params={'verbose': -1})

            self._tree_model = lgb.train(DEFAULT_PARAMS,
                                         train_data,
                                         categorical_feature=self._space.cat_idx,
                                         verbose_eval=False)
        else:
            raise NotImplementedError

    def add_trees_to_gurobi_model(self, model):
        pass