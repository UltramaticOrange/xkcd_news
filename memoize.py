class memoize(object):
  def __init__(self, maxCacheSize=255):
    self.maxCacheSize = maxCacheSize
    self.cache = {}
    self.addOrder = []

  def __call__(self, f):
    def wrapper(*args, **kwargs):
      key = (args, tuple(kwargs.keys()), tuple(kwargs.values()))
      if key not in self.cache:
        self.cache[key] = f(*args, **kwargs)
        self.addOrder.append(key)

      if len(self.addOrder) > self.maxCacheSize:
        self.cache.pop(self.addOrder[0])
        self.addOrder = self.addOrder[1:]

      return self.cache[key]
    return wrapper
