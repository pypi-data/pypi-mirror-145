# 2022.3.20 snt-mkf 
import en,difflib,requests,sys,traceback
trans_diff		= lambda src, trg:  [] if src == trg else [s for s in difflib.ndiff(src, trg) if not s.startswith('?')] #src:list, trg:list
trans_diff_merge= lambda src, trg:  [] if src == trg else [s.strip() for s in "^".join([s for s in difflib.ndiff(src, trg) if not s.startswith('?')]).replace("^+","|+").split("^") if not s.startswith("+") ]
mkf_input		= lambda i, snt, gec, toklist, gec_toklist, doc, diffmerge,pid=0: 	{"pid":pid, "sid":i, "snt":snt, "tok": toklist,  #"offset":-1,"len":-1,"re_sntbr":0,  normally, offset =0
				"pos":[t.tag_ for t in doc], "dep": [t.dep_ for t in doc],"head":[t.head.i for t in doc],  #"tag":[t.tag_ for t in doc],
				"seg":[ ("NP", sp.start, sp.end) for sp in doc.noun_chunks] + [ (np.label_, np.start,np.end) for np in doc.ents] , 
				"gec": gec, "diff": trans_diff_merge( toklist , gec_toklist) if diffmerge else trans_diff( toklist , gec_toklist)	}

def sntmkf(dskhost:str, snt:str, gec:str, diffmerge:bool=False): 
	''' snt -> mkf, for debug only '''
	try:
		doc		= spacy.nlp(snt) 
		tdoc	= spacy.nlp(gec)
		input	= mkf_input( 0,snt,gec, [t.text for t in doc], [t.text for t in tdoc], doc, diffmerge ) 
		return requests.post(f"http://{dskhost}/parser", data={"q":json.dumps({"snts": [input]}).encode("utf-8")}).json()
	except Exception as ex:
		print(">>sntmkf Ex:", ex, "\t|", snt)

def sntsmkf(pairs:list =[["She has ready.","She is ready."], ["It are ok.","It is ok.", 1]], 
		dskhost:str="dsk.jukuu.com", asdsk:bool=False , diffmerge:bool=False, getdoc=lambda snt: spacy.nlp(snt)
		):
	''' snts -> mkfs,  if asdsk=True, return dsk , with info, kw, doc   '''
	try:
		snts	= [ pair[0] for pair in pairs ] 
		pids	= [ pair[2] if len(pair) >= 3 else 0 for pair in pairs ] 
		docs	= [ getdoc(snt) for snt in snts ] 
		sntdic  = { pair[0] : pair[1] for pair in pairs }  #dict(pairs)
		input	= [ mkf_input(i,snts[i],sntdic[snts[i]], [t.text for t in doc], [t.text for t in getdoc(sntdic[snts[i]]) ], doc, diffmerge)  for i, doc in enumerate(docs)]
		return requests.post(f"http://{dskhost}/parser", data={"q":json.dumps({"snts":input, "rid":"10"} if asdsk else input).encode("utf-8")}).json()
	except Exception as ex:
		print(">>gecv1_dsk Ex:", ex, "\t|", pairs)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)
		return {"failed":str(ex)}

if __name__ == '__main__':
	print( sntsmkf(asdsk=False))