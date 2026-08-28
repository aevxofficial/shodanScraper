from file.scrape.session import ScraperSession
import json,time,random
from bs4 import BeautifulSoup

class Scraper(ScraperSession):
    def __init__(self):
        super().__init__()

    def KaydetJson(self, veri, dosya_adi="sonuc.json"):
        with open(dosya_adi, "w", encoding="utf-8") as dosya:
            json.dump(veri, dosya, ensure_ascii=False, indent=2)
        
    def Dashboard(self):
        url = self.config["base_url"] + self.config["dashboard_url"]
        
        return self.session.get(url)
        
    def Sorgu(self, ara, filtre=False):
        url = self.config["base_url"] + self.config["query_url"]
        
        if filtre:
            filtre_text = ",".join(filtre)
    
            payload = {
                "query": f'{ara} -net:{filtre_text}',
            }
            
            print(payload)
        else:
            payload = {
                "query": f'{ara}',
            }
            print(payload)
        
        sorgu = self.session.get(
            url,
            params=payload
        )
        
        return sorgu.text
    
    def SorguParse(self, sorgu):
        
        parser = BeautifulSoup(sorgu, "html.parser")
        
        check = parser.find("div",attrs={"class": "alert"})
        if check:
            return False
            
        adet = parser.find("h4", attrs={"class": "total-results"})
        icerikler = parser.find_all("div", attrs={"class": "result"})
        sonuclar = []

        for i in icerikler:
            ad = i.find("a",attrs={"class": "title"})
            link_tag = i.find("a",attrs={"class": "text-danger"})

            title = ad.get_text(strip=True) if ad else None
            link = link_tag.get("href") if link_tag else None

            sonuclar.append({
                "title": title,
                "link": link
            })
        
        print(adet.text.strip() if adet else "0")
        return {
            "adet": int((adet.text.strip().replace(",",""))),
            "sonuçlar": sonuclar
        }
    
    def ScrapeSorgu(self, ara):
        self.Dashboard()
        
        self.sonuclar = []
        
        self.filtreList = []
        
        self.adet = 1

        while True:
            self.sorgula = self.Sorgu(ara,self.filtreList)
            time.sleep(random.randint(1,3))
            self.parseEt = self.SorguParse(self.sorgula)
            
            if not self.parseEt:
                print("Bitti")
                print(self.sonuclar)
                self.KaydetJson(self.sonuclar)
                return self.sonuclar
            
            linkler = self.parseEt["sonuçlar"]
            sonuc_adet = self.parseEt["adet"]
            
            print(sonuc_adet)
            
            if sonuc_adet == 1:
                self.KaydetJson(self.sonuclar)
                break
            
            print(self.adet ,"Adet Veri Çekildi")
            self.adet += 1
            
            if not self.parseEt:
                self.KaydetJson(self.sonuclar)
                break
            
            for i in linkler:
                title = i.get("title")
                link = i.get("link")

                self.sonuclar.append({
                 "Başlık": title,
                 "Url": link
                })

                if not link:
                    continue
                  
                if "." in link:
                    host = link.split("//")[1].split(":")[0]
                elif "[" in link and "]" in link:
                    host = link.split("[")[1].split("]")[0]
                else:
                    continue

                self.filtreList.append(host)
                 
            print(self.sonuclar)
            self.KaydetJson(self.sonuclar)
            
        self.KaydetJson(self.sonuclar)
        return self.sonuclar
    
    