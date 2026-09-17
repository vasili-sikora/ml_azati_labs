from abc import ABC, abstractmethod
from dataclasses import InitVar, dataclass, field

DISCOUNT_PERCENTS = 15


@dataclass(frozen=True, order=True)
class Item:
    # note: you might want to change the order of fields
    item_id: int = field(compare=False)
    title: str
    cost: int

    def __post_init__(self):
        assert self.title, "Название не должно быть пустым"
        assert self.cost > 0, "Цена должна быть положительной"


# You may set `# type: ignore` on this class
# It is [a really old issue](https://github.com/python/mypy/issues/5374)
# But seems to be solved
@dataclass
class Position(ABC):
    item: Item

    @property
    @abstractmethod
    def cost(self) -> int | float:
        return self.item.cost


@dataclass
class CountedPosition(Position):
    count: int = 1

    @property
    def cost(self) -> int:
        return self.item.cost * self.count


@dataclass
class WeightedPosition(Position):
    weight: float = 1.0

    @property
    def cost(self) -> float:
        return self.item.cost * self.weight


@dataclass
class Order:
    order_id: int
    positions: list[Position] = field(default_factory=list)
    cost: int = field(init=False)
    have_promo: InitVar[bool] = False

    def __post_init__(self, have_promo: bool):
        total = sum(position.cost for position in self.positions)
        if have_promo:
            total *= (100 - DISCOUNT_PERCENTS) / 100

        self.cost = int(total)
