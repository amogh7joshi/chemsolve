from chemsolve.reaction import Reaction

# Original code for printing out a balanced reaction.
# More optimized, but would print them out in a different order.
# Replaced for aesthetics.
'''
      for dict in self.__balanced:
         for item in dict:
            e = list(dict.items())
            dict[item] = int(dict[item])
            if not dict[item] == 1:
               tempstr += str(dict[item])
            tempstr += str(Compound(str(item)).__str__()) + str(" ")
            if item != e[-1][0]:
               tempstr += str("+ ")
         if count == 0:
            tempstr += str("--> ")
         count += 1
'''