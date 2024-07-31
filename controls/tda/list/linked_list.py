import heapq
import time
from controls.tda.list.node import Node


class Linked_List(object):
    def __init__(self):
        self.__head = None
        self.__last = None
        self.__length = 0

    @property
    def _length(self):
        return self.__length

    @_length.setter
    def _length(self, value):
        self.__length = value

    @property
    def _head(self):
        return self.__head

    @_head.setter
    def _head(self, value):
        self.__head = value

    @property
    def is_empty(self):
        return self.__head is None or self.__length == 0

    def add_first(self, data):
        if self.is_empty:
            node = Node(data)
            self.__head = node
            self.__last = node
            self.__length += 1
        else:
            head_old = self.__head
            node = Node(data, head_old)
            self.__head = node
            self.__length += 1

    def add_last(self, data):
        if self.is_empty:
            self.add_first(data)
        else:
            aux = Node(data)
            self.__last._next = aux
            self.__last = aux
            self.__length += 1

    def add_pos(self, data, pos):
        if pos == 0:
            self.add_first(data)
        elif pos == self._length - 1:
            self.add_last(data)
        else:
            search_preview = self.get_node(pos - 1)
            aux = Node(data, search_preview._next)
            search_preview._next = aux
            self._length += 1

    def add(self, data):
        if self.is_empty:
            self.add_first(data)
        else:
            self.add_last(data)

    def get_node(self, post):
        if self.is_empty:
            raise Exception("Error, Lista vacia")
        elif post < 0 or post >= self._length:
            raise IndexError("Error, Esta fuera del limite de la lista")
        elif post == 0:
            return self.__head
        elif post == (self._length - 1):
            return self.__last
        else:
            search = self.__head
            cont = 0
            while cont < post:
                cont += 1
                search = search._next
            return search

    def get_first(self):
        if self.is_empty:
            raise Exception("Error, List is empty")
        else:
            return self.__head._data

    def get_last(self):
        if self.is_empty:
            raise Exception("Error, List is empty")
        else:
            return self.__last._data

    def get(self, index):
        if self.is_empty:
            raise Exception("Error, Lista vacia")
        elif index < 0 or index >= self._length:
            raise IndexError("Error, It is out of the limit of the list")
        elif index == 0:
            return self.get_first()
        elif index == (self._length - 1):
            return self.get_last()
        else:
            search = self.get_node(index)
            return search._data

    def __str__(self) -> str:
        out = ""
        if self.is_empty:
            out = "List is empty"
        else:
            node = self.__head
            while node is not None:
                out += "=> " + str(node._data)
                node = node._next
        return out

    @property
    def print(self):
        node = self.__head
        data = ""
        while node is not None:
            data += str(node._data) + " -> "
            node = node._next
        print(data)

    def update(self, pos, data):
        if self.is_empty:
            raise Exception("List is empty")
        elif pos < 0 or pos >= self._length:
            raise IndexError("Error, It is out of the limit of the list")
        elif pos == 0:
            self.__head._data = data
        elif pos == (self._length):
            self.__last._data = data
        else:
            nodo = self.get_node(pos)
            nodo._data = data

    def clear(self):
        self.__head = None
        self.__last = None
        self.__length = 0

    def __iter__(self):
        self.__current = self.__head
        return self

    def __next__(self):
        if self.__current is None:
            raise StopIteration
        else:
            item = self.__current._data
            self.__current = self.__current._next
            return item

    @property
    def to_array(self):
        array = []
        node = self.__head
        while node is not None:
            array.append(node._data)
            node = node._next
        return array

    def to_list(self, array):
        self.clear()
        for i in range(0, len(array)):
            self.add_last(array[i])
        return self

    def deleteFirst(self):
        if self.is_empty:
            raise IndexError("List empty")
        else:
            element = self.__head._data
            aux = self.__head._next
            self.__head = aux
            if self.__length == 1:
                self.__last = None
            self._length = self._length - 1
            return element

    def deleteLast(self):
        if self.is_empty:
            raise IndexError("List empty")
        else:
            element = self.__last._data
            aux = self.get_node(self._length - 2)

            if aux == None:
                self.__last = None
                if self.__length == 2:
                    self.__last = self.__head
                else:
                    self.__head = None
            else:
                self.__last = None
                self.__last = aux
                self.__last._next = None
            self._length = self._length - 1
            return element

    def delete(self, pos=0):

        if self.is_empty:
            raise IndexError("List empty")
        elif pos < 0 or pos >= self.__length:
            raise IndexError("Error, It is out of the limit of the list")
        elif pos == 0:
            return self.deleteFirst()
        elif pos == (self.__length - 1):
            return self.deleteLast()
        else:
            preview = self.get_node(pos - 1)
            actually = self.get_node(pos)
            element = preview._data
            next = actually._next
            actually = None
            preview._next = next
            self._length = self._length - 1
            return element

    def __getitem__(self, index):
        if index < 0 or index >= self._length:
            raise IndexError("Error, It is out of the limit of the list")
        else:
            return self.get_node(index)._data

    def search_models(self, attribute, value):
        lista = Linked_List()
        if self.is_empty:
            raise Exception("List is empty")
        else:
            array = self.to_array
            if isinstance(array[0], object):
                array = [x for x in array if getattr(x, "_" + attribute) == value]
            lista.to_list(array)
        return lista
    
     #METODO QUICKSORT
    def quick(self, attribute, asc=True, ):
        array = self.to_array
        sorted_array = self.quicksort_(array, attribute, asc)
        self.clear()
        for item in sorted_array:
            self.add_last(item)
    
    def quicksort_(self, array, attribute, asc):
        if len(array) <= 1:
            return array
        pivot = array[len(array) // 2]
        if asc:
            left = [x for x in array if getattr(x, attribute) < getattr(pivot, attribute)]
            middle = [x for x in array if getattr(x, attribute) == getattr(pivot, attribute)]
            right = [x for x in array if getattr(x, attribute) > getattr(pivot, attribute)]
        else:
            left = [x for x in array if getattr(x, attribute) > getattr(pivot, attribute)]
            middle = [x for x in array if getattr(x, attribute) == getattr(pivot, attribute)]
            right = [x for x in array if getattr(x, attribute) < getattr(pivot, attribute)]
        return self.quicksort_(left, attribute, asc) + middle + self.quicksort_(right, attribute, asc)
    #FIN DEL METODO QUICKSORT

    # Buscar por atributo y retornar el objeto con busqueda binaria
    def busquedaBinaria(self, attribute, value):
        if self.is_empty:
            raise Exception("Error, lista vacía")
        else:
            self.quick(attribute)
            array = self.to_array
            low = 0
            high = len(array) - 1
            while low <= high:
                mid = (low + high) // 2
                if getattr(array[mid], attribute) == value:
                    return array[mid]
                elif getattr(array[mid], attribute) < value:
                    low = mid + 1
                else:
                    high = mid - 1
            return None

    