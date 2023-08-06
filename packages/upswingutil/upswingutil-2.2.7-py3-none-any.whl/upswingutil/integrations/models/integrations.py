from enum import  Enum
class Providers(Enum):
    MESSERCHMITT = 'messerchmitt'
    ASSA_ABLOY = 'assa_abloy'
    VDA = 'VDA'

class PMS(Enum):
    RMS = 'rms'
    ORACLE_ON_PREM = 'oracle_onprem'
    ORACLE_OHIP = 'oracle_ohip'