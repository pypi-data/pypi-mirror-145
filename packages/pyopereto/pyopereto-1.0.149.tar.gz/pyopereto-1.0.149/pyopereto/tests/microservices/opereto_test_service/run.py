from pyopereto.client import OperetoClient


class MyTest():

    def __init__(self):
        self.c = OperetoClient()

    def run(self):
        try:
            print('This is Opereto simple test service')
            return 0
        except Exception as e:
            print(e)
            return 3

if __name__ == "__main__":
    exit(MyTest().run())