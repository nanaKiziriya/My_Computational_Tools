import numpy as _np

_A = 3*255/_np.pi # (vertical) stretch altitude to 127.5, for linear ver.
_B = _np.pi/6 # (horizontal) stretch period to 12
_D = 255/2 # translates midline up to 127.5

_channel_fncts = lambda ver,c,t,mlt,xtrm,mx : max(0,min(255,int(_np.round(mlt*(xtrm* __fncts[ver]( _np.cos(_B*(t-4*c)) **(2*mx+1)) +_D) ))))

__fncts = {
  'line' : # linear piecewise, ~plateaus
    lambda _:_A*_np.arcsin(_),
  'sine' : # sinusoidal, ~curves
    lambda _:255/2*_
}

# channel  R y G c B m (R
#     c =  0   1   2   (3
#   4*c =  0   4   8   (12
# NOTE: chnl_mix=2*mx+1 in theory only needs to be a rational>=1 with odd numerator and denominator. I'm using odd integers because I'm lazy.



def color_sequence(num_colors=12, start=0, end=0,
                   exclude_end=True, reverse=False, ver='line',
                   alpha=255, channels=(0,1,2), chnl_mult=1, chnl_extreme=1, chnl_mix=0) :

  # start,end : ~ROYGBIV mod12, red=0
  # alpha : ~RGBA [0,255]
  # channels : set peak of RGB curve, mod3
  # chnl_mult : vertical stretch multiplier, higher highs
  # chnl_extreme : vertical stretch multiplier, higher highs and lower lows
  # chnl_mix : muddle colors, whole num

  # check format of arguments
  assert ver in __fncts.keys(), f'ver must be in {__fncts.keys()}'
  assert isinstance(num_colors,int) and num_colors>0, 'num_colors must be positive int'
  assert (isinstance(start,int) or isinstance(start,float)) and (isinstance(end,int) or isinstance(end,float)), 'start and end must be number in [0,12)'
  assert start>=0 and end<12, 'start and end must be in [0,12)'
  assert isinstance(exclude_end, bool), 'exclude_end must be bool'
  assert isinstance(reverse, bool), 'reverse must be bool'
  assert 0<=alpha and alpha<=255, 'alpha channel must be in [0,255]'
  assert len(channels)==3 and all(0<=_ and _<3 for _ in channels), 'channel must be 3-tuple of numbers in [0,3)'

  try : len(chnl_mult)
  except : chnl_mult = [chnl_mult]*3
  assert len(chnl_mult)==3, 'chnl_extreme must be 1-or-3-tuple of numbers'

  try : len(chnl_extreme)
  except : chnl_extreme = [chnl_extreme]*3
  assert len(chnl_extreme)==3, 'chnl_extreme must be 1-or-3-tuple of numbers'

  try : len(chnl_mix)
  except : chnl_mix = [chnl_mix]*3
  assert len(chnl_mix)==3 and all(0<=_ and isinstance(_,int) for _ in chnl_mix), 'chnl_mix must be 1-or-3-tuple of non-negative integers'

  # Adjust end
  if end<=start : end+=12
  if exclude_end : end -= (end-start)/num_colors

  # MAP: index -> time, for color fnct input
  my_colors = map(
      lambda _ : _*(end-start)/(num_colors-1)+start,
      range(num_colors))

  # MAP: time -> rgba, (rrr,ggg,bbb), w/ chnl_extreme
  my_colors = map(
      lambda t : tuple(map( _channel_fncts, [ver]*3, channels, [t]*3, chnl_mult,chnl_extreme,chnl_mix)),
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
