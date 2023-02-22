https://github.com/anthcor/firestore-fastapi/tree/master/docs


Updating Fulfillment response parameters:
https://botflo.com/updating-dialogflow-cx-parameters-from-webhook/

https://stackoverflow.com/questions/64646879/dialogflow-cx-webhook-for-fulfilment-to-reply-user-using-nodejs
https://stackoverflow.com/questions/68838654/dialogflow-cx-transition-to-another-page-from-webhook
https://cloud.google.com/dialogflow/cx/docs/concept/fulfillment

https://developers.google.com/assistant/df-asdk/reference/dialogflow-webhook-json

https://fastapi.tiangolo.com/tutorial/first-steps/

uvicorn main:app --reload
./ngrok http 80


gcloud builds submit --tag gcr.io/ml-marcus-certification/health_bot_api

gcloud run deploy --image gcr.io/ml-marcus-certification/health_bot_api --platform managed

https://blog.somideolaoye.com/fastapi-deploy-containerized-apps-on-google-cloud-run

https://cloud.google.com/dialogflow/cx/docs/reference/rpc/google.cloud.dialogflow.cx.v3#webhookresponse

ce4ce796ff71b66303b792736bc239bd
EAANfVCUwBx0BACTsZBmW0HdlUvBNrM8ou8zc516RCqZCvrouCGXHXCcvajZBGKKyDYRADXZChwIh3oltZCl10UVimYPEOd2XxpxSFjdZB5GlNKvygtcp26fZBtYzcDbw9E3l0o88kLG2ShAyw0QWZAj4y43ZC4ZA1YjCDduO4VJD4kqJ8zCZB8yNCUZANUDBrLIh0DPOcD1H0OZA8aQZDZD
healthbot-dlsu-project-test-1

# https://github.com/anthcor/firestore-fastapi/tree/master/docs


Ako nga pala si Dr. Dhelia, ang iyong doktor na magtatanong sa iyong kalusugan ngayon.

"messaging_type": "RESPONSE",
  "message":

  {
    "text": " Ano ang pangalan mo?"
  }

  {
    "text": "Ilang taon ka na?",
  }

  {
    "text": "Ano kasarian mo lalake o babae?",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"Red",
        "payload":"<POSTBACK_PAYLOAD>"
      },{
        "content_type":"text",
        "title":"Green",
        "payload":"<POSTBACK_PAYLOAD>"
      }
    ]
  }
