from pydantic import BaseModel
from decimal import *
from fxpmath import Fxp
from typing import Type

FloatingPoint = Decimal
FixedPoint = Type[Fxp(None, signed=True, n_int=256, n_frac=18)]

class FloatingPointUnstakeTKN(BaseModel):
    a: FloatingPoint
    b: FloatingPoint
    c: FloatingPoint
    e: FloatingPoint
    m: FloatingPoint
    n: FloatingPoint
    x: FloatingPoint
    w: FloatingPoint


class FixedPointUnstakeTKN(BaseModel):
    a: FixedPoint
    b: FixedPoint
    c: FixedPoint
    e: FixedPoint
    m: FixedPoint
    n: FixedPoint
    x: FixedPoint
    w: FixedPoint
