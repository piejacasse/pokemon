from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

data = [
[1,1,1,1,1,1/2,1,0,1,1,1,1,1,1,1],
[2,1,1/2,1/2,1,2,1/2,0,1,1,1,1,1/2,2,1],
[1,2,1,1,1,1/2,2,1,1,1,2,1/2,1,1,1],
[1,1,1,1/2,1/2,1/2,2,1/2,1,1,2,1,1,1,1],
[1,1,0,2,1,2,1/2,1,2,1,1/2,2,1,1,1],
[0,1/2,2,1,1/2,1,2,1,2,1,1,1,1,2,1],
[1,1/2,1/2,2,1,1,1,1/2,1/2,1,2,1,2,1,1],
[0,1,1,1,1,1,1,2,1,1,1,1,0,1,1],
[1,1,1,1,1,1/2,2,1,1/2,1/2,2,1,1,2,1/2],
[1,1,1,1,2,2,1,1,2,1/2,1/2,1,1,1,1/2],
[1,1,1/2,1/2,2,2,1/2,1,1/2,2,1/2,1,1,1,1/2],
[1,1,2,1,0,1,1,1,1,2,1/2,1/2,1,1,1/2],
[1,2,1,2,1,1,1,1,1,1,1,1,1/2,1,1],
[1,1,2,1,2,1,1,1,1,1/2,2,1,1,1/2,2],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]
]

headers = ["Normal","Fight","Flying","Poison","Ground","Rock","Bug","Ghost","Fire","Water","Grass","Electric","Psychic","Ice","Dragon"]

# defending = {}
# attacking = {}
# for pouic in range(len(data)):
#     ligne = data[pouic]
#     print(f"ligne:{ligne}")
#     truc = ligne[pouic]
#     key = headers[pouic]
#     value = truc
#     defending[key] = value
#     print(f"defending:{defending}")
#     key = headers[pouic]
#     value = defending
#     attacking[key] = value

# print(f"attacking:\n{attacking}")
# Console().print(attacking)

defending = {}
attacking = {}
for pouic in range(len(data)):
    ligne = data[pouic]
    print(f"###NOUVELLE LIGNE####:{ligne}")
    for nombre in range(len(ligne)):
        print(f"ligne:{ligne}")
        key = headers[nombre]
        value = ligne[nombre]
        defending[key] = value
        print(f"defending:{defending}")
        key = headers[nombre]
        value = defending
        attacking[key] = value
    #on ne veut pas tout le tableau mais juste une ligne avec son type, qu'on ajoutera au dico à chaque loop
    print(f"attacking:{attacking}")

# print(f"attacking:\n{attacking}")
