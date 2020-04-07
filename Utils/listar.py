from os import listdir

def listar(path = '.'):
    arquivos = listdir(path)
    dic = {}
    dic[path] = [x for x in arquivos if x.split('.') != [x]]
    for x in [x for x in arquivos if x.split('.') == [x]]:
        dic.update(listar(path+'/'+x))
    return dic

def codificar(dicionario):
    string = ''
    for nome in dicionario:
        string += nome + ':' + str(dicionario[nome]) + "§"
    return string.replace("'", "")