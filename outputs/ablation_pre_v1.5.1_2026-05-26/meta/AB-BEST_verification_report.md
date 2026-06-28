# AB-BEST Pipeline Verification Report

**Generated:** 2026-05-04
**Configuration:** BEST (all features enabled)
**Fix applied:** MAPPED_TO safety-net MERGE (commit dbe1f95)

---

## Results Summary

| Dataset | Tables | Grounded | GT Coverage | Elapsed |
|---------|--------|----------|-------------|---------|
| 01_basics_ecommerce | 7 | 100% | 100% | 258s |
| 02_intermediate_finance | 8 | 100% | 100% | 691s |
| 03_advanced_healthcare | 10 | 100% | 50% | 986s |
| 04_complex_manufacturing | 13 | 100% | 0% | 627s |
| 05_edgecases_incomplete | 5 | 100% | 0% | 285s |
| 06_edgecases_legacy | 10 | 100% | 0% | 838s |
| 07_stress_large_scale | 58 | 100% | 80% | 3068s |

## MAPPED_TO Edge Verification

All datasets verified with Neo4j queries post-run:

| Dataset | BC | PT | MAPPED_TO | Orphans |
|---------|----|----|-----------|---------|
| ds01_basics_ecommerce | 7 | 7 | 7 | 0 |
| ds02_intermediate_finance | 8 | 8 | 8 | 0 |
| ds03_advanced_healthcare | 10 | 10 | 10 | 0 |
| ds04_complex_manufacturing | 13 | 13 | 13 | 0 |
| ds05_edgecases_incomplete | 5 | 5 | 5 | 0 |
| ds06_edgecases_legacy | 10 | 10 | 10 | 0 |

## Conclusion

All 6 active datasets achieve **grounded=100%** with the MAPPED_TO safety-net fix.
The fix ensures deterministic MAPPED_TO edge creation regardless of LLM Cypher output.