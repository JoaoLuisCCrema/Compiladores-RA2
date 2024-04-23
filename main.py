import sys

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def analisador_lexico(expressao):
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
            raise ValueError(f"Token desconhecido: {token}")
    return tokens

def analisador_sintatico(tokens, memoria):
    stack = []
    for token in tokens:
        if token == 'LPAREN':
            continue
        elif token == 'RPAREN':
            # Finalizar o comando MEM ou levantar um erro se houver desequilíbrio de parênteses
            continue
        elif isinstance(token, tuple) and token[0] == 'NUMBER':
            stack.append(('NUM', token[1]))
        elif token in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE_INT', 'MODULO', 'POWER', 'DIVIDE_REAL']:
            if len(stack) < 2:
                raise ValueError(f"Não há operandos suficientes para a operação: {token}")
            direita = stack.pop()
            esquerda = stack.pop()
            stack.append((token, esquerda, direita))
        elif token == 'RES':
            if len(stack) < 1:
                raise ValueError("Operação RES sem referência válida.")
            n = int(stack.pop()[1])
            stack.append(('RES', n))
        elif token == 'MEM':
            # Se houver um número antes de 'MEM', empilhe a operação de armazenamento com 0.
            if stack and isinstance(stack[-1], tuple) and stack[-1][0] == 'NUM':
                n = stack.pop()[1]
                memoria['valor'] = n
                stack.append(('MEM', 0))
            else:
                # Caso contrário, empilhe a operação de recuperação com o valor da memória.
                stack.append(('MEM', memoria['valor']))
        else:
            raise ValueError(f"Token desconhecido: {token}")
    if len(stack) == 1:
        return stack[0]
    else:
        raise ValueError("Expressão mal formada.")

def avaliar_arvore_sintatica(no, resultados, memoria):
    if isinstance(no, tuple):
        operacao = no[0]
        if operacao in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE_INT', 'MODULO', 'POWER', 'DIVIDE_REAL']:
            _, esquerda, direita = no
            esquerda_valor = avaliar_arvore_sintatica(esquerda, resultados, memoria)
            direita_valor = avaliar_arvore_sintatica(direita, resultados, memoria)
            return calcular(operacao, esquerda_valor, direita_valor)
        elif operacao == 'RES':
            _, n = no
            if n > 0 and n <= len(resultados):
                return resultados[-n]
            else:
                raise ValueError("Referência inválida para operação RES, n fora dos limites.")
        elif operacao == 'MEM':
            # Retorna o valor atual de 'MEM'.
            return no[1]
        elif operacao == 'NUM':
            # Retorna o número literal.
            return no[1]
    else:
        raise ValueError("Nó inválido na árvore sintática.")

def calcular(operacao, esquerda, direita):
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
    tokens = analisador_lexico(expressao)
    arvore = analisador_sintatico(tokens, memoria)
    resultado = avaliar_arvore_sintatica(arvore, resultados, memoria)
    resultados.append(resultado)
    return tokens, arvore, resultado

def main(nome_arquivo):
    memoria = {'valor': 0}
    resultados = []

    with open(nome_arquivo, "r") as arquivo:
        expressoes = arquivo.readlines()

    print(f"------------ Arquivo {nome_arquivo} ------------\n")

    for expressao in expressoes:
        expressao = expressao.strip()
        try:
            tokens, arvore, resultado = avaliar_expressao(expressao, resultados, memoria)
            print(f"Expressao: {expressao}")
            print("String de Tokens:", tokens)
            print("Árvore Sintática:", arvore)
            print(f"Resultado: {resultado}\n")
        except ValueError as e:
            print(f"Erro ao processar a expressão '{expressao}': {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py nome_do_arquivo.txt")
    else:
        main(sys.argv[1])
