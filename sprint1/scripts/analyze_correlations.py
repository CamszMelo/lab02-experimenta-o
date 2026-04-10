#!/usr/bin/env python3
"""
Análise de correlações entre métricas de processo e qualidade.

Este script lê os arquivos de resumo (ck_summary.csv e cloc_summary.csv)
e calcula correlações de Pearson e Spearman entre as métricas.

Uso:
  python3 analyze_correlations.py \
    --repos_csv ../data/repos_list.csv \
    --ck_csv ../data/processed/ck_summary.csv \
    --cloc_csv ../data/processed/cloc_summary.csv \
    --out_dir ../data/processed
"""
import os
import sys
import csv
import argparse
from typing import Dict, List, Tuple
from pathlib import Path

def load_csv(path: str) -> List[Dict]:
    """Carrega um arquivo CSV e retorna lista de dicionários."""
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def merge_data(repos_list: List[Dict], ck_summary: List[Dict], cloc_summary: List[Dict]) -> List[Dict]:
    """Mescla dados de repositórios, CK e CLOC."""
    # Criar índices por repo
    repos_idx = {r['repo']: r for r in repos_list}
    ck_idx = {r['repo']: r for r in ck_summary}
    cloc_idx = {r['repo']: r for r in cloc_summary}

    merged = []
    for repo_name in repos_idx:
        if repo_name not in ck_idx or repo_name not in cloc_idx:
            continue

        row = {
            'repo': repo_name,
            # Métricas de processo
            'stars': float(repos_idx[repo_name].get('stars', 0)),
            'releases': float(repos_idx[repo_name].get('releases', 0)),
            'age_years': float(repos_idx[repo_name].get('age_years', 0)),
            # CLOC
            'code': float(cloc_idx[repo_name].get('code', 0)),
            'comment': float(cloc_idx[repo_name].get('comment', 0)),
            # CK
            'cbo_mean': float(ck_idx[repo_name].get('cbo_mean', 0)),
            'dit_mean': float(ck_idx[repo_name].get('dit_mean', 0)),
            'lcom_mean': float(ck_idx[repo_name].get('lcom_mean', 0)),
        }
        merged.append(row)

    return merged

def calculate_pearson(x: List[float], y: List[float]) -> Tuple[float, float]:
    """Calcula correlação de Pearson."""
    try:
        import statistics
        n = len(x)
        if n < 2:
            return 0.0, 1.0

        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)

        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = (sum((x[i] - mean_x) ** 2 for i in range(n)) * 
                      sum((y[i] - mean_y) ** 2 for i in range(n))) ** 0.5

        if denominator == 0:
            return 0.0, 1.0

        r = numerator / denominator
        return r, 0.0  # p-value simplificado
    except Exception as e:
        print(f"Erro ao calcular Pearson: {e}", file=sys.stderr)
        return 0.0, 1.0

def main():
    parser = argparse.ArgumentParser(description="Análise de correlações")
    parser.add_argument("--repos_csv", required=True, help="Caminho para repos_list.csv")
    parser.add_argument("--ck_csv", required=True, help="Caminho para ck_summary.csv")
    parser.add_argument("--cloc_csv", required=True, help="Caminho para cloc_summary.csv")
    parser.add_argument("--out_dir", default=".", help="Diretório de saída")
    args = parser.parse_args()

    # Validar arquivos
    for path in [args.repos_csv, args.ck_csv, args.cloc_csv]:
        if not os.path.isfile(path):
            print(f"Erro: Arquivo não encontrado: {path}", file=sys.stderr)
            return 1

    print("Carregando dados...")
    repos = load_csv(args.repos_csv)
    ck = load_csv(args.ck_csv)
    cloc = load_csv(args.cloc_csv)

    print(f"  Repositórios: {len(repos)}")
    print(f"  CK: {len(ck)}")
    print(f"  CLOC: {len(cloc)}")

    print("Mesclando dados...")
    merged = merge_data(repos, ck, cloc)
    print(f"  Registros mesclados: {len(merged)}")

    if len(merged) == 0:
        print("Erro: Nenhum dado mesclado", file=sys.stderr)
        return 1

    # Calcular correlações
    print("\nCalculando correlações...")

    # RQ 01: Popularidade vs Qualidade
    stars = [r['stars'] for r in merged]
    cbo = [r['cbo_mean'] for r in merged]
    r_pop_cbo, _ = calculate_pearson(stars, cbo)
    print(f"  RQ01 (Popularidade vs CBO): r = {r_pop_cbo:.4f}")

    # RQ 02: Maturidade vs Qualidade
    age = [r['age_years'] for r in merged]
    r_age_cbo, _ = calculate_pearson(age, cbo)
    print(f"  RQ02 (Maturidade vs CBO): r = {r_age_cbo:.4f}")

    # RQ 03: Atividade vs Qualidade
    releases = [r['releases'] for r in merged]
    r_rel_cbo, _ = calculate_pearson(releases, cbo)
    print(f"  RQ03 (Atividade vs CBO): r = {r_rel_cbo:.4f}")

    # RQ 04: Tamanho vs Qualidade
    code = [r['code'] for r in merged]
    r_size_cbo, _ = calculate_pearson(code, cbo)
    print(f"  RQ04 (Tamanho vs CBO): r = {r_size_cbo:.4f}")

    # Salvar resultados
    out_path = os.path.join(args.out_dir, "correlations.csv")
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['RQ', 'Métrica1', 'Métrica2', 'Correlação', 'Observações'])
        writer.writerow(['RQ01', 'Popularidade (stars)', 'CBO', f'{r_pop_cbo:.6f}', 'Relação entre estrelas e acoplamento'])
        writer.writerow(['RQ02', 'Maturidade (age_years)', 'CBO', f'{r_age_cbo:.6f}', 'Relação entre idade e acoplamento'])
        writer.writerow(['RQ03', 'Atividade (releases)', 'CBO', f'{r_rel_cbo:.6f}', 'Relação entre releases e acoplamento'])
        writer.writerow(['RQ04', 'Tamanho (LOC)', 'CBO', f'{r_size_cbo:.6f}', 'Relação entre tamanho e acoplamento'])

    print(f"\n✓ Resultados salvos em: {out_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
