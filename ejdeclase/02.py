"""for c in "arbolito":
    if c in "aeiou":
        print(c*2)
    else:
        print(c)
"""

gente = ["ana", "pedro", 'Pablito']

temp = gente[0]
gente[0] = gente[-1]
gente[-1] = temp

print(gente)

