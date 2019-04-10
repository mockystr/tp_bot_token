import pickle

obj = {'asd': 1, 'case': 2}
print(obj)
obj = pickle.dumps(obj)
print(obj)
obj = pickle.loads(obj)
print(obj)