'''
conda install -c conda-forge spacy
python -m spacy download en_core_web_sm

pip install jsonlines
pip install parsedatetime
pip install ipython
pip install pandas
'''


import jsonlines

#from tqdm.autonotebook import tqdm
import jsonlines
import re

import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")

from datetime import datetime
import parsedatetime as pdt # $ pip install parsedatetime

def get_date(date_list, current_date):
  cal = pdt.Calendar()
  now = current_date
  ans = []
  #print("now: %s" % now)
  for time_string in date_list:
    x = cal.parseDT(time_string, now)[0]
    #print("%s:\t%s" % (time_string, x))
    ans.append(x.strftime("%d/%m/%Y"))
  
  return get_start_end_date(ans, current_date)

def get_start_end_date(date_list, current_date):
  if(len(date_list) == 0):
    return (current_date.strftime("%d/%m/%Y"), current_date.strftime("%d/%m/%Y"))
  elif(len(date_list) == 1):
    return (date_list[0], date_list[0])
  else:
    listt = []
    for l in date_list:
      listt.append(datetime.strptime(l, '%d/%m/%Y').date())
    x = min(listt)
    y = max(listt)
    return (x.strftime("%d/%m/%Y"), y.strftime("%d/%m/%Y"))

import re
for i in range(313,321):
  with jsonlines.open("cleaned_masdar - Copy (2).jsonl", "r") as f:
    articles2 = list(f.iter())
  articles2 = articles2[i]
  doc2 = nlp(articles2['body'])
  displacy.render(doc2, style='ent', jupyter=True)
  pattern = r"(\d{%d})"%7
  print("Product ID: ", end=" ")
  print(re.findall(pattern, str(doc2)))
  date_list = []
  for ent in filter(lambda e : e.label_ == 'DATE', doc2.ents):
    date_list.append(ent.text)
  start_date, end_date = get_date(date_list,datetime(2022,7,28))
  print("Start Date: ", start_date)
  print("End Date: ", end_date)
  print("Description: ", end=" ")
  for e in doc2.ents:
    print(e, end=" ")
  print("\n******************************************************************************************************************************")