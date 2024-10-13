import basic

client_input = """
program Teste; {comentário de exemplo}
var
    valor1, valor2: integer;
begin
    valor1 := 10;
    valor2 := valor1 + 20;
end.
"""

tokens, erro = basic.run('<stdin>', client_input)

print("ERRO RETORNADO", erro)

if erro:
    print(erro.as_string())
else:
    basic.exibir_tabela(tokens)