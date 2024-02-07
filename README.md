Set up an virtual env and load requirements.txt


To start weaviate use the docker-compose in the weaviate directory
`docker-compose up` 

#Index Data
For reading the Confluence set:
`CONFLUENCE_JSESSION_ID=` 
in `.env` file. The JSESSION_ID shall be get from the Browser cookies after logging in. 
I tried to use the token, with no success.
In `.env` set values
```  
AZURE_KEY=
AZURE_ENDPOINT=
AZURE_VERSION=
AZURE_EMBEDDING_DEPLOYMENT=
```
to be able to connect the embeddings in azure.


Make sure the weaviate Database is empty.
Then:
``` 
set -o allexport; source .env; set +o allexport
cd reader
python ./reader.py
```
and wait.

#Run it
Weviate creates an index, you get it by:
`http://127.0.0.1:8081/v1/schema`
the index is named 'class'

Add the name to the value `WEAVIATE_INDEX=` in `.env` 
Set the LLM Deplyoment to use to the value `AZURE_LLM_DEPLOYMENT` in `.env``

Load it by `set -o allexport; source .env; set +o allexport` in the console.

Start the frontend (backend is started in background then):
```
cd chat
python ./frontend.py
```
Visit: http://127.0.0.1:7860/
Type a question, get a result, type another question, get an error ;-)

