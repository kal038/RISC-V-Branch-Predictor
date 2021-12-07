'''
Kartikeya Sharma and Khoi Lam
Final Project
Saturating Counter Class for Branch Predictors
'''

class SaturatingCounter:

    def __init__(self, width = 2):
        '''
        The default is 2 bit counter although you could extend to an n-bit counter later on

        '''
        self.width = width
        self.counter = 2
        

    def get_prediction(self):
        '''
        return: True if the MSB of the number is 1 
        return: False if the MSB of the number is 0
        True signifies a prediction of Taken and False signifies a prediction of Not Taken
        '''
        bin_temp = '{0:02b}'.format(self.counter) # converts counter into binary string
        if bin_temp[0] == "1": # MSB obtained by first character in binary string
            return True
        else:
            return False 

    def decrement(self):
        if self.counter > 0:
            self.counter -= 1
        else:
            return 


    def increment(self):
        if self.counter < (2**self.width) - 1:
            #print("here")
            self.counter += 1
        else:
            #print("Saturated")
            return

    def get_width(self):
        return self.width


    def __repr__(self) -> str:
        return '{0:02b}'.format(self.counter)

    def __str__(self) -> str:
        return '{0:02b}'.format(self.counter)

"""
Unit Tests for SaturatingCounter"
"""
if __name__ == "__main__":
    my_counter = SaturatingCounter()
    print("Prediction should be False, got:" + str(my_counter.get_prediction()))
    my_counter.decrement() # should do nothing here
    print("Counter starting value should be 00, got: "+ str(my_counter))
    print("Increment Counter")
    my_counter.increment()
    print("Counter value should be 01, got: "+ str(my_counter))
    print("Prediction should be False, got:" + str(my_counter.get_prediction()))
    my_counter.increment()
    print("Increment Counter")
    print("Counter value should be 10, got: "+ str(my_counter))
    print("Prediction should be True, got:" + str(my_counter.get_prediction()))
    my_counter.increment()
    print("Increment Counter")
    print("Counter value should be 11, got: "+ str(my_counter))
    print("Prediction should be True, got:" + str(my_counter.get_prediction()))
    my_counter.increment()
    print("Increment Counter")
    print("Counter value should be 11, got: "+ str(my_counter))
    print("Prediction should be True, got:" + str(my_counter.get_prediction()))






