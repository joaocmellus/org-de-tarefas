import PySimpleGUI as sg

#Classe atividade
class atividade(object):
	def __init__(self, nome, matéria, data1, data2, descrição, concluído):
		self.nome = nome
		self.matéria = matéria
		self.data = data1, data2
		self.descrição = descrição
		self.concluído = concluído

	#Método para criar uma nova atividade
	def Add(self):
		with open(file='dados.config', encoding='utf-8', mode='a') as arq:
			nome = self.nome.replace(' ', '_')
			matéria = self.matéria.replace(' ', '_')
			data1 = self.data[0].replace(' ', '_')
			data2 = self.data[1].replace(' ', '_')
			descrição = self.descrição.replace(' ', '_')
			add = f'{nome} {matéria} {data1} {data2} {descrição} {self.concluído}\n'
			arq.write(add)

	#Método que retorna o layout com os detalhes da atividade
	def Detalhes(self):
		x = 1 
		descrição = self.descrição.replace('\.n', '\n')		
		for i in descrição:
			if i == '\n':
				x+=1
		
		TData1 = len(self.data[0]) - 1
		TData2 = len(self.data[1])

		if self.data[0] == '':
			layout = [
				[sg.Text('Nome:', size = (8,0)), sg.Text(self.nome, size = (30,0))],
				[sg.Text('Matéria:', size = (8,0)), sg.Text(self.matéria, size = (30,0))],
				[sg.Text('Prazo:', size = (8,0)), sg.Text(self.data[1], size = (TData2,0))],
				[sg.Text('Descrição:', size = (8,0))],
				[sg.Text(descrição, size = (56,x))],
				[sg.Button('Excluir'), sg.Button('Voltar')]
			]
		else:
			layout = [
				[sg.Text('Nome:', size = (8,0)), sg.Text(self.nome, size = (30,0))],
				[sg.Text('Matéria:', size = (8,0)), sg.Text(self.matéria, size = (30,0))],
				[sg.Text('Prazo:', size = (8,0)), sg.Text(self.data[0], size = (TData1,0)),sg.Text('até', size = (2,0)), sg.Text(self.data[1], size = (TData2,0))],
				[sg.Text('Descrição:', size = (8,0))],
				[sg.Text(descrição, size = (56,x))],
				[sg.Button('Excluir'), sg.Button('Voltar')]
			]
		return layout

	def Alterar(self, num):
		if self.concluído == 'n':
			self.concluído = 's'
		else:
			self.concluído = 'n'

		Excluir(num)

		with open(file='dados.config', encoding='utf-8', mode='a') as arq:
			nome = self.nome.replace(' ', '_')
			matéria = self.matéria.replace(' ', '_')
			data1 = self.data[0].replace(' ', '_')
			data2 = self.data[1].replace(' ', '_')
			descrição = self.descrição.replace(' ', '_')
			add = f'{nome} {matéria} {data1} {data2} {descrição} {self.concluído}\n'
			arq.write(add)

def Alterar_Status(num):
	atividades = Ler_Arquivo()

	tarefa = atividades[num]
	
	tarefa = atividade(tarefa[0],tarefa[1],tarefa[2],tarefa[3],tarefa[4],tarefa[5])

	tarefa.Alterar(num)


#Abrir arquivo de texto para pegar informações
def Ler_Arquivo():
	with open(file='dados.config', encoding='utf-8', mode='r') as arq:
		atividades = []
		for linha in arq:
			atividades.append(linha.replace('\n', '').split(' '))
		atividades.sort()
		return atividades


#Criar tela inicial
def Tela_inicio():
	#Tema da Tela
	sg.theme('DarkGrey9')

	atividades = Ler_Arquivo()
	
	#Definir x, novo e maior = 0 para numerar as atividades e definir o tamanho da tela
	x = 0
	novo = 0
	maior = 0

	#Separar os elementos da string
	for tarefa in atividades:
		#Definir aumentar x para númerar e definir y para alterar o texto mais tarde
		y=-1

		#Retirar os "_" do texto
		for item in tarefa:
			y+=1
			tarefa[y] = item.replace('_', ' ')
		tarefa[4] = tarefa[4].replace('\.n', '\n')

		tema = atividade(tarefa[0], tarefa[1], tarefa[2], tarefa[3], tarefa[4], tarefa[5])
		
		#Verifica qual a atividade com o maior nome
		novo = len(tema.nome)
		if novo > maior:
			maior = novo


	#Criar lista do layout vazia
	layout = []

	#Colocar as atividades no layout
	for tarefa in atividades:
		x+=1
		tema = atividade(tarefa[0], tarefa[1], tarefa[2], tarefa[3], tarefa[4], tarefa[5])
		if tema.concluído == 'n':
			layout.append([sg.Checkbox(f'{x} - {tema.nome}', size = (maior+2, 0), key = (f'CB{x}'), enable_events = True, default = False), sg.Button('Detalhes', key=x)],)
		else:
			layout.append([sg.Checkbox(f'{x} - {tema.nome}', size = (maior+2, 0), key = (f'CB{x}'), enable_events = True, default = True), sg.Button('Detalhes', key=x)],)

	#Acrescentar os botões finais
	layout.append([sg.Button('Nova'), sg.Button('Sair')])

	#Retornar a janela a ser exibida
	return sg.Window("Lista de Atividades", layout = layout, finalize = True)


#Criar tela para adicionar nova atividade
def Tela_add():
	sg.theme('DarkGrey9')

	#Cria o layout da tela
	layout = [
			[sg.Text('Nome:', size = (8,0)), sg.Input(size = (45,0), key = 'nome')],
			[sg.Text('Matéria:', size = (8,0)), sg.Input(size = (45,0), key = 'matéria')],
			[sg.Text('Data:', size = (8,0)), sg.Input(size = (10,0), key = 'data1'),sg.Text('até', size = (2,0)), sg.Input(size = (10,0), key = 'data2')],
			[sg.Text('Descrição:', size = (8,0))],
			[sg.Multiline(font=('Arial', 10), text_color='white', size=(56, 5), key='descrição')],
			[sg.Button('Enviar'), sg.Button('Voltar')]
	]
	#Retornar a janela a ser exibida
	return sg.Window("Adicionar Nova Atividade", layout = layout, finalize = True)


def Tela_detalhes(num):
	sg.theme('DarkGrey9')
	atividades = Ler_Arquivo()
	x = 1
	tarefa = atividades[num-1]
	tarefa = atividade(tarefa[0],tarefa[1],tarefa[2],tarefa[3],tarefa[4],tarefa[5])
	layout = tarefa.Detalhes()

	return sg.Window("Detalhes da Atividade", layout = layout, finalize = True)


def Excluir(num):
	with open(file='dados.config', encoding='utf-8', mode='r') as arq:
		backup = arq.read()
	with open(file='dados.config', encoding='utf-8', mode='r') as arq:
		atividades = []
		for linha in arq:
			atividades.append(linha)
		atividades.sort()
	tarefa = atividades[num]
	backup = backup.replace(tarefa, '')
	with open(file='dados.config', encoding='utf-8', mode='w') as arq:
		arq.write(backup)
		arq.close()


try:
	teste = open(file='dados.config', encoding='utf-8', mode='r')
except FileNotFoundError:
	teste = open(file='dados.config', encoding='utf-8', mode='w')
finally:
	teste.close()

inicio, add, detalhes = Tela_inicio(), None, None


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
		detalhes = Tela_detalhes(op)

	elif window == inicio and event[0:2] == 'CB':
		Alterar_Status((int(event[2:])-1))

	#Comando para ir para a Tela ADD
	if window == inicio and event == 'Nova':
		inicio.hide()
		add = Tela_add()

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
		values['descrição'] = values['descrição'].replace('\n', '\.n')
		tarefa = atividade(values['nome'], values['matéria'], values['data1'], values['data2'], values['descrição'], 'n')
		tarefa.Add()
		inicio = Tela_inicio()
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
		Excluir(op-1)
		inicio = Tela_inicio()
		window.close()
		inicio.UnHide()