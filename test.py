import time, requests, json, datetime, zoneinfo

tstamp = int(time.time())
url = f'https://ctftime.org/api/v1/events/?limit=100&start={tstamp}&finish={tstamp+604800}'
print(type(url))
print(url)
header = {'User-Agent': 'Mozilla/5.0', "content-type": "application/json"}
res = requests.get(url, headers=header)
print(type(res))
print(res.status_code)
data = res.json()
#print(data)

print(type(data))

n = len(data)

print(n)
msg = str()
dd = datetime.datetime
JST = zoneinfo.ZoneInfo('Asia/Tokyo')
print(dd.now().year)
print(type(dd.now().year))
# for i in range(n):
#     starttime = dd.fromisoformat(data[i]["start"]).astimezone(JST)
#     finishtime = dd.fromisoformat(data[i]["finish"]).astimezone(JST)
#     tmp = (
#         '-----\n'
#         f'title: {data[i]["title"]}\n'
#         f'organizers: {data[i]["organizers"][0]["name"]}\n'
#         f'URL: {data[i]["url"]}\n'
#         f'URL(CTFtime): {data[i]["ctftime_url"]}\n'
#         f'weight: {data[i]["weight"]}\n'
#         f'start: {starttime}\n'
#         f'finish: {finishtime}\n'
#         f'description:\n```{data[i]["description"][:2048]}```\n'
#     )
#     msg += tmp

# print(f'{n}件開催予定です:\n{msg}')

prefix = '^'
print(prefix + 'aaa')