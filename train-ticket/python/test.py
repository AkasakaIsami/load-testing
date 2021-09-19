from configparser import ConfigParser

cp = ConfigParser()
cp.read("config.ini")
index = int(cp.get("server", "testint"))

if __name__ == '__main__':

    for i in range(index):
        print(i)