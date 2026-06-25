# Transcritor de Vídeos/Áudios com Faster-Whisper

Script em Python que transcreve automaticamente vídeos e áudios para texto, com timestamps, usando o modelo [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper). Inclui um filtro opcional por palavras-chave, útil para localizar rapidamente trechos relevantes (ex.: termos técnicos como "IP", "PLC", "ethernet") em gravações longas.

## Funcionalidades

- Transcrição em lote de todos os vídeos/áudios de uma pasta
- Saída em `.txt` com timestamps no formato `[HH:MM:SS]`
- Suporte a GPU (CUDA) com `float16` para maior velocidade
- Filtro opcional por palavras-chave para focar em trechos específicos
- Suporte a múltiplos formatos de vídeo e áudio

## Formatos suportados

`.mp4`, `.mkv`, `.avi`, `.mov`, `.mp3`, `.wav`, `.m4a`, `.webm`

## Requisitos

- Python 3.9+
- GPU NVIDIA com CUDA configurado (o script usa `device="cuda"` por padrão)
- [FFmpeg](https://ffmpeg.org/download.html) instalado

### Instalação das dependências

```bash
pip install faster-whisper
```

### FFmpeg

O script espera o FFmpeg em `C:\ffmpeg\bin` (Windows). Ajuste o caminho na linha:

```python
os.environ["PATH"] += r";C:\ffmpeg\bin"
```

caso tenha instalado em outro local, ou remova essa linha se o FFmpeg já estiver no PATH do sistema.

## Estrutura de pastas

```
.
├── transcritor.py
├── videos/           # coloque aqui os vídeos/áudios a transcrever
└── transcricoes/     # criada automaticamente com os resultados
```

## Como usar

1. Crie a pasta `videos` (se não existir) e coloque dentro os arquivos a transcrever.
2. Ajuste as configurações no topo do script, se necessário:

```python
PASTA_VIDEOS = "./videos"
PASTA_SAIDA  = "./transcricoes"
MODELO       = "medium"   # tiny / base / small / medium / large-v3
IDIOMA       = "pt"
```

3. Execute o script:

```bash
python transcritor.py
```

4. As transcrições serão salvas em `./transcricoes/<nome_do_arquivo>.txt`.

## Filtro por palavras-chave

Por padrão o filtro está desativado (`FILTRAR = False`), gerando a transcrição completa.

Para gerar apenas os trechos que contêm certas palavras (ex.: jargão técnico em reuniões), ative o filtro e edite a lista de termos:

```python
FILTRAR = True
KEYWORDS = ["ip", "plc", "address", "network", "ethernet"]
```

Com o filtro ativo, somente as linhas cujo texto contenha pelo menos uma das palavras-chave (case-insensitive) serão escritas no arquivo final.

## Modelos disponíveis

| Modelo     | Velocidade | Precisão | Uso de VRAM |
|------------|-----------|----------|-------------|
| tiny       | Muito rápido | Baixa | Mínimo |
| base       | Rápido | Razoável | Baixo |
| small      | Médio | Boa | Médio |
| medium     | Lento | Muito boa | Alto |
| large-v3   | Muito lento | Excelente | Muito alto |

## Observações

- Caso não possua GPU disponível, altere `device="cuda"` para `device="cpu"` e `compute_type="float16"` para `compute_type="int8"` (ou `float32`), com impacto na velocidade.
- O idioma padrão é português (`pt`); altere conforme o conteúdo dos arquivos.
- Vídeos são processados em ordem alfabética.
