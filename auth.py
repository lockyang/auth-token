# !/usr/bin/python
# -*- coding:utf-8 -*-
'''
注意返回的是str，调用时，若需要int，则需要转换
'''

'''
# alias auth
# fish config
function auth
  python3 /Users/admin/env/googleAuth.py "FITA****TOKEN"
end
'''

import hmac, base64, struct, hashlib, time
import platform
import sys
import os
#from Carbon.Scrap import GetCurrentScrap, ClearCurrentScrap

"""def copy(text, flavorType='TEXT'):
    ClearCurrentScrap()
    scrap = GetCurrentScrap()
    scrap.PutScrapFlavor(flavorType, 0, text)"""

def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    # 很多网上的代码不可用，就在于这儿，没有chr字符串
    o = ord(chr(h[19])) & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    # 获取的是整数，补0
    mfaStr =  ("000000"+str(h))[-6:]

    return mfaStr

def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time())//30)

if __name__ == '__main__':
    #copy(get_totp_token(sys.argv[1]))
    token = get_totp_token(sys.argv[1])
    cmd = 'echo %s | tr -d "\n" | pbcopy' % token
    print(token,end='')
    os.system(cmd)

