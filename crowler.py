import bs4, sys, json
import urllib2

#input data

def clean_strings(st):
	return st
	if len(st)==0:
		return None
	else:
		st=st.replace(" ","")
		st=st.replace("\n","")
		return st


url = raw_input("target url : ")
if not('http' in url ):
	print "missing protocol name http/https"
	sys.exit()
numb_items = int(input("number of items : "))#stand for img,title,price.. of product
items = {}


for i in range(numb_items):
	name = raw_input("name of obejct : ")
	_tag = raw_input('tag of item : ') #price
	identifiere = raw_input('identifiere target : ') #class == 'price'
	value_ide = raw_input('identifiere value: ') #class == 'price'
	take_value = filter(None,raw_input('take these values: ').split(' ')) # input form: src alt
	items[name] = [_tag,identifiere,value_ide,take_value]

#get the page
header = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'




try:
	print "[*] getting webpage"	
	opener = urllib2.build_opener()
	opener.addheaders = [('User-Agent', header)]
	page = opener.open(url).read()
except Exception as e:
	print e
	sys.exit()

print "[*] Fetching webpage"
f_list = {}
#parse the data
bspage = bs4.BeautifulSoup(page,'html5lib')
for j in items.keys():
	_tag, identifiere, value_ide ,take_value = items[j]
	tmp = []
	for i in bspage.find_all(_tag,{identifiere:value_ide}):
		m_tmp = []
		for v in take_value:
			if v==".text":
				m_tmp.append(clean_strings(i.text.encode('ascii', errors='ignore')))
			elif ".option" in v:
				sp = v[7:].split('(')[1][:-1].split("=")
				d_tmp = []
				for d in sp[1].split('&'):
					exec "d_tmp.append(i.%s.get('%s'))"%(sp[0],d)
				m_tmp.append(d_tmp)
			else:
				m_tmp.append(i.get(v))
		tmp.append(m_tmp)
	f_list[j]=tmp


#test whether the lists is equal
if len(set(map(len,f_list.values()))) >1 :
	print "inequal number of list please check the results"
	f_list['errors'] = 1
else:
	print "perfect match "
	print "generating perfect json ..."
	a ={ }
	print f_list.values()
	for i in range(len(f_list.values()[0])):
		li= []
		for j in f_list.keys():
			li.append(f_list[j][i])
		a[i] = li
	f_list = a
	del a
	f_list['errors'] = 0

print "proceding to json"

f=open(url.split('/')[2]+'.json',"wb+")
f.writelines(json.dumps(f_list))
f.close()


print "done."




#


