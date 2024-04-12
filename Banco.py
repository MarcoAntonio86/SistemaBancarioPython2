
import mysql.connector
 
class Banco:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='banco_tds0025'
        )
        self.cursor = self.conexao.cursor()
 
        self.usuarios = {}
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3
 
        self.criar_tabela_usuarios()
 
    def criar_tabela_usuarios(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                cpf VARCHAR(11) UNIQUE NOT NULL,
                senha VARCHAR(50) NOT NULL,
                Saldo DOUBLE
            )
            """)
            print("Tabela 'usuarios' criada com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao criar tabela: {err}")
 
    def login(self):
        cpf = input("Informe o CPF: ")
        senha = input("Informe a senha: ")
 
        query = "SELECT * FROM usuarios WHERE cpf = %s AND senha = %s"
        valores = (cpf, senha)
 
        self.cursor.execute(query, valores)
        usuario = self.cursor.fetchone()
 
        if usuario:
            self.usuarios = {'cpf': usuario[2]}
            self.saldo = usuario[4]
            print("Login realizado com sucesso!")
            return True
        else:
            print("CPF ou senha incorretos.")
            return False
 
    def exibir_menu(self):
        menu = ("""
        ########## Seja Bem Vindo(a) Banco TDS0025 ##########
 
                    $$$$$$$$$$ Menu $$$$$$$$$$
                   
        [1] Logar
        [2] Depositar
        [3] Sacar
        [4] Extrato
        [5] Cadastrar Usuário
        [6] Sair
       
        ################## Agradeço a preferência ##################
        """)
        return menu
 
    def exibir_menu_logado(self):
        menu = ("""
        ########## Seja Bem Vindo(a) Banco TDS0025 ##########
 
                    $$$$$$$$$$ Menu $$$$$$$$$$
                   
        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Cadastrar Usuário
        [5] Sair
       
        ################## Agradeço a preferência ##################
        """)
        return menu
 
    def cadastrar_usuario(self):
        nome = input("Informe o nome do usuário: ")
        cpf = input("Informe o CPF do usuário (apenas números): ")
        senha = input("Informe a senha do usuário: ")
        saldo = float(input("Informe o saldo inicial: "))
 
        query = "INSERT INTO usuarios (nome, cpf, senha, Saldo) VALUES (%s, %s, %s, %s)"
        valores = (nome, cpf, senha, saldo)
 
        try:
            self.cursor.execute(query, valores)
            self.conexao.commit()
            print("Usuário cadastrado com sucesso!")
            self.usuarios = {'cpf': cpf}
            self.saldo = saldo
            self.extrato += f"Saldo Inicial: R$ {saldo:.2f}\n"
        except mysql.connector.Error as err:
            print(f"Erro ao cadastrar usuário: {err}")
 
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito: R$ {valor:.2f}\n"
 
            query = "UPDATE usuarios SET Saldo = %s WHERE cpf = %s"
            valores = (self.saldo, self.usuarios.get('cpf'))
            try:
                self.cursor.execute(query, valores)
                self.conexao.commit()
            except mysql.connector.Error as err:
                print(f"Erro ao atualizar saldo do usuário: {err}")
 
    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.LIMITE_SAQUES
 
        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente, seu saldo é: ", self.saldo)
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excedeu o limite.\nSeu limite é: ", self.limite)
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.\nSeu limite de saque é: ", self.LIMITE_SAQUES)
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque: R$ {valor:.2f}\n"
            self.numero_saques += 1
 
            query = "UPDATE usuarios SET Saldo = %s WHERE cpf = %s"
            valores = (self.saldo, self.usuarios.get('cpf'))
            try:
                self.cursor.execute(query, valores)
                self.conexao.commit()
            except mysql.connector.Error as err:
                print(f"Erro ao atualizar saldo do usuário: {err}")
        else:
            print("Operação falhou! O valor informado é inválido.")
 
    def exibir_extrato(self):
        print("\n================= Extrato ==================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("============================================")
 
    def executar(self):
        while True:
            opcao = input(self.exibir_menu())
 
            if opcao == "1":
                if self.login():
                    while True:
                        opcao_logado = input(self.exibir_menu_logado())
                       
                        if opcao_logado == "1":
                            valor = float(input("Informe o valor do depósito: "))
                            self.depositar(valor)
 
                        elif opcao_logado == "2":
                            valor = float(input("Informe o valor do saque: "))
                            self.sacar(valor)
 
                        elif opcao_logado == "3":
                            self.exibir_extrato()
 
                        elif opcao_logado == "4":
                            self.cadastrar_usuario()
 
                        elif opcao_logado == "5":
                            print("\n                Banco TDS0025 Agradece pela Parceria")
                            print("\n      5################## Volte Sempre ################## \n")
                            break
 
                        else:
                            print("Operação inválida, por favor selecione novamente a operação desejada.")
                else:
                    print("Falha no login, tente novamente ou cadastre-se.")
 
            elif opcao == "2":
                valor = float(input("Informe o valor do depósito: "))
                self.depositar(valor)
 
            elif opcao == "3":
                valor = float(input("Informe o valor do saque: "))
                self.sacar(valor)
 
            elif opcao == "4":
                self.exibir_extrato()
 
            elif opcao == "5":
                self.cadastrar_usuario()
 
            elif opcao == "6":
                print("\n                Banco TDS0025 Agradece pela Parceria")
                print("\n      5################## Volte Sempre ################## \n")
                break
 
            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")
 
# Instanciando a classe e executando o programa
banco = Banco()
banco.executar()