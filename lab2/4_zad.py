import numpy as np
import math

class DistributionTester:
    def __init__(self, generate_strategy, percentile_strategy):
        self.generate_strategy = generate_strategy
        self.percentile_strategy = percentile_strategy
    
    def generate_numbers(self, *args):
        return self.generate_strategy.generate_numbers(*args)

    def calculate_percentile(self, numbers, percentile):
        return self.percentile_strategy.calulate_percentile(numbers, percentile)
    
class SlijednoGeneriranje:
    def __init__(self, start, end, step):
        self.start = start
        self.end = end
        self.step = step

    def generate_numbers(self):
        return list(range(self.start, self.end+1, self.step))

class SlucajnoGeneriranje:
    def __init__(self, mu, sigma, nosamples):
        self.mu = mu
        self.sigma = sigma
        self.nosamples = nosamples
    
    def generate_numbers(self):
        numbers = np.random.normal(self.mu, self.sigma, self.nosamples)
        numbers.sort()
        return numbers

class FibonacciGeneriranje:
    def __init__(self, nosamples):
        self.nosamples = nosamples
    
    def generate_numbers(self):
        numbers = [1]
        if self.nosamples == 1:
            return numbers
        numbers.append(1)
        if self.nosamples == 2:
            return numbers
        for i in range(self.nosamples - 2):
            numbers.append(numbers[i] + numbers[i + 1])
        return numbers

class NajbliziRank:
    def calulate_percentile(self, numbers, percentile):
        return numbers[math.ceil(percentile * len(numbers) / 100) - 1]

class InterpolacijskiPercentil:
    def calulate_percentile(self, numbers, percentile):
        n = len(numbers)
        p = percentile * n / 100
        if p < 1:
            return numbers[0]
        if p > n:
            return numbers[-1]
        
        i = int(p)
        return numbers[i-1] + n * (percentile - (100 * (i - 0.5) / n)) * (numbers[i] - numbers[i-1]) / 100

test = DistributionTester(SlijednoGeneriranje(1, 100, 10), NajbliziRank())
numbers = test.generate_numbers()
for percentile in range(10, 100, 10):
    value = test.calculate_percentile(numbers, percentile)
    print(str(percentile) + ". percentil je: " + str(value))
print("///////")
test2 = DistributionTester(FibonacciGeneriranje(5), InterpolacijskiPercentil())
numbers2 = test2.generate_numbers()
for percentile in range(10, 100, 10):
    value = test2.calculate_percentile(numbers2, percentile)
    print(str(percentile) + ". percentil je: " + str(value))