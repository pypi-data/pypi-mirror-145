# latest-earthquake-indonesia
This package will get the latest earthquake from BMKG | Indonesian Agency for Meteorological, Climatological and Geophysics 

## HOW IT WORK?
This Package will scrape from [BMKG](https://bmkg.go.id) to get latest Quake happened in Indonesia

Thisa package will use BeatifulSoup4 and Request, to produce output in the form of JSON that is ready to be used in web or mobile application

## HOW TO USE
'''

import gempaterkini
if __name__ == '__main__':
    print('Aplikasi utama')
    result = gempaterkini.ekstraksi_data()
    gempaterkini.tampilkan_data(result)

'''

