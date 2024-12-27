import asyncio
import invoice_generator


def main():
    asyncio.run(invoice_generator.start())

if __name__ == "__main__":
    main()
