import numpy as np

# Ações
mover_missionario_esq_barco = {'numero': 0, 'ação': np.asarray([[-1, 0, +1],
                                                                [0, 0, 0]]), 'str': 'Move missionarário da esquerda para o barco'}
mover_missionario_dir_barco = {'numero': 1, 'ação': np.asarray([[0, -1, +1],
                                                                [0, 0, 0]]), 'str': 'Move missionário da direita para o barco'}
mover_missionario_para_direita = {'numero': 2, 'ação': np.asarray([[0, +1, -1],
                                                                    [0, 0, 0]]), 'str': 'Move missionário do barco para direita'}
mover_missionario_para_esquerda = {'numero': 3, 'ação': np.asarray([[+1, 0, -1],
                                                                    [0, 0, 0]]), 'str': 'Move missionário do barco para esquerda'}

mover_canibal_esq_barco = {'numero': 4, 'ação': np.asarray([[0, 0, 0],
                                                            [-1, 0, +1]]), 'str': 'Move canibal da esquerda para o barco'}
mover_canibal_dir_barco = {'numero': 5, 'ação': np.asarray([[0, 0, 0],
                                                            [0, -1, +1]]), 'str': 'Move canibal da direita para o barco'}
mover_canibal_para_direita = {'numero': 6, 'ação': np.asarray([[0, 0, 0],
                                                                [0, +1, -1]]), 'str': 'Move canibal do barco para esquerda'}
mover_canibal_para_esquerda = {'numero': 7, 'ação': np.asarray([[0, 0, 0],
                                                                [+1, 0,-1]]), 'str': 'Move canibal do barco para esquerda'}

mover_barco = {'numero': 8, 'ação': np.asarray([[0, 0, 0],
                                                [0, 0, 0]]), 'str': 'Move barco'}
class State:
    def __init__(self, estado, barco, pai, acao, profundidade):
        """
        Define o estado do problema, onde, no construtor, 'estado' é uma matriz 3x2 que mostra a quantidade de missionários e canibais nas margens esquerda, direita e no barco, 'barco' mostra o lado em que o mesmo se encontra, 'pai' é o nó pai referente àquele estado, 'acao' é o string referente à ação daquele estado e 'profundidade' representa a profundidade do estado em relação à árvore dos estados.
        """
        self.estado = estado
        self.barco = barco # right or left
        self.pai = pai
        self.acao = acao
        self.profundidade = profundidade

    def valid_state(self, action):
        """
        Verifica a validade do estado depois de sofrer alguma alteração com as ações realizadas.

        1- Verifica se nas margens há menos de 0 canibais ou missionários;

        2- Verifica se nas margens há mais de 3 canibais ou missionários;

        3- Verifica se em alguma margem há menos missionários do que canibais;

        4- Verifica se no barco há mais de 2 indivíduos ao mesmo tempo;

        5- Verifica se no barco há menos de 0 indivíduos;

        6- Verifica se no barco há indivíduos para realizar a ação 'mover_barco';

        7 e 8- Verifica a posição do barco para realizar as ações de adicionar ou remover missionários ou canibais do barco, visto que não é possível, por exemplo, que o barco esteja na esquerda e a ação seja adicionar um missionário da direita no barco.
        """
        if self.estado[0,0] < 0 or self.estado[0,1] < 0 or self.estado[1,0] < 0 or self.estado[1,1] < 0:
            return False
        
        if self.estado[0,0] > 3 or self.estado[0,1] > 3 or self.estado[1,0] > 3 or self.estado[1,1] > 3:
            return False
        
        if (self.estado[0,1] < self.estado[1,1] and self.estado[0,1] > 0) or (self.estado[0,0] < self.estado[1,0] and self.estado[0,0] > 0):
            return False
        
        if(self.estado[0,2] + self.estado[1,2]) > 2:
            return False
        
        if(self.estado[0,2] < 0 or self.estado[1,2] < 0):
            return False
        
        if ((action['numero'] is mover_barco['numero']) and (self.estado[0,2] == 0) and (self.estado[1,2] == 0)):
            return False
        
        if (((self.barco == 'left') and (action['numero'] == mover_canibal_dir_barco['numero'])) or ((self.barco == 'left') and (action['numero'] == mover_missionario_dir_barco['numero'])) or ((self.barco == 'left') and (action['numero'] == mover_canibal_para_direita['numero'])) or ((self.barco == 'left') and (action['numero'] == mover_missionario_para_direita['numero']))):
            return False
        
        if (((self.barco == 'right') and (action['numero'] == mover_canibal_esq_barco['numero'])) or ((self.barco == 'right') and (action['numero'] == mover_missionario_esq_barco['numero'])) or ((self.barco == 'right') and (action['numero'] == mover_canibal_para_esquerda['numero'])) or ((self.barco == 'right') and (action['numero'] == mover_missionario_para_esquerda['numero']))):
            return False
        
        return True
    
    def mostrar_estado(self):
        """
        Serve para mostrar o estado e sua respectiva profundidade dentro da árvore
        """
        print(self.estado)
        print('Profundidade: ', self.profundidade)
        print('\n============================\n')


    def do_action(self, action):
        """
        Serve para realizar a ação em determinado estado e retorna um novo estado caso ele seja válido
        """
        if ((action['numero'] == mover_barco['numero']) and (self.barco == 'left')):
            novo_estado = State(self.estado + action['ação'], 'right', self, action['str'], self.profundidade + 1)
        elif ((action['numero'] == mover_barco['numero']) and (self.barco =='right')):
            novo_estado = State(self.estado + action['ação'], 'left', self, action['str'], self.profundidade + 1)
        else:
            novo_estado = State(self.estado + action['ação'], self.barco, self, action['str'], self.profundidade + 1)

        if novo_estado.valid_state(action) is True:
            return novo_estado
        return None
    
    def verifica_solucao(self):
        """
        Serve para verificar se o estado é a solução esperada, retornando True caso seja.
        """
        if (self.estado[0,0] == 3 and self.estado[1,0] == 3 and self.estado[0,1] == 0 and self.estado[1,1] == 0 and self.estado[0,2] == 0 and self.estado[1,2] == 0):
            return True
        return False
    
    def to_hash(self):
        """
        Transforma o estado em um hash para evitar que estados já visto sejam visitados novamente
        """
        str_lista = str(np.reshape(self.estado, (1, 6))[0].tolist())
        str_lista += '{}'.format(self.barco)
        return hash(str_lista,)

class busca_em_profundidade():
    """
    Busca em profundidade
    """
    def __init__(self):
        self.lista_estados = []
        self.estados_visitados = []
        self.acoes = [mover_barco, mover_missionario_dir_barco, mover_missionario_esq_barco, mover_missionario_para_direita, mover_missionario_para_esquerda, mover_canibal_dir_barco, mover_canibal_esq_barco, mover_canibal_para_direita, mover_canibal_para_esquerda]

    def encontrar_solucao(self, estado_inicial: State) -> State:
        """
        Encontra a solução do problema
        """
        self.lista_estados.append(estado_inicial)
        solucao_encontrada = False
        solucao = None

        while len(self.lista_estados) > 0 and not solucao_encontrada:
            estado_atual = self.lista_estados.pop(0)
            self.estados_visitados.append(estado_atual.to_hash())
            if estado_atual.verifica_solucao():
                solucao_encontrada = True
                solucao = estado_atual
            else:
                # lista_comandos = ['Começo']
                for action in self.acoes:
                    novo_estado = estado_atual.do_action(action)
                    # lista_comandos.append(action['numero'])
                    if novo_estado is not None:
                        if not self.estados_visitados.__contains__(novo_estado.to_hash()):
                            self.lista_estados.insert(0, novo_estado)
        print('Estados visitados: ', len(self.estados_visitados))
        return solucao
    

if __name__ == "__main__":
    bfs = busca_em_profundidade()
    initial_state = State(np.asarray([[0, 3, 0],
                                        [0, 3, 0]]), 'right', None, 'Começo', 1)
    solucao= bfs.encontrar_solucao(initial_state)
    if solucao is not None:
        print("Solução Encontrada!")
        estado_atual = solucao
        solucao_completa = []
        somador = 0

        while estado_atual is not None:
            solucao_completa.append(estado_atual)
            estado_atual = estado_atual.pai
        for solucao in solucao_completa[-1::-1]:
            print(solucao.acao)
            somador += 1
            solucao.mostrar_estado()
        print("Fim")
