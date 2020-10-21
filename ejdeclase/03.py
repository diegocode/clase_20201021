estudiantes = []

while True:
    nombre = input("nombre> ")
    if nombre == "":
        break
    estudiantes.append(nombre)

for p in sorted(estudiantes):
    print(p)
