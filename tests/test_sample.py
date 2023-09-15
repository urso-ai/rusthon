def soma(num1: int, num2: int) -> int:
    return num1 + num2


if __name__ == "__main__":
    result = soma(5, 4)
    result2 = soma(result, 3)
    print(result, result2)
