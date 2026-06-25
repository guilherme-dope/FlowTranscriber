from faster_whisper import WhisperModel
import os
from pathlib import Path

os.environ["PATH"] += r";C:\ffmpeg\bin"

# ─── CONFIGURAÇÕES ───────────────────────────────────────────
PASTA_VIDEOS = "./videos"
PASTA_SAIDA  = "./transcricoes"
MODELO       = "medium"   # tiny / base / small / medium / large-v3
IDIOMA       = "pt"

# 🔍 palavras-chave (pode editar)
FILTRAR = False
KEYWORDS = ["ip", "plc", "address", "network", "ethernet"]
# ─────────────────────────────────────────────────────────────

EXTENSOES_VALIDAS = {".mp4", ".mkv", ".avi", ".mov",
                     ".mp3", ".wav", ".m4a", ".webm"}


def formatar_tempo(segundos):
    h = int(segundos // 3600)
    m = int((segundos % 3600) // 60)
    s = int(segundos % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def transcrever_video(model, caminho_video, pasta_saida):
    print(f"\nTranscrevendo: {caminho_video.name}")

    segments, info = model.transcribe(
        str(caminho_video),
        language=IDIOMA,
        beam_size=5
    )

    Path(pasta_saida).mkdir(exist_ok=True)
    saida = Path(pasta_saida) / f"{caminho_video.stem}.txt"

    with open(saida, "w", encoding="utf-8") as f:
        for seg in segments:
            texto = seg.text.strip()

            # 🔍 filtro inteligente
            if FILTRAR:
                if not any(k in texto.lower() for k in KEYWORDS):
                    continue

            inicio = formatar_tempo(seg.start)
            f.write(f"[{inicio}] {texto}\n")

    print(f"  Salvo em: {saida}")


def main():
    videos = [
        p for p in Path(PASTA_VIDEOS).iterdir()
        if p.suffix.lower() in EXTENSOES_VALIDAS
    ]

    if not videos:
        print(f"Nenhum vídeo encontrado em '{PASTA_VIDEOS}'")
        return

    print(f"Encontrados {len(videos)} vídeo(s) para transcrever.")
    print(f"Carregando modelo Faster-Whisper '{MODELO}'...")

    # 🚀 GPU + otimização
    model = WhisperModel(
        MODELO,
        device="cuda",
        compute_type="float16"
    )

    for video in sorted(videos):
        transcrever_video(model, video, PASTA_SAIDA)

    print(f"\nConcluído! Transcrições salvas em '{PASTA_SAIDA}'")


if __name__ == "__main__":
    main()