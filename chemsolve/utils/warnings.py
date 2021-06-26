#!/usr/bin/env python3
# -*- coding = utf-8 -*-
import inspect
import logging
import functools
import pkg_resources
import collections.abc

# Get the next major version.
from .._release import __version__
next_major_version = '.'.join((__version__[0] + 1, 0, 0))

# Global value to determine if warning has already been displayed.
_ISSUED_WARNINGS = []

def ChemsolveDeprecationWarning(deprecated_object = None, future_version = next_major_version):
   """Issues a warning for the deprecation of an object.

   This method, which can be used either as a decorator
   to methods/classes, or as a standalone method call
   for parameters, issues a warning that said object will
   be deprecated in a future version.

   Traditionally, the deprecation warning will be issued
   for the next major version, but when this is not the
   case, the `future_version` parameter can be adjusted.

   For situations where the method needs to be called
   directly, such as a deprecated parameter of a class,
   the `future_version` parameter can be set to 'bypass',
   in which case `deprecated_object` will be a custom
   deprecation message set during the method call.

   Examples
   --------
   Deprecating a method for a future version is as simple
   as using `ChemsolveDeprecationWarning` as a method.

   >>> @ChemsolveDeprecationWarning(
   ...   'chemsolve_method', future_version = '2.0.0')
   ... def chemsolve_method(param):
   ...   return param

   For deprecating a class parameter, `ChemsolveDeprecationWarning`
   should be used in the class's `__getattribute__` method.

   >>> class ChemsolveClass:
   ...   def __getattribute__(self, item):
   ...      if item == "deprecated_parameter":
   ...         ChemsolveDeprecationWarning(
   ...            "The parameter `deprecated_parameter` is "
   ...            "deprecated and will be removed following "
   ...            "version X.", future_version = 'bypass')

   Parameters
   ----------
   deprecated_object: str
      Either a string representing the name of the
      method/class which is decorated by this method,
      or a complete deprecation message when using
      the `bypass` mode.
   future_version: str
      A string representing the future version of the
      library in which the deprecated object will be
      removed, or the word `bypass` when deprecating
      a parameter to pass a custom message.
   """
   if future_version == 'bypass':
      # The warning is being naturally raised, not decorated onto
      # a specific function or class. So, just simply raise it.
      global _ISSUED_WARNINGS
      if deprecated_object not in _ISSUED_WARNINGS:
         logging.warning(deprecated_object)
         _ISSUED_WARNINGS.append(deprecated_object)
   else:
      # Otherwise, we need to use this method as a decorator.
      def outer_decorator(obj):
         @functools.wraps(obj)
         def inner_decorator(*args, **kwargs):
            global _ISSUED_WARNINGS
            # Get the object name.
            if isinstance(obj, collections.abc.Callable):
               deprecated_object_name = deprecated_object
            else:
               deprecated_object_name = obj.__class__.__name__

            # If a deprecation warning has not already been issued
            # for the object, then issue a new deprecation warning.
            if deprecated_object_name not in _ISSUED_WARNINGS:
               logging.warning(
                  f"The feature '{deprecated_object_name}' you are using "
                  f"will be removed following v" + str(future_version) + ".")
               _ISSUED_WARNINGS.append(deprecated_object_name)

            # If the object is a callable, return its value.
            if isinstance(obj, collections.abc.Callable):
               return obj(*args, **kwargs)
         return inner_decorator
      return outer_decorator

def get_called_class(meth):
   """Gets the class which the method was called from."""
   for cls in inspect.getmro(meth.im_class):
      if meth.__name__ in cls.__dict__:
         return cls



