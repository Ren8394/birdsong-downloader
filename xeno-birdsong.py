import json
import pandas as pd
import requests

from pathlib import Path
from tqdm import tqdm

# ------------- 
def ConstructRequestUrl(sciName:str) -> str:
  baseUrl = 'http://www.xeno-canto.org/api/2/recordings'
  audioType = 'song'
  country = 'Taiwan'
  return baseUrl + f'?query={sciName}%20cnt:{country}%20type:{audioType}'

def DownloadAudio(speciesCode, url, fileID, q):
  filename = f'{speciesCode}_XC{fileID}_{q}.mp3'
  filePath = Path.cwd().joinpath('audio', 'xeno-canto', f'{filename}')
  res = requests.get(url)
  with open(filePath, 'wb') as f:
    for data in res.iter_content(1024):
      f.write(data)

# -------------
if __name__ == '__main__':
  urlDF = pd.DataFrame(columns=['code', 'audio Url'])
  ## Load species Code
  codeDF = pd.read_csv(Path.cwd().joinpath('assets', 'code.csv'), header=0)
  for _, row in codeDF.iterrows():
    reqUrl = ConstructRequestUrl(row['sci Name'])
    res = requests.get(reqUrl)
    data = json.loads(res.text)
    ### Download and save audio, and save its url
    numberOfRecordings = data['numRecordings']
    recordings = data['recordings']
    for recording in tqdm(
      recordings, 
      total=len(recordings),
      desc=f'{"downloading...":>16}', 
      bar_format='{l_bar}{bar:32}{r_bar}{bar:-32b}'
    ):
      DownloadAudio(row['code'], recording['file'], recording['id'], recording['q'])
      urlDF = pd.concat(
        [urlDF, pd.DataFrame({
          'code': row['code'],
          'audio Url': recording['file']
        }, index=[0])],
        ignore_index=True
      )
  urlDF.to_csv(Path.cwd().joinpath('assets', 'XC_urls.csv'), header=True, index=False)