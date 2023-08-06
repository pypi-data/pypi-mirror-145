from numpy.random import default_rng
from numpy.random import SeedSequence

def initialise (entropy=None) :
  '''
  Seed (if needed) and return a random state generator.
  '''

  if entropy is None :
    sq = SeedSequence ()
    entropy = sq.entropy
  rng = default_rng (entropy)

  return rng, entropy

