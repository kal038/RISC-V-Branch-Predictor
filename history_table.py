'''
History Table Class to represent the BHT, PHT, and Meta Predictors
'''

from saturating_counter import SaturatingCounter

class HistoryTable:
    
    def __init__(self, name = "BHT", width = 2):
        self.name = name # name, e.g. BHT, PHT
        self.height = 2 ** width # height of the table
				 #  is 2 ^ num selection bits
        self.table = [None] * self.height # initialize array based on height
        for i in range(self.height):
            self.table[i] = SaturatingCounter() # for each index in array, 
						# make a saturating counter object
						# with value 10

    def increment(self, idx):
        self.table[idx].increment()
        return

    def decrement(self,idx):
        self.table[idx].decrement()

    def get_prediction(self, idx):
        return self.table[idx].get_prediction()

    def get_value(self, idx):
        return self.table[idx]

    def __repr__(self) -> str:
        return str(self.table)

    def __str__(self) -> str:
        return str(self.table)

"""
Unit Tests for HistoryTable
"""
if __name__ == "__main__":
    my_BHT = HistoryTable()
    print(my_BHT)
    my_BHT.increment(0)
    print(my_BHT)
    print("Incrementing idx 11")
    my_BHT.increment(3)
    print(my_BHT)
    print("Getting prediction from idx 11, should be False, got: " + str(my_BHT.get_prediction(3)) + ", Value = " + str(my_BHT.get_value(3)))
    print("Incrementing idx 11")
    my_BHT.increment(3)
    print(my_BHT)
    print("Getting prediction from idx 11, should be True, got: " + str(my_BHT.get_prediction(3)) + ", Value = " + str(my_BHT.get_value(3)))
    print("Incrementing idx 11")
    my_BHT.increment(3)
    print(my_BHT)
    print("Getting prediction from idx 11, should be True, got: " + str(my_BHT.get_prediction(3)) + ", Value = " + str(my_BHT.get_value(3)))
    print("Incrementing idx 11")
    my_BHT.increment(3)
    print(my_BHT)
    print("Getting prediction from idx 11, should be True, got: " + str(my_BHT.get_prediction(3)) + ", Value = " + str(my_BHT.get_value(3)))
    

