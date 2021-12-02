'''
Have to call get_prediction before update_predictor or will crash
'''
from history_table import HistoryTable
from saturating_counter import SaturatingCounter
from global_branch_history import GlobalBranchHistory
from mux import make_mux

class TournamentPred:
    


    def __init__(self, width = 2):
        '''
        For this tournament predictor we need 3 History Tables: BHT, PHT, and Meta
        We also need a 2-input Mux
        BHT table is indexed by 2 bits of PC
        PHT and Meta indexed by 2 bits of Global Branch History
        width indicates how many bits of the PC and Global Branch History we are using to index BHT, PHT, Meta
        '''
        self.BHT = HistoryTable("BHT", width) # This by default has height of 4 if we're using just 2 bits of PC to index
        self.PHT = HistoryTable("PHT", width)
        self.meta = HistoryTable("Meta", width)
        self.BHT_prediction = None
        self.PHT_prediction = None
        self.meta_predicton = None
        self.global_branch_hist = GlobalBranchHistory()
        
    def get_prediction(self, pc):
        '''
        Return: True if the prediction is Taken and False if the prediction is Not Taken
        '''
        self.BHT_prediction = self.BHT.get_prediction(pc)
        self.PHT_prediction = self.PHT.get_prediction(self.global_branch_hist.get_gbh())
        self.meta_predicton = self.meta.get_prediction(self.global_branch_hist.get_gbh()) # 0/False means that meta chose BHT and 1/True means that meta chose PHT
        mux = make_mux(lambda: self.BHT_prediction, lambda: self.PHT_prediction)
        if self.meta_predicton == True:
            mux_sel = 1
        else:
            mux_sel = 0
        
        return mux(mux_sel)


    def update_predictor(self, outcome, pc):
        '''
        Method to update the whole tournament predictor including the BHT, PHT, Meta, and Global Branch History

        Inputs: prediction -> bool, the prediction genereated by self.get_prediction
        outcome -> bool, the true outcome of the branch
        Outputs: None, changes the values of the predictors in-place

        Now there are two cases of updating the Meta predictor
        BHT Prediction == PHT Prediction: Meta stays unchanged since it can not favor one result over the other
        BHT Prediction != PHT Prediction: Increment/Decrement Meta based on which side it chose and whether that side turned out to predicted correctly
        '''
        if outcome == True:
            # outcome was that the branch was taken: increment both BHT and PHT at appropriate idx
            self.BHT.increment(pc)
            self.PHT.increment(self.global_branch_hist.get_gbh())
        else:
            # outcome was that the branch was not taken: decrement both BHT and PHT at appropriate idx
            self.BHT.decrement(pc)
            self.PHT.decrement(self.global_branch_hist.get_gbh())

        # After updating both the BHT and the PHT, decide if we need to update the meta predictor

        if self.BHT_prediction == self.PHT_prediction:
            # BHT and PHT predicted the same outcome, so meta stays the same
            pass
        else:
            # BHT and PHT predicted differently, so we have to update meta
            if self.PHT_prediction == outcome:
                # PHT predicted correctly, we have to increment to make meta choose PHT next time
                self.meta.increment(self.global_branch_hist.get_gbh())
            else:
                # PHT predicted incorrectly, we have to decrement to make meta choose BHT next time
                self.meta.decrement(self.global_branch_hist.get_gbh())
        
        # Now, the final step is to update the global branch hist
        # TODO: update the global branch history
        if outcome == True:
            self.global_branch_hist.shift_in(1)
        else:
            self.global_branch_hist.shift_in(0)

            

    def __repr__(self) -> str:
        return "BHT: " + str(self.BHT) + "\n" \
                + "PHT: " + str(self.PHT) + "\n" + \
                    "Meta:" + str(self.meta) + "\n" 






if __name__ == "__main__":
    my_tournament = TournamentPred()
    my_tournament.global_branch_hist.set_gbh("01")
    print(my_tournament)
    # Now write a test with an in-class example
    pc = 1
    global_branch_history = 1
    #my_tournament.BHT.table[pc] = 2
    my_tournament.BHT.decrement(pc) # starting value is 3, decrement once to get 2
    #my_tournament.PHT.table[global_branch_history] = 1
    my_tournament.PHT.decrement(global_branch_history)
    my_tournament.PHT.decrement(global_branch_history)
    #my_tournament.meta.table[global_branch_history] = 0
    my_tournament.meta.decrement(global_branch_history)
    my_tournament.meta.decrement(global_branch_history)
    my_tournament.meta.decrement(global_branch_history)
    print(my_tournament)
    # Now, generate prediction
    prediction = my_tournament.get_prediction(pc)
    print("Prediction from the tournament should be True, got: " + str(prediction))
    outcome = False
    my_tournament.update_predictor(outcome, pc)
    print(my_tournament)
    print(my_tournament.global_branch_hist)
