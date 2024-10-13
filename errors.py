class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.nome_arquivo}, line {self.pos_start.linha + 1}'
        return result
    
class ErroCaractereIlegal(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class ErroComentarioNaoFechado(Error):
    def __init__(self, pos_inicio):
        super().__init__(pos_inicio, pos_inicio, 'Comentário Não Fechado', 'O comentário não foi fechado corretamente com "}"')
