
from threading import Thread
from time import sleep
from random import randint
from queue import Queue

class Table:
    def __init__(self, number, guest=None):
        self.number = number  # номер стола
        self.guest = guest  # гость, который сидит за этим столом

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()  # очередь гостей
        self.tables = list(tables)  # столы в кафе

    def guest_arrival(self, *guests):  # прибытие гостей
        for guest in guests:
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    guest.start()
                    print(f'{guest.name} сел(-a) за стол номер {table.number}')
                    break
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):  # обслуживание гостей
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
                    if not self.queue.empty():
                        next_guest = self.queue.get()
                        table.guest = next_guest
                        next_guest.start()
                        print(f'{next_guest.name} вышел из очереди и сел(-а) за стол номер {table.number}')


tables = [Table(number) for number in range(1, 6)]  # Создание столов
guests_names = ['Maria', 'Michail', 'Igor', 'Darya', 'Olga', 'Nikita',
                'Galina', 'Pavel', 'Ilya', 'Alexandr']  # Имена гостей
guests = [Guest(name) for name in guests_names]  # Создание гостей

cafe = Cafe(*tables)  # Заполнение кафе столами

cafe.guest_arrival(*guests)  # Приём гостей

cafe.discuss_guests()  # Обслуживание гостей
