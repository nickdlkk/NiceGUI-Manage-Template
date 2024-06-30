# 导入当前包的所有模块，这里假设所有模块都在同一个目录下
import importlib
import inspect
import pkgutil

from . import *
from .module_base import BaseClass

# 定义一个字典来存储所有注册的类
derived_class_registry = {}

# 动态导入包内所有模块
package_name = __name__
for _, module_name, _ in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f".{module_name}", package=package_name)


# 定义一个函数来根据类名创建类的实例
def instantiate_class_by_name(class_name):
    if class_name in derived_class_registry:
        return derived_class_registry[class_name]()
    else:
        print(f"No class named {class_name} found in the registry or it does not derive from BaseClass.")


# 定义函数来注册所有继承自BaseClass的类
def register_derived_classes():
    for module_name, module in globals().items():
        if inspect.ismodule(module) and module is not importlib:
            # 遍历模块中的所有成员
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # 检查类是否继承自BaseClass且不是BaseClass本身
                if issubclass(obj, BaseClass) and obj is not BaseClass:
                    # 将类添加到注册字典中
                    derived_class_registry[obj.__name__] = obj
                    instantiate_class_by_name(obj.__name__)


# 当__init__.py被执行时，自动注册所有继承自BaseClass的类
register_derived_classes()
