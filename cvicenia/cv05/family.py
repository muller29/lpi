import os
import sys
sys.path[0:0] = [os.path.join(sys.path[0], '../../examples/sat')]
import sat

w = sat.DimacsWriter("family_in.txt")


Dorothy = 0
Virginia = 1
George = 2
Howard = 3
mena = ['Dorothy','Virginia','George','Howard']
muzi = [George, Howard]
zeny = [Dorothy, Virginia]

def otec(x):
    return x+1
def matka(x):
    return 4+x+1
def syn(x):
    return 8+x+1
def dcera(x):
    return 12+x+1
def pb(x,y):
    return 16 + 4*x + y +1
def st(x,y):
    return 32 + 4*x + y +1
def ml(x,y):
    return 48 + 4*x + y +1

roly = ['otec','matka','syn','dcera']

class Family:

    def solve():
        #zeny nesmu byt otcom, ani synom
        for i in zeny:
            w.writeClause([-otec(i)])
            w.writeClause([-syn(i)])

        #muzi semu byt matkou, ani dcerou
        for i in muzi:
            w.writeClause([-matka(i)])
            w.writeClause([-dcera(i)])

        #nikto nesmie byt otcom aj synom naraz, ani matkou a dcerou
        w.writeClause([-otec(Howard), -syn(Howard)])
        w.writeClause([-otec(George), -syn(George)])
        w.writeClause([-matka(Dorothy), -dcera(Dorothy)])
        w.writeClause([-matka(Virginia), -dcera(Virginia)])

        #prave jeden otec, syn, matka, dcera        
        w.writeClause([otec(George), otec(Howard)])        
        w.writeClause([-otec(George), -otec(Howard)])
        w.writeClause([syn(George), syn(Howard)])
        w.writeClause([-syn(George), -syn(Howard)])
        w.writeClause([matka(Dorothy), matka(Virginia)])
        w.writeClause([-matka(Dorothy), -matka(Virginia)])        
        w.writeClause([dcera(Dorothy), dcera(Virginia)])        
        w.writeClause([-dcera(Dorothy), -dcera(Virginia)])


        x = [Dorothy, Virginia, George, Howard]

        for i in range(len(x)):
            for j in range(i, len(x)):
                #A je pokrvny pribuzni B ->
                w.writeClause([-pb(x[i], x[j]), -otec(x[i]), -matka(x[j])])
                #A je pokrvny pribuzni B <-
                w.writeClause([pb(x[i], x[j]), otec(x[i])])
                w.writeClause([pb(x[i], x[j]), matka(x[j])])
                #A je starsi nez B ->
                w.writeClause([-st(x[i], x[j]),otec(x[i])])
                w.writeClause([-st(x[i], x[j]),syn(x[j])])
                #A je starsi nez B <-
                w.writeClause([st(x[i], x[j]), -matka(x[i]), -dcera(x[j])])
                #A je mladsi nez B ->
                w.writeClause([-ml(x[i], x[j]), matka(x[i]), dcera(x[i])])
                w.writeClause([-ml(x[i], x[j]), otec(x[j]), dcera(x[i])])
                #A je mladsi nez B <-
                w.writeClause([ml(x[i], x[j]), -matka(x[i]),-otec(x[j])])
                w.writeClause([ml(x[i], x[j]), -dcera(x[i])])


        #George a Dorothy su pokrvni pribuzni
        t1 = pb(George, Dorothy)

        #Howard je starsi nez George
        t2 = st(Howard,George)

        #Virgina je mladsia nez Howard
        t3 = ml(Virginia, Howard)

        #Virginia je starsia nez Dorothy
        t4 = st(Virginia, Dorothy)

        #prave 2 t su pravdive
        t = [t1, t2, t3, t4]
        for i in range(len(t)):
            p = t[:]
            p.pop(i)
            w.writeClause([-p[0], -p[1], -p[2]])
            w.writeClause([p[0], p[1], p[2]])


        w.close()
        sats = sat.SatSolver()

        return sats.solve(w, "family.out.txt")


if __name__ == "__main__":
    ok, sol = Family.solve()
    if ok:
        tmp = []
        for i in range(16):
            if sol[i] > 0:
                tmp.append(sol[i])
        for i in range(4):
            tmp[i] -= 1
            tmp[i] -= i * 4
        print(tmp)
        print("otec - {0}".format(mena[tmp[1]]))
        print("matka - {0}".format(mena[tmp[2]]))
        print("syn - {0}".format(mena[tmp[0]]))
        print("dcera - {0}".format(mena[tmp[3]]))
    else:
        print("CHYBA")
