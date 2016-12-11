# -*- coding: UTF-8 -*-
# Date : 2016.12.11
# BY   : B. K. Choi

import datetime, codecs, platform, time
import pandas as pd
from pandas import DataFrame, Series

"""
# 함수 선언 방법 
1. 목적 :
2. 원본 : 기본소스파일 이름 
3. 수정 : 날짜
4. 문제 : 문제사항 메모 
5. 예제 : example 
"""

from konlpy.tag   import Kkma
from konlpy.utils import pprint


def making_list_from_stringlist(inputDataList=[],sep=',', cutoffn=2):
    """함수 선언 방법 
    0. 파라미터 : 
    1. 목적 : 스트링리스트에서 구분자(sep)로 구분하여, 글자크기가 cutoffn 이상인것만 추출하도록 함. 
             *글자크기 조심(한글일때)       
    2. 원본 : textanalysis.py
    3. 수정 : 2016.11.30
    4. 문제 :  
    5. 예제 : 
    
if 1==1:
    txtlist  = [ "자동차|학교", "공장|운동장|마당|공터", "강아지", "", "*"]
    txtlist2 = making_list_from_stringlist(txtlist, '|',4)

    for i, each in enumerate(txtlist2): 
        for j, eachi in enumerate(each):
            print i,j, eachi, len(eachi)

    """
    
    inputDataList2 = []
    for each in inputDataList:
        each2 = each.strip()
        if each2 not in ["","-","*"]: # 빈 공란은 제거시킴
            templist = each2.split(sep)
            templist2 = []
            templist2 = [eachtemp.strip() for eachtemp in templist if len(eachtemp.strip())>= cutoffn] 
            inputDataList2.append(templist2)
    
    return inputDataList2



def making_pajek_netfile_from_excelfile(filename ='', fieldname = '',
                                        sep=',', cutoffn=2, 
                                        pajekfilename = 'test_01', 
                                        option = {'no':1,'fieldname':'Pname'}):
    """함수 선언 방법 
    0. 파라미터 : 
    1. 목적 : 엑세파일의 특정한 칼럼(필드)에 있는 단어들의 공기어 출현빈도를 계산하여 Pajek 파일의 net, vec 형태로 생성시켜줌
           
    2. 원본 : textanalysis.py
    3. 수정 : 2016.11.30
    4. 문제 :  
    5. 예제 : 
    
if 1==1:
    making_pajek_netfile_from_excelfile(filename  = 'total.xlsx', 
                                    fieldname     = 'Morpho2', 
                                    sep           = '|', 
                                    pajekfilename = 'president_1130_1',
                                    option = {'no':2,'fieldname':u'Pname'})

    """
    
    # 엑셀파일 불러오기
    xls1           = pd.ExcelFile(filename)
    sheet          = xls1.sheet_names
    df             = xls1.parse(sheet[0])
                                                  
    
    if option['no'] == 1: 
                                                  
        inputDataList2 = making_list_from_stringlist(df[fieldname].tolist(),sep,cutoffn)
        datain, header = makeIncidenceMatrix(inputDataList2)
        onemode        = making2Modeto1Mode(datain)
        makingPajekFile(onemode, header, pajekfilename)
                                                  
        #print "OK"
                                                  
    elif option['no'] == 2 :
        print "option 2"                                      
        namelist  = df[option['fieldname'] ].unique()
        for each in namelist:
            print "each= ",  each
            dfnew = df[df[option['fieldname']] == each]
            inputDataList2 = making_list_from_stringlist(dfnew[fieldname].tolist(),sep,cutoffn)
            datain, header = makeIncidenceMatrix(inputDataList2)
            onemode        = making2Modeto1Mode(datain)
            makingPajekFile(onemode, header, each + "_" + pajekfilename)
    else:
        pass
                      


def making_morpho(inputstr='', filter = [u'NNG',u'NNP',u'NNB']):
    """함수 선언 방법 
    0. 파라미터 : inputstr 문자열, filter 형태소 부호
    1. 목적 : 문자열 입력받아 형태소분석하여 문자열 리턴해줌. 문자열 튜플로 리턴되는데, 
            (1) 형태소분석결과 전체, (2) 필터에 해당하는 단어 
    2. 원본 : textanalysis.py
    3. 수정 : 2016.11.30
    4. 문제 :  
    5. 예제 : 
    
    txt = u"둘째, 나노기술을 체계적으로 발전시켜 나가겠습니다. \
            세계의 기술전쟁은 원자와 분자 수준으로 진입했습니다. \
            사람의 눈으로 볼 수 없는 극미세 물질의 세계로 들어섰습니다. \
            올해 내에 나노기술 종합 발전계획을 발표하겠습니다."

    a,b = making_mopho(txt)
    print a
    print "*"*30
    print b
    
    """
    kkma = Kkma()
    morpho = kkma.pos(inputstr)
    morpho_str = ''
    morpho2    = ''
    for each in morpho:
        morpho_str = morpho_str +'|' + each[0] +'-'+each[1]
        if each[1] in filter:
            morpho2 = morpho2 +'|' + each[0]

    return morpho_str, morpho2


def createUniqueWordList(inputDataList):
    '''
    1.목적: 문자 리스트를 입력받아서, 고유한 문자 리스트로 반환해줌
    2.원본:
    3.수정: 2016.11.17
    4.
    5.example

    a = ['abc1','def','abc1']
    r = createUniqueWordList([a])
    print r

    ['abc1', 'def'] 

    '''
    uniqueWordSet = set([])
    for document in inputDataList :
        uniqueWordSet = uniqueWordSet | set(document)
    return sorted(uniqueWordSet) # return unique word list


def makeIncidenceMatrix(inputDataList):
    '''
    1.목적 : 문자 리스트(2차)를 입력받아서, Co-Occurrence 매트릭스 리턴해 줌
    2.원본 : 
    3.수정 : 2016.11.11 
    4.
    5.example
    
    if 1 == 1:
    a = [ ['my','name','is','Tom', 'Tom'],
         ["What's", "your", "name?"],
          ['Tom', 'Tom', 'Tom', 'your', 'name']]

    m, h = makeIncidenceMatrix(a)

    print 'm=',m
    print 'h=',h
    
    >> makeIncidenceMatrix()
    m= [[2, 0, 1, 1, 1, 0, 0], [0, 1, 0, 0, 0, 1, 1], [3, 0, 0, 0, 1, 0, 1]]
    h= ['Tom', "What's", 'is', 'my', 'name', 'name?', 'your']
    '''
    
    #print ">> makeIncidenceMatrix()"
    header = createUniqueWordList(inputDataList)
    incideceMatrixList = []
    for document in inputDataList:
        returnVec = [0]* len(header)
        for word in document:
            if word in header:
                returnVec[ header.index(word)] += 1
            else:
                print "check the word : {} is not in header"
        incideceMatrixList.append(returnVec)

    return incideceMatrixList, header



##############################
# network analysis  
##############################

def making2Modeto1Mode(datain):
    '''
    1.목적 : 2 mode 행렬 입력 받아서, 1 mode 행렬로 변경해서 리턴해줌

    2.원본 : factotum.py, ppp_function.py  (파일 두개에서 생성됨)
    3.수정 : 
    4.문제 : 시간 많이 소비함(2014.7.15), 업데이트 필요
    5.example 

    
    '''

    kMax = len(datain)
    iMax = len(datain[0])
    jMax = len(datain[0])

    O = []

    for i in range(iMax):
        temp=[]
        for j in range(jMax):
            temp.append(0)
        O.append(temp)

    for i in range(iMax):
        for j in range(jMax):
            sum1 = 0
            for k in range(kMax):
                if datain[k][i] > 0:
                    if datain[k][j] > 0:
                        sum1 = sum1 + 1 #등장하는 횟수를 기준으로 한다.
                    # sum1 = sum1 + datain[k][j]
                    # sum1 += datain[k][j] # 왼쪽 로우의 값이 있을때에만, 오른쪽의 합계를 구하게 한다.
                    # 등장하는 횟수를 기준으로 한다. 즉,  a1이 1번이상 등장할때 a2가 1번 이상 등장하면 1번 등장한 것으로 간주한다.

            O[i][j]=sum1

    return O


def makingPajekFile(onemode, header, filename):
    '''
    making pajek file (2014.7.15)
    1.목적 : one mode 행렬 입력받아서 pajek file 만들어줌
    2.원본 : ppp_funtion
    3.수정 : 2016.11.11
    4.
    5. 
    '''

    total_n = len(header) # 전체 단어 갯수
    edgeList = [] # edge list


    with codecs.open(filename+".vec", 'w', 'utf-8')as fn:
        fn.write("*vertices {}\n".format(total_n))
        for i in range(total_n):
            fn.write("{}\n".format(onemode[i][i]))
        print ">>> " + filename +".vec" + " saved"

    with codecs.open(filename+".csv", 'w', 'utf-8')as fn:
        # for gephi (2016.11.30 추가함)
        fn.write("id,word,frequency\n")
        for i in range(total_n):
            #fn.write("{},{}\n".format(header[i], onemode[i][i]))
            #fn.write("%s,%d\n"%(header[i], onemode[i][i]))
            fn.write("%d,%s,%d\n"%(i+1,header[i],onemode[i][i]))
        print ">>> " + filename +".csv" + " saved"

    with codecs.open(filename+".net", 'w', 'utf-8') as fn:
        fn.write("*vertices {}\n".format(total_n))

        for i in range(total_n):
            #fn.write("{} \"{}\"\n".format(i+1, header[i]))
            fn.write("%d \"%s\"\n" %(i+1, header[i]))

        fn.write("*edges\n")

        for i in range(total_n):
            for j in range(total_n):
                if j> i: # 반쪽 행렬만 나타내기 ..
                    if onemode[i][j]>0:
                        #fn.write("{} {} {}\n".format(i+1,j+1, onemode[i][j]))
                        fn.write("{} {} {}\n".format(i+1,j+1, onemode[i][j] ) )

                        edgeList.append( ( header[i], header[j], onemode[i][j] ))
        print ">>> " + filename +".net" + " saved"

    return edgeList


def making_1mode_basic(df=DataFrame(), option2='simple_matching'):
    '''
    목적 : 입력받아서 1 mode를 리턴해 줌 
    원본 : 
    수정 : 2016.11.11
    
    '''
    datain   = df.values.tolist()
    namelist = df.index.tolist()

    iMax = len(df.index)
    
    df_result = DataFrame()
    templist = []
    index_i   = 0 
    
    for i in range(iMax):      # i : row number1
        for j in range(iMax):  # j : row number2 
            if i<j:
                p1 = np.array(datain[i])
                p2 = np.array(datain[j])
                a = 0.
                b = 0.
                c = 0.
                d = 0.
                    
                for k, eachi in enumerate(p1):
                    #print ">>> k={}, p1[{}]={}, p2[{}]={}".format(k, k, p1[k],k, p2[k])
 
                    if p1[k] > 0 :    
                        if p2[k] > 0: # 존재, 존재 
                            #print 'a'
                            a += 1
                        else:
                            #print 'b'
                            b += 1    # 존재, 미존재                             
                    else:
                        if p2[k]> 0 :# 미존재, 존재
                            #print 'c'
                            c += 1
                        else:         # 미존재, 미존재
                            #print 'd'
                            d += 1
                                
                #print '{},{} : a={},b={},c={},d={}'.format(i, j, a,b,c,d)
                
                if option2 =='simple_matching':
                    result = 1.*(a+d)/(a+b+c+d)
                elif option2 =='jaccard':
                    result = 1.*a/(a+b+c)
                elif option2 == 'russell_and_rao':
                    result = 1.*a/(a+b+c+d)
                elif option2 == 'distance':
                    result = vector_distance(p1,p2)
                else:
                    pass
                
                indexi = namelist[i]
                indexj = namelist[j]
                templist.append([indexi,indexj,result])
    
    df2 = DataFrame(templist, columns=['x','y','value'])
                
    return df2

# pajek 파일 만들기

def f_makingPajekfile_net(df,fout_edge="test_pajek_edge.net"):
    '''
    목적 : df 입력받아서 *.net 파일 만들기 
    
    수정 :   
    
    '''

    
    print ">>> df.index = \n",df.index
    print ">>> len(df.index)=", len(df.index)
    list1  = df['x'].tolist()
    list2  = df['y'].tolist()
    name    = set(list1 + list2)
    name1   = sorted(name)
    length_name = len(name1) # 고유한 이름의 갯수 
    print ">>> name1=", name1
    namedic  = {}
    namedici = {}
    for i, each in enumerate(name1):
        namedici[i]= each
        namedic[each]= i
    
    with codecs.open(fout_edge,'w', 'utf-8') as fn:
        fn.write("*vertices %d\n" %(length_name))
        
        if platform.system() == 'Darwin': #맥용
            for i in range(length_name):
                fn.write("{} \"{}\"\n".format(i+1,namedici[i].encode('utf-8') ) )
                
                # vosviewr에서 하늘 깨짐
        elif platform.system() == 'Windows': #윈도우즈용
            for i in range(length_name):
                
                #txt1 = "{} \"{}\"\n".format(i+1, namedici[i])
                txt1 = "%d \"%s\"\n" %(i+1, namedici[i])
                print txt1
                fn.write(txt1)
                
        fn.write ("*Edges\n")
        
        for i, each in enumerate(df.index):
            p1 = df.iloc[i,0]
            p2 = df.iloc[i,1]
            v  = df.iloc[i,2]
            fn.write("{} {} {}\n".format(namedic[p1]+1,namedic[p2]+1,v))

        print ">>> {} was saved !!!".format(fout_edge)

def vector_distance(v,w):
    vector = v - w 
    distance1 = np.sqrt( np.sum(np.power(vector,2.)))
    return distance1     


# sentence, paragraph
import re 
def making_sentence(data='', option=''):
    """
    목적 : 문자열 data 입력 받아서 문장 리스트 sentence 리턴해줌
    
    원본 : ppp_function
    수정 : 2016.11.11 한글 가능하게 함, 숫자 오류부문 수정 

    """
    data1 = data.strip()
    #re1       = re.compile(r'([a-zA-Z]+\s+[a-zA-Z]+\.)\W')
    #re1       = re.compile(r'([a-zA-Z|가-힣|0-9]+\s+[a-zA-Z|가-힣|0-9]+[\.\?\!])\s')
    re1       = re.compile(ur"([a-zA-Z가-힣0-9]+\s+[a-zA-Z가-힣0-9]+[\.\.\?\!])\s+")
    # 규칙 1. 최소한 단어가 2개 이상 있을 때 sentence로 간주함.
    # 규칙 2. 마지막에 마침표가 있어야 함.
    
    # + 1개 이상등장해야 함 
    # \s white space,
    # 물음표, 느낌표로 끝나면 문장끝이라고 봄
    
    newData   = re1.sub(ur'\1\r\n', data1)
    # 규칙에 부합하는 것을 넘겨 받을 때 \1 을 사용함
    #print "newData=", newData
    sentence  = newData.split('\n')
    sentence2 = []
    for i in range(len(sentence)):
        if sentence[i].strip() != '': #빈줄 제거하기 위해서..
            sentence2.append(sentence[i].strip())
        else:
            pass
    
    # 출력옵션
    if option == 'YES':
        for i, each in enumerate(sentence2):
            print 'Sentence No=',i, each
    return sentence2



def making_sentence_including_keywords(txt='', keyword='', option=''):
    '''
    목적 : 특정단어가 들어 있는 문장만 추출하는 함수 
          문자열 txt 입력받아서,
          리스트 문장단위로 만든후,
          문자열 keyword 가 있는 문장만 추출하고,
          문자열로 합쳐서 리턴해줌 
    수정 : 2016.11.11 생성 
    
    '''
    txt2 = making_sentence(txt, option)
    #for i, each in enumerate(txt2):
    #    print 'sen_no= ',i,' ', each
    
    txt3 = []
    for i, each in enumerate(txt2):
        #print i, each.count(keyword), each
        if each.count(keyword) >= 1 : # 주의 깊게 볼 것 
            #print i, each
            txt3.append(each.strip())
            
    mergedText ='\n'.join(txt3)
    if option == "YES":
        print ">>> below sentences contain ", keyword, 'in ', len(txt3),"sentences"
        for i, each in enumerate(txt3):
            print "sentence No = ", i, each
        print ">>> merged text = in", mergedText, type(mergedText)
    return mergedText


    # 함수선언 : stopwrods 제거 

def dictionary_keywords_from_file(dicfilename='keyword_list.txt'):
    """
    source : factotum.py
    date   : 2016.11.14 이전
    cf. from ppp_function.py

    
    """
    
    print ">>> dictionary_keywords_from_file"
    keywords= {}
    temp = []
    with codecs.open(dicfilename, 'r', 'utf-8') as fn :
        for each in fn:
            each = str(each)
            each = each.strip()

            if "#" in each:  # 주석부호가 있는 란은 삭제함
                pass
            else:
                if each.count("<") >= 1: # < 이 있는 줄만 포함시킴.
                    temp.append(each.lower() ) # 대문자로 바꿈
    for each in temp:
        (name1, name2) = each.split("<")
        name3 = name2.split(',') # , 쉽표
        name4=[]
        for temp in name3:
            temp1 = temp.strip()
            if temp1 != '':
                name4.append(temp1)
        keywords[name1.strip()] =  name4 # 이렇게 복잡하게 하는 이유는 ...

    return keywords# 불러온 단어사전


def keywords_from_dictionary(dic={}, keyword='', option = True):
    '''
    source : factotum.py
    date   : 2016.11.이전

    option : True :   False : 사전리턴하지 않고 입력값을 그냥 그대로 보내줌
    '''
    #print ">>> keywords_from_dictionary"

    if option == True :
        dic_keywords  = dic
        keyword = keyword.lower()
        nocount = 0
        if keyword.strip() == '':
            print "keyword is blank"
            return '-'
        for i, each in enumerate(dic_keywords.items()):
            if keyword in each[1]:
                nocount += 1
                print ">>> %d : %s was changed to %s" %(nocount, keyword, each[0])
                return each[0]    # 입력된 이름이 아닌 대표이름을 리턴해줌.
            else:
                pass
        return keyword # 최종적으로 전달할 것이 없으면, 그냥 입력된 이름을 리턴해줌.
        # (이것때문에 시간 몇시간 소비함)
    else:
        return keyword


def ppp_n_gram(option=2, textlist=[]):

    """
    1. 목적 :
	2. 원본 : 기본소스파일 이름 
	3. 수정 : 날짜
	4. 문제 : 문제사항 메모 
	5. 예제 : example 

    1. < n_gram 만들어 주기 >
    2. 원본 : ppp_function_nltk.py 
    3. 수정 : 2016.11.18
    4. 문제 : 
    5. 예제 : 

    option   : n-gram 일때 앞의 n의 수
    textlist : 단어별로 구분된 텍스트 리스트를 입력 받음 (예) ['hi','my','name']
             * 조심하시기를. 단어별로 구분된 것만 입력해 주시기기를.
    return value : 터플 리스트. (예) [ ( 'hi','my' ), ( 'my','name' ) ]

    #print ">>>ppp_n_gram()" # 너무 자주 호출됨. 그래서 ... 프린트문은 생략함

    """

    n_gram    = []
    gram      = option
    n2     = len(textlist)          # 입력 리스트의 크기, 즉 글자의 갯수
    if n2 < gram :                  # 만약에 입력 리스트의 크기보다도, 그램 갯수가 크다면, 뭘 리턴해 줘야 할까.?
        return [tuple(textlist)] # 입력한 리스트만을 리턴해 줌.

    for i in range(n2 - gram + 1):
        # 글자 처음부터 (i)  마지막 글자까지 (n-1).
        # 그런데, 마지막글자 보다 조금 더 앞까지만 갈수 있다. 왜냐면, n-gram 을 만족하기 위해서는,
        # 예를 들어서
        # gram=2 일때,  (n-2, n-1) 글자까지만 가져올수 있다.
        # gram=3 일때,  (n-3,n-2,n-1) 글자까지만 가져올수 있다.
        #  즉 i=0에서   (n-1) - (gram-1)
        # range( n2 - gram + 1)까지 해주면 된다.

        each = []

        for ni in range(gram):
            each.append(textlist[i+ni])
            # i+ni 로 하는 이유는 ,
            # i=0일때, gram=2일때, 0,1만 첨가시키기 위해서.
            # i=1일때, gram=2일때, 1,2만 첨가시키기 위해서.


        n_gram.append(tuple(each)) # tuple로 변경시켜줌
    return n_gram




if __name__ == '__main__':

    # 엑셀파일의 필드1, 필드2 조건
    # option = { 'no':1 }  # 필드하나만 함 
    # option = { 'no':2, 'fieldname':u'Pname' }  # 필드 여러개함 
    # .net, .vec, .csv 파일 생성됨
    making_pajek_netfile_from_excelfile(filename  = 'total.xlsx', 
                                    fieldname     = 'Morpho2', 
                                    sep           = '|', 
                                    pajekfilename = 'president_total_1208',
                                    option = {'no':1,'fieldname':u'Pname'})

    if 1 == 0 :
        making_pajek_netfile_from_excelfile(filename  = 'total.xlsx', 
                                    fieldname     = 'Morpho2', 
                                    sep           = '|', 
                                    pajekfilename = 'president_',
                                    option = {'no':2,'fieldname':u'Pname'})

