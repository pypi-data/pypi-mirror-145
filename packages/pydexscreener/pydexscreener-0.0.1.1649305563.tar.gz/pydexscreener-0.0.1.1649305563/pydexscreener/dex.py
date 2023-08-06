from typing import List, Optional
import httpx
from pydantic import BaseModel
from pydexscreener.Models.Pair import Pair


class PairsResponse(BaseModel):
    schemaVersion: str
    pair: Pair


class TokensResponse(BaseModel):
    schemaVersion: str
    pairs: Optional[List[Pair]]


class BaseClient:
    url: str
    client: httpx.Client

    def __init__(self, url: str):
        self.url = url
        self.client = httpx.Client()

    def __del__(self):
        self.client.close()


class DexScreenerClient(BaseClient):
    chainId: str
    pairAddress: str

    def __init__(self):
        super().__init__("https://api.dexscreener.io/latest/dex")

    def pairs(self, chainId: str, pairAddress: str) -> PairsResponse:
        r = self.client.get(f"{self.url}/pairs/{chainId}/{pairAddress}")
        return PairsResponse(**r.json())

    def tokens(self, tokenAddress: str) -> TokensResponse:
        r = self.client.get(f"{self.url}/tokens/{tokenAddress}")
        return TokensResponse(**r.json())

    def search(self, query):
        pass
