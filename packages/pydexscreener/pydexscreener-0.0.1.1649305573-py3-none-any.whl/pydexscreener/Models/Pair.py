from typing import Optional
from pydantic import BaseModel

class Transaction(BaseModel):
  buys: int
  sells: int

class Transactions(BaseModel):
  m5: Transaction
  h1: Transaction
  h6: Transaction
  h24: Transaction

class Volume(BaseModel):
  m5: int
  h1: int
  h6: int
  h24: int

class Liquidity(BaseModel):
  usd: Optional[int]
  base: int
  quote: int

class Token(BaseModel):
  address: Optional[str]
  name: Optional[str]
  symbol: str

class Pair(BaseModel):
  chainId: str
  dexId: str
  url: str
  pairAddress: str
  baseToken: Token
  quoteToken: Token
  priceNative: str
  priceUsd: Optional[str]
  txns: Transactions
  volume: Volume
  priceChange: Volume
  liquidity: Optional[Liquidity]
  fdv: Optional[int]
  pairCreatedAt: Optional[int]