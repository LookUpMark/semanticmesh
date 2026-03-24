#!/usr/bin/env python
"""Quick analysis of AB-00 trace and manual query testing."""

import json
from pathlib import Path
from src.graph.neo4j_client import Neo4jClient
from src.generation.query_graph import run_query

# Load builder trace
trace_file = Path('notebooks/ablation/ablation_results/traces/debug/builder_trace_AB-00.2026-03-24T17-25-18.338090+00-00.json')
with open(trace_file) as f:
    trace = json.load(f)

print('=' * 70)
print('🔬 AB-00 BUILDER TRACE ANALYSIS')
print('=' * 70)
print()

print('📋 CONFIGURAZIONE:')
config = trace['config']
for k, v in config.items():
    print(f'  {k}: {v}')
print()

print('📦 CHUNKING:')
chunking = trace['chunking_summary']
print(f'  Total chunks: {chunking["total_chunks"]}')
print(f'  Total tokens: {chunking["total_tokens"]}')
print(f'  Avg tokens/chunk: {chunking["avg_tokens"]:.1f}')
print(f'  Chunk size: {config["chunk_size"]}, Overlap: {config["chunk_overlap"]}')
print()

print('📝 CHUNKS (primi 3):')
for i, chunk in enumerate(trace['chunks'][:3]):
    cid = chunk['chunk_id']
    source = chunk['source']
    tokens = chunk['token_count']
    text_preview = chunk['text'][:60] + '...' if len(chunk['text']) > 60 else chunk['text']
    print(f'  Chunk {cid}: {source}, {tokens} tokens')
    print(f'    Preview: {text_preview}')
print()

print('🗄️  NEO4J STATS:')
neo4j = trace.get('neo4j_summary', {})
print(f'  Total nodes: {neo4j.get("total_nodes", "N/A")}')
print(f'  Total relationships: {neo4j.get("total_relationships", "N/A")}')
print(f'  Completed tables: {neo4j.get("completed_tables", "N/A")}')
print()

# Check current Neo4j state
print('=' * 70)
print('🔍 NEO4J GRAPH STATE')
print('=' * 70)
print()

with Neo4jClient() as client:
    # Count nodes by type
    result = client.execute_cypher('''
        MATCH (n)
        RETURN labels(n)[0] as label, count(n) as count
        ORDER BY count DESC
    ''')
    print('📊 Nodes by type:')
    for row in result:
        label = row['label']
        count = row['count']
        print(f'  {label}: {count}')
    print()

    # Sample BusinessConcept nodes
    result = client.execute_cypher('''
        MATCH (n:BusinessConcept)
        RETURN n.name as name, n.definition as definition
        LIMIT 5
    ''')
    print('📝 Business Concepts (sample):')
    for row in result:
        name = row['name'][:50]
        definition = (row['definition'] or 'N/A')[:60] + '...'
        print(f'  - {name}')
        print(f'    {definition}')
    print()

    # Show relationships
    result = client.execute_cypher('''
        MATCH (a)-[r]->(b)
        RETURN labels(a)[0] as from_type, a.name as from_name, labels(b)[0] as to_type, b.name as to_name
        LIMIT 10
    ''')
    print('🔗 Relationships (sample):')
    for row in result:
        from_name = row['from_name'][:30]
        to_name = row['to_name'][:30]
        print(f'  {from_name} → {to_name}')
    print()

# Manual query testing with ground truth comparison
print('=' * 70)
print('🧪 MANUAL QUERY TESTING')
print('=' * 70)
print()

# Load ground truth
gt_file = Path('tests/fixtures/01_basics_ecommerce/gold_standard.json')
with open(gt_file) as f:
    gt_data = json.load(f)

# Test first 5 questions
test_questions = gt_data['pairs'][:5]

for i, qa in enumerate(test_questions, 1):
    question = qa['question']
    expected = qa['expected_answer']
    expected_sources = qa['expected_sources']

    print(f'Q{i}: {question}')
    print(f'   Expected: {expected[:100]}...')
    print(f'   Expected sources: {expected_sources}')

    # Run query
    try:
        result = run_query(
            question,
            trace_enabled=True,
            query_index=i,
            builder_trace_id='manual-test',
            study_id='manual-test'
        )
        answer = result['final_answer']
        contexts = result['retrieved_contexts']
        sources = result['sources']

        print(f'   Generated answer: {answer[:150]}...')
        print(f'   Retrieved {len(contexts)} contexts')
        print(f'   Sources: {sources[:5]}')

        # Check coverage
        covered = [s for s in expected_sources if any(s in src for src in sources)]
        missing = [s for s in expected_sources if s not in covered]

        if covered:
            print(f'   ✅ Covered sources: {covered}')
        if missing:
            print(f'   ❌ Missing sources: {missing}')

    except Exception as e:
        print(f'   ❌ ERROR: {e}')

    print()
