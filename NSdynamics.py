import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Parameters
g_values = [0.03, 0.07]  # Growth rates (3%, 7%)
c_values = [0.01, 0.05]  # Consumption rates (1%, 5%)
rho_values = [0.3, 0.5, 0.7]   # Population proportions of N (30%, 50%, 70%)
T = 200   # Number of time steps

# Initial conditions
wN_0 = 1.1   # Initial per capita wealth in country N
wS_0 = 0.9   # Initial per capita wealth in country S

# Number of total combinations (2 * 2 * 3 = 12)
num_graphs = len(g_values) * len(c_values) * len(rho_values)
print(f"Total number of graphs to be generated: {num_graphs}")

# Generate graphs for each combination of g, c, and rho
for g in g_values:
    for c in c_values:
        for rho in rho_values:
            # Initialize arrays to store values over time
            wN = np.zeros(T)
            wS = np.zeros(T)

            # Set initial conditions
            wN[0] = wN_0
            wS[0] = wS_0

            # Simulation
            for t in range(T-1):
                # Update per capita wealth for country N and S
                wN[t+1] = (1 + g) * wN[t] - c * (rho * wN[t] + (1 - rho) * wS[t])
                wS[t+1] = (1 + g) * wS[t] - c * (rho * wN[t] + (1 - rho) * wS[t])

            # Plotting the results (excluding World Per Capita Wealth)
            plt.plot(wN, label="$w^N$", linestyle="-")
            plt.plot(wS, label="$w^S$", linestyle="--")

            # Labels for the axes (just t for time and w for wealth)
            plt.xlabel("t")
            plt.ylabel("w")

            # Create custom legend elements
            line_wN = Line2D([0], [0], color='blue', linestyle='-', label="$w^N$")
            line_wS = Line2D([0], [0], color='orange', linestyle='--', label="$w^S$")

            # Add g, c, and rho values to the legend
            legend_text = f"$g={int(g*100)}\%$, $c={int(c*100)}\%$, $\\rho={int(rho*100)}\%$"

            # Combine the line labels and parameter values in the legend
            plt.legend(handles=[line_wN, line_wS, Line2D([0], [0], color='white', label=legend_text)],
                       loc="upper left", fontsize="small", fancybox=True, shadow=True)

            # Reduce clutter: No title
            plt.grid(True)

            # Show the plot
            plt.show()
