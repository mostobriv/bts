import binaryninja




class VirtualTable:
    def __init__(self, addr):
        self.addr = addr

        self.populate()


    def populate(self):
        pass

    @staticmethod
    def check(addr, MIN_FUNCTIONS_REQUIRED=3):
        # 1 - there is code xref to this address
        # 2 - at least MIN_FUNCTIONS_REQUIRED valid function pointers

        functions_counted = 0
        while True:
            pass

        if functions_counted < MIN_FUNCTIONS_REQUIRED:
            return False

        return functions_counted