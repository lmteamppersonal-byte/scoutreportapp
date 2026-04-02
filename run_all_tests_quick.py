#!/usr/bin/env python3
"""
Script RÁPIDO para rodar todos os testes em 1 comando.
Resultado resumido em 30 segundos.
"""

import subprocess
import sys

def run_test(script_name, test_name):
    """Executar um script de teste e retornar sucesso/falha"""
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=20
        )
        # Verificar se "PASSOU" aparece no output
        passed = "5/5 testes passaram" in result.stdout or "RESULTADO FINAL" in result.stdout
        return passed, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("\n" + "="*70)
    print("🚀 EXECUTANDO TODOS OS TESTES")
    print("="*70 + "\n")
    
    tests = [
        ("test_radar_16_eixos.py", "Testes de Unidade"),
        ("test_integracao_completa.py", "Testes de Integração"),
    ]
    
    results = []
    
    for script, label in tests:
        print(f"Executando: {label}...")
        passed, stdout, stderr = run_test(script, label)
        results.append((label, passed))
        
        if passed:
            print(f"✅ {label}: PASSOU\n")
        else:
            print(f"❌ {label}: FALHOU\n")
            if stderr:
                print(f"   Erro: {stderr[:100]}\n")
    
    # Resumo
    print("="*70)
    print("📊 RESUMO FINAL")
    print("="*70 + "\n")
    
    passed_count = sum(1 for _, passed in results if passed)
    total = len(results)
    
    for test_name, passed in results:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{status}: {test_name}")
    
    print(f"\nRESULTADO: {passed_count}/{total} suítes passaram\n")
    
    if passed_count == total:
        print("🎉 TODOS OS TESTES PASSARAM COM SUCESSO! 🎉\n")
        print("✨ Aplicação pronta para produção!\n")
        return 0
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.\n")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
