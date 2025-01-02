from colorama import Fore, Style

# Title
INVOICE_GENERATOR_TITLE = f"\n{Fore.CYAN}==Invoice Generator=={Fore.RESET}"

# Header and Divider
SUPPLIER_MANAGER_HEADER = f"{Fore.CYAN}Supplier manager{Fore.RESET}"
SEARCH_SUPPLIER_HEADER = f"{Fore.CYAN}Search supplier{Fore.RESET}"
SEARCH_RESULTS_HEADER = f"{Fore.CYAN}Search results{Fore.RESET}"
CREATE_SUPPLIER_HEADER = f"{Fore.CYAN}Create supplier{Fore.RESET}"
SELECT_SUPPLIER_HEADER = f"{Fore.CYAN}Selected supplier{Fore.RESET}"
SUPPLIER_LIST_HEADER = f"{Fore.CYAN}Supplier list{Fore.RESET}"
DELETE_SUPPLIER_HEADER = f"{Fore.CYAN}Delete supplier{Fore.RESET}"
DIVIDER = f"{Fore.CYAN}--------------------------------{Fore.RESET}"

# Menu Text Constants
MENU_PROMPT = f"{Fore.YELLOW}\nChoose an option 1-{{max_option}}: {Fore.RESET}"
MENU_PROMPT_WITH_EXIT = f"{Fore.YELLOW}\nChoose an option {{min_value}}-{{max_option}} or type 'q' to exit: {Fore.RESET}"
INPUT_BETWEEN_VALUES = f"Input must be between {{min_value}} and {{max_value}}. Please try again."
INPUT_MUST_BE_NUMBER = f"{Fore.RED}Input must be a number. Please try again.{Fore.RESET}"
INPUT_MUST_BE_FLOAT = f"{Fore.RED}Input must be a float. Please try again.{Fore.RESET}"
INPUT_NOT_EMPTY = f"{Fore.RED}Input cannot be empty. Please try again.{Fore.RESET}"
UNEXPECTED_ERROR = f"{Fore.RED}An unexpected error occurred: {{error}}{Fore.RESET}"
SUPPLIER_CREATED_MESSAGE = f"{Fore.GREEN}\nSupplier created successfully!{Fore.RESET}"
SUPPLIER_NOT_SAVED_MESSAGE = f"{Fore.RED}\nSupplier not saved. Operation cancelled.{Fore.RESET}"
SUPPLIER_ADDITIONAL_INFO = f"{Fore.YELLOW}\nAdditional Information:{Fore.RESET}"
SUPPLIER_DELETED_MESSAGE = f"{Fore.GREEN}\nSupplier deleted successfully!{Fore.RESET}"
SUPPLIER_NOT_DELETED_MESSAGE = f"{Fore.RED}\nSupplier not deleted. Operation cancelled.{Fore.RESET}"

 