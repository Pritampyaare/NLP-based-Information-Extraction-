import json
import spacy
import re
import pickle
import datetime
from datetime import datetime
import parsedatetime as pdt
# Global vars to keep track of model status
model = None
model_ready = False

# Validate input data is JSON
def is_json(data):
  try:
    json_object = json.loads(data)
  except ValueError as e:
    return False
  return True

# When Model Blob reaches the input port
def on_model(model_blob):
    global model
    global model_ready

    import pickle
    #model = pickle.loads(model_blob)
    model = spacy.load("en_core_web_sm")
    model_ready = True
    api.logger.info("Model Received & Ready")



def get_date(date_list, current_date):
  from datetime import datetime
  import parsedatetime as pdt
  cal = pdt.Calendar()
  now = current_date
  ans = []
  #print("now: %s" % now)
  for time_string in date_list:
    if(time_string.find('to') != -1):
        a,b = time_string.split('to')
        a = cal.parseDT(a,now)[0]
        b = cal.parseDT(b,now)[0]
        return (a.strftime("%d/%m/%Y"),b.strftime("%d/%m/%Y"))
                           
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

# Client POST request received
def on_input(msg):
    error_message = ""
    success = False
    prediction = None # This line needs to be added
    final_result = []
    try:
        api.logger.info("POST request received from Client - checking if model is ready")
        if model_ready:
            api.logger.info("Model Ready")
            api.logger.info("Received data from client - validating json input")
            
            user_data = msg.body.decode('utf-8')
            # Received message from client, verify json data is valid
            if is_json(user_data):
                api.logger.info("Received valid json data from client - ready to use")
                
                # apply your model
                # obtain your results
                #text = json.loads(user_data)['email']
                text = '''
Dear all, 

 

New week, new prizes: yesterday we had the joy of learning that Henriette Michaud had received the Prix de l'Essai 2022 from the Académie Française for Freud in Bloomsbury 3123559: https://www.academie-francaise.fr/sites/academie-francaise.fr/files/palmares_2022_vf.pdf

 

Tomorrow, Hélène Carrère d'Encausse will receive an honorary prize for her work at the Hossegor book fair (Alexandra Kollontaï large format: 7757456 and plural to be published in November: 6912274).

 

Other good news that we are delighted about:

Next week marks the start of Aurélie Valognes and Virginie Grimaldi's summer promotion:
La Ritournelle 4551395 will be on RTL from next Monday until 10 July and then on France Bleu for the biggest summer run from Thursday 28 July to Wednesday 3 August.
Il nous restera ça 4702273 will accompany holidaymakers during RTL's most popular hours from Thursday 28 July to Sunday 31 July and then from Friday 12 August to Monday 15 August.
 

Cardinal Robert Sarah (Catechism of the Spiritual Life 2504824) is in the spotlight this weekend in Le Figaro Magazine with a major four-page interview (enclosed). Next week, he will receive exceptional media visibility.
 

Challenges published this week a portrait of Nicolas Forissier for L'ennemi intérieur 6180412 (en pj).
 

Sarah Briand's novel, Les pépins de Grenade 1282225, is receiving good media coverage. Femme Actuelle gave it a special mention this week (en pj), while Anne-Marie Revol praised the novel in Patricia Loison's 23H last night: https://www.francetvinfo.fr/replay-jt/franceinfo/21h-minuit/23-heures/jt-le-23h-jeudi-30-juin-2022_5230810.html
 

Janine Boissard's new novel, Quand la belle se réveillera 4082000, continues to be honoured, as shown by the fine reviews in the newspaper Centre presse (en pj) and Bruxelle culture (en pj).
 

And all the press review of the week in attachments!

 

Have a good weekend,

Sincerely yours,

Pauline

'''
                nlp = model
                ###########################################
                import re
                pattern = pattern = r"(\d{%d})"%7
                email = []
                for s in text.split('\n'):
                    if(re.findall(pattern, s)):
                        email.append(s)
                        #print(s,"***")
                #print(len(email))
                
                import re
                final_struct_list = []
                for s in email:
                  struct_list = []
                  doc2 = nlp(s)
                  #displacy.render(doc2, style='ent', jupyter=True)
                  pattern = r"(\d{%d})"%7
                  #print("Product ID: ", end=" ")
                  prod_id = re.findall(pattern, str(doc2))
                  struct_list.append(prod_id)
                  #print(prod_id)
                  date_list = []
                  for ent in filter(lambda e : e.label_ == 'DATE', doc2.ents):
                    date_list.append(ent.text)
                  start_date, end_date = get_date(date_list,datetime(2022,7,28))
                  struct_list.append(start_date)
                  #print("Start Date: ", start_date)
                  struct_list.append(end_date)
                  #print("End Date: ", end_date)
                  #print("Description: ", end=" ")
                  temp_str = ""
                  for e in doc2.ents:
                    temp_str = temp_str + str(e)+" "
                  struct_list.append(temp_str)
                  #print(temp_str)
                  final_struct_list.append(struct_list)
                  #print("\n*****************************")
                #print(final_struct_list)
                final_result = final_struct_list
                ###############################################
                success = True
            else:
                api.logger.info("Invalid JSON received from client - cannot apply model.")
                error_message = "Invalid JSON provided in request: " + user_data
                success = False
        else:
            api.logger.info("Model has not yet reached the input port - try again.")
            error_message = "Model has not yet reached the input port - try again."
            success = False
    except Exception as e:
        api.logger.error(e)
        error_message = "An error occurred: " + str(e)
    
    if success:
        # apply carried out successfully, send a response to the user
        
        msg.body = json.dumps({'marathon_minutes_prediction': final_result})
    else:
        msg.body = json.dumps({'Error': error_message})
    
    new_attributes = {'message.request.id': msg.attributes['message.request.id']}
    msg.attributes =  new_attributes
    api.send('output', msg)
    
api.set_port_callback("model", on_model)
api.set_port_callback("input", on_input)
