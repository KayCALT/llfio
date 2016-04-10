#!/usr/bin/python3

benchmark_locking_path="../build/x64/Release/benchmark_locking"

max_waiters = 8
max_entities = 8

algorithms = [ "lock_files", "byte_ranges", "atomic_append" ]
algorithms += [ "!lock_files", "!byte_ranges", "!atomic_append" ]

results = []
for y in range(0, max_waiters):
  result=[]
  for x in range(0, max_entities):
    result.append(0)
  results.append(result)

import os, subprocess

with open("benchmark_locking_matrix.csv", "wt") as oh:
  os.chdir(os.path.dirname(benchmark_locking_path))

  for algorithm in algorithms:
    for y in range(0, max_waiters):
      for x in range(0, max_entities):
        ph = subprocess.check_call(['benchmark_locking', algorithm, str(x+1), str(y+1)])
        with open("benchmark_locking.csv", "rt") as ih:
          ih.readline()
          results[y][x]=int(ih.readline())

    oh.write(algorithm+'\n')
    for x in range(0, max_entities):
      oh.write(',"'+str(x+1)+' entities"')
    oh.write('\n')
    for y in range(0, max_waiters):
      oh.write('"'+str(y+1)+' waiters"')
      for x in range(0, max_entities):
        oh.write(','+str(results[y][x]))
      oh.write('\n')
    oh.write('\n')
    
