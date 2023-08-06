# 22-4-6   
import json,os,uvicorn,time,sys
from fastapi import FastAPI, File, UploadFile,Form, Body
from fastapi.responses import HTMLResponse
from collections import Counter
app	 = FastAPI() 

import en

@app.get('/')
def home(): 
	return HTMLResponse(content=f"<h2>dsk, wrapper of dsk-7095</h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br> python -m dsk.uvirun 17095 <br><br> 2022.4.6")


import spacy,difflib,requests
nlp = spacy.load('en_core_web_sm')
from spacy.lang import en
spacy.sntbr		= (inst := en.English(), inst.add_pipe("sentencizer"))[0]
spacy.snts		= lambda essay: [ snt.text.strip() for snt in  spacy.sntbr(essay).sents]
spacy.sntpid	= lambda essay: (pid:=0, [ ( pid := pid + 1 if "\n" in snt.text else pid,  (snt.text, pid))[-1] for snt in  spacy.sntbr(essay).sents] )[-1]
trans_diff		= lambda src, trg:  [] if src == trg else [s for s in difflib.ndiff(src, trg) if not s.startswith('?')] #src:list, trg:list
trans_diff_merge= lambda src, trg:  [] if src == trg else [s.strip() for s in "^".join([s for s in difflib.ndiff(src, trg) if not s.startswith('?')]).replace("^+","|+").split("^") if not s.startswith("+") ]
mkf_input		= lambda i, snt, gec, toklist, gec_toklist, doc, diffmerge,pid=0: 	{"pid":pid, "sid":i, "snt":snt, "tok": toklist,  #"offset":-1,"len":-1,"re_sntbr":0,
				"pos":[t.tag_ for t in doc], "dep": [t.dep_ for t in doc],"head":[t.head.i for t in doc],  #"tag":[t.tag_ for t in doc],
				"seg":[ ("NP", sp.start, sp.end) for sp in doc.noun_chunks] + [ (np.label_, np.start,np.end) for np in doc.ents] , 
				"gec": gec, "diff": trans_diff_merge( toklist , gec_toklist) if diffmerge else trans_diff( toklist , gec_toklist)	}

@app.post('/gecv1/dsk')
def gecv1_dsk(arr:dict={"key":"1002-3", "rid":"10", "essay":"English is a internationaly language which becomes importantly for modern world. In China, English is took to be a foreigh language which many student choosed to learn. They begin to studying English at a early age. They use at least one hour to learn English knowledges a day. Even kids in kindergarten have begun learning simple words. That's a good phenomenan, for English is essential nowadays. In addition to, some people think English is superior than Chinese. In me opinion, though English is for great significance, but English is after all a foreign language. it is hard for people to see eye to eye. English do help us read English original works, but Chinese helps us learn a true China. Only by characters Chinese literature can send off its brilliance. Learning a country's culture, especial its classic culture, the first thing is learn its language. Because of we are Chinese, why do we give up our mother tongue and learn our owne culture through a foreign language?"}, 
	diffmerge:bool=False, body:str='essay', gecon:bool=True, dskhost:str="172.17.0.1:7095", asjson:bool=True):  #dsk.jukuu.com
	''' when 'rid':"10", to return dsk dict, else return mkf list 
	# {"snts":["hello world","I am ok."]} => mkfs if no 'rid' included
	'''
	try:
		sntpids = spacy.sntpid(arr.get(body,''))
		snts	= [snt.strip() for snt in arr['snts'] ] if 'snts' in arr else [ snt for snt,pid in sntpids ]  #spacy.snts( arr.get(body,''))
		docs	= [ nlp(snt) for snt in snts ] 
		mapgec	= pipeline_snts(snts) if gecon else { snt:snt for snt in snts}
		arr["snts"]	= [ mkf_input(i,snts[i],mapgec[snts[i]], [t.text for t in doc], [t.text for t in (doc if mapgec[snts[i]] == snts[i] else nlp(mapgec[snts[i]]) ) ], doc, diffmerge)  for i, doc in enumerate(docs) if snts[i] ] # check empty snt ? 
		res = requests.post(f"http://{dskhost}/parser", data={"q":json.dumps(arr).encode("utf-8")})
		return res.json() if asjson else res.text
	except Exception as ex:
		print(">>gecv1_dsk Ex:", ex, "\t|", arr)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)
		return str(ex)

@app.get('/dskdm/dim/{rid}')
def rid_dim(rid:str="2536901", dim:str='awl'):  
	''' 2536901   awl/ast/None
	return {eidv:dim} ''' 
	return {eidv: json.loads(redis.r.hget(eidv,'dim'))[dim] for eidv in eidvlist([rid.strip()])} if dim else {eidv: json.loads(redis.r.hget(eidv,'dim')) for eidv in eidvlist([rid.strip()])}

@app.get('/dskdm/trp/{rid}')
def rid_poslemmas(rid:str="2536901", rel:str='dobj_VERB_NOUN', topk:int=None):  
	''' 2536901   rel: dobj_VERB_NOUN/amod_NOUN_ADJ/nsubj_VERB_NOUN
	return Counter ''' 
	si = Counter()
	dep,gpos,dpos = rel.strip().split('_')[0:3]
	for eidv in eidvlist([rid.strip()]):
		for doc in eidv_docs(eidv):
			[ si.update({ f"{t.head.lemma_} {t.lemma_}" :1}) for t in doc if t.dep_ == dep and t.head.pos_ == gpos and t.pos_ == dpos ]
	return si.most_common(topk)

def run(port):
	uvicorn.run(app, host='0.0.0.0', port=port)

if __name__ == '__main__': 
	import fire
	fire.Fire(run)	