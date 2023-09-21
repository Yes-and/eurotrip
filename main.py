import pandas as pd

from generate_solution import *

df = pd.read_csv("eurotrip-flights.csv")

solutions = greedy_solution_with_time(data=df)
print(solutions)