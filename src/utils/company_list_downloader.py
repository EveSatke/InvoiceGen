import aiohttp
import os
from colorama import Fore

class CompanyListDownloader:
    def __init__(self, url, filename):
        self.url = url
        self.filename = os.path.join('src', filename)

    async def download(self):
        try:
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)

            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    with open(self.filename, "wb") as file:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            file.write(chunk)

            print(f"{Fore.GREEN}File downloaded successfully and saved as {self.filename}{Fore.RESET}")
        except aiohttp.ClientError as e:
            print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        except IOError as e:
            print(f"{Fore.RED}An error occurred while writing the file: {e}{Fore.RESET}")
    