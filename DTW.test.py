# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH|| AUM NAMAH SHIVAAYA||
import numpy as np
import matplotlib.pyplot as plt
from DTW import DTW

def test_1():
  print("################ TEST 1 ################")
  print("########################################\n")

  x = [0, 2, 0, 1, 0, 0]
  y = [0, 0, 0.5, 2, 0, 1, 0]

  cost, alignment = DTW(x, y)
  print(f"(x, y): Cost = {cost}, Alignment = {alignment}")
  
  cost, alignment = DTW(y, x)
  print(f"(y, x): Cost = {cost}, Alignment = {alignment}")
  
  print()


def test_2():
  print("################ TEST 2 ################")
  print("########################################\n")

  N, shrink_N = 100, 50
  sin = [ np.sin(2*np.pi*i/N) for i in range(N) ]
  sin_shrink = [ np.sin(2*np.pi*i/shrink_N) for i in range(shrink_N) ]
  cos = [ np.cos(2*np.pi*i/N) for i in range(N) ]
  cos_shrink = [ np.cos(2*np.pi*i/shrink_N) for i in range(shrink_N) ]

  plt.plot(sin, c="red")
  plt.plot(sin_shrink, c="red")
  plt.plot(cos, c="blue")
  plt.plot(cos_shrink, c="blue")
  plt.legend([ "sin", "sin_shrink", "cos", "cos_shrink" ])
  plt.show()

  print("ALL COMBINATIONS:\n")

  cost, alignment = DTW(sin, sin_shrink)
  print(f"(sin, sin_shrink): Cost = {cost}\nAlignment = {alignment}\n")
  cost, alignment = DTW(sin, cos)
  print(f"(sin, cos): Cost = {cost}\nAlignment = {alignment}\n")
  cost, alignment = DTW(sin, cos_shrink)
  print(f"(sin, cos_shrink): Cost = {cost}\nAlignment = {alignment}\n")
  cost, alignment = DTW(sin_shrink, cos)
  print(f"(sin_shrink, cos): Cost = {cost}\nAlignment = {alignment}\n")
  cost, alignment = DTW(sin_shrink, cos_shrink)
  print(f"(sin_shrink, cos_shrink): Cost = {cost}\nAlignment = {alignment}\n")
  cost, alignment = DTW(cos, cos_shrink)
  print(f"(cos, cos_shrink): Cost = {cost}\nAlignment = {alignment}\n")
  

if __name__ == "__main__":
  test_1()
  test_2()
