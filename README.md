HOW TO RUN IT?
1) Create a virtual environment using the command "conda create venv python==3.9 -y"
2) Activate the environment using the command "conda activate venv"
3) Create a ".env" file in the project root directory and add your API keys:                                                                                                                                                                    
   PINECONE_API_KEY="your pinecone api key"                                                                                                                                                                                                  
   OPENAI_API_KEY="your openai api key"
4) Install all the dependencies using the command "pip install -r requirements.txt"
5) To execute "storing_index.py" run the command "python storing_index.py"
6) To execute "helpdesk.py" run the command "streamlit run helpdesk.py"
