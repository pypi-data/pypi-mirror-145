import koji

s = koji.ClientSession("https://localhost:8081/kojihub")
print(s.getBuild(1))
print(s.getBuild(1))
print(s.getBuild(1))
