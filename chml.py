
import requests
import os
import time
import random
import json

global gpstr  # 声明gpstr为全局变量
gpstr = ''
os.environ['chml'] = '''
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjkyMjMzNzIwMzY4NTQ3NzU4MDcsInBheWxvYWQiOiJ7XCJ1c2VySWRcIjpcIjI4ODUzMjlcIn0ifQ.aE2qwi5NYFXP0ZZN6bllrLrCG0E8O9rHhuX-jy8YK8g
'''

def getEnv():
  env = os.getenv('chml')
  if env == None:
    print('请检查变量参数是否填写')
    exit(0)
  accounts = env.strip().split('\n')
  num_accounts = len(accounts)
  print(f'-----------本次账号运行数量：{num_accounts}-----------')
  print(f'----------项目： 长虹美菱-1----------')
  return accounts


def sign(ck):
  global gpstr  # 声明gpstr为全局变量
  headers = {
    'Host': 'hongke.changhong.com',
    'Connection': 'keep-alive',
    # 'Content-Length': '0',
    'charset': 'utf-8',
    'accept-language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.120 Mobile Safari/537.36 XWEB/1220133 MMWEBSDK/20240404 MMWEBID/8518 MicroMessenger/8.0.49.2600(0x2800313D) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64 MiniProgramEnv/android',
    'content-type': 'application/json',
    # 'Accept-Encoding': 'gzip,compress,br,deflate',
    'token': ck,
}
  params = {
    'aggrId': '608',
}

  response = requests.post('https://hongke.changhong.com/gw/applet/aggr/signin', params=params, headers=headers)
  res = response.json()
  if res.get("code") ==400:
    print("已达上限，停止请求。")
    gpstr += f'今天已签到\n'
  if res.get("code") ==200:
    print("签到成功")
    gpstr += f'签到成功\n'




def main():
  tokens = getEnv()
  for i, token in enumerate(tokens):
    parts = token.split('#')
    if len(parts) < 1:
      print("令牌格式不正确。跳过处理。")
      continue
    token = parts[0]
    total_accounts = len(tokens)
    account_no = parts[1] if len(parts) > 1 else ""
    print(f'------账号 {i + 1}/{total_accounts} {account_no} 签到-------')
    sign(token)

if __name__ == "__main__":
  main()
  try:
    import notify

    notify.send('长虹美菱', gpstr)
  except Exception as e:
    print(e)
    print('推送失败')
