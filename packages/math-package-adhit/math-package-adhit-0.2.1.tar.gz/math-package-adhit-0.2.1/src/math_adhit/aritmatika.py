def penjumlahan(a, b):
    try:
    return a + b
  except ValueError:
     return None
  except ZeroDivisionError:
      return 0
def pengurangan(a, b):
    try:
    return a - b
  except ValueError:
     return None
  except ZeroDivisionError:
      return 0
def perkalian(a, b):
    try:
    return a * b
  except ValueError:
     return None
  except ZeroDivisionError:
      return 0
def pembagian (a, b):
    try:
    return a / b
  except ValueError:
     return None
  except ZeroDivisionError:
      return 0