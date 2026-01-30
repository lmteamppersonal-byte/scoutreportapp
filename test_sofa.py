import re

def extrair_id_jogador(url):
    try:
        match = re.search(r"\/(\d+)$", url.rstrip('/'))
        if match:
            return match.group(1)
        return url.split('/')[-1]
    except:
        return None

# Test Cases
urls = [
    "https://www.sofascore.com/player/neymar/12345",
    "https://www.sofascore.com/pt/jogador/some-player/987654",
    "sofascore.com/player/111"
]

print("Testing Extraction:")
for u in urls:
    print(f"{u} -> {extrair_id_jogador(u)}")

print("\nDone.")
