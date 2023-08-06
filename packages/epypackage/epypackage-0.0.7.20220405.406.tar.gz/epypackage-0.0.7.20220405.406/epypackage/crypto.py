# -*- coding: utf-8 -*-
# @Time : 2022-01-08 21:07
# @Author : LiGuangLong
# @File : crypto.py
# @Software: PyCharm

from urllib import parse
import hashlib  # 散列算法加密库

'''
Hash，译做“散列”，也有直接音译为“哈希”的。把任意长度的输入，通过某种hash算法，变换成固定长度的输出，该输出就是散列值，也称摘要值。该算法就是哈希函数，也称摘要函数。

当前，在大部分操作系统下，hashlib模块支持md5(),sha1(), sha224(), sha256(), sha384(), sha512(), blake2b()，blake2s()，sha3_224(), sha3_256(), 
sha3_384(), sha3_512(), shake_128(), shake_256()等多种hash构造方法。这些构造方法在使用上通用，返回带有同样接口的hash对象，对算法的选择，
差别只在于构造方法的选择。例如sha1()能创建一个SHA-1对象，sha256()能创建一个SHA-256对象。然后就可以使用通用的update()方法将bytes类型的数据添加到对象里，
最后通过digest()或者hexdigest()方法获得当前的摘要。


digest:获得bytes类型的消息摘要
hexdigest:获得16进制str类型的消息摘要
digest_size:查看消息摘要的位长
注意了，update()方法现在只接受bytes类型的数据，不接收str类型。


用法:
md5 = hashlib.md5()   创建一个md5散列对象   md5 = hashlib.md5('123'.encode('utf8'))可以进行加盐操作
md5.update(bytes)     传入二进制数据流
md5.hexdigest()       获取16进制结果


更简洁的用法：
hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest()
'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2'

'''
import base64

'''

base64.b64encode(parameter)
base64.b64decode(parameter)

'''
from crypto.Cipher import AES

# pip install pycryptodome
# from Crypto.Cipher import AES
'''
from binascii import b2a_hex, a2b_hex
AES只是个基本算法，实现AES有几种模式，主要有ECB、CBC、CFB和OFB这几种（其实还有个CTR）：
1.ECB模式（电子密码本模式：Electronic codebook）
ECB是最简单的块密码加密模式，加密前根据加密块大小（如AES为128位）分成若干块，之后将每块使用相同的密钥单独加密，解密同理。
2.CBC模式（密码分组链接：Cipher-block chaining）
CBC模式对于每个待加密的密码块在加密前会先与前一个密码块的密文异或然后再用加密器加密。第一个明文块与一个叫初始化向量的数据块异或。
3.CFB模式（密文反馈：Cipher feedback）
与ECB和CBC模式只能够加密块数据不同，CFB能够将块密文（Block Cipher）转换为流密文（Stream Cipher）。
4.OFB模式（输出反馈：Output feedback）
OFB是先用块加密器生成密钥流（Keystream），然后再将密钥流与明文流异或得到密文流，解密是先用块加密器生成密钥流，再将密钥流与密文流异或得到明文，由于异或操作的对称性所以加密和解密的流程是完全一样的。

:var MODE_ECB: :ref:`Electronic Code Book (ECB) <ecb_mode>`
:var MODE_CBC: :ref:`Cipher-Block Chaining (CBC) <cbc_mode>`
:var MODE_CFB: :ref:`Cipher FeedBack (CFB) <cfb_mode>`
:var MODE_OFB: :ref:`Output FeedBack (OFB) <ofb_mode>`
:var MODE_CTR: :ref:`CounTer Mode (CTR) <ctr_mode>`
:var MODE_OPENPGP:  :ref:`OpenPGP Mode <openpgp_mode>`
:var MODE_CCM: :ref:`Counter with CBC-MAC (CCM) Mode <ccm_mode>`
:var MODE_EAX: :ref:`EAX Mode <eax_mode>`
:var MODE_GCM: :ref:`Galois Counter Mode (GCM) <gcm_mode>`
:var MODE_SIV: :ref:`Syntethic Initialization Vector (SIV) <siv_mode>`
:var MODE_OCB: :ref:`Offset Code Book (OCB) <ocb_mode>`


用法:
cryptor = AES.new(key, AES.MODE_CBC, key)    实例化一个加密对象   key是二进制流bytes格式 
encrData = cryptor.encrypt(bytes)            进行加密 加密二进制流 返回也是二进制 bytes格式  根据需要进行bese64编码
           cryptor.decrypt(byets)            解密方法  同上


           AES.new(key, AES.MODE_EBC, iv)   相对于cbc多了个iv(bytes) 其他同上


填充算法拓展
这里采用的填充算法其实有个专有名词，叫pkcs7padding。 
简单解释就是缺几位就补几：填充字符串由一个字节序列组成，每个字节填充该填充字节序列的长度。 
如果要填充8个字节,那么填充的字节的值就是0x08；要填充7个字节,那么填入的值就是0x07；以此类推。 
如果文本长度正好是BlockSize长度的倍数，也会填充一个BlockSize长度的值。这样的好处是，根据最后一个Byte的填充值即可知道填充字节数。

实际上，java中实现AES加密算法的默认模式是Cipher.getInstance("AES/ECB/PKCS5Padding") 
PKCS#5在填充方面，是PKCS#7的一个子集：PKCS#5只是对于8字节（BlockSize=8）进行填充，填充内容为0x01-0x08；但是PKCS#7不仅仅是对8字节填充，其BlockSize范围是1-255字节。 
然而因为AES并没有64位（8字节）的块, 如果采用PKCS5, 那么实质上就是采用PKCS7。
'''


def str_bytes():
	'''str.a.encode('utf-8')   字符串变字节串   加密方法 encode  '''
	text = '''
首先数字符串转为字节串
有以下几种方法
如果一个字符串中全部为英文（也就是说全是ascii的英文字符）我们可以直接在 字符串前面加 b  就可以了

举个栗子：a = b'I am a coder'
此时的 a 就是一个字节串

如果 使用了  中文字符之类了，也就是说不是在 ascii 能表示的范围的活，就要使用 encode()方法了
举个栗子：a = '我是一个码农'      这是一个带有中文的字符串，要想转成字节串，前面加上  b   的方法是会报错的
使用  a.encode('utf-8')     就可以转成字节串了， 这里的 utf-8是一个默认的参数，也可以不传   
反之把一个字节串，转换为字符串的方法是用 decode() 就可以了

举个栗子：
mm = b'I am a coder'    这里的mm就是一个字节串，转成字符串就使用 decode()方法
mmstr = mm.decode('utf-8')  这里的utf-8也是默认参数，也可以不写
同理，上面的mm字节串中，全部是英文的字符，所以，也可以使用 
mmstr = mm.decode('ascii')的方式进行转换，和utf8的转换结果是一样的
这里说明一下，为什么 参数为ascii 和 utf-8的转换结果是一样的
说明的前提是   字节码中 全部是英文的 字符，没有中文字符
ascii和 utf8   我们可以理解为一个包含与被包含的关系，  因为 ascii只有 128种编码，对英文字符来说已经足够用了，但是utf-8就包含了中文的编码，也包含了英文的编码，
我们可以理解为 utf-8是在ascii的基础上又添加了新的编码 （可以这样理解，实际上不能等同）
utf-8字符集的 前128位字符，就是和  ascii是一模一样的
所以，当 decode（）一个全部是英文字符组成的字节串的时候，参数为   decode(‘ascii’)   和 decode('utf-8')的结果是一样的
但是如果其中有汉字的话，就不会

    '''
	print(text)


def 编码_UTF8编码(内容):
	'失败返回空文本'
	try:
		return 内容.encode(encoding='UTF-8', errors='strict')
	except:
		return ''


def 编码_UTF8解码(内容):
	'失败返回空文本'
	try:
		return 内容.decode(encoding='UTF-8', errors='strict')
	except:
		return ''


def 编码_URL编码(内容):
	'失败返回空文本'
	try:
		return parse.quote(内容)
	except:
		return ''


def 编码_URL解码(内容):
	'失败返回空文本'
	try:
		return parse.unquote(内容)
	except:
		return ''


def 编码_GBK编码(内容):
	'失败返回空文本'
	try:
		return 内容.encode(encoding='GBK', errors='strict')
	except:
		return ''


def 编码_GBK解码(内容):
	'失败返回空文本'
	try:
		return 内容.decode(encoding='GBK', errors='strict')
	except:
		return ''


def 编码_ANSI到USC2(内容):
	'失败返回空文本'
	try:
		return ascii(内容)
	except:
		return ''


def 编码_USC2到ANSI(内容):
	'失败返回空文本'
	try:
		return 内容.encode('utf-8').decode('unicode_escape')
	except:
		return ''


def md5(text):
	md5 = hashlib.md5()  # 创建一个md5散列对象   md5 = hashlib.md5('123'.encode('utf8'))可以进行加盐操作
	md5.update(text.encode('utf8'))  # 传入二进制数据
	return md5.hexdigest()  # 获取加密后的值，digest是二进制，hexdigest则是十六进制


def sha_1(text):
	sha1 = hashlib.sha1()
	sha1.update(text.encode('utf8'))
	return sha1.hexdigest()


def sha_224(text):
	sha224 = hashlib.sha224()
	sha224.update(text.encode('utf8'))
	return sha224.hexdigest()


def sha_256(text):
	sha_256 = hashlib.sha256()
	sha_256.update(text.encode('utf8'))
	return sha_256.hexdigest()


def sha_512(text):
	sha_512 = hashlib.sha512()
	sha_512.update(text.encode('utf8'))
	return sha_512.hexdigest()


def beae64_encode(text, 二进制):
	if 二进制:
		return base64.b64encode(text.encode('utf-8'))
	else:
		return str(base64.b64encode(text.encode('utf-8')))[2:-1]


def beae64_decode(text, 二进制):
	if 二进制:
		return base64.b64decode(text)
	else:
		return base64.b64decode(text).decode()


def aes():
	k = b'0123456789abcdef'
	iv = b'0000000000000000'
	data = 'suyan'
	BLOCK_SIZE = 16  # Bytes
	# 数据进行 PKCS5Padding 的填充
	pad = lambda s: (s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE))
	raw = pad(str(data))

	# cryptor=AES.new(k,AES.MODE_ECB)
	cryptor = AES.new(k, AES.MODE_CBC, iv)
	enc_date = cryptor.encrypt(raw.encode('utf8'))  # 加密得到字节串
	enc_date = base64.b64encode(enc_date)  # 进行base64编码
	print(enc_date)



