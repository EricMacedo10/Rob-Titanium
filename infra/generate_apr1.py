import hashlib
import random
import string

def md5_apr1(password, salt=None):
    if salt is None:
        salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    
    magic = b"$apr1$"
    password = password.encode('utf-8')
    salt = salt.encode('utf-8')
    
    # 1. Start with password and salt
    ctx = hashlib.md5()
    ctx.update(password)
    ctx.update(magic)
    ctx.update(salt)
    
    # 2. Add intermediate hash
    final = hashlib.md5()
    final.update(password)
    final.update(salt)
    final.update(password)
    final_dict = final.digest()
    
    l = len(password)
    while l > 0:
        ctx.update(final_dict[:min(l, 16)])
        l -= 16
        
    # 3. Add bit-wise iterations
    l = len(password)
    while l > 0:
        if l & 1:
            ctx.update(b"\x00")
        else:
            ctx.update(password[:1])
        l >>= 1
    
    final_dict = ctx.digest()
    
    # 4. 1000 rounds of MD5
    for i in range(1000):
        ctx1 = hashlib.md5()
        if i & 1:
            ctx1.update(password)
        else:
            ctx1.update(final_dict)
        if i % 3:
            ctx1.update(salt)
        if i % 7:
            ctx1.update(password)
        if i & 1:
            ctx1.update(final_dict)
        else:
            ctx1.update(password)
        final_dict = ctx1.digest()
        
    # 5. Base64-like custom encoding
    itoa64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    
    def to64(v, n):
        res = ""
        for i in range(n):
            res += itoa64[v & 0x3f]
            v >>= 6
        return res
        
    reordered = to64((final_dict[0] << 16) | (final_dict[6] << 8) | final_dict[12], 4)
    reordered += to64((final_dict[1] << 16) | (final_dict[7] << 8) | final_dict[13], 4)
    reordered += to64((final_dict[2] << 16) | (final_dict[8] << 8) | final_dict[14], 4)
    reordered += to64((final_dict[3] << 16) | (final_dict[9] << 8) | final_dict[15], 4)
    reordered += to64((final_dict[4] << 16) | (final_dict[10] << 8) | final_dict[5], 4)
    reordered += to64(final_dict[11], 2)
    
    return f"$apr1${salt.decode()}${reordered}"

if __name__ == "__main__":
    # Test
    import os
    pwd = os.getenv("FTP_PASS", "YOUR_PASSWORD")
    user = os.getenv("FTP_USER", "YOUR_USER")
    salt = "Xy7z8w9v" # Salt fixo para consistência
    hash_val = md5_apr1(pwd, salt)
    print(f"{user}:{hash_val}")
