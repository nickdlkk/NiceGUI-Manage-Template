import hashlib
import os


def hash_password(password, salt):
    # 将密码和盐拼接在一起
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed


def generate_salt(length=20):
    # 生成一个随机盐
    return os.urandom(length).hex()


if __name__ == "__main__":
    password = "my_secret_password"
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    print(f"Hashed Password: {hashed_password}")
    print(f"Salt: {salt}")
