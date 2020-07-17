from enum import Enum

class FailureKind(Enum):
    Normal = 0,
    Service = 1,
    Immobilizing = 2

    @staticmethod
    def tostr(item):
        strings = {
            FailureKind.Normal: 'ETCS_normal',
            FailureKind.Service: 'ETCS_service',
            FailureKind.Immobilizing: 'ETCS_immobilizing'
        }
        retval = strings[item]
        return retval
