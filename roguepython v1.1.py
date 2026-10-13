#TO DO LIST:
    # função cls() para limpar a tela (usando os.system)
    # mudar a tela de alguma forma
    # inimigos
    # luta de fato
    # mais salas (talvez eu deixe isso pra dps que fizer a base toda do jogo
    # itens e inventário?
    # outras coisas de roguelike talvez?


import os

#-------------------------------------------CLASSES------------------------------------------

class Mapa:
    def __init__(self, y_e_x_ini: tuple, objetos: list[object], mapa: list[list[str]]):
        '''
        Executa ao instânciar a classe. A atribui os valores dados:
        X e Y inicial: Para quando o jogador entrar na sala ele poder ter posições iniciais
        advindas da conexão;
        Mapa: O mapa em si, construído por uma matriz com strings;
        Objetos: Objetos contídos no mapa, importante para o mapa saber onde desenhá-los.
        O método também cria um dicionário de conexões, importante para a troca de salas
        ser possível. Não colocamos valores nesse dicionário no momento de instância da
        classe, mas sim depois de todos os mapas serem críados para se evitar erros.
        
        '''
        self.y_ini, self.x_ini = y_e_x_ini
        self.mapa = mapa
        self.objetos = objetos

        self.conexoes = {
        'n': None,
        's': None,
        'l': None,
        'o': None,
                   }
        
    def desenha_mapa(self) -> None:
        '''
        Desenha o mapa na tela utilizando for aninhado. Também checa as localizações
        dos objetos do Mapa, os imprimindo nos locais apropriados.
        '''
        objs = False
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[i])):
                for obj in self.objetos:
                    if i == obj.y and j == obj.x:
                        print(obj.symbol, end='')
                        objs = True
                        
                if objs == True: objs = False
                else: print(self.mapa[i][j], end='')
                
            print()

    def valida_posicao(self, nova_pos: tuple) -> bool | str:
        '''
        Checa se a posição é válida para caminhar, caso tenha parede (#) retorna False,
        Caso veja uma string vázia (' '), retorna a mesma para efetuar a troca de tela.
        '''
        y, x = nova_pos
        if self.mapa[y][x] == '#':
            return False
        elif self.mapa[y][x] == ' ':
            return ' '      
        return True

    def posicao_ini_mapa(self, jogador: object, direcao: str) -> None:
        '''
        Muda a posição do jogador para encaixar com a origem do jogador no mapa, levando
        em consideração a direção na qual ele veio.
        '''
        if direcao in 'l' 'o':
            jogador.x = self.x_ini
        elif direcao in 'n' 's':
            jogador.y = self.y_ini



class Jogador:
    def __init__(self):
        '''
        Executa ao instânciar a classe. Não a atribui nenhum valor dado devido a só se ter
        um jogador a todo momento, então se pode simplesmente mudar os valores base da
        classe caso queira mudar os valores iniciais o jogador.
        '''
        self.symbol = '@'
        self.vidatotal = 100
        self.vidaatual = 100
        self.dano = 3
        self.lvl = 1
        self.y = 2
        self.x = 1

    def move(self, mapa: object, direcao: str) -> bool | object:    
        '''
        Responsável pelo movimento do jogador. puxa o método valida_posicao da classe Mapa
        para se certificar se é possível caminhar na direção escolhida pelo jogador, e
        caso seja, o trata de acordo com o retorno.
        '''                                                         
        nova_pos = converte_posicao(self, direcao)                  
        if nova_pos != None:                                        #MÉTODO MOVE RETORNA MAIS COISAS QUE DEVERIA
                                                                    #DIVIDIR RESPONSABILIDADES DE TROCA DE TELA
            valida = mapa.valida_posicao(nova_pos)
            if not valida: return False
            elif valida == ' ' : return mapa.conexoes[direcao]
            
            self.y, self.x = nova_pos
            return True

#-------------------------------------------FUNÇÕES------------------------------------------


def converte_posicao(objeto: object, direcao: str) -> tuple | bool:
    '''
    Converte a posição cardinal (abreviada para 'n', 's', 'l' ou 'o') para a lógica de
    movimento em matrizes.
    '''
    if direcao in ('n', 's', 'l', 'o'):
        y, x = objeto.y, objeto.x
        if direcao == 'n': nova_pos = (y-1, x)
        elif direcao == 's': nova_pos = (y+1, x)
        elif direcao == 'l': nova_pos = (y, x+1)
        elif direcao == 'o': nova_pos = (y, x-1)
        return nova_pos
    

#-------------------------------------------MAIN----------------------------------------------


def main():
    jogador = Jogador()
    mapa1 = Mapa((3, 10), [jogador],       [list("############"),
                                           list("#..........#"),
                                           list("#.......... "),
                                           list("#.......... "),
                                           list("#..........#"),
                                           list("############")])
    mapa2 = Mapa((3, 1), [jogador],       [list("############"),
                                           list("#..........#"),
                                           list(" ..........#"),
                                           list(" ..........#"),
                                           list("#..........#"),
                                           list("############")])

    #Conexões:
    mapa1.conexoes['l'] = mapa2
    mapa2.conexoes['o'] = mapa1
    
    mapa_atual = mapa1
    warn = ''
    while True:
        os.system('cls')
        mapa_atual.desenha_mapa()
        print(warn)
        warn = ''
        acao = input(f"Vida:{jogador.vidaatual}/{jogador.vidatotal} O que deseja fazer? ")

        movimento = jogador.move(mapa_atual, acao)
        if not movimento:
            warn = "Você não pode fazer isso!"
        
        if isinstance(movimento, Mapa):
            mapa_atual = movimento
            mapa_atual.posicao_ini_mapa(jogador, acao)
            warn = "Você passa de sala..."
            


if __name__ == '__main__':
    main()
