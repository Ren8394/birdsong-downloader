import pandas as pd
import requests
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from bs4 import BeautifulSoup as Soup
from pathlib import Path
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service

# ------------- 
def ConstructRequestUrl(taxonCode:str) -> str:
  baseUrl = 'https://media.ebird.org/catalog?'
  tag = 'song'
  regionCode = 'TW'
  return baseUrl + f'tag={tag}&regionCode={regionCode}&taxonCode={taxonCode}'

def GetMoreResultsButton(browser, cssSelector):
  try:
    button = browser.find_element_by_css_selector(cssSelector)
  except exceptions.NoSuchElementException:
    return
  else:
    return button

def GetSpeciesNextPagesUrl(driver, reqUrl, speciesCode):
  df = pd.DataFrame(columns=['code', 'page Url'])
  driver.get(reqUrl)
  button = GetMoreResultsButton(driver, '.pagination > button')
  while button is not None:
    button.click()
    button = GetMoreResultsButton(driver, '.pagination > button')
  
  soup = Soup(driver.page_source, 'lxml')
  nextPageUrls = soup.find_all('a', class_='ResultsGallery-link')
  for u in nextPageUrls:
    df = pd.concat(
      [df, pd.DataFrame({
        'code': speciesCode,
        'page Url': u.get('href')
      }, index=[0])],
      ignore_index=True
  )
  return df

def GetSpeciesAudioUrls(driver, reqUrls, speciesCodes):
  audioUrls = []
  for reqUrl, code in zip(reqUrls, speciesCodes):
    driver.get(reqUrl)
    soup = Soup(driver.page_source, 'lxml')
    if soup.find('audio') is not None:
      audioUrls.append(soup.find('audio').get('src'))
      DownloadAudio(code, soup.find('audio').get('src'))
    elif soup.find('video') is not None:
      audioUrls.append(soup.find('video').get('src'))
  return audioUrls

def DownloadAudio(speciesCode, url):
  filename = f'{speciesCode}_ML' + url.split('/')[6] + '.mp3'
  filePath = Path.cwd().joinpath('audio', 'eBird', f'{filename}')
  res = requests.get(url)
  with open(filePath, 'wb') as f:
    for data in res.iter_content(1024):
      f.write(data)

# -------------
if __name__ == '__main__':
  ## Use Chrome to crawling
  service = Service(Path.cwd().joinpath('chromedriver'))
  driver = webdriver.Chrome(service=service)
  urlDF = pd.DataFrame(columns=['code', 'page Url'])

  ## Load species taxonomyCode
  codeDF = pd.read_csv(Path.cwd().joinpath('assets', 'code.csv'), header=0)
  for _, row in codeDF.iterrows():
    reqUrl = ConstructRequestUrl(str(row['eBird Code']))
    tempDF = GetSpeciesNextPagesUrl(driver, reqUrl, row['code'])
    urlDF = pd.concat([urlDF, tempDF], ignore_index=True)
  
  ## Download and save audio, and save its url
  audioUrls = GetSpeciesAudioUrls(driver, urlDF['page Url'], urlDF['code'])
  urlDF['audio Url'] = audioUrls
  urlDF.to_csv(Path.cwd().joinpath('assets', 'ML_urls.csv'), header=True, index=False)
  
  ## Close Chrome
  driver.close()