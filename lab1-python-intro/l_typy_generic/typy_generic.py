from typing import Generic, TypeVar

T = TypeVar("T", int, float)


class VectorIterator(Generic[T]):
    def __init__(self, vector: "Vector[T]") -> None:
        """Создаёт итератор вектора из вектора"""
        self.vector: Vector[T] = vector
        self.index = 0

    def __iter__(self) -> "VectorIterator[T]":
        """Возвращает объект-итератор"""
        return self

    def __next__(self) -> T:
        """Возвращает следующий элемент из итератора"""
        if self.index >= len(self.vector):
            raise StopIteration

        element = self.vector[self.index]
        self.index += 1
        return element


class Vector(Generic[T]):
    def __init__(self, elements: list[T]) -> None:
        """Создаёт вектор из копии элементов"""
        self.elements: list[T] = elements.copy()

    def __len__(self) -> int:
        """Возвращает длину вектора"""
        return len(self.elements)

    def __getitem__(self, index: int) -> T:
        """Возвращает элемент из вектора по индексу"""
        return self.elements[index]

    def append(self, element: T) -> None:
        """Добавляет элемент в конец вектора"""
        self.elements.append(element)

    def extend(self, elements: list[T]) -> None:
        """Добавляет элементы в конец вектора"""
        self.elements.extend(elements)

    def __iter__(self) -> VectorIterator[T]:
        """Возвращает итератор вектора"""
        return VectorIterator(self)

    def __str__(self) -> str:
        """Возвращает строковое представление вектора"""
        return repr(self)

    def __repr__(self) -> str:
        """Возвращает строковое представление вектора"""
        return f"Vector({self.elements!r})"

    def __add__(self, other: "Vector[T]") -> "Vector[T]":
        """Складывает два вектора"""
        if len(self) != len(other):
            raise ValueError("Длины векторов не совпадают")

        return Vector([a + b for a, b in zip(self, other)])

    def __sub__(self, other: "Vector[T]") -> "Vector[T]":
        """Вычитает один вектор из другого"""
        if len(self) != len(other):
            raise ValueError("Длины векторов не совпадают")

        return Vector([a - b for a, b in zip(self, other)])

    def __mul__(self, scalar: T) -> "Vector[T]":
        """Умножает вектор на скаляр"""
        return Vector([element * scalar for element in self.elements])

    def __rmul__(self, scalar: T) -> "Vector[T]":
        """Умножает вектор на скаляр"""
        return self * scalar

    def dot(self, other: "Vector[T]") -> int | float:
        """Вычисляет скалярное произведение двух векторов"""
        if len(self) != len(other):
            raise ValueError("Длины векторов не совпадают")

        return sum(a * b for a, b in zip(self, other))
