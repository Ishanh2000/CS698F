# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH|| AUM SHREEHANUMATE NAMAH||

def DTW(x = [], y = []):
  M, N = len(x), len(y) # assume signals x and y have similar variance
  if (M < 1) or (N < 1): return None # can do nothing

  # Initialization
  cost = [ [ None for j in range(N+1) ] for i in range(M+1) ]
  for i in range(1, M+1): cost[i][0] = [ float('inf'), ((i-1), 0) ] # [cost, parent]
  for j in range(1, N+1): cost[0][j] = [ float('inf'), (0, (j-1)) ] # [cost, parent]
  cost[0][0] = [ 0, None ]

  # Algorithm
  for i in range(1, M+1):
    for j in range(1, N+1):
      add, parent = cost[i-1][j][0], ((i-1), j)
      if (add > cost[i-1][j-1][0]): add, parent = cost[i-1][j-1][0], ((i-1), (j-1))
      if (add > cost[i][j-1][0]): add, parent = cost[i][j-1][0], (i, (j-1))
      cost[i][j] = [ ((y[j-1] - x[i-1])**2 + add), parent ]

  totalCost = cost[M][N][0]

  alignment = [ (M, N) ]
  while True:
    i, j = alignment[-1]
    parent = cost[i][j][1]
    if parent == None: break
    alignment.append(parent)
  alignment.reverse()
  alignment = [ (a[0]-1, a[1]-1) for a in alignment[1:]]

  return totalCost, alignment

