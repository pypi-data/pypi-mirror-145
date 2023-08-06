import numpy


def splus(float_numbers):
    return sum(float_numbers)


def subtract(float_numbers):
    count = 0
    for i in float_numbers:
        if count == 0:
            sub = i

        if count > 0:
            sub -= i

        count+=1

    return sub


def multiply(float_numbers):
    return numpy.prod(float_numbers)


def divide(float_numbers):
    count = 0
    for i in float_numbers:
        if count == 0:
            div = i

        if count > 0:
            div /= i

        count+=1

    return div