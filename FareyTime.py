# Completed by Nana Kiziriya on April 26, 2026
# Originally developed on Google Colab, uploaded to GitHub

# THIS PROGRAM PROVIDES:

# fareyApprox(x:float,doPrint:bool) -> set:
    # returns (set) of good rational approximations for (x), using concepts from Diophantine approximation, particulary Farey neighbors/mediants
        # learned during CUNY Directed Reading Program, Spring 2025
    # approximations range from (round(x)) to (x), in terms of precision
    # criteria: minimize (score), defined as (error)*(denominator)
        # I came up with this criteria myself :) Balances goal of minimizing error and minimizing denominator.
        # The choice of multiplication balances scale better than addition does, and provides stopping condition of (score==0)
    # see function for further notes on implementation...

# findOTIS(series_times:pd.Series, doPrint:bool, doDeepPrint:bool):
    # LEVERAGES fareyApprox()
    # returns (set) of good rational approximations - ideally just 1 tho - for a time-precise measurement device's original time interval setting (OTIS)
    # see function for further notes...



import numpy as np
import pandas as pd
import scipy.stats as stats



# GLOBAL HELPER METHODS
_fltVal = lambda tup : tup[0]/tup[1] # float value
_ratStr = lambda tup : f"{tup[0]}/{tup[1]}" # rational string


def fareyApprox(x:float,doPrint:bool=False,embedded=False) -> set:
# FIND ALL GOOD RATIONAL APPROX. OF FLOAT (x)
# best Farey neighbor approximations minimize score (DENOMINATOR*ERROR)
# tuple format: (numer, denom, error, score)

  # Local helper methods:
  # conditional printing
  def cond_print(s) :
    if doPrint : print(("\t" if embedded else "")+s)
  # tup = tuple(numer, denom, error, score)
  ndes = lambda n,d : (n,d,abs(n/d-x),abs(n/d-x)*d) # def. score in last element
  betterThan = lambda tup1,tup2 : tup1[3]<tup2[3] # boolean
  ratTup = lambda tup : (tup[0],tup[1])

  # Print explanation
  if embedded :
    cond_print(f"Approximating {x}:")
  else :
    cond_print(f"""Finding good rational approximations for {x} using Farey neighbor mediants
    Method: minimize the score (error*denominator)
    Returns: set of good approximations\n
    """)

  # Variables
  # Farey neighbors of x
  min = ndes(int(np.floor(x)), 1)
  max = ndes(int(np.ceil(x)), 1)
  best = min if betterThan(min,max) else max
  approx_set = {ratTup(best)}

  while best[3]>0 :
    next = ndes(min[0]+max[0], min[1]+max[1]) # mediant
    if _fltVal(next)>x: max = next
    else: min = next
    if betterThan(next,best):
      best = next
      approx_set.add(ratTup(best))
      cond_print(f"\tbest {_ratStr(best)} score {best[3]} in [{_ratStr(min)}, {_ratStr(max)}]")
  cond_print(f"Set of approximations: {approx_set}\n")
  return approx_set;



def findOTIS(series_times:pd.Series, doPrint:bool=False, doDeepPrint:bool=False) -> set:

# OTIS - Original Time Interval Setting

# PURPOSE:
  # Accepts ordered list (or pd.series) of truncated time interval measurements
  # Finds original (rational) time interval using Farey neighbors/mediants

# TESTING CRITERIA:
  # 1. OTIS must approx. ALL truncated intervals
  # 2. [time_elapsed] must be valid approximation of [num_intervals*OTIS], given max possible rounding error during measurement of start and end times
    # Note: given [num_decimals_MIN] (min decimal accuracy of measurement device), the overall error (btwn [time_elapsed] and [num_intervals*OTIS]) must be no more than 10**(-1*num_decimals_MIN), because measurement rounding of start and end times each contribute at MOST half of that

# REQUIRED ASSUMPTIONS:
  # Original measurement device measures at precise time intervals
  # Error is only a result of truncation
  # Time intervals are (originally) all equal
  # time intervals are non-zero
  # Measurement device may round to fixed number of sigfigs, not fixed number of decimal places (i.e. num decimal places can decrease over time)

  # Local helper method: conditional printing
  def cond_print(s) :
    if doPrint : print(s)

  cond_print("OTIS - Original Time Interval Setting")
  cond_print("If your measurement device is calibrated to measure at even time intervals, but the recorded times are truncated, this algorithm finds the OTIS.\n")

  # << PT 1 >>
  # Find measurement device's decimal place precision
  # Note: must jump through hoops to avoid floating point error confusion in order to avoid calculating farey neighbor for same time interval more than once; so annoying uggh

  # series -> list
  # e.g. [0.01, 0.02, ...]
  list_times = series_times.tolist()
  del series_times

  # list of float -> list of str of float
  # e.g. ['0.01', '0.02', ...]
  list_times_STR = list(map(lambda _:_[0,_.find(" ")] if " " in _ else _,(str(list_times)[1:len(str(list_times))-1]).split(", ")))

  assert(len(list_times)==len(list_times_STR))

  # list of str of float -> list of str of float's decimals
  # e.g. ['0.0123', ..., '1', '1.0234] -> ['0123', ..., '', '0234']
  list_decimals_STR = list(
          map(
              lambda _ : _[_.find(".")+1 : len(_)] if ("." in _) else "",
              list_times_STR
          )
      )

  assert(len(list_times_STR)==len(list_decimals_STR))
  for i in range(len(list_decimals_STR)) :
    assert(list_decimals_STR[i] in list_times_STR[i])

  # list of str of float -> min and max decimal length of float
  # e.g. ['0.01', '0.02', '0.029', ..., '123.01'] -> 3
  # Purpose: proper rounding and final error threshold
  set_decimal_lengths = set(
          map( # returns LENGTH of each decimal portion
                len,
              list_decimals_STR
          )
      )
  num_decimals_MAX = max(set_decimal_lengths)
  num_decimals_MIN = min(set_decimal_lengths)

  # << PT 2 >>
  # TIMES -> TIME INTERVALS
  # Note: use num_decimals_MAX for rounding time differences (intervals) to avoid repeats from floating point arithmetic error
  # Available local vars:
    # iterable: list_times,  list_times_STR
    # num : num_decimals_MAX
    # bool: doPrint, doDeepPrint
  # Will create vars:
    # list_intervals (rounded using num_decimals_MAX)
    # set_intervals (set of list_intervals)

  list_intervals = [0]*(len(list_times)-1)
  for i in range(len(list_intervals)): list_intervals[i] = round(list_times[i+1]-list_times[i], num_decimals_MAX)

  assert(len(list_times)-1==len(list_intervals))

  set_intervals = set(list_intervals)

  cond_print(f"Set of recorded time intervals: {set_intervals}")

  cond_print(f"Average of intervals: {stats.describe(list_intervals)[2]}")
  cond_print(f"Variance of intervals (SHOULD BE LOW) : {stats.describe(list_intervals)[3]}") # high variance -> probably uneven time intervals
  cond_print("")

  # << PT. 3 >>
  # Begin finding OTIS

  # Method to format printing rational tuples in OTIS
  ratListStr = lambda iter_tuples : type(iter_tuples)(map(lambda _:_ratStr(_),iter_tuples))

  iter : " ".join(map(lambda _ : f"{_[0]}/{_[1]} , ",list(iter)))

  OTIS = set()
  do_once = 0

  # < CRITERIA 1 >
  # OTIS must approx. ALL truncated intervals
  for itvl in set_intervals:
    if do_once==0:
      OTIS = fareyApprox(itvl,doDeepPrint,embedded=True)
      OTIS.discard((0,1)) # OTIS non-zero
      do_once=1
    else:
      OTIS &= fareyApprox(itvl,doDeepPrint,embedded=True) # intersection <- OTIS shared by all

  cond_print(f"OTIS candidate(s) fitting crit#1: {ratListStr(OTIS)}\n")


  # < CRITERIA 2 >
  # [time_elapsed] must be valid approximation of [num_intervals*OTIS], given max possible rounding error during measurement of start and end times

  time_elapsed = round(list_times[len(list_times)-1]-list_times[0],num_decimals_MAX)
  num_intervals = len(list_intervals)
  threshold = 10**(-1*num_decimals_MIN)

  for candidate in set(OTIS): # Note: set(OTIS) to make copy of set, to avoid concurrent thread error when discarding candidates from original set
    cond_print(f"Measured time elapsed: {time_elapsed}")
    theoretical_time_elapsed = num_intervals*_fltVal(candidate)
    difference = abs(time_elapsed - theoretical_time_elapsed)
    if difference > threshold :
      OTIS.discard(candidate)
      cond_print(f"INVALID candidate: {_ratStr(candidate)} = {_fltVal(candidate)}")
    else :
      cond_print(f" VALID  candidate: {_ratStr(candidate)} = {_fltVal(candidate)}")

  cond_print("")

  if doPrint :
    print("OTIS candidate(s) fitting ALL criteria:",ratListStr(OTIS))
    if len(OTIS)>1 : print("More than 1 Original Time Interval Setting found: check original measurement device calibration to best confirm.")
    elif len(OTIS)<1 : print("This method did not find any Original Time Interval Setting values, either due to algorithm flaw OR non-constant OTIS: check original measurement device calibration (in real life) to best confirm.")
    else : print("Exactly 1 Original Time Interval Setting found: best case scenario, may utilize for further computation.")
  else :
    if len(OTIS)>0 : print("Very good time interval(s):",ratListStr(OTIS))
    else : print("This algorithm didn't find any good time intervals. Retry with message printing on, or check original measurement device calibration (in real life) to best confirm.")

  cond_print("\n. . .\n\n")

  return OTIS

def HELP_MSG() :
  print("""
  Help Message for FareyTime.py by Nana Kiziriya:

    fareyApprox(x:float,doPrint:bool) -> set:
      - returns (set) of good rational approximations for (x), using concepts from Diophantine approximation, particulary Farey neighbors/mediants
      - approximations range from (round(x)) to (x), in terms of precision
      - criteria: minimize (score), defined as (error)*(denominator)
          I came up with this criteria myself :) Balances goal of minimizing error and minimizing denominator.
          The choice of multiplication balances scale better than addition does, and provides stopping condition of (score==0)
      - see function in source code for further notes on implementation...

    findOTIS(series_times:pd.Series, doPrint:bool, doDeepPrint:bool):
      - LEVERAGES fareyApprox()
      - returns (set) of good rational approximations - ideally just 1 tho - for a time-precise measurement device's original time interval setting (OTIS)
      - further notes:
          # OTIS - Original Time Interval Setting
          # PURPOSE:
            # Accepts ordered list (or pd.series) of truncated time interval measurements
            # Finds original (rational) time interval using Farey neighbors/mediants
          # TESTING CRITERIA:
            # 1. OTIS must approx. ALL truncated intervals
            # 2. [time_elapsed] must be valid approximation of [num_intervals*OTIS], given max possible rounding error during measurement of start and end times
              # Note: given [num_decimals_MIN] (min decimal accuracy of measurement device), the overall error (btwn [time_elapsed] and [num_intervals*OTIS]) must be no more than 10**(-1*num_decimals_MIN), because measurement rounding of start and end times each contribute at MOST half of that
          # REQUIRED ASSUMPTIONS:
            # Original measurement device measures at precise time intervals
            # Error is only a result of truncation
            # Time intervals are (originally) all equal
            # time intervals are non-zero
            # Measurement device may round to fixed number of sigfigs, not fixed number of decimal places (i.e. num decimal places can decrease over time)
  """)
