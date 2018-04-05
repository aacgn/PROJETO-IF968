#############################################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)                            #
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)                                     #
# Bacharelado em Sistemas de Informacao                                                     #
# IF968 -- Programacao 1                                                                    #
#                                                                                           #
# Autor:    Antonio Augusto Correa Gondim Neto (aacgn)                                      #
#                                                                                           #
#                                                                                           #
# Email:    aacgn@cin.ufpe.br                                                               #
#                                                                                           #
#                                                                                           #
# Data:        2016-06-04                                                                   #
# Descricao:  Este e' um modelo de arquivo para ser utilizado para a implementacao          #
#                do projeto pratico da disciplina de Programacao 1.                         #
#                 A descricao do projeto encontra-se no site da disciplina e trata-se       #
#                de uma adaptacao do projeto disponivel em                                  #
#                http://nifty.stanford.edu/2016/manley-urness-movie-review-sentiment/       #
#                O objetivo deste projeto e' implementar um sistema de analise de           #
#                sentimentos de comentarios de filmes postados no site Rotten Tomatoes.     #
#                                                                                           #
# Licenca: The MIT License (MIT)                                                            #
#            Copyright(c) 2016 Antonio Augusto Correa Gondim Neto (aacgn)                   #
#                                                                                           #
#                                                                                           #
#############################################################################################

import sys
import re
import time

def split_on_separators(original, separators):
    '''    Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separtors' e' uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' e' uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    '''            
    return filter(lambda x: x != '',re.split('[{0}]'.format(separators),original))

def clean_up(s):
    ''' Retorna uma versao da string 's' na qual todas as letras sao
        convertidas para minusculas e caracteres de pontuacao sao removidos
        de ambos os extremos. A pontuacao presente no interior da string
        e' mantida intacta.
    '''
    neutralLIST = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours\tourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']
    punctuationLIST = ['', ' '' ', ',', ';', '[', ']', '[]', '*', '#', '<', '>', '<>', '?', ':', '!', '(', ')', '()', '-', '.']  
    punctuation = ''''!"',;:.-?)([]<>*#\n\t\r'''
    s = s.lower().strip(punctuation)
    lista = s.split()
    result = ""
    for x in lista:
        if not ((x in neutralLIST) or (x in punctuationLIST)):
            x = x.strip(punctuation)
            result += x + " "
    return result

def readTestSet(fname):
    ''' Esta funcao le o arquivo contendo o conjunto de teste
	    retorna um vetor/lista de pares (escore,texto) dos
	    comentarios presentes no arquivo.
	''' 
    reviews = []

    testFILE = open(fname, "r")
    for p in testFILE:
        p = p.replace("\n","")
        p = p.replace("\t","")
        reviews.append((int(p[0]), p[1:]))

    testFILE.close()

    return reviews

def readTrainingSet(fname):
    '''    Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,escore,freq) com o escore
        medio das palavras no comentarios.
    '''
    a = []
    trainFILE = open(fname, "r")

    for x in trainFILE:
        x = x.replace("\n","")
        x = x.replace("\t","")
        a.append(x)
        
    trainFILE.close()
    
    dictVALUE = {}
    dictWORDS = dictVALUE.keys()
    
    for x in a:
        x = x.lower()
        x = x.split()
        for y in x:
            if y == x[0]:
                score = int(y)
            else:
                if not y in list(dictWORDS):
                    dictVALUE[y] = (y, score, 1)
                else:
                    dictVALUE[y] = (y, dictVALUE[y][1]+score, dictVALUE[y][2]+1)    
        
    return dictVALUE

def computeSentiment(words, review):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario e' a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore e' 2.
        Review e' a parte textual de um comentario.
        Words e' o dicionario com as palavras e seus escores medios no conjunto
        de treinamento.
    '''
    reviewP = review[1].lower()
    reviewP = clean_up(reviewP)
    reviewP = list(split_on_separators(reviewP, ' \/-'))
    scoreFINAL = 0
    countFINAL = 0
    dictWORDS = words.keys()

    for x in reviewP:
        if x in list(dictWORDS):
            scoreFINAL += words[x][1]/words[x][2]
            countFINAL += 1
        else:
            scoreFINAL += 2
            countFINAL += 1

    if countFINAL > 0:        
        return scoreFINAL / countFINAL
    else:
        return review[0]

def computeSumSquaredErrors(words, reviews):
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario e' obtido com a
        funcao computeSentiment. 
        Reviews e' um vetor de pares (escore,texto)
        Words e' um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    '''   
    qERROR = 0
    for b in reviews:
        testVALUE = b[0]
        iaVALUE = computeSentiment(words, b)
        dif = testVALUE - iaVALUE
        dif = dif*dif
        qERROR += dif
    qERROR /= len(reviews)      
    return qERROR

    
def main():
    
    if len(sys.argv) < 3:
        print ('Numero invalido de argumentos')
        print ('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste>')
        sys.exit(0)

    # Le arquivo de treino e computa valor das palavras
    words = readTrainingSet(sys.argv[1])

    # Le arquivo de teste e calcula o valor de cada comentário, baseando-se no valor das palavras anteriormente calculado pela leitura da arquivo de treino
    reviews = readTestSet(sys.argv[2])
    
    # Calcula e exibe a disperssão geral do software, vendo a diferença entre o valor calculado e sua real qualitatividade representativa.
    sse = computeSumSquaredErrors(words, reviews)
    print ('A soma do quadrado dos erros divido pelo tamanho da lista de teste é: {0}'.format(sse))
            

if __name__ == '__main__':
   main()
    
