# 2022.4.6  upgrade of xwps-dsk.py, add mq support 
import json, time, traceback, fire,sys, redis, hashlib ,socket,os

rhost		= os.getenv("rhost", "127.0.0.1")
rport		= int(os.getenv('rport', 6379))
rdb			= int(os.getenv('rdb', 0))
redis.r		= redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=True) 
redis.bs	= redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=False) 
redis.ttl	= int (os.getenv("ttl", 7200) )
redis.dskhost= os.getenv("dskhost", "172.17.0.1:7095")
now			= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
trantab		= str.maketrans("，　。！“”‘’；：？％＄＠＆＊（）［］＋－ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ１２３４５６７８９０ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ", ", .!\"\"'';:?%$@&*()[]+-ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz") #str.translate(trantab)
is_ascii    = lambda snt: ( res:=snt.translate(trantab).strip(), res.isascii() if res else False)[-1] #is_valid	= lambda snt:	snt.isascii() if snt else False

import spacy
if not hasattr(spacy, 'nlp'):
	from spacy.lang import en
	spacy.sntbr		= (inst := en.English(), inst.add_pipe("sentencizer"))[0]
	spacy.snts		= lambda essay, trim=True: [ snt.text.strip() if trim else snt.text for snt in  spacy.sntbr(essay).sents]
	spacy.sntpid	= lambda essay: (pid:=0, [ ( pid := pid + 1 if "\n" in snt.text else pid,  (snt.text, pid))[-1] for snt in  spacy.sntbr(essay).sents] )[-1]
	spacy.sntpidoff	= lambda essay: (pid:=0, doc:=spacy.sntbr(essay), [ ( pid := pid + 1 if "\n" in snt.text else pid,  (snt.text, pid, doc[snt.start].idx))[-1] for snt in  doc.sents] )[-1]
	spacy.nlp		= spacy.load('en_core_web_sm')
	spacy.frombs	= lambda bs: list(spacy.tokens.DocBin().from_bytes(bs).get_docs(spacy.nlp.vocab))[0] if bs else None
	spacy.tobs		= lambda doc: ( doc_bin:= spacy.tokens.DocBin(), doc_bin.add(doc), doc_bin.to_bytes())[-1]

def getscore(snts): 
	''' '''
	from en.dims import docs_to_dims
	from dsk.score import dims_score
	docs = [ ( bs := redis.bs.get(f"bs:{snt}"), doc := spacy.frombs(bs) if bs else spacy.nlp(snt))[-1] for snt in snts ]
	dims = docs_to_dims(snts, docs) 
	if not 'internal_sim' in dims: dims['internal_sim'] = 0.2
	return dims_score(dims) 

def gecsnts(snts:list=["She has ready.","It are ok."], topk=0, timeout=3):
	''' use blpop-based func, 2022.4.4 '''
	from dsk import xgecv1 
	try:
		gecs	= redis.r.mget([ f"gec:{snt}" for snt in snts])
		newsnts = [snt for snt, gec in zip(snts, gecs) if snt and gec is None ]
		if topk > 0 and len(newsnts) > topk : newsnts = newsnts[0:topk] # only trans topk sents

		res		= xgecv1.xgecsnts_blpop(newsnts, timeout=timeout) 
		if res is None : # how to notify the result of this timeout event? 
			redis.r.publish('gecv1_timeout', json.dumps(snts)) #arr['gecv1_timeout'] = newsnts # for debug 
			return { snt: gec for snt, gec in zip(snts, gecs) if gec is not None}

		sntdic  = json.loads(res[1]) #('suc:1649063447036-0', '{"She has ready.": "She is ready.", "It are ok.": "It is ok."}')
		return { snt: gec if gec is not None else sntdic.get(snt,snt) for snt, gec in zip(snts, gecs)}
	except Exception as ex:
		print(">>gecsnts Ex:", ex, "\t|", snts)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)
		return {}

def _adjust_by_wordlist(snt, mkf):
	''' '''
	for k,v in mkf['feedback'].items(): 
		if 'word_list' in v:
			offset = snt.find(v['word_list']) 
			if offset >= 0: 
				v['ibeg_byte'] = offset 
				v['iend_byte'] = offset + len(v['word_list'])
		else: 
			del v['ibeg_byte']
			del v['iend_byte']

def gecv1_dsk(arr:dict={"essay":"English is a internationaly language which becomes importantly for modern world. 中文In China, English is took to be a foreigh language which many student choosed to learn. They begin to studying English at a early age. They use at least one hour to learn English knowledges a day. Even kids in kindergarten have begun learning simple words. That's a good phenomenan, for English is essential nowadays. In addition to, some people think English is superior than Chinese. In me opinion, though English is for great significance, but English is after all a foreign language. it is hard for people to see eye to eye. English do help us read English original works, but Chinese helps us learn a true China. Only by characters Chinese literature can send off its brilliance. Learning a country's culture, especial its classic culture, the first thing is learn its language. Because of we are Chinese, why do we give up our mother tongue and learn our owne culture through a foreign language?"}, timeout=3):  
	''' asdsk:bool=True, diffmerge:bool=False,  topk:int=0, gecoff:bool=True, dskhost:str="172.17.0.1:7095",  '''
	from dsk import mkf 
	try:
		start	= time.time()
		id		= arr.get('id',arr.get('key','0'))
		essay	= arr.get("essay", arr.get('doc','')) #.strip()
		redis.r.zadd(f"tim:{id}", {'start':start})
		if not essay: return {"failed":"empty essay"}

		sntpids = spacy.sntpid(essay)  # [(snt,pid) ]
		snts	= [snt for snt,pid in sntpids ] 	#cleans  = [snt.translate(trantab) for snt in snts] # keep the same length
		tags	= [ is_ascii(snt) for snt in snts] # True/False : is pure English or not
		valids  = [ snt for snt, tag in zip(snts, tags) if tag ]
		redis.r.zadd(f"tim:{id}", {'sntbr':time.time()}) #pairs	=  snt_pairs(essay) # (snt, True/False) 
		[redis.r.xadd('xsnt', {'snt':snt}) for snt in valids]  # notify:  spacy/gec 

		sntdic  = gecsnts(valids, topk =int(arr.get('topk',0)), timeout=timeout) #sntdic	= gecv1.gecsnts(valids, topk =int(arr.get('topk',0))) if not 'gecoff' in arr else {snt:snt for snt in valids}
		redis.r.zadd(f"tim:{id}", {'gec':time.time()})

		if 'debug' in arr: 
			redis.r.hset(f"snts:{id}", "valids", json.dumps(valids), {"tags": json.dumps(tags), "snts":json.dumps([snt for snt,pid in sntpids ]),"pids":json.dumps([pid for snt,pid in sntpids ])})
			hitted_snts = [ snt for snt in valids if redis.bs.exists(f'bs:{snt}')] # pre-set by xsnt-spacy
			redis.r.hset(f"debug:{id}", "hitted-spacy-cnt", len(hitted_snts), 
				{"hitted-spacy-ratio": len(hitted_snts)/(len(valids)+0.1), 
				"hitted-gec-cnt": len([ snt for snt in valids if redis.bs.exists(f'gec:{snt}')]),
				"total-valid-sent": len(valids)})
			
		mkfs = mkf.sntsmkf([ (snt, sntdic.get(snt, snt)) for snt in valids ], 
					dskhost = redis.dskhost,  asdsk=False, 	diffmerge=arr.get('diffmerge', False), 
					getdoc=lambda snt: ( bs := redis.bs.get(f"bs:{snt}"), doc := spacy.frombs(bs) if bs else spacy.nlp(snt), redis.bs.setex(f"bs:{snt}", 7200, spacy.tobs(doc)) if not bs else None )[1] ) if valids else []
		[_adjust_by_wordlist(snt,mkf) for snt,mkf in zip(valids, mkfs)]

		sntmkf = dict(zip(valids, mkfs))
		redis.r.zadd(f"tim:{id}", {'mkfs':time.time()})
		[redis.r.expire(f"{name}:{id}", redis.ttl) for name in ('tim','debug','snts')]
		
		if 'score' in arr:  arr.update( getscore(valids))  # only topk considered
		arr["timing"] = time.time() - start

		fds = [ sntmkf.get(snt, {'feedback':{}, 'meta':{'snt':snt}}) for snt in snts ] 
		[ fd['meta'].update({"sid":i}) for i, fd in enumerate(fds) ]
		[ fd['meta'].update({"pid":sntpid[1], "snt_ori": sntpid[0]}) for sntpid, fd in zip(sntpids,fds) ]
		return {'snt': fds,  "info": arr}

	except Exception as ex:
		print(">>gecv1_dsk Ex:", ex, "\t|", arr)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)
		return str(ex)

def xconsume(stream, group, maxlen=100000, waitms=3600000):
	'''rhost=192.168.201.120 python xwps.py xconsume xwps dsk
	XTRIM mystream MAXLEN ~ 1000
	'''
	try:
		redis.r.xgroup_create(stream, group,  mkstream=True)
		#redis.r.xtrim(stream, maxlen)
	except Exception as e:
		print(e)
		
	print(gecv1_dsk(), flush=True) # warmup, to init gpu , if any 
	consumer_name = f'consumer_{socket.gethostname()}_{os.getpid()}'
	print(f"** xpws redis consumer started: {consumer_name}|{stream}|{group}| ", redis.r, flush=True)
	while True:
		item = redis.r.xreadgroup(group, consumer_name, {stream: '>'}, count=1, noack=True, block= waitms )
		try:
			if not item: break
			id,arr = item[0][1][0]  #[['_new_snt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
			redis.r.hset(f"debug:{id}", "inputlen", len(arr), {'time': now()})
			redis.r.expire(f"debug:{id}", redis.ttl)

			try:
				arr['id'] = id 
				dsk = gecv1_dsk(arr)
				redis.r.lpush(f"suc:{id}", json.dumps(dsk) )
				redis.r.expire(f"suc:{id}", redis.ttl) 
			except Exception as e1:
				print ("parse err:", e1, arr) 
				redis.r.lpush(f"err:{id}", json.dumps(arr))
				redis.r.expire(f"err:{id}", redis.ttl) 
				redis.r.setex(f"exception:{id}", redis.ttl, str(e1))

		except Exception as e:
			print(">>[xconsumeEx]", e, "\t|", item, "\t|",  now())

	redis.r.xgroup_delconsumer(stream, group, consumer_name)
	redis.r.close()
	print ("Quitted:", consumer_name, "\t",now())

def consume(queue, host='172.17.0.1', port=5672, user='pigai', pwd='NdyX3KuCq', durable=True, heartbeat=0, prefetch_count=1, debug=False,
		essay_field = 'essay', gecoff=False, score=False, topk= 0, # when> 0, mean only topk snts considered 
		dsk_exchange="wps-dsk", routing_key="wps-dsk-to-callback",  #wps-dsk-to-callback  pigai_callback_api_essay
		essay_exchange = 'wps-essay', expired_routing_key="wps-essay-long", timeout=3, failed_routing_key="wps-essay-failed"):
	''' mq consumer, set timeout = -1, upon long-essay '''
	import pika 
	credentials = pika.PlainCredentials(user, pwd)
	parameters	= pika.ConnectionParameters(host, port, '/', credentials, heartbeat=heartbeat)
	connection	= pika.BlockingConnection(parameters)
	channel		= connection.channel()
	channel.queue_declare(queue=queue, durable=durable)
	channel.basic_qos(prefetch_count=prefetch_count)

	def callback(ch, method, properties, body):
		try:
			body	= body.decode(encoding='UTF-8',errors='ignore')
			key		= arr.get('key',hashlib.md5(body.encode(encoding='UTF-8')).hexdigest())
			arr		= json.loads(body, strict=False) if body.startswith("{") else {"key":key, "essay": body} # allow mq to store pure essay string

			if not 'id' in arr : arr['id'] = arr['key'] 
			if gecoff : arr['gecoff'] = 1
			if score:	arr['score'] = 1
			if topk >0 : arr['topk'] = topk 

			mkfs	= gecv1_dsk( arr, timeout=timeout ) 
			ch.basic_publish(exchange=arr.get('exchange', dsk_exchange), routing_key=arr.get("routing_key",routing_key), body=json.dumps(mkfs))

		except Exception as err:
			ch.basic_publish(exchange=essay_exchange, routing_key=failed_routing_key, body=body)
			print("Failed:", err, "\n", body)
			exc_type, exc_value, exc_traceback_obj = sys.exc_info()
			traceback.print_tb(exc_traceback_obj)

		ch.basic_ack(delivery_tag = method.delivery_tag)

	print("begin to consume queue: ", queue, host, port, flush=True)
	channel.basic_consume(queue, callback, auto_ack=False)
	channel.start_consuming()

def process(infile, outfile=None):
	''' line json -> dsk  '''
	print ("started to process:", infile, flush=True)
	with open(outfile if outfile else infile + ".dsk" , 'w') as fw: 
		for line in open(infile, 'r').readlines():
			try:
				arr = json.loads(line.strip(), strict=False)
				dsk = gecv1_dsk(arr)
				fw.write( json.dumps(dsk)  + "\n")
			except Exception as ex:
				print ("process ex:", ex, line[0:36]) 
	print ('finished:', infile) 

if __name__ == '__main__':
	fire.Fire({"consume":consume, "xconsume":xconsume, 'process':process, 
	'testdsk': lambda: gecv1_dsk(), 
	'gecsnts': lambda: gecsnts(),
	'testgec': lambda: ( redis.r.delete('gec:She has ready.'),  gecsnts(['gec:She has ready.']) )[-1],  #rhost=192.168.201.120 python xwps.py testgec  | gec:She has ready.: She is ready.
	})
