import json

a = {'aaa', 2}
b = json.dumps(a)
c = json.loads(b)

print(b)
print(type(c))