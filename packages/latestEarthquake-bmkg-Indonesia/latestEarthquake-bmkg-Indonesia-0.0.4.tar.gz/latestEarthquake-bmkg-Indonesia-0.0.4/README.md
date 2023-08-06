# latest-indonesia-earthquake
This package will get the latest earthquake in Indonesia from BMKG | Meteorological, Climatological, and Geophysical Agency

# How it works?
This package will scrape from [BMKG](https://www.bmkg.go.id/), to get the latest earthquake in Indonesia using **BeautifulSoup4** and **Request** to produce JSON as a return.

# How to use?
```
import latestEarthquakeID

if __name__ == '__main__':
    result = latestEarthquakeID.ekstraksi_data()
    latestEarthquakeID.tampilkan_data(result)
```

# Author
Theo Brata