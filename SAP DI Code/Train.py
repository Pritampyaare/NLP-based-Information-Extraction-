# Example Python script to perform training on input data & generate Metrics & Model Blob
def on_input(data):
    
    import spacy
    
    nlp = spacy.load("en_core_web_sm")
    
    # to send metrics to the Submit Metrics operator, create a Python dictionary of key-value pairs
    metrics_dict = {"kpi1": "1"}
    
    # send the metrics to the output port - Submit Metrics operator will use this to persist the metrics 
    api.send("metrics", api.Message(metrics_dict))

    # create & send the model blob to the output port - Artifact Producer operator will use this to persist the model and create an artifact ID
    import pickle
    model_bob = pickle.dumps(nlp)
    model_blob = bytes("example", 'utf-8')
    api.send("modelBlob", model_blob)
    
api.set_port_callback("input", on_input)

