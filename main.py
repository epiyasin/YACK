import system_diagnostics
import benchmarking
import plotting
import utils
from settings import Settings

settings = Settings()

def main():
    choice = utils.get_user_choice()

    if choice == 'load':
        utils.handle_load_choice()
    elif choice == 'run':
        utils.handle_run_choice()
    else:
        print("Invalid choice. Please enter 'run' or 'load'.")

if __name__ == "__main__":
    main()
