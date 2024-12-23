import aiohttp

class CompanyListDownloader:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename

    async def download(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    with open(self.filename, "wb") as file:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            file.write(chunk)

            print(f"File downloaded successfully and saved as {self.filename}")
        except aiohttp.ClientError as e:
            print(f"An error occurred: {e}")
    