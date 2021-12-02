
from history_table import HistoryTable
from saturating_counter import SaturatingCounter
from mux import make_mux

class TournamentPred:
    


    def __init__(self):
        '''
        For this tournament predictor we need 3 History Tables: BHT, PHT, and Meta
        We also need a 2-input Mux
        BHT table is indexed by 2 bits of PC
        PHT and Meta indexed by 2 bits of Global Branch History
        '''
        self.BHT = HistoryTable("BHT") # This by default has height of 4 if we're using just 2 bits of PC to index
        self.PHT = HistoryTable("PHT")
        self.meta = HistoryTable("Meta")
        
    def get_prediction(self, pc, global_branch_hist):
        '''
        Return: True if the prediction is Taken and False if the prediction is Not Taken
        '''
        mux = make_mux(self.BHT.get_prediction(pc), self.PHT.get_prediction(global_branch_hist))
        if self.meta.get_prediction(global_branch_hist) == True:
            mux_sel = 1
        else:
            mux_sel = 0

        return mux(mux_sel)


    def update_predictor(self, prediction, result):
        '''
        Method to 

        Inputs: prediction -> bool, the prediction genereated by self.get_prediction
        result -> bool, the true outcome of the branch
        Outputs: None, changes the values of the predictors in-place

        Now there are two cases of updating the tournament predictor
        Wrong Prediction:
        Right Prediction:
        '''

        if prediction == result:
            # Right Prediction Case
            pass

        else:
            # Wrong Prediction Case
            pass

    def __repr__(self) -> str:
        return "BHT: " + str(self.BHT) + "\n" \
                + "PHT: " + str(self.PHT) + "\n" + \
                    "Meta:" + str(self.meta) + "\n" 






if __name__ == "__main__":
    my_tournament = TournamentPred()
    print(my_tournament)