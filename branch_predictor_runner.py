from branch_predictor_info import BranchPredictorInfo
from tournament_pred import TournamentPred

def print_pct_taken():
	num_taken = 0
	for branch_event in BranchPredictorInfo.grouped_branch_seqs:
		if branch_event["is_taken"]:
			num_taken += 1
	pct_taken = \
	num_taken / len(BranchPredictorInfo.grouped_branch_seqs)
	print(pct_taken * 100)

def simulate_tp(width: int):
	tp = TournamentPred(width = TABLE_WIDTH)
	correct_preds = 0
	for branch_event in BranchPredictorInfo.grouped_branch_seqs:
		pc_sel = int( \
		(int(branch_event["instr"]["pc"], 16) / (2**TABLE_WIDTH)) \
		% (2**TABLE_WIDTH)
		)
		branch_event_pred = \
		tp.get_prediction(pc_sel)
		if branch_event_pred == branch_event["is_taken"]:
			correct_preds += 1
		else:
			tp.update_predictor(
				branch_event["is_taken"],
				pc_sel
			)
	pct_correct = \
	correct_preds / len(BranchPredictorInfo.grouped_branch_seqs)
	# print(f"TABLE_WIDTH: {width}; pct_correct: {pct_correct * 100}")	
	print(pct_correct * 100)

if __name__ == "__main__":
	BranchPredictorInfo.init()
	print(BranchPredictorInfo.get_str())	
	print_pct_taken()
	for TABLE_WIDTH in range(1, 17):
		simulate_tp(width = TABLE_WIDTH)
