import requests
from bs4 import BeautifulSoup


"""
Method = fungsi 
Field/Atribut = variabel
Constructor = method yang pertama kali dipanggil saat object diciptakan untuk medeklarasikan semua variabel/field pada 
kelas ini 

"""

class Bencana:
    def __init__(self, url, description):
        self.description = description
        self.result = None;
        self.url = url

    def tampilkan_keterangan(self):
        print(self.description)


    def scrapping_data(self):
        pass

    def tampilkan_data(self):
        pass

    def run(self):
        self.scrapping_data()
        self.tampilkan_data()


class  GempaTerkini(Bencana):

    def __init__(self, url):
        super(GempaTerkini, self).__init__(url, 'To get the lastest earthquake in Indonesia from BMKG.go.id')

    def scrapping_data(self):
        try:
            content = requests.get(self.url)
        except Exception:
            self.result =  None
        if content.status_code == 200:
            soup = BeautifulSoup(content.text, 'html.parser')
            result = soup.find('span', {'class': 'waktu'})
            result = result.text.split(', ')
            waktu = result[1]
            tanggal = result[0]
            result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            result = result.findChildren('li')


            i = 0
            magnitudo = None
            ls = None
            bt = None
            pusat = None
            dirasakan = None
            lokasi = None

            for res in result:
                if i == 1:
                    magnitudo = res.text
                elif i == 2:
                    kedalaman = res.text
                elif i == 3:
                    koordinat = res.text.split(' - ')
                    ls = koordinat[0]
                    bt = koordinat[1]

                elif i == 4:
                    lokasi = res.text

                elif i == 5:
                    dirasakan = res.text

                i = i + 1
            hasil = dict()
            hasil['tanggal'] = tanggal
            hasil['waktu'] = waktu
            hasil['magnitudo'] = magnitudo
            hasil['kedalaman'] = kedalaman
            hasil['koordinat'] = {'ls': ls, 'bt': bt}
            hasil['lokasi'] = lokasi
            hasil['dirasakan'] = dirasakan
            self.result = hasil
        else:
            return None


    def tampilkan_data(self):
        if self.result is None:
            print('Tidak bisa menemukan data gempa terkini')
            return
        print('Gempa terakhir berdasarkan data BMKG')
        print(f"Tanggal, {self.result['tanggal']}")
        print(f"waktu, {self.result['waktu']}")
        print(f"Magnitudo, {self.result['magnitudo']}")
        print(f"kedalaman, {self.result['kedalaman']}")
        print(f"koordinat: {self.result['koordinat']['ls']}, {self.result['koordinat']['bt']}")
        print(f"Lokasi: {self.result['lokasi']}")
        print(f"Dirasakan, {self.result['dirasakan']}")

class BanjirTerkini(Bencana):
    def __init__(self, url):
        super(BanjirTerkini, self).__init__(url, 'Not yet implementad, but it should return last flood in Indonesia')



if __name__ == '__main__':
    gempa_di_indeonesia = GempaTerkini('https://bmkg.go.id')
    gempa_di_indeonesia.tampilkan_keterangan()
    gempa_di_indeonesia.run()

    banjir_di_indonesia = BanjirTerkini('\n Not Yet')
    banjir_di_indonesia.tampilkan_keterangan()


