import requests
from bs4 import BeautifulSoup

import latestEarthquakeID

description = 'To get latest indonesian earthquake information from BMKG.go.id'


def ekstraksi_data():
    """
    Tanggal : 22 Januari 2022
    Waktu : 15:34:38 WIB
    Magnitudo : 3.9
    Kedalaman : 10 km
    Lokasi : 7.49 LS - 107.31 BT
    Pusat_gempa : Pusat gempa berada di darat 57 km BaratDaya Kab-Bandung
    Diraskan : Dirasakan (Skala MMI): III Cidaun, III Cidora, III Cijayanti, III Rancabuaya, II Pamengpeuk, II Pakenjeng, II Bungbulang, II Cisompet, II Margaasih
    :return:
    """
    try:
        content = requests.get('https://www.bmkg.go.id/')
    except Exception:
        return None
        print(Exception)

    if content.status_code == 200:
        # print(content.text)
        soup = BeautifulSoup(content.text, "html.parser")
        result = soup.find('span', {'class': 'waktu'})
        result = result.text.split(', ')
        tanggal = result[0]
        waktu = result[1]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        i = 0
        magnitudo = None
        kedalaman = None
        ls = None
        bt = None
        pusat = None
        dirasakan = None

        for res in result:
            # print(i, res)
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                pusat = res.text
            elif i == 5:
                dirasakan = res.text
            i = i + 1

        hasil = dict()
        hasil['Tanggal'] = tanggal
        hasil['Waktu'] = waktu
        hasil['Magnitudo'] = magnitudo
        hasil['Kedalaman'] = kedalaman
        hasil['Lokasi'] = {'LS': ls, 'BT': bt}
        hasil['Pusat'] = pusat
        hasil['Dirasakan'] = dirasakan
        return hasil
    else:
        return None


def tampilkan_data(result):
    if result is None:
        print("Data tidak ditemukan")
        return

    print("Gempa terakhir bersarkan data BMKG")
    print(f"Tanggal     : {result['Tanggal']}")
    print(f"Waktu       : {result['Waktu']}")
    print(f"Magnitudo   : {result['Magnitudo']}")
    print(f"Kedalaman   : {result['Kedalaman']}")
    print(f"Lokasi      : {result['Lokasi']['LS']}, {result['Lokasi']['BT']}")
    print(f"Pusat       : {result['Pusat']}")
    print(f"Dirasakan   : {result['Dirasakan']}")


if __name__ == '__main__':
    # print('Aplikasi Utama')
    print('Deskripsi package', description)
    result = latestEarthquakeID.ekstraksi_data()
    latestEarthquakeID.tampilkan_data(result)
