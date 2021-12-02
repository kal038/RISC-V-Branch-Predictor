from history_table import HistoryTable
from saturating_counter import SaturatingCounter
from global_branch_history import GlobalBranchHistory
from bpa_pyriscv.mux import make_mux

class BTB:

	def __init__(self):
		self.lookup_table = {}
 
	def get_prediction(self, pc: int):
		if pc not in self.lookup_table.keys(): return None
		else: return self.lookup_table[pc] 

	def update_predictor(self, pc_lookup: int, pc_targ: int):
		self.lookup_table[pc_lookup] = pc_targ

	def __repr__(self) -> str:
		pass

