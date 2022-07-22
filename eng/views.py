from django.shortcuts import render
from gingerit.gingerit import GingerIt
# import language_tool_python
from googletrans import Translator
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import string
import googletrans
 
def Home(request):
    dict={'lang_p':googletrans.LANGUAGES}
    return render(request,"index.html",dict)
 
def Change(request):
    text=request.GET.get('text')
    grammer=request.GET.get('grammer')
    cap=request.GET.get('cap')
    punc=request.GET.get('punc')
    bold=request.GET.get('bold')
    italic=request.GET.get('italic')
    space=request.GET.get('space')
    lang=request.GET.get('lang')
    olang=request.GET.get('olang')
    dlang=request.GET.get('langip')
    title=request.GET.get('title')
    summary=request.GET.get('summary')
    t=text
    if olang=='on':
        translator=Translator()
        redlang=dlang[:2]
        translated=translator.translate(text,dest=redlang)
        text=translated.text
        
    if lang=='on':
        translator = Translator()
        translated = translator.translate(text)
        print(translator.detect(text))
        text=translated.text
        
    if grammer=='on':
        parser=GingerIt()
        text=parser.parse(t)

    if summary == 'on':
        def sumi(text):
            a=text.split('.')
            sen=[]
            for i in a:
                sen.append(i.replace('[^a-zA-Z]',' ').split())
            sen.pop()
            return sen
        def sen_sim(sent1,sent2,stopwords=None):
            if stopwords is None:
                stopwords=[]
            sent1=[w.lower() for w in sent1]
            sent2=[w.lower() for w in sent2]
            all_words=list(set(sent1+sent2))
            v1=[0]*(len(all_words))
            v2=[0]*(len(all_words))
            for  w in sent1:
                if w in stopwords:
                    continue
                v1[all_words.index(w)]+=1
            for  w in sent2:
                if w in stopwords:
                    continue
                v2[all_words.index(w)]+=1
            return 1-cosine_distance(v1,v2)
        def gen_sim(sen,stop_words):
            mat=np.zeros((len(sen),len(sen)))
            for idx1 in range(len(sen)):
                for idx2 in range(len(sen)):
                    if idx1==idx2:
                        continue
                    else:
                        mat[idx1][idx2]=sen_sim(sen[idx1],sen[idx2],stop_words)
            return mat
        def gen_summary(text,top_n=1):
            stop_words=stopwords.words('english')
            sum_txt=[]
            sen=sumi(text)
            sim_mat=gen_sim(sen,stop_words)
            sen_sim_grph=nx.from_numpy_array(sim_mat)
            scores=nx.pagerank(sen_sim_grph)
            rk_sen=sorted(((scores[i],s) for i,s in enumerate(sen)),reverse=True)
            for i in range(top_n):
                sum_txt.append(" ".join(rk_sen[i][1]))
            return ". ".join(sum_txt)
        n=len(t.split('.'))
        text=gen_summary(t,n-1)
            
    if cap=='on':
        text=text.upper()
 
    if punc=='on':
        sym= string.punctuation
        s=''
        for i in text:
            if i not in sym:
                s+=i
        text=s
    if title=='on':
        text=text.title()
   
    if space=='on':
        s=''
        for i in range(len(text)-1):
            if text[i]!=' ' and text[i+1]!=' ':
                s+=text[i]
            else:
                pass
    
    dict2={
        'text':text,
        'bold':bold,
        'italic':italic,
        'unpurified':t,
        'lang_p':googletrans.LANGUAGES
        }
    return render(request,"index.html",dict2)

