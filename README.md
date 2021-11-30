Kartikeya Sharma and Khoi Lam
CSCI 320 Final Project
Branch Prediction Analyzer

1. Basic Commands

First, go to the main folder of this project. 
$ cd <wherever you imported this repository>/branch-prediction-analyzer

1.1 Extracting the instructions from a binary to an output file (for example - contents of output.txt:

                   0: PC: xxxxxxxx, IR: xxxxxxxx
                   1: PC: 80000000, IR: 00000093, li ra,0x0
                   2: PC: 80000004, IR: 00000113, li sp,0x0
                   3: PC: 80000008, IR: 00000193, li gp,0x0
                   4: PC: 8000000c, IR: 00000213, li tp,0x0
                   5: PC: 80000010, IR: 00000293, li t0,0x0
                   6: PC: 80000014, IR: 00000313, li t1,0x0
                   7: PC: 80000018, IR: 00000393, li t2,0x0
                   8: PC: 8000001c, IR: 00000413, li s0,0x0

                   ...
):

$ ./instr_extract.sh -e bpa-pyriscv/riscv_isa/programs/return -o output.txt

NOTE: If your command prompt mentions that you do not have permission to run the instr_extract .sh script,
then run the following command: 
$ chmod +x instr_extract.sh.

1.2 Importing the output of instructions into the BranchPredictor class:

$ python3 branch_predictor_runner.py output.txt 

I currently have the runner setup such that it prints out the list of dictionaries, where each
dictionary is an instruction (aka "Instructions" in the output) and the list of dictionaries,
where each dictionary is a branch event, so to speak (aka "Grouped Branch Sequences" in the output).

Example output:

Instructions:
[
0: None,
1: {'pc': '80000000', 'ir': '00000093', 'str': 'li ra,0x0'},
2: {'pc': '80000004', 'ir': '00000113', 'str': 'li sp,0x0'},
3: {'pc': '80000008', 'ir': '00000193', 'str': 'li gp,0x0'},
4: {'pc': '8000000c', 'ir': '00000213', 'str': 'li tp,0x0'},

...

Grouped Branch Sequences
[
0: {'instr': {'pc': '8000008c', 'ir': '0002ca63', 'str': 'bltz t0,0x800000a0'}, 'predicted_pc': '800000a0', 'actual_pc': '800000a0', 'is_taken': True},
1: {'instr': {'pc': '800000c4', 'ir': '00b57063', 'str': 'bgeu a0,a1,0x800000c4'}, 'predicted_pc': '800000c4', 'actual_pc': '800000c8', 'is_taken': False},
2: {'instr': {'pc': '80001284', 'ir': '02078863', 'str': 'beqz a5,0x800012b4'}, 'predicted_pc': '800012b4', 'actual_pc': '800012b4', 'is_taken': True},

...
