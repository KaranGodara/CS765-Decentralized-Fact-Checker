# CS765-Decentralized-Fact-Checker

## Team Members 
| Name | Roll Number |
| --- | --- |
|Isha Arora | 210050070|
|Karan Godara | 210050082|

## Running instructions
- The simulator and grapher are written in Python3

### Simulator
- The simulator is run by main.py
- To see the usage of the simulator, run the following command:
```python3 main.py --help```
- The above command will display the following:
```
usage: python3 run.py [-h] [--n N] [--q q] [--p p] [--r r] [--T_sim T_SIM] [--data OUTPUT_DIR]

Simulation of a Decentralized Fact Checker (DApp)

options:
  -h, --help                  show this help message and exit
  --n N                       Number of voters in the DApp
  --p p                       Fraction of honest voters with 90% correctness probability
  --q q                       Fraction of malicious voters 
  --r r                       Average number of news coming to DApp in a day
  --T_sim T_SIM               Simulation time (in s)
  --data OUTPUT_DIR           Output directory
```
- Options are given default values, so if you want to run the simulator with the default values, you can simply run:
```python3 run.py```
- The default values are:
    - n: 20
    - q: 0.3
    - p: 0.6
    - r: 20
    - T_sim: 1000000
    - data: data
- The output of the simulator will be stored in the output directory. The following files will be generated:
    - DApp: Overall info of the simulation setup is written in it.
    - trust_{x}: Contains info about nature of each voter and the trustworthiness of it after each news processed by the DApp. Here 0<=x<n.
### Grapher
- The graphs for analysis of simulation is done by grapher.py
- Note, the grapher require manual code changes to plot new graph for new data. Therefore, if wanting to use it, appropriately do these changes.
- To run the grapher use the command:
```python3 grapher.py``` 

## Directory Structure
- This directory contains the following files:
    - [dapp.py](dapp.py): The class DApp is the contract with all the code
    - [link.py](link.py): The link class connects class objects of DApp and one voter, useful for communication between them
    - [main.py](main.py): The code that intializes the simulator and runs the simulation and prints final report post simulation
    - [simulator.py](simulator.py): The simulator class
    - [trust.py](trust.py): For each voter, this class have info/functions required to calculate trustworthiness of the voter
    - [voter.py](voter.py): The voter class denoting the voter for the DApp
    - [grapher.py](grapher.py): The helper program to plot graphs for analysis
    - [pseudo-code.sol](pseudo-code.sol): The file contains pseudo code of the DApp in the solidity language
    - [Report.pdf](Report.pdf): The report of this assignment
    - [data](results): This directory contains the results of the simulation and analysis that we have used in the report
    - [graphs](graphs): This directory contains all the plots used in the report, these plots were made using grapher.py
 
## Libraries used and their versions
- matplotlib (3.8.0)
- numpy (1.26.1)
- simpy (4.1.1)
