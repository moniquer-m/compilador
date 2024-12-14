# Analisador Léxico, Sintático e Semântico para C
---

### Como executar:

> Certifique-se de ter Python instalado em seu sistema.
> 
1. Clone o repositório ou baixe os arquivos parser.py e t1.py.
2. Abra um terminal e navegue até o diretório contendo os arquivos.
3. Execute o analisador com o seguinte comando:
    
    python parser.py
    
4. O programa analisará o código C de exemplo embutido no arquivo parser.py. Para analisar um código diferente, modifique a variável test_code no final do arquivo parser.py.

## Relatório de Implementação:

1. Análise Léxica
    
    A análise léxica é implementada no arquivo t1.py usando a biblioteca PLY (Python Lex-Yacc). Esta fase divide o código-fonte em tokens, que são as unidades básicas da linguagem, como identificadores, palavras-chave, operadores e literais.
    
    ### Principais aspectos:
    
    - Definição de tokens para a linguagem C
    - Uso de expressões regulares para reconhecer padrões
    - Tratamento de comentários e espaços em branco
    
    ---
    
2. Análise Sintática
    
    A análise sintática é implementada na classe Parser no arquivo parser.py. Esta fase verifica se a sequência de tokens forma estruturas válidas da linguagem C.
    
    ### Principais aspectos:
    
    - Implementação do método de análise descendente recursiva
    - Funções para cada não-terminal da gramática (ex: program(), function_declaration(), statement())
    - Tratamento de estruturas como declarações, atribuições, condicionais e loops
    
    Exemplo de regra sintática:
    
    ```python
    def if_statement(self):
        self.eat('IF')
        self.eat('LPAREN')
        self.expression()
        self.eat('RPAREN')
        self.compound_statement()
        if self.current_token and self.current_token.type == 'ELSE':
            self.eat('ELSE')
            self.compound_statement()
    ```
    
    ---
    
3. Análise Semântica
    
    A análise semântica é incorporada na análise sintática, realizando verificações durante a construção da árvore sintática.
    
    ### Principais aspectos:
    
    1. Declaração de variáveis: Verifica se as variáveis são declaradas antes do uso.
        
        ### Exemplo:
        
        ```
           if not self.symbol_table.declare(var_name, var_type): self.error(f"Variável '{var_name}' já declarada neste escopo")
        
        ```
        
    2. Verificação de tipos: Garante que os tipos são compatíveis em atribuições e operações.
        
        ### Exemplo:
        
        ```
           if not self.check_types(var_type, expr_type):self.error(f"Tipo incompatível na atribuição. Esperado {var_type}, recebido {expr_type}")
        
        ```
        
    3. Escopo: Mantém um controle de escopo para variáveis.
        
        ### Exemplo:
        
        ```python
        self.symbol_table.enter_scope()
        …
        self.symbol_table.exit_scope()
        ```
        
    4. Função main: Verifica a presença da função main.
        
        ### Exemplo:
        
        ```
          if not self.has_main: self.error("Função main() não encontrada")
        
        ```
        
    5. Tabela de Símbolos
        
        A tabela de símbolos é implementada na classe SymbolTable. Ela mantém informações sobre identificadores e seus tipos, gerenciando diferentes escopos.
        
        ### Exemplo:
        
        ```
        class SymbolTable:
        	def __init__(self):
            self.scopes = [{}]
        
        	def declare(self, name, type):
            if name in self.scopes[-1]:
                return False
            self.scopes[-1][name] = type
            return True
        
        ```
        
    
    ---
    
4. Relação com a Teoria de Compiladores
- Análise Léxica: Implementa o conceito de tokenização, transformando a entrada em uma sequência de tokens.
- Análise Sintática: Utiliza o método de análise descendente recursiva, que é uma forma de parsing top-down.
- Análise Semântica: Realiza verificações de tipo e escopo, essenciais para garantir a correção semântica do programa.
- Tabela de Símbolos: Implementa o conceito de gerenciamento de identificadores e seus atributos.

Esta implementação demonstra os princípios fundamentais da construção de compiladores, aplicando conceitos teóricos em um analisador prático para um subconjunto da linguagem C.
