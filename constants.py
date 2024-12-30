from colorama import Fore, Style

# Title
INVOICE_GENERATOR_TITLE = f"\n{Fore.CYAN}==Invoice Generator=={Fore.RESET}"

# Header and Divider
SUPPLIER_MANAGER_HEADER = f"{Fore.CYAN}Supplier Manager{Fore.RESET}"
CREATE_SUPPLIER_HEADER = f"{Fore.CYAN}Create Supplier{Fore.RESET}"
DIVIDER = f"{Fore.CYAN}--------------------------------{Fore.RESET}"

# Menu Text Constants
MENU_PROMPT = f"{Fore.YELLOW}\nChoose an option 1-{{max_option}}: {Fore.RESET}"
INVALID_OPTION_MESSAGE = f"{Fore.RED}Invalid option. Please enter a number between 1 and {{max_option}}.{Fore.RESET}"
INPUT_MUST_BE_NUMBER = f"{Fore.RED}Input must be a number. Please try again.{Fore.RESET}"
UNEXPECTED_ERROR = f"{Fore.RED}An unexpected error occurred: {{error}}{Fore.RESET}"
SUPPLIER_CREATED_MESSAGE = f"{Fore.GREEN}\nSupplier created successfully!{Fore.RESET}"
SUPPLIER_NOT_SAVED_MESSAGE = f"{Fore.RED}\nSupplier not saved. Operation cancelled.{Fore.RESET}"

 