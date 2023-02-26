class atividade(object):
	def __init__(self, nome, matéria, data1, data2, descrição):
		self.nome = nome
		self.matéria = matéria
		self.data = data1, data2
		self.descrição = descrição
	def detalhes(self):
		print(f'Nome: {self.nome}		Matéria: {self.matéria}\nPrazo: {self.data[0]} até {self.data[1]}\nDescrição:\n{self.descrição}\n')



def add():
	arq = open(file='dados.config', encoding='utf-8', mode='a')
	nome = input('Insira o nome da tarefa: ').replace(' ', '_')
	matéria = input('Insira a matéria referenta à tarefa: ').replace(' ', '_')
	data1 = input('Insira a data em que recebeu a tarefa: ').replace(' ', '_')
	data2 = input('Insira a data de entrega da tarefa: ').replace(' ', '_')
	descrição = input('Insira a descrição da tarefa: ').replace(' ', '_')
	add = f'{nome} {matéria} {data1} {data2} {descrição}\n'
	arq.write(add)
	print('Atividade adicionada!\n')
	arq.close()


def ver(num):
	global atividades
	arq = open(file='dados.config', encoding='utf-8', mode='r')	
	tarefa = atividades[num-1]
	x = -1
	for item in tarefa:
		x+=1
		tarefa[x] = item.replace('_', ' ')
	tema = atividade(tarefa[0], tarefa[1], tarefa[2], tarefa[3], tarefa[4])
	tema.detalhes()
	arq.close()


def lista():
	global atividades
	with open(file='dados.config', encoding='utf-8', mode='r') as arq:
		x = 0
		atividades = []
		for linha in arq:
			atividades.append(linha.replace('\n', '').split(' '))
		atividades.sort()
	print('	Atividades Pendentes:')
	for tarefa in atividades:
		x+=1
		y=-1
		for item in tarefa:
			y+=1
			tarefa[y] = item.replace('_', ' ')
		tema = atividade(tarefa[0], tarefa[1], tarefa[2], tarefa[3], tarefa[4])
		print(x, '-', tema.nome, tema.data[1] )
	arq.close()


def alterar(num):
	with open(file='dados.config', encoding='utf-8', mode='r') as arq:
		backup = arq.read()
	with open(file='dados.config', encoding='utf-8', mode='r') as arq:
		atividades = []
		for linha in arq:
			atividades.append(linha)
		atividades.sort()
	tarefa = atividades[num-1]
	backup = backup.replace(tarefa, '')
	arq = open(file='dados.config', encoding='utf-8', mode='w')
	arq.write(backup)
	arq.close()

try:
	teste = open(file='dados.config', encoding='utf-8', mode='r')
except FileNotFoundError:
	teste = open(file='dados.config', encoding='utf-8', mode='w')
finally:
	teste.close()

while True:
	inicio = input('	Opções:\n1 - Ver atividades\n2 - Adicionar uma nova atividade\n0 - Sair do Programa\n')
	if inicio == '1':
		while True:
			lista()
			print('0 - Voltar')
			op = input()
			try:
				int(op)
			except ValueError:
				print()
				print('Opção Inválida!\n')
			else:
				op = int(op)
				print()
				if op > 0 and op < len(atividades)+1:
					ver(op)
					while True:
						act = input('1 - Remover atividade\n0 - Voltar\n')						
						if act == '1':
							alterar(op)
							break
						elif act == '0':
							break
						else:
							print('Opção Inválida!\n')
							continue
				elif op == 0:
					break
				else:
					print('Opção Inválida!\n')
					continue

	elif inicio == '2':
		print()
		add()
		continue

	elif inicio == '0':
		break
	else:
		print('Opção Inválida!\n')
		continue
input('Fim do Programa!')