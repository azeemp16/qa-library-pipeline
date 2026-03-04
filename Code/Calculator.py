class Calculator:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def get_sum(self):
        return self.num1 + self.num2

    def get_difference(self):
        return self.num1 - self.num2

    def get_product(self):
        return self.num1 * self.num2

    def get_quotient(self):
        return self.num1 / self.num2


class Scientific_Calculator(Calculator):
    def __init__(self, num1, num2):
        super().__init__(num1, num2)

    def science_stuff(self):
        # get_sum() does NOT take parameters, so remove them
        answer = self.get_sum()
        answer = answer ** self.num1
        return answer


if __name__ == "__main__":
    myCalc = Calculator(num1=100, num2=20)
    answer = myCalc.get_sum()
    print(answer)
