import os

a = "MyIAYoloTeam.pt"

for root, dirs, files in os.walk(r'C:/Users'):
    for name in files:
        if name == a:
            print(os.path.abspath(os.path.join(root, name))
)


             