Units = ["wei","gwei","eth"]
ethm = [[1,10e-9,10e-18],[10e9,1,10e-9],[10e18,10e9,1]]


def conversation_rate(fro, to):
    return ethm[Units.index(fro)][Units.index(to)]

def convert(fro, to, amount):
    return conversation_rate(fro, to) * amount
