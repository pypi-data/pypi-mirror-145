# --------------------------------------------------------------------------
# File: _subinterfaces.py
# ---------------------------------------------------------------------------
# Licensed Materials - Property of IBM
# 5725-A06 5725-A29 5724-Y48 5724-Y49 5724-Y54 5724-Y55 5655-Y21
# Copyright IBM Corporation 2008, 2022. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with
# IBM Corp.
# ------------------------------------------------------------------------
"""Sub-interfaces of the CPLEX API."""
from contextlib import closing, contextmanager
from io import StringIO
import numbers

from . import _constants
from . import _procedural as CPX_PROC
from ._baseinterface import BaseInterface
from ._multiobjsoln import MultiObjSolnInterface
from ._matrices import (SparsePair, SparseTriple, _HBMatrix,
                        unpack_pair, unpack_triple)
from ._aux_functions import (apply_freeform_one_arg,
                             apply_freeform_two_args,
                             max_arg_length,
                             validate_arg_lengths, apply_pairs,
                             delete_set_by_range,
                             make_group, _group,
                             init_list_args, listify,
                             unzip, convert_sequence)
from ..exceptions import CplexSolverError, WrongNumberOfArgumentsError
from ..constant_class import ConstantClass


class Histogram():
    """A class to retrieve histogram data of the columns or rows of the
    linear constraint matrix.

    See `VariablesInterface.get_histogram()` and
    `LinearConstraintInterface.get_histogram()`.
    """

    def __init__(self, c, key):
        self.__hist = CPX_PROC.gethist(c._env._e, c._lp, key[0])
        self.orientation = key

    def __getitem__(self, key):
        """Returns the number of columns/rows with a given nonzero count."""
        if isinstance(key, int):
            if key < 0:
                raise IndexError("histogram keys must be non-negative")
            return self.__hist[key]
        if isinstance(key, slice):
            start, stop, step = key.start, key.stop, key.step
            if start is None:
                start = 0
            if stop is None or stop > len(self.__hist):
                stop = len(self.__hist)
            if step is None:
                step = 1
            if start < 0:
                raise IndexError("histogram keys must be non-negative")
            if stop < 0:
                raise IndexError("histogram keys must be non-negative")
            return [self.__hist[i] for i in range(start, stop, step)]
        raise TypeError("key must be an integer or a slice")

    def __str__(self):
        """Returns a string containing a histogram in human readable form."""
        if self.orientation[0] == "c":
            hdr0 = "Column counts (excluding fixed variables):"
            hdr1 = "    Nonzero Count:"
            hdr2 = "Number of Columns:"
        else:
            hdr0 = "Row counts (excluding fixed variables):"
            hdr1 = " Nonzero Count:"
            hdr2 = "Number of Rows:"
        rng = len(self.__hist)
        maxhist = max(self.__hist)
        length = max(2,
                     len(str(rng)),
                     len(str(maxhist))) + 2
        perline = max((75 - len(hdr1)) / length, 1)
        ret = ""
        i = 0
        needs_hdr0 = True
        while True:
            if i >= rng:
                break
            for j in range(i, rng):
                if self.__hist[j] != 0:
                    break
            else:
                break
            if needs_hdr0:
                ret = ret + hdr0 + "\n\n"
                needs_hdr0 = False
            ret = ret + hdr1
            k = 0
            for j in range(i, rng):
                if k >= perline:
                    break
                if self.__hist[j] == 0:
                    continue
                ret = ret + str("%*d" % (length, j))
                k += 1

            ret = ret + "\n"
            ret = ret + hdr2
            k = 0
            jj = i
            for j in range(i, rng):
                if k >= perline:
                    break
                jj += 1
                if self.__hist[j] == 0:
                    continue
                ret = ret + str("%*d" % (length, self.__hist[j]))
                k += 1
            ret = ret + "\n\n"
            i = jj
        return ret


class AdvancedVariablesInterface(BaseInterface):
    """Methods for advanced operations on variables."""

    def __init__(self, parent):
        """Creates a new AdvancedVariablesInterface.

        The advanced variables interface is exposed by the top-level
        `Cplex` class as Cplex.variables.advanced.  This constructor is
        not meant to be used externally.
        """
        super().__init__(cplex=parent._cplex, advanced=True)

    def protect(self, *args):
        """Prevents variables from being aggregated during presolve.

        protect may be called with either a single variable identifier
        or a sequence of variable identifiers.  A variable identifier
        is either an index or a name of a variable.

        Note
          Subsequent calls to protect will replace previously protected
          variables with the new set of protected variables.

        Note
          If presolve can fix a variable to a value, it will be removed
          from the problem even if it has been protected.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ["a", "b", "c", "d"])
        >>> c.variables.advanced.protect("a")
        >>> c.variables.advanced.protect(["b", "d"])
        """
        a = listify(self._cplex.variables._conv(args[0]))
        CPX_PROC.copyprotected(self._env._e, self._cplex._lp, a)

    def get_protected(self):
        """Returns the currently protected variables.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ["a", "b", "c", "d"])
        >>> c.variables.advanced.protect("a")
        >>> c.variables.advanced.get_protected()
        [0]
        >>> c.variables.advanced.protect(["b", "d"])
        >>> c.variables.advanced.get_protected()
        [1, 3]
        """
        return CPX_PROC.getprotected(self._env._e, self._cplex._lp)

    def tighten_lower_bounds(self, *args):
        """Tightens the lower bounds on the specified variables.

        There are two forms by which
        variables.advanced.tighten_lower_bounds may be called.

        variables.advanced.tighten_lower_bounds(i, lb)
          i must be a variable name or index and lb must be a real
          number.  Sets the lower bound of the variable whose index
          or name is i to lb.

        variables.advanced.tighten_lower_bounds(seq_of_pairs)
          seq_of_pairs must be a list or tuple of (i, lb) pairs, each
          of which consists of a variable name or index and a real
          number.  Sets the lower bound of the specified variables to
          the corresponding values.  Equivalent to
          [variables.advanced.tighten_lower_bounds(pair[0], pair[1]) for pair in seq_of_pairs].

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ["x0", "x1", "x2"])
        >>> c.variables.advanced.tighten_lower_bounds(0, 1.0)
        >>> c.variables.get_lower_bounds()
        [1.0, 0.0, 0.0]
        >>> c.variables.advanced.tighten_lower_bounds([(2, 3.0), ("x1", -1.0)])
        >>> c.variables.get_lower_bounds()
        [1.0, -1.0, 3.0]
        """
        def tlb(a, b):
            CPX_PROC.tightenbds(self._env._e, self._cplex._lp, a,
                                'L' * len(a), b)
        apply_pairs(tlb, self._cplex.variables._conv, *args)

    def tighten_upper_bounds(self, *args):
        """Tightens the upper bounds on the specified variables.

        There are two forms by which
        variables.advanced.tighten_upper_bounds may be called.

        variables.advanced.tighten_upper_bounds(i, lb)
          i must be a variable name or index and lb must be a real
          number.  Sets the upper bound of the variable whose index
          or name is i to lb.

        variables.advanced.tighten_upper_bounds(seq_of_pairs)
          seq_of_pairs must be a list or tuple of (i, lb) pairs, each
          of which consists of a variable name or index and a real
          number.  Sets the upper bound of the specified variables to
          the corresponding values.  Equivalent to
          [variables.advanced.tighten_upper_bounds(pair[0], pair[1]) for pair in seq_of_pairs].

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ["x0", "x1", "x2"])
        >>> c.variables.advanced.tighten_upper_bounds(0, 1.0)
        >>> c.variables.advanced.tighten_upper_bounds([(2, 3.0), ("x1", 10.0)])
        >>> c.variables.get_upper_bounds()
        [1.0, 10.0, 3.0]
        """
        def tub(a, b):
            CPX_PROC.tightenbds(self._env._e, self._cplex._lp, a,
                                'U' * len(a), b)
        apply_pairs(tub, self._cplex.variables._conv, *args)


class VarTypes(ConstantClass):
    """Constants defining variable types

    For a definition of each type, see those topics in the CPLEX User's
    Manual.
    """
    continuous = _constants.CPX_CONTINUOUS
    binary = _constants.CPX_BINARY
    integer = _constants.CPX_INTEGER
    semi_integer = _constants.CPX_SEMIINT
    semi_continuous = _constants.CPX_SEMICONT


class VariablesInterface(BaseInterface):
    """Methods for adding, querying, and modifying variables.

    Example usage:

    >>> import cplex
    >>> c = cplex.Cplex()
    >>> indices = c.variables.add(names = ["x0", "x1", "x2"])
    >>> # default values for lower_bounds are 0.0
    >>> c.variables.get_lower_bounds()
    [0.0, 0.0, 0.0]
    >>> # values can be set either one at a time or many at a time
    >>> c.variables.set_lower_bounds(0, 1.0)
    >>> c.variables.set_lower_bounds([("x1", -1.0), (2, 3.0)])
    >>> # values can be queried as a range
    >>> c.variables.get_lower_bounds(0, "x1")
    [1.0, -1.0]
    >>> # values can be queried as a sequence in arbitrary order
    >>> c.variables.get_lower_bounds(["x1", "x2", 0])
    [-1.0, 3.0, 1.0]
    >>> # can query the number of variables
    >>> c.variables.get_num()
    3
    >>> c.variables.set_types(0, c.variables.type.binary)
    >>> c.variables.get_num_binary()
    1
    """

    type = VarTypes()
    """See `VarTypes()` """

    def __init__(self, cplex):
        """Creates a new VariablesInterface.

        The variables interface is exposed by the top-level `Cplex` class
        as `Cplex.variables`.  This constructor is not meant to be used
        externally.
        """
        super().__init__(cplex=cplex, getindexfunc=CPX_PROC.getcolindex)
        self.advanced = AdvancedVariablesInterface(self)
        """See `AdvancedVariablesInterface()` """

    def get_num(self):
        """Returns the number of variables in the problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> t = c.variables.type
        >>> indices = c.variables.add(types = [t.continuous, t.binary, t.integer])
        >>> c.variables.get_num()
        3
        """
        return CPX_PROC.getnumcols(self._env._e, self._cplex._lp)

    def get_num_integer(self):
        """Returns the number of integer variables in the problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> t = c.variables.type
        >>> indices = c.variables.add(types = [t.continuous, t.binary, t.integer])
        >>> c.variables.get_num_integer()
        1
        """
        return CPX_PROC.getnumint(self._env._e, self._cplex._lp)

    def get_num_binary(self):
        """Returns the number of binary variables in the problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> t = c.variables.type
        >>> indices = c.variables.add(types = [t.semi_continuous, t.binary, t.integer])
        >>> c.variables.get_num_binary()
        1
        """
        return CPX_PROC.getnumbin(self._env._e, self._cplex._lp)

    def get_num_semicontinuous(self):
        """Returns the number of semi-continuous variables in the problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> t = c.variables.type
        >>> indices = c.variables.add(types = [t.semi_continuous, t.semi_integer, t.semi_integer])
        >>> c.variables.get_num_semicontinuous()
        1
        """
        return CPX_PROC.getnumsemicont(self._env._e, self._cplex._lp)

    def get_num_semiinteger(self):
        """Returns the number of semi-integer variables in the problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> t = c.variables.type
        >>> indices = c.variables.add(types = [t.semi_continuous, t.semi_integer, t.semi_integer])
        >>> c.variables.get_num_semiinteger()
        2
        """
        return CPX_PROC.getnumsemiint(self._env._e, self._cplex._lp)

    def _add(self, obj, lb, ub, types, names, columns):
        """non-public"""
        if not isinstance(types, str):
            types = "".join(types)
        arg_list = [obj, lb, ub, types, names, columns]
        num_new_cols = max_arg_length(arg_list)
        validate_arg_lengths(
            arg_list,
            extra_msg=": obj, lb, ub, types, names, columns"
        )
        num_old_cols = self.get_num()
        if columns == []:
            CPX_PROC.newcols(self._env._e, self._cplex._lp, obj, lb, ub,
                             types, names)
        else:
            with CPX_PROC.chbmatrix(columns, self._cplex._env_lp_ptr,
                                    1) as (cmat, nnz):
                CPX_PROC.addcols(self._env._e, self._cplex._lp,
                                 num_new_cols, nnz, obj,
                                 cmat, lb, ub, names)
            if types != "":
                CPX_PROC.chgctype(
                    self._env._e, self._cplex._lp,
                    list(range(num_old_cols, num_old_cols + num_new_cols)),
                    types)

    def add(self, obj=None, lb=None, ub=None, types="", names=None,
            columns=None):
        """Adds variables and related data to the problem.

        variables.add accepts the keyword arguments obj, lb, ub,
        types, names, and columns.

        If more than one argument is specified, all arguments must
        have the same length.

        obj is a list of floats specifying the linear objective
        coefficients of the variables.

        lb is a list of floats specifying the lower bounds on the
        variables.

        ub is a list of floats specifying the upper bounds on the
        variables.

        types must be either a list of single-character strings or a
        string containing the types of the variables.

        Note
          If types is specified, the problem type will be a MIP, even if
          all variables are specified to be continuous.

        names is a list of strings.

        columns may be either a list of sparse vectors or a matrix in
        list-of-lists format.

        Note
          The entries of columns must not contain duplicate indices.
          If an entry of columns references a row more than once,
          either by index, name, or a combination of index and name,
          an exception will be raised.

        Returns an iterator containing the indices of the added
        variables.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(names=["c0", "c1", "c2"])
        >>> indices = c.variables.add(
        ...     obj=[1.0, 2.0, 3.0],
        ...     types=[c.variables.type.integer] * 3)
        >>> indices = c.variables.add(
        ...     obj=[1.0, 2.0, 3.0],
        ...     lb=[-1.0, 1.0, 0.0],
        ...     ub=[100.0, cplex.infinity, cplex.infinity],
        ...     types=[c.variables.type.integer] * 3,
        ...     names=["0", "1", "2"],
        ...     columns=[cplex.SparsePair(ind=['c0', 2],
        ...                               val=[1.0, -1.0]),
        ...              [['c2'],[2.0]],
        ...              cplex.SparsePair(ind=[0, 1],
        ...                               val=[3.0, 4.0])])
        >>> c.variables.get_lower_bounds()
        [0.0, 0.0, 0.0, -1.0, 1.0, 0.0]
        >>> c.variables.get_cols("1")
        SparsePair(ind = [2], val = [2.0])
        """
        obj, lb, ub, names, columns = init_list_args(obj, lb, ub, names,
                                                     columns)
        return self._add_iter(self.get_num, self._add,
                              obj, lb, ub, types, names, columns)

    def delete(self, *args):
        """Deletes variables from the problem.

        There are four forms by which variables.delete may be called.

        variables.delete()
          deletes all variables from the problem.

        variables.delete(i)
          i must be a variable name or index. Deletes the variable
          whose index or name is i.

        variables.delete(s)
          s must be a sequence of variable names or indices. Deletes
          the variables with names or indices contained within s.
          Equivalent to [variables.delete(i) for i in s].

        variables.delete(begin, end)
          begin and end must be variable indices or variable names.
          Deletes the variables with indices between begin and end,
          inclusive of end. Equivalent to
          variables.delete(range(begin, end + 1)). This will give the
          best performance when deleting batches of variables.

        See :cpxapi:`CPXdelcols` in the Callable Library Reference Manual
        for more detail.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=[str(i) for i in range(10)])
        >>> c.variables.get_num()
        10
        >>> c.variables.delete(8)
        >>> c.variables.get_names()
        ['0', '1', '2', '3', '4', '5', '6', '7', '9']
        >>> c.variables.delete("1", 3)
        >>> c.variables.get_names()
        ['0', '4', '5', '6', '7', '9']
        >>> c.variables.delete([2, "0", 5])
        >>> c.variables.get_names()
        ['4', '6', '7']
        >>> c.variables.delete()
        >>> c.variables.get_names()
        []
        """
        def _delete(begin, end=None):
            CPX_PROC.delcols(self._env._e, self._cplex._lp, begin, end)
        delete_set_by_range(_delete, self._conv, self.get_num(), *args)

    def set_lower_bounds(self, *args):
        """Sets the lower bound for a variable or set of variables.

        There are two forms by which variables.set_lower_bounds may be
        called.

        variables.set_lower_bounds(i, lb)
          i must be a variable name or index and lb must be a real
          number.  Sets the lower bound of the variable whose index
          or name is i to lb.

        variables.set_lower_bounds(seq_of_pairs)
          seq_of_pairs must be a list or tuple of (i, lb) pairs, each
          of which consists of a variable name or index and a real
          number.  Sets the lower bound of the specified variables to
          the corresponding values.  Equivalent to
          [variables.set_lower_bounds(pair[0], pair[1]) for pair in seq_of_pairs].

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ["x0", "x1", "x2"])
        >>> c.variables.set_lower_bounds(0, 1.0)
        >>> c.variables.get_lower_bounds()
        [1.0, 0.0, 0.0]
        >>> c.variables.set_lower_bounds([(2, 3.0), ("x1", -1.0)])
        >>> c.variables.get_lower_bounds()
        [1.0, -1.0, 3.0]
        """
        def setlb(a, b):
            CPX_PROC.chgbds(self._env._e, self._cplex._lp, a, "L" * len(a), b)
        apply_pairs(setlb, self._conv, *args)

    def set_upper_bounds(self, *args):
        """Sets the upper bound for a variable or set of variables.

        There are two forms by which variables.set_upper_bounds may be
        called.

        variables.set_upper_bounds(i, ub)
          i must be a variable name or index and ub must be a real
          number.  Sets the upper bound of the variable whose index
          or name is i to ub.

        variables.set_upper_bounds(seq_of_pairs)
          seq_of_pairs must be a list or tuple of (i, ub) pairs, each
          of which consists of a variable name or index and a real
          number.  Sets the upper bound of the specified variables to
          the corresponding values.  Equivalent to
          [variables.set_upper_bounds(pair[0], pair[1]) for pair in seq_of_pairs].

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ["x0", "x1", "x2"])
        >>> c.variables.set_upper_bounds(0, 1.0)
        >>> c.variables.set_upper_bounds([("x1", 10.0), (2, 3.0)])
        >>> c.variables.get_upper_bounds()
        [1.0, 10.0, 3.0]
        """
        def setub(a, b):
            CPX_PROC.chgbds(self._env._e, self._cplex._lp, a, "U" * len(a), b)
        apply_pairs(setub, self._conv, *args)

    def set_names(self, *args):
        """Sets the name of a variable or set of variables.

        There are two forms by which variables.set_names may be
        called.

        variables.set_names(i, name)
          i must be a variable name or index and name must be a
          string.

        variables.set_names(seq_of_pairs)
          seq_of_pairs must be a list or tuple of (i, name) pairs,
          each of which consists of a variable name or index and a
          string.  Sets the name of the specified variables to the
          corresponding strings.  Equivalent to
          [variables.set_names(pair[0], pair[1]) for pair in seq_of_pairs].

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> t = c.variables.type
        >>> indices = c.variables.add(types = [t.continuous, t.binary, t.integer])
        >>> c.variables.set_names(0, "first")
        >>> c.variables.set_names([(2, "third"), (1, "second")])
        >>> c.variables.get_names()
        ['first', 'second', 'third']
        """
        def setnames(a, b):
            CPX_PROC.chgcolname(self._env._e, self._cplex._lp, a, b)
        apply_pairs(setnames, self._conv, *args)

    def set_types(self, *args):
        """Sets the type of a variable or set of variables.

        There are two forms by which variables.set_types may be
        called.

        variables.set_types(i, type)
          i must be a variable name or index and name must be a
          single-character string.

        variables.set_types(seq_of_pairs)
          seq_of_pairs must be a list or tuple of (i, type) pairs,
          each of which consists of a variable name or index and a
          single-character string.  Sets the type of the specified
          variables to the corresponding strings.  Equivalent to
          [variables.set_types(pair[0], pair[1]) for pair in seq_of_pairs].

        Note
          If the types are set, the problem will be treated as a MIP,
          even if all variable types are continuous.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(5)])
        >>> c.variables.set_types(0, c.variables.type.continuous)
        >>> c.variables.set_types([("1", c.variables.type.integer),\
                                   ("2", c.variables.type.binary),\
                                   ("3", c.variables.type.semi_continuous),\
                                   ("4", c.variables.type.semi_integer)])
        >>> c.variables.get_types()
        ['C', 'I', 'B', 'S', 'N']
        >>> c.variables.type[c.variables.get_types(0)]
        'continuous'
        """
        if len(args) == 2:
            indices = [self._conv(args[0])]
            xctypes = args[1]
        elif len(args) == 1:
            indices, xctypes = unzip(args[0])
            indices = self._conv(indices)
            xctypes = "".join(xctypes)
        else:
            raise WrongNumberOfArgumentsError()
        CPX_PROC.chgctype(self._env._e, self._cplex._lp, indices, xctypes)

    def get_lower_bounds(self, *args):
        """Returns the lower bounds on variables from the problem.

        There are four forms by which variables.get_lower_bounds may be called.

        variables.get_lower_bounds()
          return the lower bounds on all variables from the problem.

        variables.get_lower_bounds(i)
          i must be a variable name or index.  Returns the lower
          bound on the variable whose index or name is i.

        variables.get_lower_bounds(s)
          s must be a sequence of variable names or indices.  Returns
          the lower bounds on the variables with indices the members
          of s.  Equivalent to
          [variables.get_lower_bounds(i) for i in s]

        variables.get_lower_bounds(begin, end)
          begin and end must be variable indices or variable names.
          Returns the lower bounds on the variables with indices between
          begin and end, inclusive of end. Equivalent to
          variables.get_lower_bounds(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(lb = [1.5 * i for i in range(10)],\
                                      names = [str(i) for i in range(10)])
        >>> c.variables.get_num()
        10
        >>> c.variables.get_lower_bounds(8)
        12.0
        >>> c.variables.get_lower_bounds("1",3)
        [1.5, 3.0, 4.5]
        >>> c.variables.get_lower_bounds([2,"0",5])
        [3.0, 0.0, 7.5]
        >>> c.variables.get_lower_bounds()
        [0.0, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5]
        """
        def getlb(a, b=self.get_num() - 1):
            return CPX_PROC.getlb(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(getlb, self._conv, args)

    def get_upper_bounds(self, *args):
        """Returns the upper bounds on variables from the problem.

        There are four forms by which variables.get_upper_bounds may be called.

        variables.get_upper_bounds()
          return the upper bounds on all variables from the problem.

        variables.get_upper_bounds(i)
          i must be a variable name or index.  Returns the upper
          bound on the variable whose index or name is i.

        variables.get_upper_bounds(s)
          s must be a sequence of variable names or indices.  Returns
          the upper bounds on the variables with indices the members
          of s.  Equivalent to
          [variables.get_upper_bounds(i) for i in s]

        variables.get_upper_bounds(begin, end)
          begin and end must be variable indices or variable names.
          Returns the upper bounds on the variables with indices between
          begin and end, inclusive of end. Equivalent to
          variables.get_upper_bounds(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(ub = [(1.5 * i) + 1.0 for i in range(10)],\
                                      names = [str(i) for i in range(10)])
        >>> c.variables.get_num()
        10
        >>> c.variables.get_upper_bounds(8)
        13.0
        >>> c.variables.get_upper_bounds("1",3)
        [2.5, 4.0, 5.5]
        >>> c.variables.get_upper_bounds([2,"0",5])
        [4.0, 1.0, 8.5]
        >>> c.variables.get_upper_bounds()
        [1.0, 2.5, 4.0, 5.5, 7.0, 8.5, 10.0, 11.5, 13.0, 14.5]
        """
        def getub(a, b=self.get_num() - 1):
            return CPX_PROC.getub(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(getub, self._conv, args)

    def get_names(self, *args):
        """Returns the names of variables from the problem.

        There are four forms by which variables.get_names may be called.

        variables.get_names()
          return the names of all variables from the problem.

        variables.get_names(i)
          i must be a variable index.  Returns the name of variable i.

        variables.get_names(s)
          s must be a sequence of variable indices.  Returns the
          names of the variables with indices the members of s.
          Equivalent to [variables.get_names(i) for i in s]

        variables.get_names(begin, end)
          begin and end must be variable indices. Returns the names of
          the variables with indices between begin and end, inclusive of
          end. Equivalent to variables.get_names(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ['x' + str(i) for i in range(10)])
        >>> c.variables.get_num()
        10
        >>> c.variables.get_names(8)
        'x8'
        >>> c.variables.get_names(1,3)
        ['x1', 'x2', 'x3']
        >>> c.variables.get_names([2,0,5])
        ['x2', 'x0', 'x5']
        >>> c.variables.get_names()
        ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9']
        """
        def getname(a, b=self.get_num() - 1):
            return CPX_PROC.getcolname(
                self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(getname, self._conv, args)

    def get_types(self, *args):
        """Returns the types of variables from the problem.

        There are four forms by which variables.types may be called.

        variables.types()
          return the types of all variables from the problem.

        variables.types(i)
          i must be a variable name or index.  Returns the type of
          the variable whose index or name is i.

        variables.types(s)
          s must be a sequence of variable names or indices.  Returns
          the types of the variables with indices the members of s.
          Equivalent to [variables.get_types(i) for i in s]

        variables.types(begin, end)
          begin and end must be variable indices or variable names.
          Returns the types of the variables with indices between begin
          and end, inclusive of end. Equivalent to
          variables.get_types(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> t = c.variables.type
        >>> indices = c.variables.add(names = [str(i) for i in range(5)],\
                                      types = [t.continuous, t.integer,\
                                      t.binary, t.semi_continuous, t.semi_integer])
        >>> c.variables.get_num()
        5
        >>> c.variables.get_types(3)
        'S'
        >>> c.variables.get_types(1,3)
        ['I', 'B', 'S']
        >>> c.variables.get_types([2,0,4])
        ['B', 'C', 'N']
        >>> c.variables.get_types()
        ['C', 'I', 'B', 'S', 'N']
        """
        def gettype(a, b=self.get_num() - 1):
            return CPX_PROC.getctype(self._env._e, self._cplex._lp, a, b)
        t = [i for i in "".join(apply_freeform_two_args(
            gettype, self._conv, args))]
        return t[0] if len(t) == 1 else t

    def get_cols(self, *args):
        """Returns a set of columns of the linear constraint matrix.

        Returns a list of SparsePair instances or a single SparsePair
        instance, depending on the form by which it was called.

        There are four forms by which variables.get_cols may be called.

        variables.get_cols()
          return the entire linear constraint matrix.

        variables.get_cols(i)
          i must be a variable name or index.  Returns the column of
          the linear constraint matrix associated with variable i.

        variables.get_cols(s)
          s must be a sequence of variable names or indices.  Returns
          the columns of the linear constraint matrix associated with
          the variables with indices the members of s.  Equivalent to
          [variables.get_cols(i) for i in s]

        variables.get_cols(begin, end)
          begin and end must be variable indices or variable names.
          Returns the columns of the linear constraint matrix associated
          with the variables with indices between begin and end,
          inclusive of end. Equivalent to
          variables.get_cols(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(names=['c1', 'c2'])
        >>> indices = c.variables.add(
        ...     names=[str(i) for i in range(3)],
        ...     columns=[cplex.SparsePair(ind=['c1'], val=[1.0]),
        ...     cplex.SparsePair(ind=['c2'], val=[2.0]),
        ...     cplex.SparsePair(ind=['c1','c2'], val=[3.0, 4.0])])
        >>> c.variables.get_num()
        3
        >>> c.variables.get_cols(2)
        SparsePair(ind = [0, 1], val = [3.0, 4.0])
        >>> for col in c.variables.get_cols(1, 2):
        ...     print(col)
        SparsePair(ind = [1], val = [2.0])
        SparsePair(ind = [0, 1], val = [3.0, 4.0])
        >>> for col in c.variables.get_cols([2, 0, 1]):
        ...     print(col)
        SparsePair(ind = [0, 1], val = [3.0, 4.0])
        SparsePair(ind = [0], val = [1.0])
        SparsePair(ind = [1], val = [2.0])
        >>> for col in c.variables.get_cols():
        ...     print(col)
        SparsePair(ind = [0], val = [1.0])
        SparsePair(ind = [1], val = [2.0])
        SparsePair(ind = [0, 1], val = [3.0, 4.0])
        """
        def getcols(a, b=self.get_num() - 1):
            mat = _HBMatrix()
            t = CPX_PROC.getcols(self._env._e, self._cplex._lp, a, b)
            mat.matbeg = t[0]
            mat.matind = t[1]
            mat.matval = t[2]
            return [m for m in mat]
        return apply_freeform_two_args(getcols, self._conv, args)

    def get_histogram(self):
        """Returns a histogram of the columns of the linear constraint matrix.

        To access the number of columns with given nonzero counts, use
        slice notation.  If a negative nonzero count is queried in
        this manner an IndexError will be raised.

        The __str__ method of the `Histogram` object returns a string
        displaying the number of columns with given nonzeros counts in
        human readable form.

        The data member "orientation" of the histogram object is
        "column", indicating that the histogram shows the nonzero
        counts for the columns of the linear constraint matrix.

        >>> import cplex
        >>> c = cplex.Cplex("ind.lp")
        >>> histogram = c.variables.get_histogram()
        >>> print(histogram)
        Column counts (excluding fixed variables):
        <BLANKLINE>
            Nonzero Count:   1   2   3
        Number of Columns:   1   6  36
        <BLANKLINE>
        <BLANKLINE>
        >>> histogram[2]
        6
        >>> histogram[0:4]
        [0, 1, 6, 36]
        """
        return Histogram(self._cplex, "column")


class AdvancedLinearConstraintInterface(BaseInterface):
    """Methods for handling lazy cuts and user cuts.

    Lazy cuts are constraints not specified in the constraint
    matrix of the MIP problem, but that must be not be violated
    in a solution. Using lazy cuts makes sense when there are a
    large number of constraints that must be satisfied at a solution,
    but are unlikely to be violated if they are left out. When
    you add lazy cuts to your model, set the CPLEX parameter
    c.parameters.preprocessing.reduce to 0 (zero) or 1 (one)
    in order to turn off dual reductions.

    User cuts are constraints that are implied by the constraint
    matrix and integrality requirements. Adding user cuts is helpful
    to tighten the MIP formulation. When you add user cuts, set
    the CPLEX parameter cplex.parameters.preprocessing.reformulations to
    cplex.parameters.preprocessing.reformulations.values.interfere_uncrush or
    cplex.parameters.preprocessing.reformulations.values.none to make sure
    that CPLEX makes only reductions that do not interfere with crushing
    linear forms (cuts in this case).
    """

    def __init__(self, parent):
        """Creates a new AdvancedLinearConstraintInterface.

        The advanced linear constraints interface is exposed by the
        top-level `Cplex` class as Cplex.linear_constraints.advanced.
        This constructor is not meant to be used externally.
        """
        super().__init__(cplex=parent._cplex, advanced=True)

    def get_num_lazy_constraints(self):
        """Returns the number of lazy cuts in the problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=[str(i) for i in range(10)])
        >>> cut = cplex.SparsePair(ind=[0, 1, 4], val=[1.0, 1.0, 1.0])
        >>> indices = c.linear_constraints.advanced.add_lazy_constraints(
        ...     lin_expr=[cut],
        ...     senses="E",
        ...     rhs=[0.0],
        ...     names=["lz1"])
        >>> c.linear_constraints.advanced.get_num_lazy_constraints()
        1
        """
        return CPX_PROC._getnumlazyconstraints(self._env._e, self._cplex._lp)

    def get_num_user_cuts(self):
        """Returns the number of user cuts in the problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=[str(i) for i in range(10)])
        >>> cut = cplex.SparsePair(ind=[0, 1, 4], val=[1.0, 1.0, 1.0])
        >>> indices = c.linear_constraints.advanced.add_user_cuts(
        ...     lin_expr=[cut],
        ...     senses="E",
        ...     rhs=[0.0],
        ...     names=["usr1"])
        >>> c.linear_constraints.advanced.get_num_user_cuts()
        1
        """
        return CPX_PROC._getnumusercuts(self._env._e, self._cplex._lp)

    def _add_lazy_constraints(self, lin_expr, senses, rhs, names):
        """non-public"""
        if not isinstance(senses, str):
            senses = "".join(senses)
        validate_arg_lengths(
            [rhs, senses, names, lin_expr],
            extra_msg=": lin_expr, senses, rhs, names"
        )
        CPX_PROC.addlazyconstraints(
            self._env._e, self._cplex._lp, rhs, senses,
            lin_expr, names)

    def add_lazy_constraints(self, lin_expr=None, senses="", rhs=None,
                             names=None):
        """Adds lazy constraints to the problem.

        linear_constraints.advanced.add_lazy_constraints accepts the
        keyword arguments lin_expr, senses, rhs, and names.

        If more than one argument is specified, all arguments must
        have the same length.

        lin_expr may be either a list of SparsePair instances or a
        matrix in list-of-lists format.

        Note
          The entries of lin_expr must not contain duplicate indices.
          If an entry of lin_expr references a variable more than
          once, either by index, name, or a combination of index and
          name, an exception will be raised.

        senses must be either a list of single-character strings or a
        string containing the senses of the linear constraints.

        rhs is a list of floats, specifying the righthand side of
        each linear constraint.

        names is a list of strings.

        Returns an iterator containing the indices of the added lazy
        constraints.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=[str(i) for i in range(10)])
        >>> cut = cplex.SparsePair(ind=[0, 1, 4], val=[1.0, 1.0, 1.0])
        >>> indices = c.linear_constraints.advanced.add_lazy_constraints(
        ...     lin_expr=[cut],
        ...     senses="E",
        ...     rhs=[0.0],
        ...     names=["lz1"])
        >>> cut2 = cplex.SparsePair(ind=[0, 2, 4], val=[1.0, 1.0, 1.0])
        >>> cut3 = cplex.SparsePair(ind=[0, 2, 5], val=[1.0, 1.0, 1.0])
        >>> indices = c.linear_constraints.advanced.add_lazy_constraints(
        ...     lin_expr=[cut2, cut3],
        ...     senses="EE",
        ...     rhs=[0.0, 0.0],
        ...     names=["lz2", "lz3"])
        >>> c.linear_constraints.advanced.get_num_lazy_constraints()
        3
        """
        lin_expr, rhs, names = init_list_args(lin_expr, rhs, names)
        return self._add_iter(self.get_num_lazy_constraints,
                              self._add_lazy_constraints,
                              lin_expr, senses, rhs, names)

    def _add_user_cuts(self, lin_expr, senses, rhs, names):
        """non-public"""
        if not isinstance(senses, str):
            senses = "".join(senses)
        validate_arg_lengths(
            [rhs, senses, names, lin_expr],
            extra_msg=": lin_expr, senses, rhs, names"
        )
        CPX_PROC.addusercuts(
            self._env._e, self._cplex._lp, rhs, senses,
            lin_expr, names)

    def add_user_cuts(self, lin_expr=None, senses="", rhs=None, names=None):
        """Adds user cuts to the problem.

        linear_constraints.advanced.add_user_cuts accepts the keyword
        arguments lin_expr, senses, rhs, and names.

        If more than one argument is specified, all arguments must
        have the same length.

        lin_expr may be either a list of SparsePair instances or a
        matrix in list-of-lists format.

        Note
          The entries of lin_expr must not contain duplicate indices.
          If an entry of lin_expr references a variable more than
          once, either by index, name, or a combination of index and
          name, an exception will be raised.

        senses must be either a list of single-character strings or a
        string containing the senses of the linear constraints.

        rhs is a list of floats, specifying the righthand side of
        each linear constraint.

        names is a list of strings.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=[str(i) for i in range(10)])
        >>> cut = cplex.SparsePair(ind=[0, 1, 4], val=[1.0, 1.0, 1.0])
        >>> indices = c.linear_constraints.advanced.add_user_cuts(
        ...     names=["usr1"],
        ...     lin_expr=[cut],
        ...     senses="E",
        ...     rhs=[0.0])
        >>> cut2 = cplex.SparsePair(ind=[0, 2, 4], val=[1.0, 1.0, 1.0])
        >>> cut3 = cplex.SparsePair(ind=[0, 2, 5], val=[1.0, 1.0, 1.0])
        >>> indices = c.linear_constraints.advanced.add_user_cuts(
        ...     lin_expr=[cut2, cut3],
        ...     senses = "EE",
        ...     rhs=[0.0, 0.0],
        ...     names=["usr2", "usr3"])
        >>> c.linear_constraints.advanced.get_num_user_cuts()
        3
        """
        lin_expr, senses, rhs, names = init_list_args(
            lin_expr, senses, rhs, names)
        return self._add_iter(self.get_num_user_cuts, self._add_user_cuts,
                              lin_expr, senses, rhs, names)

    def free_lazy_constraints(self):
        """Removes all lazy constraints from the problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=[str(i) for i in range(10)])
        >>> cut = cplex.SparsePair(ind=[0, 1, 4], val=[1.0, 1.0, 1.0])
        >>> indices = c.linear_constraints.advanced.add_lazy_constraints(
        ...     lin_expr = [cut],
        ...     senses = "E",
        ...     rhs = [0.0],
        ...     names = ["lz1"])
        >>> c.linear_constraints.advanced.get_num_lazy_constraints()
        1
        >>> c.linear_constraints.advanced.free_lazy_constraints()
        >>> c.linear_constraints.advanced.get_num_lazy_constraints()
        0
        """
        CPX_PROC.freelazyconstraints(self._env._e, self._cplex._lp)

    def free_user_cuts(self):
        """Removes all user cuts from the problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=[str(i) for i in range(10)])
        >>> cut = cplex.SparsePair(ind=[0, 1, 4], val=[1.0, 1.0, 1.0])
        >>> indices = c.linear_constraints.advanced.add_user_cuts(
        ...     lin_expr=[cut],
        ...     senses="E",
        ...     rhs=[0.0],
        ...     names=["usr1"])
        >>> c.linear_constraints.advanced.get_num_user_cuts()
        1
        >>> c.linear_constraints.advanced.free_user_cuts()
        >>> c.linear_constraints.advanced.get_num_user_cuts()
        0
        """
        CPX_PROC.freeusercuts(self._env._e, self._cplex._lp)


class LinearConstraintInterface(BaseInterface):
    """Methods for adding, modifying, and querying linear constraints."""

    def __init__(self, cplex):
        """Creates a new LinearConstraintInterface.

        The linear constraints interface is exposed by the top-level
        `Cplex` class as `Cplex.linear_constraints`.  This constructor is
        not meant to be used externally.
        """
        super().__init__(cplex=cplex, getindexfunc=CPX_PROC.getrowindex)
        self.advanced = AdvancedLinearConstraintInterface(self)
        """See `AdvancedLinearConstraintInterface()` """

    def get_num(self):
        """Returns the number of linear constraints.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(names = ["c1", "c2", "c3"])
        >>> c.linear_constraints.get_num()
        3
        """
        return CPX_PROC.getnumrows(self._env._e, self._cplex._lp)

    def _add(self, lin_expr, senses, rhs, range_values, names):
        """non-public"""
        if not isinstance(senses, str):
            senses = "".join(senses)
        arg_list = [rhs, senses, range_values, names, lin_expr]
        num_new_rows = max_arg_length(arg_list)
        validate_arg_lengths(
            arg_list,
            extra_msg=": lin_expr, senses, rhs, range_values, names"
        )
        num_old_rows = self.get_num()
        if lin_expr:
            with CPX_PROC.chbmatrix(lin_expr, self._cplex._env_lp_ptr,
                                    0) as (rmat, nnz):
                CPX_PROC.addrows(self._env._e, self._cplex._lp, 0,
                                 num_new_rows, nnz, rhs, senses,
                                 rmat, [], names)
            if range_values != []:
                CPX_PROC.chgrngval(
                    self._env._e, self._cplex._lp,
                    list(range(num_old_rows, num_old_rows + num_new_rows)),
                    range_values)
        else:
            if senses.find('R') != -1 and not range_values:
                range_values = [0.0] * len(senses)
            CPX_PROC.newrows(self._env._e, self._cplex._lp, rhs, senses,
                             range_values, names)

    def add(self, lin_expr=None, senses="", rhs=None, range_values=None,
            names=None):
        """Adds linear constraints to the problem.

        linear_constraints.add accepts the keyword arguments lin_expr,
        senses, rhs, range_values, and names.

        If more than one argument is specified, all arguments must
        have the same length.

        lin_expr may be either a list of SparsePair instances or a
        matrix in list-of-lists format.

        Note
          The entries of lin_expr must not contain duplicate indices.
          If an entry of lin_expr references a variable more than
          once, either by index, name, or a combination of index and
          name, an exception will be raised.

        senses must be either a list of single-character strings or a
        string containing the senses of the linear constraints.
        Each entry must
        be one of 'G', 'L', 'E', and 'R', indicating
        greater-than-or-equal-to (>=), less-than-or-equal-to (<=),
        equality (=), and ranged constraints, respectively.

        rhs is a list of floats, specifying the righthand side of
        each linear constraint.

        range_values is a list of floats, specifying the difference
        between lefthand side and righthand side of each linear constraint.
        If range_values[i] > 0 (zero) then the constraint i is defined as
        rhs[i] <= rhs[i] + range_values[i]. If range_values[i] < 0 (zero)
        then constraint i is defined as
        rhs[i] + range_value[i] <= a*x <= rhs[i].

        names is a list of strings.

        Returns an iterator containing the indices of the added linear
        constraints.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ["x1", "x2", "x3"])
        >>> indices = c.linear_constraints.add(\
                lin_expr = [cplex.SparsePair(ind = ["x1", "x3"], val = [1.0, -1.0]),\
                            cplex.SparsePair(ind = ["x1", "x2"], val = [1.0, 1.0]),\
                            cplex.SparsePair(ind = ["x1", "x2", "x3"], val = [-1.0] * 3),\
                            cplex.SparsePair(ind = ["x2", "x3"], val = [10.0, -2.0])],\
                senses = ["E", "L", "G", "R"],\
                rhs = [0.0, 1.0, -1.0, 2.0],\
                range_values = [0.0, 0.0, 0.0, -10.0],\
                names = ["c0", "c1", "c2", "c3"])
        >>> c.linear_constraints.get_rhs()
        [0.0, 1.0, -1.0, 2.0]
        """
        lin_expr, senses, rhs, range_values, names = init_list_args(
            lin_expr, senses, rhs, range_values, names)
        return self._add_iter(self.get_num, self._add,
                              lin_expr, senses, rhs, range_values, names)

    def delete(self, *args):
        """Removes linear constraints from the problem.

        There are four forms by which linear_constraints.delete may be
        called.

        linear_constraints.delete()
          deletes all linear constraints from the problem.

        linear_constraints.delete(i)
          i must be a linear constraint name or index. Deletes the
          linear constraint whose index or name is i.

        linear_constraints.delete(s)
          s must be a sequence of linear constraint names or indices.
          Deletes the linear constraints with names or indices contained
          within s. Equivalent to [linear_constraints.delete(i) for i in s].

        linear_constraints.delete(begin, end)
          begin and end must be linear constraint indices or linear
          constraint names. Deletes the linear constraints with indices
          between begin and end, inclusive of end. Equivalent to
          linear_constraints.delete(range(begin, end + 1)). This will
          give the best performance when deleting batches of linear
          constraints.

        See :cpxapi:`CPXdelrows` in the Callable Library Reference Manual
        for more detail.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(names=[str(i) for i in range(10)])
        >>> c.linear_constraints.get_num()
        10
        >>> c.linear_constraints.delete(8)
        >>> c.linear_constraints.get_names()
        ['0', '1', '2', '3', '4', '5', '6', '7', '9']
        >>> c.linear_constraints.delete("1", 3)
        >>> c.linear_constraints.get_names()
        ['0', '4', '5', '6', '7', '9']
        >>> c.linear_constraints.delete([2, "0", 5])
        >>> c.linear_constraints.get_names()
        ['4', '6', '7']
        >>> c.linear_constraints.delete()
        >>> c.linear_constraints.get_names()
        []
        """
        def _delete(begin, end=None):
            CPX_PROC.delrows(self._env._e, self._cplex._lp, begin, end)
        delete_set_by_range(_delete, self._conv, self.get_num(), *args)

    def set_rhs(self, *args):
        """Sets the righthand side of a set of linear constraints.

        There are two forms by which linear_constraints.set_rhs may be
        called.

        linear_constraints.set_rhs(i, rhs)
          i must be a row name or index and rhs must be a real number.
          Sets the righthand side of the row whose index or name is
          i to rhs.

        linear_constraints.set_rhs(seq_of_pairs)
          seq_of_pairs must be a list or tuple of (i, rhs) pairs, each
          of which consists of a row name or index and a real
          number.  Sets the righthand side of the specified rows to
          the corresponding values.  Equivalent to
          [linear_constraints.set_rhs(pair[0], pair[1]) for pair in seq_of_pairs].

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(names = ["c0", "c1", "c2", "c3"])
        >>> c.linear_constraints.get_rhs()
        [0.0, 0.0, 0.0, 0.0]
        >>> c.linear_constraints.set_rhs("c1", 1.0)
        >>> c.linear_constraints.get_rhs()
        [0.0, 1.0, 0.0, 0.0]
        >>> c.linear_constraints.set_rhs([("c3", 2.0), (2, -1.0)])
        >>> c.linear_constraints.get_rhs()
        [0.0, 1.0, -1.0, 2.0]
        """
        def chgrhs(a, b):
            CPX_PROC.chgrhs(self._env._e, self._cplex._lp, a, b)
        apply_pairs(chgrhs, self._conv, *args)

    def set_names(self, *args):
        """Sets the name of a linear constraint or set of linear constraints.

        There are two forms by which linear_constraints.set_names may be
        called.

        linear_constraints.set_names(i, name)
          i must be a linear constraint name or index and name must be a
          string.

        linear_constraints.set_names(seq_of_pairs)
          seq_of_pairs must be a list or tuple of (i, name) pairs,
          each of which consists of a linear constraint name or index and a
          string.  Sets the name of the specified linear constraints to the
          corresponding strings.  Equivalent to
          [linear_constraints.set_names(pair[0], pair[1]) for pair in seq_of_pairs].

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(names = ["c0", "c1", "c2", "c3"])
        >>> c.linear_constraints.set_names("c1", "second")
        >>> c.linear_constraints.get_names(1)
        'second'
        >>> c.linear_constraints.set_names([("c3", "last"), (2, "middle")])
        >>> c.linear_constraints.get_names()
        ['c0', 'second', 'middle', 'last']
        """
        def setnames(a, b):
            CPX_PROC.chgrowname(self._env._e, self._cplex._lp, a, b)
        apply_pairs(setnames, self._conv, *args)

    def set_senses(self, *args):
        """Sets the sense of a linear constraint or set of linear constraints.

        There are two forms by which linear_constraints.set_senses may be
        called.

        linear_constraints.set_senses(i, type)
          i must be a row name or index and name must be a
          single-character string.

        linear_constraints.set_senses(seq_of_pairs)
          seq_of_pairs must be a list or tuple of (i, sense) pairs,
          each of which consists of a row name or index and a
          single-character string.  Sets the sense of the specified
          rows to the corresponding strings.  Equivalent to
          [linear_constraints.set_senses(pair[0], pair[1]) for pair in seq_of_pairs].

        The senses of the constraints must be one of 'G', 'L', 'E',
        and 'R', indicating greater-than-or-equal-to (>=),
        less-than-or-equal-to (<=), equality (=), and ranged constraints,
        respectively.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(names = ["c0", "c1", "c2", "c3"])
        >>> c.linear_constraints.get_senses()
        ['E', 'E', 'E', 'E']
        >>> c.linear_constraints.set_senses("c1", "G")
        >>> c.linear_constraints.get_senses(1)
        'G'
        >>> c.linear_constraints.set_senses([("c3", "L"), (2, "R")])
        >>> c.linear_constraints.get_senses()
        ['E', 'G', 'R', 'L']
        """
        if len(args) == 2:
            indices = [self._conv(args[0])]
            senses = args[1]
        elif len(args) == 1:
            indices, senses = unzip(args[0])
            indices = self._conv(indices)
            senses = "".join(senses)
        else:
            raise WrongNumberOfArgumentsError()
        CPX_PROC.chgsense(self._env._e, self._cplex._lp,
                          indices, senses)

    def set_linear_components(self, *args):
        """Sets a linear constraint or set of linear constraints.

        There are two forms by which this method may be called:

        linear_constraints.set_linear_components(i, lin)
          i must be a row name or index and lin must be either a
          SparsePair or a pair of sequences, the first of which
          consists of variable names or indices, the second of which
          consists of floats.

        linear_constraints.set_linear_components(seq_of_pairs)
          seq_of_pairs must be a list or tuple of (i, lin) pairs,
          each of which consists of a row name or index and a vector
          as described above.  Sets the specified rows
          to the corresponding vector.  Equivalent to
          [linear_constraints.set_linear_components(pair[0], pair[1])
          for pair in seq_of_pairs].

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(names=["c0", "c1", "c2", "c3"])
        >>> indices = c.variables.add(names=["x0", "x1"])
        >>> c.linear_constraints.set_linear_components("c0", [["x0"], [1.0]])
        >>> c.linear_constraints.get_rows("c0")
        SparsePair(ind = [0], val = [1.0])
        >>> c.linear_constraints.set_linear_components([
        ...     ("c3", cplex.SparsePair(ind=["x1"], val=[-1.0])),
        ...     (2, [[0, 1], [-2.0, 3.0]])])
        >>> c.linear_constraints.get_rows("c3")
        SparsePair(ind = [1], val = [-1.0])
        >>> c.linear_constraints.get_rows(2)
        SparsePair(ind = [0, 1], val = [-2.0, 3.0])
        """
        def setlin(cons, vars_):
            validate_arg_lengths([cons, vars_])
            cons = convert_sequence(cons, self._get_index)
            varcache = {}
            for c, v in zip(cons, vars_):
                ind, val = unpack_pair(v)
                CPX_PROC.chgcoeflist(
                    self._env._e,
                    self._cplex._lp,
                    [c] * len(ind),
                    convert_sequence(
                        ind,
                        self._cplex.variables._get_index,
                        varcache
                    ),
                    val
                )
        apply_pairs(setlin, self._conv, *args)

    def set_range_values(self, *args):
        """Sets the range values for a set of linear constraints.

        That is, this method sets the lefthand side (lhs) for each ranged
        constraint of the form lhs <= lin_expr <= rhs.

        The range values are a list of floats, specifying the difference
        between lefthand side and righthand side of each linear constraint.
        If range_values[i] > 0 (zero) then the constraint i is defined as
        rhs[i] <= rhs[i] + range_values[i]. If range_values[i] < 0 (zero)
        then constraint i is defined as
        rhs[i] + range_value[i] <= a*x <= rhs[i].

        Note that changing the range values will not change the sense of a
        constraint; you must call the method set_senses() of the class
        LinearConstraintInterface to change the sense of a ranged row if
        the previous range value was 0 (zero) and the constraint sense was not
        'R'. Similarly, changing the range coefficient from a nonzero value to
        0 (zero) will not change the constraint sense from 'R" to "E"; an
        additional call of setsenses() is required to accomplish that.

        There are two forms by which linear_constraints.set_range_values may be
        called.

        linear_constraints.set_range_values(i, range)
          i must be a row name or index and range must be a real
          number.  Sets the range value of the row whose index or
          name is i to range.

        linear_constraints.set_range_values(seq_of_pairs)
          seq_of_pairs must be a list or tuple of (i, range) pairs, each
          of which consists of a row name or index and a real
          number.  Sets the range values for the specified rows to
          the corresponding values.  Equivalent to
          [linear_constraints.set_range_values(pair[0], pair[1]) for pair in seq_of_pairs].

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(names = ["c0", "c1", "c2", "c3"])
        >>> c.linear_constraints.set_range_values("c1", 1.0)
        >>> c.linear_constraints.get_range_values()
        [0.0, 1.0, 0.0, 0.0]
        >>> c.linear_constraints.set_range_values([("c3", 2.0), (2, -1.0)])
        >>> c.linear_constraints.get_range_values()
        [0.0, 1.0, -1.0, 2.0]
        """
        def chgrngval(a, b):
            CPX_PROC.chgrngval(self._env._e, self._cplex._lp, a, b)
        apply_pairs(chgrngval, self._conv, *args)

    def set_coefficients(self, *args):
        """Sets individual coefficients of the linear constraint matrix.

        There are two forms by which
        linear_constraints.set_coefficients may be called.

        linear_constraints.set_coefficients(row, col, val)
          row and col must be indices or names of a linear constraint
          and variable, respectively.  The corresponding coefficient
          is set to val.

        linear_constraints.set_coefficients(coefficients)
          coefficients must be a list of (row, col, val) triples as
          described above.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(names = ["c0", "c1", "c2", "c3"])
        >>> indices = c.variables.add(names = ["x0", "x1"])
        >>> c.linear_constraints.set_coefficients("c0", "x1", 1.0)
        >>> c.linear_constraints.get_rows(0)
        SparsePair(ind = [1], val = [1.0])
        >>> c.linear_constraints.set_coefficients([("c2", "x0", 2.0),\
                                                   ("c2", "x1", -1.0)])
        >>> c.linear_constraints.get_rows("c2")
        SparsePair(ind = [0, 1], val = [2.0, -1.0])
        """
        if len(args) == 3:
            arg_list = [[arg] for arg in args]
        elif len(args) == 1:
            arg_list = unzip(args[0])
        else:
            raise WrongNumberOfArgumentsError()
        CPX_PROC.chgcoeflist(
            self._env._e, self._cplex._lp,
            self._conv(arg_list[0]),
            self._cplex.variables._conv(arg_list[1]),
            arg_list[2])

    def get_rhs(self, *args):
        """Returns the righthand side of constraints from the problem.

        Can be called by four forms.

        linear_constraints.get_rhs()
          return the righthand side of all linear constraints from
          the problem.

        linear_constraints.get_rhs(i)
          i must be a linear constraint name or index.  Returns the
          righthand side of the linear constraint whose index or
          name is i.

        linear_constraints.get_rhs(s)
          s must be a sequence of linear constraint names or indices.
          Returns the righthand side of the linear constraints with
          indices the members of s.  Equivalent to
          [linear_constraints.get_rhs(i) for i in s]

        linear_constraints.get_rhs(begin, end)
          begin and end must be linear constraint indices or linear
          constraint names. Returns the righthand side of the linear
          constraints with indices between begin and end, inclusive
          of end. Equivalent to
          linear_constraints.get_rhs(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(rhs = [1.5 * i for i in range(10)],\
                                     names = [str(i) for i in range(10)])
        >>> c.linear_constraints.get_num()
        10
        >>> c.linear_constraints.get_rhs(8)
        12.0
        >>> c.linear_constraints.get_rhs("1",3)
        [1.5, 3.0, 4.5]
        >>> c.linear_constraints.get_rhs([2,"0",5])
        [3.0, 0.0, 7.5]
        >>> c.linear_constraints.get_rhs()
        [0.0, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5]
        """
        def getrhs(a, b=self.get_num() - 1):
            return CPX_PROC.getrhs(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(getrhs, self._conv, args)

    def get_senses(self, *args):
        """Returns the senses of constraints from the problem.

        Can be called by four forms.

        linear_constraints.get_senses()
          return the senses of all linear constraints from the
          problem.

        linear_constraints.get_senses(i)
          i must be a linear constraint name or index.  Returns the
          sense of the linear constraint whose index or name is i.

        linear_constraints.get_senses(s)
          s must be a sequence of linear constraint names or indices.
          Returns the senses of the linear constraints with indices
          the members of s.  Equivalent to
          [linear_constraints.get_senses(i) for i in s]

        linear_constraints.get_senses(begin, end)
          begin and end must be linear constraint indices or linear
          constraint names. Returns the senses of the linear constraints
          with indices between begin and end, inclusive of end.
          Equivalent to
          linear_constraints.get_senses(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(
        ...     senses=["E", "G", "L", "R"],
        ...     names=[str(i) for i in range(4)])
        >>> c.linear_constraints.get_num()
        4
        >>> c.linear_constraints.get_senses(1)
        'G'
        >>> c.linear_constraints.get_senses("1",3)
        ['G', 'L', 'R']
        >>> c.linear_constraints.get_senses([2,"0",1])
        ['L', 'E', 'G']
        >>> c.linear_constraints.get_senses()
        ['E', 'G', 'L', 'R']
        """
        def getsense(a, b=self.get_num() - 1):
            return CPX_PROC.getsense(self._env._e, self._cplex._lp, a, b)
        s = [i for i in "".join(apply_freeform_two_args(
            getsense, self._conv, args))]
        return s[0] if len(s) == 1 else s

    def get_range_values(self, *args):
        """Returns the range values of linear constraints from the problem.

        That is, this method returns the lefthand side (lhs) for each
        ranged constraint of the form lhs <= lin_expr <= rhs. This method
        makes sense only for ranged constraints, that is, linear constraints
        of sense 'R'.

        The range values are a list of floats, specifying the difference
        between lefthand side and righthand side of each linear constraint.
        If range_values[i] > 0 (zero) then the constraint i is defined as
        rhs[i] <= rhs[i] + range_values[i]. If range_values[i] < 0 (zero)
        then constraint i is defined as
        rhs[i] + range_value[i] <= a*x <= rhs[i].

        Can be called by four forms.

        linear_constraints.get_range_values()
          return the range values of all linear constraints from the
          problem.

        linear_constraints.get_range_values(i)
          i must be a linear constraint name or index.  Returns the
          range value of the linear constraint whose index or name is i.

        linear_constraints.get_range_values(s)
          s must be a sequence of linear constraint names or indices.
          Returns the range values of the linear constraints with
          indices the members of s.  Equivalent to
          [linear_constraints.get_range_values(i) for i in s]

        linear_constraints.get_range_values(begin, end)
          begin and end must be linear constraint indices or linear
          constraint names. Returns the range values of the linear
          constraints with indices between begin and end, inclusive
          of end. Equivalent to
          linear_constraints.get_range_values(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(\
                range_values = [1.5 * i for i in range(10)],\
                senses = ["R"] * 10,\
                names = [str(i) for i in range(10)])
        >>> c.linear_constraints.get_num()
        10
        >>> c.linear_constraints.get_range_values(8)
        12.0
        >>> c.linear_constraints.get_range_values("1",3)
        [1.5, 3.0, 4.5]
        >>> c.linear_constraints.get_range_values([2,"0",5])
        [3.0, 0.0, 7.5]
        >>> c.linear_constraints.get_range_values()
        [0.0, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5]
        """
        def getrngval(a, b=self.get_num() - 1):
            return CPX_PROC.getrngval(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(getrngval, self._conv, args)

    def get_coefficients(self, *args):
        """Returns coefficients by row, column coordinates.

        There are two forms by which
        linear_constraints.get_coefficients may be called.

        linear_constraints.get_coefficients(row, col)
          returns the coefficient.

        linear_constraints.get_coefficients(sequence_of_pairs)
          returns a list of coefficients.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ["x0", "x1"])
        >>> indices = c.linear_constraints.add(\
                names = ["c0", "c1"],\
                lin_expr = [[[1], [1.0]], [[0, 1], [2.0, -1.0]]])
        >>> c.linear_constraints.get_coefficients("c0", "x1")
        1.0
        >>> c.linear_constraints.get_coefficients([("c1", "x0"), ("c1", "x1")])
        [2.0, -1.0]
        """
        def getcoef(row, col):
            return CPX_PROC.getcoef(self._env._e, self._cplex._lp, row, col)
        if len(args) == 2:
            return getcoef(self._conv(args[0]),
                           self._cplex.variables._conv(args[1]))
        if len(args) == 1:
            return [self.get_coefficients(*arg) for arg in args[0]]
        raise WrongNumberOfArgumentsError()

    def get_rows(self, *args):
        """Returns a set of rows of the linear constraint matrix.

        Returns a list of SparsePair instances or a single SparsePair
        instance, depending on the form by which it was called.

        There are four forms by which linear_constraints.get_rows may be
        called.

        linear_constraints.get_rows()
          return the entire linear constraint matrix.

        linear_constraints.get_rows(i)
          i must be a row name or index.  Returns the ith row of
          the linear constraint matrix.

        linear_constraints.get_rows(s)
          s must be a sequence of row names or indices.  Returns the
          rows of the linear constraint matrix indexed by the members
          of s.  Equivalent to
          [linear_constraints.get_rows(i) for i in s]

        linear_constraints.get_rows(begin, end)
          begin and end must be row indices or row names. Returns the
          rows of the linear constraint matrix with indices between begin
          and end, inclusive of end. Equivalent to
          linear_constraints.get_rows(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=["x1", "x2", "x3"])
        >>> indices = c.linear_constraints.add(
        ...     names=["c0", "c1", "c2", "c3"],
        ...     lin_expr=[
        ...         cplex.SparsePair(ind=["x1", "x3"], val=[1.0, -1.0]),
        ...         cplex.SparsePair(ind=["x1", "x2"], val=[1.0, 1.0]),
        ...         cplex.SparsePair(ind=["x1", "x2", "x3"], val=[-1.0] * 3),
        ...         cplex.SparsePair(ind=["x2", "x3"], val=[10.0, -2.0])
        ...     ]
        ... )
        >>> c.linear_constraints.get_rows(0)
        SparsePair(ind = [0, 2], val = [1.0, -1.0])
        >>> for row in c.linear_constraints.get_rows(1,3):
        ...     print(row)
        SparsePair(ind = [0, 1], val = [1.0, 1.0])
        SparsePair(ind = [0, 1, 2], val = [-1.0, -1.0, -1.0])
        SparsePair(ind = [1, 2], val = [10.0, -2.0])
        >>> for row in c.linear_constraints.get_rows(["c2", 0]):
        ...     print(row)
        SparsePair(ind = [0, 1, 2], val = [-1.0, -1.0, -1.0])
        SparsePair(ind = [0, 2], val = [1.0, -1.0])
        >>> for row in c.linear_constraints.get_rows():
        ...     print(row)
        SparsePair(ind = [0, 2], val = [1.0, -1.0])
        SparsePair(ind = [0, 1], val = [1.0, 1.0])
        SparsePair(ind = [0, 1, 2], val = [-1.0, -1.0, -1.0])
        SparsePair(ind = [1, 2], val = [10.0, -2.0])
        """
        def getrows(begin, end=self.get_num() - 1):
            mat = _HBMatrix()
            t = CPX_PROC.getrows(self._env._e, self._cplex._lp, begin, end)
            mat.matbeg = t[0]
            mat.matind = t[1]
            mat.matval = t[2]
            return [m for m in mat]
        return apply_freeform_two_args(getrows, self._conv, args)

    def get_num_nonzeros(self):
        """Returns the number of nonzeros in the linear constraint
        matrix.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=["x1", "x2", "x3"])
        >>> indices = c.linear_constraints.add(
        ...     names=["c0", "c1", "c2", "c3"],
        ...     lin_expr=[
        ...         cplex.SparsePair(ind=["x1", "x3"], val=[1.0, -1.0]),
        ...         cplex.SparsePair(ind=["x1", "x2"], val=[1.0, 1.0]),
        ...         cplex.SparsePair(ind=["x1", "x2", "x3"], val=[-1.0] * 3),
        ...         cplex.SparsePair(ind=["x2", "x3"], val=[10.0, -2.0])
        ...     ]
        ... )
        >>> c.linear_constraints.get_num_nonzeros()
        9
        """
        return CPX_PROC.getnumnz(self._env._e, self._cplex._lp)

    def get_names(self, *args):
        """Returns the names of linear constraints from the problem.

        There are four forms by which linear_constraints.get_names may be called.

        linear_constraints.get_names()
          return the names of all linear constraints from the problem.

        linear_constraints.get_names(i)
          i must be a linear constraint index.  Returns the name of row i.

        linear_constraints.get_names(s)
          s must be a sequence of row indices.  Returns the names of
          the linear constraints with indices the members of s.
          Equivalent to [linear_constraints.get_names(i) for i in s]

        linear_constraints.get_names(begin, end)
          begin and end must be linear constraint indices. Returns the
          names of the linear constraints with indices between begin and
          end, inclusive of end. Equivalent to
          linear_constraints.get_names(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.linear_constraints.add(names = ["c" + str(i) for i in range(10)])
        >>> c.linear_constraints.get_num()
        10
        >>> c.linear_constraints.get_names(8)
        'c8'
        >>> c.linear_constraints.get_names(1, 3)
        ['c1', 'c2', 'c3']
        >>> c.linear_constraints.get_names([2, 0, 5])
        ['c2', 'c0', 'c5']
        >>> c.linear_constraints.get_names()
        ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9']
        """
        def getname(a, b=self.get_num() - 1):
            return CPX_PROC.getrowname(self._env._e, self._cplex._lp,
                                       a, b)
        return apply_freeform_two_args(getname, self._conv, args)

    def get_histogram(self):
        """Returns a histogram of the rows of the linear constraint matrix.

        To access the number of rows with given nonzero counts, use
        slice notation.  If a negative nonzero count is queried in
        this manner an IndexError will be raised.

        The __str__ method of the `Histogram` object returns a string
        displaying the number of rows with given nonzeros counts in
        human readable form.

        The data member "orientation" of the histogram object is
        "row", indicating that the histogram shows the nonzero
        counts for the rows of the linear constraint matrix.

        >>> import cplex
        >>> c = cplex.Cplex("ind.lp")
        >>> histogram = c.linear_constraints.get_histogram()
        >>> print(histogram)
        Row counts (excluding fixed variables):
        <BLANKLINE>
         Nonzero Count:   3   4   5  10  37
        Number of Rows:   1   9   1   4   1
        <BLANKLINE>
        <BLANKLINE>
        >>> histogram[4]
        9
        >>> histogram[2:7]
        [0, 1, 9, 1, 0]
        """
        return Histogram(self._cplex, "row")


class IndicatorType(ConstantClass):
    """Identifiers for types of indicator constraints."""
    if_ = _constants.CPX_INDICATOR_IF
    """CPX_INDICATOR_IF ('->')."""
    onlyif = _constants.CPX_INDICATOR_ONLYIF
    """CPX_INDICATOR_ONLYIF ('<-')"""
    iff = _constants.CPX_INDICATOR_IFANDONLYIF
    """CPX_INDICATOR_IFANDONLYIF ('<->')"""


class IndicatorConstraintInterface(BaseInterface):
    """Methods for adding, modifying, and querying indicator constraints."""

    type_ = IndicatorType()
    """See `IndicatorType()`"""

    def __init__(self, cplex):
        """Creates a new IndicatorConstraintInterface.

        The indicator constraints interface is exposed by the top-level
        `Cplex` class as `Cplex.indicator_constraints`.  This constructor
        is not meant to be used externally.
        """
        super().__init__(cplex=cplex,
                         getindexfunc=CPX_PROC.getindconstrindex)

    def get_num(self):
        """Returns the number of indicator constraints.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.indicator_constraints.add(name="ind1")
        0
        >>> c.indicator_constraints.get_num()
        1
        """
        return CPX_PROC.getnumindconstrs(self._env._e, self._cplex._lp)

    def _add_batch(self, lin_expr, sense, rhs, indvar, complemented, name,
                   indtype):
        if not isinstance(sense, str):
            sense = "".join(sense)
        arg_list = [lin_expr, sense, rhs, indvar, complemented, name,
                    indtype]
        num_new_rows = max_arg_length(arg_list)
        validate_arg_lengths(
            arg_list,
            ": lin_expr, sense, rhs, indvar, complemented, name, indtype"
        )
        with CPX_PROC.chbmatrix(lin_expr, self._cplex._env_lp_ptr,
                                0) as (linmat, nnz):
            CPX_PROC.addindconstr(self._env._e, self._cplex._lp,
                                  num_new_rows,
                                  self._cplex.variables._conv(indvar),
                                  complemented, rhs, sense,
                                  linmat, indtype, name, nnz)

    def add_batch(self, lin_expr=None, sense=None, rhs=None, indvar=None,
                  complemented=None, name=None, indtype=None):
        """Adds indicator constraints to the problem.

        Takes up to eight keyword arguments.

        If more than one argument is specified, all arguments must
        have the same length.

        lin_expr : either a list of SparsePair instances or a matrix in
        list-of-lists format.

        Note
          lin_expr must not contain duplicate indices.  If lin_expr
          references a variable more than once, either by index, name,
          or a combination of index and name, an exception will be
          raised.

        sense : must be either a list of single-character strings or a
        string containing the senses of the indicator constraints.
        Each entry must be one of 'G', 'L', 'E', indicating
        greater-than-or-equal-to (>=), less-than-or-equal-to (<=), and
        equality (=), respectively. Left unspecified, the default is 'E'.

        rhs : a list of floats, specifying the righthand side of each
        indicator constraint.

        indvar : a list of names or indices (or a mixture of the two), of
        the variables that control whether the constraint is active or
        not.

        complemented : a list of values (0 or 1). Default value of 0
        instructs CPLEX to interpret indicator constraint as active when
        the indicator variable is 1. Set complemented to 1 to instruct
        CPLEX that the indicator constraint is active when indvar = 0.

        name : a list of strings that determine the names of the
        individual constraints.

        indtype : a list of the types of indicator constraints. Defaults
        to CPX_INDICATOR_IF ('->').  See `IndicatorType()`.

        Returns an iterator containing the indices of the added indicator
        constraints.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=["x1", "x2", "x3"])
        >>> indices = c.indicator_constraints.add_batch(
        ...     lin_expr=[cplex.SparsePair(ind=["x2"], val=[2.0]),
        ...               cplex.SparsePair(ind=["x3"], val=[2.0])],
        ...     sense="LL",
        ...     rhs=[1.0, 1.0],
        ...     indvar=["x1", "x2"],
        ...     complemented=[0, 0],
        ...     name=["ind1", "ind2"],
        ...     indtype=[c.indicator_constraints.type_.if_,
        ...              c.indicator_constraints.type_.if_])
        >>> len(list(indices))
        2
        """
        (lin_expr, sense, rhs, indvar,
         complemented, name, indtype) = init_list_args(
             lin_expr, sense, rhs, indvar, complemented, name, indtype)
        return self._add_iter(self.get_num, self._add_batch,
                              lin_expr, sense, rhs, indvar, complemented,
                              name, indtype)

    def _add(self, lin_expr, sense, rhs, indvar, complemented, name,
             indtype):
        """non-public"""
        self._add_batch([lin_expr], sense, [rhs], [indvar], [complemented],
                        [name], [indtype])

    def add(self, lin_expr=None, sense="E", rhs=0.0, indvar=0,
            complemented=0, name="", indtype=IndicatorType.if_):
        """Adds an indicator constraint to the problem.

        Takes up to eight keyword arguments.

        lin_expr : either a SparsePair or a list of two lists, the first of
        which contains variable indices or names, the second of which
        contains values.

        Note
          lin_expr must not contain duplicate indices.  If lin_expr
          references a variable more than once, either by index, name,
          or a combination of index and name, an exception will be
          raised.

        sense : the sense of the constraint, may be "L", "G", or "E":
        default is "E"

        rhs : a float defining the righthand side of the constraint

        indvar : the name or index of the variable that controls if
        the constraint is active

        complemented : default value of 0 instructs CPLEX to interpret
        indicator constraint as active when the indicator variable is 1.
        Set complemented to 1 to instruct CPLEX that the indicator
        constraint is active when indvar = 0.

        name : the name of the constraint.

        indtype : the type of indicator constraint. Defaults to
        CPX_INDICATOR_IF ('->').  See `IndicatorType()`.

        Returns the index of the added indicator constraint.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ["x1", "x2"])
        >>> c.indicator_constraints.add(
        ...     indvar="x1",
        ...     complemented=0,
        ...     rhs=1.0,
        ...     sense="G",
        ...     lin_expr=cplex.SparsePair(ind=["x2"], val=[2.0]),
        ...     name="ind1",
        ...     indtype=c.indicator_constraints.type_.if_)
        0
        """
        if lin_expr is None:
            lin_expr = SparsePair()
        # We only ever create one indicator constraint at a time.
        return self._add_single(self.get_num, self._add, lin_expr,
                                sense, rhs, indvar, complemented,
                                name, indtype)

    def delete(self, *args):
        """Deletes indicator constraints from the problem.

        There are four forms by which indicator_constraints.delete may be
        called.

        indicator_constraints.delete()
          deletes all indicator constraints from the problem.

        indicator_constraints.delete(i)
          i must be an indicator constraint name or index. Deletes
          the indicator constraint whose index or name is i.

        indicator_constraints.delete(s)
          s must be a sequence of indicator constraint names or
          indices.  Deletes the indicator constraints with names or
          indices contained within s. Equivalent to
          [indicator_constraints.delete(i) for i in s].

        indicator_constraints.delete(begin, end)
          begin and end must be indicator constraint indices or indicator
          constraint names. Deletes the indicator constraints with
          indices between begin and end, inclusive of end. Equivalent to
          indicator_constraints.delete(range(begin, end + 1)). This will
          give the best performance when deleting batches of indicator
          constraints.

        See :mipapi:`CPXdelindconstrs` in the Callable Library Reference
        Manual for more detail.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> [c.indicator_constraints.add(name=str(i)) for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.indicator_constraints.get_num()
        10
        >>> c.indicator_constraints.delete(8)
        >>> c.indicator_constraints.get_names()
        ['0', '1', '2', '3', '4', '5', '6', '7', '9']
        >>> c.indicator_constraints.delete("1", 3)
        >>> c.indicator_constraints.get_names()
        ['0', '4', '5', '6', '7', '9']
        >>> c.indicator_constraints.delete([2, "0", 5])
        >>> c.indicator_constraints.get_names()
        ['4', '6', '7']
        >>> c.indicator_constraints.delete()
        >>> c.indicator_constraints.get_names()
        []
        """
        def _delete(begin, end=None):
            CPX_PROC.delindconstrs(self._env._e, self._cplex._lp, begin, end)
        delete_set_by_range(_delete, self._conv, self.get_num(), *args)

    def get_indicator_variables(self, *args):
        """Returns the indicator variables of a set of indicator constraints.

        May be called by four forms.

        indicator_constraints.get_indicator_variables()
          return the indicator variables of all indicator constraints
          from the problem.

        indicator_constraints.get_indicator_variables(i)
          i must be an indicator constraint name or index.  Returns the
          indicator variables of the indicator constraint whose index
          or name is i.

        indicator_constraints.get_indicator_variables(s)
          s must be a sequence of indicator constraint names or
          indices.  Returns the indicator variables of the indicator
          constraints with indices the members of s.  Equivalent to
          [indicator_constraints.get_indicator_variables(i) for i in s]

        indicator_constraints.get_indicator_variables(begin, end)
          begin and end must be indicator constraint indices or indicator
          constraint names. Returns the indicator variables of the
          indicator constraints with indices between begin and end,
          inclusive of end. Equivalent to
          indicator_constraints.get_indicator_variables(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(11)], types = "B" * 11)
        >>> [c.indicator_constraints.add(
        ...      name=str(i), indvar=i,
        ...      lin_expr=cplex.SparsePair(ind=[i+1], val=[1.0]))
        ...  for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.indicator_constraints.get_num()
        10
        >>> c.indicator_constraints.get_indicator_variables(8)
        8
        >>> c.indicator_constraints.get_indicator_variables("1",3)
        [1, 2, 3]
        >>> c.indicator_constraints.get_indicator_variables([2,"0",5])
        [2, 0, 5]
        >>> c.indicator_constraints.get_indicator_variables()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        def getindvar(begin, end=self.get_num() - 1):
            return CPX_PROC.getindconstr_constant(
                self._env._e, self._cplex._lp, begin, end)[1]
        return apply_freeform_two_args(getindvar, self._conv, args)

    def get_complemented(self, *args):
        """Returns whether a set of indicator constraints is complemented.

        May be called by four forms.

        indicator_constraints.get_complemented()
          return whether or not all indicator constraints from the
          problem are complemented.

        indicator_constraints.get_complemented(i)
          i must be an indicator constraint name or index.  Returns
          whether or not the indicator constraint whose index or name
          is i is complemented.

        indicator_constraints.get_complemented(s)
          s must be a sequence of indicator constraint names or
          indices.  Returns whether or not the indicator constraints
          with indices the members of s are complemented.  Equivalent
          to [indicator_constraints.get_complemented(i) for i in s]

        indicator_constraints.get_complemented(begin, end)
          begin and end must be indicator constraint indices or indicator
          constraint names. Returns whether or not the indicator
          constraints with indices between begin and end, inclusive of
          end, are complemented. Equivalent to
          indicator_constraints.get_complemented(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(11)], types = "B" * 11)
        >>> [c.indicator_constraints.add(
        ...      name=str(i), indvar=10,
        ...      complemented=i % 2)
        ...  for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.indicator_constraints.get_num()
        10
        >>> c.indicator_constraints.get_complemented(8)
        0
        >>> c.indicator_constraints.get_complemented("1",3)
        [1, 0, 1]
        >>> c.indicator_constraints.get_complemented([2,"0",5])
        [0, 0, 1]
        >>> c.indicator_constraints.get_complemented()
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        """
        def getcomp(begin, end=self.get_num() - 1):
            return CPX_PROC.getindconstr_constant(
                self._env._e, self._cplex._lp, begin, end)[2]
        return apply_freeform_two_args(getcomp, self._conv, args)

    def get_num_nonzeros(self, *args):
        """Returns the number of nonzeros in a set of indicator constraints.

        May be called by four forms.

        indicator_constraints.get_num_nonzeros()
          return the number of nonzeros in all indicator constraints
          from the problem.

        indicator_constraints.get_num_nonzeros(i)
          i must be an indicator constraint name or index.  Returns the
          number of nonzeros in the indicator constraint whose index
          or name is i.

        indicator_constraints.get_num_nonzeros(s)
          s must be a sequence of indicator constraint names or
          indices.  Returns the number of nonzeros in the indicator
          constraints with indices the members of s.  Equivalent to
          [indicator_constraints.get_num_nonzeros(i) for i in s]

        indicator_constraints.get_num_nonzeros(begin, end)
          begin and end must be indicator constraint indices or indicator
          constraint names. Returns the number of nonzeros in the
          indicator constraints with indices between begin and end,
          inclusive of end. Equivalent to
          indicator_constraints.get_num_nonzeros(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(11)], types = "B" * 11)
        >>> [c.indicator_constraints.add(
        ...      name=str(i), indvar=10,
        ...      lin_expr=[range(i), [1.0 * (j+1.0) for j in range(i)]])
        ...  for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.indicator_constraints.get_num()
        10
        >>> c.indicator_constraints.get_num_nonzeros(8)
        8
        >>> c.indicator_constraints.get_num_nonzeros("1",3)
        [1, 2, 3]
        >>> c.indicator_constraints.get_num_nonzeros([2,"0",5])
        [2, 0, 5]
        >>> c.indicator_constraints.get_num_nonzeros()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        def getnnz(a):
            # NB: We return surplus here for nzcnt (this is on purpose).
            return CPX_PROC.getindconstr_constant(
                self._env._e, self._cplex._lp, a, a)[5]
        return apply_freeform_one_arg(
            getnnz, self._conv, self.get_num(), args)

    def get_rhs(self, *args):
        """Returns the righthand side of a set of indicator constraints.

        May be called by four forms.

        indicator_constraints.get_rhs()
          return the righthand side of all indicator constraints
          from the problem.

        indicator_constraints.get_rhs(i)
          i must be an indicator constraint name or index.  Returns the
          righthand side of the indicator constraint whose index or
          name is i.

        indicator_constraints.get_rhs(s)
          s must be a sequence of indicator constraint names or
          indices.  Returns the righthand side of the indicator
          constraints with indices the members of s.  Equivalent to
          [indicator_constraints.get_rhs(i) for i in s]

        indicator_constraints.get_rhs(begin, end)
          begin and end must be indicator constraint indices or indicator
          constraint names. Returns the righthand side of the indicator
          constraints with indices between begin and end, inclusive of
          end. Equivalent to
          indicator_constraints.get_rhs(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> [c.indicator_constraints.add(rhs=1.5 * i, name=str(i)) for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.indicator_constraints.get_num()
        10
        >>> c.indicator_constraints.get_rhs(8)
        12.0
        >>> c.indicator_constraints.get_rhs("1",3)
        [1.5, 3.0, 4.5]
        >>> c.indicator_constraints.get_rhs([2,"0",5])
        [3.0, 0.0, 7.5]
        >>> c.indicator_constraints.get_rhs()
        [0.0, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5]
        """
        def getrhs(begin, end=self.get_num() - 1):
            return CPX_PROC.getindconstr_constant(
                self._env._e, self._cplex._lp, begin, end)[3]
        return apply_freeform_two_args(getrhs, self._conv, args)

    def get_senses(self, *args):
        """Returns the sense of a set of indicator constraints.

        May be called by four forms.

        indicator_constraints.get_senses()
          return the senses of all indicator constraints from the
          problem.

        indicator_constraints.get_senses(i)
          i must be an indicator constraint name or index.  Returns the
          sense of the indicator constraint whose index or name is i.

        indicator_constraints.get_senses(s)
          s must be a sequence of indicator constraint names or
          indices.  Returns the senses of the indicator constraints
          with indices the members of s.  Equivalent to
          [indicator_constraints.get_senses(i) for i in s]

        indicator_constraints.get_senses(begin, end)
          begin and end must be indicator constraint indices or indicator
          constraint names. Returns the senses of the indicator
          constraints with indices between begin and end, inclusive of
          end. Equivalent to
          indicator_constraints.get_senses(range(begin, end + 1)).


        >>> import cplex
        >>> c = cplex.Cplex()
        >>> [c.indicator_constraints.add(name=str(i), sense=j)
        ...  for i, j in enumerate("EGLE")]
        [0, 1, 2, 3]
        >>> c.indicator_constraints.get_num()
        4
        >>> c.indicator_constraints.get_senses(1)
        'G'
        >>> c.indicator_constraints.get_senses("1",3)
        ['G', 'L', 'E']
        >>> c.indicator_constraints.get_senses([2,"0",1])
        ['L', 'E', 'G']
        >>> c.indicator_constraints.get_senses()
        ['E', 'G', 'L', 'E']
        """
        def getsense(begin, end=self.get_num() - 1):
            return CPX_PROC.getindconstr_constant(
                self._env._e, self._cplex._lp, begin, end)[4]
        result = apply_freeform_two_args(getsense, self._conv, args)
        s = [i for i in "".join(result)]
        return s[0] if len(s) == 1 else s

    def get_types(self, *args):
        """Returns the type of a set of indicator constraints.

        See `IndicatorType()`.

        May be called by four forms.

        indicator_constraints.get_types()
          return the types of all indicator constraints from the
          problem.

        indicator_constraints.get_types(i)
          i must be an indicator constraint name or index.  Returns the
          type of the indicator constraint whose index or name is i.

        indicator_constraints.get_types(s)
          s must be a sequence of indicator constraint names or
          indices.  Returns the types of the indicator constraints
          with indices the members of s.  Equivalent to
          [indicator_constraints.get_types(i) for i in s]

        indicator_constraints.get_types(begin, end)
          begin and end must be indicator constraint indices or indicator
          constraint names. Returns the types of the indicator
          constraints with indices between begin and end, inclusive of
          end. Equivalent to
          indicator_constraints.get_types(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> idx = c.indicator_constraints.add(name='i1')
        >>> c.indicator_constraints.get_types(idx)
        1
        >>> c.indicator_constraints.type_[1]
        'if_'
        """
        def gettype(begin, end=self.get_num() - 1):
            return CPX_PROC.getindconstr_constant(
                self._env._e, self._cplex._lp, begin, end)[0]
        return apply_freeform_two_args(gettype, self._conv, args)

    def get_linear_components(self, *args):
        """Returns the linear constraint of a set of indicator
        constraints.

        Returns a list of SparsePair instances or a single SparsePair
        instance, depending on the form by which it was called.

        May be called by four forms.

        indicator_constraints.get_linear_components()
          return the linear components of all indicator constraints
          from the problem.

        indicator_constraints.get_linear_components(i)
          i must be an indicator constraint name or index.  Returns the
          linear component of the indicator constraint whose index or
          name is i.

        indicator_constraints.get_linear_components(s)
          s must be a sequence of indicator constraint names or
          indices.  Returns the linear components of the indicator
          constraints with indices the members of s.  Equivalent to
          [indicator_constraints.get_linear_components(i) for i in s]

        indicator_constraints.get_linear_components(begin, end)
          begin and end must be indicator constraint indices or indicator
          constraint names. Returns the linear components of the
          indicator constraints with indices between begin and end,
          inclusive of end. Equivalent to
          indicator_constraints.get_linear_components(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(
        ...     names=[str(i) for i in range(4)],
        ...     types="B" * 4
        ... )
        >>> [c.indicator_constraints.add(
        ...      name=str(i), indvar=3,
        ...      lin_expr=[range(i), [1.0 * (j+1.0) for j in range(i)]])
        ...  for i in range(3)]
        [0, 1, 2]
        >>> c.indicator_constraints.get_num()
        3
        >>> c.indicator_constraints.get_linear_components(2)
        SparsePair(ind = [0, 1], val = [1.0, 2.0])
        >>> for row in c.indicator_constraints.get_linear_components("0", 1):
        ...     print(row)
        SparsePair(ind = [], val = [])
        SparsePair(ind = [0], val = [1.0])
        >>> for row in c.indicator_constraints.get_linear_components([1, "0"]):
        ...     print(row)
        SparsePair(ind = [0], val = [1.0])
        SparsePair(ind = [], val = [])
        >>> for row in c.indicator_constraints.get_linear_components():
        ...     print(row)
        SparsePair(ind = [], val = [])
        SparsePair(ind = [0], val = [1.0])
        SparsePair(ind = [0, 1], val = [1.0, 2.0])
        """
        def getlin(begin, end=self.get_num() - 1):
            mat = _HBMatrix()
            mat.matbeg, mat.matind, mat.matval = CPX_PROC.getindconstr(
                self._env._e, self._cplex._lp, begin, end)
            return [m for m in mat]
        return apply_freeform_two_args(getlin, self._conv, args)

    def get_names(self, *args):
        """Returns the names of a set of indicator constraints.

        May be called by four forms.

        indicator_constraints.get_names()
          return the names of all indicator constraints from the
          problem.

        indicator_constraints.get_names(i)
          i must be an indicator constraint index.  Returns the name
          of constraint i.

        indicator_constraints.get_names(s)
          s must be a sequence of indicator constraint indices.
          Returns the names of the indicator constraints with indices
          the members of s.  Equivalent to
          [indicator_constraints.get_names(i) for i in s]

        indicator_constraints.get_names(begin, end)
          begin and end must be indicator constraint indices. Returns the
          names of the indicator constraints with indices between begin
          and end, inclusive of end. Equivalent to
          indicator_constraints.get_names(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> [c.indicator_constraints.add(name="i" + str(i))
        ...  for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.indicator_constraints.get_num()
        10
        >>> c.indicator_constraints.get_names(8)
        'i8'
        >>> c.indicator_constraints.get_names(1, 3)
        ['i1', 'i2', 'i3']
        >>> c.indicator_constraints.get_names([2, 0, 5])
        ['i2', 'i0', 'i5']
        >>> c.indicator_constraints.get_names()
        ['i0', 'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9']
        """
        def getname(a):
            return CPX_PROC.getindconstrname(
                self._env._e, self._cplex._lp, a)
        return apply_freeform_one_arg(
            getname, self._conv, self.get_num(), args)


class QuadraticConstraintInterface(BaseInterface):
    """Methods for adding, modifying, and querying quadratic constraints."""

    def __init__(self, cplex):
        """Creates a new QuadraticConstraintInterface.

        The quadratic constraints interface is exposed by the top-level
        `Cplex` class as `Cplex.quadratic_constraints`.  This constructor
        is not meant to be used externally.
        """
        super().__init__(cplex=cplex, getindexfunc=CPX_PROC.getqconstrindex)

    def get_num(self):
        """Returns the number of quadratic constraints.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ['x','y'])
        >>> l = cplex.SparsePair(ind = ['x'], val = [1.0])
        >>> q = cplex.SparseTriple(ind1 = ['x'], ind2 = ['y'], val = [1.0])
        >>> [c.quadratic_constraints.add(name=str(i), lin_expr=l, quad_expr=q)
        ...  for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.quadratic_constraints.get_num()
        10
        """
        return CPX_PROC.getnumqconstrs(self._env._e, self._cplex._lp)

    def _add(self, lin_expr, quad_expr, sense, rhs, name):
        """non-public"""
        ind, val = unpack_pair(lin_expr)
        if len(val) == 1 and val[0] == 0.0:
            ind = []
            val = []
        ind1, ind2, qval = unpack_triple(quad_expr)
        varcache = {}
        CPX_PROC.addqconstr(self._env._e, self._cplex._lp, rhs, sense,
                            self._cplex.variables._conv(ind, varcache),
                            val,
                            self._cplex.variables._conv(ind1, varcache),
                            self._cplex.variables._conv(ind2, varcache),
                            qval, name)

    def add(self, lin_expr=None, quad_expr=None, sense="L", rhs=0.0, name=""):
        """Adds a quadratic constraint to the problem.

        Takes up to five keyword arguments:

        lin_expr : either a SparsePair or a list of two lists specifying
        the linear component of the constraint.

        Note
          lin_expr must not contain duplicate indices.  If lin_expr
          references a variable more than once, either by index, name,
          or a combination of index and name, an exception will be
          raised.

        quad_expr : either a SparseTriple or a list of three lists
        specifying the quadratic component of the constraint.

        Note
          quad_expr must not contain duplicate indices.  If quad_expr
          references a matrix entry more than once, either by indices,
          names, or a combination of indices and names, an exception
          will be raised.

        sense : either "L", "G", or "E"

        rhs : a float specifying the righthand side of the constraint.

        name : the name of the constraint.

        Returns the index of the added quadratic constraint.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ['x','y'])
        >>> l = cplex.SparsePair(ind = ['x'], val = [1.0])
        >>> q = cplex.SparseTriple(ind1 = ['x'], ind2 = ['y'], val = [1.0])
        >>> c.quadratic_constraints.add(name = "my_quad",
        ...                             lin_expr = l,
        ...                             quad_expr = q,
        ...                             rhs = 1.0,
        ...                             sense = "G")
        0
        """
        if lin_expr is None:
            lin_expr = SparsePair([0], [0.0])
        if quad_expr is None:
            quad_expr = SparseTriple([0], [0], [0.0])
        # We only ever create one quadratic constraint at a time.
        return self._add_single(self.get_num, self._add,
                                lin_expr, quad_expr, sense, rhs, name)

    def delete(self, *args):
        """Deletes quadratic constraints from the problem.

        There are four forms by which quadratic_constraints.delete may be
        called.

        quadratic_constraints.delete()
          deletes all quadratic constraints from the problem.

        quadratic_constraints.delete(i)
          i must be a quadratic constraint name or index. Deletes
          the quadratic constraint whose index or name is i.

        quadratic_constraints.delete(s)
          s must be a sequence of quadratic constraint names or
          indices. Deletes the quadratic constraints with names or
          indices contained within s. Equivalent to
          [quadratic_constraints.delete(i) for i in s].

        quadratic_constraints.delete(begin, end)
          begin and end must be quadratic constraint indices or quadratic
          constraint names. Deletes the quadratic constraints with
          indices between begin and end, inclusive of end. Equivalent to
          quadratic_constraints.delete(range(begin, end + 1)). This will
          give the best performance when deleting batches of quadratic
          constraints.

        See :socpapi:`CPXdelqconstrs` in the Callable Library Reference
        Manual for more detail.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=['x', 'y'])
        >>> l = cplex.SparsePair(ind=['x'], val=[1.0])
        >>> q = cplex.SparseTriple(ind1=['x'], ind2=['y'], val=[1.0])
        >>> [c.quadratic_constraints.add(
        ...      name=str(i), lin_expr=l, quad_expr=q)
        ...  for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.quadratic_constraints.get_num()
        10
        >>> c.quadratic_constraints.delete(8)
        >>> c.quadratic_constraints.get_names()
        ['0', '1', '2', '3', '4', '5', '6', '7', '9']
        >>> c.quadratic_constraints.delete("1", 3)
        >>> c.quadratic_constraints.get_names()
        ['0', '4', '5', '6', '7', '9']
        >>> c.quadratic_constraints.delete([2, "0", 5])
        >>> c.quadratic_constraints.get_names()
        ['4', '6', '7']
        >>> c.quadratic_constraints.delete()
        >>> c.quadratic_constraints.get_names()
        []
        """
        def _delete(begin, end=None):
            CPX_PROC.delqconstrs(self._env._e, self._cplex._lp, begin, end)
        delete_set_by_range(_delete, self._conv, self.get_num(), *args)

    def get_rhs(self, *args):
        """Returns the righthand side of a set of quadratic constraints.

        Can be called by four forms.

        quadratic_constraints.get_rhs()
          return the righthand side of all quadratic constraints
          from the problem.

        quadratic_constraints.get_rhs(i)
          i must be a quadratic constraint name or index.  Returns the
          righthand side of the quadratic constraint whose index or
          name is i.

        quadratic_constraints.get_rhs(s)
          s must be a sequence of quadratic constraint names or
          indices.  Returns the righthand side of the quadratic
          constraints with indices the members of s.  Equivalent to
          [quadratic_constraints.get_rhs(i) for i in s]

        quadratic_constraints.get_rhs(begin, end)
          begin and end must be quadratic constraint indices or quadratic
          constraint names. Returns the righthand side of the quadratic
          constraints with indices between begin and end, inclusive of
          end. Equivalent to
          quadratic_constraints.get_rhs(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(10)])
        >>> [c.quadratic_constraints.add(rhs=1.5 * i, name=str(i))
        ...  for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.quadratic_constraints.get_num()
        10
        >>> c.quadratic_constraints.get_rhs(8)
        12.0
        >>> c.quadratic_constraints.get_rhs("1",3)
        [1.5, 3.0, 4.5]
        >>> c.quadratic_constraints.get_rhs([2,"0",5])
        [3.0, 0.0, 7.5]
        >>> c.quadratic_constraints.get_rhs()
        [0.0, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5]
        """
        def getrhs(a):
            return CPX_PROC.getqconstr_info(
                self._env._e, self._cplex._lp, a)[0]
        return apply_freeform_one_arg(
            getrhs, self._conv, self.get_num(), args)

    def get_senses(self, *args):
        """Returns the senses of a set of quadratic constraints.

        Can be called by four forms.

        quadratic_constraints.get_senses()
          return the senses of all quadratic constraints from the
          problem.

        quadratic_constraints.get_senses(i)
          i must be a quadratic constraint name or index.  Returns the
          sense of the quadratic constraint whose index or name is i.

        quadratic_constraints.get_senses(s)
          s must be a sequence of quadratic constraint names or
          indices.  Returns the senses of the quadratic constraints
          with indices the members of s.  Equivalent to
          [quadratic_constraints.get_senses(i) for i in s]

        quadratic_constraints.get_senses(begin, end)
          begin and end must be quadratic constraint indices or quadratic
          constraint names. Returns the senses of the quadratic
          constraints with indices between begin and end, inclusive of
          end. Equivalent to
          quadratic_constraints.get_senses(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ["x0"])
        >>> [c.quadratic_constraints.add(name=str(i), sense=j)
        ...  for i, j in enumerate("GGLL")]
        [0, 1, 2, 3]
        >>> c.quadratic_constraints.get_num()
        4
        >>> c.quadratic_constraints.get_senses(1)
        'G'
        >>> c.quadratic_constraints.get_senses("1",3)
        ['G', 'L', 'L']
        >>> c.quadratic_constraints.get_senses([2,"0",1])
        ['L', 'G', 'G']
        >>> c.quadratic_constraints.get_senses()
        ['G', 'G', 'L', 'L']
        """
        def getsense(a):
            return CPX_PROC.getqconstr_info(
                self._env._e, self._cplex._lp, a)[1]
        return apply_freeform_one_arg(
            getsense, self._conv, self.get_num(), args)

    def get_linear_num_nonzeros(self, *args):
        """Returns the number of nonzeros in the linear part of a set of quadratic constraints.

        Can be called by four forms.

        quadratic_constraints.get_linear_num_nonzeros()
          return the number of nonzeros in all quadratic constraints
          from the problem.

        quadratic_constraints.get_linear_num_nonzeros(i)
          i must be a quadratic constraint name or index.  Returns the
          number of nonzeros in the quadratic constraint whose index
          or name is i.

        quadratic_constraints.get_linear_num_nonzeros(s)
          s must be a sequence of quadratic constraint names or
          indices.  Returns the number of nonzeros in the quadratic
          constraints with indices the members of s.  Equivalent to
          [quadratic_constraints.get_linear_num_nonzeros(i) for i in s]

        quadratic_constraints.get_linear_num_nonzeros(begin, end)
          begin and end must be quadratic constraint indices or quadratic
          constraint names. Returns the number of nonzeros in the
          quadratic constraints with indices between begin and end,
          inclusive of end. Equivalent to
          quadratic_constraints.get_linear_num_nonzeros(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(11)], types = "B" * 11)
        >>> [c.quadratic_constraints.add(
        ...      name = str(i),
        ...      lin_expr = [range(i), [1.0 * (j+1.0) for j in range(i)]])
        ...  for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.quadratic_constraints.get_num()
        10
        >>> c.quadratic_constraints.get_linear_num_nonzeros(8)
        8
        >>> c.quadratic_constraints.get_linear_num_nonzeros("1",3)
        [1, 2, 3]
        >>> c.quadratic_constraints.get_linear_num_nonzeros([2,"0",5])
        [2, 0, 5]
        >>> c.quadratic_constraints.get_linear_num_nonzeros()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        def getlinnz(a):
            return CPX_PROC.getqconstr_info(
                self._env._e, self._cplex._lp, a)[2]
        return apply_freeform_one_arg(
            getlinnz, self._conv, self.get_num(), args)

    def get_linear_components(self, *args):
        """Returns the linear part of a set of quadratic constraints.

        Returns a list of SparsePair instances or one SparsePair
        instance.

        Can be called by four forms.

        quadratic_constraints.get_linear_components()
          return the linear components of all quadratic constraints
          from the problem.

        quadratic_constraints.get_linear_components(i)
          i must be a quadratic constraint name or index.  Returns the
          linear component of the quadratic constraint whose index or
          name is i.

        quadratic_constraints.get_linear_components(s)
          s must be a sequence of quadratic constraint names or
          indices.  Returns the linear components of the quadratic
          constraints with indices the members of s.  Equivalent to
          [quadratic_constraints.get_linear_components(i) for i in s]

        quadratic_constraints.get_linear_components(begin, end)
          begin and end must be quadratic constraint indices or quadratic
          constraint names. Returns the linear components of the
          quadratic constraints with indices between begin and end,
          inclusive of end. Equivalent to
          quadratic_constraints.get_linear_components(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(
        ...     names=[str(i) for i in range(4)],
        ...     types="B" * 4
        ... )
        >>> [c.quadratic_constraints.add(
        ...      name=str(i),
        ...      lin_expr=[range(i), [1.0 * (j+1.0) for j in range(i)]])
        ...  for i in range(3)]
        [0, 1, 2]
        >>> c.quadratic_constraints.get_num()
        3
        >>> c.quadratic_constraints.get_linear_components(2)
        SparsePair(ind = [0, 1], val = [1.0, 2.0])
        >>> for row in c.quadratic_constraints.get_linear_components("0", 1):
        ...     print(row)
        SparsePair(ind = [], val = [])
        SparsePair(ind = [0], val = [1.0])
        >>> for row in c.quadratic_constraints.get_linear_components([1, "0"]):
        ...     print(row)
        SparsePair(ind = [0], val = [1.0])
        SparsePair(ind = [], val = [])
        >>> for row in c.quadratic_constraints.get_linear_components():
        ...     print(row)
        SparsePair(ind = [], val = [])
        SparsePair(ind = [0], val = [1.0])
        SparsePair(ind = [0, 1], val = [1.0, 2.0])
        """
        def getlin(a):
            return SparsePair(*CPX_PROC.getqconstr_lin(
                self._env._e, self._cplex._lp, a))
        return apply_freeform_one_arg(
            getlin, self._conv, self.get_num(), args)

    def get_quad_num_nonzeros(self, *args):
        """Returns the number of nonzeros in the quadratic part of a set of quadratic constraints.

        Can be called by four forms.

        quadratic_constraints.get_quad_num_nonzeros()
          Returns the number of nonzeros in all quadratic constraints
          from the problem.

        quadratic_constraints.get_quad_num_nonzeros(i)
          i must be a quadratic constraint name or index.  Returns the
          number of nonzeros in the quadratic constraint whose index
          or name is i.

        quadratic_constraints.get_quad_num_nonzeros(s)
          s must be a sequence of quadratic constraint names or
          indices.  Returns the number of nonzeros in the quadratic
          constraints with indices the members of s.  Equivalent to
          [quadratic_constraints.get_quad_num_nonzeros(i) for i in s]

        quadratic_constraints.get_quad_num_nonzeros(begin, end)
          begin and end must be quadratic constraint indices or quadratic
          constraint names. Returns the number of nonzeros in the
          quadratic constraints with indices between begin and end,
          inclusive of end. Equivalent to
          quadratic_constraints.get_quad_num_nonzeros(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(11)])
        >>> [c.quadratic_constraints.add(
        ...      name = str(i),
        ...      quad_expr = [range(i), range(i), [1.0 * (j+1.0) for j in range(i)]])
        ...  for i in range(1, 11)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.quadratic_constraints.get_num()
        10
        >>> c.quadratic_constraints.get_quad_num_nonzeros(8)
        9
        >>> c.quadratic_constraints.get_quad_num_nonzeros("1",2)
        [1, 2, 3]
        >>> c.quadratic_constraints.get_quad_num_nonzeros([2,"1",5])
        [3, 1, 6]
        >>> c.quadratic_constraints.get_quad_num_nonzeros()
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        """
        def getquadnz(a):
            return CPX_PROC.getqconstr_info(
                self._env._e, self._cplex._lp, a)[3]
        return apply_freeform_one_arg(
            getquadnz, self._conv, self.get_num(), args)

    def get_quadratic_components(self, *args):
        """Returns the quadratic part of a set of quadratic constraints.

        Can be called by four forms.

        quadratic_constraints.get_quadratic_components()
          return the quadratic components of all quadratic constraints
          from the problem.

        quadratic_constraints.get_quadratic_components(i)
          i must be a quadratic constraint name or index.  Returns the
          quadratic component of the quadratic constraint whose index or
          name is i.

        quadratic_constraints.get_quadratic_components(s)
          s must be a sequence of quadratic constraint names or
          indices.  Returns the quadratic components of the quadratic
          constraints with indices the members of s.  Equivalent to
          [quadratic_constraints.get_quadratic_components(i) for i in s]

        quadratic_constraints.get_quadratic_components(begin, end)
          begin and end must be quadratic constraint indices or quadratic
          constraint names. Returns the quadratic components of the
          quadratic constraints with indices between begin and end,
          inclusive of end. Equivalent to
          quadratic_constraints.get_quadratic_components(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(
        ...     names=[str(i) for i in range(4)]
        ... )
        >>> [c.quadratic_constraints.add(
        ...      name="q{0}".format(i),
        ...      quad_expr=[range(i), range(i),
        ...                 [1.0 * (j+1.0) for j in range(i)]])
        ...  for i in range(1, 3)]
        [0, 1]
        >>> c.quadratic_constraints.get_num()
        2
        >>> c.quadratic_constraints.get_quadratic_components(1)
        SparseTriple(ind1 = [0, 1], ind2 = [0, 1], val = [1.0, 2.0])
        >>> for quad in c.quadratic_constraints.get_quadratic_components("q1", 1):
        ...     print(quad)
        SparseTriple(ind1 = [0], ind2 = [0], val = [1.0])
        SparseTriple(ind1 = [0, 1], ind2 = [0, 1], val = [1.0, 2.0])
        >>> for quad in c.quadratic_constraints.get_quadratic_components(["q2", 0]):
        ...     print(quad)
        SparseTriple(ind1 = [0, 1], ind2 = [0, 1], val = [1.0, 2.0])
        SparseTriple(ind1 = [0], ind2 = [0], val = [1.0])
        >>> for quad in c.quadratic_constraints.get_quadratic_components():
        ...     print(quad)
        SparseTriple(ind1 = [0], ind2 = [0], val = [1.0])
        SparseTriple(ind1 = [0, 1], ind2 = [0, 1], val = [1.0, 2.0])
        """
        def getquad(a):
            return SparseTriple(*CPX_PROC.getqconstr_quad(
                self._env._e, self._cplex._lp, a))
        return apply_freeform_one_arg(
            getquad, self._conv, self.get_num(), args)

    def get_names(self, *args):
        """Returns the names of a set of quadratic constraints.

        Can be called by four forms.

        quadratic_constraints.get_names()
          return the names of all quadratic constraints from the
          problem.

        quadratic_constraints.get_names(i)
          i must be a quadratic constraint index.  Returns the name
          of constraint i.

        quadratic_constraints.get_names(s)
          s must be a sequence of quadratic constraint indices.
          Returns the names of the quadratic constraints with indices
          the members of s.  Equivalent to
          [quadratic_constraints.get_names(i) for i in s]

        quadratic_constraints.get_names(begin, end)
          begin and end must be quadratic constraint indices. Returns
          the names of the quadratic constraints with indices between
          begin and end, inclusive of end. Equivalent to
          quadratic_constraints.get_names(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(11)])
        >>> [c.quadratic_constraints.add(
        ...      name = "q" + str(i),
        ...      quad_expr = [range(i), range(i), [1.0 * (j+1.0) for j in range(i)]])
        ...  for i in range(1, 11)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.quadratic_constraints.get_num()
        10
        >>> c.quadratic_constraints.get_names(8)
        'q9'
        >>> c.quadratic_constraints.get_names(1, 3)
        ['q2', 'q3', 'q4']
        >>> c.quadratic_constraints.get_names([2, 0, 5])
        ['q3', 'q1', 'q6']
        >>> c.quadratic_constraints.get_names()
        ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']
        """
        def getname(a):
            return CPX_PROC.getqconstrname(
                self._env._e, self._cplex._lp, a)
        return apply_freeform_one_arg(
            getname, self._conv, self.get_num(), args)


class SOSType(ConstantClass):
    """Constants defining the type of special ordered sets.

    For a definition of SOS type 1 and 2, see those topics in the CPLEX
    User's Manual.
    """
    SOS1 = _constants.CPX_TYPE_SOS1
    SOS2 = _constants.CPX_TYPE_SOS2


class SOSInterface(BaseInterface):
    """Class containing methods for Special Ordered Sets (SOS)."""

    type = SOSType()
    """See `SOSType()` """

    def __init__(self, cplex):
        """Creates a new SOSInterface.

        The SOS interface is exposed by the top-level `Cplex` class as
        `Cplex.SOS`.  This constructor is not meant to be used
        externally.
        """
        super().__init__(cplex=cplex, getindexfunc=CPX_PROC.getsosindex)

    def get_num(self):
        """Returns the number of special ordered sets."""
        return CPX_PROC.getnumsos(self._env._e, self._cplex._lp)

    # FIXME: 'type' and 'SOS' are bad variable names.  type is a "reserved"
    #        word and SOS should be lowercased.
    def _add(self, type, SOS, name):
        """non-public"""
        indices, weights = unpack_pair(SOS)
        CPX_PROC.addsos(self._env._e, self._cplex._lp, type, [0],
                        self._cplex.variables._conv(indices),
                        weights, [name])

    def add(self, type="1", SOS=None, name=""):
        """Adds a special ordered set constraint to the problem.

        Takes three keyword arguments.

        type : can be either SOS.type.SOS1 or SOS.type.SOS2

        SOS : either a SparsePair or a list of two lists, the first of
        which contains variable indices or names, the second of which
        contains the weights to assign to those variables.

        name: the name of the SOS

        Returns the index of the added SOS constraint.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(10)])
        >>> c.SOS.add(type = "1", name = "type_one",
        ...           SOS = cplex.SparsePair(ind = ["2", "3"],
        ...                                  val = [25.0, 18.0]))
        0
        >>> c.SOS.add(type = "2", name = "type_two",
        ...           SOS = cplex.SparsePair(ind = ["2", "4", "7", "3"],
        ...                                  val = [1.0, 3.0, 25.0, 18.0]))
        1
        """
        if SOS is None:
            SOS = SparsePair([0], [0.0])
        # We only ever create one sos constraint at a time.
        return self._add_single(self.get_num, self._add,
                                type, SOS, name)

    def delete(self, *args):
        """Deletes special ordered sets from the problem.

        There are four forms by which SOS.delete may be called.

        SOS.delete()
          deletes all SOS constraints from the problem.

        SOS.delete(i)
          i must be a SOS constraint name or index. Deletes the SOS
          constraint indexed as i or named i.

        SOS.delete(s)
          s must be a sequence of SOS constraint names or indices.
          Deletes the SOS constraints with names or indices contained
          within s. Equivalent to [SOS.delete(i) for i in s].

        SOS.delete(begin, end)
          begin and end must be SOS constraint indices or SOS constraint
          names. Deletes the SOS constraints with indices between begin
          and end, inclusive of end. Equivalent to
          SOS.delete(range(begin, end + 1)). This will give the best
          performance when deleting batches of SOS constraints.

        See :mipapi:`CPXdelsos` in the Callable Library Reference Manual
        for more detail.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=['x', 'y'])
        >>> l = cplex.SparsePair(ind=['x'], val=[1.0])
        >>> [c.SOS.add(name=str(i), SOS=l) for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.SOS.get_num()
        10
        >>> c.SOS.delete(8)
        >>> c.SOS.get_names()
        ['0', '1', '2', '3', '4', '5', '6', '7', '9']
        >>> c.SOS.delete("1", 3)
        >>> c.SOS.get_names()
        ['0', '4', '5', '6', '7', '9']
        >>> c.SOS.delete([2, "0", 5])
        >>> c.SOS.get_names()
        ['4', '6', '7']
        >>> c.SOS.delete()
        >>> c.SOS.get_names()
        []
        """
        def _delete(begin, end=None):
            CPX_PROC.delsos(self._env._e, self._cplex._lp, begin, end)
        delete_set_by_range(_delete, self._conv, self.get_num(), *args)

    def get_sets(self, *args):
        """Returns the sets of variables and their corresponding weights.

        Returns a SparsePair instance or a list of SparsePair instances.

        Can be called by four forms.

        SOS.get_sets()
          return the set of variables and weights of all SOS
          constraints from the problem.

        SOS.get_sets(i)
          i must be a SOS constraint name or index.  Returns the set
          of variables and weights of the SOS constraint whose index
          or name is i.

        SOS.get_sets(s)
          s must be a sequence of SOS constraint names or indices.
          Returns the variables and weights of the SOS constraints
          with indices the members of s.  Equivalent to
          [SOS.get_sets(i) for i in s]

        SOS.get_sets(begin, end)
          begin and end must be SOS constraint indices or SOS constraint
          names. Returns the variables and weights of the SOS constraints
          with indices between begin and end, inclusive of end.
          Equivalent to SOS.get_sets(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(
        ...     names=[str(i) for i in range(4)],
        ...     types="B" * 4
        ... )
        >>> [c.SOS.add(
        ...      name="s{0}".format(i),
        ...      SOS=[range(i), [1.0 * (j+1.0) for j in range(i)]])
        ...  for i in range(1, 3)]
        [0, 1]
        >>> c.SOS.get_num()
        2
        >>> c.SOS.get_sets(1)
        SparsePair(ind = [0, 1], val = [1.0, 2.0])
        >>> for s in c.SOS.get_sets("s1", 1):
        ...     print(s)
        SparsePair(ind = [0], val = [1.0])
        SparsePair(ind = [0, 1], val = [1.0, 2.0])
        >>> for s in c.SOS.get_sets(["s2", 0]):
        ...     print(s)
        SparsePair(ind = [0, 1], val = [1.0, 2.0])
        SparsePair(ind = [0], val = [1.0])
        >>> for s in c.SOS.get_sets():
        ...     print(s)
        SparsePair(ind = [0], val = [1.0])
        SparsePair(ind = [0, 1], val = [1.0, 2.0])
        """
        def getsos(a, b=self.get_num() - 1):
            ret = CPX_PROC.getsos(self._env._e, self._cplex._lp, a, b)
            mat = _HBMatrix()
            mat.matbeg = ret[0]
            mat.matind = ret[1]
            mat.matval = ret[2]
            return [m for m in mat]
        return apply_freeform_two_args(getsos, self._conv, args)

    def get_types(self, *args):
        """Returns the type of a set of special ordered sets.

        Return values are attributes of Cplex.SOS.type.

        Can be called by four forms.

        SOS.get_types()
          return the type of all SOS constraints.

        SOS.get_types(i)
          i must be a SOS constraint name or index.  Returns the type
          of the SOS constraint whose index or name is i.

        SOS.get_types(s)
          s must be a sequence of SOS constraint names or indices.
          Returns the type of the SOS constraints with indices the
          members of s.  Equivalent to [SOS.get_types(i) for i in s]

        SOS.get_types(begin, end)
          begin and end must be SOS constraint indices or SOS constraint
          names. Returns the type of the SOS constraints with indices
          between begin and end, inclusive of end. Equivalent to
          SOS.get_types(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(11)], types = "B" * 11)
        >>> [c.SOS.add(name = str(i), type = str(i % 2 + 1))
        ...  for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.SOS.get_num()
        10
        >>> c.SOS.get_types(8)
        '1'
        >>> c.SOS.get_types("1",3)
        ['2', '1', '2']
        >>> c.SOS.get_types([2,"0",5])
        ['1', '1', '2']
        >>> c.SOS.get_types()
        ['1', '2', '1', '2', '1', '2', '1', '2', '1', '2']
        """
        def gettype(a, b=self.get_num() - 1):
            return CPX_PROC.getsos_info(self._env._e, self._cplex._lp, a, b)[0]
        t = [i for i in "".join(apply_freeform_two_args(
            gettype, self._conv, args))]
        return t[0] if len(t) == 1 else t

    def get_num_members(self, *args):
        """Returns the size of a set of special ordered sets.

        Can be called by four forms.

        SOS.get_num_members()
          return the number of variables in all SOS constraints from
          the problem.

        SOS.get_num_members(i)
          i must be a SOS constraint name or index.  Returns the
          number of variables in the SOS constraint whose index or
          name is i.

        SOS.get_num_members(s)
          s must be a sequence of SOS constraint names or indices.
          Returns the number of variables in the SOS constraints with
          indices the members of s.  Equivalent to
          [SOS.get_num_members(i) for i in s]

        SOS.get_num_members(begin, end)
          begin and end must be SOS constraint indices or SOS constraint
          names. Returns the number of variables in the SOS constraints
          with indices between begin and end, inclusive of end.
          Equivalent to SOS.get_num_members(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(11)], types = "B" * 11)
        >>> [c.SOS.add(name = str(i),
        ...            SOS = [range(i), [1.0 * (j+1.0) for j in range(i)]])
        ...  for i in range(1,11)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.SOS.get_num()
        10
        >>> c.SOS.get_num_members(7)
        8
        >>> c.SOS.get_num_members("1",2)
        [1, 2, 3]
        >>> c.SOS.get_num_members([3,"1",4])
        [4, 1, 5]
        >>> c.SOS.get_num_members()
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        """
        def getsize(a):
            return CPX_PROC.getsos_info(self._env._e, self._cplex._lp, a, a)[1]
        return apply_freeform_one_arg(
            getsize, self._conv, self.get_num(), args)

    def get_names(self, *args):
        """Returns the names of a set of special ordered sets.

        Can be called by four forms.

        SOS.get_names()
          return the names of all SOS constraints from the problem.

        SOS.get_names(i)
          i must be an SOS constraint index.  Returns the name of
          SOS constraint i.

        SOS.get_names(s)
          s must be a sequence of SOS constraint indices.  Returns
          the names of the SOS constraints with indices the members
          of s.  Equivalent to [SOS.get_names(i) for i in s]

        SOS.get_names(begin, end)
          begin and end must be SOS constraint indices. Returns the names
          of the SOS constraints with indices between begin and end,
          inclusive of end. Equivalent to
          SOS.get_names(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ["x0"])
        >>> [c.SOS.add(name = "sos" + str(i)) for i in range(1, 11)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.SOS.get_num()
        10
        >>> c.SOS.get_names(8)
        'sos9'
        >>> c.SOS.get_names(1, 3)
        ['sos2', 'sos3', 'sos4']
        >>> c.SOS.get_names([2, 0, 5])
        ['sos3', 'sos1', 'sos6']
        >>> c.SOS.get_names()
        ['sos1', 'sos2', 'sos3', 'sos4', 'sos5', 'sos6', 'sos7', 'sos8', 'sos9', 'sos10']
        """
        def getname(a, b=self.get_num() - 1):
            return CPX_PROC.getsosname(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(getname, self._conv, args)


class EffortLevel(ConstantClass):
    """Effort levels associated with a MIP start"""
    auto = _constants.CPX_MIPSTART_AUTO
    check_feasibility = _constants.CPX_MIPSTART_CHECKFEAS
    solve_fixed = _constants.CPX_MIPSTART_SOLVEFIXED
    solve_MIP = _constants.CPX_MIPSTART_SOLVEMIP
    repair = _constants.CPX_MIPSTART_REPAIR
    no_check = _constants.CPX_MIPSTART_NOCHECK


class MIPStartsInterface(BaseInterface):
    """Contains methods pertaining to MIP starts."""

    effort_level = EffortLevel()
    """See `EffortLevel()` """

    def __init__(self, cplex):
        """Creates a new MIPStartsInterface.

        The MIP starts interface is exposed by the top-level `Cplex`
        class as `Cplex.MIP_starts`.  This constructor is not meant to be
        used externally.
        """
        super().__init__(cplex=cplex,
                         getindexfunc=CPX_PROC.getmipstartindex)

    def get_num(self):
        """Returns the number of MIP starts currently stored.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(
        ...     names = [str(i) for i in range(11)],
        ...     types = "I" * 11)
        >>> indices = c.MIP_starts.add(
        ...     [(cplex.SparsePair(ind = [i], val = [0.0]),
        ...       c.MIP_starts.effort_level.auto) for i in range(5)])
        >>> c.MIP_starts.get_num()
        5
        """
        return CPX_PROC.getnummipstarts(self._env._e, self._cplex._lp)

    def read(self, filename):
        """Reads MIP starts from a file.

        This method reads a file in the format MST and copies the
        information of all the MIP starts contained in that file into a
        CPLEX problem object.  The parameter cplex.parameters.advance
        must be set to cplex.parameters.advance.values.standard, its
        default value, or cplex.parameters.advance.values.alternate
        in order for the MIP starts to be used.

        Note
          If the MIP start file is successfully read, then any
          previously existing MIP starts will be deleted.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> c.MIP_starts.write("test_all.mst")
        >>> c.MIP_starts.read("test_all.mst")
        """
        CPX_PROC.readcopymipstarts(self._env._e, self._cplex._lp, filename)

    def write(self, filename, begin=-1, end=-1):
        """Writes a set of MIP starts to a file.

        If called with only a filename, writes all MIP starts to that
        file.

        If called with a filename and one index or name of a MIP
        start, writes only that MIP start to the file.

        If called with a filename and two indices or names of MIP
        starts, writes all MIP starts between the first and second
        index or name, inclusive of begin and end, to the file.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(
        ...     names = [str(i) for i in range(11)], types = "I" * 11)
        >>> indices = c.MIP_starts.add(
        ...     [(cplex.SparsePair(ind = [i], val = [0.0]),
        ...       c.MIP_starts.effort_level.auto) for i in range(5)])
        >>> c.MIP_starts.write("test_all.mst")
        >>> c.MIP_starts.write("test_one.mst", 1)
        >>> c.MIP_starts.write("test_four.mst", 1, 4)
        """
        if begin == -1 and end == -1:
            begin = 0
            end = self.get_num() - 1
        if end == -1:
            end = begin
        CPX_PROC.writemipstarts(self._env._e, self._cplex._lp, filename,
                                begin, end)

    def _add(self, *args):
        """non-public"""
        if len(args) == 1:
            for arg in args[0]:
                self._add(*arg)
        else:
            if len(args) == 2:
                name = ""
            elif len(args) == 3:
                name = args[2]
            else:
                raise WrongNumberOfArgumentsError()
            ind, val = unpack_pair(args[0])
            CPX_PROC.addmipstarts(
                self._env._e, self._cplex._lp, [0],
                self._cplex.variables._conv(ind),
                val, [args[1]], [name])

    def add(self, *args):
        """Adds MIP starts to the problem.

        To add a single MIP start, call this method as

        cpx.MIP_starts.add(start, effort_level, name)

        The first argument, start, must be either a SparsePair
        instance or a list of two lists, the first of which contains
        variable indices or names, the second of which contains the
        values that those variables take.

        The second argument, effort_level, must be an attribute of
        MIP_starts.effort_level.

        The third optional argument is the name of the MIP start.

        To add a set of MIP starts, call this method as

        cpx.MIP_starts.add(sequence)

        where sequence is a list or tuple of pairs (start,
        effort_level) or triples (start, effort_level, name) as
        described above.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(11)],
        ...                           types = "I" * 11)
        >>> indices = c.MIP_starts.add(
        ...     cplex.SparsePair(ind = [0], val = [0.0]),
        ...     c.MIP_starts.effort_level.repair, "first")
        >>> indices = c.MIP_starts.add(
        ...     cplex.SparsePair(ind = [1], val = [0.0]),
        ...     c.MIP_starts.effort_level.solve_MIP)
        >>> indices = c.MIP_starts.add(
        ...     [([[2, 4], [0.0, 1.0]],
        ...       c.MIP_starts.effort_level.auto, "third"),
        ...      ([[3, 4], [1.0, 3.0]],
        ...       c.MIP_starts.effort_level.check_feasibility)])
        >>> c.MIP_starts.get_num()
        4
        >>> c.MIP_starts.get_names()
        ['first', 'm2', 'third', 'm4']
        """
        return self._add_iter(self.get_num, self._add, *args)

    def change(self, *args):
        """Changes a MIP start or set of MIP starts.

        To change a single MIP start, call this method as

        cpx.MIP_starts.change(ID, start, effort_level)

        The first argument, ID, must be an index or name of an
        existing MIP start.

        The second argument, start, must be either a SparsePair
        instance or a list of two lists, the first of which contains
        variable indices or names, the second of which contains the
        values that those variables take.  If the MIP start identified
        by ID already has a value for a variable specified by start,
        that value is replaced.

        The third argument, effort_level, must be an attribute of
        MIP_starts.effort_level.

        To change multiple MIP starts, call this method as

        cpx.MIP_starts.change(sequence)

        where sequence is a list of tuple of triples (ID, start,
        effort_level) as described above.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(
        ...     names = ["x{0}".format(i) for i in range(4)],
        ...     types = "I" * 4
        ... )
        >>> indices = c.MIP_starts.add(
        ...     [(cplex.SparsePair(ind = [i], val = [0.0]),
        ...       c.MIP_starts.effort_level.auto) for i in range(3)])
        >>> for s in c.MIP_starts.get_starts():
        ...     print(s)
        (SparsePair(ind = [0], val = [0.0]), 0)
        (SparsePair(ind = [1], val = [0.0]), 0)
        (SparsePair(ind = [2], val = [0.0]), 0)
        >>> c.MIP_starts.get_names()
        ['m1', 'm2', 'm3']
        >>> check = c.MIP_starts.effort_level.check_feasibility
        >>> repair = c.MIP_starts.effort_level.repair
        >>> c.MIP_starts.change("m1", [["x0", "x1"], [1.0, 2.0]], check)
        >>> c.MIP_starts.get_starts("m1")
        (SparsePair(ind = [0, 1], val = [1.0, 2.0]), 1)
        >>> c.MIP_starts.change(1, [[1, 2], [-1.0, -2.0]], repair)
        >>> c.MIP_starts.get_starts("m2")
        (SparsePair(ind = [1, 2], val = [-1.0, -2.0]), 4)
        >>> c.MIP_starts.change([(1, [[0, 2], [-1.0, 2.0]], check),
        ...                      ("m3", [["x0", 2], [3.0, 2.0]], repair)])
        >>> for s in c.MIP_starts.get_starts(["m2", "m3"]):
        ...     print(s)
        (SparsePair(ind = [0, 1, 2], val = [-1.0, -1.0, 2.0]), 1)
        (SparsePair(ind = [0, 2], val = [3.0, 2.0]), 4)
        """
        if len(args) == 3:
            ind, val = unpack_pair(args[1])
            CPX_PROC.chgmipstarts(
                self._env._e, self._cplex._lp, [self._conv(args[0])], [0],
                self._cplex.variables._conv(ind),
                val, [args[2]])
        elif len(args) == 1:
            for arg in args[0]:
                self.change(arg[0], arg[1], arg[2])
        else:
            raise WrongNumberOfArgumentsError()

    def delete(self, *args):
        """Deletes MIP starts from the problem.

        There are four forms by which MIP_starts.delete may be called.

        MIP_starts.delete()
          deletes all MIP starts from the problem.

        MIP_starts.delete(i)
          i must be a MIP start name or index. Deletes the MIP start
          whose index or name is i.

        MIP_starts.delete(s)
          s must be a sequence of MIP start names or indices.
          Deletes the MIP starts with names or indices contained within
          s. Equivalent to [MIP_starts.delete(i) for i in s].

        MIP_starts.delete(begin, end)
          begin and end must be MIP start indices or MIP start names.
          Deletes the MIP starts with indices between begin and end,
          inclusive of end. Equivalent to
          MIP_starts.delete(range(begin, end + 1)). This will give the
          best performance when deleting batches of MIP starts.

        See :mipapi:`CPXdelmipstarts` in the Callable Library Reference
        Manual for more detail.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=['x', 'y'], types=["II"])
        >>> indices = c.MIP_starts.add(
        ...     [(cplex.SparsePair(ind=['x'], val=[1.0]),
        ...       c.MIP_starts.effort_level.auto, str(i))
        ...      for i in range(10)])
        >>> c.MIP_starts.get_num()
        10
        >>> c.MIP_starts.delete(8)
        >>> c.MIP_starts.get_names()
        ['0', '1', '2', '3', '4', '5', '6', '7', '9']
        >>> c.MIP_starts.delete("1", 3)
        >>> c.MIP_starts.get_names()
        ['0', '4', '5', '6', '7', '9']
        >>> c.MIP_starts.delete([2, "0", 5])
        >>> c.MIP_starts.get_names()
        ['4', '6', '7']
        >>> c.MIP_starts.delete()
        >>> c.MIP_starts.get_names()
        []
        """

        def _delete(begin, end=None):
            CPX_PROC.delmipstarts(self._env._e, self._cplex._lp, begin, end)
        delete_set_by_range(_delete, self._conv, self.get_num(), *args)

    def get_starts(self, *args):
        """Returns a set of MIP starts.

        Returns a SparsePair instance or a list of SparsePair instances.

        Can be called by four forms.

        MIP_starts.get_starts()
          return the starting vector for all MIP starts from the
          problem.

        MIP_starts.get_starts(i)
          i must be a MIP start name or index.  Returns the starting
          vector for the MIP start whose index or name is i.

        MIP_starts.get_starts(s)
          s must be a sequence of MIP start names or indices.
          Returns the starting vector for the MIP starts with indices
          the members of s.  Equivalent to [MIP_starts.get_starts(i)
          for i in s]

        MIP_starts.get_starts(begin, end)
          begin and end must be MIP start indices or MIP start names.
          Returns the starting vector for the MIP starts with indices
          between begin and end, inclusive of end. Equivalent to
          MIP_starts.get_starts(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(
        ...     names=[str(i) for i in range(11)],
        ...     types="B" * 11)
        >>> indices =c.MIP_starts.add(
        ...     [(cplex.SparsePair(ind=[i], val=[1.0 * i]),
        ...       c.MIP_starts.effort_level.auto, str(i))
        ...      for i in range(10)])
        >>> c.MIP_starts.get_num()
        10
        >>> c.MIP_starts.get_starts(7)
        (SparsePair(ind = [7], val = [7.0]), 0)
        >>> for s in c.MIP_starts.get_starts("0", 2):
        ...     print(s)
        (SparsePair(ind = [0], val = [0.0]), 0)
        (SparsePair(ind = [1], val = [1.0]), 0)
        (SparsePair(ind = [2], val = [2.0]), 0)
        >>> for s in c.MIP_starts.get_starts([2, "0", 5]):
        ...     print(s)
        (SparsePair(ind = [2], val = [2.0]), 0)
        (SparsePair(ind = [0], val = [0.0]), 0)
        (SparsePair(ind = [5], val = [5.0]), 0)
        >>> c.MIP_starts.delete(3,9)
        >>> for s in c.MIP_starts.get_starts():
        ...     print(s)
        (SparsePair(ind = [0], val = [0.0]), 0)
        (SparsePair(ind = [1], val = [1.0]), 0)
        (SparsePair(ind = [2], val = [2.0]), 0)
        >>> c.MIP_starts.effort_level[0]
        'auto'
        """
        def getmst(a, b=self.get_num() - 1):
            ret = CPX_PROC.getmipstarts(self._env._e, self._cplex._lp, a, b)
            mat = _HBMatrix()
            mat.matbeg = ret[0]
            mat.matind = ret[1]
            mat.matval = ret[2]
            return [(m, ret[3][i]) for (i, m) in enumerate(mat)]
        return apply_freeform_two_args(getmst, self._conv, args)

    def get_effort_levels(self, *args):
        """Returns the effort levels for a set of MIP starts.

        Can be called by four forms.

        MIP_starts.get_effort_levels()
          return the effort level for all MIP starts from the
          problem.

        MIP_starts.get_effort_levels(i)
          i must be a MIP start name or index.  Returns the effort
          level for the MIP start whose index or name is i.

        MIP_starts.get_effort_levels(s)
          s must be a sequence of MIP start names or indices.
          Returns the effort level for the MIP starts with indices
          the members of s.  Equivalent to
          [MIP_starts.get_effort_levels(i) for i in s]

        MIP_starts.get_effort_levels(begin, end)
          begin and end must be MIP start indices or MIP start names.
          Returns the effort level for the MIP starts with indices
          between begin and end, inclusive of end. Equivalent to
          MIP_starts.get_effort_levels(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(
        ...     names = [str(i) for i in range(10)],
        ...     types = "B" * 10)
        >>> indices = c.MIP_starts.add(
        ...     [(cplex.SparsePair(ind = [i], val = [1.0 * i]),
        ...       c.MIP_starts.effort_level.auto, str(i))
        ...      for i in range(10)])
        >>> c.MIP_starts.change([(1, [[0], [0.0]], c.MIP_starts.effort_level.check_feasibility),\
                                 (2, [[0], [0.0]], c.MIP_starts.effort_level.solve_fixed),\
                                 (3, [[0], [0.0]], c.MIP_starts.effort_level.solve_MIP),\
                                 (4, [[0], [0.0]], c.MIP_starts.effort_level.repair),\
                                 (5, [[0], [0.0]], c.MIP_starts.effort_level.no_check)])
        >>> c.MIP_starts.get_num()
        10
        >>> c.MIP_starts.effort_level[c.MIP_starts.get_effort_levels(3)]
        'solve_MIP'
        >>> [c.MIP_starts.effort_level[i] for i in c.MIP_starts.get_effort_levels("0",2)]
        ['auto', 'check_feasibility', 'solve_fixed']
        >>> [c.MIP_starts.effort_level[i] for i in c.MIP_starts.get_effort_levels([2,"0",5])]
        ['solve_fixed', 'auto', 'no_check']
        >>> c.MIP_starts.get_effort_levels()
        [0, 1, 2, 3, 4, 5, 0, 0, 0, 0]
        """
        def geteffort(a, b=self.get_num() - 1):
            return CPX_PROC.getmipstarts_effort(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(geteffort, self._conv, args)

    def get_num_entries(self, *args):
        """Returns the number of variables specified by a set of MIP starts.

        Can be called by four forms.

        MIP_starts.get_num_entries()
          return the length of the starting vector for all MIP starts
          from the problem.

        MIP_starts.get_num_entries(i)
          i must be a MIP start name or index.  Returns the length of
          the starting vector for the MIP start whose index or name
          is i.

        MIP_starts.get_num_entries(s)
          s must be a sequence of MIP start names or indices.
          Returns the length of the starting vector for the MIP
          starts with indices the members of s.  Equivalent to
          [MIP_starts.get_num_entries(i) for i in s]

        MIP_starts.get_num_entries(begin, end)
          begin and end must be MIP start indices or MIP start names.
          Returns the length of the starting vector for the MIP starts
          with indices between begin and end, inclusive of end.
          Equivalent to
          MIP_starts.get_num_entries(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(
        ...     names = [str(i) for i in range(11)],
        ...     types = "B" * 11)
        >>> indices = c.MIP_starts.add(
        ...     [(cplex.SparsePair(ind = range(i), val = [0.0] * i),
        ...       c.MIP_starts.effort_level.auto, str(i - 1))
        ...      for i in range(1, 11)])
        >>> c.MIP_starts.get_num()
        10
        >>> c.MIP_starts.get_num_entries(3)
        4
        >>> c.MIP_starts.get_num_entries("0",2)
        [1, 2, 3]
        >>> c.MIP_starts.get_num_entries([2,"0",5])
        [3, 1, 6]
        >>> c.MIP_starts.get_num_entries()
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        """
        def getmstsize(a):
            return CPX_PROC.getmipstarts_size(self._env._e, self._cplex._lp, a, a)
        return apply_freeform_one_arg(
            getmstsize, self._conv, self.get_num(), args)

    def get_names(self, *args):
        """Returns the names of a set of MIP starts.

        Can be called by four forms.

        MIP_starts.get_names()
          return the names of all MIP starts from the problem.

        MIP_starts.get_names(i)
          i must be a MIP start index.  Returns the name of MIP start i.

        MIP_starts.get_names(s)
          s must be a sequence of MIP start indices.  Returns the
          names of the MIP starts with indices the members of s.
          Equivalent to [MIP_starts.get_names(i) for i in s]

        MIP_starts.get_names(begin, end)
          begin and end must be MIP start indices. Returns the names of
          the MIP starts with indices between begin and end, inclusive of
          end. Equivalent to MIP_starts.get_names(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(
        ...     names = [str(i) for i in range(11)],
        ...     types = "B" * 11)
        >>> indices = c.MIP_starts.add(
        ...     [(cplex.SparsePair(ind = range(i), val = [0.0] * i),
        ...       c.MIP_starts.effort_level.auto, "mst" + str(i - 1))
        ...      for i in range(1, 11)])
        >>> c.MIP_starts.get_num()
        10
        >>> c.MIP_starts.get_names(8)
        'mst8'
        >>> c.MIP_starts.get_names(1, 3)
        ['mst1', 'mst2', 'mst3']
        >>> c.MIP_starts.get_names([2, 0, 5])
        ['mst2', 'mst0', 'mst5']
        >>> c.MIP_starts.get_names()
        ['mst0', 'mst1', 'mst2', 'mst3', 'mst4', 'mst5', 'mst6', 'mst7', 'mst8', 'mst9']
        """
        def getname(a, b=self.get_num() - 1):
            return CPX_PROC.getmipstartname(self._env._e, self._cplex._lp,
                                            a, b)
        return apply_freeform_two_args(getname, self._conv, args)


class ObjSense(ConstantClass):
    """Constants defining the sense of the objective function.

    See :cpxapi:`CPXgetobjsen` in the Callable Library Reference
    Manual for more detail.
    """
    maximize = _constants.CPX_MAX
    """See CPX_MAX in the C API."""

    minimize = _constants.CPX_MIN
    """See CPX_MIN in the C API."""


class ObjectiveInterface(BaseInterface):
    """Contains methods for querying and modifying the objective function."""

    sense = ObjSense()
    """See `ObjSense()` """

    def set_linear(self, *args):
        """Changes the linear part of the objective function.

        Can be called by two forms:

        objective.set_linear(var, value)
          var must be a variable index or name and value must be a
          float.  Changes the coefficient of the variable identified
          by var to value.

        objective.set_linear(sequence)
          sequence is a sequence of pairs (var, value) as described
          above.  Changes the coefficients for the specified
          variables to the given values.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(4)])
        >>> c.objective.get_linear()
        [0.0, 0.0, 0.0, 0.0]
        >>> c.objective.set_linear(0, 1.0)
        >>> c.objective.get_linear()
        [1.0, 0.0, 0.0, 0.0]
        >>> c.objective.set_linear("3", -1.0)
        >>> c.objective.get_linear()
        [1.0, 0.0, 0.0, -1.0]
        >>> c.objective.set_linear([("2", 2.0), (1, 0.5)])
        >>> c.objective.get_linear()
        [1.0, 0.5, 2.0, -1.0]
        """

        def chgobj(a, b):
            CPX_PROC.chgobj(self._env._e, self._cplex._lp, a, b)
        apply_pairs(chgobj, self._cplex.variables._conv, *args)

    def set_quadratic(self, *args):
        """Sets the quadratic part of the objective function.

        Call this method with a list with length equal to the number
        of variables in the problem.

        If the quadratic objective function is separable, the entries
        of the list must all be of type float or int.

        If the quadratic objective function is not separable, the
        entries of the list must be either SparsePair instances or
        lists of two lists, the first of which contains variable
        indices or names, the second of which contains the values that
        those variables take.

        Note
          Successive calls to set_quadratic will overwrite any previous
          quadratic objective function.  To modify only part of the
          quadratic objective function, use the method
          set_quadratic_coefficients.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=[str(i) for i in range(3)])
        >>> c.objective.set_quadratic(
        ...     [cplex.SparsePair(ind=[0, 1, 2], val=[1.0, -2.0, 0.5]),
        ...      cplex.SparsePair(ind=[0, 1], val=[-2.0, -1.0]),
        ...      cplex.SparsePair(ind=[0, 2], val=[0.5, -3.0])]
        ... )
        >>> for q in c.objective.get_quadratic():
        ...     print(q)
        SparsePair(ind = [0, 1, 2], val = [1.0, -2.0, 0.5])
        SparsePair(ind = [0, 1], val = [-2.0, -1.0])
        SparsePair(ind = [0, 2], val = [0.5, -3.0])
        >>> c.objective.set_quadratic([1.0, 2.0, 3.0])
        >>> for q in c.objective.get_quadratic():
        ...     print(q)
        SparsePair(ind = [0], val = [1.0])
        SparsePair(ind = [1], val = [2.0])
        SparsePair(ind = [2], val = [3.0])
        """
        if len(args) != 1:
            raise WrongNumberOfArgumentsError()
        if isinstance(args[0], _HBMatrix):
            CPX_PROC.copyquad(
                self._env._e, self._cplex._lp, args[0].matbeg,
                self._cplex.variables._conv(args[0].matind),
                args[0].matval)
        elif isinstance(args[0][0], numbers.Number):
            CPX_PROC.copyqpsep(self._env._e, self._cplex._lp, args[0])
        else:
            self.set_quadratic(_HBMatrix(args[0]))

    def set_quadratic_coefficients(self, *args):
        """Sets coefficients of the quadratic component of the objective
        function.

        To set a single coefficient, call this method as

        objective.set_quadratic_coefficients(v1, v2, val)

        where v1 and v2 are names or indices of variables and val is
        the value for the coefficient.

        To set multiple coefficients, call this method as

        objective.set_quadratic_coefficients(sequence)

        where sequence is a list or tuple of triples (v1, v2, val) as
        described above.

        Note
          Since the quadratic objective function must be symmetric, each
          triple in which v1 is different from v2 is used to set both
          the (v1, v2) coefficient and the (v2, v1) coefficient.  If
          (v1, v2) and (v2, v1) are set with a single call, the second
          value is stored.

        Note
          Attempting to set many coefficients with set_quadratic_coefficients
          can be time consuming. Instead, use the method set_quadratic to set
          the quadratic part of the objective efficiently.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=[str(i) for i in range(3)])
        >>> c.objective.set_quadratic_coefficients(0, 1, 1.0)
        >>> for q in c.objective.get_quadratic():
        ...     print(q)
        SparsePair(ind = [1], val = [1.0])
        SparsePair(ind = [0], val = [1.0])
        SparsePair(ind = [], val = [])
        >>> c.objective.set_quadratic_coefficients([(1, 1, 2.0),
        ...                                         (0, 2, 3.0)])
        >>> for q in c.objective.get_quadratic():
        ...     print(q)
        SparsePair(ind = [1, 2], val = [1.0, 3.0])
        SparsePair(ind = [0, 1], val = [1.0, 2.0])
        SparsePair(ind = [0], val = [3.0])
        >>> c.objective.set_quadratic_coefficients([(0, 1, 4.0),
        ...                                         (1, 0, 5.0)])
        >>> for q in c.objective.get_quadratic():
        ...     print(q)
        SparsePair(ind = [1, 2], val = [5.0, 3.0])
        SparsePair(ind = [0, 1], val = [5.0, 2.0])
        SparsePair(ind = [0], val = [3.0])
        """
        if len(args) not in (3, 1):
            raise WrongNumberOfArgumentsError()
        if isinstance(args[0], (str, int)):
            arg_list = [args]
        else:
            arg_list = args[0]
        varcache = {}
        for i, j, val in arg_list:
            CPX_PROC.chgqpcoef(self._env._e, self._cplex._lp,
                               self._cplex.variables._conv(i, varcache),
                               self._cplex.variables._conv(j, varcache),
                               val)

    def set_sense(self, sense):
        """Sets the sense of the objective function.

        The argument to this method must be either
        objective.sense.minimize or objective.sense.maximize.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.objective.sense[c.objective.get_sense()]
        'minimize'
        >>> c.objective.set_sense(c.objective.sense.maximize)
        >>> c.objective.sense[c.objective.get_sense()]
        'maximize'
        >>> c.objective.set_sense(c.objective.sense.minimize)
        >>> c.objective.sense[c.objective.get_sense()]
        'minimize'
        """
        CPX_PROC.chgobjsen(self._env._e, self._cplex._lp, sense)

    def set_name(self, name):
        """Sets the name of the objective function.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.objective.set_name("cost")
        >>> c.objective.get_name()
        'cost'
        """
        CPX_PROC.copyobjname(self._env._e, self._cplex._lp, name)

    def get_linear(self, *args):
        """Returns the linear coefficients of a set of variables.

        Can be called by four forms.

        objective.get_linear()
          return the linear objective coefficients of all variables
          from the problem.

        objective.get_linear(i)
          i must be a variable name or index.  Returns the linear
          objective coefficient of the variable whose index or name
          is i.

        objective.get_linear(s)
          s must be a sequence of variable names or indices.  Returns
          the linear objective coefficient of the variables with
          indices the members of s.  Equivalent to
          [objective.get_linear(i) for i in s]

        objective.get_linear(begin, end)
          begin and end must be variable indices or variable names.
          Returns the linear objective coefficient of the variables with
          indices between begin and end, inclusive of end. Equivalent to
          objective.get_linear(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(obj = [1.5 * i for i in range(10)],\
                            names = [str(i) for i in range(10)])
        >>> c.variables.get_num()
        10
        >>> c.objective.get_linear(8)
        12.0
        >>> c.objective.get_linear("1",3)
        [1.5, 3.0, 4.5]
        >>> c.objective.get_linear([2,"0",5])
        [3.0, 0.0, 7.5]
        >>> c.objective.get_linear()
        [0.0, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5]
        """
        def getobj(a, b=self._cplex.variables.get_num() - 1):
            return CPX_PROC.getobj(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(
            getobj, self._cplex.variables._conv, args)

    def get_quadratic(self, *args):
        """Returns a set of columns of the quadratic component of the
        objective function.

        Returns a SparsePair instance or a list of SparsePair instances.

        Can be called by four forms.

        objective.get_quadratic()
          return the entire quadratic objective function.

        objective.get_quadratic(i)
          i must be a variable name or index.  Returns the column of
          the quadratic objective function associated with the
          variable whose index or name is i.

        objective.get_quadratic(s)
          s must be a sequence of variable names or indices.  Returns
          the columns of the quadratic objective function associated
          with the variables with indices the members of s.
          Equivalent to [objective.get_quadratic(i) for i in s]

        objective.get_quadratic(begin, end)
          begin and end must be variable indices or variable names.
          Returns the columns of the quadratic objective function
          associated with the variables with indices between begin and
          end, inclusive of end. Equivalent to
          objective.get_quadratic(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=[str(i) for i in range(10)])
        >>> c.variables.get_num()
        10
        >>> c.objective.set_quadratic([1.5 * i for i in range(10)])
        >>> c.objective.get_quadratic(8)
        SparsePair(ind = [8], val = [12.0])
        >>> for q in c.objective.get_quadratic("1", 3):
        ...     print(q)
        SparsePair(ind = [1], val = [1.5])
        SparsePair(ind = [2], val = [3.0])
        SparsePair(ind = [3], val = [4.5])
        >>> for q in c.objective.get_quadratic([3, "1", 5]):
        ...     print(q)
        SparsePair(ind = [3], val = [4.5])
        SparsePair(ind = [1], val = [1.5])
        SparsePair(ind = [5], val = [7.5])
        >>> for q in c.objective.get_quadratic():
        ...     print(q)
        SparsePair(ind = [], val = [])
        SparsePair(ind = [1], val = [1.5])
        SparsePair(ind = [2], val = [3.0])
        SparsePair(ind = [3], val = [4.5])
        SparsePair(ind = [4], val = [6.0])
        SparsePair(ind = [5], val = [7.5])
        SparsePair(ind = [6], val = [9.0])
        SparsePair(ind = [7], val = [10.5])
        SparsePair(ind = [8], val = [12.0])
        SparsePair(ind = [9], val = [13.5])
        """
        num = self._cplex.variables.get_num()

        def getquad(begin, end=num - 1):
            mat = _HBMatrix()
            t = CPX_PROC.getquad(self._env._e, self._cplex._lp, begin, end)
            mat.matbeg, mat.matind, mat.matval = t
            return [m for m in mat]
        return apply_freeform_two_args(
            getquad, self._cplex.variables._conv, args)

    def get_quadratic_coefficients(self, *args):
        """Returns individual coefficients from the quadratic objective function.

        To query a single coefficient, call this as

        objective.get_quadratic_coefficients(v1, v2)

        where v1 and v2 are indices or names of variables.

        To query multiple coefficients, call this method as

        objective.get_quadratic_coefficients(sequence)

        where sequence is a list or tuple of pairs (v1, v2) as
        described above.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(3)])
        >>> c.objective.set_quadratic_coefficients(0, 1, 1.0)
        >>> c.objective.get_quadratic_coefficients("1", 0)
        1.0
        >>> c.objective.set_quadratic_coefficients([(1, 1, 2.0), (0, 2, 3.0), (1, 0, 5.0)])
        >>> c.objective.get_quadratic_coefficients([(1, 0), (1, "1"), (2, "0")])
        [5.0, 2.0, 3.0]
        """
        def getqpcoef(v1, v2):
            return CPX_PROC.getqpcoef(self._env._e, self._cplex._lp, v1, v2)
        if len(args) == 2:
            indices = self._cplex.variables._conv(args)
            return getqpcoef(indices[0], indices[1])
        if len(args) == 1:
            return [self.get_quadratic_coefficients(*arg) for arg in args[0]]
        raise WrongNumberOfArgumentsError()

    def get_sense(self):
        """Returns the sense of the objective function.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.objective.sense[c.objective.get_sense()]
        'minimize'
        >>> c.objective.set_sense(c.objective.sense.maximize)
        >>> c.objective.sense[c.objective.get_sense()]
        'maximize'
        >>> c.objective.set_sense(c.objective.sense.minimize)
        >>> c.objective.sense[c.objective.get_sense()]
        'minimize'
        """
        return CPX_PROC.getobjsen(self._env._e, self._cplex._lp)

    def get_name(self):
        """Returns the name of the objective function.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.objective.set_name("cost")
        >>> c.objective.get_name()
        'cost'
        """
        return CPX_PROC.getobjname(self._env._e, self._cplex._lp)

    def get_num_quadratic_variables(self):
        """Returns the number of variables with quadratic coefficients.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(3)])
        >>> c.objective.set_quadratic_coefficients(0, 1, 1.0)
        >>> c.objective.get_num_quadratic_variables()
        2
        >>> c.objective.set_quadratic([1.0, 0.0, 0.0])
        >>> c.objective.get_num_quadratic_variables()
        1
        >>> c.objective.set_quadratic_coefficients([(1, 1, 2.0), (0, 2, 3.0)])
        >>> c.objective.get_num_quadratic_variables()
        3
        """
        return CPX_PROC.getnumquad(self._env._e, self._cplex._lp)

    def get_num_quadratic_nonzeros(self):
        """Returns the number of nonzeros in the quadratic objective function.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = [str(i) for i in range(3)])
        >>> c.objective.set_quadratic_coefficients(0, 1, 1.0)
        >>> c.objective.get_num_quadratic_nonzeros()
        2
        >>> c.objective.set_quadratic_coefficients([(1, 1, 2.0), (0, 2, 3.0)])
        >>> c.objective.get_num_quadratic_nonzeros()
        5
        >>> c.objective.set_quadratic_coefficients([(0, 1, 4.0), (1, 0, 0.0)])
        >>> c.objective.get_num_quadratic_nonzeros()
        3
        """
        return CPX_PROC.getnumqpnz(self._env._e, self._cplex._lp)

    def get_offset(self):
        """Returns the constant offset of the objective function for a problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> offset = c.objective.get_offset()
        >>> abs(offset - 0.0) < 1e-6
        True
        """
        return CPX_PROC.getobjoffset(self._env._e, self._cplex._lp)

    def set_offset(self, offset):
        """Sets the constant offset of the objective function for a problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.objective.set_offset(3.14)
        >>> offset = c.objective.get_offset()
        >>> abs(offset - 3.14) < 1e-6
        True
        """
        return CPX_PROC.chgobjoffset(self._env._e, self._cplex._lp, offset)


class ProgressInterface(BaseInterface):
    """Methods to query the progress of optimization."""

    def __init__(self, parent):
        """Creates a new ProgressInterface.

        The progress interface is exposed by the top-level `Cplex`
        class as Cplex.solution.progress.  This constructor is not
        meant to be used externally.
        """
        super().__init__(cplex=parent._cplex, advanced=True)

    def get_num_iterations(self):
        """Returns the number of iterations executed so far.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.solve()
        >>> num_iter = c.solution.progress.get_num_iterations()
        """
        if self._cplex._is_MIP():
            return CPX_PROC.getmipitcnt(self._env._e, self._cplex._lp)
        siftcnt = CPX_PROC.getsiftitcnt(self._env._e, self._cplex._lp)
        if siftcnt > 0:
            return siftcnt
        baritcnt = CPX_PROC.getbaritcnt(self._env._e, self._cplex._lp)
        if baritcnt > 0:
            return baritcnt
        return CPX_PROC.getitcnt(self._env._e, self._cplex._lp)

    def get_num_barrier_iterations(self):
        """Returns the number of barrier iterations.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("qcp.lp")
        >>> c.solve()
        >>> num_iter = c.solution.progress.get_num_barrier_iterations()
        """
        return CPX_PROC.getbaritcnt(self._env._e, self._cplex._lp)

    def get_num_sifting_iterations(self):
        """Returns the number of sifting iterations.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.parameters.lpmethod.set(c.parameters.lpmethod.values.sifting)
        >>> c.solve()
        >>> num_iter = c.solution.progress.get_num_sifting_iterations()
        """
        return CPX_PROC.getsiftitcnt(self._env._e, self._cplex._lp)

    def get_num_phase_one_iterations(self):
        """Returns the number of iterations to find a feasible solution.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> num_iter = c.solution.progress.get_num_phase_one_iterations()
        """
        return CPX_PROC.getphase1cnt(self._env._e, self._cplex._lp)

    def get_num_sifting_phase_one_iterations(self):
        """Returns the number of sifting iterations to find a feasible solution.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.parameters.lpmethod.set(c.parameters.lpmethod.values.sifting)
        >>> c.solve()
        >>> num_iter = c.solution.progress.get_num_sifting_phase_one_iterations()
        """
        return CPX_PROC.getsiftphase1cnt(self._env._e, self._cplex._lp)

    def get_num_nodes_processed(self):
        """Returns the number of nodes processed.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.parameters.randomseed.set(1)
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> num_nodes = c.solution.progress.get_num_nodes_processed()
        """
        return CPX_PROC.getnodecnt(self._env._e, self._cplex._lp)

    def get_num_nodes_remaining(self):
        """Returns the number of nodes left to process.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> num_nodes = c.solution.progress.get_num_nodes_remaining()
        """
        return CPX_PROC.getnodeleftcnt(self._env._e, self._cplex._lp)

    def get_num_primal_push(self):
        """Returns the number of primal push operations.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.parameters.lpmethod.set(c.parameters.lpmethod.values.barrier)
        >>> c.solve()
        >>> num_push = c.solution.progress.get_num_primal_push()
        """
        return CPX_PROC.getcrossppushcnt(self._env._e, self._cplex._lp)

    def get_num_primal_exchange(self):
        """Returns the number of primal exchange operations.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.parameters.lpmethod.set(c.parameters.lpmethod.values.barrier)
        >>> c.solve()
        >>> num_exch = c.solution.progress.get_num_primal_exchange()
        """
        return CPX_PROC.getcrosspexchcnt(self._env._e, self._cplex._lp)

    def get_num_dual_push(self):
        """Returns the number of dual push operations.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.parameters.lpmethod.set(c.parameters.lpmethod.values.barrier)
        >>> c.solve()
        >>> num_push = c.solution.progress.get_num_dual_push()
        """
        return CPX_PROC.getcrossdpushcnt(self._env._e, self._cplex._lp)

    def get_num_dual_exchange(self):
        """Returns the number of dual exchange operations.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.parameters.lpmethod.set(c.parameters.lpmethod.values.barrier)
        >>> c.solve()
        >>> num_exch = c.solution.progress.get_num_dual_exchange()
        """
        return CPX_PROC.getcrossdexchcnt(self._env._e, self._cplex._lp)

    def get_num_conflict_passes(self):
        """Returns the number of passes performed by the conflict
        refiner.

        See :cpxapi:`CPXgetconflictnumpasses` in the Callable Library
        Reference Manual.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> c.read("infeasible.lp")
        >>> c.conflict.refine()
        >>> c.solution.progress.get_num_conflict_passes()
        5
        """
        return CPX_PROC.getconflictnumpasses(self._env._e, self._cplex._lp)


class InfeasibilityInterface(BaseInterface):
    """Methods for computing degree of infeasibility in a solution vector.

    Each of these methods takes one required argument, x, which must
    be a list of floats with length equal to the number of variables.

    If no other arguments are provided, the methods return the
    violation for all constraints of the given type.

    If one string or integer is provided, it is taken to be the name
    or index of a constraint of the given type.  The methods return
    the violation of that constraint.

    If two strings or integers are provided, they are taken to be the
    names or indices of constraints of the given type.  All violations
    for constraints between the first and second, inclusive, are
    returned in a list.

    If a sequence of strings or integers are provided, they are taken
    to be the names or indices of constraints of the given type.  All
    violations for constraints identified in the sequence are returned
    in a list.
    """

    def __init__(self, parent):
        """Creates a new InfeasibilityInterface.

        The infeasibility interface is exposed by the top-level `Cplex`
        class as Cplex.solution.infeasibility.  This constructor is not
        meant to be used externally.
        """
        super().__init__(cplex=parent._cplex, advanced=True)

    def bound_constraints(self, x, *args):
        """Returns the amount by which variable bounds are violated by x.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> c.solution.infeasibility.bound_constraints(c.solution.get_values(), 2)
        0.0
        >>> c.solution.infeasibility.bound_constraints(c.solution.get_values(), "x10")
        0.0
        >>> c.solution.infeasibility.bound_constraints(c.solution.get_values(), ["x10", 8])
        [0.0, 0.0]
        >>> bd = c.solution.infeasibility.bound_constraints(c.solution.get_values())
        >>> bd[15]
        0.0
        """
        def getinfeas(a, b=self._cplex.variables.get_num() - 1):
            return CPX_PROC.getcolinfeas(self._env._e, self._cplex._lp, x, a, b)
        return apply_freeform_two_args(
            getinfeas, self._cplex.variables._conv, args)

    def linear_constraints(self, x, *args):
        """Returns the amount by which a set of linear constraints are violated by x.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> sol_vals = c.solution.get_values()
        >>> getrowinfeas = c.solution.infeasibility.linear_constraints
        >>> abs(getrowinfeas(sol_vals, "c10"))
        0.0
        >>> abs(getrowinfeas(sol_vals, 7))
        0.0
        >>> [abs(x) for x in getrowinfeas(sol_vals, ["c13", 4])]
        [0.0, 0.0]
        >>> lconstraint = getrowinfeas(sol_vals)
        >>> abs(lconstraint[5])
        0.0

        """
        def getinfeas(a, b=self._cplex.linear_constraints.get_num() - 1):
            return CPX_PROC.getrowinfeas(self._env._e, self._cplex._lp, x, a, b)
        return apply_freeform_two_args(
            getinfeas, self._cplex.linear_constraints._conv, args)

    def quadratic_constraints(self, x, *args):
        """Returns the amount by which a set of quadratic constraints are violated by x.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("miqcp.lp")
        >>> c.solve()
        >>> getqconstrinfeas = c.solution.infeasibility.quadratic_constraints
        >>> abs(getqconstrinfeas(c.solution.get_values(), 2)) < 1e-6
        True
        >>> abs(getqconstrinfeas(c.solution.get_values(), "QC3")) < 1e-6
        True
        >>> [abs(x) < 1e-6 for x in getqconstrinfeas(c.solution.get_values(), [1, "QC1"])]
        [True, True]
        >>> [abs(x) < 1e-6 for x in getqconstrinfeas(c.solution.get_values())]
        [True, True, True, True]

        """
        def getinfeas(a, b=self._cplex.quadratic_constraints.get_num() - 1):
            return CPX_PROC.getqconstrinfeas(self._env._e, self._cplex._lp, x, a, b)
        return apply_freeform_two_args(
            getinfeas, self._cplex.quadratic_constraints._conv, args)

    def indicator_constraints(self, x, *args):
        """Returns the amount by which indicator constraints are violated by x.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> c.solution.infeasibility.indicator_constraints(c.solution.get_values(), 3)
        0.0
        >>> c.solution.infeasibility.indicator_constraints(c.solution.get_values(), "c21")
        0.0
        >>> c.solution.infeasibility.indicator_constraints(c.solution.get_values(), ["c21", 10])
        [0.0, 0.0]
        >>> iconstraint = c.solution.infeasibility.indicator_constraints(c.solution.get_values())
        >>> iconstraint[5]
        0.0
        """
        def getinfeas(a, b=self._cplex.indicator_constraints.get_num() - 1):
            return CPX_PROC.getindconstrinfeas(self._env._e, self._cplex._lp, x, a, b)
        return apply_freeform_two_args(
            getinfeas, self._cplex.indicator_constraints._conv, args)

    def SOS_constraints(self, x, *args):
        """Returns the amount by which SOS constraints are violated by x.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("miqcp.lp")
        >>> c.solve()
        >>> c.solution.infeasibility.SOS_constraints(c.solution.get_values(), 0)
        0.0
        >>> c.solution.infeasibility.SOS_constraints(c.solution.get_values(), "set1")
        0.0
        >>> c.solution.infeasibility.SOS_constraints(c.solution.get_values(), ["set1", 0])
        [0.0, 0.0]
        >>> c.solution.infeasibility.SOS_constraints(c.solution.get_values())
        [0.0]
        """
        def getinfeas(a, b=self._cplex.SOS.get_num() - 1):
            return CPX_PROC.getsosinfeas(self._env._e, self._cplex._lp, x, a, b)
        return apply_freeform_two_args(
            getinfeas, self._cplex.SOS._conv, args)


class CutType(ConstantClass):
    """Identifiers for types of cuts."""
    # NB: If you edit these, look at MIPInfoCallback.cut_type too!
    cover = _constants.CPX_CUT_COVER
    GUB_cover = _constants.CPX_CUT_GUBCOVER
    flow_cover = _constants.CPX_CUT_FLOWCOVER
    clique = _constants.CPX_CUT_CLIQUE
    fractional = _constants.CPX_CUT_FRAC
    MIR = _constants.CPX_CUT_MIR
    flow_path = _constants.CPX_CUT_FLOWPATH
    disjunctive = _constants.CPX_CUT_DISJ
    implied_bound = _constants.CPX_CUT_IMPLBD
    zero_half = _constants.CPX_CUT_ZEROHALF
    multi_commodity_flow = _constants.CPX_CUT_MCF
    _local_cover = _constants.CPX_CUT_LOCALCOVER
    _tighten = _constants.CPX_CUT_TIGHTEN
    _objective_disjunctive = _constants.CPX_CUT_OBJDISJ
    lift_and_project = _constants.CPX_CUT_LANDP
    user = _constants.CPX_CUT_USER
    table = _constants.CPX_CUT_TABLE
    solution_pool = _constants.CPX_CUT_SOLNPOOL
    local_implied_bound = _constants.CPX_CUT_LOCALIMPLBD
    BQP = _constants.CPX_CUT_BQP
    RLT = _constants.CPX_CUT_RLT
    benders = _constants.CPX_CUT_BENDERS
    __num_types = _constants.CPX_CUT_NUM_TYPES


class MIPSolutionInterface(BaseInterface):
    """Methods for accessing solutions to a MIP."""

    cut_type = CutType()
    """See `CutType()` """

    def __init__(self, parent):
        """Creates a new MIPSolutionInterface.

        The MIP solution interface is exposed by the top-level `Cplex`
        class as Cplex.solution.MIP.  This constructor is not meant to
        be used externally.
        """
        super().__init__(cplex=parent._cplex, advanced=True)

    def get_best_objective(self):
        """Returns the currently best known bound of all the remaining
        open nodes in a branch-and-cut tree.

        It is computed for a minimization problem as the minimum
        objective function value of all remaining unexplored nodes.
        Similarly, it is computed for a maximization problem as the
        maximum objective function value of all remaining unexplored
        nodes.

        For a regular MIP optimization, this value is also the best known
        bound on the optimal solution value of the MIP problem.  In fact,
        when a problem has been solved to optimality, this value matches
        the optimal solution value.

        However, for the populate method, the value can also exceed the
        optimal solution value if CPLEX has already solved the model to
        optimality but continues to search for additional solutions.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> best_obj = c.solution.MIP.get_best_objective()
        >>> abs(best_obj - 499.0) < 1e-6
        True
        """
        return CPX_PROC.getbestobjval(self._env._e, self._cplex._lp)

    def get_cutoff(self):
        """Returns the MIP cutoff value.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> cutoff = c.solution.MIP.get_cutoff()
        >>> abs(cutoff - 499.0) < 1e-6
        True
        """
        return CPX_PROC.getcutoff(self._env._e, self._cplex._lp)

    def get_mip_relative_gap(self):
        """Returns the MIP relative gap.

        See :mipapi:`CPXgetmiprelgap` in the Callable Library Reference
        Manual for more detail.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> c.solution.MIP.get_mip_relative_gap()
        0.0
        """
        return CPX_PROC.getmiprelgap(self._env._e, self._cplex._lp)

    def get_incumbent_node(self):
        """Returns the node number of the best solution found.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.parameters.randomseed.set(1)
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.parameters.threads.set(1)
        >>> c.solve()
        >>> c.solution.MIP.get_incumbent_node() >= 0
        True

        """
        return CPX_PROC.getnodeint(self._env._e, self._cplex._lp)

    def get_num_cuts(self, cut_type):
        """Returns the number of cuts of the specified type.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.parameters.randomseed.set(1)
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> ncuts = c.solution.MIP.get_num_cuts(
        ...     c.solution.MIP.cut_type.zero_half)

        """
        return CPX_PROC.getnumcuts(self._env._e, self._cplex._lp, cut_type)

    def get_subproblem_status(self):
        """Returns the solution status of the last subproblem optimization.

        Returns an attribute of Cplex.solution.status if there was an
        error termination where a subproblem could not be solved to
        completion during mixed integer optimization.  Otherwise 0
        (zero) is returned if no error occurred.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> c.solution.MIP.get_subproblem_status()
        0
        """
        return CPX_PROC.getsubstat(self._env._e, self._cplex._lp)


class BasisVarStatus(ConstantClass):
    """Status values returned by basis query methods."""
    at_lower_bound = _constants.CPX_AT_LOWER
    basic = _constants.CPX_BASIC
    at_upper_bound = _constants.CPX_AT_UPPER
    free_nonbasic = _constants.CPX_FREE_SUPER


class BasisInterface(BaseInterface):
    """Methods for accessing the basis of a solution."""

    status = BasisVarStatus()
    """See `BasisVarStatus()` """

    def __init__(self, parent):
        """Creates a new BasisInterface.

        The basis interface is exposed by the top-level `Cplex` class as
        Cplex.solution.basis.  This constructor is not meant to be used
        externally.
        """
        super().__init__(cplex=parent._cplex, advanced=True)

    def get_basis(self):
        """Returns the status of structural and slack variables.

        Returns a pair of lists of attributes of solution.basis.status.
        The first lists the status of the structural variables (of length
        equal to the number of variables), the second lists the status of
        the slack variables (of length equal to the number of linear
        constraints).

        See :cpxapi:`CPXgetbase` in the Callable Library Reference Manual
        for more detail.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> pair_of_lists = c.solution.basis.get_basis()
        """
        return CPX_PROC.getbase(self._env._e, self._cplex._lp)

    def write(self, filename):
        """Writes the basis to a file.

        See :cpxapi:`CPXmbasewrite` in the Callable Library Reference
        Manual and also `InitialInterface.read_basis()`.

        Example:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> c.solution.basis.write("lpex.bas")
        """
        CPX_PROC.mbasewrite(self._env._e, self._cplex._lp, filename)

    def get_header(self):
        """Returns the basis header.

        Returns a pair (head, x), where head is a list of variable
        indices and x is a list of floats indicating the values of
        those variables.  Indices of basic slacks are specified by
        -rowindex - 1.
        """
        return CPX_PROC.getbhead(self._env._e, self._cplex._lp)

    def get_basic_row_index(self, row):
        """Returns the position of a basic slack variable in the basis header.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.solve()
        >>> c.solution.basis.get_basic_row_index(2)
        3
        """
        return CPX_PROC.getijrow(self._env._e, self._cplex._lp, row, True)

    def get_basic_col_index(self, col):
        """Returns the position of a basic structural variable in the basis header.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.solve()
        >>> c.solution.basis.get_basic_col_index(2)
        1
        """
        return CPX_PROC.getijrow(self._env._e, self._cplex._lp, col, False)

    def get_primal_norms(self):
        """Returns norms from the primal steepest edge.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.parameters.preprocessing.presolve.set(c.parameters.preprocessing.presolve.values.off)
        >>> c.parameters.simplex.pgradient.set(c.parameters.simplex.pgradient.values.steep)
        >>> c.parameters.lpmethod.set(c.parameters.lpmethod.values.primal)
        >>> c.solve()
        >>> pnorm = c.solution.basis.get_primal_norms()
        >>> for i, j in zip(pnorm[1], [1.722656, 1.691406, 2.0, 1.062499]):
        ...     abs(i - j) < 1e-6
        ...
        True
        True
        True
        True
        """
        return CPX_PROC.getpnorms(self._env._e, self._cplex._lp)

    def get_dual_norms(self):
        """Returns norms from the dual steepest edge.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.parameters.lpmethod.set(c.parameters.lpmethod.values.dual)
        >>> c.solve()
        >>> c.solution.basis.get_dual_norms()
        ([1.0, 1.0, 1.0, 1.0], [1, 2, 3, -3])
        """
        return CPX_PROC.getdnorms(self._env._e, self._cplex._lp)

    def get_basis_dual_norms(self):
        """Returns basis and dual norms.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.parameters.lpmethod.set(c.parameters.lpmethod.values.dual)
        >>> c.solve()
        >>> c.solution.basis.get_basis_dual_norms()
        ([2, 1, 1, 1], [0, 0, 1, 0], [1.0, 1.0, 1.0, 1.0])
        """
        return CPX_PROC.getbasednorms(self._env._e, self._cplex._lp)

    def get_num_primal_superbasic(self):
        """Returns the number of primal superbasic variables.

        """
        return CPX_PROC.getpsbcnt(self._env._e, self._cplex._lp)

    def get_num_dual_superbasic(self):
        """Returns the number of primal superbasic variables.

        """
        return CPX_PROC.getdsbcnt(self._env._e, self._cplex._lp)


class SensitivityInterface(BaseInterface):
    """Methods for sensitivity analysis."""

    def __init__(self, parent):
        """Creates a new SensitivityInterface.

        The sensitivity interface is exposed by the top-level `Cplex`
        class as Cplex.solution.sensitivity.  This constructor is not
        meant to be used externally.
        """
        super().__init__(cplex=parent._cplex, advanced=True)

    def lower_bounds(self, *args):
        """Returns the sensitivity of a set of lower bounds.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.solve()
        >>> c.solution.sensitivity.lower_bounds(1)
        (-1e+20, 17.5)
        >>> c.solution.sensitivity.lower_bounds('x3')
        (-1e+20, 42.5)
        >>> c.solution.sensitivity.lower_bounds(["x3", 0])
        [(-1e+20, 42.5), (-1e+20, 40.0)]
        >>> c.solution.sensitivity.lower_bounds()
        [(-1e+20, 40.0), (-1e+20, 17.5), (-1e+20, 42.5), (-1e+20, 0.625)]
        """
        def sa(a, b=self._cplex.variables.get_num() - 1):
            return unzip(CPX_PROC.boundsa_lower(self._env._e, self._cplex._lp, a, b))
        return apply_freeform_two_args(
            sa, self._cplex.variables._conv, args)

    def upper_bounds(self, *args):
        """Returns the sensitivity of a set of upper bounds.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.solve()
        >>> c.solution.sensitivity.upper_bounds(1)
        (17.5, 1e+20)
        >>> c.solution.sensitivity.upper_bounds("x3")
        (42.5, 1e+20)
        >>> bupper = c.solution.sensitivity.upper_bounds(["x3", 0])
        >>> for i, j in zip(bupper, [(42.5, 1e+20), (36.428571, 155.0)]):
        ...     abs(i[0] - j[0]) < 1e-6 and abs(i[1]- j[1]) < 1e-6
        ...
        True
        True
        >>> bupper = c.solution.sensitivity.upper_bounds()
        >>> for i, j in zip(bupper[3], (0.625, 1e+20)):
        ...     abs(i - j) < 1e-6
        ...
        True
        True
        """
        def sa(a, b=self._cplex.variables.get_num() - 1):
            return unzip(CPX_PROC.boundsa_upper(self._env._e, self._cplex._lp, a, b))
        return apply_freeform_two_args(
            sa, self._cplex.variables._conv, args)

    def bounds(self, *args):
        """Returns the sensitivity of a set of both lower and upper bounds.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.solve()
        >>> c.solution.sensitivity.bounds(1)
        (-1e+20, 17.5, 17.5, 1e+20)
        >>> c.solution.sensitivity.bounds("x3")
        (-1e+20, 42.5, 42.5, 1e+20)
        >>> c.solution.sensitivity.bounds(["x3", 1])
        [(-1e+20, 42.5, 42.5, 1e+20), (-1e+20, 17.5, 17.5, 1e+20)]
        >>> bd = c.solution.sensitivity.bounds()
        >>> bd[1]
        (-1e+20, 17.5, 17.5, 1e+20)
        """
        def sa(a, b=self._cplex.variables.get_num() - 1):
            return unzip(CPX_PROC.boundsa(self._env._e, self._cplex._lp, a, b))
        return apply_freeform_two_args(
            sa, self._cplex.variables._conv, args)

    def objective(self, *args):
        """Returns the sensitivity of part of the objective function.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.solve()
        >>> c.solution.sensitivity.objective(1)
        (-3.0, 5.0)
        >>> c.solution.sensitivity.objective("x3")
        (-1e+20, -2.0)
        >>> c.solution.sensitivity.objective(["x3", 1])
        [(-1e+20, -2.0), (-3.0, 5.0)]
        >>> c.solution.sensitivity.objective()
        [(-1e+20, 2.5), (-3.0, 5.0), (-1e+20, -2.0), (0.0, 4.0)]
        """
        def sa(a, b=self._cplex.variables.get_num() - 1):
            return unzip(CPX_PROC.objsa(self._env._e, self._cplex._lp, a, b))
        return apply_freeform_two_args(
            sa, self._cplex.variables._conv, args)

    def rhs(self, *args):
        """Returns the sensitivity of the righthand side of a set of linear constraints.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.solve()
        >>> rhssa = c.solution.sensitivity.rhs(1)
        >>> for i, j in zip(rhssa, (20.0, 46.666666)):
        ...     abs(i - j) < 1e-6
        ...
        True
        True
        >>> c.solution.sensitivity.rhs("c3")
        (-1e+20, 112.5)
        >>> rhssa = c.solution.sensitivity.rhs(["c3", 1])
        >>> for i, j in zip(rhssa, [(-1e+20, 112.5), (20.0, 46.666666)]):
        ...     abs(i[0] - j[0]) < 1e-6 and abs(i[1]- j[1]) < 1e-6
        ...
        True
        True
        >>> rhssa = c.solution.sensitivity.rhs()
        >>> for i, j in zip(rhssa[3], (-1e+20, 42.5)):
        ...     abs(i - j) < 1e-6
        ...
        True
        True
        """
        def sa(a, b=self._cplex.linear_constraints.get_num() - 1):
            return unzip(CPX_PROC.rhssa(self._env._e, self._cplex._lp, a, b))
        return apply_freeform_two_args(
            sa, self._cplex.linear_constraints._conv, args)


class FilterType(ConstantClass):
    """Attributes define the filter types."""
    diversity = _constants.CPX_SOLNPOOL_FILTER_DIVERSITY
    range = _constants.CPX_SOLNPOOL_FILTER_RANGE


class SolnPoolFilterInterface(BaseInterface):
    """Methods for solution pool filters."""

    type = FilterType()
    """See `FilterType()` """

    def __init__(self, parent):
        """Creates a new SolnPoolFilterInterface.

        The solution pool filter interface is exposed by the top-level
        `Cplex` class as Cplex.solution.pool.filter.  This constructor
        is not meant to be used externally.
        """
        super().__init__(cplex=parent._cplex, advanced=True,
                         getindexfunc=CPX_PROC.getsolnpoolfilterindex)

    def _add_diversity_filter(self, lb, ub, expression, weights, name):
        """non-public"""
        ind, val = unpack_pair(expression)
        validate_arg_lengths(
            [ind, val, weights],
            extra_msg=": expression, weights"
        )
        CPX_PROC.addsolnpooldivfilter(
            self._env._e, self._cplex._lp, lb, ub,
            self._cplex.variables._conv(ind),
            weights, val, name)

    def add_diversity_filter(self, lb, ub, expression, weights=None,
                             name=''):
        """Adds a diversity filter to the solution pool.

        The arguments determine, in order,

        the lower bound (float)

        the upper bound (float)

        the variables and values it takes as either a SparsePair or a
        list of two lists.

        a set of weights (a list of floats with the same length as
        expression).  If an empty list is given, then weights of 1.0
        (one) will be used.

        name (string)

        Returns the index of the added diversity filter.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> c.solution.pool.filter.add_diversity_filter(
        ...     300, 600, [['x1','x2'], [1,1]], [2,1], "")
        0
        """
        (weights,) = init_list_args(weights)
        return self._add_single(self.get_num, self._add_diversity_filter,
                                lb, ub, expression, weights, name)

    def _add_range_filter(self, lb, ub, expression, name):
        """non-public"""
        ind, val = unpack_pair(expression)
        CPX_PROC.addsolnpoolrngfilter(
            self._env._e, self._cplex._lp, lb, ub,
            self._cplex.variables._conv(ind),
            val, name)

    def add_range_filter(self, lb, ub, expression, name=''):
        """Adds a range filter to the solution pool.

        The arguments determine, in order,

        the lower bound (float)

        the upper bound (float)

        the variables and values it takes as either a SparsePair or a
        list of two lists.

        name (string)

        Returns the index of the added range filter.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> c.solution.pool.filter.add_range_filter(
        ...     300, 600, [['x1','x2'], [1,1]], "")
        0
        """
        return self._add_single(self.get_num, self._add_range_filter,
                                lb, ub, expression, name)

    def get_diversity_filters(self, *args):
        """Returns a set of diversity filters.

        Returns filters as pairs of (SparsePair, weights), where
        weights is a list of floats.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ['x','y'], types = ["BB"])
        >>> f = cplex.SparsePair(ind = ['x'],val = [1.0])
        >>> [c.solution.pool.filter.add_diversity_filter(
        ...      0, 1, f, [1], str(i))
        ...  for i in range(2)]
        [0, 1]
        >>> c.solution.pool.filter.get_diversity_filters(0)
        (SparsePair(ind = [0], val = [1.0]), [1.0])
        >>> c.solution.pool.filter.get_diversity_filters("1")
        (SparsePair(ind = [0], val = [1.0]), [1.0])
        >>> c.solution.pool.filter.get_diversity_filters([0, "1"])
        [(SparsePair(ind = [0], val = [1.0]), [1.0]), (SparsePair(ind = [0], val = [1.0]), [1.0])]
        >>> c.solution.pool.filter.get_diversity_filters()
        [(SparsePair(ind = [0], val = [1.0]), [1.0]), (SparsePair(ind = [0], val = [1.0]), [1.0])]
        """
        def getflt(a):
            ret = CPX_PROC.getsolnpooldivfilter(
                self._env._e, self._cplex._lp, a)
            return (SparsePair(ret[2], ret[4]), ret[3])
        return apply_freeform_one_arg(
            getflt, self._conv, self.get_num(), args)

    def get_range_filters(self, *args):
        """Returns a set of range filters.

        Returns filters as SparsePair instances.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ['x','y'], types = ["II"])
        >>> f = cplex.SparsePair(ind = ['x'],val = [1.0])
        >>> [c.solution.pool.filter.add_range_filter(
        ...      0.0, 1.0, f, str(i)) for i in range(2)]
        [0, 1]
        >>> c.solution.pool.filter.get_range_filters(0)
        SparsePair(ind = [0], val = [1.0])
        >>> c.solution.pool.filter.get_range_filters("1")
        SparsePair(ind = [0], val = [1.0])
        >>> c.solution.pool.filter.get_range_filters([0, "1"])
        [SparsePair(ind = [0], val = [1.0]), SparsePair(ind = [0], val = [1.0])]
        >>> c.solution.pool.filter.get_range_filters()
        [SparsePair(ind = [0], val = [1.0]), SparsePair(ind = [0], val = [1.0])]
        """
        def getflt(a):
            ret = CPX_PROC.getsolnpoolrngfilter(
                self._env._e, self._cplex._lp, a)
            return SparsePair(ret[2], ret[3])
        return apply_freeform_one_arg(
            getflt, self._conv, self.get_num(), args)

    def _getfilter_constant(self, which):
        filter_type = self.get_types(which)
        if filter_type == self.type.diversity:
            func = CPX_PROC.getsolnpooldivfilter_constant
        else:
            assert filter_type == self.type.range
            func = CPX_PROC.getsolnpoolrngfilter_constant
        return func(self._env._e, self._cplex._lp, which)

    def get_bounds(self, *args):
        """Returns (lb, ub) pairs for a set of filters.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=['x', 'y'], types=["BB"])
        >>> f = cplex.SparsePair(ind=['x'], val=[1.0])
        >>> [c.solution.pool.filter.add_diversity_filter(
        ...      0, 1, f, [1], "div{0}".format(i)) for i in range(2)]
        [0, 1]
        >>> [c.solution.pool.filter.add_range_filter(
        ...      0, 1, f, "rng{0}".format(i)) for i in range(2)]
        [2, 3]
        >>> c.solution.pool.filter.get_bounds(0)
        (0.0, 1.0)
        >>> c.solution.pool.filter.get_bounds("rng0")
        (0.0, 1.0)
        >>> c.solution.pool.filter.get_bounds(["div0", 2])
        [(0.0, 1.0), (0.0, 1.0)]
        >>> c.solution.pool.filter.get_bounds()
        [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]
        """
        def getbds(which):
            lb, ub, _ = self._getfilter_constant(which)
            return (lb, ub)
        return apply_freeform_one_arg(
            getbds, self._conv, self.get_num(), args)

    def get_num_nonzeros(self, *args):
        """Returns the number of variables specified by a set of filters.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=['x', 'y'], types=["BB"])
        >>> f = cplex.SparsePair(ind=['x'], val=[1.0])
        >>> [c.solution.pool.filter.add_diversity_filter(
        ...      0, 1, f, [1], "div{0}".format(i)) for i in range(2)]
        [0, 1]
        >>> [c.solution.pool.filter.add_range_filter(
        ...      0, 1, f, "rng{0}".format(i)) for i in range(2)]
        [2, 3]
        >>> c.solution.pool.filter.get_num_nonzeros(0)
        1
        >>> c.solution.pool.filter.get_num_nonzeros("rng0")
        1
        >>> c.solution.pool.filter.get_num_nonzeros(["div0", 2])
        [1, 1]
        >>> c.solution.pool.filter.get_num_nonzeros()
        [1, 1, 1, 1]
        """
        def getnnz(which):
            _, _, nnz = self._getfilter_constant(which)
            return nnz
        return apply_freeform_one_arg(
            getnnz, self._conv, self.get_num(), args)

    def delete(self, *args):
        """Deletes filters from the problem.

        There are four forms by which filters.delete may be called.

        filters.delete()
          deletes all filters from the problem.

        filters.delete(i)
          i must be a filter name or index. Deletes the filter whose
          index or name is i.

        filters.delete(s)
          s must be a sequence of filter names or indices. Deletes
          the filters with names or indices contained within s.
          Equivalent to [filters.delete(i) for i in s].

        filters.delete(begin, end)
          begin and end must be filter indices or filter names. Deletes
          the filters with indices between begin and end, inclusive of
          end. Equivalent to filters.delete(range(begin, end + 1)). This
          will give the best performance when deleting batches of
          filters.

        See :mipapi:`CPXdelsolnpoolfilters` in the Callable Library
        Reference Manual for more detail.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names=['x', 'y'], types=['II'])
        >>> f = cplex.SparsePair(ind=['x'], val=[1.0])
        >>> [c.solution.pool.filter.add_range_filter(
        ...      0.0, 1.0, f, str(i)) for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.solution.pool.filter.get_num()
        10
        >>> c.solution.pool.filter.delete(8)
        >>> c.solution.pool.filter.get_names()
        ['0', '1', '2', '3', '4', '5', '6', '7', '9']
        >>> c.solution.pool.filter.delete('1', 3)
        >>> c.solution.pool.filter.get_names()
        ['0', '4', '5', '6', '7', '9']
        >>> c.solution.pool.filter.delete([2, '0', 5])
        >>> c.solution.pool.filter.get_names()
        ['4', '6', '7']
        >>> c.solution.pool.filter.delete()
        >>> c.solution.pool.filter.get_names()
        []
        """
        def _delete(begin, end=None):
            CPX_PROC.delsolnpoolfilters(self._env._e, self._cplex._lp,
                                        begin, end)
        delete_set_by_range(_delete, self._conv, self.get_num(), *args)

    def get_types(self, *args):
        """Returns the types of a set of filters.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ['x','y'], types = ["II"])
        >>> f = cplex.SparsePair(ind = ['x'],val = [1.0])
        >>> [c.solution.pool.filter.add_range_filter(
        ...      0.0, 1.0, f, str(i)) for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.solution.pool.filter.get_types(3)
        2
        >>> c.solution.pool.filter.get_types("5")
        2
        >>> c.solution.pool.filter.get_types([2, "8"])
        [2, 2]
        >>> c.solution.pool.filter.get_types()
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        """
        def gettype(a):
            return CPX_PROC.getsolnpoolfiltertype(self._env._e, self._cplex._lp, a)
        return apply_freeform_one_arg(
            gettype, self._conv, self.get_num(), args)

    def get_names(self, *args):
        """Returns the names of filters, given their indices.

        There are four forms by which solution.pool.filter.get_names may be called.

        solution.pool.filter.get_names()
          return the names of all solution pool filters from the problem.

        solution.pool.filter.get_names(i)
          i must be a solution filter index.  Returns the name of row i.

        solution.pool.filter.get_names(s)
          s must be a sequence of row indices.  Returns the names of
          the solution pool filters with indices the members of s.
          Equivalent to [solution.pool.filter.get_names(i) for i in s]

        solution.pool.filter.get_names(begin, end)
          begin and end must be solution filter indices. Returns the
          names of the solution pool filter with indices between begin
          and end, inclusive of end. Equivalent to
          solution.pool.filter.get_names(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(names = ['x','y'], types = ["II"])
        >>> f = cplex.SparsePair(ind = ['x'],val = [1.0])
        >>> [c.solution.pool.filter.add_range_filter(
        ...      0.0, 1.0, f, str(i)) for i in range(10)]
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> c.solution.pool.filter.get_names()
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        >>> c.solution.pool.filter.get_names(6)
        '6'
        >>> c.solution.pool.filter.get_names([5, 3])
        ['5', '3']
        >>> c.solution.pool.filter.get_names(3, 5)
        ['3', '4', '5']
        """
        def getname(a):
            return CPX_PROC.getsolnpoolfiltername(
                self._env._e, self._cplex._lp, a)
        return apply_freeform_one_arg(
            getname, self._conv, self.get_num(), args)

    def write(self, filename):
        """Writes the filters to a file.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> c.solution.pool.filter.add_range_filter(
        ...     300, 600, [['x1','x2'], [1,1]], "")
        0
        >>> c.solution.pool.filter.write("ind.flt")
        """
        CPX_PROC.fltwrite(self._env._e, self._cplex._lp, filename)

    def read(self, filename):
        """Reads filters from a file.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> c.solution.pool.filter.add_range_filter(
        ...     300, 600, [['x1','x2'], [1,1]], "")
        0
        >>> c.solution.pool.filter.write("ind.flt")
        >>> c.solution.pool.filter.read("ind.flt")
        """
        CPX_PROC.readcopysolnpoolfilters(self._env._e, self._cplex._lp,
                                         filename)

    def get_num(self):
        """Returns the number of filters in the problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> c.solution.pool.filter.add_range_filter(
        ...     300, 600, [['x1','x2'], [1,1]], "")
        0
        >>> c.solution.pool.filter.get_num()
        1
        """
        return CPX_PROC.getsolnpoolnumfilters(self._env._e, self._cplex._lp)


class QualityMetric(ConstantClass):
    """Measures of solution quality."""
    max_primal_infeasibility = _constants.CPX_MAX_PRIMAL_INFEAS
    max_scaled_primal_infeasibility = _constants.CPX_MAX_SCALED_PRIMAL_INFEAS
    sum_primal_infeasibilities = _constants.CPX_SUM_PRIMAL_INFEAS
    sum_scaled_primal_infeasibilities = _constants.CPX_SUM_SCALED_PRIMAL_INFEAS
    max_dual_infeasibility = _constants.CPX_MAX_DUAL_INFEAS
    max_scaled_dual_infeasibility = _constants.CPX_MAX_SCALED_DUAL_INFEAS
    sum_dual_infeasibilities = _constants.CPX_SUM_DUAL_INFEAS
    sum_scaled_dual_infeasibilities = _constants.CPX_SUM_SCALED_DUAL_INFEAS
    max_int_infeasibility = _constants.CPX_MAX_INT_INFEAS
    sum_integer_infeasibilities = _constants.CPX_SUM_INT_INFEAS
    max_primal_residual = _constants.CPX_MAX_PRIMAL_RESIDUAL
    max_scaled_primal_residual = _constants.CPX_MAX_SCALED_PRIMAL_RESIDUAL
    sum_primal_residual = _constants.CPX_SUM_PRIMAL_RESIDUAL
    sum_scaled_primal_residual = _constants.CPX_SUM_SCALED_PRIMAL_RESIDUAL
    max_dual_residual = _constants.CPX_MAX_DUAL_RESIDUAL
    max_scaled_dual_residual = _constants.CPX_MAX_SCALED_DUAL_RESIDUAL
    sum_dual_residual = _constants.CPX_SUM_DUAL_RESIDUAL
    sum_scaled_dual_residual = _constants.CPX_SUM_SCALED_DUAL_RESIDUAL
    max_comp_slack = _constants.CPX_MAX_COMP_SLACK
    sum_comp_slack = _constants.CPX_SUM_COMP_SLACK
    max_x = _constants.CPX_MAX_X
    max_scaled_x = _constants.CPX_MAX_SCALED_X
    max_pi = _constants.CPX_MAX_PI
    max_scaled_pi = _constants.CPX_MAX_SCALED_PI
    max_slack = _constants.CPX_MAX_SLACK
    max_scaled_slack = _constants.CPX_MAX_SCALED_SLACK
    max_reduced_cost = _constants.CPX_MAX_RED_COST
    max_scaled_reduced_cost = _constants.CPX_MAX_SCALED_RED_COST
    sum_x = _constants.CPX_SUM_X
    sum_scaled_x = _constants.CPX_SUM_SCALED_X
    sum_pi = _constants.CPX_SUM_PI
    sum_scaled_pi = _constants.CPX_SUM_SCALED_PI
    sum_slack = _constants.CPX_SUM_SLACK
    sum_scaled_slack = _constants.CPX_SUM_SCALED_SLACK
    sum_reduced_cost = _constants.CPX_SUM_RED_COST
    sum_scaled_reduced_cost = _constants.CPX_SUM_SCALED_RED_COST
    kappa = _constants.CPX_KAPPA
    objective_gap = _constants.CPX_OBJ_GAP
    dual_objective = _constants.CPX_DUAL_OBJ
    primal_objective = _constants.CPX_PRIMAL_OBJ
    max_quadratic_primal_residual = _constants.CPX_MAX_QCPRIMAL_RESIDUAL
    sum_quadratic_primal_residual = _constants.CPX_SUM_QCPRIMAL_RESIDUAL
    max_quadratic_slack_infeasibility = _constants.CPX_MAX_QCSLACK_INFEAS
    sum_quadratic_slack_infeasibility = _constants.CPX_SUM_QCSLACK_INFEAS
    max_quadratic_slack = _constants.CPX_MAX_QCSLACK
    sum_quadratic_slack = _constants.CPX_SUM_QCSLACK
    max_indicator_slack_infeasibility = _constants.CPX_MAX_INDSLACK_INFEAS
    sum_indicator_slack_infeasibility = _constants.CPX_SUM_INDSLACK_INFEAS
    max_pwl_slack_infeasibility = _constants.CPX_MAX_PWLSLACK_INFEAS
    sum_pwl_slack_infeasibility = _constants.CPX_SUM_PWLSLACK_INFEAS
    exact_kappa = _constants.CPX_EXACT_KAPPA
    kappa_stable = _constants.CPX_KAPPA_STABLE
    kappa_suspicious = _constants.CPX_KAPPA_SUSPICIOUS
    kappa_unstable = _constants.CPX_KAPPA_UNSTABLE
    kappa_illposed = _constants.CPX_KAPPA_ILLPOSED
    kappa_max = _constants.CPX_KAPPA_MAX
    kappa_attention = _constants.CPX_KAPPA_ATTENTION


@contextmanager
def _temp_results_stream(cpx, temp_stream):
    old_results_stream = cpx._env._get_results_stream()
    try:
        yield cpx._env.set_results_stream(temp_stream)
    finally:
        cpx._env.set_results_stream(old_results_stream._file)


class QualityMetrics():
    """A class containing measures of the quality of a solution.

    The __str__ method of this class prints all available measures of
    the quality of the solution in human readable form.

    This class may have a different set of data members depending on
    the optimization algorithm used and the quality metrics that are
    available.

    An instance of this class always has the member quality_type,
    which is one of the following strings:

     * "feasopt"
     * "simplex"
     * "quadratically_constrained"
     * "barrier"
     * "MIP"

    If self.quality_type is "feasopt" this instance has the following
    members:

     * scaled
     * max_x
     * max_bound_infeas
     * max_Ax_minus_b
     * max_slack

    If self.scaled is 1, this instance also has the members:

     * max_scaled_x
     * max_scaled_bound_infeas
     * max_scaled_Ax_minus_b
     * max_scaled_slack

    If self.quality_type is "simplex" this instance has the following
    members:

     * scaled
     * max_x
     * max_pi
     * max_reduced_cost
     * max_bound_infeas
     * max_reduced_cost_infeas
     * max_Ax_minus_b
     * max_c_minus_Bpi
     * max_slack

    If self.scaled is 1, this instance also has the members:

     * max_scaled_x
     * max_scaled_pi
     * max_scaled_reduced_cost
     * max_scaled_bound_infeas
     * max_scaled_reduced_cost_infeas
     * max_scaled_Ax_minus_b
     * max_scaled_c_minus_Bpi
     * max_scaled_slack

    If the condition number of the final basis is available, this
    instance has the member:

     * kappa

    If self.quality_type is "quadratically_constrained" this instance
    has the following members:

     * objective
     * norm_total
     * norm_max
     * error_Ax_b_total
     * error_Ax_b_max
     * error_xQx_dx_f_total
     * error_xQx_dx_f_max
     * x_bound_error_total
     * x_bound_error_max
     * slack_bound_error_total
     * slack_bound_error_max
     * quadratic_slack_bound_error_total
     * quadratic_slack_bound_error_max
     * normalized_error_max

    If self.quality_type is "barrier" this instance has the following
    members:

     * primal_objective
     * dual_objective
     * duality_gap
     * complementarity_total
     * column_complementarity_total
     * column_complementarity_max
     * row_complementarity_total
     * row_complementarity_max
     * primal_norm_total
     * primal_norm_max
     * dual_norm_total
     * dual_norm_max
     * primal_error_total
     * primal_error_max
     * dual_error_total
     * dual_error_max
     * primal_x_bound_error_total
     * primal_x_bound_error_max
     * primal_slack_bound_error_total
     * primal_slack_bound_error_max
     * dual_pi_bound_error_total
     * dual_pi_bound_error_max
     * dual_reduced_cost_bound_error_total
     * dual_reduced_cost_bound_error_max
     * primal_normalized_error
     * dual_normalized_error

    If self.quality_type is "MIP" and this instance was generated for
    a specific member of the solution pool, it has the members:

     * solution_name
     * num_solutions

    If self.quality_type is "MIP", this instance was not generated for
    a specific member of the solution pool, and kappa statistics are
    available, it has the members:

     * max_kappa
     * pct_kappa_stable
     * pct_kappa_suspicious
     * pct_kappa_unstable
     * pct_kappa_illposed
     * kappa_attention

    If self.quality_type is "MIP" and this instance was generated for
    the incumbent solution, it has the members:

     * solver
     * objective
     * x_norm_total
     * x_norm_max
     * error_Ax_b_total
     * error_Ax_b_max
     * x_bound_error_total
     * x_bound_error_max
     * integrality_error_total
     * integrality_error_max
     * slack_bound_error_total
     * slack_bound_error_max

    If in addition the problem this instance was generated for has
    indicator constraints, it has the members:

     * indicator_slack_bound_error_total
     * indicator_slack_bound_error_max

    if in addition the problem this instance was generated for has
    piecewise linear constraints, it has the members:

     * piecewise_linear_error_total
     * piecewise_linear_error_max

    If solver is "MIQCP" this instance also has the members:

     * error_xQx_dx_f_total
     * error_xQx_dx_f_max
     * quadratic_slack_bound_error_total
     * quadratic_slack_bound_error_max

    See also `SolutionInterface.get_quality_metrics` and
    `SolnPoolInterface.get_quality_metrics`.
    """

    def __init__(self, c, soln=-1):
        idata, data = CPX_PROC.getqualitymetrics(c._env._e, c._lp, soln)
        # We get the "to string" from showquality by temporarily
        # hijacking the results stream.
        with closing(StringIO()) as output, \
             _temp_results_stream(c, output):  # noqa: E127
            CPX_PROC.showquality(c._env._e, c._lp, soln)
            self._tostring = output.getvalue()
        if idata[0] == 0:
            self.quality_type = "feasopt"
            self.scaled = idata[1] == 1
            if idata[2] == 1:
                self.max_bound_infeas = data[0]
                if self.scaled:
                    self.max_scaled_bound_infeas = data[1]
            else:
                self.max_bound_infeas = 0.0
                if self.scaled:
                    self.max_scaled_bound_infeas = 0.0
            if idata[3] == 1:
                self.max_Ax_minus_b = data[2]
                if self.scaled:
                    self.max_scaled_Ax_minus_b = data[3]
            else:
                self.max_Ax_minus_b = 0.0
                if self.scaled:
                    self.max_scaled_Ax_minus_b = 0.0
            self.max_x = data[4]
            if self.scaled:
                self.max_scaled_x = data[5]
            if idata[4] == 1:
                self.max_slack = data[6]
                if self.scaled:
                    self.max_scaled_slack = data[7]
            else:
                self.max_slack = 0.0
                if self.scaled:
                    self.max_scaled_slack = 0.0
        elif idata[0] == 1:
            self.quality_type = "simplex"
            self.scaled = idata[1] == 1
            if idata[2] == 1:
                self.max_bound_infeas = data[0]
                if self.scaled:
                    self.max_scaled_bound_infeas = data[1]
            else:
                self.max_bound_infeas = 0.0
                if self.scaled:
                    self.max_scaled_bound_infeas = 0.0
            if idata[3] == 1:
                self.max_reduced_cost_infeas = data[2]
                if self.scaled:
                    self.max_scaled_reduced_cost_infeas = data[3]
            else:
                self.max_reduced_cost_infeas = 0.0
                if self.scaled:
                    self.max_scaled_reduced_cost_infeas = 0.0
            if idata[6] == 1:
                self.max_Ax_minus_b = data[4]
                if self.scaled:
                    self.max_scaled_Ax_minus_b = data[5]
            else:
                self.max_Ax_minus_b = 0.0
                if self.scaled:
                    self.max_scaled_Ax_minus_b = 0.0
            if idata[7] == 1:
                self.max_c_minus_Bpi = data[6]
                if self.scaled:
                    self.max_scaled_c_minus_Bpi = data[7]
            else:
                self.max_c_minus_Bpi = 0.0
                if self.scaled:
                    self.max_scaled_c_minus_Bpi = 0.0
            self.max_x = data[8]
            if self.scaled:
                self.max_scaled_x = data[9]
            if idata[8] == 1:
                self.max_slack = data[10]
                if self.scaled:
                    self.max_scaled_slack = data[11]
            else:
                self.max_slack = 0.0
                if self.scaled:
                    self.max_scaled_slack = 0.0
            self.max_pi = data[12]
            if self.scaled:
                self.max_scaled_pi = data[13]
            self.max_reduced_cost = data[14]
            if self.scaled:
                self.max_scaled_reduced_cost = data[15]
            if idata[9] == 1:
                self.kappa = data[16]
        elif idata[0] == 2:
            self.quality_type = "quadratically_constrained"
            self.objective = data[0]
            self.norm_total = data[1]
            self.norm_max = data[2]
            self.error_Ax_b_total = data[3]
            self.error_Ax_b_max = data[4]
            self.error_xQx_dx_f_total = data[5]
            self.error_xQx_dx_f_max = data[6]
            self.x_bound_error_total = data[7]
            self.x_bound_error_max = data[8]
            self.slack_bound_error_total = data[9]
            self.slack_bound_error_max = data[10]
            self.quadratic_slack_bound_error_total = data[11]
            self.quadratic_slack_bound_error_max = data[12]
            self.normalized_error_max = data[13]
        elif idata[0] == 3:
            self.quality_type = "barrier"
            self.primal_objective = data[0]
            self.dual_objective = data[1]
            self.duality_gap = data[2]
            self.complementarity_total = data[3]
            self.column_complementarity_total = data[4]
            self.column_complementarity_max = data[5]
            self.row_complementarity_total = data[6]
            self.row_complementarity_max = data[7]
            self.primal_norm_total = data[8]
            self.primal_norm_max = data[9]
            self.dual_norm_total = data[10]
            self.dual_norm_max = data[11]
            self.primal_error_total = data[12]
            self.primal_error_max = data[13]
            self.dual_error_total = data[14]
            self.dual_error_max = data[15]
            self.primal_x_bound_error_total = data[16]
            self.primal_x_bound_error_max = data[17]
            self.primal_slack_bound_error_total = data[18]
            self.primal_slack_bound_error_max = data[19]
            self.dual_pi_bound_error_total = data[20]
            self.dual_pi_bound_error_max = data[21]
            self.dual_reduced_cost_bound_error_total = data[22]
            self.dual_reduced_cost_bound_error_max = data[23]
            self.primal_normalized_error = data[24]
            self.dual_normalized_error = data[25]
        elif idata[0] == 4:
            self.quality_type = "MIP"
            if soln >= 0:
                self.solution_name = c.solution.pool.get_names(soln)
                self.num_solutions = c.solution.pool.get_num()
            if idata[4] == 1:
                if idata[2] == 0:
                    self.solver = "MILP"
                elif idata[2] == 1:
                    self.solver = "MIQP"
                elif idata[2] == 2:
                    self.solver = "MIQCP"
                    self.error_xQx_dx_f_total = data[6]
                    self.error_xQx_dx_f_max = data[7]
                    self.quadratic_slack_bound_error_total = data[14]
                    self.quadratic_slack_bound_error_max = data[15]
                self.objective = data[1]
                self.x_norm_total = data[2]
                self.x_norm_max = data[3]
                self.error_Ax_b_total = data[4]
                self.error_Ax_b_max = data[5]
                self.x_bound_error_total = data[8]
                self.x_bound_error_max = data[9]
                self.integrality_error_total = data[10]
                self.integrality_error_max = data[11]
                self.slack_bound_error_total = data[12]
                self.slack_bound_error_max = data[13]
                if idata[3] == 1:
                    self.indicator_slack_bound_error_total = data[16]
                    self.indicator_slack_bound_error_max = data[17]
                if idata[5] == 1:
                    self.piecewise_linear_error_total = data[24]
                    self.piecewise_linear_error_max = data[25]
            if idata[1] == 1:
                self.max_kappa = data[18]
                self.pct_kappa_stable = data[19]
                self.pct_kappa_suspicious = data[20]
                self.pct_kappa_unstable = data[21]
                self.pct_kappa_illposed = data[22]
                self.kappa_attention = data[23]

    def __str__(self):
        """Returns a string containing quality metrics in human readable form."""
        # See __init__ (above) to see how this is constructed.
        return self._tostring


class SolnPoolInterface(BaseInterface):
    """Methods for accessing the solution pool."""

    incumbent = _constants.CPX_INCUMBENT_ID
    """See `_constants.CPX_INCUMBENT_ID` """

    quality_metric = QualityMetric()
    """See `QualityMetric()` """

    def __init__(self, parent):
        """Creates a new SolnPoolInterface.

        The solution pool interface is exposed by the top-level `Cplex`
        class as Cplex.solution.pool.  This constructor is not meant to
        be used externally.
        """
        super().__init__(cplex=parent._cplex, advanced=True,
                         getindexfunc=CPX_PROC.getsolnpoolsolnindex)
        self.filter = SolnPoolFilterInterface(self)
        """See `SolnPoolFilterInterface()` """

    def get_objective_value(self, soln):
        """Returns the objective value for a member of the solution pool.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> obj_val = c.solution.pool.get_objective_value(0)
        >>> abs(obj_val - 499.0) < 1e-6
        True
        """
        if not isinstance(soln, int):
            soln = self.get_indices(soln)
        return CPX_PROC.getsolnpoolobjval(self._env._e, self._cplex._lp, soln)

    def get_values(self, soln, *args):
        """Returns the values of a set of variables for a given solution.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.parameters.randomseed.set(1)
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> v1 = c.solution.pool.get_values(1, 2)
        >>> v2 = c.solution.pool.get_values(1, "x2")
        >>> somevals = c.solution.pool.get_values(1, [2, "x2"])
        >>> v1 == somevals[0], v2 == somevals[1]
        (True, True)
        >>> allvals = c.solution.pool.get_values(1)
        >>> v1 == allvals[2]
        True
        """

        if not isinstance(soln, int):
            soln = self.get_indices(soln)

        def getx(a, b=self._cplex.variables.get_num() - 1):
            return CPX_PROC.getsolnpoolx(self._env._e, self._cplex._lp, soln, a, b)
        return apply_freeform_two_args(
            getx, self._cplex.variables._conv, args)

    def get_linear_slacks(self, soln, *args):
        """Returns a set of linear slacks for a given solution.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> s1 = c.solution.pool.get_linear_slacks(1, 1)
        >>> s2 = c.solution.pool.get_linear_slacks(1, "c2")
        >>> someslacks = c.solution.pool.get_linear_slacks(1, [1, "c2"])
        >>> s1 == someslacks[0], s2 == someslacks[1]
        (True, True)
        >>> allslacks = c.solution.pool.get_linear_slacks(1)
        >>> s1 == allslacks[1]
        True
        """
        if not isinstance(soln, int):
            soln = self.get_indices(soln)

        def getslacks(a, b=self._cplex.linear_constraints.get_num() - 1):
            return CPX_PROC.getsolnpoolslack(self._env._e, self._cplex._lp, soln, a, b)
        return apply_freeform_two_args(
            getslacks, self._cplex.linear_constraints._conv, args)

    def get_quadratic_slacks(self, soln, *args):
        """Returns a set of quadratic slacks for a given solution.

        Can be called by four forms.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.parameters.randomseed.set(1)
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("miqcp.lp")
        >>> c.solve()
        >>> var = c.solution.pool.get_quadratic_slacks(1, 1)
        >>> var = c.solution.pool.get_quadratic_slacks(1, "QC3")
        >>> vars = c.solution.pool.get_quadratic_slacks(1, ["QC3", 1])
        >>> vars = c.solution.pool.get_quadratic_slacks(1)
        """
        if not isinstance(soln, int):
            soln = self.get_indices(soln)

        def getqslacks(a, b=self._cplex.quadratic_constraints.get_num() - 1):
            return CPX_PROC.getsolnpoolqconstrslack(self._env._e, self._cplex._lp, soln, a, b)
        return apply_freeform_two_args(
            getqslacks, self._cplex.quadratic_constraints._conv, args)

    def get_integer_quality(self, soln, which):
        """Returns the integer quality of a given solution.

        The integer quality of a solution can either be a single attribute of
        solution.pool.quality_metrics or a sequence of such
        attributes.

        Note
          This corresponds to the CPLEX callable library function
          CPXgetsolnpoolintquality.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> quality_metric = c.solution.pool.quality_metric
        >>> misi = quality_metric.max_indicator_slack_infeasibility
        >>> c.solution.pool.get_integer_quality(1, misi)
        0
        """
        if not isinstance(soln, int):
            soln = self.get_indices(soln)
        if isinstance(which, int):
            return CPX_PROC.getsolnpoolintquality(
                self._env._e, self._cplex._lp, soln, which)
        return [CPX_PROC.getsolnpoolintquality(self._env._e,
                                               self._cplex._lp, soln, a)
                for a in which]

    def get_float_quality(self, soln, which):
        """Returns the float quality of a given solution.

        The float quality of a solution can either be a single attribute of
        solution.pool.quality_metrics or a sequence of such
        attributes.

        Note
          This corresponds to the CPLEX callable library function
          CPXgetsolnpooldblquality.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> qual = c.solution.pool.get_float_quality(1,\
                                 c.solution.pool.quality_metric.max_indicator_slack_infeasibility)
        >>> abs(qual) < 1.e-6
        True
        """
        if not isinstance(soln, int):
            soln = self.get_indices(soln)
        if isinstance(which, int):
            return CPX_PROC.getsolnpooldblquality(
                self._env._e, self._cplex._lp, soln, which)
        return [CPX_PROC.getsolnpooldblquality(self._env._e,
                                               self._cplex._lp, soln, a)
                for a in which]

    def get_mean_objective_value(self):
        """Returns the average among the objective values in the solution pool.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.parameters.randomseed.set(1)
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> mov = c.solution.pool.get_mean_objective_value()
        """
        return CPX_PROC.getsolnpoolmeanobjval(self._env._e, self._cplex._lp)

    def delete(self, *args):
        """Deletes solutions from the solution pool.

        There are four forms by which pool.delete may be called.

        pool.delete()
          deletes all solutions from the problem.

        pool.delete(i)
          i must be a solution name or index. Deletes the solution
          whose index or name is i.

        pool.delete(s)
          s must be a sequence of solution names or indices. Deletes
          the solutions with names or indices contained within s.
          Equivalent to [pool.delete(i) for i in s].

        pool.delete(begin, end)
          begin and end must be solution indices or solution names.
          Deletes the solutions with indices between begin and end,
          inclusive of end. Equivalent to
          pool.delete(range(begin, end + 1)). This will give the best
          performance when deleting batches of solutions from the
          solution pool.

        See :mipapi:`CPXdelsolnpoolsolns` in the Callable Library
        Reference Manual for more detail.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.parameters.randomseed.set(1)
        >>> c.parameters.mip.limits.populate.set(5)
        >>> c.populate_solution_pool()
        >>> names = c.solution.pool.get_names()
        >>> c.solution.pool.delete(1)
        >>> n = c.solution.pool.get_names()
        >>> del names[1]
        >>> n == names
        True
        >>> c.solution.pool.delete(names[1])
        >>> n = c.solution.pool.get_names()
        >>> names.remove(names[1])
        >>> n == names
        True
        >>> c.solution.pool.delete([names[1], 0])
        >>> n = c.solution.pool.get_names()
        >>> names.remove(names[1])
        >>> del names[0]
        >>> n == names
        True
        >>> c.solution.pool.delete()
        >>> c.solution.pool.get_names()
        []
        """
        def _delete(begin, end=None):
            CPX_PROC.delsolnpoolsolns(self._env._e, self._cplex._lp,
                                      begin, end)
        delete_set_by_range(_delete, self._conv, self.get_num(), *args)

    def get_names(self, *args):
        """Returns the names of a set of solutions.

        There are four forms by which solution.pool.get_names may be called.

        solution.pool.get_names()
          return the names of all solutions from the problem.

        solution.pool.get_names(i)
          i must be a solution index.  Returns the name of row i.

        solution.pool.get_names(s)
          s must be a sequence of row indices.  Returns the names of
          the solutions with indices the members of s.
          Equivalent to [solution.pool.get_names(i) for i in s]

        solution.pool.get_names(begin, end)
          begin and end must be solution indices. Returns the names of
          the solutions with indices between begin and end, inclusive of
          end. Equivalent to
          solution.pool.get_names(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.parameters.randomseed.set(1)
        >>> c.parameters.mip.limits.populate.set(10)
        >>> c.populate_solution_pool()
        >>> names = c.solution.pool.get_names()
        >>> names[1] == c.solution.pool.get_names(1)
        True
        >>> [names[i] for i in [1,2]] == c.solution.pool.get_names([1,2])
        True
        >>> names[1:5] == c.solution.pool.get_names(1, 4)
        True
        """
        def getname(a):
            return CPX_PROC.getsolnpoolsolnname(self._env._e,
                                                self._cplex._lp,
                                                a)
        return apply_freeform_one_arg(
            getname, self._conv, self.get_num(), args)

    def get_num_replaced(self):
        """Returns the number of solution pool members that have been replaced.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> c.solution.pool.get_num_replaced()
        0
        """
        return CPX_PROC.getsolnpoolnumreplaced(self._env._e, self._cplex._lp)

    def get_num(self):
        """Returns the number of solutions in the solution pool.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.parameters.randomseed.set(1)
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> num = c.solution.pool.get_num()
        """
        return CPX_PROC.getsolnpoolnumsolns(self._env._e, self._cplex._lp)

    def write(self, filename, which=None):
        """Writes solutions to a file.

        If no second argument is provided, all solutions are written
        to file.

        If a second argument is provided, it is the index of a
        solution in the solution pool.  Only that solution will be
        written to file.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.parameters.randomseed.set(1)
        >>> c.parameters.mip.limits.populate.set(10)
        >>> c.populate_solution_pool()
        >>> c.solution.pool.write("ind.sol",4)
        """
        if which is None:
            CPX_PROC.solwritesolnpoolall(self._env._e, self._cplex._lp,
                                         filename)
        else:
            CPX_PROC.solwritesolnpool(self._env._e, self._cplex._lp,
                                      which, filename)

    def get_quality_metrics(self, soln):
        """Returns an object containing measures of the quality of the
        specified solution.

        See `QualityMetrics`.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> c.parameters.randomseed.set(1)
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> qm = c.solution.pool.get_quality_metrics(0)
        """
        if not isinstance(soln, int):
            soln = self.get_indices(soln)
        return QualityMetrics(self._cplex, soln)


class AdvancedSolutionInterface(BaseInterface):
    """Advanced methods for accessing solution information.

    Example usage:

    >>> import cplex
    >>> c = cplex.Cplex()
    >>> out = c.set_results_stream(None)
    >>> out = c.set_log_stream(None)
    >>> c.read("lpex.mps")
    >>> c.solve()
    >>> binvcol = c.solution.advanced.binvcol()
    >>> binvrow = c.solution.advanced.binvrow()
    >>> binvacol = c.solution.advanced.binvacol()
    >>> binvarow = c.solution.advanced.binvarow()
    >>> binvcol[0][24], binvcol[1][6]
    (-0.215, 1.0)
    >>> binvrow[24][0], binvrow[6][1]
    (-0.215, 1.0)
    >>> [x for i,x in enumerate(binvacol[0]) if i in range(0,3)], [x for i,x in enumerate(binvacol[1]) if i in range(0,3)]
    ([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    >>> [x for i,x in enumerate(binvarow[0]) if i in range(0,2)], [x for i,x in enumerate(binvarow[1]) if i in range(0,2)], [x for i,x in enumerate(binvarow[2]) if i in range(0,2)]
    ([1.0, 0.0], [0.0, 1.0], [0.0, 0.0])
    >>> btran = c.solution.advanced.btran([1.0] * c.linear_constraints.get_num())
    >>> bbtran = [x if x else 0.0 for i,x in enumerate(btran) if i in range(14,17)]
    >>> [x if x else 0.0 for x in bbtran]
    [0.0, 2.0, 1.0]
    >>> ftran = c.solution.advanced.ftran([1.0] * c.linear_constraints.get_num())
    >>> ftran[0]
    2.891
    """

    def __init__(self, parent):
        """Creates a new AdvancedSolutionInterface.

        The advanced solution interface is exposed by the top-level
        `Cplex` class as Cplex.solution.advanced.  This constructor is
        not meant to be used externally.
        """
        super().__init__(cplex=parent._cplex, advanced=True)

    def binvcol(self, *args):
        """Returns a set of columns of the inverted basis matrix.

        Can be called by four forms.

        solution.advanced.binvcol()
          returns the inverted basis matrix as a list of columns.

        solution.advanced.binvcol(i)
          i must be a linear constraint name or index.  Returns the
          column of the inverted basis matrix associated with i.

        solution.advanced.binvcol(s)
          s must be a sequence of linear constraint names or indices.
          Returns the columns of the inverted basis matrix associated
          with the members of s.  Equivalent to
          [solution.advanced.binvcol(i) for i in s]

        solution.advanced.binvcol(begin, end)
          begin and end must be linear constraint indices or linear
          constraint names. Returns the columns of the inverted basis
          matrix associated with the linear constraints between begin
          and end, inclusive of end. Equivalent to
          solution.advanced.binvcol(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> binvcol = c.solution.advanced.binvcol()
        >>> binvcol[0][24], binvcol[1][6]
        (-0.215, 1.0)
        """
        def inv(a):
            return CPX_PROC.binvcol(self._env._e, self._cplex._lp, a)
        return apply_freeform_one_arg(
            inv, self._cplex.linear_constraints._conv,
            self._cplex.linear_constraints.get_num(), args)

    def binvrow(self, *args):
        """Returns a set of rows of the inverted basis matrix.

        Can be called by four forms.

        solution.advanced.binvrow()
          returns the inverted basis matrix as a list of rows.

        solution.advanced.binvrow(i)
          i must be a linear constraint name or index.  Returns the
          row of the inverted basis matrix associated with i.

        solution.advanced.binvrow(s)
          s must be a sequence of linear constraint names or indices.
          Returns the rows of the inverted basis matrix associated
          with the members of s.  Equivalent to
          [solution.advanced.binvrow(i) for i in s]

        solution.advanced.binvrow(begin, end)
          begin and end must be linear constraint indices or linear
          constraint names. Returns the rows of the inverted basis matrix
          associated with the linear constraints between begin and end,
          inclusive of end. Equivalent to
          solution.advanced.binvrow(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> binvrow = c.solution.advanced.binvrow()
        >>> binvrow[24][0], binvrow[6][1]
        (-0.215, 1.0)
        """
        def inv(a):
            return CPX_PROC.binvrow(self._env._e, self._cplex._lp, a)
        return apply_freeform_one_arg(
            inv, self._cplex.linear_constraints._conv,
            self._cplex.linear_constraints.get_num(), args)

    def binvacol(self, *args):
        """Returns a set of columns of the tableau.

        Can be called by four forms.

        solution.advanced.binvacol()
          returns the tableau as a list of columns.

        solution.advanced.binvacol(i)
          i must be a variable name or index.  Returns the column of
          the tableau associated with i.

        solution.advanced.binvacol(s)
          s must be a sequence of variable names or indices.  Returns
          the columns of the tableau associated with the members of s.
          Equivalent to [solution.advanced.binvacol(i) for i in s]

        solution.advanced.binvacol(begin, end)
          begin and end must be variable indices or variable names.
          Returns the columns of the tableau associated with the
          variables between begin and end, inclusive of end. Equivalent
          to solution.advanced.binvacol(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> binvacol = c.solution.advanced.binvacol()
        >>> [x for i,x in enumerate(binvacol[0]) if i in range(0,3)], [x for i,x in enumerate(binvacol[1]) if i in range(0,3)]
        ([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
        """
        def inv(a):
            return CPX_PROC.binvacol(self._env._e, self._cplex._lp, a)
        return apply_freeform_one_arg(
            inv, self._cplex.variables._conv,
            self._cplex.variables.get_num(), args)

    def binvarow(self, *args):
        """Returns a set of rows of the tableau.

        Can be called by four forms.

        solution.advanced.binvacol()
          returns the tableau as a list of rows.

        solution.advanced.binvacol(i)
          i must be a linear constraint name or index.  Returns the
          row of the tableau associated with i.

        solution.advanced.binvacol(s)
          s must be a sequence of linear constraint names or indices.
          Returns the rows of the tableau associated with the members
          of s.  Equivalent to [solution.advanced.binvacol(i)
          for i in s]

        solution.advanced.binvacol(begin, end)
          begin and end must be linear constraint indices or variable
          names. Returns the rows of the tableau associated with the
          variables between begin and end, inclusive of end. Equivalent
          to solution.advanced.binvacol(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> binvarow = c.solution.advanced.binvarow()
        >>> [x for i,x in enumerate(binvarow[0]) if i in range(0,2)], [x for i,x in enumerate(binvarow[1]) if i in range(0,2)], [x for i,x in enumerate(binvarow[2]) if i in range(0,2)]
        ([1.0, 0.0], [0.0, 1.0], [0.0, 0.0])
        """
        def inv(a):
            return CPX_PROC.binvarow(self._env._e, self._cplex._lp, a)
        return apply_freeform_one_arg(
            inv, self._cplex.linear_constraints._conv,
            self._cplex.linear_constraints.get_num(), args)

    def btran(self, y):
        """Performs a backward linear solve using the basis matrix.

        Returns the solution to the linear system

        x^T B = y^T

        y must be a list of floats with length equal to the number of
        linear constraints.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> btran = c.solution.advanced.btran([1.0] * c.linear_constraints.get_num())
        >>> bbtran = [x if x else 0.0 for i,x in enumerate(btran) if i in range(14,17)]
        >>> [x if x else 0.0 for x in bbtran]
        [0.0, 2.0, 1.0]
        """
        return CPX_PROC.btran(self._env._e, self._cplex._lp, y)

    def ftran(self, x):
        """Performs a linear solve using the basis matrix.

        Returns the solution to the linear system

        B x = y

        y must be a list of floats with length equal to the number of
        linear constraints.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> ftran = c.solution.advanced.ftran([1.0] * c.linear_constraints.get_num())
        >>> ftran[0]
        2.891
        """
        return CPX_PROC.ftran(self._env._e, self._cplex._lp, x)

    def get_gradients(self, *args):
        """Returns information useful in post-solution analysis after an
        LP has been solved and a basis is available.

        See :cpxapi:`CPXgetgrad` in the Callable Library Reference Manual
        for more detail.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> grad = c.solution.advanced.get_gradients(1)
        >>> grad.ind[1]
        1
        >>> grad.val[1]
        1.0
        """
        def getgrad(a):
            return SparsePair(*CPX_PROC.getgrad(self._env._e, self._cplex._lp, a))
        return apply_freeform_one_arg(
            getgrad, self._cplex.variables._conv,
            self._cplex.variables.get_num(), args)

    def get_linear_slacks_from_x(self, x):
        """Computes the slack values from the given solution x

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> slack = c.solution.advanced.get_linear_slacks_from_x(c.solution.get_values())
        >>> abs(slack[3]) < 1e-6
        True
        """
        return CPX_PROC.slackfromx(self._env._e, self._cplex._lp, x)

    def get_quadratic_slacks_from_x(self, x):
        """Computes the slack values for quadratic constraints from the given solution x

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("qcp.lp")
        >>> c.solve()
        >>> qslack = c.solution.advanced.get_quadratic_slacks_from_x(c.solution.get_values())
        >>> abs(qslack[0]) < 1e-6
        True
        """
        return CPX_PROC.qconstrslackfromx(self._env._e, self._cplex._lp, x)

    def get_linear_reduced_costs_from_pi(self, pi):
        """Computes the reduced costs from the given dual solution pi

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> reducedcost = c.solution.advanced.get_linear_reduced_costs_from_pi(\
                                                                    c.solution.get_dual_values())
        >>> abs(reducedcost[0]) < 1e-6
        True
        """
        return CPX_PROC.djfrompi(self._env._e, self._cplex._lp, pi)

    def get_quadratic_reduced_costs_from_pi(self, pi, x):
        """Computes the reduced costs for QP from the given solution (pi, x)

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("qp.lp")
        >>> c.solve()
        >>> qreducedcost = c.solution.advanced.get_quadratic_reduced_costs_from_pi(\
                                                                    c.solution.get_dual_values(),\
                                                                    c.solution.get_values())
        >>> abs(qreducedcost[0]) < 1e-6
        True
        """
        return CPX_PROC.qpdjfrompi(self._env._e, self._cplex._lp, pi, x)

    def get_Driebeek_penalties(self, basic_variables):
        """Returns values known as Driebeek penalties for a sequence of basic variables.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> c_stat, _ = c.solution.basis.get_basis()
        >>> b = [i for i, v in enumerate(c_stat) if v == c.solution.basis.status.basic]
        >>> penalties = c.solution.advanced.get_Driebeek_penalties(b)
        >>> penalties[0]
        (0.34477142857142856, 8.021494102228047)
        """
        return unzip(CPX_PROC.mdleave(
            self._env._e, self._cplex._lp,
            self._cplex.variables._conv(basic_variables)))

    def get_quadratic_indefinite_certificate(self):
        """Compute a vector x that satisfies x'Qx < 0

        Such a vector demonstrates that the matrix Q violates the
        assumption of positive semi-definiteness, and can be an aid in
        debugging a user's program if indefiniteness is an unexpected
        outcome.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("qpindef.lp")
        >>> x = c.solution.advanced.get_quadratic_indefinite_certificate()
        >>> abs(-0.5547001 - x[1]) < 1e-6
        True
        """
        return CPX_PROC.qpindefcertificate(self._env._e, self._cplex._lp)

    def dual_farkas(self):
        """Returns Farkas proof of infeasibility for the active LP model after proven infeasibility.

        See :cpxapi:`CPXdualfarkas` in the Callable Library Reference
        Manual for more detail.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> indices = c.linear_constraints.add(senses="L", rhs=[-1])
        >>> indices = c.variables.add(lb=[1], ub=[2],columns=[[[0],[1]]])
        >>> c.parameters.lpmethod.set(c.parameters.lpmethod.values.dual)
        >>> c.parameters.preprocessing.presolve.set(c.parameters.preprocessing.presolve.values.off)
        >>> c.solve()
        >>> y = c.solution.advanced.dual_farkas()
        >>> y[1]
        2.0
        """
        return CPX_PROC.dualfarkas(self._env._e, self._cplex._lp)

    def get_diverging_index(self):
        """Returns the index of the diverging row or column

        if the problem is not unbounded, get_diverging_index returns -1.

        If the problem is unbounded, get_diverging_index returns the
        index of the diverging variable in the augmented form of the
        constraint matrix.  In other words, if the diverging variable
        is a structural variable, get_diverging_index returns its
        index; if the diverging variable is a slack or ranged
        variable, get_diverging_index returns the sum of the number of
        structural variables and the index of the corresponding
        constraint.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> indices = c.variables.add(obj=[1,1],lb=[1,-cplex.infinity],ub=[2,cplex.infinity])
        >>> c.parameters.lpmethod.set(c.parameters.lpmethod.values.primal)
        >>> c.parameters.preprocessing.presolve.set(c.parameters.preprocessing.presolve.values.off)
        >>> c.solve()
        >>> idx = c.solution.advanced.get_diverging_index()
        >>> idx
        1
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> indices = c.variables.add(obj=[-1,-1],lb=[1,1],ub=[2,2])
        >>> indices = c.linear_constraints.add(lin_expr = [[[0,1],[-1,-1]]], rhs=[-10], senses="L")
        >>> c.parameters.lpmethod.set(c.parameters.lpmethod.values.dual)
        >>> c.parameters.preprocessing.presolve.set(c.parameters.preprocessing.presolve.values.off)
        >>> c.solve()
        >>> idx = c.solution.advanced.get_diverging_index()
        >>> idx
        2
        """
        return CPX_PROC.getijdiv(self._env._e, self._cplex._lp)

    def get_ray(self):
        """Returns an unbounded direction, i.e., ray, if a LP model is unbounded

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("unblp.lp")
        >>> c.parameters.preprocessing.presolve.set(c.parameters.preprocessing.presolve.values.off)
        >>> c.solve()
        >>> ray = c.solution.advanced.get_ray()
        >>> ray[0]
        -1.0
        """
        return CPX_PROC.getray(self._env._e, self._cplex._lp)


class SolutionMethod(ConstantClass):
    """Solution methods."""
    none = _constants.CPX_ALG_NONE
    primal = _constants.CPX_ALG_PRIMAL
    dual = _constants.CPX_ALG_DUAL
    barrier = _constants.CPX_ALG_BARRIER
    feasopt = _constants.CPX_ALG_FEASOPT
    MIP = _constants.CPX_ALG_MIP
    pivot = _constants.CPX_ALG_PIVOT
    pivot_in = _constants.CPX_ALG_PIVOTIN
    pivot_out = _constants.CPX_ALG_PIVOTOUT


class SolutionStatus(ConstantClass):
    """Solution status codes.

    For documentation of each status code, see the reference manual
    of the CPLEX Callable Library, especially the group
    optim.cplex.callable.solutionstatus.
    """
    unknown = 0  # There is no constant for this.
    optimal = _constants.CPX_STAT_OPTIMAL
    unbounded = _constants.CPX_STAT_UNBOUNDED
    infeasible = _constants.CPX_STAT_INFEASIBLE
    feasible = _constants.CPX_STAT_FEASIBLE
    infeasible_or_unbounded = _constants.CPX_STAT_INForUNBD
    optimal_infeasible = _constants.CPX_STAT_OPTIMAL_INFEAS
    num_best = _constants.CPX_STAT_NUM_BEST
    feasible_relaxed_sum = _constants.CPX_STAT_FEASIBLE_RELAXED_SUM
    optimal_relaxed_sum = _constants.CPX_STAT_OPTIMAL_RELAXED_SUM
    feasible_relaxed_inf = _constants.CPX_STAT_FEASIBLE_RELAXED_INF
    optimal_relaxed_inf = _constants.CPX_STAT_OPTIMAL_RELAXED_INF
    feasible_relaxed_quad = _constants.CPX_STAT_FEASIBLE_RELAXED_QUAD
    optimal_relaxed_quad = _constants.CPX_STAT_OPTIMAL_RELAXED_QUAD
    abort_obj_limit = _constants.CPX_STAT_ABORT_OBJ_LIM
    abort_primal_obj_limit = _constants.CPX_STAT_ABORT_PRIM_OBJ_LIM
    abort_dual_obj_limit = _constants.CPX_STAT_ABORT_DUAL_OBJ_LIM
    first_order = _constants.CPX_STAT_FIRSTORDER
    abort_iteration_limit = _constants.CPX_STAT_ABORT_IT_LIM
    abort_time_limit = _constants.CPX_STAT_ABORT_TIME_LIM
    abort_dettime_limit = _constants.CPX_STAT_ABORT_DETTIME_LIM
    abort_user = _constants.CPX_STAT_ABORT_USER
    optimal_face_unbounded = _constants.CPX_STAT_OPTIMAL_FACE_UNBOUNDED
    conflict_feasible = _constants.CPX_STAT_CONFLICT_FEASIBLE
    conflict_minimal = _constants.CPX_STAT_CONFLICT_MINIMAL
    conflict_abort_contradiction = _constants.CPX_STAT_CONFLICT_ABORT_CONTRADICTION
    conflict_abort_time_limit = _constants.CPX_STAT_CONFLICT_ABORT_TIME_LIM
    conflict_abort_dettime_limit = _constants.CPX_STAT_CONFLICT_ABORT_DETTIME_LIM
    conflict_abort_iteration_limit = _constants.CPX_STAT_CONFLICT_ABORT_IT_LIM
    conflict_abort_node_limit = _constants.CPX_STAT_CONFLICT_ABORT_NODE_LIM
    conflict_abort_obj_limit = _constants.CPX_STAT_CONFLICT_ABORT_OBJ_LIM
    conflict_abort_memory_limit = _constants.CPX_STAT_CONFLICT_ABORT_MEM_LIM
    conflict_abort_user = _constants.CPX_STAT_CONFLICT_ABORT_USER
    relaxation_unbounded = _constants.CPXMIP_ABORT_RELAXATION_UNBOUNDED
    abort_relaxed = _constants.CPXMIP_ABORT_RELAXED
    optimal_tolerance = _constants.CPXMIP_OPTIMAL_TOL
    solution_limit = _constants.CPXMIP_SOL_LIM
    populate_solution_limit = _constants.CPXMIP_POPULATESOL_LIM
    node_limit_feasible = _constants.CPXMIP_NODE_LIM_FEAS
    node_limit_infeasible = _constants.CPXMIP_NODE_LIM_INFEAS
    fail_feasible = _constants.CPXMIP_FAIL_FEAS
    fail_infeasible = _constants.CPXMIP_FAIL_INFEAS
    mem_limit_feasible = _constants.CPXMIP_MEM_LIM_FEAS
    mem_limit_infeasible = _constants.CPXMIP_MEM_LIM_INFEAS
    fail_feasible_no_tree = _constants.CPXMIP_FAIL_FEAS_NO_TREE
    fail_infeasible_no_tree = _constants.CPXMIP_FAIL_INFEAS_NO_TREE
    optimal_populated = _constants.CPXMIP_OPTIMAL_POPULATED
    optimal_populated_tolerance = _constants.CPXMIP_OPTIMAL_POPULATED_TOL
    benders_num_best = _constants.CPX_STAT_BENDERS_NUM_BEST

    MIP_optimal = _constants.CPXMIP_OPTIMAL
    MIP_infeasible = _constants.CPXMIP_INFEASIBLE
    MIP_time_limit_feasible = _constants.CPXMIP_TIME_LIM_FEAS
    MIP_time_limit_infeasible = _constants.CPXMIP_TIME_LIM_INFEAS
    MIP_dettime_limit_feasible = _constants.CPXMIP_DETTIME_LIM_FEAS
    MIP_dettime_limit_infeasible = _constants.CPXMIP_DETTIME_LIM_INFEAS
    MIP_abort_feasible = _constants.CPXMIP_ABORT_FEAS
    MIP_abort_infeasible = _constants.CPXMIP_ABORT_INFEAS
    MIP_optimal_infeasible = _constants.CPXMIP_OPTIMAL_INFEAS
    MIP_unbounded = _constants.CPXMIP_UNBOUNDED
    MIP_infeasible_or_unbounded = _constants.CPXMIP_INForUNBD
    MIP_feasible_relaxed_sum = _constants.CPXMIP_FEASIBLE_RELAXED_SUM
    MIP_optimal_relaxed_sum = _constants.CPXMIP_OPTIMAL_RELAXED_SUM
    MIP_feasible_relaxed_inf = _constants.CPXMIP_FEASIBLE_RELAXED_INF
    MIP_optimal_relaxed_inf = _constants.CPXMIP_OPTIMAL_RELAXED_INF
    MIP_feasible_relaxed_quad = _constants.CPXMIP_FEASIBLE_RELAXED_QUAD
    MIP_optimal_relaxed_quad = _constants.CPXMIP_OPTIMAL_RELAXED_QUAD
    MIP_feasible = _constants.CPXMIP_FEASIBLE

    multiobj_optimal = _constants.CPX_STAT_MULTIOBJ_OPTIMAL
    multiobj_infeasible = _constants.CPX_STAT_MULTIOBJ_INFEASIBLE
    multiobj_inforunbd = _constants.CPX_STAT_MULTIOBJ_INForUNBD
    multiobj_non_optimal = _constants.CPX_STAT_MULTIOBJ_NON_OPTIMAL
    multiobj_stopped = _constants.CPX_STAT_MULTIOBJ_STOPPED
    multiobj_unbounded = _constants.CPX_STAT_MULTIOBJ_UNBOUNDED


class SolutionType(ConstantClass):
    """Solution types"""
    none = _constants.CPX_NO_SOLN
    basic = _constants.CPX_BASIC_SOLN
    nonbasic = _constants.CPX_NONBASIC_SOLN
    primal = _constants.CPX_PRIMAL_SOLN


class SolutionInterface(BaseInterface):
    """Methods for querying the solution to an optimization problem."""

    method = SolutionMethod()
    """See `SolutionMethod()` """
    quality_metric = QualityMetric()
    """See `QualityMetric()` """
    status = SolutionStatus()
    """See `SolutionStatus()` """
    type = SolutionType()
    """See `SolutionType()` """

    def __init__(self, cplex):
        """Creates a new SolutionInterface.

        The solution interface is exposed by the top-level `Cplex` class
        as Cplex.solution.  This constructor is not meant to be used
        externally.
        """
        super().__init__(cplex)
        self.progress = ProgressInterface(self)
        """See `ProgressInterface()` """
        self.infeasibility = InfeasibilityInterface(self)
        """See `InfeasibilityInterface()` """
        self.MIP = MIPSolutionInterface(self)
        """See `MIPSolutionInterface()` """
        self.basis = BasisInterface(self)
        """See `BasisInterface()` """
        self.sensitivity = SensitivityInterface(self)
        """See `SensitivityInterface()` """
        self.pool = SolnPoolInterface(self)
        """See `SolnPoolInterface()` """
        self.advanced = AdvancedSolutionInterface(self)
        """See `AdvancedSolutionInterface()` """
        self.multiobj = MultiObjSolnInterface(self)
        """See `MultiObjSolnInterface()` """

    def get_status(self):
        """Returns the status of the solution.

        Returns an attribute of Cplex.solution.status.
        For interpretations of the status codes, see the
        reference manual of the CPLEX Callable Library,
        especially the group optim.cplex.callable.solutionstatus

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.solve()
        >>> c.solution.get_status()
        1
        """
        return CPX_PROC.getstat(self._env._e, self._cplex._lp)

    def get_method(self):
        """Returns the method used to solve the problem.

        Returns an attribute of Cplex.solution.method.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.solve()
        >>> c.solution.get_method()
        2
        """
        return CPX_PROC.getmethod(self._env._e, self._cplex._lp)

    def get_status_string(self, status_code=None):
        """Returns a string describing the status of the solution.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.solve()
        >>> c.solution.get_status_string()
        'optimal'
        """
        if status_code is None:
            status_code = self.get_status()
        return CPX_PROC.getstatstring(self._env._e, status_code)

    def get_objective_value(self):
        """Returns the value of the objective function.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.solve()
        >>> c.solution.get_objective_value()
        -202.5
        """
        return CPX_PROC.getobjval(self._env._e, self._cplex._lp)

    def get_values(self, *args):
        """Returns the values of a set of variables at the solution.

        Can be called by four forms.

        solution.get_values()
          return the values of all variables from the problem.

        solution.get_values(i)
          i must be a variable name or index.  Returns the value of
          the variable whose index or name is i.

        solution.get_values(s)
          s must be a sequence of variable names or indices.  Returns
          the values of the variables with indices the members of s.
          Equivalent to [solution.get_values(i) for i in s]

        solution.get_values(begin, end)
          begin and end must be variable indices or variable names.
          Returns the values of the variables with indices between begin
          and end, inclusive of end. Equivalent to
          solution.get_values(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> c.solution.get_values([0, 4, 5])
        [25.5, 0.0, 80.0]
        """
        def getx(a, b=self._cplex.variables.get_num() - 1):
            return CPX_PROC.getx(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(
            getx, self._cplex.variables._conv, args)

    def get_reduced_costs(self, *args):
        """Returns the reduced costs of a set of variables.

        The values returned by this method are defined to be the dual
        multipliers for bound constraints on the specified variables.

        Can be called by four forms.

        solution.get_reduced_costs()
          return the reduced costs of all variables from the problem.

        solution.get_reduced_costs(i)
          i must be a variable name or index.  Returns the reduced
          cost of the variable whose index or name is i.

        solution.get_reduced_costs(s)
          s must be a sequence of variable names or indices.  Returns
          the reduced costs of the variables with indices the members
          of s.  Equivalent to [solution.get_reduced_costs(i) for i
          in s]

        solution.get_reduced_costs(begin, end)
          begin and end must be variable indices or variable names.
          Returns the reduced costs of the variables with indices between
          begin and end, inclusive of end. Equivalent to
          solution.get_reduced_costs(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> c.solution.get_reduced_costs([0, 4, 5])
        [0.0, 10.0, 0.0]
        """
        def getdj(a, b=self._cplex.variables.get_num() - 1):
            return CPX_PROC.getdj(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(
            getdj, self._cplex.variables._conv, args)

    def get_dual_values(self, *args):
        """Returns a set of dual values.

        Note that the values returned by this function are not only
        meaningful for linear programs. Also for second order cone
        programs, they provide information about the dual solution.
        Refer to the user manual to see how to use the values returned by
        this function for second order cone programs.

        Can be called by four forms.

        solution.get_dual_values()
          return all dual values from the problem.

        solution.get_dual_values(i)
          i must be a linear constraint name or index.  Returns the
          dual value associated with the linear constraint whose
          index or name is i.

        solution.get_dual_values(s)
          s must be a sequence of linear constraint names or indices.
          Returns the dual values associated with the linear
          constraints with indices the members of s.  Equivalent to
          [solution.get_dual_values(i) for i in s]

        solution.get_dual_values(begin, end)
          begin and end must be linear constraint indices or linear
          constraint names. Returns the dual values associated with the
          linear constraints with indices between begin and end,
          inclusive of end. Equivalent to
          solution.get_dual_values(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> pi = c.solution.get_dual_values([0, 1])
        >>> for i, j in zip(pi, [-0.628571, 0.0]):
        ...     abs(i - j) < 1e-6
        ...
        True
        True
        """
        def getpi(a, b=self._cplex.linear_constraints.get_num() - 1):
            return CPX_PROC.getpi(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(
            getpi, self._cplex.linear_constraints._conv, args)

    def get_quadratic_dualslack(self, *args):
        """Returns the dual slack for a quadratic constraint.

        The function returns the dual slack vector of its arguments as a
        SparsePair.
        The function argument may be either the index or the name of a
        quadratic constraint.
        """
        def getqconstrdslack(q):
            res = CPX_PROC.getqconstrdslack(self._env._e, self._cplex._lp, q)
            if res:
                return SparsePair(res[0], res[1])
            return SparsePair()
        return apply_freeform_one_arg(
            getqconstrdslack,
            self._cplex.quadratic_constraints._conv,
            CPX_PROC.getnumqconstrs(self._env._e, self._cplex._lp),
            args)

    def get_linear_slacks(self, *args):
        """Returns a set of linear slacks.

        Can be called by four forms.

        solution.get_linear_slacks()
          return all linear slack values from the problem.

        solution.get_linear_slacks(i)
          i must be a linear constraint name or index.  Returns the
          slack values associated with the linear constraint whose
          index or name is i.

        solution.get_linear_slacks(s)
          s must be a sequence of linear constraint names or indices.
          Returns the slack values associated with the linear
          constraints with indices the members of s.  Equivalent to
          [solution.get_linear_slacks(i) for i in s]

        solution.get_linear_slacks(begin, end)
          begin and end must be linear constraint indices or linear
          constraint names. Returns the slack values associated with the
          linear constraints with indices between begin and end,
          inclusive of end. Equivalent to
          solution.get_linear_slacks(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> abs(c.solution.get_linear_slacks(5)) < 1e-6
        True
        """
        def getslack(a, b=self._cplex.linear_constraints.get_num() - 1):
            return CPX_PROC.getslack(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(
            getslack, self._cplex.linear_constraints._conv, args)

    def get_indicator_slacks(self, *args):
        """Returns a set of indicator slacks.

        Can be called by four forms.

        solution.get_indicator_slacks()
          return all indicator slack values from the problem.

        solution.get_indicator_slacks(i)
          i must be a indicator constraint name or index.  Returns
          the slack values associated with the indicator constraint
          whose index or name is i.

        solution.get_indicator_slacks(s)
          s must be a sequence of indicator constraint names or
          indices.  Returns the slack values associated with the
          indicator constraints with indices the members of s.
          Equivalent to [solution.get_indicator_slacks(i) for i in s]

        solution.get_indicator_slacks(begin, end)
          begin and end must be indicator constraint indices or indicator
          constraint names. Returns the slack values associated with the
          indicator constraints with indices between begin and end,
          inclusive of end. Equivalent to
          solution.get_indicator_slacks(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("ind.lp")
        >>> c.solve()
        >>> c.solution.get_indicator_slacks([0, 18])
        [1e+20, 0.0]
        """
        def getindslack(a, b=self._cplex.indicator_constraints.get_num() - 1):
            return CPX_PROC.getindconstrslack(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(
            getindslack, self._cplex.indicator_constraints._conv,
            args)

    def get_quadratic_slacks(self, *args):
        """Returns a set of quadratic slacks.

        Can be called by four forms.

        solution.get_quadratic_slacks()
          return all quadratic slack values from the problem.

        solution.get_quadratic_slacks(i)
          i must be a quadratic constraint name or index.  Returns
          the slack values associated with the quadratic constraint
          whose index or name is i.

        solution.get_quadratic_slacks(s)
          s must be a sequence of quadratic constraint names or
          indices.  Returns the slack values associated with the
          quadratic constraints with indices the members of s.
          Equivalent to [solution.get_quadratic_slacks(i) for i in s]

        solution.get_quadratic_slacks(begin, end)
          begin and end must be quadratic constraint indices or quadratic
          constraint names. Returns the slack values associated with the
          quadratic constraints with indices between begin and end,
          inclusive of end. Equivalent to
          solution.get_quadratic_slacks(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> c.read("qcp.lp")
        >>> c.solve()
        >>> slack = c.solution.get_quadratic_slacks(0)
        >>> abs(slack) < 1e-6
        True
        """
        def getqslack(a, b=self._cplex.quadratic_constraints.get_num() - 1):
            return CPX_PROC.getqconstrslack(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(
            getqslack, self._cplex.quadratic_constraints._conv, args)

    def get_integer_quality(self, which):
        """Returns a measure of the quality of the solution.

        The measure of the quality of a solution can be a single attribute of
        solution.quality_metrics or a sequence of such
        attributes.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> m = c.solution.quality_metric
        >>> c.solution.get_integer_quality([m.max_x, m.max_dual_infeasibility])
        [18, -1]
        """
        if isinstance(which, int):
            return CPX_PROC.getintquality(self._env._e, self._cplex._lp, which)
        return [CPX_PROC.getintquality(self._env._e, self._cplex._lp, a)
                for a in which]

    def get_float_quality(self, which):
        """Returns a measure of the quality of the solution.

        The measure of the quality of a solution can be a single attribute of
        solution.quality_metrics or a sequence of such attributes.

        Note
          This corresponds to the CPLEX callable library function
          CPXgetdblquality.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> m = c.solution.quality_metric
        >>> c.solution.get_float_quality([m.max_x, m.max_dual_infeasibility])
        [500.0, 0.0]
        """
        if isinstance(which, int):
            return CPX_PROC.getdblquality(self._env._e, self._cplex._lp, which)
        return [CPX_PROC.getdblquality(self._env._e, self._cplex._lp, a)
                for a in which]

    def get_solution_type(self):
        """Returns the type of the solution.

        Returns an attribute of Cplex.solution.type.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> c.solution.get_solution_type()
        1
        """
        return CPX_PROC.solninfo(self._env._e, self._cplex._lp)[1]

    def is_primal_feasible(self):
        """Returns whether or not the solution is known to be primal feasible.

        Note
          Returning False does not necessarily mean that the problem is
          not primal feasible, only that it is not proved to be primal
          feasible.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> c.solution.is_primal_feasible()
        True
        """
        return bool(CPX_PROC.solninfo(self._env._e, self._cplex._lp)[2])

    def is_dual_feasible(self):
        """Returns whether or not the solution is known to be dual feasible.

        Note
          Returning False does not necessarily mean that the problem is
          not dual feasible, only that it is not proved to be dual
          feasible.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> c.solution.is_dual_feasible()
        True
        """
        return bool(CPX_PROC.solninfo(self._env._e, self._cplex._lp)[3])

    def get_activity_levels(self, *args):
        """Returns the activity levels for set of linear constraints.

        Can be called by four forms.

        solution.get_activity_levels()
          return the activity levels for all linear constraints from
          the problem.

        solution.get_activity_levels(i)
          i must be a linear constraint name or index.  Returns the
          activity levels for the linear constraint whose index or
          name is i.

        solution.get_activity_levels(s)
          s must be a sequence of linear constraint names or indices.
          Returns the activity levels for the linear constraints with
          indices the members of s.  Equivalent to
          [solution.get_activity_levels(i) for i in s]

        solution.get_activity_levels(begin, end)
          begin and end must be linear constraint indices or linear
          constraint names. Returns the activity levels for the linear
          constraints with indices between begin and end, inclusive of
          end. Equivalent to
          solution.get_activity_levels(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> c.solution.get_activity_levels([2, 3, 12])
        [80.0, 0.0, 500.0]
        """
        def getax(a, b=self._cplex.linear_constraints.get_num() - 1):
            return CPX_PROC.getax(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(
            getax, self._cplex.linear_constraints._conv, args)

    def get_quadratic_activity_levels(self, *args):
        """Returns the activity levels for set of quadratic constraints.

        Can be called by four forms.

        solution.get_quadratic_activity_levels()
          return the activity levels for all quadratic constraints
          from the problem.

        solution.get_quadratic_activity_levels(i)
          i must be a quadratic constraint name or index.  Returns
          the activity levels for the quadratic constraint whose
          index or name is i.

        solution.get_quadratic_activity_levels(s)
          s must be a sequence of quadratic constraint names or
          indices.  Returns the activity levels for the quadratic
          constraints with indices the members of s.  Equivalent to
          [solution.get_quadratic_activity_levels(i) for i in s]

        solution.get_quadratic_activity_levels(begin, end)
          begin and end must be quadratic constraint indices or quadratic
          constraint names. Returns the activity levels for the quadratic
          constraints with indices between begin and end, inclusive of
          end. Equivalent to
          solution.get_quadratic_activity_levels(range(begin, end + 1)).

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> c.read("qcp.lp")
        >>> c.solve()
        >>> xqxax = c.solution.get_quadratic_activity_levels()
        >>> abs(xqxax[0] - 2.015616) < 1e-6
        True
        """
        def getxqxax(a, b=self._cplex.quadratic_constraints.get_num() - 1):
            return CPX_PROC.getxqxax(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(
            getxqxax, self._cplex.quadratic_constraints._conv, args)

    def get_quality_metrics(self):
        """Returns an object containing measures of the solution quality.

        See `QualityMetrics`.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> qm = c.solution.get_quality_metrics()
        """
        return QualityMetrics(self._cplex)

    def write(self, filename):
        """Writes the incumbent solution to a file.

        See :cpxapi:`CPXsolwrite` in the Callable Library Reference
        Manual and also `InitialInterface.read_start()`.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> c.solve()
        >>> c.solution.write("lpex.sol")
        """
        CPX_PROC.solwrite(self._env._e, self._cplex._lp, filename)


class PresolveStatus(ConstantClass):
    """Presolve status codes"""
    no_reductions = 0
    has_problem = 1
    empty_problem = 2


class PresolveMethod(ConstantClass):
    """Presolve solution methods"""
    none = _constants.CPX_ALG_NONE
    primal = _constants.CPX_ALG_PRIMAL
    dual = _constants.CPX_ALG_DUAL
    barrier = _constants.CPX_ALG_BARRIER


class PresolveColStatus(ConstantClass):
    """Presolve variable status codes"""
    lower_bound = _constants.CPX_PRECOL_LOW
    upper_bound = _constants.CPX_PRECOL_UP
    fixed = _constants.CPX_PRECOL_FIX
    aggregated = _constants.CPX_PRECOL_AGG
    other = _constants.CPX_PRECOL_OTHER


class PresolveRowStatus(ConstantClass):
    """Presolve linear constraint status codes"""
    reduced = _constants.CPX_PREROW_RED
    aggregated = _constants.CPX_PREROW_AGG
    other = _constants.CPX_PREROW_OTHER


class PresolveInterface(BaseInterface):
    """Methods for dealing with the presolved problem."""

    status = PresolveStatus()
    """See `PresolveStatus()` """
    method = PresolveMethod()
    """See `PresolveMethod()` """
    col_status = PresolveColStatus()
    """See `PresolveColStatus()` """
    row_status = PresolveRowStatus()
    """See `PresolveRowStatus()` """

    def crush_formula(self, formula):
        """Crushes a linear formula down into the presolved space.

        formula may either be an instance of the SparsePair class or a
        sequence of length two, the first entry of which contains
        variable names or indices, the second entry of which contains
        the float values associated with those variables.

        Returns a (crushed_formula, offset) pair, where
        crushed_formula is a SparsePair object containing the crushed
        formula in terms of the presolved variables and offset is the
        value of the linear formula corresponding to variables that
        have been removed in the presolved problem.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        >>> c.presolve.crush_formula(cplex.SparsePair(ind = [1, 2], val = [1.0] * 2))
        (SparsePair(ind = [1, 2], val = [1.0, 1.0]), 0.0)
        """
        ind, val = unpack_pair(formula)
        ret = CPX_PROC.crushform(self._env._e, self._cplex._lp, ind, val)
        return (SparsePair(ret[1], ret[2]), ret[0])

    def crush_x(self, x):
        """Projects a primal solution down to the presolved space.

        x must be a list of floats with length equal to the number of
        variables in the original problem.  Returns a list of floats
        with length equal to the number of variables in the presolved
        problem.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        >>> c.presolve.crush_x([1.0] * 4)
        [1.0, 1.0, 1.0]
        """
        return CPX_PROC.crushx(self._env._e, self._cplex._lp, x)

    def crush_pi(self, pi):
        """Projects a dual solution down to the presolved space.

        pi must be a list of floats with length equal to the number of
        linear constraints in the original problem.  Returns a list of
        floats with length equal to the number of linear constraints
        in the presolved problem.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        >>> c.presolve.crush_pi([1.0] * 4)
        [1.0, 1.0, 1.0]
        """
        return CPX_PROC.crushpi(self._env._e, self._cplex._lp, pi)

    def uncrush_formula(self, pre_formula):
        """Uncrushes a linear formula up from the presolved space.

        formula may either be an instance of the SparsePair class or a
        sequence of length two, the first entry of which contains
        variable names or indices, the second entry of which contains
        the float values associated with those variables.

        Returns a (formula, offset) pair, where formula is a
        SparsePair object containing the formula in terms of variables
        in the original problem and offset is the value of the linear
        formula corresponding to variables that have been removed in
        the presolved problem.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        >>> c.presolve.uncrush_formula(cplex.SparsePair(ind = [1, 2], val = [1.0] * 2))
        (SparsePair(ind = [1, 2], val = [1.0, 1.0]), 0.0)
        """
        ind, val = unpack_pair(pre_formula)
        ret = CPX_PROC.uncrushform(self._env._e, self._cplex._lp, ind, val)
        return (SparsePair(ret[1], ret[2]), ret[0])

    def uncrush_x(self, pre_x):
        """Projects a primal presolved solution up to the original space.

        x must be a list of floats with length equal to the number of
        variables in the presolved problem.  Returns a list of floats
        with length equal to the number of variables in the original
        problem.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        >>> c.presolve.uncrush_x([1.0] * 3)
        [1.0, 1.0, 1.0, 0.0]
        """
        return CPX_PROC.uncrushx(self._env._e, self._cplex._lp, pre_x)

    def uncrush_pi(self, pre_pi):
        """Projects a dual presolved solution up to the presolved space.

        pi must be a list of floats with length equal to the number of
        linear constraints in the presolved problem.  Returns a list
        of floats with length equal to the number of linear
        constraints in the original problem.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        >>> c.presolve.uncrush_pi([1.0] * 3)
        [1.0, 1.0, 1.0, 0.0]
        """
        return CPX_PROC.uncrushpi(self._env._e, self._cplex._lp, pre_pi)

    def free(self):
        """Frees the presolved problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        >>> c.presolve.free()
        """
        CPX_PROC.freepresolve(self._env._e, self._cplex._lp)

    def get_status(self):
        """Returns the status of presolve.

        Returns an attribute of Cplex.presolve.status.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        >>> c.presolve.get_status()
        1
        """
        return CPX_PROC.getprestat_status(self._env._e, self._cplex._lp)

    def get_row_status(self):
        """Returns the status of the original linear constraints.

        Returns a list of integers with length equal to the number of
        linear constraints in the original problem.  Each entry of
        this list is an attribute of Cplex.presolve.row_status.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        >>> c.presolve.get_row_status()
        [-3, 1, 2, -3]
        """
        return CPX_PROC.getprestat_r(self._env._e, self._cplex._lp)

    def get_col_status(self):
        """Returns the status of the original variables.

        Returns a list of integers with length equal to the number of
        variables in the original problem.  Each entry of this list
        is an attribute of Cplex.presolve.col_status.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        >>> c.presolve.get_col_status()
        [0, 1, 2, -5]
        """
        return CPX_PROC.getprestat_c(self._env._e, self._cplex._lp)

    def get_presolved_row_status(self):
        """Returns the status of the presolved linear constraints.

        Returns a list of integers with length equal to the number of
        linear constraints in the presolved problem.  -1 indicates
        that the presolved linear constraint corresponds to more than
        one linear constraint in the original problem.  Otherwise the
        value is the index of the corresponding linear constraint in
        the original problem.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        >>> c.presolve.get_presolved_row_status()
        [-1, 1, 2]
        """
        return CPX_PROC.getprestat_or(self._env._e, self._cplex._lp)

    def get_presolved_col_status(self):
        """Returns the status of the presolved variables.

        Returns a list of integers with length equal to the number of
        variables in the presolved problem.  -1 indicates that the
        presolved variable corresponds to a linear combination of more
        than one variable in the original problem.  Otherwise the
        value is the index of the corresponding variable in the
        original problem.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        >>> c.presolve.get_presolved_col_status()
        [0, 1, 2]
        """
        return CPX_PROC.getprestat_oc(self._env._e, self._cplex._lp)

    def add_rows(self, lin_expr=None, senses="", rhs=None, names=None):
        """Adds linear constraints to the presolved problem.

        presolve.add_rows accepts the keyword arguments lin_expr,
        senses, rhs, and names.

        If more than one argument is specified, all arguments must
        have the same length.

        lin_expr may be either a list of SparsePair instances or a
        matrix in list-of-lists format.

        Note
          The entries of lin_expr must not contain duplicate indices.
          If an entry of lin_expr references a variable more than
          once, either by index, name, or a combination of index and
          name, an exception will be raised.

        senses must be either a list of single-character strings or a
        string containing the types of the variables.

        rhs is a list of floats, specifying the righthand side of
        each linear constraint.

        names is a list of strings.

        The specified constraints are added to both the original
        problem and the presolved problem.
        """
        lin_expr, senses, rhs, names = init_list_args(
            lin_expr, senses, rhs, names)
        if not isinstance(senses, str):
            senses = "".join(senses)
        validate_arg_lengths(
            [rhs, senses, names, lin_expr],
            extra_msg=": lin_expr, senses, rhs, names"
        )
        if isinstance(lin_expr, list):
            rmat = _HBMatrix(lin_expr)
        CPX_PROC.preaddrows(self._env._e, self._cplex._lp, rhs, senses,
                            rmat.matbeg, rmat.matind, rmat.matval, names)
        # TODO: We don't return an iterator here because there's no way to
        #       get indices of presolve rows from names.

    def set_objective(self, objective):
        """Sets the linear objective function of the presolved problem.

        objective must be either a SparsePair instance or a list of
        two lists, the first of which contains variable indices or
        names, the second of which contains floats.

        The objective function of both the original problem and the
        presolved problem are changed.

        """
        ind, val = unpack_pair(objective)
        CPX_PROC.prechgobj(self._env._e, self._cplex._lp, ind, val)

    def presolve(self, method):
        """Solves the presolved problem.

        method must be an attribute of Cplex.presolve.method.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("example.mps")
        >>> c.presolve.presolve(c.presolve.method.dual)
        """
        CPX_PROC.presolve(self._env._e, self._cplex._lp, method)

    def write(self, filename):
        """Writes the presolved problem to a file."""
        return CPX_PROC.preslvwrite(self._env._e, self._cplex._lp,
                                    filename)


class FeasoptConstraintType(ConstantClass):
    """Types of constraints"""
    lower_bound = _constants.CPX_CON_LOWER_BOUND
    upper_bound = _constants.CPX_CON_UPPER_BOUND
    linear = _constants.CPX_CON_LINEAR
    quadratic = _constants.CPX_CON_QUADRATIC
    indicator = _constants.CPX_CON_INDICATOR


class FeasoptInterface(BaseInterface):
    """Finds a minimal relaxation of the problem that is feasible.

    This is a callable class. To find a feasible relaxation of a problem,
    invoke the `__call__` method of this class.
    """

    constraint_type = FeasoptConstraintType()
    """See `FeasoptConstraintType()` """

    def all_constraints(self):
        """Returns an object instructing feasopt to relax all constraints.

        Calling Cplex.feasopt(Cplex.feasopt.all_constraints()) will
        result in every constraint being relaxed independently with
        equal weight.

        See also the `__call__` method of this class.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.feasopt.all_constraints()
        """
        gp = self.upper_bound_constraints()._gp
        gp += self.lower_bound_constraints()._gp
        gp += self.linear_constraints()._gp
        gp += self.quadratic_constraints()._gp
        gp += self.indicator_constraints()._gp
        return _group(gp)

    def upper_bound_constraints(self, *args):
        """Returns an object instructing feasopt to relax all upper bounds.

        If called with no arguments, every upper bound is assigned
        weight 1.0.

        If called with one or more arguments, every upper bound is
        assigned a weight equal to the float passed in as the first
        argument.

        If additional arguments are specified, they determine a subset
        of upper bounds to be relaxed.  If one variable index or name
        is specified, it is the only upper bound that can be relaxed.
        If two variable indices or names are specified, then upper
        bounds of all variables between the first and the second,
        inclusive, can be relaxed.  If a sequence of variable names or
        indices is passed in, all of their upper bounds can be
        relaxed.

        See also the `__call__` method of this class.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.feasopt.upper_bound_constraints()
        """
        return self._make_group(self.constraint_type.upper_bound, *args)

    def lower_bound_constraints(self, *args):
        """Returns an object instructing feasopt to relax all lower bounds.

        If called with no arguments, every lower bound is assigned
        weight 1.0.

        If called with one or more arguments, every lower bound is
        assigned a weight equal to the float passed in as the first
        argument.

        If additional arguments are specified, they determine a subset
        of lower bounds to be relaxed.  If one variable index or name
        is specified, it is the only lower bound that can be relaxed.
        If two variable indices or names are specified, then lower
        bounds of all variables between the first and the second,
        inclusive, can be relaxed.  If a sequence of variable names or
        indices is passed in, all of their lower bounds can be
        relaxed.

        See also the `__call__` method of this class.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.feasopt.lower_bound_constraints()
        """
        return self._make_group(self.constraint_type.lower_bound, *args)

    def linear_constraints(self, *args):
        """Returns an object instructing feasopt to relax all linear constraints.

        If called with no arguments, every linear constraint is
        assigned weight 1.0.

        If called with one or more arguments, every linear constraint
        is assigned a weight equal to the float passed in as the first
        argument.

        If additional arguments are specified, they determine a subset
        of linear constraints to be relaxed.  If one linear constraint
        index or name is specified, it is the only linear constraint
        that can be relaxed.  If two linear constraint indices or
        names are specified, then all linear constraints between the
        first and the second, inclusive, can be relaxed.  If a sequence
        of linear constraint names or indices is passed in, all of their
        linear constraints can be relaxed.

        See also the `__call__` method of this class.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.feasopt.linear_constraints()
        """
        return self._make_group(self.constraint_type.linear, *args)

    def quadratic_constraints(self, *args):
        """Returns an object instructing feasopt to relax all quadratic constraints.

        If called with no arguments, every quadratic constraint is
        assigned weight 1.0.

        If called with one or more arguments, every quadratic
        constraint is assigned a weight equal to the float passed in
        as the first argument.

        If additional arguments are specified, they determine a subset
        of quadratic constraints to be relaxed.  If one quadratic
        constraint index or name is specified, it is the only
        quadratic constraint that can be relaxed.  If two quadratic
        constraint indices or names are specified, then all quadratic
        constraints between the first and the second, inclusive, can be
        relaxed.  If a sequence of quadratic constraint names or indices
        is passed in, all of their quadratic constraints can be relaxed.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.feasopt.quadratic_constraints()
        """
        return self._make_group(self.constraint_type.quadratic, *args)

    def indicator_constraints(self, *args):
        """Returns an object instructing feasopt to relax all indicator constraints.

        If called with no arguments, every indicator constraint is
        assigned weight 1.0.

        If called with one or more arguments, every indicator
        constraint is assigned a weight equal to the float passed in
        as the first argument.

        If additional arguments are specified, they determine a subset
        of indicator constraints to be relaxed.  If one indicator
        constraint index or name is specified, it is the only
        indicator constraint that can be relaxed.  If two indicator
        constraint indices or names are specified, then all indicator
        constraints between the first and the second, inclusive, can be
        relaxed.  If a sequence of indicator constraint names or indices
        is passed in, all of their indicator constraints can be relaxed.

        See also the `__call__` method of this class.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.feasopt.indicator_constraints()
        """
        return self._make_group(self.constraint_type.indicator, *args)

    def __call__(self, *args):
        """Finds a minimal relaxation of the problem that is feasible.

        This method can take arbitrarily many arguments. Either the
        object returned by feasopt.all_constraints() or any combination
        of constraint groups and objects returned by
        `upper_bound_constraints()`, `lower_bound_constraints()`,
        `linear_constraints()`, `quadratic_constraints()`, or
        `indicator_constraints()` may be used to specify the constraints
        to consider.

        Constraint groups are sequences of length two, the first entry of
        which is the preference for the group (a float), the second of
        which is a sequence of pairs (type, id), where type is an
        attribute of self.constraint_type and id is either an index or a
        valid name for the type.

        See :cpxapi:`CPXfeasoptext` in the Callable Library Reference
        Manual.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("infeasible.lp")
        >>> c.feasopt(c.feasopt.all_constraints())
        >>> c.solution.get_objective_value()
        2.0
        >>> c.solution.get_values()
        [3.0, 2.0, 3.0, 2.0]
        """
        if not args:
            raise WrongNumberOfArgumentsError(
                "Requires at least one argument")
        gpref, gbeg, ind, indt = [], [], [], []
        args = list(args)  # so we can call extend() below
        for group in args:
            if isinstance(group, _group):
                args.extend(group._gp)
                continue
            gpref.append(group[0])
            gbeg.append(len(ind))
            for con in group[1]:
                tran = self._getconvfunc(con[0])
                indt.append(con[0])
                ind.append(tran(con[1]))
        self._cplex._setup_callbacks()
        CPX_PROC.feasoptext(self._env._e, self._cplex._lp,
                            gpref, gbeg, ind, indt)

    def _make_group(self, which, *args):
        conv = self._getconvfunc(which)
        max_num = self._getnum(which)
        return make_group(conv, max_num, which, *args)

    def _getinterface(self, which):
        contype = self.constraint_type
        switcher = {
            contype.lower_bound: self._cplex.variables,
            contype.upper_bound: self._cplex.variables,
            contype.linear: self._cplex.linear_constraints,
            contype.quadratic: self._cplex.quadratic_constraints,
            contype.indicator: self._cplex.indicator_constraints
        }
        return switcher[which]

    def _getnum(self, which):
        interface = self._getinterface(which)
        return interface.get_num()

    def _getconvfunc(self, which):
        interface = self._getinterface(which)
        return interface._conv


class ConflictStatus(ConstantClass):
    """Status codes returned by conflict.get"""
    excluded = _constants.CPX_CONFLICT_EXCLUDED
    possible_member = _constants.CPX_CONFLICT_POSSIBLE_MEMBER
    member = _constants.CPX_CONFLICT_MEMBER


class ConflictConstraintType(ConstantClass):
    """Types of constraints"""
    lower_bound = _constants.CPX_CON_LOWER_BOUND
    upper_bound = _constants.CPX_CON_UPPER_BOUND
    linear = _constants.CPX_CON_LINEAR
    quadratic = _constants.CPX_CON_QUADRATIC
    indicator = _constants.CPX_CON_INDICATOR
    SOS = _constants.CPX_CON_SOS
    pwl = _constants.CPX_CON_PWL


class ConflictInterface(BaseInterface):
    """Methods for identifying conflicts among constraints."""

    group_status = ConflictStatus()
    """See `ConflictStatus()` """
    constraint_type = ConflictConstraintType()
    """See `ConflictConstraintType()` """

    def __init__(self, cplex):
        """Creates a new ConflictInterface.

        The conflict interface is exposed by the top-level `Cplex` class
        as Cplex.conflict.  This constructor is not meant to be used
        externally.
        """
        super().__init__(cplex)

    def all_constraints(self):
        """Returns an object instructing the conflict refiner to include
        all constraints.

        Calling
        Cplex.conflict.refine(Cplex.conflict.all_constraints()) or
        Cplex.conflict.refine_MIP_start(Cplex.conflict.all_constraints())
        will result in every constraint being included in the search
        for conflicts with equal preference.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.conflict.all_constraints()
        """
        gp = self.upper_bound_constraints()._gp
        gp += self.lower_bound_constraints()._gp
        gp += self.linear_constraints()._gp
        gp += self.quadratic_constraints()._gp
        gp += self.SOS_constraints()._gp
        gp += self.indicator_constraints()._gp
        gp += self.pwl_constraints()._gp
        return _group(gp)

    def upper_bound_constraints(self, *args):
        """Returns an object instructing the conflict refiner to include
        all upper bounds.

        If called with no arguments, every upper bound is assigned
        weight 1.0.

        If called with one or more arguments, every upper bound is
        assigned a weight equal to the float passed in as the first
        argument.

        If additional arguments are specified, they determine a subset
        of upper bounds to be included.  If one variable index or name
        is specified, it is the only upper bound that will be
        included.  If two variable indices or names are specified, then
        upper bounds of all variables between the first and the
        second, inclusive, will be included.  If a sequence of
        variable names or indices is passed in, all of their upper
        bounds will be included.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.conflict.upper_bound_constraints()
        """
        return self._make_group(self.constraint_type.upper_bound, *args)

    def lower_bound_constraints(self, *args):
        """Returns an object instructing the conflict refiner to include
        all lower bounds.

        If called with no arguments, every lower bound is assigned
        weight 1.0.

        If called with one or more arguments, every lower bound is
        assigned a weight equal to the float passed in as the first
        argument.

        If additional arguments are specified, they determine a subset
        of lower bounds to be included.  If one variable index or name
        is specified, it is the only lower bound that will be
        included.  If two variable indices or names are specified, then
        lower bounds of all variables between the first and the
        second, inclusive, will be included.  If a sequence of
        variable names or indices is passed in, all of their lower
        bounds will be included.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.conflict.lower_bound_constraints()
        """
        return self._make_group(self.constraint_type.lower_bound, *args)

    def linear_constraints(self, *args):
        """Returns an object instructing the conflict refiner to include
        all linear constraints.

        If called with no arguments, every linear constraint is
        assigned weight 1.0.

        If called with one or more arguments, every linear constraint
        is assigned a weight equal to the float passed in as the first
        argument.

        If additional arguments are specified, they determine a subset
        of linear constraints to be included.  If one linear
        constraint index or name is specified, it is the only linear
        constraint that will be included.  If two linear constraint
        indices or names are specified, then all linear constraints
        between the first and the second, inclusive, will be included.
        If a sequence of linear constraint names or indices is passed
        in, they will all be included.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.conflict.linear_constraints()
        """
        return self._make_group(self.constraint_type.linear, *args)

    def quadratic_constraints(self, *args):
        """Returns an object instructing the conflict refiner to include
        all quadratic constraints.

        If called with no arguments, every quadratic constraint is
        assigned weight 1.0.

        If called with one or more arguments, every quadratic
        constraint is assigned a weight equal to the float passed in
        as the first argument.

        If additional arguments are specified, they determine a subset
        of quadratic constraints to be included.  If one quadratic
        constraint index or name is specified, it is the only
        quadratic constraint that will be included.  If two quadratic
        constraint indices or names are specified, then all quadratic
        constraints between the first and the second, inclusive, will
        be included.  If a sequence of quadratic constraint names or
        indices is passed in, they will all be included.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.conflict.quadratic_constraints()
        """
        return self._make_group(self.constraint_type.quadratic, *args)

    def indicator_constraints(self, *args):
        """Returns an object instructing the conflict refiner to include
        all indicator constraints.

        If called with no arguments, every indicator constraint is
        assigned weight 1.0.

        If called with one or more arguments, every indicator
        constraint is assigned a weight equal to the float passed in
        as the first argument.

        If additional arguments are specified, they determine a subset
        of indicator constraints to be included.  If one indicator
        constraint index or name is specified, it is the only
        indicator constraint that will be included.  If two indicator
        constraint indices or names are specified, the all indicator
        constraints between the first and the second, inclusive, will
        be included.  If a sequence of indicator constraint names or
        indices is passed in, they will all be included.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.conflict.indicator_constraints()
        """
        return self._make_group(self.constraint_type.indicator, *args)

    def pwl_constraints(self, *args):
        """Returns an object instructing the conflict refiner to include
        all PWL constraints.

        If called with no arguments, every PWL constraint is assigned
        weight 1.0.

        If called with one or more arguments, every PWL constraint is
        assigned a weight equal to the float passed in as the first
        argument.

        If additional arguments are specified, they determine a subset
        of PWL constraints to be included. If one PWL constraint index or
        name is specified, it is the only PWL constraint that will be
        included. If two PWL constraint indices or names are specified,
        then all PWL constraints between the first and the second,
        inclusive, will be included. If a sequence of PWL constraint
        names or indices is passed in, they will all be included.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.conflict.pwl_constraints()
        """
        return self._make_group(self.constraint_type.pwl, *args)

    def SOS_constraints(self, *args):
        """Returns an object instructing the conflict refiner to include
        all SOS constraints.

        If called with no arguments, every SOS constraint is assigned
        weight 1.0.

        If called with one or more arguments, every SOS constraint is
        assigned a weight equal to the float passed in as the first
        argument.

        If additional arguments are specified, they determine a subset
        of SOS constraints to be included.  If one SOS constraint
        index or name is specified, it is the only SOS constraint that
        will be included.  If two SOS constraint indices or names are
        specified, then all SOS constraints between the first and the
        second, inclusive, will be included.  If a sequence of SOS
        constraint names or indices is passed in, they will all be
        included.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> group = c.conflict.SOS_constraints()
        """
        return self._make_group(self.constraint_type.SOS, *args)

    @staticmethod
    def _expand_groups(args):
        """Expands group arguments passed to the refine methods

        These should be either _group objects or tuples of length two
        (the first entry of which is the preference for the group (a
        float), the second of which is a tuple of pairs (type, id),
        where type is an attribute of conflict.constraint_type and id is
        either an index or a valid name for the type).

        As _group objects can contain many tuples, this method makes
        sure that the expanded order is maintained.
        """
        groups = []
        for arg in args:
            try:
                # Grab the tuple list out of any _group objects we encounter.
                groups.extend(arg._gp)
            except AttributeError:
                # Otherwise, we assume these are tuples.
                groups.append(arg)
        return groups

    def _separate_groups(self, args):
        """Separates group information into individual lists.

        This, so they can be passed into the callable library in the
        expected format.
        """
        grppref, grpbeg, grpind, grptype = [], [], [], []
        groups = self._expand_groups(args)
        for group in groups:
            pref, contpl = group
            grppref.append(pref)
            grpbeg.append(len(grpind))
            for contype, conid in contpl:
                tran = self._getconvfunc(contype)
                grptype.append(contype)
                grpind.append(tran(conid))
        return grppref, grpbeg, grpind, grptype

    def _compose_groups(self, grppref, grpbeg, grpind, grptype):
        """Convert individual lists of group information into group
        format.

        These are tuples of length two (the first entry of which is the
        preference for the group (a float), the second of which is a
        tuple of pairs (type, id), where type is an attribute of
        conflict.constraint_type and id is either an index or a valid
        name for the type).
        """
        groups = []
        grpbeglen = len(grpbeg)
        for i in range(grpbeglen):
            begin = grpbeg[i]
            if i == grpbeglen - 1:
                end = len(grpind)
            else:
                end = grpbeg[i + 1]
            groups.append((grppref[i], tuple(zip(grptype[begin:end],
                                                 grpind[begin:end]))))
        return groups

    def _make_group(self, which, *args):
        conv = self._getconvfunc(which)
        max_num = self._getnum(which)
        return make_group(conv, max_num, which, *args)

    def _getinterface(self, which):
        contype = self.constraint_type
        switcher = {
            contype.lower_bound: self._cplex.variables,
            contype.upper_bound: self._cplex.variables,
            contype.linear: self._cplex.linear_constraints,
            contype.quadratic: self._cplex.quadratic_constraints,
            contype.SOS: self._cplex.SOS,
            contype.indicator: self._cplex.indicator_constraints,
            contype.pwl: self._cplex.pwl_constraints
        }
        return switcher[which]

    def _getnum(self, which):
        interface = self._getinterface(which)
        return interface.get_num()

    def _getconvfunc(self, which):
        interface = self._getinterface(which)
        return interface._conv

    def refine_MIP_start(self, MIP_start, *args):
        """Identifies a minimal conflict among a set of constraints for a
        given MIP start.

        This method can take arbitrarily many arguments.  The first
        argument must be either a name or index of a MIP start.
        Additional arguments are optional and can be the object returned
        by `all_constraints()` or any combination of constraint groups
        and objects returned by `upper_bound_constraints()`,
        `lower_bound_constraints()`, `linear_constraints()`,
        `quadratic_constraints()`, `indicator_constraints()`,
        `pwl_constraints()`, or `SOS_constraints()` may be used to
        specify the constraints to consider. If no additional arguments
        are specified, then constraint groups are created automatically
        as in the CPLEX interactive.

        Constraint groups are sequences of length two, the first entry
        of which is the preference for the group (a float), the second
        of which is a sequence of pairs (type, id), where type is an
        attribute of conflict.constraint_type and id is either an index
        or a valid name for the type.

        See :mipapi:`CPXrefinemipstartconflictext` and in the Callable
        Library Reference Manual.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> indices = c.variables.add([1], [0], [0], c.variables.type.binary)
        >>> indices = c.variables.add([2], [0], [0], c.variables.type.binary)
        >>> c.solve()
        >>> indices = c.linear_constraints.add(
        ...     lin_expr=[[[0, 1], [1.0, 1.0]]], senses="E", rhs=[2.0])
        >>> c.conflict.refine_MIP_start(0, c.conflict.all_constraints())
        >>> c.conflict.get()
        [-1, -1, -1, -1, 3]
        >>> c.conflict.group_status[3], c.conflict.group_status[-1]
        ('member', 'excluded')
        >>> c.conflict.get_groups(0, 3)
        [(1.0, ((2, 0),)), (1.0, ((2, 1),)), (1.0, ((1, 0),)), (1.0, ((1, 1),))]
        """
        self._cplex._setup_callbacks()
        mipstartindex = self._cplex.MIP_starts._conv(MIP_start)
        if args:
            grppref, grpbeg, grpind, grptype = self._separate_groups(args)
        else:
            grppref, grpbeg, grpind, grptype = None, None, None, None
        CPX_PROC.refinemipstartconflictext(self._env._e, self._cplex._lp,
                                           mipstartindex,
                                           grppref, grpbeg, grpind, grptype)

    def refine(self, *args):
        """Identifies a minimal conflict among a set of constraints.

        This method can take arbitrarily many arguments.  Either the
        object returned by `all_constraints()` or any combination of
        constraint groups and objects returned by
        `upper_bound_constraints()`, `lower_bound_constraints()`,
        `linear_constraints()`, `quadratic_constraints()`,
        `indicator_constraints()`, `pwl_constraints()`, or
        `SOS_constraints()` may be used to specify the constraints to
        consider. Alternatively, if no arguments are specified, then
        constraint groups are created automatically as in the CPLEX
        interactive.

        Constraint groups are sequences of length two, the first entry
        of which is the preference for the group (a float), the second
        of which is a sequence of pairs (type, id), where type is an
        attribute of conflict.constraint_type and id is either an index or
        a valid name for the type.

        See :cpxapi:`CPXrefineconflictext` in the Callable Library
        Reference Manual.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> c.read("infeasible.lp")
        >>> c.conflict.refine(c.conflict.linear_constraints(),
        ...                   c.conflict.lower_bound_constraints())
        >>> c.conflict.get()
        [3, -1, 3, -1, -1, -1]
        >>> c.conflict.group_status[3], c.conflict.group_status[-1]
        ('member', 'excluded')
        >>> c.conflict.get_groups([0, 2])
        [(1.0, ((3, 0),)), (1.0, ((1, 0),))]
        """
        self._cplex._setup_callbacks()
        if args:
            grppref, grpbeg, grpind, grptype = self._separate_groups(args)
        else:
            grppref, grpbeg, grpind, grptype = None, None, None, None
        CPX_PROC.refineconflictext(self._env._e, self._cplex._lp,
                                   grppref, grpbeg, grpind, grptype)

    def get(self, *args):
        """Returns the status of a set of groups of constraints.

        Can be called by four forms.

        If called with no arguments, returns a list containing the
        status of all constraint groups.

        If called with one integer argument, returns the status of
        that constraint group.

        If called with two integer arguments, returns the status of
        all constraint groups between the first and second argument,
        inclusive.

        If called with a sequence of integers as its argument, returns
        the status of all constraint groups in the sequence.

        The status codes are attributes of
        Cplex.conflict.group_status.

        See :cpxapi:`CPXgetconflictext` in the Callable Library Reference
        Manual.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> c.read("infeasible.lp")
        >>> c.conflict.refine(c.conflict.all_constraints())
        >>> confstatus = c.conflict.get()
        """
        def getconflict(a, b=self.get_num_groups() - 1):
            return CPX_PROC.getconflictext(self._env._e, self._cplex._lp, a, b)
        return apply_freeform_two_args(getconflict, None, args)

    def get_num_groups(self):
        """Returns the number of constraint groups used in the last call
        to `refine()` or `refine_MIP_start()`.

        See :cpxapi:`CPXgetconflictnumgroups` in the Callable Library
        Reference Manual.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> c.read("infeasible.lp")
        >>> c.conflict.refine(c.conflict.all_constraints())
        >>> c.conflict.get_num_groups()
        10
        """
        return CPX_PROC.getconflictnumgroups(self._env._e, self._cplex._lp)

    def get_groups(self, *args):
        """Returns the groups of constraints used in the last call to
        `refine()` or `refine_MIP_start()`.

        Can be called by four forms.

        If called with no arguments, returns a list containing all
        constraint groups.

        If called with one integer argument, returns that constraint
        group.

        If called with two integer arguments, returns all constraint
        groups between the first and second argument, inclusive.

        If called with a sequence of integers as its argument, returns
        all constraint groups in the sequence.

        Constraint groups are tuples of length two, the first entry of
        which is the preference for the group (a float), the second of
        which is a tuple of pairs (type, id), where type is an
        attribute of conflict.constraint_type and id is either an index
        or a valid name for the type.

        See :cpxapi:`CPXgetconflictgroups` in the Callable Library
        Reference Manual.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> c.read("infeasible.lp")
        >>> c.conflict.refine(c.conflict.all_constraints())
        >>> groups = c.conflict.get_groups()
        """
        def getgroups(begin, end=self.get_num_groups() - 1):
            (grppref, grpbeg, grpind,
             grptype) = CPX_PROC.getconflictgroups(self._env._e,
                                                   self._cplex._lp,
                                                   begin, end)
            return self._compose_groups(grppref, grpbeg, grpind, grptype)
        return apply_freeform_two_args(getgroups, None, args)

    def write(self, filename):
        """Writes the conflict to a file.

        See :cpxapi:`CPXclpwrite` in the Callable Library Reference
        Manual.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> c.read("infeasible.lp")
        >>> c.conflict.refine(c.conflict.all_constraints())
        >>> c.conflict.write("conflict.clp")
        """
        CPX_PROC.clpwrite(self._env._e, self._cplex._lp, filename)


class PivotVarStatus(ConstantClass):
    """Use as input to pivoting methods."""
    at_lower_bound = _constants.CPX_AT_LOWER
    at_upper_bound = _constants.CPX_AT_UPPER


class AdvancedCplexInterface(BaseInterface):
    """Advanced control of a Cplex object."""

    no_variable = _constants.CPX_NO_VARIABLE
    """See `_constants.CPX_NO_VARIABLE` """
    variable_status = PivotVarStatus()
    """See `PivotVarStatus()` """

    def delete_names(self):
        """Deletes all names from the problem and its objects."""
        CPX_PROC.delnames(self._env._e, self._cplex._lp)

    def basic_presolve(self):
        """Performs bound strengthening and detects redundant rows.

        Returns a tuple containing three lists: a list containing the
        strengthened lower bounds, a list containing the strengthened
        upper bounds, and a list containing the status of each row.

        See :cpxapi:`CPXbasicpresolve` in the Callable Library Reference
        Manual.

        Note
          This method does not create a presolved problem.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> c.read("lpex.mps")
        >>> redlb, redub, rstat = c.advanced.basic_presolve()
        """
        return CPX_PROC.basicpresolve(self._env._e, self._cplex._lp)

    def pivot(self, enter, leave, status):
        """Pivots a variable into the basis.

        enter is a name or index of a variable or linear constraint.
        The index of a slack variable is specified by a negative
        integer; -i - 1 refers to the slack associated with the ith
        linear constraint.  enter must not identify a basic variable.

        leave is a name or index of a variable or linear constraint.
        The index of a slack variable is specified by a negative
        integer; -i - 1 refers to the slack associated with the ith
        linear constraint.  leave must identify either a basic
        variable or a non-basic variable with both a lower and upper
        bound to indicate that it is to move to its opposite bound.
        leave may also be set to Cplex.advanced.no_variable to
        instruct CPLEX to use a ratio test to determine the entering
        variable.

        Note
          If a linear constraint has the same name as a column, it must
          be specified by -index - 1, not by name.

        status must be an attribute of Cplex.advanced.variable_status
        specifying the nonbasic status to be assigned to the leaving
        variable after the basis change.

        """
        def conv(var):
            try:
                return self._cplex.variables._conv(var)
            except CplexSolverError:
                # Variable name not found, try linear constraints.
                return -self._cplex.linear_constraints._conv(var) - 1
        CPX_PROC.pivot(self._env._e, self._cplex._lp, conv(enter),
                       conv(leave), status)

    def pivot_slacks_in(self, which):
        """Forcibly pivots slack variables into the basis.

        which may be either a single linear constraint index or name
        or a sequence of linear constraint indices or names.

        """
        x = listify(self._cplex.linear_constraints._conv(which))
        CPX_PROC.pivotin(self._env._e, self._cplex._lp, x)

    def pivot_fixed_variables_out(self, which):
        """Forcibly pivots structural variables out of the basis.

        which may be either a single variable index or name or a
        sequence of variable indices or names.

        """
        x = listify(self._cplex.variables._conv(which))
        CPX_PROC.pivotout(self._env._e, self._cplex._lp, x)

    def strong_branching(self, variables, it_limit):
        """Performs strong branching.

        variables is a sequence of names or indices of variables.

        it_limit is an integer that specifies the number of iterations
        allowed.

        Returns a list of pairs (down_penalty, up_penalty) with the
        same length as variables containing the penalties for
        branching down or up, respectively, on each variable.

        See :cpxapi:`CPXstrongbranch` in the Callable Library Reference
        Manual for more detail.

        Example usage:

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> out = c.set_results_stream(None)
        >>> out = c.set_log_stream(None)
        >>> itlim = c.parameters.simplex.limits.iterations.get()
        >>> c.read("example.mps")
        >>> c.solve()
        >>> vars = list(range(c.variables.get_num()))
        >>> result = c.advanced.strong_branching(vars, itlim)
        """
        def conv(var):
            return self._cplex.variables._conv(var)
        return unzip(CPX_PROC.strongbranch(
            self._env._e, self._cplex._lp,
            conv(variables), it_limit))

    def complete(self):
        """See :cpxapi:`CPXcompletelp` in the Callable Library Reference
        Manual."""
        CPX_PROC.completelp(self._env._e, self._cplex.lp)


class BranchDirection(ConstantClass):
    """Constants defining branch directions"""
    default = _constants.CPX_BRANCH_GLOBAL
    down = _constants.CPX_BRANCH_DOWN
    up = _constants.CPX_BRANCH_UP


class OrderInterface(BaseInterface):
    """Methods for setting and querying a priority order for branching.

    Example usage:

    >>> import cplex
    >>> c = cplex.Cplex()
    >>> indices = c.variables.add(names = [str(i) for i in range(5)])
    >>> c.variables.set_types(zip(list(range(5)), ["C","I","I","I","I"]))
    >>> c.order.set([(1, 10, c.order.branch_direction.up), ('3', 5, c.order.branch_direction.down)])
    >>> c.order.get()
    [(1, 10, 1), (3, 5, -1)]
    >>> c.order.get_variables()
    [1, 3]
    """

    branch_direction = BranchDirection()
    """See `BranchDirection()` """

    def get(self):
        """Returns a list of triples (variable, priority, direction)
        representing the priority order for branching.
        """
        return unzip(CPX_PROC.getorder(self._env._e, self._cplex._lp))

    def get_variables(self):
        """Returns the variables for which an order has been set."""
        return CPX_PROC.getorder(self._env._e, self._cplex._lp)[0]

    def set(self, order):
        """Sets the priority order for branching.

        order must be a list of triples (variable, priority, direction).

        variable must be an index or name of a variable.

        priority must be a nonnegative integer.

        direction must be an attribute of order.branch_direction.
        """
        ord = unzip(order)
        ord[0] = self._cplex.variables._conv(ord[0])
        CPX_PROC.copyorder(self._env._e, self._cplex._lp, *ord)

    def read(self, filename):
        """Reads a priority order from a file."""
        CPX_PROC.readcopyorder(self._env._e, self._cplex._lp, filename)

    def write(self, filename):
        """Writes the priority order to a file."""
        CPX_PROC.ordwrite(self._env._e, self._cplex._lp, filename)


class InitialInterface(BaseInterface):
    """Methods to set starting information for an optimization algorithm
    to solve continuous problems (LP, QP, QCP).

    Note
      Data passed to these methods cannot be queried immediately from
      the methods in Cplex.solution.  Those methods will return
      data only after Cplex.solve() or Cplex.feasopt() has been called.
    """

    status = BasisVarStatus()
    """See `BasisVarStatus()` """

    def set_start(self, col_status, row_status, col_primal, row_primal,
                  col_dual, row_dual):
        """Sets basis statuses, primal values, and dual values.

        The arguments col_status, col_primal, and col_dual are lists
        that either have length equal to the number of variables or
        are empty.  If col_status is empty, then row_status must also
        be empty.  If col_primal is empty, then row_primal must also
        be empty.

        The arguments row_status, row_primal, and row_dual are lists
        that either have length equal to the number of linear
        constraints or are empty.  If row_status is empty, the
        col_status must also be empty.  If row_dual is empty, then
        col_dual must also be empty.

        Each entry of col_status and row_status must be an attribute of
        Cplex.start.status.

        Each entry of col_primal and row_primal must be a float
        specifying the starting primal values for the columns and
        rows, respectively.

        Each entry of col_dual and row_dual must be a float
        specifying the starting dual values for the columns and rows,
        respectively.

        Note
          The starting information is ignored by the optimizers if the
          parameter cplex.parameters.advance is set to
          cplex.parameters.advance.values.none.

        >>> import cplex
        >>> c = cplex.Cplex()
        >>> indices = c.variables.add(
        ...     names=["v{0}".format(i) for i in range(5)]
        ... )
        >>> indices = c.linear_constraints.add(
        ...     names=["r{0}".format(i) for i in range(3)]
        ... )
        >>> s = c.start.status
        >>> c.start.set_start(
        ...     [s.basic] * 3 + [s.at_lower_bound] * 2,
        ...     [s.basic] + [s.at_upper_bound] * 2,
        ...     [0.0] * 5,
        ...     [1.0] * 3,
        ...     [2.0] * 5,
        ...     [3.0] * 3
        ... )
        """
        CPX_PROC.copystart(self._env._e, self._cplex._lp, col_status,
                           row_status, col_primal, row_primal, col_dual,
                           row_dual)

    def read_start(self, filename):
        """Reads the starting information from a file.

        See :cpxapi:`CPXreadcopystartinfo` in the Callable Library
        Reference Manual and also `SolutionInterface.write()`.

        Example usage:

        >>> import cplex
        >>> c1 = cplex.Cplex()
        >>> out = c1.set_results_stream(None)
        >>> out = c1.set_log_stream(None)
        >>> c1.read("lpex.mps")
        >>> c1.solve()
        >>> c1.solution.write("lpex.sol")
        >>> c2 = cplex.Cplex()
        >>> out = c2.set_results_stream(None)
        >>> out = c2.set_log_stream(None)
        >>> c2.read("lpex.mps")
        >>> c2.start.read_start("lpex.sol")
        """
        CPX_PROC.readcopystartinfo(self._env._e, self._cplex._lp, filename)

    def read_basis(self, filename):
        """Reads the starting basis from a file.

        See :cpxapi:`CPXreadcopybase` in the Callable Library Reference
        Manual and also `BasisInterface.write()`.

        Example:

        >>> import cplex
        >>> c1 = cplex.Cplex()
        >>> out = c1.set_results_stream(None)
        >>> out = c1.set_log_stream(None)
        >>> c1.read("lpex.mps")
        >>> c1.solve()
        >>> c1.solution.basis.write("lpex.bas")
        >>> c2 = cplex.Cplex()
        >>> out = c2.set_results_stream(None)
        >>> out = c2.set_log_stream(None)
        >>> c2.read("lpex.mps")
        >>> c2.start.read_basis("lpex.bas")
        """
        CPX_PROC.readcopybase(self._env._e, self._cplex._lp, filename)
