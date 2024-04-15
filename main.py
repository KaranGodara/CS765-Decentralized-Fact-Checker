import argparse
import simpy
import os

from simulator import Simulator

def main():
    # Creating ArgumentParser object
    parser = argparse.ArgumentParser(description='Simulation of DApp trustworthiness calculation')

    # Adding arguments
    parser.add_argument('--n', type=int, default=20, help='Number of voters in the DApp')
    parser.add_argument('--q', type=float, default=0.2, help='Fraction of malicious voters')
    parser.add_argument('--p', type=float, default=0.8, help='Fraction of honest voters with 90% correctness probability')
    parser.add_argument('--r', type=int, default=20, help='Average number of news coming to DApp in a day')
    parser.add_argument('--data', type=str, default="data", help='Output directory')
    parser.add_argument('--T_sim', type=int, default=100000, help='Simulation time (in s)')


    # Parse the command-line arguments
    args = parser.parse_args()

    env = simpy.Environment()

    # Simulating the DApp
    sim = Simulator(args.r, args.n, args.q, args.p, args.data, env)
    
    # Setting up the environment for simulation
    sim.setup_env()

    # Start the simulation
    print("Simulation begins...")
    sim.start_simulation()

    # Starting simulation
    env.run(until=args.T_sim)

    print("Simulation finished")

    # Creating the directories in the path if not present already
    os.makedirs(os.path.dirname(f"{args.data}/DApp"), exist_ok=True)

     # Writing the trustworthiness to the file
    with open(f"{args.data}/DApp", 'w') as file:
        file.write(f"Total News : {sim.DApp.num_news}\n")
        file.write(f"Fake News : {sim.DApp.fake_news}\n")
        file.write(f"Real News : {sim.DApp.real_news}\n")

        file.write("\nVoter Stats\n")
        for id in range(sim.N):
            file.write(f"For Voter : {id}\n")

            if(sim.voters[id].honest == 1) : 
                file.write(f"\tType : Honest\n")
            else:
                file.write(f"\tType : Malicious\n")

            file.write(f"\tProbability of correctness : {sim.voters[id].correct_prob}\n")

            file.write(f"\tCorrect Votes : {sim.DApp.trustworthiness[id].num_correct}\n")
            file.write(f"\tIncorrect Votes : {sim.DApp.trustworthiness[id].num_incorrect}\n")
            file.write(f"\tTruthworthiness : {sim.DApp.trustworthiness[id].trustworthiness}\n")
            file.write("\n")

if __name__ == "__main__":
    main()