class MyList(list):
    def __init__(self, lst):
        super().__init__(lst)
        self.sum = self._sum()

    def add(self, other):
        len_max = max(len(self), len(other))
        result = [0 for _ in range(len_max)]
        for i in range(len_max):
            try:
                result[i] = self[i] + other[i]
            except IndexError:
                if len(self) > len(other):
                    result[i] = self[i]
                else:
                    result[i] = other[i]
        return result

    def sub(self,other):
        return self.add(list(map(lambda x: -x, other)))

    def _sum(self):
        weight = 0
        for tmp in self:
            weight += tmp
        return weight

    def __lt__(self, other):
        return self.sum < other.sum

    def __le__(self, other):
        return self.sum <= other.sum

    def __eq__(self, other):
        return self.sum == other.sum

    def __ne__(self, other):
        return self.sum != other.sum

    def __gt__(self, other):
        return self.sum > other.sum

    def __ge__(self, other):
        return self.sum >= other.sum


if __name__ == '__main__':
    first = MyList([1, 2, 3, 4])
    second = MyList([4, 5, 6, 5, 5])
    print(len(first), len(second))
    print(first, second)
    print(first.add(second))
    print(first.sub(second))
    print(first <= second)
