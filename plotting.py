import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from settings import Settings

settings = Settings()

def toggle_scale(event, axes):
    current_xscale = axes[0].get_xscale()
    new_scale = "log" if current_xscale == "linear" else "linear"
    for ax in axes:
        ax.set_xscale(new_scale)
        ax.set_yscale(new_scale)
    plt.draw()

def plotting(results_cpu, results_gpu, cpu_cores):
    # Plotting
    matrix_sizes = sorted(results_cpu.keys())

    fig = plt.figure(figsize=settings.figure_size)
    ax = fig.add_axes([0.1, 0.2, 0.8, 0.7])  # [left, bottom, width, height] 

    # Plot CPU results
    for j, cores in enumerate(cpu_cores):
        times_for_cores = [np.mean(results_cpu[size][j]) for size in matrix_sizes]
        times_min = [np.min(results_cpu[size][j]) for size in matrix_sizes]
        times_max = [np.max(results_cpu[size][j]) for size in matrix_sizes]
        
        yerr = [times_for_cores[i] - times_min[i] for i in range(len(times_for_cores))]
        ax.errorbar(matrix_sizes, times_for_cores, yerr=yerr, label=f"CPU ({cores} cores)", marker='o')

    # Plot GPU results
    gpu_times = [np.mean(results_gpu[size]) for size in matrix_sizes]
    gpu_times_min = [np.min(results_gpu[size]) for size in matrix_sizes]
    gpu_times_max = [np.max(results_gpu[size]) for size in matrix_sizes]
    
    yerr = [gpu_times[i] - gpu_times_min[i] for i in range(len(gpu_times))]
    ax.errorbar(matrix_sizes, gpu_times, yerr=yerr, label="GPU", marker='x', color='black')

    ax.set_xlabel("Matrix Size")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("Matrix Multiplication Time")
    ax.legend()
    ax.grid(True)

    # Add the toggle button
    ax_button = plt.axes([0.35, 0.05, 0.3, 0.05])  # x-position, y-position, width, height
    button = Button(ax_button, 'Toggle Scale')
    button.on_clicked(lambda event: toggle_scale(event, [ax]))

    plt.show()
