# -*- coding: utf-8 -*-
#
################################################################################
# probably it is python 2
#
# def execute_function(self, func, *nargs, **kwargs):
    # """
    # Execute a function object within the execution context.
    # @returns The result of the function call.
    # """
    # # makes a copy of the func
    # import types
    # fn = types.FunctionType(func.func_code,
                            # func.func_globals.copy(),
                            # name=func.func_name,
                            # argdefs=func.func_defaults,
                            # closure=func.func_closure)
    # fn.func_globals.update(self.globals)
    # return fn(*nargs, **kwargs)


# def copy_func(func):
    # """
    # Return a copy of a function with a shallow copy of the original's
    # func_globals.
    # """
    # import types
    # return types.FunctionType(func.func_code, dict(func.func_globals),
                              # name=func.func_name, argdefs=func.func_defaults,
                              # closure=func.func_closure)



###########################################################
"""
__code__
__globals__
__name__
__defaults__
__closure__
"""
# -------------------------------
def copy_func(func):
    import types
    return types.FunctionType(func.__code, dict(func.__globals__),
                              name=func.__name__, argdefs=func.__defaults__,
                              closure=func.__closure__)


def execute_function(self, func, *nargs, **kwargs):
    """
    Execute a function object within the execution context.
    @returns The result of the function call.
    """
    # makes a copy of the func
    import types
    fn = types.FunctionType(func.__code__,
                            func.__globals__.copy(),
                            name=func.__name__,
                            argdefs=func.__defaults__,
                            closure=func.__closure__)

    fn.__globals__.update(self.globals)

    return fn(*nargs, **kwargs)
