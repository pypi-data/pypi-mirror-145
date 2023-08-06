from re import sub as resub

tr_char = "ğĞüÜşŞıİöÖçÇ"
en_char = "gGuUsSiIoOcC"

def rename_file(filename):
  filename = list(filename)
  for x in range(len(filename)):
    if filename[x] in tr_char:
      filename[x] = en_char[tr_char.index(filename[x])]
  filename = "".join(t for t in filename)
  return resub("[^a-zA-Z0-9 \n\.]", "", filename)