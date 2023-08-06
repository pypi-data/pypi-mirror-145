__version__ = '0.1.0'
def _get_var_type(code):
  type = []
  i = 0
  while True:
    if code[i] == " ":
      break
    else:
      type.append(code[i])
      i += 1
  type = str(type)
  type = remove(type)
  return [type, code.replace(type + " ", "")]
def _get_var_name(code):
  name = []
  i = 0
  while True:
    if code[i] == " ":
      break
    else:
      name.append(code[i])
      i += 1
  name = str(name)
  name = remove(name)
  return [name, code.replace(name + " ", "")]
def _get_var_value(code):
  value = code.replace("= ", "")
  return value