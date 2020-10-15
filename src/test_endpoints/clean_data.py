import re

pattern = r"(^([\S]+))|(?<=\()(.*?)(?=\))|(?<=\:)(.*?)(?=\.\.\.)(^([\S]+))|(?<=\()(.*?)(?=\))|(?<=\:)(.*?)(?=\.\.\.)"

data = []

with open("time.txt","r") as f:
   for line in f:
      valid_data = [val.strip() for tup in re.findall(pattern,line) for val in tup if len(val)>0][1:]
      if len(valid_data) == 4:
         data.append(valid_data)
      else:
         break

with open("time.csv","a") as f:
   print("Function,Class,Description,Time",file=f)

   for d in data:
      print(",".join(d),file=f)