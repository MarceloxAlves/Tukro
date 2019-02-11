
def busca_palavra(keyword, texto):
    resultados = []
    for i in range(0,texto.__len__()):
        inicio = None
        if texto[i] == keyword:
            palavra = ''
            for j in range(i,texto.__len__()):
                if texto[j] == " " and palavra.__len__() > 1:
                    resultados.append(palavra)
                    break
                else:
                    palavra += texto[j]
    return resultados