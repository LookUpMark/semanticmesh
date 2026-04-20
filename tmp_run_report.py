import json
from pathlib import Path

d = json.loads(Path('outputs/ablation/AB-BEST/datasets/02_intermediate_finance/run.json').read_text())
q = d['query']
b = d['builder']
pq = d['per_question']

print('timestamp:', d['timestamp'])
print('run_tag:', d['run_tag'])
print()
print('=== BUILDER ===')
print('triplets:', b['triplets'])
print('entities:', b['entities'])
print('tables_parsed:', b['tables_parsed'])
print('tables_completed:', b['tables_completed'])
print('elapsed_s:', b['elapsed_s'])
print()
print('=== QUERY ===')
print('grounded_rate:', q['grounded_rate'])
print('avg_gt_coverage:', q['avg_gt_coverage'])
print('avg_top_score:', q['avg_top_score'])
print('abstained:', q['abstained_count'])
print('grounded_count:', q['grounded_count'], '/', q['total_questions'])
print()

for p in pq:
    print(f"{p['query_id']} | grounded={p['grounded']} | gt={p['gt_coverage']:.2f} | score={p['retrieval_quality_score']:.3f} | type={p['query_type']} | diff={p['difficulty']} | gate={p['retrieval_gate_decision']} | chunks={p['retrieval_chunk_count']} | grader_rej={p['grader_rejection_count']}")
