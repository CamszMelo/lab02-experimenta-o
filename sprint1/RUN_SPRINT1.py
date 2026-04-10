#!/usr/bin/env python3
"""
Script de orquestração para Sprint 1 - Laboratório 02

Este script automatiza a execução completa da Sprint 1:
1. Verifica dependências (git, cloc, java)
2. Valida a lista de repositórios
3. Executa o processamento em streaming
4. Gera estatísticas resumidas

Uso:
  python3 RUN_SPRINT1.py --max 100 --workers 4
  python3 RUN_SPRINT1.py --max 1000 --workers 8
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_dependency(name, cmd=None):
    """Verifica se uma dependência está instalada."""
    if cmd is None:
        cmd = name
    try:
        result = subprocess.run([cmd, "--version"], capture_output=True, timeout=5)
        if result.returncode == 0:
            print(f"✓ {name} encontrado")
            return True
    except Exception:
        pass
    print(f"✗ {name} NÃO encontrado")
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Orquestrador da Sprint 1 - Análise de Qualidade de Repositórios Java"
    )
    parser.add_argument("--max", type=int, default=1000, help="Máximo de repositórios a processar (padrão: 1000)")
    parser.add_argument("--workers", type=int, default=4, help="Número de workers paralelos (padrão: 4)")
    parser.add_argument("--skip-deps", action="store_true", help="Pular verificação de dependências")
    parser.add_argument("--verbose", action="store_true", help="Modo verboso")
    args = parser.parse_args()

    # Diretórios
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"
    processed_dir = data_dir / "processed"
    work_dir = data_dir / "_stream_tmp"
    repos_csv = data_dir / "repos_list.csv"
    ck_jar = script_dir / "tools" / "ck" / "ck-0.7.0-jar-with-dependencies.jar"

    print("=" * 70)
    print("SPRINT 1 - Análise de Qualidade de Repositórios Java")
    print("=" * 70)

    # Verificar dependências
    if not args.skip_deps:
        print("\n[1/3] Verificando dependências...")
        deps_ok = all([
            check_dependency("git"),
            check_dependency("cloc"),
            check_dependency("java"),
        ])
        if not deps_ok:
            print("\nERRO: Algumas dependências não foram encontradas.")
            print("No Ubuntu/Debian, instale com: sudo apt-get install git cloc default-jre")
            return 1

    # Validar arquivos
    print("\n[2/3] Validando arquivos...")
    if not repos_csv.exists():
        print(f"✗ Arquivo não encontrado: {repos_csv}")
        return 1
    print(f"✓ Lista de repositórios encontrada: {repos_csv}")

    if not ck_jar.exists():
        print(f"✗ JAR do CK não encontrado: {ck_jar}")
        return 1
    print(f"✓ CK JAR encontrado: {ck_jar}")

    # Criar diretórios
    processed_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    # Executar processamento
    print(f"\n[3/3] Processando {args.max} repositórios com {args.workers} worker(s)...")
    print("-" * 70)

    process_script_candidates = [
        script_dir / "scripts" / "process_streaming.py",
        script_dir / "sprint1" / "scripts" / "process_streaming.py",
    ]
    process_script = next((p for p in process_script_candidates if p.exists()), None)
    if process_script is None:
        print("✗ Script process_streaming.py não encontrado em nenhum dos caminhos esperados.")
        print("Procurado em:")
        for candidate in process_script_candidates:
            print(f"  - {candidate}")
        return 1

    cmd = [
        sys.executable,
        str(process_script),
        "--csv", str(repos_csv),
        "--work_dir", str(work_dir),
        "--out_dir", str(processed_dir),
        "--max", str(args.max),
        "--ck_jar", str(ck_jar),
        "--workers", str(args.workers),
    ]

    if args.verbose:
        cmd.append("--verbose")

    result = subprocess.run(cmd, cwd=str(script_dir))

    if result.returncode == 0:
        print("-" * 70)
        print("\n✓ Sprint 1 concluída com sucesso!")
        print(f"\nResultados salvos em:")
        print(f"  - {processed_dir / 'ck_summary.csv'}")
        print(f"  - {processed_dir / 'cloc_summary.csv'}")
        return 0
    else:
        print("\n✗ Erro durante o processamento")
        return 1

if __name__ == "__main__":
    sys.exit(main())
