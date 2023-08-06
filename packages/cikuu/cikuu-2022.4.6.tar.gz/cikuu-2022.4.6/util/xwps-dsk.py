# 2022.4.2
import json, time, traceback, en, fire,sys, redis, hashlib ,socket 
from dsk import mkf,gecv1

now				= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
trantab			= str.maketrans("，。！“”‘’；：？％＄＠＆＊（）［］＋－ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ１２３４５６７８９０ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ", ",.!\"\"'';:?%$@&*()[]+-ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz") #str.translate(trantab)
is_sent_valid	= lambda snt:	snt.isascii() if snt else False

def getscore(snts): 
	''' '''
	from en.dims import docs_to_dims
	from dsk.score import dims_score
	docs = [ ( bs := redis.bs.get(f"bs:{snt}"), doc := spacy.frombs(bs) if bs else spacy.nlp(snt))[-1] for snt in snts ]
	dims = docs_to_dims(snts, docs) 
	if not 'internal_sim' in dims: dims['internal_sim'] = 0.2
	return dims_score(dims) 

def gecv1_dsk(arr:dict={"essay":"English is a internationaly language which becomes importantly for modern world. 中文In China, English is took to be a foreigh language which many student choosed to learn. They begin to studying English at a early age. They use at least one hour to learn English knowledges a day. Even kids in kindergarten have begun learning simple words. That's a good phenomenan, for English is essential nowadays. In addition to, some people think English is superior than Chinese. In me opinion, though English is for great significance, but English is after all a foreign language. it is hard for people to see eye to eye. English do help us read English original works, but Chinese helps us learn a true China. Only by characters Chinese literature can send off its brilliance. Learning a country's culture, especial its classic culture, the first thing is learn its language. Because of we are Chinese, why do we give up our mother tongue and learn our owne culture through a foreign language?"},):  
	''' asdsk:bool=True, diffmerge:bool=False,  topk_snts:int=0, gecoff:bool=True, dskhost:str="172.17.0.1:7095",  '''
	try:
		start	= time.time()
		id		= arr.get('id','0')
		essay	= arr.get("essay", arr.get('doc','')).strip()
		redis.r.zadd(f"tim:{id}", {'start':start})
		if not essay: return {"failed":"empty essay"}

		sntpids = spacy.sntpid(essay)  # [(snt,pid) ]
		snts	= [snt for snt,pid in sntpids ]
		cleans  = [snt.translate(trantab) for snt in snts] # keep the same length
		tags	= [ is_sent_valid(snt.strip()) for snt in cleans] # True/False : is pure English or not
		valids  = [ clean for clean, tag in zip(cleans, tags) if tag ]
		redis.r.zadd(f"tim:{id}", {'sntbr':time.time()}) #pairs	=  snt_pairs(essay) # (snt, True/False) 
		[redis.r.xadd('xsnt', {'snt':snt}) for snt in valids]

		sntdic	= gecv1.gecsnts(valids, topk =int(arr.get('topk',0))) if not 'gecoff' in arr else {snt:snt for snt in valids}
		redis.r.zadd(f"tim:{id}", {'gec':time.time()})

		if 'debug' in arr: 	 #redis.r.hmset(f"debug:{id}", sntdic)
			hitted_snts = [ snt for snt in valids if redis.bs.exists(f'bs:{snt}')] # pre-set by xsnt-spacy
			redis.r.hset(f"debug:{id}", "hitted", len(hitted_snts), {"hitted_ratio": len(hitted_snts)/(len(valids)+0.1), "total_valid_sent": len(valids)})
			
		mkfs = mkf.sntsmkf([ (snt, sntdic.get(snt, snt)) for snt in valids ], 
					dskhost = redis.dskhost,  asdsk=False, 	diffmerge=arr.get('diffmerge', False), 
					getdoc=lambda snt: ( bs := redis.bs.get(f"bs:{snt}"), doc := spacy.frombs(bs) if bs else spacy.nlp(snt), redis.bs.setex(f"bs:{snt}", 7200, spacy.tobs(doc)) if not bs else None )[1] ) if valids else []
		sntmkf = dict(zip(valids, mkfs))
		redis.r.zadd(f"tim:{id}", {'mkfs':time.time()})
		redis.r.expire(f"tim:{id}", redis.ttl)
		
		if 'score' in arr:  arr.update( getscore(valids))  # only topk considered
		arr["timing"] = time.time() - start

		fds = [ sntmkf.get(clean, {'feedback':{}, 'meta':{'snt':snt}}) for snt, clean in zip(snts,cleans) ] #, 'clean': clean
		[ fd['meta'].update({"sid":i}) for i, fd in enumerate(fds) ]
		[ fd['meta'].update({"pid":sntpid[1]}) for sntpid, fd in zip(sntpids,fds) ]
		return {'snt': fds,  "info": arr}

	except Exception as ex:
		print(">>gecv1_dsk Ex:", ex, "\t|", arr)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)
		return str(ex)

def consume(stream, group, host='127.0.0.1', port=6379, db=0, maxlen=100000, waitms=3600000, ttl=7200, dskhost="172.17.0.1:7095"):
	''' python xwps-dsk.py xwps dsk --host 192.168.201.120 
	XTRIM mystream MAXLEN ~ 1000
	'''
	redis.r		= redis.Redis(host=host, port=port, db=db, decode_responses=True) 
	redis.bs	= redis.Redis(host=host, port=port, db=db, decode_responses=False) 
	redis.ttl	= ttl
	redis.dskhost= dskhost
	try:
		redis.r.xgroup_create(stream, group,  mkstream=True)
	except Exception as e:
		print(e)
	redis.r.xtrim(stream, maxlen)
	
	print(gecv1_dsk(), flush=True) # warmup, to init gpu , if any 
	consumer_name = f'consumer_{socket.gethostname()}_{os.getpid()}'
	print(f"Redis consumer started: {consumer_name}|{stream}|{group}| ", redis.r, flush=True)
	while True:
		item = redis.r.xreadgroup(group, consumer_name, {stream: '>'}, count=1, noack=True, block= waitms )
		try:
			if not item: break
			id,arr = item[0][1][0]  #[['_new_snt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
			redis.r.hset(f"debug:{id}", "inputlen", len(arr), {'time': now()})
			redis.r.expire(f"debug:{id}", ttl)

			try:
				arr['id'] = id 
				dsk = gecv1_dsk(arr)
				res = json.dumps(dsk)
				redis.r.lpush(f"suc:{id}", res )
				redis.r.expire(f"suc:{id}", ttl) 
			except Exception as e1:
				print ("parse err:", e1, arr) 
				redis.r.lpush(f"err:{id}", json.dumps(arr))
				redis.r.expire(f"err:{id}", ttl) 
				redis.r.setex(f"exception:{id}", ttl, str(e1))

		except Exception as e:
			print(">>[xconsumeEx]", e, "\t|", item, "\t|",  now())

	redis.r.xgroup_delconsumer(stream, group, consumer_name)
	redis.r.close()
	print ("Quitted:", consumer_name, "\t",now())

if __name__ == '__main__':
	fire.Fire(consume)  
	#fire.Fire({"consume":consume, "hello":lambda : print(gecv1_dsk()), }

'''
ImportError: cannot import name 'docs_to_dim' from 'en.dims' (/home/ubuntu/data/miniconda3/envs/cuda113/lib/python3.8/site-packages/en/dims.py)
#snt_pairs		= lambda essay: [ (snt.text,is_sent_valid(snt.text.strip())  ) for snt in spacy.sntbr(essay).sents]
#snts		= lambda essay: [ snt.text for snt in spacy.sntbr(essay).sents ]
#cleans		= lambda snts: [snt.translate(trantab) for snt in snts]  # keep the same length
#tags		= lambda cleans: [ is_sent_valid(snt.strip()) for snt in cleans] # True/False : is pure English or not
#valids		= lambda snts, tags: [ snt for snt, tag in zip(snts, tags) if tag ]

		eng_snts = [] # only keep pure English sents
		snt_toid = {}
		for i, row in enumerate(pairs):
			if row[1]:
				snt_toid[i] = len(eng_snts)
				eng_snts.append( row[0])
'''