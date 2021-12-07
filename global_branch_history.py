class GlobalBranchHistory:
    
    def __init__(self, width = 2):
        self.width = width # number of selecting bits
        self.history = [0] * self.width # e.g. [0, 1]

    def shift_in(self, bit_val):
        if self.width == 2:
            self.history[self.width - 1] = self.history[0]
            self.history[0] = bit_val
        else:
            temp_arr = self.history[:self.width-1]
            self.history[0] = bit_val
            self.history[1:] = temp_arr

    def get_gbh(self):
        out = ""
        for char in self.history:
            out += str(char)
        return int(out, 2)

    def __repr__(self) -> str:
        out = ""
        for char in self.history:
            out += str(char)
        return out

    def set_gbh(self, value_as_string):
        for i in range(len(value_as_string)):
            self.history[i] = int(value_as_string[i])


"""
Units Tests for GlobalBranchHistory
"""
if __name__ == "__main__":
    my_gbh = GlobalBranchHistory()
    print(my_gbh.history)
    my_gbh.shift_in(1)
    print(my_gbh.history)
    print(my_gbh.get_gbh())
    my_gbh.shift_in(1)
    print(my_gbh.history)
    print(my_gbh.get_gbh())
    my_gbh.shift_in(1)
    print(my_gbh.history)
    print(my_gbh.get_gbh())
    my_gbh.shift_in(0)
    print(my_gbh.history)
    print(my_gbh.get_gbh())
    my_gbh.shift_in(0)
    print(my_gbh.history)
    print(my_gbh.get_gbh())
    print("----------------------------------")
    my_gbh = GlobalBranchHistory(7)
    my_gbh.set_gbh("0111110")
    print(my_gbh)
    my_gbh.shift_in(1)
    print(my_gbh)
