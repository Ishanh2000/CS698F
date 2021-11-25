# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import torch
from soft_dtw_cuda import SoftDTW
import soft_dtw_cuda
from time import time

totalTime = 0
totalDTW = 0

dim6_dirs = [
  "../raw_templates/bow_down",
  "../raw_templates/bow_up",
  "../raw_templates/flip",
  "../raw_templates/flop",
]

# testFilePath = "../test/16.csv" # must not be present in any of above directories

sdtw = SoftDTW(use_cuda=False, gamma=0.1)

def extractData(fPath):
  with open(fPath) as f: return [[float(x) for x in row[1:]] for row in list(csv.reader(f))[1:]]

def getAllScores(fPath):
  fData = torch.Tensor([extractData(fPath)]) # pass as singleton array
  fDataCuda = fData#.cuda()
  allScores = {}
  for dim6_dir in dim6_dirs:
    scores = []
    for tName in os.listdir(dim6_dir):
      # print(f"{dim6_dir}/{tName}")
      tData = torch.Tensor([extractData(f"{dim6_dir}/{tName}")]) # pass as singleton array
      tDataCuda = tData#.cuda()
      _start = time()
      loss = sdtw(fDataCuda, tDataCuda)
      _end = time()
      global totalTime, totalDTW
      totalTime += (_end - _start)
      totalDTW += 1
      scores.append(loss[0].item())
    allScores[dim6_dir] = scores

  return allScores

def getPattern(fPath):
  allScores = getAllScores(fPath)
  allMeans = {}
  for pName in allScores:
    allMeans[pName] = np.average(allScores[pName])
  return min(allMeans, key=allMeans.get), allMeans

from time import time

if __name__ == "__main__":
  # print(getAllScores(testFilePath))
  print("start")
  testFiles = [
    "../test/testdemo.csv",
    "../test/test1.csv",
    "../test/test_bow_down.csv",
    "../test/test_bow_up.csv",
    "../test/test_flip.csv",
    "../test/test_flop.csv",
  ]
  totalTime = 0
  totalDTW = 0
  PERFORM_FOR_N_ITERATIONS = 1
  for _ in range(PERFORM_FOR_N_ITERATIONS): # perform 10 times as a test
    for fName in testFiles:
      pName, pAvgs = getPattern(fName)
      print(f"\nTESTING: {fName} ...")
      # print(pAvgs)
      print(f"RECOMMENDED: {pName}\n")
  print(f"TotalTime = {totalTime}")
  print(f"Total DTW = {totalDTW}")