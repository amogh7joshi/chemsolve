import inspect
import logging
import warnings
import collections.abc
import functools
import pkg_resources

current_version = pkg_resources.get_distribution("chemsolve").version

# Global value to determine if warning has already been displayed.
warned = []

def ChemsolveDeprecationWarning(deprecated_object = None, future_version = current_version):
   """
   Warning that a class or method will be removed in a future version.
   If a future version is not specified, then the current version is assumed.
   """
   def outer_decorator(obj):
      @functools.wraps(obj)
      def inner_decorator(*args, **kwargs):
         global warned
         # Get the object name.
         if deprecated_object:
            deprecated_object_name = deprecated_object
         if isinstance(obj, collections.abc.Callable):
            deprecated_object_name = deprecated_object
         elif isinstance(obj, object):
            deprecated_object_name = obj.__class__.__name__
         else:
            raise TypeError("INTERNAL: Got unknown object of unknown type, something is broken.")

         if deprecated_object_name not in warned:
            logging.warning((f"The feature '{deprecated_object_name}' you are using will be removed "
                             f"following v" + str(future_version) + "."))

            # Add to tracker.
            warned.append(deprecated_object_name)

         # Return general method.
         if isinstance(obj, collections.abc.Callable):
            return obj(*args, **kwargs)
      return inner_decorator
   return outer_decorator

def get_called_class(meth):
   """
   Gets the class which the method was called from.
   """
   for cls in inspect.getmro(meth.im_class):
      if meth.__name__ in cls.__dict__:
         return cls

def assert_presence(initial, determiner):
   """
   Determine if an item in one list is present in another list.
   Used to confirm that a reactant is also present as a product.
   """
   for item in initial:
      if item not in determiner:
         raise ValueError("A reactant must also be a product in a reaction.")



