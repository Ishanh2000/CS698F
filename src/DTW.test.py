# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH|| AUM NAMAH SHIVAAYA||
import numpy as np
import matplotlib.pyplot as plt
from DTW import DTW, DTW_from_file
import os
# from os import listdir
# from os.path import isfile, join

def test_1():
  print("################ TEST 1 ################")
  print("########################################\n")

  x = [0, 2, 0, 1, 0, 0]
  y = [0, 0, 0.5, 2, 0, 1, 0]

  cost, alignment = DTW(x, y)
  print(f"(x, y): Cost = {cost}, Alignment = {alignment}")
  
  cost, alignment = DTW(y, x)
  print(f"(y, x): Cost = {cost}, Alignment = {alignment}")
  
  cost, alignment = DTW(x, x)
  print(f"(x, x): Cost = {cost}, Alignment = {alignment}")
  
  cost, alignment = DTW(y, y)
  print(f"(y, y): Cost = {cost}, Alignment = {alignment}")
  
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


def test_3():
  templates = [
    "../raw_templates/backward/",
    "../raw_templates/cross/",
    "../raw_templates/forward/",
    "../raw_templates/wave/",
  ]
  testFiles = [
    "../test/backward/sensor.csv",
    # "../test/cross/sensor.csv",
    # "../test/forward/sensor.csv",
    # "../test/wave/sensor.csv",
  ]
  for tf in testFiles:
    # perform DTW again each file in template folders.
    for dirPath in templates:
      for obj in os.listdir(dirPath):
        objPath = os.path.join(dirPath, obj)
        if not os.path.isfile(objPath): continue
        scores, _ = DTW_from_file(os.path.abspath(tf), os.path.abspath(objPath))
      # recordFiles = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]
      # print(recordFiles)

def test_4():
  testPath = "/home/ishanhmisra/CS698F/Project/test/backward/sensor.csv"
  recordPaths = [
    "/home/ishanhmisra/CS698F/Project/raw_templates/backward/1.csv",
    "/home/ishanhmisra/CS698F/Project/raw_templates/cross/1.csv",
    "/home/ishanhmisra/CS698F/Project/raw_templates/forward/1.csv",
    "/home/ishanhmisra/CS698F/Project/raw_templates/wave/1.csv",
  ]
  for recordPath in recordPaths:
    scores = DTW_from_file(testPath, recordPath)
    print(f"{recordPath}")
    print(f"\tax = {round(scores['ax'][0], 4)}, ay = {round(scores['ay'][0], 4)}, az = {round(scores['az'][0], 4)}")
    print(f"\taT = {round(scores['aT'][0], 4)}\n")



if __name__ == "__main__":
  # test_1()
  # test_2()
  # test_3()
  test_4()
