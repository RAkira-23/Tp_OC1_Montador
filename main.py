def regis(reg):
    limpo = reg.replace("x", "").replace(",", "").replace("(", "").replace(")", "")
    return format(int(limpo), '05b')

def compd(n, bits=12):
    if "(" in n:
        n = n.split("(")[0]
    num = int(n)
    bit = (1 << bits) - 1
    return format(num & bit, f'0{bits}b')

def R(k, u, f7="0000000"):
    rd = regis(k[1])
    rs1 = regis(k[2])
    rs2 = regis(k[3])
    return f7 + rs2 + rs1 + u + rd + "0110011"

def I(k, u):
    rd = regis(k[1])
    if "(" in k[2]:
        imm = compd(k[2])
        rs1 = regis(k[2].split("(")[1])
    else:
        rs1 = regis(k[2])
        imm = compd(k[3])
    
    if k[0].lower() == "lh":
        cod7b = "0000011"
    else:
        cod7b = "0010011"
    return imm + rs1 + u + rd + cod7b

def S(k, u):
    rs2 = regis(k[1])
    imm = compd(k[2])
    rs1 = regis(k[2].split("(")[1])
    imm_hi = imm[0:7]
    imm_lo = imm[7:12]
    return imm_hi + rs2 + rs1 + u + imm_lo + "0100011"

def B(k, u):
    rs1 = regis(k[1])
    rs2 = regis(k[2])
    imm = compd(k[3], bits=13)
    res = imm[0] + imm[2:8] + rs2 + rs1 + u + imm[8:12] + imm[1] + "1100011"
    return res

def org(k):
    inst = k[0].lower().replace(",", "")
    if inst == "add":  return R(k, "000")
    if inst == "or":   return R(k, "110")
    if inst == "sll":  return R(k, "001")
    if inst == "lh":   return I(k, "001")
    if inst == "andi": return I(k, "111")
    if inst == "sh":   return S(k, "001")
    if inst == "bne":  return B(k, "001")
    return ""

with open("entrada.asm", "r") as arq:
    linhas = [l.strip() for l in arq.readlines() if l.strip()]

with open("saida.bin", "w") as saida:
    for linha in linhas:
        li = linha.replace(",", " ").split()
        if li:
            resultado = org(li)
            if resultado:
                print(resultado)
                saida.write(resultado + "\n")