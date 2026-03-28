#!/usr/bin/env python3
"""
🚀 AUTO SYNC - Scout Report Pro
Script de sincronização automática com GitHub

Uso:
    python auto_sync.py          # Sincronizar com intervalo 60s
    python auto_sync.py --once   # Sincronizar uma vez e sair
    python auto_sync.py --interval 30  # Sincronizar a cada 30s
"""

import os
import sys
import time
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional


class Colors:
    """Cores para output no terminal"""
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color


class GitAutoSync:
    """Gerenciador de sincronização automática com GitHub"""
    
    def __init__(self, repo_path: str = "/workspaces/scoutreportapp", 
                 branch: str = "main", remote: str = "origin"):
        self.repo_path = Path(repo_path)
        self.branch = branch
        self.remote = remote
        
        if not self.repo_path.exists():
            self.log_error(f"Repositório não encontrado: {repo_path}")
            sys.exit(1)
    
    def log_info(self, message: str) -> None:
        """Log informativo"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{Colors.BLUE}[INFO]{Colors.NC} {timestamp} - {message}")
    
    def log_success(self, message: str) -> None:
        """Log de sucesso"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{Colors.GREEN}[✅]{Colors.NC} {timestamp} - {message}")
    
    def log_warning(self, message: str) -> None:
        """Log de aviso"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{Colors.YELLOW}[⚠️]{Colors.NC} {timestamp} - {message}")
    
    def log_error(self, message: str) -> None:
        """Log de erro"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{Colors.RED}[❌]{Colors.NC} {timestamp} - {message}")
    
    def run_git_command(self, command: str) -> Tuple[int, str, str]:
        """Executar comando git e retornar código, stdout, stderr"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            self.log_error("Timeout ao executar comando git")
            return 1, "", "Timeout"
    
    def has_changes(self) -> bool:
        """Verificar se há mudanças para commit"""
        returncode, _, _ = self.run_git_command("git diff-index --quiet HEAD --")
        return returncode != 0
    
    def count_changes(self) -> int:
        """Contar número de arquivos com mudanças"""
        returncode, stdout, _ = self.run_git_command("git status --short")
        if returncode == 0:
            return len(stdout.strip().split('\n')) if stdout.strip() else 0
        return 0
    
    def add_all_changes(self) -> bool:
        """Adicionar todos os arquivos modificados"""
        returncode, _, stderr = self.run_git_command("git add -A")
        if returncode != 0:
            self.log_error(f"Falha ao adicionar arquivos: {stderr}")
            return False
        return True
    
    def commit_changes(self, message: str) -> bool:
        """Fazer commit das mudanças"""
        returncode, _, stderr = self.run_git_command(f'git commit -m "{message}"')
        if returncode != 0:
            if "nothing to commit" in stderr or "nothing to commit" in str(returncode):
                return True  # Nenhuma mudança é ok
            self.log_error(f"Falha ao fazer commit: {stderr}")
            return False
        self.log_success(f"Commit criado: {message}")
        return True
    
    def push_changes(self) -> bool:
        """Fazer push das mudanças"""
        returncode, _, stderr = self.run_git_command(
            f"git push {self.remote} {self.branch}"
        )
        
        if returncode != 0:
            self.log_warning(f"Push falhou: {stderr}")
            self.log_info("Tentando pull com rebase...")
            
            # Tentar pull com rebase
            returncode, _, stderr = self.run_git_command(
                f"git pull --rebase {self.remote} {self.branch}"
            )
            if returncode != 0:
                self.log_error(f"Rebase falhou: {stderr}")
                return False
            
            # Tentar push novamente
            returncode, _, stderr = self.run_git_command(
                f"git push {self.remote} {self.branch}"
            )
            if returncode != 0:
                self.log_error(f"Push após rebase falhou: {stderr}")
                return False
            
            self.log_success("Push realizado após rebase")
        else:
            self.log_success(f"Push para {self.remote}/{self.branch} realizado")
        
        return True
    
    def sync(self) -> bool:
        """Sincronizar mudanças com GitHub"""
        self.log_info("Verificando mudanças...")
        
        if not self.has_changes():
            self.log_info("Nenhuma mudança detectada")
            return True
        
        # Contar mudanças
        changes_count = self.count_changes()
        self.log_warning(f"Detectadas {changes_count} mudanças")
        
        # Adicionar mudanças
        if not self.add_all_changes():
            return False
        
        # Criar mensagem de commit
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_msg = f"🔄 Sincronização automática - {timestamp}"
        
        # Fazer commit
        if not self.commit_changes(commit_msg):
            return False
        
        # Fazer push
        if not self.push_changes():
            return False
        
        self.log_info("GitHub Actions iniciará testes automaticamente...")
        self.log_info("Streamlit Cloud fará deploy se os testes passarem...")
        return True
    
    def watch(self, interval: int = 60) -> None:
        """Monitorar e sincronizar continuamente"""
        self.log_info(f"Iniciando monitor de sincronização (intervalo: {interval}s)")
        self.log_info(f"Repositório: {self.repo_path}")
        self.log_info(f"Branch: {self.branch}")
        self.log_info("Pressione CTRL+C para parar")
        print()
        
        iteration = 1
        
        try:
            while True:
                try:
                    print(f"{Colors.YELLOW}═{'═' * 58}{Colors.NC}")
                    self.log_info(f"Ciclo #{iteration} de sincronização")
                    self.sync()
                    print(f"{Colors.YELLOW}═{'═' * 58}{Colors.NC}")
                    self.log_info(f"Próxima verificação em {interval} segundos...")
                    print()
                    
                    time.sleep(interval)
                    iteration += 1
                    
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    self.log_error(f"Erro durante sincronização: {str(e)}")
                    time.sleep(5)
        
        except KeyboardInterrupt:
            print()
            self.log_warning("Sincronização automática parada pelo usuário")
            sys.exit(0)


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="🚀 Auto Sync - Scout Report Pro",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python auto_sync.py              # Sincronizar continuamente (60s)
  python auto_sync.py --once       # Sincronizar uma vez e sair
  python auto_sync.py --interval 30  # Sincronizar a cada 30 segundos
        """
    )
    parser.add_argument('--once', action='store_true',
                       help='Sincronizar uma vez e sair')
    parser.add_argument('--interval', type=int, default=60,
                       help='Intervalo entre sincronizações (segundos)')
    parser.add_argument('--repo', type=str, default='/workspaces/scoutreportapp',
                       help='Caminho do repositório')
    
    args = parser.parse_args()
    
    # Mostrar banner
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         🚀 AUTO SYNC - Scout Report Pro                  ║")
    print("║                                                            ║")
    print("║  Sincronização automática com GitHub                     ║")
    print("║  GitHub Actions: Testes automáticos                      ║")
    print("║  Streamlit Cloud: Deploy automático se testes passarem  ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Criar sincronizador
    syncer = GitAutoSync(repo_path=args.repo)
    
    # Sincronizar
    if args.once:
        syncer.log_info("Sincronizando uma vez...")
        success = syncer.sync()
        sys.exit(0 if success else 1)
    else:
        syncer.watch(interval=args.interval)


if __name__ == "__main__":
    main()
