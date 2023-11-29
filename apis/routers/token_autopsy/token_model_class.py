from pydantic import BaseModel
from typing import List, Dict, Optional


class TokenInfo(BaseModel):
   anti_whale_modifiable: Optional[str] = None
   buy_tax: Optional[str] = None
   can_take_back_ownership: Optional[str] = None
   cannot_buy: Optional[str] = None
   cannot_sell_all: Optional[str] = None
   creator_address: Optional[str] = None
   creator_balance: Optional[str] = None
   creator_percent: Optional[str] = None
   dex: Optional[List[Dict]] = None
   external_call: Optional[str] = None
   hidden_owner: Optional[str] = None
   holder_count: Optional[str] = None
   holders: Optional[List[Dict]] = None
   honeypot_with_same_creator: Optional[str] = None
   is_airdrop_scam: Optional[str] = None
   is_anti_whale: Optional[str] = None
   is_blacklisted: Optional[str] = None
   is_honeypot: Optional[str] = None
   is_in_dex: Optional[str] = None
   is_mintable: Optional[str] = None
   is_open_source: Optional[str] = None
   is_proxy: Optional[str] = None
   is_true_token: Optional[str] = None
   is_whitelisted: Optional[str] = None
   lp_holder_count: Optional[str] = None
   lp_holders: Optional[List[Dict]] = None
   lp_total_supply: Optional[str] = None
   note: Optional[str] = None
   other_potential_risks: Optional[str] = None
   owner_address: Optional[str] = None
   owner_balance: Optional[str] = None
   owner_change_balance: Optional[str] = None
   owner_percent: Optional[str] = None
   personal_slippage_modifiable: Optional[str] = None
   selfdestruct: Optional[str] = None
   sell_tax: Optional[str] = None
   slippage_modifiable: Optional[str] = None
   token_name: Optional[str] = None
   token_symbol: Optional[str] = None
   total_supply: Optional[str] = None
   trading_cooldown: Optional[str] = None
   transfer_pausable: Optional[str] = None
   trust_list: Optional[str] = None
   error: Optional[str] = None


class TokenModel(BaseModel):
 address: Optional[str] = None
 name: Optional[str] = None
 symbol: Optional[str] = None

class LiquidityModel(BaseModel):
 base: Optional[int] = None
 quote: Optional[float] = None
 usd: Optional[float] = None

class PriceChangeModel(BaseModel):
 h1: Optional[float] = None
 h24: Optional[float] = None
 h6: Optional[float] = None
 m5: Optional[float] = None

class TxnsModel(BaseModel):
 buys: Optional[int] = None
 sells: Optional[int] = None

class VolumeModel(BaseModel):
 h1: Optional[float] = None
 h24: Optional[float] = None
 h6: Optional[float] = None
 m5: Optional[float] = None

class DexScreenerModel(BaseModel):
 baseToken: Optional[TokenModel] = None
 chainId: Optional[str] = None
 dexId: Optional[str] = None
 fdv: Optional[int] = None
 labels: Optional[List[str]] = None
 liquidity: Optional[LiquidityModel] = None
 pairAddress: Optional[str] = None
 pairCreatedAt: Optional[int] = None
 priceChange: Optional[PriceChangeModel] = None
 priceNative: Optional[str] = None
 priceUsd: Optional[str] = None
 quoteToken: Optional[TokenModel] = None
 txns: Optional[Dict[str, TxnsModel]] = None
 url: Optional[str] = None
 volume: Optional[VolumeModel] = None
