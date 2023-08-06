# 2022.4.2
import json, time, traceback, en, fire,sys, redis, hashlib ,socket #, util
from dsk import mkf,gecv1

now				= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
#logger			= util.getlog("xwps-dsk.log")
is_sent_valid	= lambda snt:	( snt := snt.strip(), snt.isascii() if snt else False )[-1]
valid_snts		= lambda essay: [ (snt.text,snt[0].idx  ) for snt in spacy.sntbr(essay).sents if is_sent_valid(snt.text)]

def gecv1_dsk(arr:dict={"key":"1002-3", "essay":"English is a internationaly language which becomes importantly for modern world. In China, English is took to be a foreigh language which many student choosed to learn. They begin to studying English at a early age. They use at least one hour to learn English knowledges a day. Even kids in kindergarten have begun learning simple words. That's a good phenomenan, for English is essential nowadays. In addition to, some people think English is superior than Chinese. In me opinion, though English is for great significance, but English is after all a foreign language. it is hard for people to see eye to eye. English do help us read English original works, but Chinese helps us learn a true China. Only by characters Chinese literature can send off its brilliance. Learning a country's culture, especial its classic culture, the first thing is learn its language. Because of we are Chinese, why do we give up our mother tongue and learn our owne culture through a foreign language?"},):  
	''' asdsk:bool=True, diffmerge:bool=False,  topk_snts:int=0, gecoff:bool=True, dskhost:str="172.17.0.1:7095",  '''
	try:
		start	= time.time()
		id		= arr.get('id','0')
		essay	= arr.get("essay", arr.get('doc','')).strip()
		redis.r.zadd(f"tim:{id}", {'start':start})
		if not essay: return {"failed":"empty essay"}

		pairs	=  valid_snts(essay) # (snt, offset) 
		topk_snts = int(arr.get('topk_snts',0))
		if topk_snts > 0 and topk_snts < len(pairs):  pairs = pairs[0:topk_snts]
		redis.r.zadd(f"tim:{id}", {'sntbr':time.time()})

		snts	= [row[0] for row in pairs]
		[redis.r.xadd('xsnt', {'snt':snt}) for snt in snts]
		sntdic	= gecv1.gecsnts(snts, topk =int(arr.get('topk',0))) if not 'gecoff' in arr else {snt:snt for snt in snts}
		redis.r.zadd(f"tim:{id}", {'gec':time.time()})

		if 'debug' in arr: 	 #redis.r.hmset(f"debug:{id}", sntdic)
			hitted_snts = [ snt for snt in snts if redis.bs.exists(f'bs:{snt}')] # pre-set by xsnt-spacy
			redis.r.hset(f"debug:{id}", "hitted", len(hitted_snts), {"hitted_ratio": len(hitted_snts)/(len(snts)+0.1), "total_sent": len(snts)})
			
		dsk		= mkf.sntsmkf([ (row[0], sntdic.get(row[0], row[0])) for row in pairs], 
					dskhost = redis.dskhost, 
					asdsk=arr.get('asdsk', True),
					diffmerge=arr.get('diffmerge', False), 
					getdoc=lambda snt: ( bs := redis.bs.get(f"bs:{snt}"), doc := spacy.frombs(bs) if bs else spacy.nlp(snt), redis.bs.setex(f"bs:{snt}", 7200, spacy.tobs(doc)) if not bs else None )[1] ) if snts else { "snt":[]} #[{'feedback': {'_modern@confusion': {'cate': 
		redis.r.zadd(f"tim:{id}", {'dsk':time.time()})
		
		if 'snt' in dsk: [ arsnt.get('meta',{}).update({'offset': pairs[i][1]})  for i, arsnt in enumerate(dsk['snt']) ]
		if not 'info' in dsk: dsk['info'] = {}
		dsk['info'].update(arr)
		dsk['info'].update({"timing": time.time() -start})
		if 'debug' in arr: redis.r.setex(f"dsk:{id}", redis.ttl, json.dumps(dsk))
		redis.r.zadd(f"tim:{id}", {'asjson':time.time()})
		redis.r.expire(f"tim:{id}", redis.ttl)
		return dsk 
	except Exception as ex:
		print(">>gecv1_dsk Ex:", ex, "\t|", arr)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)
		return str(ex)

def consume(stream, group, host='127.0.0.1', port=6379, db=0, waitms=3600000, ttl=7200, dskhost="172.17.0.1:7095"):
	''' python xwps-dsk.py xwps dsk --host 192.168.201.120 '''
	redis.r		= redis.Redis(host=host, port=port, db=db, decode_responses=True) 
	redis.bs	= redis.Redis(host=host, port=port, db=db, decode_responses=False) 
	redis.ttl	= ttl
	redis.dskhost= dskhost
	try:
		redis.r.xgroup_create(stream, group,  mkstream=True)
	except Exception as e:
		print(e)
	
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
	fire.Fire(consume)  #	"hello":lambda : print(gecv1_dsk()), 
