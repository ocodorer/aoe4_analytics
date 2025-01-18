import requests


headers = {
"authority": "aoe4world.com",
"accept": "application/json",
#"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
"accept-encoding": "gzip, deflate, br, zstd",
"accept-language": 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
'cache-control': 'max-age=0',
##"cookie": '_ga=GA1.1.693391180.1712254281; _ga_LTB9BPX5KM=GS1.1.1735841859.167.1.1735841868.0.0.0; _aoe4world_session=IHO5h1fq23mrHECB62FPKBhlAuVrytB8t%2B3R0O1jcoq4A8S7H9tH5SNOrD%2BXM5Pv6uXclpcEhldLmf57CNJPRd2esvDqeZdk9Sg8iAb2aPsuWm9df2TL4eicaZ8TfZi8Z6uZRHlgUUln%2FjDjuBw5QrVC10U4LGqIG3eLuTLzJDFLA%2BDVD0Ld2Z4hfVbX%2FrmNU2iCR9%2Fl3NNt5cWsmuzhWqX8zEsP9H2UIsKEjX9BYEgaeG4gVOES6wnNVlSft7oYhcc11jgQD84OHFMu%2FpNXxgu7nzFqMDFYFc6x%2FGtKSwvT8THwQFRqa0zueogrtHMjrAxwuwGkUgsbeFJ6AuCd2by9BbTeel4b--37IowlnwETgXgMi6--Aq6sqBDRzyufpPYPuNduUg%3D%3D',
"if-none-match": 'W/"816fe75bb140a3efe17800932f289ed7"',
"priority": "u=0, i",
# 'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
# "sec-ch-ua-mobile": '?0',
# "sec-ch-ua-platform": '"Windows"',
# "sec-fetch-dest": "document",
# "sec-fetch-mode": "navigate",
# "sec-fetch-site": "none",
# "sec-fetch-user": "?1",
# "upgrade-insecure-requests": "1",
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}
# a = requests.get("https://aoe4world.com/players/7245194-Your-mom-s-cat/games/159711182/summary", headers=headers, verify=False)
# a = requests.get("https://aoe4world.com/players/7245194-Your-mom-s-cat/games/159750593/summary?camelize=true", headers=headers, verify=False)

# print(a.content, a.headers)

# print(a.content.decode("unicode_escape").encode("utf-8"))

# with open("foogame.txt", "wb") as fo:
#     fo.write(a.content)

#https://aoe4world.com/players/7245194-Your-mom-s-cat/games/159711182?sig=8d74103bc2aa3fdfa780ba5d40491622057ebaa3
# https://aoe4world.com/players/7245194-Your-mom-s-cat/games/159750593?sig=68a3ad96998cb8c4444e99ac6472fbe348708c0c


# import magic

# blob = open('foogame.txt', 'rb').read()
# m = magic.open(magic.MAGIC_MIME_ENCODING)
# m.load()
# encoding = m.buffer(blob)  # "utf-8" "us-ascii" etc
# print(encoding)


# import gzip

# "fetch = opener.open(request) # basically get a response object"
# data = gzip.decompress(a.content)
# data = str(data,'utf-8')

import requests
from bs4 import BeautifulSoup as bs


# headers = {'Accept': '*/*',
#  'Connection': 'keep-alive',
#  'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683 Safari/537.36 OPR/57.0.3098.91'}
res = requests.get("https://aoe4world.com/players/7245194-Your-mom-s-cat/games/159750593/summary?camelize=true", headers=headers)


import chardet

result = chardet.detect(res.content)
print(result)winget install --id Git.Git -e --source winget