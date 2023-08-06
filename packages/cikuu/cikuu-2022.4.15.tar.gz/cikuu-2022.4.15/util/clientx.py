# client sample, 2022.4.2
import redis, fire

def run(host, port=6379, timeout=10):
	''' host: 127.0.0.1,  192.168.1.55, 192.168.201.120, 172.17.0.1, 172.18.0.1 '''
	r	= redis.Redis(host=host,port=port, decode_responses=True)
	# when topk= 0 or missing, means translate all the sents , gecoff= 1 , to disable gec 
	id  = r.xadd("xwps", {"debug":1, "topk":32, "essay":'''\nProposal for Film Adaptation\nFrom Netflix\n \n216 Driftwood Road, Los Gatos, California, 91355\n(209)658-9336  Email:docxnflx@temporary-mail.net\n\nMarch 28, 2022\n\nLiu Cixin'''})
	print ( "id:", id,flush=True)
	res	= r.blpop([f"suc:{id}",f"err:{id}"], timeout=timeout)
	print (res if res is not None else "result is None") 

if __name__ == '__main__':
	fire.Fire(run)
