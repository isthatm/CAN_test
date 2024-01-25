class One:
    def __init__(self, number1) -> None:
        self.number1 = number1
    
    def add_one_to_number1(self):
        self.number1 += 1
        print(self.number1)

class Two (One):
    def __init__(self, number2) -> None:
        self.number2 = number2
        super().__init__(number2)
        super().add_one_to_number1()
        # print(self.number1)

if __name__ == '__main__':
    number2 = Two(2)

    