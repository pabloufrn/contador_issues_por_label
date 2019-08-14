import csv
import requests
import urllib.parse
import requests_cache
from collections import Counter

def list_issues(repo, token):
	issues = []
	stop = False
	page = 1
	while not stop:
		per_page = 100
		params = {
			'state': 'all',
			'page': page,
			'per_page': per_page,
			'access_token': token
		}
		url = 	'https://api.github.com/repos/{}/issues?'.format(repo)+\
				urllib.parse.urlencode(params)
		print(("[/*] requisitando issues:"+\
	    	"\n\trepo: {}\n\turl:{}").format(repo, url)+"\n[*/]")
		request = requests.get(url)
		if request.ok:
			conteudo = request.json()
			number_rows = len(conteudo)
			if(number_rows < per_page):
				stop = True
			if(number_rows > 0):
				for issue in conteudo:
					keys = ('id', 'title','user','html_url','pull_request','url','labels')
					props = {k:issue[k] for k in keys if k in issue}
					issues.append(props)
			else:
				stop = True
		else:
			print("[#] Erro na requisição.")
			return []
		page+=1
	return issues
	
def write(filename, issues):
	counter_issues = Counter()
	counter_pulls = Counter()
	counter_total = Counter()
	for issue in issues:
		for label in issue['labels']:
			counter_total[label['name']] += 1
			if('pull_request' in issue):
				counter_pulls[label['name']] += 1
			else:
				counter_issues[label['name']] += 1
	total_pairs = sorted(counter_total.items(), key=lambda item: item[1], reverse=True)
	with open(filename, mode='w+') as csv_file:
	    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	    csv_writer.writerow(['label','issues','pulls','total'])
	    for key, value in total_pairs:
        	csv_writer.writerow([key, counter_issues[key], counter_pulls[key], value])

def write_label_set(filename, issues):
	counter_issues = Counter()
	counter_pulls = Counter()
	counter_total = Counter()
	for issue in issues:
		labels = "|".join(label['name'] for label in issue['labels']) if len(issue['labels']) != 0 else "no label"
		counter_total[labels] += 1
		if('pull_request' in issue):
			counter_pulls[labels] += 1
		else:
			counter_issues[labels] += 1
	total_pairs = sorted(counter_total.items(), key=lambda item: item[1], reverse=True)
	with open(filename, mode='w+') as csv_file:
	    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	    csv_writer.writerow(['labels','issues','pulls','total'])
	    for key, value in total_pairs:
        	csv_writer.writerow([key, counter_issues[key], counter_pulls[key], value]) 

def show_label_list_count(file_prefix, issues, labelSet):
	counter_issues = 0 
	counter_pulls = 0
	with open(file_prefix + '_issues.txt', mode='w+') as issues_file, \
		 open(file_prefix + '_pulls.txt', mode='w+') as pulls_file:
		for issue in issues:
			for label in issue['labels']:
				if(label['name'] in labelSet):
					if('pull_request' in issue):
						counter_pulls += 1
						pulls_file.write(issue['html_url'] + '\n')
					else:
						counter_issues += 1
						issues_file.write(issue['html_url'] + '\n')
					break
	print("A contagem de issues com essas label é {}. As issues estão listadas no arquivo {}.".
		format(counter_issues, file_prefix + '_issues.txt'))
	print("A contagem de pulls request com essas label é {}. As issues estão listadas no arquivo {}.".
		format(counter_pulls, file_prefix + '_pulls.txt'))
	  
def get_label_set(filename):
	labelSet = set()
	with open(filename, mode='r') as txt_file:
		lines = txt_file.read().splitlines()
		for line in lines:
			labelSet.add(line)
	return labelSet


if __name__ == '__main__':
	requests_cache.install_cache('main_cache', expire_after=None)
	issues_kibana = list_issues('elastic/kibana', '1770a8c910e38146ecdef22039ad8f1155223cb9')
	issues_cas = list_issues('apereo/cas', '1770a8c910e38146ecdef22039ad8f1155223cb9')
	# write_label_set('kibana.csv', issues_kibana)
	# write_label_set('cas.csv', issues_cas)
	# write_label_set('kibana_label_set.csv', issues_kibana)
	# write_label_set('cas_label_set.csv', issues_cass)
	show_label_list_count('kibana', issues_kibana, get_label_set('labels_kibana.txt'))
	show_label_list_count('cas', issues_cas, get_label_set('labels_cas.txt'))

	
