import textos  # Importa o módulo convertido no passo anterior
from typing import List, Dict, Union, Tuple


class Numerologo:
    """
    Classe para realizar a análise numerológica de nomes e datas.
    """

    # Mapeamento de letras para números
    _alfabeto: Dict[str, int] = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
        'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9,
        's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8
    }

    _vogais: Dict[str, int] = {
        'a': 1, 'b': 0, 'c': 0, 'd': 0, 'e': 5, 'f': 0, 'g': 0, 'h': 0, 'i': 9,
        'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 6, 'p': 0, 'q': 0, 'r': 0,
        's': 0, 't': 0, 'u': 3, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0
    }

    _consoantes: Dict[str, int] = {
        'a': 0, 'b': 2, 'c': 3, 'd': 4, 'e': 0, 'f': 6, 'g': 7, 'h': 8, 'i': 0,
        'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 0, 'p': 7, 'q': 8, 'r': 9,
        's': 1, 't': 2, 'u': 0, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8
    }

    # Constantes de compatibilidade
    _NaturalFit = 2
    _EasyFit = 1
    _Neutral = 0
    _Challenge = -1

    _chances_de_compatibilidade: Dict[int, str] = {
        -2: "Ruins",
        -1: "Não Muito Boas",
        0: "Neutras",
        1: "Boas",
        2: "Muito Boas",
        3: "Excelentes",
        4: "Perfeitas"
    }

    # Mapeamento de compatibilidade (baseado em números reduzidos 1-9)
    # A estrutura original em Scala é Map[Int, Map[Int, Int]].
    _compatibilidade: Dict[int, Dict[int, int]] = {
        1: {
            1: _NaturalFit, 5: _NaturalFit, 7: _NaturalFit,
            3: _EasyFit, 9: _EasyFit,
            8: _Neutral,
            2: _Challenge, 4: _Challenge, 6: _Challenge
        },
        2: {
            2: _NaturalFit, 4: _NaturalFit, 8: _NaturalFit,
            3: _EasyFit, 6: _EasyFit,
            9: _Neutral,
            1: _Challenge, 5: _Challenge, 7: _Challenge
        },
        3: {
            3: _NaturalFit, 6: _NaturalFit, 9: _NaturalFit,
            1: _EasyFit, 2: _EasyFit, 5: _EasyFit,
            4: _Challenge, 7: _Challenge, 8: _Challenge
        },
        4: {
            2: _NaturalFit, 4: _NaturalFit, 8: _NaturalFit,
            6: _EasyFit, 7: _EasyFit,
            1: _Challenge, 3: _Challenge, 5: _Challenge, 9: _Challenge
        },
        5: {
            1: _NaturalFit, 5: _NaturalFit, 7: _NaturalFit,
            3: _EasyFit, 9: _EasyFit,
            8: _Neutral,
            2: _Challenge, 4: _Challenge, 6: _Challenge
        },
        6: {
            3: _NaturalFit, 6: _NaturalFit, 9: _NaturalFit,
            2: _EasyFit, 4: _EasyFit, 8: _EasyFit,
            1: _Challenge, 5: _Challenge, 7: _Challenge
        },
        7: {
            1: _NaturalFit, 5: _NaturalFit, 7: _NaturalFit,
            4: _EasyFit,
            9: _Neutral,
            2: _Challenge, 3: _Challenge, 6: _Challenge, 8: _Challenge
        },
        8: {
            2: _NaturalFit, 4: _NaturalFit, 8: _NaturalFit,
            6: _EasyFit,
            1: _Neutral, 5: _Neutral,
            3: _Challenge, 7: _Challenge, 9: _Challenge
        },
        9: {
            3: _NaturalFit, 6: _NaturalFit, 9: _NaturalFit,
            1: _EasyFit, 5: _EasyFit,
            2: _Neutral, 7: _Neutral,
            4: _Challenge, 8: _Challenge
        }
    }

    def _letras_do_nome(self, nome: str) -> List[str]:
        """
        Normaliza o nome: minúsculas, remove espaços e acentos.
        Implementação corrigida do Scala para normalizar acentos.
        """
        # Remove espaços e converte para minúsculas
        nome_limpo = nome.lower().replace(" ", "")

        # Tabela de tradução para remover acentos (corrigindo a lógica do Scala)
        acento_mapping = str.maketrans(
            "áàâãäéèêẽëíìîĩïóòôõöúùûũüçñ",
            "aaaaaeeeeeiiiiiooooouuuuucn"
        )
        nome_normalizado = nome_limpo.translate(acento_mapping)

        # Retorna a lista de caracteres (strings de um caractere)
        return list(nome_normalizado)

    def _digitos_para_inteiros(self, data: str) -> List[int]:
        """Converte uma string de data (e.g., '11/05/1976') para uma lista de dígitos inteiros."""
        return [int(d) for d in data if d.isdigit()]

    def _somar_valores(self, valores: List[int]) -> int:
        """Soma uma lista de valores."""
        return sum(valores)

    def _quebrar_numero(self, numero: int) -> List[int]:
        """Quebra um número em seus dígitos (ex: 45 -> [4, 5])."""
        return [int(d) for d in str(numero)]

    def _reduzir(self, numeros: List[int]) -> int:
        """
        Redução numerológica. Soma os dígitos até obter um número de 1 a 9, 11 ou 22.
        """
        resultado: int = self._somar_valores(numeros)

        # Retorna o resultado se for 1-9 ou os números mestres 11, 22
        if (1 <= resultado <= 9) or resultado == 11 or resultado == 22:
            return resultado
        else:
            # Caso contrário, quebra o número e repete o processo (recursão)
            return self._reduzir(self._quebrar_numero(resultado))

    # --- Métodos de cálculo numerológico ---

    def caminho_da_vida(self, data: str) -> int:
        """Calcula o Número do Caminho da Vida."""
        return self._reduzir(self._digitos_para_inteiros(data))

    def destino(self, nome: str) -> int:
        """Calcula o Número do Destino (Expressão)."""
        letras = self._letras_do_nome(nome)
        valores = [self._alfabeto.get(c, 0) for c in letras]
        return self._reduzir(valores)

    def desejo_da_alma(self, nome: str) -> int:
        """Calcula o Número do Desejo da Alma (Vogais)."""
        letras = self._letras_do_nome(nome)
        valores = [self._vogais.get(c, 0) for c in letras]
        return self._reduzir(valores)

    def sonhos_interiores(self, nome: str) -> int:
        """Calcula o Número dos Sonhos Interiores (Consoantes)."""
        letras = self._letras_do_nome(nome)
        valores = [self._consoantes.get(c, 0) for c in letras]
        return self._reduzir(valores)

    def aniversario(self, data: str) -> int:
        """Calcula o Número do Aniversário (dia do nascimento)."""
        try:
            # Pega o primeiro elemento da data (dia) e converte para int
            return int(data.split("/")[0])
        except (ValueError, IndexError):
            return 0  # Valor padrão em caso de erro

    # --- Métodos de análise/saída ---

    def _reduzir_para_compatibilidade(self, numero: int) -> int:
        """Reduz 11 para 2 e 22 para 4 (como no código Scala original)."""
        if numero == 11:
            return 2
        if numero == 22:
            return 4
        return numero

    def analise(self, nome: str, data: str) -> str:
        """
        Gera o relatório HTML/XML da análise numerológica individual.
        """
        cdv = self.caminho_da_vida(data)
        dest = self.destino(nome)
        alma = self.desejo_da_alma(nome)
        sonhos = self.sonhos_interiores(nome)
        aniv = self.aniversario(data)

        # Obtém o conteúdo de 'textos' (agora o módulo textos.py)
        descricoes = textos.descricoes
        cdv_text = textos.caminhoDaVida.get(cdv, "Análise não disponível.")
        dest_text = textos.destino.get(dest, "Análise não disponível.")
        alma_text = textos.desejoDaAlma.get(alma, "Análise não disponível.")
        sonhos_text = textos.sonhosInteriores.get(
            sonhos, "Análise não disponível.")
        aniv_text = textos.aniversario.get(aniv, "Descrição não disponível.")

        return f"""
<div class="analise">
    <div class="cabecalho">
        <h1>Análise Numerológica &mdash; {nome} &mdash; {data} </h1>
    </div>
    <div class="caminho-da-vida">
        <h2>O Número do Caminho da Vida: {cdv}</h2>
        {descricoes.get('caminhoDaVida', 'Descrição não encontrada.')}
        {cdv_text}
    </div>
    <div class="destino">
        <h2>O Número do Destino: {dest}</h2>
        {descricoes.get('destino', 'Descrição não encontrada.')}
        {dest_text}
    </div>
    <div class="desejo-da-alma">
        <h2>O Número do Desejo da Alma: {alma}</h2>
        {descricoes.get('desejoDaAlma', 'Descrição não encontrada.')}
        {alma_text}
    </div>
    <div class="sonhos-interiores">
        <h2>O Número dos Sonhos Interiores: {sonhos}</h2>
        {descricoes.get('sonhosInteriores', 'Descrição não encontrada.')}
        {sonhos_text}
    </div>
    <div class="aniversario">
        <h2>O Número do Aniversário: {aniv}</h2>
        {descricoes.get('aniversario', 'Descrição não encontrada.')}
        {aniv_text}
    </div>
</div>
        """

    def analise_de_compatibilidade(self, nome1: str, data1: str, nome2: str, data2: str) -> str:
        """
        Gera o relatório HTML/XML da análise de compatibilidade.
        """
        # 1. Obter os números originais
        caminho1_orig = self.caminho_da_vida(data1)
        caminho2_orig = self.caminho_da_vida(data2)
        destino1_orig = self.destino(nome1)
        destino2_orig = self.destino(nome2)

        # 2. Reduzir 11->2 e 22->4 para o cálculo de compatibilidade (como no Scala)
        caminho1 = self._reduzir_para_compatibilidade(caminho1_orig)
        caminho2 = self._reduzir_para_compatibilidade(caminho2_orig)
        destino1 = self._reduzir_para_compatibilidade(destino1_orig)
        destino2 = self._reduzir_para_compatibilidade(destino2_orig)

        # 3. Calcular o Fator de Compatibilidade (soma dos índices)
        # O Scala usava List(caminho1, caminho2).sortWith(_<_) para a chave do texto,
        # mas para o cálculo do fator, usava o valor não ordenado no Map aninhado.
        # Python: usa .get() com um valor padrão de 0 para evitar KeyError, mas assume
        # que os números 1-9 estão presentes no dicionário.
        try:
            compatibilidade1 = self._compatibilidade[caminho1][caminho2]
        except KeyError:
            compatibilidade1 = 0

        try:
            compatibilidade2 = self._compatibilidade[destino1][destino2]
        except KeyError:
            compatibilidade2 = 0

        fator = compatibilidade1 + compatibilidade2
        chances = self._chances_de_compatibilidade.get(fator, "Indefinidas")

        # 4. Preparar as chaves (tuplas ordenadas) para buscar o texto do módulo 'textos'
        # O módulo 'textos' (converted from Scala's Textos object) usa tuplas (menor, maior) como chave
        indice_caminho: Tuple[int, int] = tuple(sorted([caminho1, caminho2]))
        indice_destino: Tuple[int, int] = tuple(sorted([destino1, destino2]))

        # 5. Obter os textos de compatibilidade
        compatibilidade_caminho_text = textos.compatibilidades.get(
            indice_caminho, "Texto de compatibilidade não encontrado.")
        compatibilidade_destino_text = textos.compatibilidades.get(
            indice_destino, "Texto de compatibilidade não encontrado.")

        return f"""
<div class="analise">
    <div class="cabecalho">
        <h1 class="titulo-compatibilidade">Análise Numerológica de Compatibilidade</h1>
        <div class="container dados">
            <h2 class="dados dados1"> {nome1} ({caminho1_orig}/{destino1_orig}) -- {data1} </h2>
            <h2 class="dados dados2"> {nome2} ({caminho2_orig}/{destino2_orig}) -- {data2} </h2>
        </div>
    </div>
    <div class="compatibilidade">
        <h3 class="resumo-compatibilidade">Chances de Compatibilidade: {chances} </h3>
    </div>
    <div class="container-analise-completa" data-role="collapsible">
        <h3>Ver mais detalhes</h3>
        <div class="caminho-da-vida">
            <h3>Compatibilidade dos Caminhos da Vida: {caminho1_orig} e {caminho2_orig}</h3>
            {compatibilidade_caminho_text}
        </div>
        <div class="destino">
            <h3>Compatibilidade dos Destinos: {destino1_orig} e {destino2_orig}</h3>
            {compatibilidade_destino_text}
        </div>
    </div>
</div>
        """

# --- Bloco de execução principal (equivalente ao object Numerologo.main em Scala) ---


if __name__ == '__main__':
    # Valores de exemplo do main original em Scala
    nome_exemplo = "Carlos Augusto Marcicano"
    data_exemplo = "11/05/1976"

    numerologo = Numerologo()

    # Demonstração de analise (substitui println(numerologo.analise(nome, data)))
    print("--- Relatório de Análise Individual ---")
    print(numerologo.analise(nome_exemplo, data_exemplo))

    # Demonstração de analiseDeCompatibilidade (substitui println(numerologo.analiseDeCompatibilidade(nome, data, nome, data)))
    print("\n--- Relatório de Análise de Compatibilidade (Consigo Mesmo) ---")
    print(numerologo.analise_de_compatibilidade(
        nome_exemplo, data_exemplo, nome_exemplo, data_exemplo))
