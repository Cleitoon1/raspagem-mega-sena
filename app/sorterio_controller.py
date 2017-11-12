import json
import requests
from bottle import template, static_file
from sqlalchemy import create_engine, desc
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from app import engine, app, create_session
from app.sorteio import Sorteio

engine = create_engine('sqlite:///megasena.db', echo=True)
create_session = sessionmaker(bind=engine)

# arquivos estaticos
@app.get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='app/static/css')


@app.get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='app/static/js')


@app.get('/<filename:re:.*\.json>')
def jsons(filename):
    return static_file(filename, root='app/static/js')


@app.get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='app/static/img')


@app.get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='app/static/fonts')


def buscar_sorteios_api(todos=True, numero=0):
    url, lst_sorteios = 'https://www.lotodicas.com.br/api/mega-sena/', []
    if todos:
        ultimo_sorterio = json.loads(requests.get(url).text)
        lst_sorteios.append(Sorteio(**ultimo_sorterio))
        for i in range(1, int(ultimo_sorterio["numero"])):
            lst_sorteios.append(Sorteio(**json.loads(requests.get(url + str(i)).text)))
        return lst_sorteios
    return Sorteio(**json.loads(requests.get(url + str(numero)).text)) if numero > 0 else Sorteio(**json.loads(requests.get(url).text))

def criar_session():
    return create_session()


def adicionar_todos_sorterios():
    session = criar_session()
    session.bulk_save_objects(buscar_sorteios_api())
    session.commit()


def dados_ganhadores():
    session = create_session()
    retorno = [x._asdict() for x in session.query(func.sum(Sorteio.valor_mega).label("total_mega"),
        func.sum(Sorteio.valor_quina).label("total_quina"), func.sum(Sorteio.valor_quadra).label("total_quadra"),
        func.sum(Sorteio.ganhadores_mega).label("ganhadores_mega"), func.sum(Sorteio.ganhadores_quina).label("ganhadores_quina"),
        func.sum(Sorteio.ganhadores_quadra).label("ganhadores_quadra"))][0]
    return [{"jogo": "Mega", "ganhadores": retorno["ganhadores_mega"], "valor": retorno["total_mega"]},
            {"jogo": "Quina", "ganhadores": retorno["ganhadores_quina"], "valor": retorno["total_quina"]},
            {"jogo": "Quadra", "ganhadores": retorno["ganhadores_quadra"], "valor": retorno["total_quadra"]}]

def sorteios_acumulados():
    retorno = [x._asdict() for x in create_session().query(Sorteio.acumulado.label("acumulado"),
                    func.count(Sorteio.acumulado).label("quantidade")).group_by(Sorteio.acumulado).all()]
    for i, x in enumerate(retorno):
        if x["acumulado"] == True:
            retorno[i]["acumulado"] = "sim"
        else:
            retorno[i]["acumulado"] = "não"
    return retorno

def numero_mais_saidos():
    lst_sequencias, lst_numeros = [x.lst_numeros for x in create_session().query(Sorteio).all()], []
    for n in lst_sequencias:
        for x in n:
            num = int(x)
            if any(d['numero'] == num for d in lst_numeros):
                for index, item in enumerate(lst_numeros):
                    if item["numero"] == num:
                        lst_numeros[index]["quantidade"] = lst_numeros[index]["quantidade"] + 1
            else:
                lst_numeros.append({"numero": num, "quantidade": 1})
    return sorted(lst_numeros, key=lambda k: k["quantidade"], reverse=True)[:6]

def numero_menos_saidos():
    lst_sequencias, lst_numeros = [x.lst_numeros for x in create_session().query(Sorteio).all()], []
    for n in lst_sequencias:
        for x in n:
            num = int(x)
            if any(d['numero'] == num for d in lst_numeros):
                for index, item in enumerate(lst_numeros):
                    if item["numero"] == num:
                        lst_numeros[index]["quantidade"] = lst_numeros[index]["quantidade"] + 1
            else:
                lst_numeros.append({"numero": num, "quantidade": 1})
    return sorted(lst_numeros, key=lambda k: k["quantidade"])[:6]

def maiores_premios():
    return [x._asdict() for x in create_session().query(Sorteio.id.label("numero"), Sorteio.valor_mega.label("valor"),
                        Sorteio.data).filter(Sorteio.acumulado == False).order_by(desc(Sorteio.valor_mega)).limit(6)]

@app.get("/")
def index():
    return template('index.html', dezenas_mais=numero_mais_saidos(), dezenas_menos=numero_menos_saidos(),
            dados_premios=dados_ganhadores(), premios=maiores_premios(), acumulados= sorteios_acumulados())