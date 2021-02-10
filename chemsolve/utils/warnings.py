import inspect
import logging
import pkg_resources

current_version = pkg_resources.get_distribution("chemsolve").version

def get_called_class():
   '''
   Gets the class which the method was called from.
   '''
   stack = inspect.stack()
   tclass = stack[1][0].f_locals["self"].__class__.__name__
   return tclass

def ChemsolveDeprecationWarning(deprecated_object, future_version = current_version):
   '''
   Warning that a class or method will be removed in a future version.
   If a future version is not specified, then the current version is assumed.
   '''
   # Get the object name.
   deprecated_object_name = deprecated_object.__class__.__name__
   logging.warning((f"The feature '{deprecated_object_name}' you are using will be removed "
                    f"following v" + str(future_version) + "."))

def assert_presence(initial, determiner):
   '''
   Determine if an item in one list is present in another list.
   Used to confirm that a reactant is also present as a product.
   '''
   for item in initial:
      if item not in determiner:
         raise ValueError("A reactant must also be a product in a reaction.")



