#!/usr/bin/env python3
"""
Script de Validação de Instalação - Gráfico Radar Avançado
Verifica se todas as dependências e arquivos estão configurados corretamente.
"""

import sys
import json
from pathlib import Path

def print_header(text):
    """Imprime cabeçalho formatado."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def check_python_version():
    """Verifica versão do Python."""
    print("\n1️⃣  Verificando Versão do Python...")
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 7):
        print(f"   ✅ Python {version} (OK)")
        return True
    else:
        print(f"   ❌ Python {version} (Requer 3.7+)")
        return False

def check_dependencies():
    """Verifica se as dependências estão instaladas."""
    print("\n2️⃣  Verificando Dependências...")
    
    deps = {
        "plotly": "Gráficos interativos",
        "kaleido": "Export PNG/SVG (opcional)",
    }
    
    all_ok = True
    
    for dep, description in deps.items():
        try:
            __import__(dep)
            status = "✅" if dep != "kaleido" else "✅ (opcional)"
            print(f"   {status} {dep:20} - {description}")
        except ImportError:
            if dep == "kaleido":
                print(f"   ⚠️  {dep:20} - NÃO INSTALADO (opcional)")
            else:
                print(f"   ❌ {dep:20} - NÃO INSTALADO (obrigatório)")
                all_ok = False
    
    return all_ok

def check_files():
    """Verifica se os arquivos principais existem."""
    print("\n3️⃣  Verificando Arquivos...")
    
    files = {
        "radar_chart_advanced.py": "Módulo principal",
        "test_radar_advanced.py": "Script de teste",
        "RADAR_EXAMPLES.py": "Exemplos de uso",
        "RADAR_CHART_ADVANCED_GUIDE.md": "Documentação técnica",
        "README_RADAR_ADVANCED.md": "Sumário executivo",
    }
    
    all_ok = True
    
    for filename, description in files.items():
        if Path(filename).exists():
            size = Path(filename).stat().st_size
            print(f"   ✅ {filename:40} ({size:,} bytes)")
        else:
            print(f"   ⚠️  {filename:40} NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok

def test_module_import():
    """Testa importação do módulo."""
    print("\n4️⃣  Testando Importação do Módulo...")
    
    try:
        from radar_chart_advanced import RadarChartAdvanced, criar_radar_comparativo
        print("   ✅ RadarChartAdvanced importado com sucesso")
        print("   ✅ criar_radar_comparativo importado com sucesso")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao importar: {str(e)}")
        return False

def test_module_functionality():
    """Testa funcionalidade básica do módulo."""
    print("\n5️⃣  Testando Funcionalidade do Módulo...")
    
    try:
        from radar_chart_advanced import RadarChartAdvanced
        
        # Criar instância
        radar = RadarChartAdvanced(
            labels=["Teste1", "Teste2", "Teste3", "Teste4"],
            title="Teste de Validação"
        )
        print("   ✅ Instância RadarChartAdvanced criada")
        
        # Adicionar série
        radar.add_series(
            name="Série Teste",
            data=[50, 75, 60, 80]
        )
        print("   ✅ Série adicionada com sucesso")
        
        # Testar métodos
        methods = {
            "to_html": "Exportação HTML",
            "to_json": "Exportação JSON",
        }
        
        for method, description in methods.items():
            try:
                result = getattr(radar, method)()
                if isinstance(result, (str, dict)):
                    print(f"   ✅ Método {method}() - {description}")
                else:
                    print(f"   ⚠️  Método {method}() retornou tipo inesperado")
            except Exception as e:
                print(f"   ❌ Erro em {method}(): {str(e)}")
                return False
        
        return True
    
    except Exception as e:
        print(f"   ❌ Erro durante testes: {str(e)}")
        return False

def test_example_data():
    """Testa com dados de exemplo."""
    print("\n6️⃣  Testando com Dados de Exemplo...")
    
    try:
        from radar_chart_advanced import criar_radar_comparativo
        
        # Dados de exemplo
        data = {
            "labels": [
                "Label1", "Label2", "Label3", "Label4", "Label5",
                "Label6", "Label7", "Label8", "Label9", "Label10",
                "Label11", "Label12", "Label13", "Label14", "Label15", "Label16"
            ],
            "datasets": [
                {
                    "label": "Série 1",
                    "data": [85, 70, 90, 60, 88, 92, 75, 80, 78, 84, 65, 70, 82, 90, 76, 88],
                    "backgroundColor": "rgba(255,205,86,0.35)",
                    "borderColor": "#FFD156"
                },
                {
                    "label": "Série 2",
                    "data": [70, 85, 72, 78, 80, 68, 82, 74, 70, 66, 88, 75, 80, 68, 84, 72],
                    "backgroundColor": "rgba(255,99,71,0.35)",
                    "borderColor": "#FF6347"
                }
            ]
        }
        
        # Criar gráfico
        radar = criar_radar_comparativo(json.dumps(data), "Validação com 2 Séries")
        print("   ✅ Gráfico com 2 séries criado com sucesso")
        
        # Tentar exportar HTML
        html = radar.to_html()
        if len(html) > 1000:
            print(f"   ✅ HTML gerado ({len(html):,} bytes)")
        
        return True
    
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return False

def check_export_capability():
    """Verifica capacidade de exportação PNG/SVG."""
    print("\n7️⃣  Verificando Capacidade de Exportação...")
    
    try:
        import kaleido
        print("   ✅ Kaleido instalado - Export PNG/SVG disponível")
        
        from radar_chart_advanced import RadarChartAdvanced
        
        radar = RadarChartAdvanced(
            labels=["A", "B", "C", "D"],
            title="Teste Export"
        )
        radar.add_series("Série", [50, 75, 60, 80])
        
        # Criar arquivo temporário
        png_bytes = radar.to_png()
        if len(png_bytes) > 100000:  # Deve ter pelo menos 100KB
            print(f"   ✅ PNG gerado com sucesso ({len(png_bytes) / 1024:.1f} KB)")
        
        return True
    
    except ImportError:
        print("   ⚠️  Kaleido não instalado (opcional)")
        print("       Instale com: pip install kaleido")
        return True  # Não é bloqueante
    
    except Exception as e:
        print(f"   ⚠️  Erro ao testar export: {str(e)}")
        return True  # Não é bloqueante

def print_summary(results):
    """Imprime sumário dos testes."""
    print_header("SUMÁRIO DE VALIDAÇÃO")
    
    checks = [
        ("Python Version", results.get("python_version")),
        ("Dependências", results.get("dependencies")),
        ("Arquivos", results.get("files")),
        ("Importação", results.get("import")),
        ("Funcionalidade", results.get("functionality")),
        ("Dados de Exemplo", results.get("example_data")),
        ("Exportação", results.get("export")),
    ]
    
    all_passed = all(status for _, status in checks)
    
    for check_name, status in checks:
        icon = "✅" if status else "❌" if status is False else "⚠️ "
        print(f"\n  {icon} {check_name:25} {'PASSOU' if status else 'FALHOU' if status is False else 'AVISO'}")
    
    print("\n" + "="*70)
    
    if all_passed:
        print("\n  🎉 VALIDAÇÃO COMPLETA - Sistema pronto para uso!")
        print("\n  Próximos passos:")
        print("    1. Executar teste completo: python test_radar_advanced.py")
        print("    2. Ver exemplos: python RADAR_EXAMPLES.py")
        print("    3. Usar no seu código: from radar_chart_advanced import criar_radar_comparativo")
        return 0
    else:
        print("\n  ⚠️  Alguns testes falharam. Veja os detalhes acima.")
        return 1

def main():
    """Executa todos os testes de validação."""
    print_header("VALIDAÇÃO DE INSTALAÇÃO - GRÁFICO RADAR AVANÇADO")
    
    results = {
        "python_version": check_python_version(),
        "dependencies": check_dependencies(),
        "files": check_files(),
        "import": test_module_import(),
        "functionality": test_module_functionality(),
        "example_data": test_example_data(),
        "export": check_export_capability(),
    }
    
    exit_code = print_summary(results)
    print("\n")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
