# -*- coding: UTF-8 -*-
import base64

import Crypto
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_cipper
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


# 使用 rsa库进行RSA签名和加解密
class RsaUtil(object):
    PUBLIC_KEY_PATH = 'master-private.pem'  # 公钥
    PRIVATE_KEY_PATH = 'master-public.pem'  # 私钥
    # PUBLIC_KEY_PATH = None # 公钥
    # PRIVATE_KEY_PATH = None  # 私钥

    PUBLIC_KEY_PATH_STR = None
    PRIVATE_KEY_PATH_STR = None

    # 初始化key
    def __init__(self,
                 pub_key=None,
                 pri_key=None,
                 company_pub_file=None,
                 company_pri_file=None):
        if company_pub_file:
            self.company_public_key = RSA.importKey(
                open(company_pub_file).read())
        if company_pri_file:
            self.company_private_key = RSA.importKey(
                open(company_pri_file).read())
        if pub_key:
            self.company_public_key = RSA.importKey(pub_key)
        if pri_key:
            self.company_private_key = RSA.importKey(pri_key)
        pass

    def gren(self):
        gene_bit_num = 1024
        # gene_pkcs_mod = 1 | 8
        gene_pkcs_mod = 1
        gene_passphrase = None
        # 伪随机数生成器
        random_generator = Random.new().read
        # rsa算法生成实例
        rsa_key = RSA.generate(2048, random_generator)
        # master的秘钥对的生成
        private_pem = rsa_key.exportKey(
            passphrase=gene_passphrase, pkcs=gene_pkcs_mod)
        # print(private_pem)
        with open('master-private.pem', 'wb') as f:
            f.write(private_pem)

        public_pem = rsa_key.publickey().exportKey()
        print(public_pem)
        with open('master-public.pem', 'wb') as f:
            f.write(public_pem)

        public_pem = rsa_key.publickey().exportKey()
        pass

    def load_rsa_key(self, pub=PUBLIC_KEY_PATH, pri=PRIVATE_KEY_PATH):
        print(open(pub).read())
        print(pub, pri)
        if pub:
            self.company_public_key = RSA.importKey(open(pub).read())
            print(self.company_public_key.n)
        if pri:
            self.company_private_key = RSA.importKey(open(pri).read())
            print(self.company_private_key.n)
        pass

    def get_max_length(self, rsa_key, encrypt=True):
        """加密内容过长时 需要分段加密 换算每一段的长度.
            :param rsa_key: 钥匙.
            :param encrypt: 是否是加密.
        """
        blocksize = Crypto.Util.number.size(rsa_key.n) / 8
        reserve_size = 11  # 预留位为11
        if not encrypt:  # 解密时不需要考虑预留位
            reserve_size = 0
        maxlength = blocksize - reserve_size
        return maxlength

    # 加密 支付方公钥
    def encrypt_by_public_key(self, encrypt_message):
        """使用公钥加密.
            :param encrypt_message: 需要加密的内容.
            加密之后需要对接过进行base64转码
        """
        encrypt_result = b''
        max_length = int(self.get_max_length(self.company_public_key))
        cipher = PKCS1_v1_5_cipper.new(self.company_public_key)
        while encrypt_message:
            input_data = encrypt_message[:max_length]
            encrypt_message = encrypt_message[max_length:]
            out_data = cipher.encrypt(input_data.encode(encoding='utf-8'))
            encrypt_result += out_data
        encrypt_result = base64.b64encode(encrypt_result)
        return encrypt_result

    # 加密 支付方私钥
    def encrypt_by_private_key(self, encrypt_message):
        """使用私钥加密.
            :param encrypt_message: 需要加密的内容.
            加密之后需要对接过进行base64转码
        """
        encrypt_result = b""
        max_length = int(self.get_max_length(self.company_private_key))
        cipher = PKCS1_v1_5_cipper.new(self.company_public_key)
        while encrypt_message:
            input_data = encrypt_message[:max_length]
            encrypt_message = encrypt_message[max_length:]
            out_data = cipher.encrypt(input_data.encode(
                encoding='utf-8').strip() + b"\n")
            encrypt_result += out_data
        encrypt_result = base64.b64encode(encrypt_result)
        return encrypt_result

    def decrypt_by_public_key(self, decrypt_message):
        """使用公钥解密.
            :param decrypt_message: 需要解密的内容.
            解密之后的内容直接是字符串，不需要在进行转义
        """
        decrypt_result = b""
        max_length = self.get_max_length(self.company_public_key, False)
        decrypt_message = base64.b64decode(decrypt_message)
        cipher = PKCS1_v1_5_cipper.new(self.company_public_key)
        while decrypt_message:
            input_data = decrypt_message[:max_length]
            decrypt_message = decrypt_message[max_length:]
            out_data = cipher.decrypt(input_data.encode(encoding='utf-8'), '')
            decrypt_result += out_data
        return decrypt_result

    def decrypt_by_private_key(self, decrypt_message):
        """使用私钥解密.
            :param decrypt_message: 需要解密的内容.
            解密之后的内容直接是字符串，不需要在进行转义
        """
        decrypt_result = b""
        max_length = int(self.get_max_length(self.company_private_key, False))
        decrypt_message = base64.b64decode(decrypt_message)
        cipher = PKCS1_v1_5_cipper.new(self.company_private_key)
        while decrypt_message:
            input_data = decrypt_message[:max_length]
            decrypt_message = decrypt_message[max_length:]
            out_data = cipher.decrypt(input_data, '')
            decrypt_result += str(out_data).encode(
                encoding='utf-8').strip() + b"\n"
        return decrypt_result

    # 签名 商户私钥 base64转码
    def sign_by_private_key(self, message):
        """私钥签名.
            :param message: 需要签名的内容.
            签名之后，需要转义后输出
        """
        cipher = PKCS1_v1_5.new(
            self.company_private_key)  # 用公钥签名，会报错 raise TypeError("No private key") 如下
        # if not self.has_private():
        #   raise TypeError("No private key")
        hs = SHA.new(message)
        signature = cipher.sign(hs)
        return base64.b64encode(signature)

    def verify_by_public_key(self, message, signature):
        """公钥验签.
            :param message: 验签的内容.
            :param signature: 对验签内容签名的值（签名之后，会进行b64encode转码，所以验签前也需转码）.
        """
        signature = base64.b64decode(signature)
        cipher = PKCS1_v1_5.new(self.company_public_key)
        hs = SHA.new(message)

        # digest = hashlib.sha1(message).digest()  # 内容摘要的生成方法有很多种，只要签名和解签用的是一样的就可以

        return cipher.verify(hs, signature)


pri_key = "MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAN8Fv+ZPU+rxX2Qr3Q+no4olyDTxi3Ke51KYg4GkKmkrRQLqv5NbiC+Tg6DjE35xXNSR6VHvak8nt9a0lBRvi2inSK1OuAcjWspkuu5dmrUbgL5o4G036VvO+6jQlkKGV7ZLA5RcqsJiFVyRwWn5R3EspUVtuVGxOvxLcgv5+qwLAgMBAAECgYByXxd3e80UWm5KB7iZU6YprZCLnieeQ2Fr2SzvqgnZ30fH5C0U28buZx8Evg78NBSgKqfVzgrdxwefQwIBrOZ3cnspRtui4ahO6rXFmSCVAKhK7ibRG9Rhk1B+4SPu/ONZfr7/4eAc/5IyhTOpl6FiCO3wWttjB7q8qinY5NvigQJBAP1ggg1sKLqSO50BEe3sbhsvUfuuF79qRz3Cj5z4CIqm9oYIo5JlYr9A77WH22uvz9LE+aYiDYbGO50d1QmD90sCQQDhVMwE/E2y/KNx6kmkXcHJG5UBrzpbWZoBG9UZykwqlAHYpMHJWXAPi7xFqml4pU4rxUa9HpVRCbkcRNnFM2ZBAkAK/86FgKV/++sklLBPkMzy1yoK7/LN93IiRzjuyoGsazUWeneHWmlf/hSp37zxvs8Zyj1ALghCSoa5+lqOMDFjAkEAirjkvbECuM2WZjxByCI8em4zpwzU1YZtLH+RC0ai65ehJ1oPP8GDHt79Mrp+IltKq+HQ8f9RF8nvn3q3wxMowQJBALPY4LsnCUwnavEqlet6CvjuTmJFjq/nuSZwz1UiP9UVa8/EYSGcuUi5OjeN5h+wt9Y7y6qYLQScOQ0rT3aih0o="
# pub_key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCylvPMI6QHoNmAOt0Pb+ONACaobN6LV65F9NnzjGugUFd1nwc4QJyfvn1sWYLvZi1zBw5Lbx1xDaBPazaz73JGu8ugyhIMr4V/dY7b4GKtMfwMMgGoEChigYlTRXeWR1suzIMxyMLsp8LUqyjfY6ebJa2L9niun0t7P4E7MaLTIQIDAQAB"
# data = "qACiIm0zLNB33dgJPHwP6E/v408h2mT6B90palMghxYfKFzIdG8Ws7C/lUeEr5h0rqYbzxBK2fLIMxYeuPGX69EVwD7wpZfnmgqwYi+aFbKBNpRVq1fqTkj8gF5sdpBNmUgOmC4pfqWNgBO2grHIxLGSMpBuuPLbrcJIm6UqYccrssRmXF5mqkqJvt072kgKF5VEUI9NrF4BLzX3Gz/Fb11OX7jnC89U4S7xPrafTzyP0nr+2dwwEh22fYH3Jfyi7k2NjTNbnS6QfzktI4s0B/oLoW6wbNnVlSSwKraX8f1IKPKFe8IdcLBjV2CeIrxq8cfqmjf7ATcTndoAhLt+f5E8Loqy59j85jsbWgk+hPir/kYpHxhnl7ZgGEiijmMnqg2/hWQ717w82cSLKBLeOtJ3rucxUNlhKcmZMf9RrS8hC7ajwPPP5cDmVZNf45Y+OH7JUTNan22F+QQzI7Szavclpw6ffHlgFsrZ4YPs1k2CFsEEsrlGHCvvEGeduwt7"
# key = base64.b64decode(pri_key)
#
# print(key)
# decrypt_result = rsaUtil.decrypt_by_private_key(base64.b64decode(data))
# print("解密结果：>>> ")
# print(decrypt_result)
rsaUtil = RsaUtil()
# rsaUtil.gren()
rsaUtil.load_rsa_key()

message = 'hellworldhellworldhellworldhell'
print("明文内容：>>> ")
print(message)
encrypy_result = rsaUtil.encrypt_by_public_key(message)
print("加密结果：>>> ")
print(encrypy_result)
decrypt_result = rsaUtil.decrypt_by_private_key(encrypy_result)
print("解密结果：>>> ")
print(decrypt_result)
decrypt_result2 = rsaUtil.decrypt_by_public_key(encrypy_result)
print("解密结果2：>>> ")
print(decrypt_result2)
# sign = rsaUtil.sign_by_private_key(bytearray(message.encode(encoding='utf-8')))
# print("签名结果：>>> ")
# print(sign)
# print("验签结果：>>> ")
# print(rsaUtil.verify_by_public_key(bytearray(message.encode(encoding='utf-8')), sign))
