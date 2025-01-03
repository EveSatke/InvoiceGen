import asyncio
from setup import setup_dependencies

def main():
    # asyncio.run(menu_manager.start())
    
    generator = setup_dependencies()
    generator.main_menu()

if __name__ == "__main__":
    main()
