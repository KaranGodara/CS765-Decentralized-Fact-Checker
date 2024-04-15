import matplotlib.pyplot as plt
import numpy as np

# Define N
N = 500

def plot_p_variance(file_number, txt, type):
    # Define q_array and p_array
    q_array = [10, 20, 30]
    p_array = [10, 30, 50, 70, 100]

    # Plot for each value of q
    for i in range(len(q_array)):
        q_value = q_array[i]
        # Create a plot
        plt.figure(figsize=(8, 6))

        # Plot for each value of p
        for j in range(len(p_array)):
            if file_number[i*len(p_array) + j] != -1 :
                p_value = p_array[j]
                # Initialize arrays to store x and y values for the plot
                x_values = []
                y_values = []

                # Read file
                filename = f"plots/q_{q_value}_p_{p_value}_r_10_Tsim_120000_n_{N}/trust_{file_number[i*len(p_array) + j]}"
                with open(filename, 'r') as file:
                    lines = file.readlines()
                    # Extract x and y values from lines
                    for line in lines:
                        if "News Count :" in line:
                            x_values.append(int((line.split(',')[0]).split(':')[1]))
                            y_values.append(int((line.split(',')[1]).split(':')[1]))

                # Plot the data for the current (q_value, p_value)
                plt.plot(x_values, y_values, label=f'p={p_value/100}')

        # Add labels and legend
        plt.xlabel('News Count')
        plt.ylabel('Trust Value')
        plt.title(f"q = {q_value/100}, N = {N}")
        plt.legend()

        # Restricting the displayed points on x-axis
        plt.xticks(np.arange(min(x_values), max(x_values) + 1, 1000))
        plt.ylim(0,100)

        # Adding caption
        plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
        
        # Saving the plot 
        plt.savefig(f"graphs/PQVAR_q_{q_value}_N_{N}_type_{type}.png")

def plot_pqn_variance(p, q, N, H90_file_number = -1, H70_file_number = -1, M_file_number = -1):
    plt.figure(figsize=(8, 6))

    ################ Plotting H90 first ####################
    if H90_file_number != -1:
        # Initialize arrays to store x and y values for the plot
        x_values = []
        y_values = []

        # Read file
        filename = f"plots/q_{q}_p_{p}_r_10_Tsim_120000_n_{N}/trust_{H90_file_number}"
        with open(filename, 'r') as file:
            lines = file.readlines()
            # Extract x and y values from lines
            for line in lines:
                if "News Count :" in line:
                    x_values.append(int((line.split(',')[0]).split(':')[1]))
                    y_values.append(int((line.split(',')[1]).split(':')[1]))

        # Plot the data for the current (q_value, p_value)
        plt.plot(x_values, y_values, label=f'Honest 90%')

    #####################################################

    ################ Plotting H70 second ####################
    # Initialize arrays to store x and y values for the plot
    if H70_file_number != -1:
        x_values = []
        y_values = []

        # Read file
        filename = f"plots/q_{q}_p_{p}_r_10_Tsim_120000_n_{N}/trust_{H70_file_number}"
        with open(filename, 'r') as file:
            lines = file.readlines()
            # Extract x and y values from lines
            for line in lines:
                if "News Count :" in line:
                    x_values.append(int((line.split(',')[0]).split(':')[1]))
                    y_values.append(int((line.split(',')[1]).split(':')[1]))

        # Plot the data for the current (q_value, p_value)
        plt.plot(x_values, y_values, label=f'Honest 70%')

    #####################################################

    ################ Plotting Malicious last ####################
    if M_file_number != -1:
        # Initialize arrays to store x and y values for the plot
        x_values = []
        y_values = []

        # Read file
        filename = f"plots/q_{q}_p_{p}_r_10_Tsim_120000_n_{N}/trust_{M_file_number}"
        with open(filename, 'r') as file:
            lines = file.readlines()
            # Extract x and y values from lines
            for line in lines:
                if "News Count :" in line:
                    x_values.append(int((line.split(',')[0]).split(':')[1]))
                    y_values.append(int((line.split(',')[1]).split(':')[1]))

        # Plot the data for the current (q_value, p_value)
        plt.plot(x_values, y_values, label=f'Malicious')

    #####################################################

    # Add labels and legend
    plt.xlabel('News Count')
    plt.ylabel('Trust Value')
    plt.title(f"p = {p/100}, q = {q/100}, N = {N}")
    plt.legend()

    # Restricting the displayed points on x-axis
    plt.xticks(np.arange(min(x_values), max(x_values) + 1, 1000))
    plt.ylim(0,100)

    # Adding caption
    # plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
    
    # Saving the plot 
    plt.savefig(f"graphs/IDV_p_{p}_q_{q}_N_{N}.png")


def plot_N_variance(h90, h70, m, N_value):
    p = 60
    q = 30
    # Plot for each value of q

    # Create a plot
    plt.figure(figsize=(8, 6))

    ############### Plotting Honest with 90% ############################
    x_values = []
    y_values = []

    # Read file
    filename = f"plots/q_{q}_p_{p}_r_10_Tsim_120000_n_{N_value}/trust_{h90}"
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Extract x and y values from lines
        for line in lines:
            if "News Count :" in line:
                x_values.append(int((line.split(',')[0]).split(':')[1]))
                y_values.append(int((line.split(',')[1]).split(':')[1]))

    # Plot the data for the current (q_value, p_value)
    plt.plot(x_values, y_values, label=f'Honest with 90%')
    ###################################################################

    ############### Plotting Honest with 70% ############################
    x_values = []
    y_values = []

    # Read file
    filename = f"plots/q_{q}_p_{p}_r_10_Tsim_120000_n_{N_value}/trust_{h70}"
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Extract x and y values from lines
        for line in lines:
            if "News Count :" in line:
                x_values.append(int((line.split(',')[0]).split(':')[1]))
                y_values.append(int((line.split(',')[1]).split(':')[1]))

    # Plot the data for the current (q_value, p_value)
    plt.plot(x_values, y_values, label=f'Honest with 70%')
    ###################################################################

    ############### Plotting Malicious ############################
    x_values = []
    y_values = []

    # Read file
    filename = f"plots/q_{q}_p_{p}_r_10_Tsim_120000_n_{N_value}/trust_{m}"
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Extract x and y values from lines
        for line in lines:
            if "News Count :" in line:
                x_values.append(int((line.split(',')[0]).split(':')[1]))
                y_values.append(int((line.split(',')[1]).split(':')[1]))

    # Plot the data for the current (q_value, p_value)
    plt.plot(x_values, y_values, label=f'Malicious')
    ###################################################################


    # Add labels and legend
    plt.xlabel('News Count')
    plt.ylabel('Trust Value')
    plt.title(f"Variation on N = {N_value}, q = {q/100}, p = {p/100}")
    plt.legend()

    # Restricting the displayed points on x-axis
    plt.xticks(np.arange(min(x_values), max(x_values) + 1, 1000))
    plt.ylim(0,100)
    
    # Saving the plot 
    plt.savefig(f"graphs/NVAR_p_{p}_q_{q}_N_{N_value}.png")

def plot_Mal(h90, h70, m, N_value, mnum):
    p = 60
    q = 30
    # Plot for each value of q

    # Create a plot
    plt.figure(figsize=(8, 6))

    ############### Plotting Honest with 90% ############################
    x_values = []
    y_values = []

    # Read file
    filename = f"plots/MAL{mnum}_q_{q}_p_{p}_r_10_Tsim_120000_n_{N_value}/trust_{h90}"
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Extract x and y values from lines
        for line in lines:
            if "News Count :" in line:
                x_values.append(int((line.split(',')[0]).split(':')[1]))
                y_values.append(int((line.split(',')[1]).split(':')[1]))

    # Plot the data for the current (q_value, p_value)
    plt.plot(x_values, y_values, label=f'Honest with 90%')
    ###################################################################

    ############### Plotting Honest with 70% ############################
    x_values = []
    y_values = []

    # Read file
    filename = f"plots/MAL{mnum}_q_{q}_p_{p}_r_10_Tsim_120000_n_{N_value}/trust_{h70}"
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Extract x and y values from lines
        for line in lines:
            if "News Count :" in line:
                x_values.append(int((line.split(',')[0]).split(':')[1]))
                y_values.append(int((line.split(',')[1]).split(':')[1]))

    # Plot the data for the current (q_value, p_value)
    plt.plot(x_values, y_values, label=f'Honest with 70%')
    ###################################################################

    ############### Plotting Malicious ############################
    x_values = []
    y_values = []

    # Read file
    filename = f"plots/MAL{mnum}_q_{q}_p_{p}_r_10_Tsim_120000_n_{N_value}/trust_{m}"
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Extract x and y values from lines
        for line in lines:
            if "News Count :" in line:
                x_values.append(int((line.split(',')[0]).split(':')[1]))
                y_values.append(int((line.split(',')[1]).split(':')[1]))

    # Plot the data for the current (q_value, p_value)
    plt.plot(x_values, y_values, label=f'Malicious')
    ###################################################################


    # Add labels and legend
    plt.xlabel('News Count')
    plt.ylabel('Trust Value')
    plt.title(f"Variation on N = {N_value}, q = {q/100}, p = {p/100}")
    plt.legend()

    # Restricting the displayed points on x-axis
    plt.xticks(np.arange(min(x_values), max(x_values) + 1, 1000))
    plt.ylim(0,100)
    
    # Saving the plot 
    plt.savefig(f"graphs/M{mnum}_p_{p}_q_{q}_N_{N_value}.png")

def plot_Mal3(h90, h70, m, hf90, hf70, N_value):
    p = 60
    q = 30
    # Plot for each value of q

    # Create a plot
    plt.figure(figsize=(8, 6))

    ############### Plotting Honest with 90% ############################
    x_values = []
    y_values = []

    # Read file
    filename = f"plots/MAL3_q_{q}_p_{p}_r_10_Tsim_120000_n_{N_value}/trust_{h90}"
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Extract x and y values from lines
        for line in lines:
            if "News Count :" in line:
                x_values.append(int((line.split(',')[0]).split(':')[1]))
                y_values.append(int((line.split(',')[1]).split(':')[1]))

    # Plot the data for the current (q_value, p_value)
    plt.plot(x_values, y_values, label=f'Honest with 90%')
    ###################################################################

    ############### Plotting Honest with 70% ############################
    x_values = []
    y_values = []

    # Read file
    filename = f"plots/MAL3_q_{q}_p_{p}_r_10_Tsim_120000_n_{N_value}/trust_{h70}"
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Extract x and y values from lines
        for line in lines:
            if "News Count :" in line:
                x_values.append(int((line.split(',')[0]).split(':')[1]))
                y_values.append(int((line.split(',')[1]).split(':')[1]))

    # Plot the data for the current (q_value, p_value)
    plt.plot(x_values, y_values, label=f'Honest with 70%')
    ###################################################################

    ############### Plotting Malicious ############################
    x_values = []
    y_values = []

    # Read file
    filename = f"plots/MAL3_q_{q}_p_{p}_r_10_Tsim_120000_n_{N_value}/trust_{m}"
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Extract x and y values from lines
        for line in lines:
            if "News Count :" in line:
                x_values.append(int((line.split(',')[0]).split(':')[1]))
                y_values.append(int((line.split(',')[1]).split(':')[1]))

    # Plot the data for the current (q_value, p_value)
    plt.plot(x_values, y_values, label=f'Malicious')
    ###################################################################

    ############### Plotting HFall_90 ############################
    x_values = []
    y_values = []

    # Read file
    filename = f"plots/MAL3_q_{q}_p_{p}_r_10_Tsim_120000_n_{N_value}/trust_{hf90}"
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Extract x and y values from lines
        for line in lines:
            if "News Count :" in line:
                x_values.append(int((line.split(',')[0]).split(':')[1]))
                y_values.append(int((line.split(',')[1]).split(':')[1]))

    # Plot the data for the current (q_value, p_value)
    plt.plot(x_values, y_values, label=f'Honest 90% turned malicious')
    ###################################################################

    ############### Plotting HFall_70 ############################
    x_values = []
    y_values = []

    # Read file
    filename = f"plots/MAL3_q_{q}_p_{p}_r_10_Tsim_120000_n_{N_value}/trust_{hf70}"
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Extract x and y values from lines
        for line in lines:
            if "News Count :" in line:
                x_values.append(int((line.split(',')[0]).split(':')[1]))
                y_values.append(int((line.split(',')[1]).split(':')[1]))

    # Plot the data for the current (q_value, p_value)
    plt.plot(x_values, y_values, label=f'Honest 70% turned malicious')
    ###################################################################


    # Add labels and legend
    plt.xlabel('News Count')
    plt.ylabel('Trust Value')
    plt.title(f"Variation on N = {N_value}, q = {q/100}, p = {p/100}")
    plt.legend()

    # Restricting the displayed points on x-axis
    plt.xticks(np.arange(min(x_values), max(x_values) + 1, 1000))
    plt.ylim(0,100)
    
    # Saving the plot 
    plt.savefig(f"graphs/M3_p_{p}_q_{q}_N_{N_value}.png")



def main():
    ############ FOR P variance prints ###################
    # for honest with 90% correctness
    honest_90 = [8,1,2,1,0, 5,9,1,0,0, 2,9,0,2,1]
    plot_p_variance(honest_90, "For Honest Voter with 90% correctness", "H90")

    # for honest with 70% correctness
    honest_70 = [0,0,0,5,-1, 0,1,0,3,-1, 0,0,3,0,-1]
    plot_p_variance(honest_70, "For Honest Voter with 70% correctness", "H70")

    # for malicious
    malicious = [7,3,1,0,1, 15,0,5,1,23, 1,3,1,1,0]
    plot_p_variance(malicious, "For Malicious Voter ", "M")

    ############ FOR individual prints ###################
    # for honest with 90% correctness
    # plot_pqn_variance(p = 100, q = 40, N = 500, H90_file_number = 1, H70_file_number = -1, M_file_number = 0) 

    ############ FOR N Value prints ###################
    # N_array = [10, 100, 1000, 5000]
    # H90_file_number = [1, 5, 0, 0]
    # H70_file_number = [4, 0, 2, 4]
    # M_file_number = [0, 2, 5, 12]
    # for i, N_value in enumerate(N_array):
    #     plot_N_variance(H90_file_number[i], H70_file_number[i], M_file_number[i], N_value)

    ############# For Mal 2 with varying N ##############
    # N_array = [10, 100, 500, 1000] ## Add 5000 later
    # H90_file_number = [0, 3, 2, 5]
    # H70_file_number = [2, 1, 7, 0]
    # M_file_number = [3, 2, 16, 2]
    # for i, N_value in enumerate(N_array):
    #     plot_Mal(H90_file_number[i], H70_file_number[i], M_file_number[i], N_value, 2)

    ############# For Mal 3 with varying N ##############
    # N_value = 500
    # H90_file_number = 495
    # H70_file_number = 499
    # M_file_number = 6
    # H90_Fall = 0
    # H70_Fall = 4
    # plot_Mal3(H90_file_number, H70_file_number, M_file_number, H90_Fall, H70_Fall, N_value)

if __name__ == "__main__":
    main()