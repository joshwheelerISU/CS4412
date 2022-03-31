import math
import random


def prime_test(N, k):
    # This is main function, that is connected to the Test button. You don't need to touch it.
    return fermat(N, k), miller_rabin(N, k)


def mod_exp(x, y, N):
    # You will need to implement this function and change the return value.   
    if y == 0:                                                              # constant time
        return 1                                                            # constant time
    else:
        z = mod_exp(x, math.floor(y/2), N)                                  # recursive call that will run log(y) times
        if y % 2 == 0:                                                      # constant time
            return (z ** 2) % N                                             # constant time
        else:
            return (x * (z ** 2)) % N                                       # constant time


def fprobability(k):
    # You will need to implement this function and change the return value.   
    x = 1 / (math.pow(2,k))
    return (1-x)*100


def mprobability(k):
    # You will need to implement this function and change the return value.   
    x = 1 / (math.pow(4, k))
    return (1 - x) * 100


def fermat(N, k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    # start with the assumption the number is prime
    while k > 0:
        l = random.randint(2, N - 2)
        if mod_exp(l, N-1, N) != 1:
            return 'composite'  # number is not prime, exit loop
        k = k-1
    return 'prime'


def miller_rabin(N, k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    # check for base cases like 2 or even numbers
    if N % 2 == 0:
        return 'composite'
    elif N == 2:
        return 'prime'
    else:    # begin main loop
        while k > 0:
            l = random.randint(2, N-1)  # pick random l
            if mod_exp(l, N - 1, N) != 1 or mod_exp(l, N - 1, N) != -1:
                return 'composite'
            else:
                k = k - 1  # allow the loop to continue
        return 'prime'

