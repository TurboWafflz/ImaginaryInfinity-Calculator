import os
import inspect
for module in os.listdir("plugins"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    module=module[:-3]
    moduleRaw=module
    module="plugins."+module
    print(module)
    __import__(module, locals(), globals())
    #functions = dir(moduleRaw)
    #print(dir(moduleRaw))
    #for function in functions:
    #    __import__(module, locals(), globals(), fromlist=function)
    #    print(module+"."+function)
del module
