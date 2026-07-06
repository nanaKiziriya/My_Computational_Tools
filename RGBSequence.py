import numpy as np

A = 3*255/np.pi
B = np.pi/6
D = 255/2


_channel_fncts = {
  'pure' : # linear piecewise, ~plateaus
    lambda c,t,mlt,mx : max(0,min(255,int(np.round( (mlt*A*np.arcsin(np.cos(B*(t-4*c))**(2*mx+1))+D) )))),
  'visible' : # sinusoidal, ~curves
    lambda c,t,mlt,mx : max(0,min(255,int(np.round( (mlt*255/2*np.cos(B*(t-4*c))**(2*mx+1)+D)))))
}
# channel  R y G c B m (R
#     c =  0   1   2   (3
#   4*c =  0   4   8   (12
# NOTE: chnl_mix=2*mx+1 in theory only needs to be a rational>=1 with odd numerator and denominator. I'm using odd integers because I'm lazy.



def color_sequence(num_colors=12, start=0, end=0,
                   exclude_end=True, reverse=False, ver='pure',
                   alpha=255, channels=(0,1,2), chnl_mult=1, chnl_mix=0) :

  # check format of arguments
  assert ver in _channel_fncts.keys(), f'ver must be in {_channel_fncts.keys()}'
  assert isinstance(num_colors,int) and num_colors>0, 'num_colors must be positive int'
  assert (isinstance(start,int) or isinstance(start,float)) and (isinstance(end,int) or isinstance(end,float)), 'start and end must be number in [0,12)'
  assert start>=0 and end<12, 'start and end must be in [0,12)'
  assert isinstance(exclude_end, bool), 'exclude_end must be bool'
  assert isinstance(reverse, bool), 'reverse must be bool'
  assert 0<=alpha and alpha<=255, 'alpha channel must be in [0,255]'
  assert len(channels)==3 and all(0<=_ and _<3 for _ in channels), 'channel must be 3-tuple of numbers in [0,3)'

  try : len(chnl_mult)
  except : chnl_mult = [chnl_mult]*3
  assert len(chnl_mult)==3, 'chnl_mult must be 1-or-3-tuple of numbers'

  try : len(chnl_mix)
  except : chnl_mix = [chnl_mix]*3
  assert len(chnl_mix)==3 and all(0<=_ and isinstance(_,int) for _ in chnl_mix), 'chnl_mix must be 1-or-3-tuple of non-negative integers'

  # Adjust end
  if end<=start : end+=12
  if exclude_end : end -= (end-start)/n

  # MAP: index -> time, for color fnct input
  my_colors = map(
      lambda _ : _*(end-start)/(n-1)+start,
      range(num_colors))

  # MAP: time -> rgba, (rrr,ggg,bbb), w/ chnl_mult
  my_colors = map(
      lambda t : tuple(map( _channel_fncts[ver], channels, [t]*3, chnl_mult,chnl_mix)),
      my_colors)
  
  # MAP: rgb -> rgba, (rrr,ggg,bbb,aaa)
  my_colors = map(
      lambda rgb : rgb+tuple([alpha]),
      my_colors)
  
  # MAP: rgba -> hex, '#rrggbbaa'
  my_colors = map(
      lambda rgba:'#'+''.join(tuple(map(
          lambda _:"{:02x}".format(_),
          rgba))),
      my_colors)
  
  # Final touches
  my_colors = tuple(my_colors)
  if reverse : my_colors = tuple(reversed(my_colors))
  
  
  return my_colors
