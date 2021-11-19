class Output:
    p = '\033[95m'
    b = '\033[94m'
    c = '\033[96m'
    g = '\033[92m'
    y = '\033[93m'
    r = '\033[91m'
    ENDC = '\033[0m'
    B = '\033[1m'
    u = '\033[4m'
    clear = '\33modeJ'

    @classmethod
    def create(cls, text, mod):
        prefix = ''
        for char in mod:
            prefix += getattr(cls, char)

        return prefix + text + cls.ENDC
