# test_basic.py
import unittest
from basic import Lexer, TOKEN_IDENTIFIER, TOKEN_KEYWORD, ErroCaractereIlegal

class TestLexer(unittest.TestCase):
    def test_identificador_valido(self):
        lexer = Lexer("test", "varName")
        tokens, error = lexer.criar_tokens()
        self.assertIsNone(error)
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].tipo, TOKEN_IDENTIFIER)
        self.assertEqual(tokens[0].valor, "varName")

    def test_identificadores_invalidos(self):
        invalid_identifiers = [
            '1varName', 
            'var@name',
            'var#name'
        ]
        for identifier in invalid_identifiers:
            with self.subTest(identifier=identifier):
                lexer = Lexer("test", identifier)
                tokens, error = lexer.criar_tokens()
                self.assertIsNotNone(error)
                self.assertIsInstance(error, ErroCaractereIlegal)

    def test_palavras_chave(self):
        keywords = [
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
            ]
        for keyword in keywords:
            with self.subTest(keyword=keyword):
                lexer = Lexer("test", keyword)
                tokens, error = lexer.criar_tokens()
                self.assertIsNone(error)
                self.assertEqual(len(tokens), 2) 
                self.assertEqual(tokens[0].tipo, TOKEN_KEYWORD)
                self.assertEqual(tokens[0].valor, keyword)

if __name__ == "__main__":
    unittest.main()