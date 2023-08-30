import system_diagnostics
import benchmarking
import plotting
import utils
from settings import Settings

settings = Settings()

def main():
    # Ask user's choice
    choice = input("Do you want to run a new benchmark or load a saved one? (Enter 'run' or 'load'): ").lower()

    if choice == 'load':
        cpu_cores, _ = system_diagnostics.get_system_info()[:2]
        directory = "DEBUG_benchmark" if settings.debug else "RUNTIME_benchmark"
        saved_benchmarks = utils.list_saved_benchmarks(directory)

        if not saved_benchmarks:
            print("No benchmarks found. Running a new benchmark.")
            choice = 'run'
        else:
            print("List of saved benchmarks:")
            for i, name in enumerate(saved_benchmarks):
                print(f"{i + 1}. {name}")

            while True:
                benchmark_choice = input("Enter the number of the benchmark you want to load, or type the name of the csv: ")
                if benchmark_choice.isdigit():
                    benchmark_choice = int(benchmark_choice)
                    if 1 <= benchmark_choice <= len(saved_benchmarks):
                        filename = saved_benchmarks[benchmark_choice - 1]
                        break
                    else:
                        print(f"Invalid choice. Please choose a number between 1 and {len(saved_benchmarks)}.")
                else:
                    filename = benchmark_choice
                    if filename in saved_benchmarks:
                        break
                    else:
                        print("Invalid filename. Please choose from the list.")

            results_cpu, results_gpu = utils.load_csv(filename, directory)
            plotting.plotting(results_cpu, results_gpu, cpu_cores)
            return

    if choice == 'run':
        cpu_cores, sizes_to_test, _ = system_diagnostics.get_system_info()
        system_diagnostics.print_system_info()
        results_cpu, results_gpu = benchmarking.benchmark(cpu_cores, sizes_to_test)
        utils.save_csv(results_cpu, results_gpu, cpu_cores)
        plotting.plotting(results_cpu, results_gpu, cpu_cores)


if __name__ == "__main__":
    main()
