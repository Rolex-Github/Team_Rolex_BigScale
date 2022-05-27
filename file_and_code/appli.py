from flask import Flask,render_template,flash, request, url_for
from google.cloud import automl
from google.api_core.client_options import ClientOptions
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/teiffouet/component-access-key.json"

# TODO(developer): set the following variables
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        # getting input with name = targetfrase in HTML form
        text = request.form.get("targetfrase")
        project_id = "rising-dominion-348717"
        model_id = "TCN6916178827362172928"
        content = text
        print(content)

        options = ClientOptions(api_endpoint='eu-automl.googleapis.com')
        prediction_client = automl.PredictionServiceClient.from_service_account_json("rising-dominion-348717-eab6ba6d4f22.json", client_options=options)


        # Get the full path of the model.
        model_full_id = automl.AutoMlClient.model_path(project_id,'eu',model_id)

        text_snippet = automl.TextSnippet(content=content,mime_type='text/')
        payload = automl.ExamplePayload(text_snippet=text_snippet)

        response = prediction_client.predict(name=model_full_id, payload=payload)
       
       #return response.payload
        for annotation_payload in response.payload:
            print(u"Predicted class name: {}".format(annotation_payload.display_name))
            print(
                u"Predicted class score: {}".format(annotation_payload.classification.score)
            )
        return render_template("result.html", data=response.payload, result=text)
    if request.method == 'GET':
        return "<h3> nothing to show </h3>"

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)

#if __name__ == '__main__':
#   app.run(host="127.0.0.1", port=8080, debug = True)