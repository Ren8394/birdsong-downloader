# Birdsong-Downloader

---
In our project, [birdsong-classification](https://github.com/Ren8394/birdsong-classification), Our data is recorded by the passive monitoring device so the audio is usually vague. To obtain clear audio of the birdsong, we decided to download audio from open source websites, Xeno-Canto and eBird.

Adventages:

* Easily to label
* Better quality

Open Source:  

1. Xeno-Canto (Use API)
   1. [Xeno-Canto API v2](https://xeno-canto.org/explore/api)
2. eBird (Use Crawler - [chromedriver](https://chromedriver.chromium.org/))
   1. Parse science name to [taxonomy Code](https://www.birds.cornell.edu/clementschecklist/download/)
   2. Construct request urls and start crawling

## Target Species

---
| Code  | Generic Name | Specific Name |
| :---: | :----------: | :-----------: |
|  YB   |    Yuhina    |  brunneiceps  |
|  AA   |  Abroscopus  |  albogularis  |
|  HA   | Heterophasia |  auricularis  |
|  CR   |  Cyanoderma  |   ruficeps    |
|  ML   |   Myiomela   |    leucura    |
|  LS   |  Liocichla   |    steerii    |
|  BG   | Brachypteryx |  goodfellowi  |
|  PAL  |   Pnoepyga   |   formosana   |
|  FH   |   Ficedula   |  hyperythra   |
|  NV   |   Niltava    |    vivida     |
|  PS   | Pericrocotus |    solaris    |
|  PM   |    Parus     |  monticolus   |
|  ME   | Erythrogenys | erythrocnemis |
|  AC   | Arborophila  | crudigularis  |
|  SE   |    Sitta     |   europaea    |
|  PA   |  Periparus   |     ater      |

## How to Use

---
(defaults --> country: Taiwan, audio type: song)

* Add "eBird Code" to get eBird audio.
* Add "sci Name" to get xeno-canto audio.
* To custom you target:
  * Adjust `ConstructRequestUrl` in [ebird-birdsong](ebird-birdsong.py)
  * Adjust `ConstructRequestUrl` in [xeno-birdsong](xeno-birdsong.py)
