class MyList(list):
    def add(self, other):
        """
        Метод складывает два списка.
        Итерируясь по индексам списков, кладу сумму значений в новый список.
        Когда доходим до конца меньшего, кладется значение из большего списка.
        """
        len_max = max(len(self), len(other))
        result = MyList([0 for _ in range(len_max)])
        for i in range(len_max):
            try:
                result[i] = self[i] + other[i]
            except IndexError:
                if len(self) > len(other):
                    result[i] = self[i]
                else:
                    result[i] = other[i]
        return result

    def sub(self, other):
        """Метод вычитает два списка."""
        return self.add(list(map(lambda x: -x, other)))


    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)


if __name__ == '__main__':
    first = MyList([1, 2, 3, 4])
    second = MyList([4, 5, 6, 5, 5])
    print(len(first), len(second))
    print(first, second)
    print(first.add(second))
    print(first.sub(second))
    print(first != second)
