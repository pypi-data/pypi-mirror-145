class PythonUtils:
    def __init__(self):
        print("调用构造方法")

    def NoneDefaultVale(param: object, default: object) -> object:
        if param is None:
            return default
        else:
            return param
