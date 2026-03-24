#!/usr/bin/env python
"""Run AB-00 with lazy extraction and file logging."""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# Enable lazy extraction BEFORE importing anything else
os.environ["USE_LAZY_EXTRACTION"] = "true"

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Setup file logging
log_dir = Path("notebooks/ablation/ablation_results/logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"ab00_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure logging to both file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
logger.info(f"Logging to: {log_file}")
logger.info("=" * 70)
logger.info("AB-00 ABLATION STUDY - LAZY EXTRACTION MODE")
logger.info("=" * 70)

try:
    from src.evaluation.ablation_runner import run_ablation

    logger.info("Configuration:")
    logger.info("  - Lazy extraction: ENABLED (bypasses LM Studio)")
    logger.info("  - Debug trace: ENABLED")
    logger.info("  - Dataset: 01_basics_ecommerce")
    logger.info("  - RAGAS: ENABLED")
    logger.info("")

    # Run AB-00 with debug trace
    metrics = run_ablation(
        experiment_id="AB-00",
        dataset_path=Path("tests/fixtures/01_basics_ecommerce/gold_standard_simple.json"),
        run_ragas=True,
        debug_trace=True,
    )

    logger.info("")
    logger.info("=" * 70)
    logger.info("RESULTS SUMMARY")
    logger.info("=" * 70)
    for key, value in metrics.items():
        if isinstance(value, float):
            logger.info(f"  {key}: {value:.4f}")
        else:
            logger.info(f"  {key}: {value}")

    logger.info("")
    logger.info(f"Full log saved to: {log_file}")

except Exception as e:
    logger.error(f"Error during AB-00 run: {e}", exc_info=True)
    sys.exit(1)
