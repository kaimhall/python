import pygame
import time
import random

class GoldMaze:
    def __init__(self):
        pygame.init()
        
        self.kello = pygame.time.Clock()
        
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
        
        self.kolikot = 5
        self.lapi = False
        self.loppu = False
        self.kuollut = False
        
        self.lataa_kuvat()
        self.uusi_peli()
       
        self.korkeus = len(self.kartta)
        self.leveys = len(self.kartta[0])
        self.skaala = self.kuvat[0].get_width()

        nayton_korkeus = self.skaala * self.korkeus
        nayton_leveys = self.skaala * self.leveys
        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus + self.skaala))
        self.fontti = pygame.font.SysFont("Arial", 24)
        
        pygame.display.set_caption("Robo Gold Maze")
        
        self.ovi_y, self.ovi_x = self.etsi_ovi()
        self.nayta_ovi()
        self.silmukka()

    def lataa_kuvat(self):
        self.kuvat = []
        koko = (40, 40)

        lattia = pygame.Surface(koko)
        lattia.fill((0,0,0))
        self.kuvat.append(lattia)
        
        seina = pygame.Surface(koko)
        seina.fill((105,105,105))
        self.kuvat.append(seina)    
        
        robo = pygame.image.load("robo.png")
        robo = pygame.transform.scale(robo, koko)
        self.kuvat.append(robo)

        hirvio = pygame.image.load("hirvio.png")
        hirvio = pygame.transform.scale(hirvio, koko)
        self.kuvat.append(hirvio)

        kolikko = pygame.image.load("kolikko.png")
        kolikko = pygame.transform.scale(kolikko, koko)
        self.kuvat.append(kolikko)   
        
        ovi = pygame.image.load("ovi.png")
        ovi = pygame.transform.scale(ovi, koko)
        self.kuvat.append(ovi) 
    
    def uusi_peli(self):
        # taikanumerot: 0=lattia, 1=seinä, 2=robo, 3=morko, 4=kolikko, 5=ovi
        self.kartta = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 4, 0, 0, 0, 0, 0, 0, 1, 0, 5, 1, 4, 1],
                       [1, 0, 1, 2, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1],
                       [1, 3, 1, 1, 1, 0, 0, 0, 1, 0, 0, 3, 0, 1],
                       [1, 0, 0, 0, 0, 0, 1, 3, 0, 0, 1, 0, 1, 1],
                       [1, 0, 0, 0, 1, 1, 1, 4, 0, 0, 1, 0, 0, 1],
                       [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
                       [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 3, 1, 1],
                       [1, 4, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 4, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            
            if tapahtuma.type == pygame.QUIT:
                exit()
            
            if tapahtuma.type == pygame.KEYDOWN:
                
                if tapahtuma.key == pygame.K_LEFT:
                    self.siirra_robo(0,-1)
                
                if tapahtuma.key == pygame.K_RIGHT:
                    self.siirra_robo(0,1)
                
                if tapahtuma.key == pygame.K_UP:
                    self.siirra_robo(-1,0)
                
                if tapahtuma.key == pygame.K_DOWN:
                    self.siirra_robo(1,0)

                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
            
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()

            if tapahtuma.type == pygame.USEREVENT + 1:
                valinta = random.choice([1,2,3,4])
                morko_x = random.choice([-1,1])
                morko_y = random.choice([-1,1])
                
                if valinta == 1:
                    self.siirra_morko(0, morko_x)
                elif valinta == 2:
                    self.siirra_morko(morko_y, 0)
                if valinta == 3:
                    self.siirra_morko(0, morko_x)
                elif valinta == 4:
                    self.siirra_morko(morko_y, 0)

    def etsi_robo(self):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [2]:
                    return (y,x)

    def etsi_morko(self):
        morko = []
        for rivi in range(self.korkeus):
            for sarake in range(self.leveys):
                if self.kartta[rivi][sarake] in [3]:
                    morko.append((rivi,sarake))
        return morko
                    

    def etsi_ovi(self):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [5]:
                    ovi = (y,x)
                    return ovi

    def nayta_ovi(self):
        if self.lapi:
            self.kartta[self.ovi_y][self.ovi_x] = 5
        else:
            self.kartta[self.ovi_y][self.ovi_x] = 0

    def siirra_robo(self, siirra_robo_y, siirra_robo_x):
        
        if not self.kuollut and not self.loppu:
        
            vanha_y, vanha_x = self.etsi_robo()
            uusi_y = vanha_y + siirra_robo_y
            uusi_x = vanha_x + siirra_robo_x
            
            if self.kartta[uusi_y][uusi_x] == 1: return
            
            elif self.kartta[uusi_y][uusi_x] == 3:
                self.kartta[vanha_y][vanha_x] = 0
                self.kartta[uusi_y][uusi_x] = 3
                self.kuolema()

            elif self.kartta[uusi_y][uusi_x] == 4:
                self.kartta[vanha_y][vanha_x] = 0
                self.kartta[uusi_y][uusi_x] = 2
                
                self.kolikot -= 1
                if self.kolikot == 0:
                    self.lapi = True
                    self.nayta_ovi()

            elif self.kartta[uusi_y][uusi_x] == 5 and self.kolikot == 0:
                self.kartta[vanha_y][vanha_x] = 0
                self.kartta[uusi_y][uusi_x] = 5
                self.the_end()

            else:
                self.kartta[vanha_y][vanha_x] = 0
                self.kartta[uusi_y][uusi_x] = 2

    def siirra_morko(self, siirra_morko_y, siirra_morko_x):
        morot = self.etsi_morko()
        print(morot)
        idx = random.randint(0,4)
        
        vanha_y, vanha_x = morot[idx]
        uusi_y = vanha_y + siirra_morko_y
        uusi_x = vanha_x + siirra_morko_x
        
        if self.kartta[uusi_y][uusi_x] == 1: return
        elif self.kartta[uusi_y][uusi_x] == 4: return
        elif self.kartta[uusi_y][uusi_x] == 5: return #kaatuu kun morko jää ilmestyvän oven alle
        elif self.kartta[uusi_y][uusi_x] == 3: return
        
        else:
            self.kartta[vanha_y][vanha_x] = 0
            self.kartta[uusi_y][uusi_x] = 3
    
    def the_end(self):
        self.loppu = True
        return self.loppu

    def kuolema(self):
        self.kuollut = True
        return self.kuollut

    def piirra_naytto(self):
        self.naytto.fill((0, 0, 0))

        for y in range(self.korkeus):
            for x in range(self.leveys):
                ruutu = self.kartta[y][x]
                self.naytto.blit(self.kuvat[ruutu], (x * self.skaala, y * self.skaala))

        if self.lapi == False:    
            teksti = self.fontti.render("Get the Gold!", True, (255, 255, 255))
            self.naytto.blit(teksti, (25, self.korkeus * self.skaala + 10))
        else:    
            teksti = self.fontti.render("Escape!", True, (255, 255, 255))
            self.naytto.blit(teksti, (25, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("F2 = uusi peli", True, (105, 105, 105))
        self.naytto.blit(teksti, (200, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("Esc = sulje peli", True, (105, 105, 105))
        self.naytto.blit(teksti, (400, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("Kolikoita jäljellä: " + str(self.kolikot), True, (255, 255, 255))
        self.naytto.blit(teksti, (0 + 40 ,0 +5))

        if self.loppu:
            teksti = self.fontti.render("You made it!!!", True, (255, 255, 255))
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))
        
        if self.kuollut:            
            teksti = self.fontti.render("You did not make it!!!", True, (255, 255, 255))
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))

        pygame.display.flip()
        self.kello.tick(24)

if __name__ == "__main__":
    GoldMaze()