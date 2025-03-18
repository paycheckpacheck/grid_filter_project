import numpy as np
import fdtd
import matplotlib.pyplot as plt  # Import matplotlib for plotting

# Define simulation size (25x25 grid)
grid_size = (25, 25, 1)  # 2D grid in the xy-plane with depth 1

# Initialize the FDTD grid with the defined size
grid = fdtd.Grid(shape=grid_size, grid_spacing=1e-6)  # Grid spacing is 1 micron

# Material properties
# Copper (approximate values at GHz frequencies)
copper_permittivity = 1.0
copper_permeability = 1.0
# FR4
fr4_permittivity = 4.5
fr4_permeability = 1.0

# Conduction pattern: 1 = copper, 0 = FR4
#define your own pattern here
# Initialize all pixels as FR4
conduction_pattern = np.zeros((25, 25))

# random conduction pattern
conduction_pattern = np.random.choice([0, 1], size=(25, 25))


# Define a specific copper pattern (e.g., a straight line)
conduction_pattern[12, :] = 1  # A horizontal copper line at y=12

# Define the material at each point based on the conduction pattern
for x in range(25):
    for y in range(25):
        if conduction_pattern[x, y] == 1:
            # Copper pixel
            grid[x, y, 0] = fdtd.Object(permittivity=copper_permittivity)
        else:
            # FR4 pixel
            grid[x, y, 0] = fdtd.Object(permittivity=fr4_permittivity)


# Add a line source as the input signal
grid[5, :, 0] = fdtd.LineSource(period=15e-9, name="input_source")  # Line source at x=5

# Add a line detector to measure output at x=20
grid[20, :, 0] = fdtd.LineDetector(name="output_detector")  # Line detector at x=20

# Define the simulation duration
timesteps = 1000

# Run the simulation
grid.run(timesteps)

# Retrieve the results from the output detector
output_detector = grid.detectors[0]
output_signal = output_detector.E  # Electric field data

# Since output_signal may be multi-dimensional, average over the detector points
output_signal_mean = np.mean(output_signal, axis=1)  # Averaging over y-axis


plt.figure()

plt.plot(timesteps, output_signal_mean[:])

plt.show()

