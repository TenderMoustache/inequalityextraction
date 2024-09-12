import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Parameters
n = 5000  # Number of initial agents in each category
timesteps_initial = 25  # Number of initial time steps before recombining
timesteps_final = 25  # Number of additional time steps after recombining (total 200)
beta_values = [0.3, 0.5, 0.7]  # Different values of beta for different speeds of integration
epsilon_C_std = 1.0  # Standard deviation of noise for W^C
epsilon_S_std = 1.0  # Standard deviation of noise for W^S
epsilon_W_std = 1.0  # Standard deviation of noise for W^W

# Initialize W^C and W^S randomly between 0 and 100
initial_W_C = np.random.rand(n) * 100  # Initial values for W^C between 0 and 100
initial_W_S = np.random.rand(n) * 100  # Initial values for W^S between 0 and 100

# Apply % extraction of each agent's W^S and add to W^C
E_i = 0.25 * initial_W_S  # Extract % of each agent's initial W^S
initial_W_C += E_i  # Add extracted amount to W^C
initial_W_S -= E_i  # Subtract extracted amount from W^S

# Function to simulate the initial system (W^C and W^S)
def simulate_initial(beta_C, beta_S, timesteps):
    W_C = np.zeros((n, timesteps))
    W_S = np.zeros((n, timesteps))
    
    # Set initial values
    W_C[:, 0] = initial_W_C
    W_S[:, 0] = initial_W_S
    
    avg_W_C = np.zeros(timesteps)
    avg_W_S = np.zeros(timesteps)
    
    for t in range(timesteps - 1):
        avg_W_C[t] = np.mean(W_C[:, t])
        avg_W_S[t] = np.mean(W_S[:, t])
        
        # Update each agent's W^C and W^S
        epsilon_C = np.random.normal(0, epsilon_C_std, n)
        epsilon_S = np.random.normal(0, epsilon_S_std, n)
        
        W_C[:, t+1] = beta_C * W_C[:, t] + (1 - beta_C) * avg_W_C[t] + epsilon_C
        W_S[:, t+1] = beta_S * W_S[:, t] + (1 - beta_S) * avg_W_S[t] + epsilon_S

    avg_W_C[-1] = np.mean(W_C[:, -1])
    avg_W_S[-1] = np.mean(W_S[:, -1])
    
    return W_C, W_S, avg_W_C, avg_W_S

# Function to simulate the combined system (W^W), keeping track of the original groups
def simulate_combined(beta_W, timesteps, W_W_initial):
    W_W = np.zeros((2*n, timesteps))  # Now we have 10000 agents
    
    # Set initial values
    W_W[:, 0] = W_W_initial
    
    avg_W_W_C = np.zeros(timesteps)  # Average wealth for agents originally from W^C
    avg_W_W_S = np.zeros(timesteps)  # Average wealth for agents originally from W^S
    
    for t in range(timesteps - 1):
        # Compute averages for the two groups
        avg_W_W_C[t] = np.mean(W_W[:n, t])
        avg_W_W_S[t] = np.mean(W_W[n:, t])
        
        # Update each agent's W^W
        epsilon_W = np.random.normal(0, epsilon_W_std, 2*n)
        
        W_W[:, t+1] = beta_W * W_W[:, t] + (1 - beta_W) * np.mean(W_W[:, t]) + epsilon_W

    # Compute final averages
    avg_W_W_C[-1] = np.mean(W_W[:n, -1])
    avg_W_W_S[-1] = np.mean(W_W[n:, -1])
    
    return W_W, avg_W_W_C, avg_W_W_S

# Color scheme
colors = ['b', 'g', 'r']

# Run simulation for each beta value and print the first period when avg_W_S >= avg_W_C
plt.figure(figsize=(12, 6))

for i, beta in enumerate(beta_values):
    # Simulate the initial system for initial periods
    W_C_final, W_S_final, avg_W_C_initial, avg_W_S_initial = simulate_initial(beta, beta, timesteps_initial)

    # Combine W^C and W^S into W^W , renumbering to 10000 agents
    W_W_initial = np.concatenate([W_C_final[:, -1], W_S_final[:, -1]])

    # Simulate the combined system for additional periods
    W_W_final, avg_W_W_C_final, avg_W_W_S_final = simulate_combined(beta, timesteps_final, W_W_initial)

    # Combine the first and last time steps
    total_avg_W_C = np.concatenate([avg_W_C_initial, avg_W_W_C_final])
    total_avg_W_S = np.concatenate([avg_W_S_initial, avg_W_W_S_final])

    # Find the first period when average W^S >= W^C and mark it
    first_period = None
    for t in range(len(total_avg_W_S)):
        if total_avg_W_S[t] >= total_avg_W_C[t]:
            first_period = t
            print(f"For beta = {beta}, first period where avg W^S >= avg W^C is: {t}")
            break

    # Plot the results using the same color scheme for W^C and W^S but different line styles
    plt.plot(total_avg_W_C, color=colors[i], linestyle='-', label=f'$\\beta = {beta}$ (W^C)')
    plt.plot(total_avg_W_S, color=colors[i], linestyle='--', label=f'$\\beta = {beta}$ (W^S)')

    # Mark the first period where W^S >= W^C with a marker
    if first_period is not None:
        plt.plot(first_period, total_avg_W_S[first_period], 'o', color=colors[i], markersize=8, label=f'Marker $\\beta = {beta}$')


        
# Create custom legend
custom_lines = [Line2D([0], [0], color='k', linestyle='-', lw=2, label=r'$W^C$'),
                Line2D([0], [0], color='k', linestyle='--', lw=2, label=r'$W^S$')]
plt.legend(handles=custom_lines + [Line2D([0], [0], color=colors[i], lw=2, label=f'$\\beta = {beta_values[i]}$') for i in range(len(beta_values))], loc='center left', fontsize='medium', fancybox=True, shadow=True)

plt.title(f'Evolution of Average Wealth Over Time (25% Extraction, Different $\\beta$ Values)')
plt.xlabel('Time Steps')
plt.ylabel('Average Wealth')
plt.grid(True)
plt.show()
