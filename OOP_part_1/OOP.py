import numpy as np

class User:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Booking:
    def __init__(self, equipment, user, start_time, end_time):
        self.equipment = equipment
        self.user = user
        self.start_time = start_time
        self.end_time = end_time

    def is_intersect(self, other):
        # Пересечение происходит, если начало одного бронирования находится внутри другого бронирования
        return (self.start_time < other.end_time and self.end_time > other.start_time)

    def __str__(self):
        return f"{self.equipment} booked by {self.user} from {self.start_time} to {self.end_time}"


class LabEquipment:
    def __init__(self):
        self.equipment = []
        self.booking_history = []

    def add_equipment(self, equipment_name):
        if equipment_name not in self.equipment:
            self.equipment.append(equipment_name)

    def is_available(self, equipment_name, start_time, end_time):
        for booking in self.booking_history:
            if booking.equipment == equipment_name and booking.is_intersect(Booking(equipment_name, None, start_time, end_time)):
                return False
        return True

    def book(self, equipment_name, user, start_time, end_time):
        if equipment_name not in self.equipment:
            raise ValueError("Requested equipment is not available.")
        if self.is_available(equipment_name, start_time, end_time):
            new_booking = Booking(equipment_name, user, start_time, end_time)
            self.booking_history.append(new_booking)
            print(f"Booking successful: {new_booking}")
        else:
            raise ValueError("Requested time slot is not available.")

class MemoryOutOfBoundsError(Exception):
    pass

class InvalidInstructionError(Exception):
    pass

class GenCodeInterpreter:
    def __init__(self):
        self.memory = [0] * 5000
        self.pointer = 0
        self.output_buffer = ""

    def eval(self, program):
        self.output_buffer = ""
        for instruction in program:
            if instruction == 'A':
                self.pointer += 1
                if self.pointer >= len(self.memory):
                    raise MemoryOutOfBoundsError("Pointer moved beyond the memory limit.")
            elif instruction == 'T':
                self.pointer -= 1
                if self.pointer < 0:
                    raise MemoryOutOfBoundsError("Pointer moved before the start of the memory.")
            elif instruction == 'G':
                self.memory[self.pointer] = (self.memory[self.pointer] + 1) % 256
            elif instruction == 'C':
                self.memory[self.pointer] = (self.memory[self.pointer] - 1) % 256
            elif instruction == 'N':
                self.output_buffer += chr(self.memory[self.pointer])
            else:
                raise InvalidInstructionError(f"Invalid instruction: {instruction}")
        return self.output_buffer

def meet_the_dunders():
    res = 0

    matrix = []
    for idx in range(0, 100, 10):
        matrix += [list(range(idx, idx + 10))]

    def func_1(x):
        return x in range(1, 5, 2)
        
    def func_2(x):
        return [x[col] for col in selected_columns_indices]
        
    selected_columns_indices = list(filter(func_1, range(len(matrix))))
    selected_columns = map(func_2, matrix)

    arr = np.array(list(selected_columns))

    mask = arr[:, 1] % 3 == 0
    new_arr = arr[mask]

    product = new_arr @ new_arr.T

    if (product[0] < 1000).all() and (product[2] > 1000).any():
        res = int(product.mean() // 10 % 100)
    return res
