# 导入当前包的所有模块

import importlib  # 用于动态导入模块
import inspect
import pkgutil  # 用于遍历包中的所有模块

from . import *
from .module_base import BaseClass

# 定义一个字典来存储所有注册的类
derived_class_registry = {}

# 动态导入包内所有模块
package_name = __name__


# 改为递归寻找所有子模块
def get_submodule(module_path, parent_module_name):
    import_module = []
    for i, module_name, ispkg in pkgutil.iter_modules(module_path):
        name = ""
        if parent_module_name is None:
            name = f".{module_name}"
        else:
            name = f"{parent_module_name}.{module_name}"
        sub_module = importlib.import_module(name, package=package_name)
        import_module.append(sub_module)
        # 导入该模块下的所有子模块
        if ispkg:
            import_module = import_module + get_submodule(sub_module.__path__, name)
    return import_module


import_module = get_submodule(__path__, None)

# print(f"modules {import_module}")


# 当__init__.py被执行时，自动注册所有继承自BaseClass的类，以此来注册所有装饰器
instance_dict = {}
for module in import_module:
    print(f"Registering derived class {module.__name__} in {module}")
    # 遍历模块中的所有成员
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # 检查类是否继承自BaseClass且不是BaseClass本身
        if issubclass(obj, BaseClass) and obj is not BaseClass:
            # 将类添加到注册字典中
            derived_class_registry[obj.__name__] = obj
            instance_dict[obj.__name__] = obj()
