import PySimpleGUI as sg
import dbm.dumb
import uuid
import json
import os

TEMA = 'LightBlue3'
ICON = 'icon.ico'

def salvar(dados: dict, _id = None) -> None:
	'Converte um dicionário em str e salva no banco de dados'
	with dbm.dumb.open('dados/dados', 'w')	as db:
		if _id == None:
			while True:
				_id = str(uuid.uuid1())[:5]
				if _id not in db:
					break
		dados['id'] = _id
		dados = json.dumps(dados)
		db[_id] = dados

def abrir() -> list:
	'Acessa o banco de dados e retorna uma lista com o conteúdo'
	lista_dados = []
	lista_temporaria = []
	with dbm.dumb.open('dados/dados', 'r')	as db:
		for i in db:
			lista_temporaria.append(db[i])
		lista_temporaria.sort()
		for i in lista_temporaria:
			lista_dados.append(json.loads(i))
	return lista_dados

def excluir(posição: int) -> None:
	'Exclui o id do banco de dados'
	lista_dados = abrir()
	atividade = lista_dados[posição]
	_id = atividade['id']
	with dbm.dumb.open('dados/dados', 'w') as db:
		del db[_id]
	backup = abrir()
	with open('dados/dados.dat', 'w') as arq:
		arq.write('')
	with dbm.dumb.open('dados/dados', 'w') as db:
		for i in backup:
			_id = i['id']
			db[_id] = json.dumps(i)

def alterar_status(op: int):
	'Altera o valor booleano do status'
	lista_dados = abrir()
	alterar = lista_dados[op]
	if alterar['status'] == False:
		alterar['status'] = True
	else:
		alterar['status'] = False
	salvar(alterar, alterar['id'])

#Criar tela inicial
def tela_inicio():
	'Retorna a janela da tela inicial'
	sg.theme(TEMA)
	atividades = abrir()
	#Verifica o tamanho do maior título
	maior = 0
	for i in atividades:
		novo = len(i['título'])
		if novo > maior:
			maior = novo
	if maior < 30:
		maior = 30
	#Criar layout
	layout = []
	if len(atividades) > 0:
		x = 0
		for i in atividades:
			x += 1
			if i['status'] == False:
				layout.append([sg.Checkbox(f'{x} - ' + i['título'], size = (maior+2, 0), key = (f'CB{x}'), enable_events = True, default = False), sg.Button('Detalhes', key=x)],)
			else:
				layout.append([sg.Checkbox(f'{x} - ' + i['título'], size = (maior+2, 0), key = (f'CB{x}'), enable_events = True, default = True), sg.Button('Detalhes', key=x)],)
	else:
		layout.append([sg.Text('', size = (30,3))])
	#Acrescentar os botões finais
	layout.append([sg.Button('Nova'), sg.Button('Sair')])
	#Retornar a janela a ser exibida
	return sg.Window("Lista de Atividades", layout = layout, finalize = True, icon = ICON)

#Criar tela para adicionar nova atividade
def tela_adicionar():
	sg.theme(TEMA)
	#Layout da tela
	layout = [
			[sg.Text('Nome:', size = (8,0)), sg.Input(size = (45,0), key = 'nome')],
			[sg.Text('Matéria:', size = (8,0)), sg.Input(size = (45,0), key = 'matéria')],
			[sg.Text('Data:', size = (8,0)), sg.Input(size = (10,0), key = 'data')],
			[sg.Text('Descrição:', size = (8,0))],
			[sg.Multiline(font=('Arial', 10), text_color='black', size=(56, 5), key='descrição')],
			[sg.Button('Enviar'), sg.Button('Voltar')]
	]
	#Retornar a janela a ser exibida
	return sg.Window("Adicionar Nova Atividade", layout = layout, finalize = True, icon = ICON)

def tela_detalhes(num):
	sg.theme(TEMA)
	atividades = abrir()
	tarefa = atividades[num-1]
	#Deifinir tamanho da string
	tamanho_descrição = tarefa['descrição'].count('\n')
	if tamanho_descrição == 0:
		tamanho_descrição = 1
	if tarefa['data'] == '':
		layout = [
			[sg.Text('Nome:', size = (8,0)), sg.Text(tarefa['título'], size = (30,0))],
			[sg.Text('Matéria:', size = (8,0)), sg.Text(tarefa['matéria'], size = (30,0))],
			[sg.Text('Descrição:', size = (8,0))],
			[sg.Text(tarefa['descrição'], size = (56,tamanho_descrição))],
			[sg.Button('Excluir'), sg.Button('Voltar')]
		]
	else:
		layout = [
			[sg.Text('Nome:', size = (8,0)), sg.Text(tarefa['título'], size = (30,0))],
			[sg.Text('Matéria:', size = (8,0)), sg.Text(tarefa['matéria'], size = (30,0))],
			[sg.Text('Prazo:', size = (8,0)), sg.Text(tarefa['data'], size = (len(tarefa['data']),0))],
			[sg.Text('Descrição:', size = (8,0))],
			[sg.Text(tarefa['descrição'], size = (56,tamanho_descrição))],
			[sg.Button('Excluir'), sg.Button('Voltar')]
		]
	return sg.Window("Detalhes da Atividade", layout = layout, finalize = True, icon = ICON)

def main():
	inicio, add, detalhes = tela_inicio(), None, None
	while True:
		#Lê todas as janelas, e seus respectivos eventos e valores
		window, event, values = sg.read_all_windows()
	#LISTA COM OS COMANDOS
	#Comandos para a primeira janela(INICIO)
		#Comando para fechar
		if window == inicio and event == sg.WIN_CLOSED:
			break
		if window == inicio and event == 'Sair':
			break
		#Comando para ir para a Tela Detalhes
		if window == inicio and type(event) == int:
			op = event
			inicio.hide()
			detalhes = tela_detalhes(op)
		elif window == inicio and event[0:2] == 'CB':
			alterar_status((int(event[2:])-1))
		#Comando para ir para a Tela ADD
		if window == inicio and event == 'Nova':
			inicio.hide()
			add = tela_adicionar()
	#Comandos para a tela ADD
		#Comando para fechar
		if window == add and event == sg.WIN_CLOSED:
			window.close()
			inicio.UnHide()
		if window == add and event == 'Voltar':
			window.close()
			inicio.UnHide()
		#adicionar Nova Tarefa
		if window == add and event == 'Enviar':
			atividade = {
				"título" 	:	values['nome'],
				"matéria" 	:	values['matéria'],
				"data"		:	values['data'],
				"descrição"	:	values['descrição'],
				"status"	:	False
			}
			salvar(atividade)
			inicio = tela_inicio()
			window.close()
			inicio.UnHide()
	#Comando para a tela Detalhes
		if window == detalhes and event == sg.WIN_CLOSED:
			window.close()
			inicio.UnHide()
		if window == detalhes and event == 'Voltar':
			window.close()
			inicio.UnHide()
		#comando excluir
		if window == detalhes and event == 'Excluir':
			excluir(op-1)
			inicio = tela_inicio()
			window.close()
			inicio.UnHide()

if __name__ == '__main__':
	if not os.path.exists('dados/dados.dat'):
		if not os.path.exists('dados'):
			os.mkdir('dados')
		with dbm.dumb.open('dados/dados', 'n') as db:
			pass
	main()