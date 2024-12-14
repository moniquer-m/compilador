# parser.py

from t1 import tokens, lexer

# Lista de funções da biblioteca padrão
STANDARD_FUNCTIONS = ['printf', 'scanf', 'malloc', 'free', 'exit']

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name, type):
        if name in self.scopes[-1]:
            return False
        self.scopes[-1][name] = type
        return True

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def get_type(self, name):
        return self.lookup(name)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.symbol_table = SymbolTable()
        self.has_main = False
        self.next()

    def next(self):
        self.current_token = self.lexer.token()
        while self.current_token and self.current_token.type in ['NEWLINE']:
            print(f"Skipping token: {self.current_token}")
            self.current_token = self.lexer.token()
        print(f"Current token: {self.current_token}")

    def error(self, message):
        raise Exception(f'Erro: {message}. Token atual: {self.current_token}')

    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            print(f"Eating token: {self.current_token}")
            value = self.current_token.value
            self.next()
            return value
        else:
            self.error(f"Token esperado: {token_type}")

    def check_types(self, left_type, right_type):
        if left_type == right_type:
            print(f"Verificação semântica: Tipos compatíveis - {left_type} e {right_type}")
            return True
        if left_type == 'float' and right_type == 'int':
            print(f"Verificação semântica: Tipos compatíveis - {left_type} pode receber {right_type}")
            return True
        print(f"Verificação semântica: Tipos incompatíveis - {left_type} e {right_type}")
        return False

    def get_expression_type(self, expr):
        if isinstance(expr, str):
            if expr.isdigit():
                return 'int'
            try:
                float(expr)
                return 'float'
            except ValueError:
                return self.symbol_table.get_type(expr)
        return None

    def program(self):
        while self.current_token:
            if self.current_token.type in ['INT', 'FLOAT', 'CHAR', 'VOID']:
                self.function_declaration()
        if not self.has_main:
            self.error("Função main() não encontrada")
        else:
            print("Verificação semântica: Função main() encontrada")

    def function_declaration(self):
        return_type = self.type_spec()
        if self.current_token.type == 'MAIN':
            self.has_main = True
            name = self.eat('MAIN')
        else:
            name = self.eat('ID')
        self.eat('LPAREN')
        self.symbol_table.enter_scope()
        self.parameters()
        self.eat('RPAREN')
        self.compound_statement()
        self.symbol_table.exit_scope()
        print(f"Verificação semântica: Função '{name}' declarada com tipo de retorno {return_type}")

    def type_spec(self):
        if self.current_token.type in ['INT', 'FLOAT', 'CHAR', 'VOID']:
            return self.eat(self.current_token.type)
        else:
            self.error("Tipo de dado esperado")

    def parameters(self):
        if self.current_token.type != 'RPAREN':
            self.parameter()
            while self.current_token.type == 'COMMA':
                self.eat('COMMA')
                self.parameter()

    def parameter(self):
        param_type = self.type_spec()
        param_name = self.eat('ID')
        if not self.symbol_table.declare(param_name, param_type):
            self.error(f"Parâmetro '{param_name}' já declarado")
        print(f"Verificação semântica: Parâmetro '{param_name}' declarado com tipo {param_type}")

    def compound_statement(self):
        self.eat('LBRACES')
        while self.current_token and self.current_token.type != 'RBRACES':
            self.statement()
        self.eat('RBRACES')

    def statement(self):
        if self.current_token.type in ['INT', 'FLOAT', 'CHAR']:
            self.declaration()
        elif self.current_token.type == 'ID':
            self.assignment_or_function_call()
        elif self.current_token.type == 'IF':
            self.if_statement()
        elif self.current_token.type == 'FOR':
            self.for_statement()
        elif self.current_token.type == 'WHILE':
            self.while_statement()
        elif self.current_token.type == 'RETURN':
            self.return_statement()
        else:
            self.error("Declaração inválida")
        
        if self.current_token and self.current_token.type == 'SEMICOLON':
            self.eat('SEMICOLON')

    def declaration(self):
        var_type = self.type_spec()
        var_name = self.eat('ID')
        if not self.symbol_table.declare(var_name, var_type):
            self.error(f"Variável '{var_name}' já declarada neste escopo")
        print(f"Verificação semântica: Variável '{var_name}' declarada com tipo {var_type}")
        while self.current_token.type == 'COMMA':
            self.eat('COMMA')
            var_name = self.eat('ID')
            if not self.symbol_table.declare(var_name, var_type):
                self.error(f"Variável '{var_name}' já declarada neste escopo")
            print(f"Verificação semântica: Variável '{var_name}' declarada com tipo {var_type}")
        if self.current_token.type == 'EQUALS':
            self.eat('EQUALS')
            expr = self.expression()
            expr_type = self.get_expression_type(expr)
            if not self.check_types(var_type, expr_type):
                self.error(f"Tipo incompatível na atribuição. Esperado {var_type}, recebido {expr_type}")

    def assignment_or_function_call(self):
        var_name = self.eat('ID')
        var_type = self.symbol_table.get_type(var_name)
        if var_type is None and var_name not in STANDARD_FUNCTIONS:
            self.error(f"Variável ou função '{var_name}' não declarada")
        print(f"Verificação semântica: Variável ou função '{var_name}' utilizada")
        if self.current_token.type == 'EQUALS':
            self.eat('EQUALS')
            expr = self.expression()
            expr_type = self.get_expression_type(expr)
            if not self.check_types(var_type, expr_type):
                self.error(f"Tipo incompatível na atribuição. Esperado {var_type}, recebido {expr_type}")
        elif self.current_token.type == 'LPAREN':
            self.eat('LPAREN')
            if self.current_token.type != 'RPAREN':
                self.arguments()
            self.eat('RPAREN')
            print(f"Verificação semântica: Chamada de função '{var_name}'")
        elif self.current_token.type in ['PLUS', 'MINUS']:
            op = self.current_token.type
            self.eat(op)
            if self.current_token.type == op:  # Verifica se é ++ ou --
                self.eat(op)
                print(f"Verificação semântica: Operação de incremento/decremento em '{var_name}'")
            else:
                expr = self.expression()
                expr_type = self.get_expression_type(expr)
                if not self.check_types(var_type, expr_type):
                    self.error(f"Tipo incompatível na operação. Esperado {var_type}, recebido {expr_type}")
        return var_name

    def arguments(self):
        self.expression()
        while self.current_token.type == 'COMMA':
            self.eat('COMMA')
            self.expression()

    def if_statement(self):
        self.eat('IF')
        self.eat('LPAREN')
        self.expression()
        self.eat('RPAREN')
        print("Verificação semântica: Início do bloco if")
        self.compound_statement()
        if self.current_token and self.current_token.type == 'ELSE':
            self.eat('ELSE')
            print("Verificação semântica: Início do bloco else")
            self.compound_statement()
        print("Verificação semântica: Fim da estrutura if-else")

    def for_statement(self):
        self.eat('FOR')
        self.eat('LPAREN')
        if self.current_token.type in ['INT', 'FLOAT', 'CHAR']:
            self.declaration()
        else:
            self.assignment_or_function_call()
        self.eat('SEMICOLON')
        self.expression()
        self.eat('SEMICOLON')
        self.assignment_or_function_call()
        self.eat('RPAREN')
        print("Verificação semântica: Início do loop for")
        self.compound_statement()
        print("Verificação semântica: Fim do loop for")

    def while_statement(self):
        self.eat('WHILE')
        self.eat('LPAREN')
        self.expression()
        self.eat('RPAREN')
        print("Verificação semântica: Início do loop while")
        self.compound_statement()
        print("Verificação semântica: Fim do loop while")

    def return_statement(self):
        self.eat('RETURN')
        if self.current_token.type != 'SEMICOLON':
            self.expression()
        print("Verificação semântica: Declaração de retorno")

    def expression(self):
        return self.logical_or()

    def logical_or(self):
        node = self.logical_and()
        while self.current_token and self.current_token.type == 'OR':
            self.eat('OR')
            self.logical_and()
        return node

    def logical_and(self):
        node = self.equality()
        while self.current_token and self.current_token.type == 'AND':
            self.eat('AND')
            self.equality()
        return node

    def equality(self):
        node = self.relational()
        while self.current_token and self.current_token.type in ['EQ', 'NE']:
            self.eat(self.current_token.type)
            self.relational()
        return node

    def relational(self):
        node = self.additive()
        while self.current_token and self.current_token.type in ['LT', 'LE', 'GT', 'GE']:
            self.eat(self.current_token.type)
            self.additive()
        return node

    def additive(self):
        node = self.multiplicative()
        while self.current_token and self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token.type
            self.eat(op)
            self.multiplicative()
        return node

    def multiplicative(self):
        node = self.unary()
        while self.current_token and self.current_token.type in ('TIMES', 'DIVIDE'):
            op = self.current_token.type
            self.eat(op)
            self.unary()
        return node

    def unary(self):
        if self.current_token.type in ['PLUS', 'MINUS', 'NOT']:
            self.eat(self.current_token.type)
            return self.unary()
        else:
            return self.factor()

    def factor(self):
        if self.current_token.type in ['INTEGER', 'REAL', 'CHAR', 'STRING']:
            return self.eat(self.current_token.type)
        elif self.current_token.type == 'ID':
            return self.assignment_or_function_call()
        elif self.current_token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expression()
            self.eat('RPAREN')
            return node
        else:
            self.error("Fator inválido")

    def parse(self):
        self.program()
        print("Análise sintática e semântica concluída com sucesso!")

# Código de teste
if __name__ == "__main__":
    test_code = '''
    int main() {
        int x, y;
        float z;
        x = 5;
        y = 10;
        z = 3.14;
        
        if (x < y && z > 3.0) {
            printf("Hello, world!");
            x++;
        } else {
            y--;
        }
        
        for (int i = 0; i < 10; i++) {
            x = x + i;
        }
        
        while (x < 100) {
            x = x + 1;
        }

        return 0;
    }
    '''
    
    lexer.input(test_code)
    parser = Parser(lexer)
    parser.parse()