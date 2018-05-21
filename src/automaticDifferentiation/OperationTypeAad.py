from enum import Enum


class OperationTypeAad(Enum):
    INPUT = 'INPUT'
    MANUAL = 'MANUAL'
    ADDITION = 'ADDITION'
    ADDITION1 = 'ADDITION1'
    SUBTRACTION = 'SUBTRACTION'
    SUBTRACTION1 = 'SUBTRACTION1'
    MULTIPLICATION = 'MULTIPLICATION'
    MULTIPLICATION1 = 'MULTIPLICATION1'
    DIVISION = 'DIVISION'
    DIVISION1 = 'DIVISION1'
    DIVISION2 = 'DIVISION2'
    SIN = 'SIN'
    COS = 'COS'
    EXP = 'EXP'
    LOG = 'LOG'
    SQRT = 'SQRT'
    POW = 'POW'
    POW1 = 'POW1'
    POW2 = 'POW2'
    NORMALCDF = 'NORMALCDF'

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False
