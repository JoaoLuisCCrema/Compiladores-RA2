#Joao Lucas M N C e Joao Luis C C
#To execute the program, write on the terminal:
# python main.py operacoes1.txt
# python main.py operacoes2.txt
# python main.py operacoes3.txt

import sys

class Node:
    def __init__(self, value):
        """Initialize a Node with a value and no children."""
        self.value = value
        self.left = None
        self.right = None

def analisador_lexico(expressao):
    """Lexical analyzer that converts expression into tokens based on defined symbols and numbers."""
    simbolos = {
        '+': 'PLUS', '-': 'MINUS', '*': 'TIMES', '/': 'DIVIDE_INT', '%': 'MODULO',
        '^': 'POWER', '|': 'DIVIDE_REAL', '(': 'LPAREN', ')': 'RPAREN',
        'RES': 'RES', 'MEM': 'MEM'
    }
    tokens = []
    for token in expressao.replace('(', ' ( ').replace(')', ' ) ').split():
        if token in simbolos:
            tokens.append(simbolos[token])
        elif token.replace('.', '', 1).isdigit() or token.isdigit():
            tokens.append(('NUMBER', float(token)))
        else:
            raise ValueError(f"Unrecognized token: {token}")
    return tokens

def analisador_sintatico(tokens, memoria):
    """Syntax analyzer that builds an expression tree from tokens and a memory dictionary."""
    stack = []
    for token in tokens:
        if token == 'LPAREN':
            continue
        elif token == 'RPAREN':
            continue
        elif isinstance(token, tuple) and token[0] == 'NUMBER':
            stack.append(('NUM', token[1]))
        elif token in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE_INT', 'MODULO', 'POWER', 'DIVIDE_REAL']:
            if len(stack) < 2:
                raise ValueError("Not enough operands for operation.")
            right = stack.pop()
            left = stack.pop()
            stack.append((token, left, right))
        elif token == 'RES':
            if len(stack) < 1:
                raise ValueError("Invalid reference for RES operation.")
            n = int(stack.pop()[1])
            stack.append(('RES', n))
        elif token == 'MEM':
            if stack and isinstance(stack[-1], tuple) and stack[-1][0] == 'NUM':
                n = stack.pop()[1]
                memoria['valor'] = n
                stack.append(('MEM', 0))
            else:
                stack.append(('MEM', memoria['valor']))
        else:
            raise ValueError(f"Unrecognized token: {token}")
    if len(stack) == 1:
        return stack[0]
    else:
        raise ValueError("Malformed expression.")

def avaliar_arvore_sintatica(no, resultados, memoria):
    """Evaluate the syntax tree to compute the result."""
    if isinstance(no, tuple):
        operation = no[0]
        if operation in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE_INT', 'MODULO', 'POWER', 'DIVIDE_REAL']:
            _, left, right = no
            left_value = avaliar_arvore_sintatica(left, resultados, memoria)
            right_value = avaliar_arvore_sintatica(right, resultados, memoria)
            return calcular(operation, left_value, right_value)
        elif operation == 'RES':
            _, n = no
            if n > 0 and n <= len(resultados):
                return resultados[-n]
            else:
                raise ValueError("Invalid reference for RES operation.")
        elif operation == 'MEM':
            return no[1]
        elif operation == 'NUM':
            return no[1]
    else:
        raise ValueError("Invalid node in syntax tree.")

def calcular(operacao, esquerda, direita):
    """Helper function to perform arithmetic operations."""
    if operacao == 'PLUS':
        return esquerda + direita
    elif operacao == 'MINUS':
        return esquerda - direita
    elif operacao == 'TIMES':
        return esquerda * direita
    elif operacao == 'DIVIDE_INT':
        return int(esquerda) // int(direita)
    elif operacao == 'MODULO':
        return esquerda % direita
    elif operacao == 'POWER':
        return esquerda ** direita
    elif operacao == 'DIVIDE_REAL':
        return esquerda / direita
    return 0

def avaliar_expressao(expressao, resultados, memoria):
    """Evaluate the full expression and store the result."""
    tokens = analisador_lexico(expressao)
    arvore = analisador_sintatico(tokens, memoria)
    resultado = avaliar_arvore_sintatica(arvore, resultados, memoria)
    resultados.append(resultado)
    return tokens, arvore, resultado

def main(nome_arquivo):
    """Main function to read expressions from a file and evaluate them."""
    memoria = {'valor': 0}
    resultados = []

    with open(nome_arquivo, "r") as arquivo:
        expressoes = arquivo.readlines()

    print(f"------------ File {nome_arquivo} ------------\n")

    for expressao in expressoes:
        expressao = expressao.strip()
        try:
            tokens, arvore, resultado = avaliar_expressao(expressao, resultados, memoria)
            print(f"Expression: {expressao}")
            print("Token String:", tokens)
            print("Syntax Tree:", arvore)
            print(f"Result: {resultado}\n")
        except ValueError as e:
            print(f"Error processing expression '{expressao}': {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py file_name.txt")
    else:
        main(sys.argv[1])
