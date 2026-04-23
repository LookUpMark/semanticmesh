#!/usr/bin/env python3
"""Manual API integration test — KG Snapshots, Conversations, and all API endpoints.

Tests every endpoint against a live API server.

Usage:
    python scripts/test_api_features.py [--base-url http://127.0.0.1:8765]
"""
from __future__ import annotations

import json
import sys
import time
import uuid
from pathlib import Path

import requests

BASE_URL = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--base-url" else "http://127.0.0.1:8765"
API = f"{BASE_URL}/api/v1"

PASS_COUNT = 0
FAIL_COUNT = 0
WARN_COUNT = 0


def ok(name: str, detail: str = ""):
    global PASS_COUNT
    PASS_COUNT += 1
    print(f"  [PASS] {name}" + (f" — {detail}" if detail else ""))


def fail(name: str, detail: str = ""):
    global FAIL_COUNT
    FAIL_COUNT += 1
    print(f"  [FAIL] {name}" + (f" — {detail}" if detail else ""))


def warn(name: str, detail: str = ""):
    global WARN_COUNT
    WARN_COUNT += 1
    print(f"  [WARN] {name}" + (f" — {detail}" if detail else ""))


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def get(path: str, **kwargs) -> requests.Response:
    return requests.get(f"{API}{path}", timeout=30, **kwargs)


def post(path: str, json_data=None, **kwargs) -> requests.Response:
    return requests.post(f"{API}{path}", json=json_data, timeout=60, **kwargs)


def patch(path: str, json_data=None, **kwargs) -> requests.Response:
    return requests.patch(f"{API}{path}", json=json_data, timeout=30, **kwargs)


def delete(path: str, **kwargs) -> requests.Response:
    return requests.delete(f"{API}{path}", timeout=30, **kwargs)


# ═══════════════════════════════════════════════════════════════════════
# 1. HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════

def test_health():
    section("1. HEALTH CHECK")
    r = requests.get(f"{BASE_URL}/health", timeout=10)
    if r.status_code == 200 and r.json().get("status") == "ok":
        ok("GET /health", f"status={r.json()}")
    else:
        fail("GET /health", f"status_code={r.status_code} body={r.text[:200]}")


# ═══════════════════════════════════════════════════════════════════════
# 2. CONFIG ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════

def test_config():
    section("2. CONFIG ENDPOINTS")

    # GET config
    r = get("/config")
    if r.status_code == 200 and isinstance(r.json(), dict):
        ok("GET /config", f"keys={len(r.json())}")
    else:
        fail("GET /config", f"status={r.status_code}")

    # POST config — apply a harmless override
    r = post("/config", {"overrides": {"LOG_LEVEL": "INFO"}})
    if r.status_code == 200:
        body = r.json()
        if "applied" in body:
            ok("POST /config (harmless override)", f"applied={body.get('applied')}")
        else:
            warn("POST /config", f"unexpected body: {body}")
    else:
        fail("POST /config", f"status={r.status_code} body={r.text[:200]}")

    # POST config — blocked sensitive key
    r = post("/config", {"overrides": {"OPENROUTER_API_KEY": "hacked"}})
    if r.status_code == 200:
        body = r.json()
        blocked = body.get("blocked", [])
        if "OPENROUTER_API_KEY" in blocked:
            ok("POST /config (sensitive key blocked)", f"blocked={blocked}")
        else:
            fail("POST /config sensitive block", f"key not in blocked: {body}")
    else:
        # Some implementations may reject with 400/422
        if r.status_code in (400, 422):
            ok("POST /config (sensitive key rejected)", f"status={r.status_code}")
        else:
            fail("POST /config sensitive", f"status={r.status_code}")


# ═══════════════════════════════════════════════════════════════════════
# 3. GRAPH STATS & DATA
# ═══════════════════════════════════════════════════════════════════════

def test_graph_endpoints():
    section("3. GRAPH STATS & DATA")

    # Graph stats
    r = get("/demo/graph/stats")
    if r.status_code == 200:
        body = r.json()
        ok("GET /demo/graph/stats", f"nodes={body.get('total_nodes', '?')} edges={body.get('total_edges', '?')}")
    else:
        fail("GET /demo/graph/stats", f"status={r.status_code}")

    # Graph data (for vis-network)
    r = get("/demo/graph/data")
    if r.status_code == 200:
        body = r.json()
        n = len(body.get("nodes", []))
        e = len(body.get("edges", []))
        ok("GET /demo/graph/data", f"nodes={n} edges={e}")
    else:
        fail("GET /demo/graph/data", f"status={r.status_code}")


# ═══════════════════════════════════════════════════════════════════════
# 4. KG SNAPSHOTS — Full CRUD Cycle
# ═══════════════════════════════════════════════════════════════════════

def test_kg_snapshots() -> str | None:
    section("4. KG SNAPSHOTS — CRUD Cycle")
    snapshot_id = None

    # 4a. List snapshots (initial)
    r = get("/demo/kg/snapshots")
    if r.status_code == 200:
        snapshots = r.json()
        ok("GET /demo/kg/snapshots (list)", f"count={len(snapshots)}")
    else:
        fail("GET /demo/kg/snapshots", f"status={r.status_code}")
        return None

    # 4b. Save current KG as snapshot
    test_name = f"test-snapshot-{uuid.uuid4().hex[:8]}"
    r = post("/demo/kg/snapshots", {"name": test_name, "description": "Automated test snapshot"})
    if r.status_code == 200:
        body = r.json()
        snapshot_id = body.get("id")
        ok("POST /demo/kg/snapshots (save)", f"id={snapshot_id} name={body.get('name')}")
    elif r.status_code == 409:
        warn("POST /demo/kg/snapshots", "409 — empty graph? Trying anyway")
    else:
        fail("POST /demo/kg/snapshots (save)", f"status={r.status_code} body={r.text[:200]}")
        return None

    if not snapshot_id:
        warn("KG Snapshot", "No snapshot created — graph may be empty. Skipping load/rename/delete tests.")
        return None

    # 4c. List again — should include new snapshot
    r = get("/demo/kg/snapshots")
    if r.status_code == 200:
        ids = [s["id"] for s in r.json()]
        if snapshot_id in ids:
            ok("Snapshot appears in list", f"id={snapshot_id}")
        else:
            fail("Snapshot NOT in list", f"id={snapshot_id} list_ids={ids}")
    else:
        fail("GET /demo/kg/snapshots (re-list)", f"status={r.status_code}")

    # 4d. Get active snapshot
    r = get("/demo/kg/snapshots/active")
    if r.status_code == 200:
        active = r.json()
        ok("GET /demo/kg/snapshots/active", f"active={active}")
    elif r.status_code == 404:
        ok("GET /demo/kg/snapshots/active", "no active snapshot (expected if save doesn't auto-activate)")
    else:
        fail("GET /demo/kg/snapshots/active", f"status={r.status_code}")

    # 4e. Load the snapshot (clears Neo4j, restores)
    r = post(f"/demo/kg/snapshots/{snapshot_id}/load")
    if r.status_code == 200:
        body = r.json()
        ok("POST /demo/kg/snapshots/{id}/load", f"loaded: {body}")
    else:
        fail("POST /demo/kg/snapshots/{id}/load", f"status={r.status_code} body={r.text[:300]}")

    # 4f. Verify active snapshot is now set
    r = get("/demo/kg/snapshots/active")
    if r.status_code == 200:
        active = r.json()
        if active and active.get("id") == snapshot_id:
            ok("Active snapshot matches loaded", f"id={active.get('id')}")
        else:
            fail("Active snapshot mismatch", f"expected={snapshot_id} got={active}")
    else:
        fail("GET /demo/kg/snapshots/active after load", f"status={r.status_code}")

    # 4g. Verify graph stats after load (should have nodes)
    r = get("/demo/graph/stats")
    if r.status_code == 200:
        body = r.json()
        total = body.get("total_nodes", 0)
        if total > 0:
            ok("Graph has data after snapshot load", f"total_nodes={total}")
        else:
            warn("Graph empty after snapshot load", "snapshot might have been saved from empty graph")
    else:
        fail("GET /demo/graph/stats after load", f"status={r.status_code}")

    # 4h. Rename snapshot
    new_name = f"renamed-{uuid.uuid4().hex[:6]}"
    r = patch(f"/demo/kg/snapshots/{snapshot_id}", {"name": new_name, "description": "Updated description"})
    if r.status_code == 200:
        body = r.json()
        if body.get("name") == new_name:
            ok("PATCH /demo/kg/snapshots/{id} (rename)", f"new_name={new_name}")
        else:
            fail("Rename name mismatch", f"expected={new_name} got={body.get('name')}")
    else:
        fail("PATCH /demo/kg/snapshots/{id}", f"status={r.status_code}")

    # 4i. Eject active snapshot (clear pointer, keep data)
    r = post("/demo/kg/snapshots/eject")
    if r.status_code == 200:
        ok("POST /demo/kg/snapshots/eject", "active pointer cleared")
    else:
        fail("POST /demo/kg/snapshots/eject", f"status={r.status_code}")

    # 4j. Verify no active snapshot
    r = get("/demo/kg/snapshots/active")
    if r.status_code == 200:
        active = r.json()
        if active is None or active == {}:
            ok("No active snapshot after eject", "as expected")
        elif active.get("id") is None:
            ok("No active snapshot after eject", f"response={active}")
        else:
            fail("Still has active after eject", f"active={active}")
    elif r.status_code == 404:
        ok("No active after eject (404)", "expected")
    else:
        fail("GET active after eject", f"status={r.status_code}")

    # 4k. Delete the test snapshot
    r = delete(f"/demo/kg/snapshots/{snapshot_id}")
    if r.status_code == 200:
        ok("DELETE /demo/kg/snapshots/{id}", f"deleted={snapshot_id}")
    else:
        fail("DELETE /demo/kg/snapshots/{id}", f"status={r.status_code}")

    # 4l. Verify deleted
    r = get("/demo/kg/snapshots")
    if r.status_code == 200:
        ids = [s["id"] for s in r.json()]
        if snapshot_id not in ids:
            ok("Snapshot removed from list after delete", f"remaining={len(ids)}")
        else:
            fail("Snapshot STILL in list after delete", f"id={snapshot_id}")
    else:
        fail("GET /demo/kg/snapshots (post-delete)", f"status={r.status_code}")

    return snapshot_id


# ═══════════════════════════════════════════════════════════════════════
# 5. CONVERSATIONS — Full CRUD Cycle
# ═══════════════════════════════════════════════════════════════════════

def test_conversations():
    section("5. CONVERSATIONS — CRUD Cycle")
    conv_id = None

    # 5a. List conversations (initial)
    r = get("/demo/conversations")
    if r.status_code == 200:
        convs = r.json()
        ok("GET /demo/conversations (list)", f"count={len(convs)}")
    else:
        fail("GET /demo/conversations", f"status={r.status_code}")

    # 5b. Save a new conversation
    session_id = f"test-session-{uuid.uuid4().hex[:8]}"
    messages = [
        {"role": "user", "content": "What tables map to the Customer concept?"},
        {"role": "assistant", "content": "The CUSTOMER_MASTER table maps to the Customer concept with confidence 0.87.", "metadata": {"sources": ["CUSTOMER_MASTER"]}},
        {"role": "user", "content": "What about products?"},
        {"role": "assistant", "content": "TB_PRODUCT maps to the Product concept.", "metadata": {"sources": ["TB_PRODUCT"]}},
    ]
    r = post("/demo/conversations", {
        "session_id": session_id,
        "title": "Test conversation — API integration test",
        "messages": messages,
        "active_snapshot_id": None,
    })
    if r.status_code == 200:
        body = r.json()
        conv_id = body.get("id")
        ok("POST /demo/conversations (save)", f"id={conv_id} title={body.get('title')}")
    else:
        fail("POST /demo/conversations (save)", f"status={r.status_code} body={r.text[:300]}")
        return

    # 5c. List again — should include new conversation
    r = get("/demo/conversations")
    if r.status_code == 200:
        ids = [c["id"] for c in r.json()]
        if conv_id in ids:
            ok("Conversation appears in list", f"id={conv_id}")
        else:
            fail("Conversation NOT in list", f"id={conv_id}")
    else:
        fail("GET /demo/conversations (re-list)", f"status={r.status_code}")

    # 5d. Get full conversation (with messages)
    r = get(f"/demo/conversations/{conv_id}")
    if r.status_code == 200:
        body = r.json()
        msg_count = len(body.get("messages", []))
        if msg_count == 4:
            ok("GET /demo/conversations/{id} (detail)", f"messages={msg_count}")
        else:
            fail("Message count mismatch", f"expected=4 got={msg_count}")

        # Verify message content preserved
        msgs = body.get("messages", [])
        if msgs and msgs[0].get("content") == "What tables map to the Customer concept?":
            ok("Message content preserved", "first message matches")
        else:
            fail("Message content corrupted", f"first msg={msgs[0] if msgs else 'empty'}")

        # Verify metadata preserved
        if msgs and len(msgs) > 1:
            meta = msgs[1].get("metadata")
            if meta and meta.get("sources") == ["CUSTOMER_MASTER"]:
                ok("Message metadata preserved", f"sources={meta.get('sources')}")
            else:
                fail("Message metadata lost or corrupted", f"metadata={meta}")
    else:
        fail("GET /demo/conversations/{id}", f"status={r.status_code}")

    # 5e. Rename conversation
    new_title = "Renamed — API test conversation"
    r = patch(f"/demo/conversations/{conv_id}", {"title": new_title})
    if r.status_code == 200:
        body = r.json()
        if body.get("title") == new_title:
            ok("PATCH /demo/conversations/{id} (rename)", f"title={new_title}")
        else:
            fail("Rename title mismatch", f"expected={new_title} got={body.get('title')}")
    else:
        fail("PATCH /demo/conversations/{id}", f"status={r.status_code}")

    # 5f. Save a SECOND conversation (test multi-conversation listing)
    session_id_2 = f"test-session-{uuid.uuid4().hex[:8]}"
    r = post("/demo/conversations", {
        "session_id": session_id_2,
        "title": "Second test conversation",
        "messages": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ],
    })
    conv_id_2 = None
    if r.status_code == 200:
        conv_id_2 = r.json().get("id")
        ok("POST second conversation", f"id={conv_id_2}")
    else:
        fail("POST second conversation", f"status={r.status_code}")

    # 5g. List — verify ordering (newest first)
    r = get("/demo/conversations")
    if r.status_code == 200:
        convs = r.json()
        if len(convs) >= 2:
            # Newest should be first
            first_id = convs[0].get("id")
            if first_id == conv_id_2:
                ok("Conversations ordered by updated_at DESC", f"newest first: {first_id}")
            else:
                warn("Ordering unclear", f"first={first_id} expected={conv_id_2}")
        ok(f"Multiple conversations listed", f"count={len(convs)}")
    else:
        fail("GET /demo/conversations", f"status={r.status_code}")

    # 5h. Delete both test conversations
    for cid in [conv_id, conv_id_2]:
        if cid:
            r = delete(f"/demo/conversations/{cid}")
            if r.status_code == 200:
                ok(f"DELETE conversation {cid[:12]}...", "deleted")
            else:
                fail(f"DELETE conversation {cid[:12]}...", f"status={r.status_code}")

    # 5i. Verify both deleted
    r = get("/demo/conversations")
    if r.status_code == 200:
        ids = [c["id"] for c in r.json()]
        remaining = [cid for cid in [conv_id, conv_id_2] if cid and cid in ids]
        if not remaining:
            ok("All test conversations cleaned up", f"total remaining: {len(ids)}")
        else:
            fail("Some test conversations still present", f"ids={remaining}")


# ═══════════════════════════════════════════════════════════════════════
# 6. DEMO BUILD & QUERY
# ═══════════════════════════════════════════════════════════════════════

def test_demo_build_query():
    section("6. DEMO BUILD & QUERY")

    # 6a. List jobs
    r = get("/demo/jobs")
    if r.status_code == 200:
        ok("GET /demo/jobs", f"count={len(r.json())}")
    else:
        fail("GET /demo/jobs", f"status={r.status_code}")

    # 6b. Start a build (with test fixtures, lazy extraction for speed)
    fixtures = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "01_basics_ecommerce"
    docs = [str(fixtures / "business_glossary.txt"), str(fixtures / "data_dictionary.txt")]
    ddls = [str(fixtures / "schema.sql")]

    r = post("/demo/build", {
        "doc_paths": docs,
        "ddl_paths": ddls,
        "clear_graph": True,
        "lazy_extraction": True,
    })
    if r.status_code == 200:
        body = r.json()
        job_id = body.get("job_id")
        ok("POST /demo/build", f"job_id={job_id}")
    else:
        fail("POST /demo/build", f"status={r.status_code} body={r.text[:300]}")
        return

    # 6c. Poll build status until done (max 5 minutes)
    max_wait = 300
    poll_interval = 5
    elapsed = 0
    final_status = None
    while elapsed < max_wait:
        time.sleep(poll_interval)
        elapsed += poll_interval
        r = get(f"/demo/build/{job_id}")
        if r.status_code == 200:
            body = r.json()
            status = body.get("status")
            step = body.get("current_step", "?")
            print(f"    ... [{elapsed}s] status={status} step={step}")
            if status in ("done", "failed"):
                final_status = status
                break
        else:
            fail(f"GET /demo/build/{job_id}", f"status={r.status_code}")
            break

    if final_status == "done":
        r = get(f"/demo/build/{job_id}")
        body = r.json()
        ok("Build completed", f"tables={body.get('tables_completed')} triplets={body.get('triplets_extracted')}")
    elif final_status == "failed":
        r = get(f"/demo/build/{job_id}")
        fail("Build failed", f"error={r.json().get('error', '?')[:200]}")
        return
    else:
        fail("Build timeout", f"elapsed={elapsed}s")
        return

    # 6d. Query the built graph
    r = post("/demo/query", {"question": "What table maps to the Customer concept?"})
    if r.status_code == 200:
        body = r.json()
        answer = body.get("answer", "")[:200]
        sources = body.get("sources", [])
        ok("POST /demo/query", f"answer_len={len(answer)} sources={sources}")
        if answer:
            ok("Query returned an answer", f"preview: {answer[:100]}...")
        else:
            warn("Query returned empty answer", "")
    else:
        fail("POST /demo/query", f"status={r.status_code} body={r.text[:300]}")


# ═══════════════════════════════════════════════════════════════════════
# 7. ABLATION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════

def test_ablation():
    section("7. ABLATION ENDPOINTS")

    # 7a. Get ablation matrix
    r = get("/ablation/matrix")
    if r.status_code == 200:
        matrix = r.json()
        ok("GET /ablation/matrix", f"studies={len(matrix)}")
    else:
        fail("GET /ablation/matrix", f"status={r.status_code}")

    # 7b. Get available datasets
    r = get("/ablation/datasets")
    if r.status_code == 200:
        datasets = r.json()
        ok("GET /ablation/datasets", f"datasets={len(datasets)}")
    else:
        fail("GET /ablation/datasets", f"status={r.status_code}")

    # 7c. List ablation jobs
    r = get("/ablation/jobs")
    if r.status_code == 200:
        ok("GET /ablation/jobs", f"count={len(r.json())}")
    else:
        fail("GET /ablation/jobs", f"status={r.status_code}")

    # 7d. Try to get an evaluation bundle (may or may not exist)
    r = get("/ablation/bundle/AB-00/01_basics_ecommerce")
    if r.status_code == 200:
        ok("GET /ablation/bundle/AB-00/01_basics_ecommerce", "bundle exists")
    elif r.status_code == 404:
        ok("GET /ablation/bundle (404)", "no bundle yet — expected for fresh install")
    else:
        fail("GET /ablation/bundle", f"status={r.status_code}")

    # 7e. Try to get AI Judge payload
    r = get("/ablation/evaluate/AB-00/01_basics_ecommerce")
    if r.status_code == 200:
        ok("GET /ablation/evaluate/AB-00/01_basics_ecommerce", "AI Judge payload available")
    elif r.status_code == 404:
        ok("GET /ablation/evaluate (404)", "no bundle — expected")
    else:
        fail("GET /ablation/evaluate", f"status={r.status_code}")


# ═══════════════════════════════════════════════════════════════════════
# 8. KG SNAPSHOT ROUND-TRIP (save → clear → load → verify)
# ═══════════════════════════════════════════════════════════════════════

def test_kg_snapshot_roundtrip():
    section("8. KG SNAPSHOT ROUND-TRIP (save → clear → load → verify)")

    # Get initial graph stats
    r = get("/demo/graph/stats")
    if r.status_code != 200:
        fail("Can't get initial stats", f"status={r.status_code}")
        return
    initial_stats = r.json()
    initial_nodes = initial_stats.get("total_nodes", 0)
    if initial_nodes == 0:
        warn("Graph is empty — can't test round-trip meaningfully", "skipping")
        return

    ok(f"Initial graph has data", f"nodes={initial_nodes}")

    # Save snapshot
    snap_name = f"roundtrip-test-{uuid.uuid4().hex[:6]}"
    r = post("/demo/kg/snapshots", {"name": snap_name, "description": "Round-trip test"})
    if r.status_code != 200:
        fail("Save snapshot for round-trip", f"status={r.status_code}")
        return
    snap_id = r.json()["id"]
    ok("Saved snapshot for round-trip", f"id={snap_id}")

    # Clear the graph
    r = requests.delete(f"{API}/demo/graph", params={"confirm": "true"}, timeout=30)
    if r.status_code == 200:
        ok("Graph cleared", "DETACH DELETE all")
    else:
        fail("Clear graph", f"status={r.status_code}")
        return

    # Verify graph is empty
    r = get("/demo/graph/stats")
    if r.status_code == 200:
        post_clear = r.json().get("total_nodes", -1)
        if post_clear == 0:
            ok("Graph confirmed empty after clear", f"nodes={post_clear}")
        else:
            fail("Graph not empty after clear", f"nodes={post_clear}")
    else:
        fail("Stats after clear", f"status={r.status_code}")

    # Load snapshot back
    r = post(f"/demo/kg/snapshots/{snap_id}/load")
    if r.status_code == 200:
        ok("Snapshot loaded", f"response={r.json()}")
    else:
        fail("Load snapshot", f"status={r.status_code} body={r.text[:300]}")
        return

    # Verify graph restored
    r = get("/demo/graph/stats")
    if r.status_code == 200:
        restored_stats = r.json()
        restored_nodes = restored_stats.get("total_nodes", 0)
        if restored_nodes == initial_nodes:
            ok("Node count fully restored", f"initial={initial_nodes} restored={restored_nodes}")
        elif restored_nodes > 0:
            # Slight differences possible due to embedding regeneration nodes, etc.
            diff_pct = abs(restored_nodes - initial_nodes) / max(initial_nodes, 1) * 100
            if diff_pct < 10:
                ok(f"Node count ~restored (within 10%)", f"initial={initial_nodes} restored={restored_nodes} diff={diff_pct:.1f}%")
            else:
                fail(f"Significant node count difference", f"initial={initial_nodes} restored={restored_nodes} diff={diff_pct:.1f}%")
        else:
            fail("Graph still empty after load", f"restored_nodes={restored_nodes}")
    else:
        fail("Stats after load", f"status={r.status_code}")

    # Verify data integrity — check specific node types
    r = get("/demo/graph/stats")
    if r.status_code == 200:
        stats = r.json()
        node_counts = stats.get("node_counts", stats.get("nodes", {}))
        print(f"    Restored node counts: {node_counts}")
        edge_counts = stats.get("edge_counts", stats.get("edges", {}))
        print(f"    Restored edge counts: {edge_counts}")

    # Clean up: delete test snapshot
    r = delete(f"/demo/kg/snapshots/{snap_id}")
    if r.status_code == 200:
        ok("Cleaned up round-trip snapshot", f"deleted {snap_id}")
    else:
        warn("Cleanup failed", f"status={r.status_code}")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  COMPREHENSIVE API & FEATURE TEST SUITE")
    print(f"  Target: {BASE_URL}")
    print("=" * 60)

    test_health()
    test_config()
    test_graph_endpoints()
    test_kg_snapshots()
    test_conversations()
    test_demo_build_query()
    test_ablation()
    test_kg_snapshot_roundtrip()

    section("SUMMARY")
    print(f"  PASS: {PASS_COUNT}")
    print(f"  FAIL: {FAIL_COUNT}")
    print(f"  WARN: {WARN_COUNT}")
    print(f"  Total assertions: {PASS_COUNT + FAIL_COUNT + WARN_COUNT}")
    if FAIL_COUNT == 0:
        print("\n  ✅ ALL TESTS PASSED")
    else:
        print(f"\n  ❌ {FAIL_COUNT} FAILURE(S) DETECTED")


if __name__ == "__main__":
    main()
