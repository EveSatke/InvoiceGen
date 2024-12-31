import asyncio
from setup import setup_dependencies

def main():
    # asyncio.run(invoice_generator.start())
    
    generator = setup_dependencies()
    generator.main_menu()

if __name__ == "__main__":
    main()
