from tarantool import Connection

c = Connection('127.0.0.1', 3301)

result = c.insert("tester", (5, 'Emir Dj', 2000))
print(result)
