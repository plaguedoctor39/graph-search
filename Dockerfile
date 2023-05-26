FROM python:3.9

WORKDIR /home/user/
RUN mkdir -p data graph func
COPY graph/main.py ./graph/main.py
COPY graph/graph_structure.py ./graph/graph_structure.py
COPY graph/search.py ./graph/search.py
COPY func/Auxiliary_functions.py ./graph/func/Auxiliary_functions.py
COPY data/shipsData200.xlsx ./data/shipsData200.xlsx
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "graph/main.py"]


