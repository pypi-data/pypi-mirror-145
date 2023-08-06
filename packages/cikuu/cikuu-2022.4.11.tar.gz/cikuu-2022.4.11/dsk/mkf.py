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
		sntdic  = { pair[0] : pair[1] for pair in pairs }  # 1. change to lighter nltk tokenizer 2. when snt=trans, keep unchanged toklist 
		input	= [ mkf_input(i,snts[i],sntdic[snts[i]], [t.text for t in doc], [t.text for t in (doc if snts[i] == sntdic[snts[i]] else getdoc(sntdic[snts[i]]) ) ], doc, diffmerge)  for i, doc in enumerate(docs)]
		mkfs	= requests.post(f"http://{dskhost}/parser", data={"q":json.dumps({"snts":input, "rid":"10"} if asdsk else input).encode("utf-8")}).json()
		#if isinstance(mkfs, list) and adjust_ibeg_byte:  [_adjust_ibeg_byte(doc,mkf) for doc,mkf in zip(docs, mkfs)]
		return mkfs 
	except Exception as ex:
		print(">>gecv1_dsk Ex:", ex, "\t|", pairs)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)
		return {"failed":str(ex)}

def consume(stream, group, rhost='127.0.0.1', rport=6379, rdb=0, waitms=3600000, ttl=7200, precount=64, gecoff:bool=False, dskhost:str="dsk.jukuu.com"):
	''' python mkf.py xsnt mkf , 2022.4.3'''
	import redis
	redis.r		= redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=True) 
	redis.bs	= redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=False) 

	try:
		redis.r.xgroup_create(stream, group,  mkstream=True)
	except Exception as e:
		print(e)

	consumer_name = f'consumer_{socket.gethostname()}_{os.getpid()}'
	print(f"Redis consumer started: {consumer_name}|{stream}|{group}| ", redis.r, flush=True)
	while True:
		item = redis.r.xreadgroup(group, consumer_name, {stream: '>'}, count=precount, noack=True, block= waitms )
		try:
			if not item: break
			snts	= [arr.get('snt','') for id,arr in item[0][1]] #[['xtest', [('1648947215933-0', {'snt': '1'}), ('1648947215933-1', {'2': '2'}), ('1648947215934-0', {'3': '3'}), ('1648947215934-1', {'4': '4'}), ('1648947215934-2', {'5': '5'}), ('1648947215935-0', {'6': '6'}), ('1648947215935-1', {'7': '7'}), ('1648947215935-2', {'8': '8'}), ('1648947215936-0', {'9': '9'})]]]
			newsnts = [snt for snt in snts if snt and not redis.r.exists(f"mkf:{snt}") ]

			### to be updated 2022.4.3
			docs	= [ getdoc(snt) for snt in snts ] 
			sntdic  = { pair[0] : pair[1] for pair in pairs }  #dict(pairs)
			input	= [ mkf_input(i,snts[i],sntdic[snts[i]], [t.text for t in doc], [t.text for t in getdoc(sntdic[snts[i]]) ], doc, diffmerge)  for i, doc in enumerate(docs)]
			mkfs	= requests.post(f"http://{dskhost}/parser", data={"q":input.encode("utf-8")}).json()

			[redis.r.setex(f"mkf:{snt}", ttl, json.dumps(mkf) ) for snt, mkf in zip(snts,mkfs) ]
		except Exception as e:
			print(">>[xconsumeEx]", e, "\t|", item, "\t|",  now())

	redis.r.xgroup_delconsumer(stream, group, consumer_name)
	redis.r.close()
	print ("Quitted:", consumer_name, "\t",now())

if __name__ == '__main__':
	print( sntsmkf(asdsk=False, ))
	import fire 
	fire.Fire(consume) 

'''
def _adjust_ibeg_byte(doc, mkf):
	#ibeg/iend starts with 1,  ^ 
	for k,v in mkf['feedback'].items(): 
		if 'ibeg' in v : v['ibeg_byte'] = doc[ int(v['ibeg']) -1 ].idx # failed to align
		if 'iend' in v : v['iend_byte'] = doc[ int(v['iend']) -1 ].idx
'''