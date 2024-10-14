# basic.py
# Autor: Víctor Barreto
# Data: 2023-10-13
# Descrição: Este arquivo contém a implementação da classe Lexer.

from contants import DIGITOS
from errors import ErroCaractereIlegal, ErroComentarioNaoFechado

# Tokens
TOKEN_COMMA = 'COMMA' 
TOKEN_INT = 'INT'
TOKEN_FLOAT = 'FLOAT'
TOKEN_PLUS = 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_MULTIPLY = 'MULTIPLY'
TOKEN_DIVIDE = 'DIVIDE'
TOKEN_LEFT_PAREN = 'LEFT_PAREN'
TOKEN_RIGHT_PAREN = 'RIGHT_PAREN'
TOKEN_IDENTIFIER = 'IDENTIFIER'
TOKEN_KEYWORD = 'KEYWORD'
TOKEN_ASSIGN = 'ASSIGN'
TOKEN_SEMICOLON = 'SEMICOLON'
TOKEN_COLON = 'COLON'
TOKEN_PERIOD = 'PERIOD'

# Operadores relacionais
TOKEN_IGUAL = 'IGUAL'
TOKEN_MENOR_QUE = 'MENOR_QUE'
TOKEN_MAIOR_QUE = 'MAIOR_QUE'
TOKEN_MENOR_OU_IGUAL = 'MENOR_OU_IGUAL'
TOKEN_MAIOR_OU_IGUAL = 'MAIOR_OU_IGUAL'
TOKEN_DIFERENTE = 'DIFERENTE'

TOKEN_EOF = 'EOF'


# Palavras-chave permitidas
KEYWORDS = {
    'program', 
    'var', 
    'integer', 
    'real', 
    'begin', 
    'end',
    'boolean',
    'procedure',
    'if',
    'then',
    'else',
    'while',
    'do',
    'not',
    }

class Posicao:
    def __init__(self, indice, linha, coluna, nome_arquivo, texto_arquivo):
        self.indice = indice
        self.linha = linha
        self.coluna = coluna
        self.nome_arquivo = nome_arquivo
        self.texto_arquivo = texto_arquivo

    def avancar(self, caractere_atual):
        self.indice += 1
        self.coluna += 1

        if caractere_atual == '\n':
            self.linha += 1
            self.coluna = 0

        return self

    def copiar(self):
        return Posicao(self.indice, self.linha, self.coluna, self.nome_arquivo, self.texto_arquivo)

class Token:
    def __init__(self, tipo, valor=None, linha=0):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha

    def __repr__(self):
        if self.valor: 
            return f'{self.tipo}:{self.valor} (Linha {self.linha})'
        return f'{self.tipo} (Linha {self.linha})'

class Lexer:
    def __init__(self, nome_arquivo, texto):
        self.nome_arquivo = nome_arquivo
        self.texto = texto
        self.posicao = Posicao(-1, 0, -1, nome_arquivo, texto)
        self.char_atual = None
        self.avancar()

    def avancar(self):
        self.posicao.avancar(self.char_atual)
        self.char_atual = self.texto[self.posicao.indice] if self.posicao.indice < len(self.texto) else None

    def criar_tokens(self):
        tokens = []

        while self.char_atual is not None:
            if self.char_atual in ' \t\n':
                self.avancar()
            elif self.char_atual in DIGITOS:
                token, erro = self.criar_numero()
                if erro: 
                    return [], erro
                tokens.append(token)
            elif self.char_atual.isalpha():
                token, erro = self.criar_identificador()
                if erro: 
                    return [], erro
                tokens.append(token)
            elif self.char_atual == '+':
                tokens.append(Token(TOKEN_PLUS, '+', self.posicao.linha))
                self.avancar()
            elif self.char_atual == '-':
                tokens.append(Token(TOKEN_MINUS, '-', self.posicao.linha))
                self.avancar()
            elif self.char_atual == '*':
                tokens.append(Token(TOKEN_MULTIPLY, '*', self.posicao.linha))
                self.avancar()
            elif self.char_atual == '/':
                tokens.append(Token(TOKEN_DIVIDE, '/', self.posicao.linha))
                self.avancar()
            elif self.char_atual == '(':
                tokens.append(Token(TOKEN_LEFT_PAREN, '(', self.posicao.linha))
                self.avancar()
            elif self.char_atual == ')':
                tokens.append(Token(TOKEN_RIGHT_PAREN, ')', self.posicao.linha))
                self.avancar()
            elif self.char_atual == ';':
                tokens.append(Token(TOKEN_SEMICOLON, ';', self.posicao.linha))
                self.avancar()
            elif self.char_atual == ':':
                if self.proximo_caractere() == '=':
                    self.avancar()
                    self.avancar()
                    tokens.append(Token(TOKEN_ASSIGN, ':=', self.posicao.linha))
                else:
                    tokens.append(Token(TOKEN_COLON, ':', self.posicao.linha))
                    self.avancar()
            elif self.char_atual == ',':
                tokens.append(Token(TOKEN_COMMA, ',', self.posicao.linha))
                self.avancar()
            elif self.char_atual == '.':
                tokens.append(Token(TOKEN_PERIOD, '.', self.posicao.linha))
                self.avancar()
            elif self.char_atual == '{':
                erro = self.pular_comentario()
                if erro: 
                    return [], erro
            elif self.char_atual == '=':
                tokens.append(Token(TOKEN_IGUAL, '=', self.posicao.linha))
                self.avancar()
            elif self.char_atual == '<':
                if self.proximo_caractere() == '>':
                    self.avancar()
                    self.avancar()
                    tokens.append(Token(TOKEN_DIFERENTE, '<>', self.posicao.linha))
                elif self.proximo_caractere() == '=':
                    self.avancar()
                    self.avancar()
                    tokens.append(Token(TOKEN_MENOR_OU_IGUAL, '<=', self.posicao.linha))
                else:
                    tokens.append(Token(TOKEN_MENOR_QUE, '<', self.posicao.linha))
                    self.avancar()
            elif self.char_atual == '>':
                if self.proximo_caractere() == '=':
                    self.avancar()
                    self.avancar()
                    tokens.append(Token(TOKEN_MAIOR_OU_IGUAL, '>=', self.posicao.linha))
                else:
                    tokens.append(Token(TOKEN_MAIOR_QUE, '>', self.posicao.linha))
                    self.avancar()
            else:
                posicao_inicio = self.posicao.copiar()
                char = self.char_atual
                self.avancar()
                return [], ErroCaractereIlegal(posicao_inicio, self.posicao, "'" + char + "'")

        tokens.append(Token(TOKEN_EOF, None, self.posicao.linha))
        return tokens, None

    def criar_numero(self):
        numero_str = ''
        ponto_contador = 0
        linha = self.posicao.linha

        while self.char_atual is not None and (self.char_atual in DIGITOS or self.char_atual == '.'):
            if self.char_atual == '.':
                if ponto_contador == 1: 
                    break  # Mais de um ponto decimal encontrado
                ponto_contador += 1
            numero_str += self.char_atual
            self.avancar()

        # Verifica se há letras logo após o número, o que é inválido
        if self.char_atual is not None and self.char_atual.isalpha():
            posicao_inicio = self.posicao.copiar()
            while self.char_atual is not None and self.char_atual.isalnum():
                numero_str += self.char_atual  # Consumir todo o token inválido
                self.avancar()
            return None, ErroCaractereIlegal(posicao_inicio, self.posicao, f"'{numero_str}'")

        # Retorna o token apropriado
        if ponto_contador == 0:
            return Token(TOKEN_INT, int(numero_str), linha), None
        else:
            return Token(TOKEN_FLOAT, float(numero_str), linha), None

    def criar_identificador(self):
        identificador_str = ''
        linha = self.posicao.linha

        # Primeiro caractere deve ser uma letra
        if not self.char_atual.isalpha():
            posicao_inicio = self.posicao.copiar()
            char = self.char_atual
            self.avancar()
            return None, ErroCaractereIlegal(posicao_inicio, self.posicao, f"'{char}'")

        # Continua enquanto houver letras, dígitos ou sublinhas
        while self.char_atual is not None and (self.char_atual.isalnum() or self.char_atual == '_'):
            identificador_str += self.char_atual
            self.avancar()

        # Verifica se é uma palavra reservada ou identificador
        if identificador_str in KEYWORDS:
            return Token(TOKEN_KEYWORD, identificador_str, linha), None
        else:
            return Token(TOKEN_IDENTIFIER, identificador_str, linha), None


    def pular_comentario(self):
        pos_inicio = self.posicao.copiar()  # Guardar posição inicial para o caso de erro
        self.avancar()  # Pula o '{'
        
        while self.char_atual is not None:
            if self.char_atual == '}':
                self.avancar()  # Comentário fechado corretamente
                return
            self.avancar()
        
        # Se sair do loop sem encontrar '}', o comentário não foi fechado
        return ErroComentarioNaoFechado(pos_inicio)

    def proximo_caractere(self):
        if self.posicao.indice + 1 < len(self.texto):
            return self.texto[self.posicao.indice + 1]
        return None

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.criar_tokens()
    return tokens, error

# Função para exibir a tabela
def exibir_tabela(tokens):
    print(f"{'Token':<15} {'Classificação':<20} {'Linha':<5}")
    print('-' * 45)
    print()

    for token in tokens:
        valor = token.valor if token.valor is not None else ''  # Evita NoneType error
        classificacao = classificar_token(token)
        print(f"{valor:<15} {classificacao:<20} {token.linha:<5}")

def classificar_token(token):
    if token.tipo == TOKEN_KEYWORD:
        return 'Palavra reservada'
    elif token.tipo == TOKEN_IDENTIFIER:
        return 'Identificador'
    elif token.tipo in {TOKEN_INT, TOKEN_FLOAT}:
        return 'Número inteiro' if token.tipo == TOKEN_INT else 'Número real'
    elif token.tipo in {TOKEN_PLUS, TOKEN_MINUS, TOKEN_MULTIPLY, TOKEN_DIVIDE}:
        return 'Operador'
    elif token.tipo in {TOKEN_IGUAL, TOKEN_MENOR_QUE, TOKEN_MAIOR_QUE, 
                        TOKEN_MENOR_OU_IGUAL, TOKEN_MAIOR_OU_IGUAL, TOKEN_DIFERENTE}:
        return 'Operador relacional'
    elif token.tipo == TOKEN_ASSIGN:
        return 'Atribuição'
    elif token.tipo in {TOKEN_SEMICOLON, TOKEN_COLON, TOKEN_PERIOD, TOKEN_COMMA}:
        return 'Delimitador'
    elif token.tipo == TOKEN_EOF:
        return 'Fim de arquivo'
    return 'Desconhecido'
