from random import randint


class LRUCache:
    def __init__(self, capacity: int) -> None:
        """
        При инициализации запрашиваем размер кэша, сам кэш задается диктом.
        Добавляем счётчик элементов. В дикте значением является список, где
        первым значением идёт строка, которую помещаем в кэш, вторым идёт
        счетчик количества обращений к объекту кэша.
        """
        self.capacity = capacity
        self.cache = {}
        self.counter = 0

    def get(self, key: str) -> str:
        """
        Пытаемся увеличить счётчик обращений к объекту кэша.
        """
        try:
            self.cache[key][1] += 1
        except KeyError:
            pass
        return self.cache.get(key, [''])

    def set(self, key: str, value: str) -> None:
        """
        Если в кэше есть место, добавляем новый объект сразу и увел. счётчик
        объектов. Если места нет, за самый старый берется сначала первый, далее
        итерируясь по ключам ищем более ненужный объект и удаляем его.
        """
        if self.counter >= self.capacity:
            most_old = [list(self.cache.keys())[0], list(self.cache.values())[0][1]]
            for tmp in self.cache.keys():
                if self.cache[tmp][1] < most_old[1]:
                    most_old = [tmp, self.cache[tmp][1]]
            self.delete(most_old[0])
        for tmp in self.cache.keys():
            self.cache[tmp][1] += -1
        self.cache[key] = [value, 0]
        self.counter += 1

    def delete(self, key: str) -> None:
        """
        поп)))0)
        """
        self.cache.pop(key)

    @staticmethod
    def _validate_input_choice(inp) -> int:
        """
        Валидация инпута в UI
        """
        try:
            number = int(inp)
        except ValueError:
            print("You entered not an integer number", )
        else:
            try:
                if not (number > 0 and number <= 4):
                    raise ValueError("Your number should be 1, 2, 3 or 4")
            except ValueError as err:
                print(err)
            else:
                return number

    def user_interface(self):
        """
        Текстовый UI для удобства работы
        """
        while True:
            choice = None
            while choice is None:
                print('1. get\n2. set\n3. delete\n4. exit')
                tmp = input()
                choice = self._validate_input_choice(tmp)
            if choice == 1:
                print(f'{lru_cache.cache}\nEnter which key you want to get: ', end="")
                print(self.get(input())[0])
            if choice == 2:
                print('Enter key: ', end='')
                key = input()
                print('Enter value: ', end='')
                value = input()
                self.set(key, value)
            if choice == 3:
                print(f'{lru_cache.cache}\nEnter which key you want to delete: ', end="")
                print(self.delete(input()))
            if choice == 4:
                break


if __name__ == '__main__':
    lru_cache = LRUCache(4)
    lru_cache.user_interface()
