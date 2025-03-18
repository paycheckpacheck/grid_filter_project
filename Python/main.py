import numpy as np
import cv2
import matplotlib.pyplot as plt


def compute_transfer_function(s_params, frequency):
    """
    Compute the transfer function from S-parameters at a given frequency.
    This is a placeholder for the actual computation based on the application.
    """
    # Example: simple gain calculation
    return np.abs(s_params) * np.exp(-1j * frequency)


def spatial_fft(transfer_function, grid_size=(25, 25)):
    """
    Compute the spatial FFT of the transfer function.
    """
    # Reshape the transfer function into the grid size
    tf_grid = transfer_function.reshape(grid_size)

    # Compute the FFT
    fft_result = np.fft.fft2(tf_grid)
    return np.fft.fftshift(fft_result)  # Shift zero frequency to center


def current_density_contour(fft_result, grid_size=(25, 25)):
    """
    Generate the current density contour from the FFT result.
    """
    # Compute magnitude of the FFT result
    magnitude = np.abs(fft_result)

    # Normalize the magnitude to fit between 0 and 255
    norm_magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Create a contour plot
    plt.figure(figsize=(8, 8))
    plt.contourf(norm_magnitude, levels=20, cmap='viridis')
    plt.colorbar(label='Current Density Magnitude')
    plt.title('Current Density Contour')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.show()


def main():
    # Example S-parameters (random complex values for demonstration)
    num_s_params = 25 * 25
    s_params = np.random.random(num_s_params) + 1j * np.random.random(num_s_params)

    # Frequency in Hz (example value)
    frequency = 1e9  # 1 GHz

    # Compute the transfer function
    transfer_function = compute_transfer_function(s_params, frequency)

    # Compute the spatial FFT
    fft_result = spatial_fft(transfer_function)

    # Generate the current density contour
    current_density_contour(fft_result)


if __name__ == "__main__":
    main()
