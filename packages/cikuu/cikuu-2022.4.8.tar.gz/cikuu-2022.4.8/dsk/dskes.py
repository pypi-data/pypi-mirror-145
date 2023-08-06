# 22-3-13 
import json, sys, time, fire,traceback, os
from elasticsearch import Elasticsearch,helpers
from dsk import *

dskes_host  = os.getenv("dskes_host", "127.0.0.1") 
dskes_port  = os.getenv("dskes_host", 9200)
fire.es		= Elasticsearch([ f"http://{dskes_host}:{dskes_port}" ]) 

def get_eid_ver(eid):
	try:
		res = fire.es.get(index=fire.index, id=id) # doc_type=self.index_type,
		return int(res['hits']['hits']['_source'].get('ver',0))
	except Exception as ex:
		return 0

def index_dsk(dsk, index, rid, uid, eid, ver) : 
	try:
		info = dsk.get("info", {})
		snts  = [ ar['meta']['snt'].strip() for ar in dsk['snt']] 
		final_score = float( info.get('final_score',0) ) 
		if ver <= get_eid_ver(eid): return 
		fire.es.delete_by_query(index=fire.index, conflicts='proceed', body={"query":{"match":{"eid":eid}}})

		actions=[]
		actions.append({'_op_type':'index', '_index':index, '_id': eid, '_source':{'type':'doc', 'eid': eid, 'rid': rid , 'uid': uid, 'ver':ver, 'final_score':final_score}})
		for idx, snt in enumerate(snts) : 
			doc = spacy.getdoc(snt.strip())
			sntlen = len(doc)
			if not sntlen : continue
			actions.append({'_op_type':'index', '_index':index,  '_id': f"{eid}:snt-{idx}",  '_source': {'snt':doc.text, "eid":eid, 'rid': rid , 'uid': uid, 'tc':sntlen, 'awl': sum([ len(t.text) for t in doc])/sntlen ,  'type':'snt',	'postag':' '.join(['^'] + [f"{t.text}_{t.lemma_}_{t.tag_}_{t.pos_}" for t in doc] + ['$']) }})
			[actions.append({'_op_type':'index', '_index':index, '_id': f"{eid}:snt-{idx}:trp-{t.i}",  '_source': {"eid":eid, 'rid': rid , 'uid': uid,'type':'trp', 'src': f"{eid}:snt-{idx}", 'gov': t.head.lemma_, 'rel': f"{t.dep_}_{t.head.pos_}_{t.pos_}", 'dep': t.lemma_ }}) for t in doc if t.dep_ not in ('punct')]
			[actions.append({'_op_type':'index', '_index':index, '_id': f"{eid}:snt-{idx}:tok-{t.i}",  '_source': {"eid":eid, 'rid': rid , 'uid': uid,'type':'tok', 'src': f"{eid}:snt-{idx}", 'lex': t.text, 'low': t.text.lower(), 'lem': t.lemma_, 'pos': t.pos_, 'tag': t.tag_, 'i':t.i, 'head': t.head.i }}) for t in doc]
			[actions.append({'_op_type':'index', '_index':index, '_id': f"{eid}:snt-{idx}:np-{np.start}",  '_source': {"eid":eid, 'rid': rid , 'uid': uid,'type':'np', 'src': f"{eid}:snt-{idx}", 'lem': doc[np.end-1].lemma_, 'chunk': np.text, }}) for np in doc.noun_chunks]
		
			for ar in dsk['snt']:
				for kp, v in ar['feedback'].items():
					actions.append({'_op_type':'index', '_index':index,  '_id': f"{eid}:snt-{idx}:kp-{v['ibeg']}",  '_source': {"eid":eid, 'rid': rid , 'uid': uid, 'type':'feedback',
					'src': f"{eid}:snt-{idx}",  'kp':v['kp'], 'cate': v['cate']} })

		helpers.bulk(client=fire.es,actions=actions, raise_on_error=False)
		if fire.debug: print ("eid:", eid, 'ver:', ver, "rid:", rid, "uid:", uid)
	except Exception as ex:
		print ('index_dsk ex:', ex)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)

def readline(infile, sepa=None):
	with open(infile, 'r') as fp: #,encoding='utf-8'
		while True:
			line = fp.readline()
			if not line: break
			yield line.strip().split(sepa) if sepa else line.strip()

if __name__ == '__main__': 
	print(spacy.getdoc("hello world"))

# docker run -d --restart=always --name es -p 9200:9200 -p 5601:5601 -v /data/dskes-9200:/home/elasticsearch/elasticsearch-7.15.1/data -e "discovery.type=single-node" nshou/elasticsearch-kibana
