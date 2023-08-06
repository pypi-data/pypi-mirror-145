import numbers

def check_dimension(dimension):
    """returns variable type object, input can be:
        - '(lb,ub) for 'Real' and 'Integer'
        - a list of str for 'Categorical'"""

    if len(dimension) == 2:
        # dim is categorical if any value is str
        if any([isinstance(dim, str) for dim in dimension]):
            return Categorical(dimension)

        # dim is integer if any value is int
        elif all([isinstance(dim, numbers.Integral) for dim in dimension]):

            # if bounds are 0 and 1 we define dim as bin, i.e. binary
            if dimension[0] == 0 and dimension[1] == 1:
                return Integer(*dimension, is_binary=True)
            else:
                return Integer(*dimension)

        # dim is real if all previous checks failed
        elif any([isinstance(dim, numbers.Real) for dim in dimension]):
            return Real(*dimension)
    else:
        if any([isinstance(dim, str) for dim in dimension]):
            return Categorical(dimension)

    raise ValueError(f"invalid dimension {dimension}, please read documentation"
                     f" for supported types")


class Dimension:

    def __repr__(self):
        return f"{self.__class__.__name__}: " \
               f"({','.join([str(bnd) for bnd in self.bounds])})"

    @property
    def bounds(self):
        raise NotImplementedError

    @property
    def var_type(self):
        raise NotImplementedError

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) or value is None:
            self._name = value
        else:
            raise ValueError("dimension's name must be either str or None.")

class Categorical(Dimension):
    def __init__(self, cats):
        self.cat_enc = {self.var_type(cat): idx for idx, cat in enumerate(cats)}
        self.inv_cat_enc = {self.cat_enc[cat]: cat for cat in self.cat_enc}

    @property
    def bounds(self):
        return list(self.cat_enc.keys())

    @property
    def var_type(self):
        return str

    @property
    def type_name(self):
        return "CAT"

class Integer(Dimension):
    def __init__(self, lb, ub, is_binary=False):
        self.is_binary = is_binary
        self._lb = self.var_type(lb)
        self._ub = self.var_type(ub)

    @property
    def bounds(self):
        return (self._lb, self._ub)

    @property
    def var_type(self):
        return int

    @property
    def type_name(self):
        if self.is_binary:
            return "BIN"
        else:
            return "INT"


class Real(Dimension):
    def __init__(self, lb, ub):
        self._lb = self.var_type(lb)
        self._ub = self.var_type(ub)

    @property
    def bounds(self):
        return (self._lb, self._ub)

    @property
    def var_type(self):
        return float

    @property
    def type_name(self):
        return "REAL"

class Space:

    def __init__(self, dimensions):
        # store names if dimensions is dict
        if isinstance(dimensions, dict):
            var_names = [name for name in dimensions]
            self.dimensions = [check_dimension(dimensions[name])
                               for name in var_names]
            for dim, name in zip(self.dimensions, var_names):
                dim.name = name

        # give default names if it's a list
        else:
            self.dimensions = [check_dimension(dim) for dim in dimensions]
            for idx, dim in enumerate(self.dimensions):
                dim.name = f"{'_'.join([dim.type_name, str(idx)])}"


        self.cat_idx = {idx for idx, dim in enumerate(self.dimensions)
                        if isinstance(dim, Categorical)}
        self.real_idx = {idx for idx, dim in enumerate(self.dimensions)
                         if isinstance(dim, Real)}
        self.int_idx = {idx for idx, dim in enumerate(self.dimensions)
                        if isinstance(dim, Integer)}
        self.bin_idx = {idx for idx, dim in enumerate(self.dimensions)
                        if isinstance(dim, Integer) and dim.is_binary}

    def __iter__(self):
        return iter(self.dimensions)

    def __repr__(self):
        return "\nList of dimensions: \n" + \
               "\n".join(["-> " + str(dim) for dim in self.dimensions])

    def get_gurobi_core(self):
        """returns fresh gurobi model with the input variables pre-defined"""
        import gurobipy as grb
        model_core = grb.Model()

        model_core._var_enc = []

        # add variables to gurobi model
        for idx, dim in enumerate(self.dimensions):
            if idx in self.real_idx:
                new_var = model_core.addVar(lb=dim.bounds[0],
                                            ub=dim.bounds[1],
                                            name= dim.name,
                                            vtype='C')
            elif idx in self.int_idx:
                if dim.is_binary:
                    new_var = model_core.addVar(name=dim.name,
                                                vtype='B')
                else:
                    new_var = model_core.addVar(lb=dim.bounds[0],
                                                ub=dim.bounds[1],
                                                name=dim.name,
                                                vtype='I')
            elif idx in self.cat_idx:
                new_var = []
                for cat in dim.bounds:
                    new_var.append(
                        model_core.addVar(name=f"{dim.name}_is_{cat}",
                                          vtype='B')
                    )
                model_core.addConstr(grb.quicksum(new_var) == 1,
                                     name=f"{dim.name}_CAT_SUM")
            else:
                raise ValueError(f"variable for dimension {dim} couldn't be located!")

            model_core._var_enc.append(new_var)

        model_core.update()
        return model_core