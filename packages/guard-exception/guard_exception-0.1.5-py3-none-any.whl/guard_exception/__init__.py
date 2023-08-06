__autor__ = "Rafael Fernando Garcia Sagastume"
__copyright__ = "Copyright 2022, Rafael Fernando Garcia Sagastume"
__license__ = "BSD 3-Clause License"
__version__ = "0.1.5"
__maintainer__ = "Rafael Fernando Garcia Sagastume"
__status__ = "Production"


def guardException(f, **kwargs):
    """
    Description: catch fatal errors or any type of error,
    used to easily normalize executions in fast tween calls with PythonKit

    arguments: f: function to be executed
    kwargs: arguments to be passed to the function

    return: result of the function or str error message if any error occurs
    """

    error = None
    resultado = None
    try:
        resultado = f(**kwargs)
    except Exception as e:
        error = e.__str__()

    return {"data:": resultado, "error": error}
