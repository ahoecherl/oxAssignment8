from copy import deepcopy

def differentiate(fun, *args, epsilon=.000001, scheme='Forward'):
    argcount = args.__len__()
    derivative = [0.0] * argcount
    basevalue = fun(*args)
    if scheme == 'Forward':
        for i in range(0, argcount):
            mutargs = list(args)
            mutargs[i] = args[i]+epsilon
            mutargs = tuple(mutargs)
            bumpvalue = fun(*mutargs)
            derivative[i] = (bumpvalue - basevalue)/epsilon
    if scheme == 'Backward':
        for i in range(0, argcount):
            mutargs = list(deepcopy(args))
            mutargs[i] = args[i]+epsilon
            mutargs = tuple(mutargs)
            bumpvalue = fun(*mutargs)
            derivative[i] = (bumpvalue - basevalue)/epsilon
    return derivative