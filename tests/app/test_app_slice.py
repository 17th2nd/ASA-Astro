"""App-layer tests for the ASA-Astro V1 thin slice (pin → snapshot → one Objective → receipt).

Runs against the real pinned kernel and the repository's own Astro engine; nothing is mocked.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

from app import pin as pinmod

ROOT = Path(__file__).resolve().parents[2]

try:
    PIN = pinmod.verify_pin()
    PIN_ERROR = None
except Exception as exc:  # pragma: no cover - environment without the materialised pin
    PIN, PIN_ERROR = None, str(exc)

NEEDS_PIN = unittest.skipIf(PIN is None, f"pinned ASA checkout not verified ({PIN_ERROR}); run "
                            "python3 tools/asa_baseline.py --config config/asa-baseline-current-dev.json")


def resolve_pointer(document, pointer: str):
    node = document
    if pointer in ("", "/"):
        return node
    for raw in pointer.lstrip("/").split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        node = node[int(token)] if isinstance(node, list) else node[token]
    return node


class _TempDataDir(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._old = os.environ.get("ASA_ASTRO_APP_DATA_DIR")
        os.environ["ASA_ASTRO_APP_DATA_DIR"] = self._tmp.name

    def tearDown(self):
        if self._old is None:
            os.environ.pop("ASA_ASTRO_APP_DATA_DIR", None)
        else:
            os.environ["ASA_ASTRO_APP_DATA_DIR"] = self._old
        self._tmp.cleanup()


class PinTests(unittest.TestCase):
    def test_pin_is_the_633f837a_current_dev_file(self):
        cfg = pinmod.app_config()
        self.assertEqual(cfg["asa_pin_file"], "config/asa-baseline-current-dev.json")
        record = pinmod.pin_record()
        self.assertRegex(record["sha"], r"^[0-9a-f]{40}$")
        self.assertNotIn(record["sha"], json.dumps(cfg), "app config must not duplicate the pinned SHA")
        self.assertIsNone(re.search(r"[0-9a-f]{40}", json.dumps(cfg)), "app config must not carry any commit SHA")

    @NEEDS_PIN
    def test_verified_checkout_matches_pin(self):
        self.assertEqual(PIN["asa_baseline"], pinmod.pin_record()["sha"])
        activated = pinmod.activate()
        self.assertEqual(activated["pinned_sha"], pinmod.pin_record()["sha"])


@NEEDS_PIN
class SliceRoundTrip(_TempDataDir):
    def test_pin_snapshot_objective_receipt(self):
        from app import slice as s
        view = s.run_slice()
        run_dir = Path(os.environ["ASA_ASTRO_APP_DATA_DIR"]) / "runs" / view["run_id"]
        for name in s.ARTIFACTS:
            self.assertTrue((run_dir / name).is_file(), name)
        receipt_text = (run_dir / "receipt.json").read_text(encoding="utf-8")
        receipt = json.loads(receipt_text)
        self.assertRegex(receipt["receipt_id"], r"^RCPT-[0-9a-f]{64}$")
        self.assertEqual(view["run_id"], receipt["receipt_id"])
        self.assertTrue(view["receipt"]["receipt_id_verified"])
        self.assertEqual((run_dir / "receipt.sha256").read_text().split()[0], hashlib.sha256(receipt_text.rstrip("\n").encode()).hexdigest())
        self.assertEqual(receipt["asa_baseline"], pinmod.pin_record()["sha"])
        snap = json.loads((run_dir / "snapshot.json").read_text())
        self.assertEqual(snap["summary"]["digest"], receipt["kernel_digest"])
        self.assertEqual(receipt["objective_name"], json.loads((run_dir / "objective.json").read_text())["name"])
        self.assertEqual(view["compat_shims"][0]["id"], "app-compat-proposer-uao")
        self.assertIn("observation_evidence", view)
        self.assertFalse(view["observation_evidence"]["present"], "Objective path has no observation evidence yet")

    def test_every_displayed_item_cites_an_existing_field(self):
        from app import slice as s
        view = s.run_slice()
        run_dir = Path(os.environ["ASA_ASTRO_APP_DATA_DIR"]) / "runs" / view["run_id"]
        docs = {}
        items = (view["claims"] + view["unknowns"] + view["next_evidence"] + view["results"]
                 + view["explanation"]["summary"] + view["explanation"]["per_entity"])
        self.assertTrue(items)
        for item in items:
            ref = item["source"]
            if ref["artifact"] not in docs:
                docs[ref["artifact"]] = json.loads((run_dir / ref["artifact"]).read_text())
            resolve_pointer(docs[ref["artifact"]], ref["pointer"])  # raises if the cited field does not exist

    def test_honesty_labels(self):
        from app import slice as s
        view = s.run_slice()
        labels = {c["label"] for c in view["claims"]}
        self.assertLessEqual(labels, {"hypothesis", "established-in-ASA-state"})
        if view["snapshot"]["universe"]["data_class"] != "real":
            self.assertEqual(view["claim_counts"]["established-in-ASA-state"], 0)
        for c in view["claims"]:
            if c["group"] in ("objective-result", "plan"):
                self.assertEqual(c["label"], "hypothesis")
            if c["label"] == "hypothesis":
                self.assertTrue(c["reasons"])
        self.assertTrue(all(n["label"] == "hypothesis" for n in view["next_evidence"]))
        self.assertTrue(any(u["kind"] == "data-class" for u in view["unknowns"]))

    def test_rerun_reproduces_identical_receipt(self):
        from app import slice as s
        first = s.run_slice()
        second = s.run_slice()
        self.assertEqual(first["run_id"], second["run_id"])
        self.assertTrue(second["reproduced"])
        lines = (Path(os.environ["ASA_ASTRO_APP_DATA_DIR"]) / "runs" / first["run_id"] / "invocations.jsonl").read_text().splitlines()
        self.assertEqual(len(lines), 2)
        self.assertTrue(json.loads(lines[1])["reproduced_identical_receipt_id"])

    def test_unknown_objective_rejected(self):
        from app import slice as s
        with self.assertRaises(ValueError):
            s.run_slice("../../etc/passwd")
        with self.assertRaises(ValueError):
            s.run_slice("no-such-objective")


class _Landmarks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags, self.ids, self.label_for, self.controls, self.live, self.lang = [], set(), set(), [], False, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if tag == "html":
            self.lang = a.get("lang")
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "label" and "for" in a:
            self.label_for.add(a["for"])
        if tag in ("input", "select", "textarea"):
            self.controls.append(a.get("id"))
        if a.get("aria-live") in ("polite", "assertive"):
            self.live = True


@NEEDS_PIN
class HttpTests(_TempDataDir):
    def setUp(self):
        super().setUp()
        from app.server import make_server
        self.httpd = make_server("127.0.0.1", 0, quiet=True)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        super().tearDown()

    def get(self, path):
        with urllib.request.urlopen(self.base + path, timeout=60) as r:
            return r.status, r.headers.get("Content-Type"), r.read()

    def post(self, path, body):
        req = urllib.request.Request(self.base + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read())

    def test_api_round_trip_and_search(self):
        status, ctype, body = self.get("/api/pin")
        self.assertEqual(json.loads(body)["pinned_sha"], pinmod.pin_record()["sha"])
        status, view = self.post("/api/runs", {"objective": "A-exoplanet-transit-followup"})
        self.assertEqual(status, 201)
        run_id = view["run_id"]
        status, again = self.post("/api/runs", {"objective": "A-exoplanet-transit-followup"})
        self.assertEqual((status, again["run_id"], again["reproduced"]), (200, run_id, True))
        _, _, body = self.get(f"/api/runs/{run_id}")
        self.assertEqual(json.loads(body)["receipt"]["receipt_id"], run_id)
        _, _, body = self.get(f"/api/runs/{run_id}/artifacts/receipt.json")
        self.assertEqual(json.loads(body)["receipt_id"], run_id)
        _, _, body = self.get("/api/runs?q=transit")
        self.assertEqual([r["run_id"] for r in json.loads(body)["runs"]], [run_id])
        _, _, body = self.get("/api/runs?q=zz-no-match-zz")
        self.assertEqual(json.loads(body)["runs"], [])

    def test_rejections(self):
        for path in ("/api/runs/RCPT-x", "/api/runs/../../etc/passwd", "/static/../server.py", "/nope"):
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                self.get(path)
            self.assertEqual(ctx.exception.code, 404, path)
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.post("/api/runs", {"objective": "no-such"})
        self.assertEqual(ctx.exception.code, 400)

    def test_frontend_accessibility_smoke(self):
        status, ctype, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertTrue(ctype.startswith("text/html"))
        p = _Landmarks()
        p.feed(body.decode("utf-8"))
        self.assertEqual(p.lang, "en")
        for tag in ("header", "nav", "main", "footer", "h1"):
            self.assertIn(tag, p.tags)
        self.assertTrue(p.live, "progress/status needs aria-live")
        self.assertTrue(p.controls)
        for control in p.controls:
            self.assertIn(control, p.label_for, f"form control {control} has no <label for>")
        for section in ("pin", "snapshot", "receipt", "claims", "unknowns", "observation", "next", "runs"):
            self.assertIn(section, p.ids)
        for asset in ("/static/app.js", "/static/styles.css"):
            self.assertEqual(self.get(asset)[0], 200)
        self.assertNotRegex(body.decode(), r"https?://(?!www\.w3\.org)", "no CDN / remote dependency")


if __name__ == "__main__":
    unittest.main()
