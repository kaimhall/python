#%%
import json
class Tilasto:
    def __init__(self):
        self.pelaajat = []
    
    def hae_data(self):
        t_nimi = input('tiedosto: ')
        try:
            with open(t_nimi) as tiedosto:
                data = tiedosto.read()
                tiedot = json.loads(data)
                for pelaaja in tiedot:
                    self.pelaajat.append(pelaaja)
                print(f'luettiin {len(self.pelaajat)} pelaajan tiedot\n')
        except IOError:
            print('problem!')
    
    def hae_pelaaja(self):
        nimi = input('nimi: ')
        l = [(pelaaja['name'], pelaaja['team'], pelaaja['assists'], pelaaja['goals'], pelaaja['goals'] + pelaaja['assists']) for pelaaja in self.pelaajat if pelaaja['name'] == nimi]
        for p in l:
            print(f'{p[0]:<20} {p[1]} {p[3]:>3} + {p[2]:} = {p[4]:>3}')
    
    def hae_joukkueet(self):
        l = list(set([pelaaja.get('team') for pelaaja in self.pelaajat]))
        l.sort()
        for joukkue in l:
            print(joukkue)

    def hae_maat(self):
        l = list(set([pelaaja.get('nationality') for pelaaja in self.pelaajat]))
        l.sort()
        for maa in l:
            print(maa)

    def hae_joukkueen_pelaajat(self):
        joukkue = input('joukkue: ')
        l = [(pelaaja['name'], pelaaja['team'], pelaaja['assists'], pelaaja['goals'], pelaaja['goals'] + pelaaja['assists']) for pelaaja in self.pelaajat if pelaaja['team'] == joukkue]
        
        for p in sorted(l, key= lambda p: p[2] + p[3]):
            print(f'{p[0]:<20} {p[1]} {p[3]:>3} + {p[2]:} = {p[4]:>3}')
    
    def hae_maan_pelaajat(self):
        maa = input('joukkue: ')
        l = [(pelaaja['name'], pelaaja['team'], pelaaja['assists'], pelaaja['goals'], pelaaja['goals'] + pelaaja['assists']) for pelaaja in self.pelaajat if pelaaja['nationality'] == maa]
        
        for p in sorted(l, key= lambda p: p[2] + p[3]): 
            print(f'{p[0]:<20} {p[1]} {p[3]:>3} + {p[2]:} = {p[4]:>3}') 

    def max_pisteet(self):
        maara = int(input('kuinka monta: '))
        l = [(pelaaja['name'], pelaaja['team'], pelaaja['assists'], pelaaja['goals'], pelaaja['goals'] + pelaaja['assists']) for pelaaja in self.pelaajat] 
        l = sorted(l, key= lambda p: p[2] + p[3], reverse= True) 
        for p in l[0:maara]:
            print(f'{p[0]:<20} {p[1]} {p[3]:>3} + {p[2]:} = {p[4]:>3}')

    def max_maalit(self):
        maara = int(input('kuinka monta: '))
        l = [(pelaaja['name'], pelaaja['team'], pelaaja['assists'], pelaaja['goals'], pelaaja['goals'] + pelaaja['assists']) for pelaaja in self.pelaajat] 
        l = sorted(l, key= lambda p: p[3], reverse= True) 
        for p in l[0:maara]:
            print(f'{p[0]:<20} {p[1]} {p[3]:>3} + {p[2]:} = {p[4]:>3}')

    def ohje(self):
        print("komento:")
        print("0 lopetus")
        print("1 hae pelaaja")
        print("2 joukkueet")
        print("3 maat")
        print("4 joukkueen pelaajat")
        print("5 maan pelaajat")
        print("6 eniten pisteitä")
        print("7 eniten maaleja")
        
    def suorita(self):
        self.ohje()
        while True:
            print("")
            komento = input("komento: ")
            if komento == "0": break
            elif komento == "1": self.hae_pelaaja()
            elif komento == "2": self.hae_joukkueet()
            elif komento == "3": self.hae_maat()
            elif komento == "4": self.hae_joukkueen_pelaajat()
            elif komento == "5": self.hae_maan_pelaajat()
            elif komento == "6": self.max_pisteet()
            elif komento == "7": self.max_maalit()
            self.ohje()

def main():
    nhl = Tilasto()
    nhl.hae_data()
    nhl.suorita()
    

if __name__ == '__main__':
    main()
# %%
