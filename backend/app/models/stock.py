from pydantic import BaseModel, Field
from typing import Optional


class LiveStock(BaseModel):
    """Live stock data from GSE API"""

    symbol: Optional[str] = Field(None, alias="symbol")
    name: str = Field(..., alias="name")
    price: float = Field(..., alias="price")
    change: float = Field(..., alias="change")
    volume: int = Field(..., alias="volume")

    class Config:
        populate_by_name = True


class CompanyProfile(BaseModel):
    """Company profile information"""

    name: str = Field(..., alias="name")
    sector: Optional[str] = Field(None, alias="sector")
    industry: Optional[str] = Field(None, alias="industry")
    address: Optional[str] = Field(None, alias="address")
    telephone: Optional[str] = Field(None, alias="telephone")
    email: Optional[str] = Field(None, alias="email")
    website: Optional[str] = Field(None, alias="website")
    directors: Optional[list[dict]] = Field(None, alias="directors")

    class Config:
        populate_by_name = True


class EquityInfo(BaseModel):
    """Complete equity information"""

    name: str = Field(..., alias="name")
    price: float = Field(..., alias="price")
    capital: Optional[float] = Field(None, alias="capital")
    shares: Optional[int] = Field(None, alias="shares")
    dps: Optional[float] = Field(None, alias="dps")
    eps: Optional[float] = Field(None, alias="eps")
    company: Optional[CompanyProfile] = Field(None, alias="company")

    class Config:
        populate_by_name = True


class EquityList(BaseModel):
    """List of equities"""

    equities: list[EquityInfo]
