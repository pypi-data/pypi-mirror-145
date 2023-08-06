class UncertaintyMetric:

    def __init__(self,
                 space,
                 unc_metric: str = 'exploration',
                 unc_scaling: str = 'standard',
                 dist_metric: str = 'squared_euclidean',
                 cat_dist_metric: str = 'goodall4'):
        self._space = space

        self._unc_metric = unc_metric
        self._unc_scaling = unc_scaling

        # init non-categorical distance metric
        if dist_metric == 'squared_euclidean':
            self._dist_metric = SquaredEuclidean()
        elif dist_metric == 'euclidean':
            self._dist_metric = Euclidean()
        elif dist_metric == 'manhattan':
            self._dist_metric = Manhattan()
        else:
            raise ValueError(f"distance metric '{dist_metric}' doesn't exist")

        # init categorical distance metric
        if self._space.cat_idx:
            if cat_dist_metric == 'overlap':
                self._cat_dist_metric = Overlap()
            elif cat_dist_metric == 'goodall4':
                self._cat_dist_metric = Goodall4()
            else:
                raise ValueError(f"categorical distance metric '{cat_dist_metric}' "
                                 f"doesn't exist")
        else:
            self._cat_dist_metric = None

    def add_to_gurobi_model(self, model):
        """adds uncertainty model to gurobi optimization model"""





    def predict(self, X):
        pass

    def update(self, X_ref):
        # record current reference points, i.e., points to which distance is quantified
        # split reference points into continuous, integer and categorical vars
        self._X_cat_ref = X_ref[:, self._space.cat_idx] if self._space.cat_idx else None
        self._X_real_ref = X_ref[:, self._space.real_idx] if self._space.real_idx else None


        # compute the scaling attributes


class DistanceMetric:

    def get_closest_distance(self, X_ref, X):
        pass

    def add_to_gurobi_model(self, cat_rhs=None):
        pass


class CatDistanceMetric:

    def get_closest_distance(self, X_ref, X):
        pass

    def get_gurobi_model_diff(self):
        pass


class SquaredEuclidean(DistanceMetric):
    pass

class Euclidean(DistanceMetric):
    pass

class Manhattan(DistanceMetric):
    pass

class Overlap(CatDistanceMetric):
    pass

class Goodall4(CatDistanceMetric):
    pass

