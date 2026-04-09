#!/usr/bin/env python3
"""
Similarity manual-labeling tool (0/1/2) for ICHTP.

Features:
- Auto-scan image assets under selected roots.
- Randomly sample hundreds/thousands of image pairs.
- Browser UI for manual labeling (0=不相似, 1=有點相似, 2=很相似).
- Resume labeling progress by session.
- Export merged CSV for analysis.

Example:
    python scripts/similarity_label_tool.py --sample-size 1000 --session ir2_similarity_v1
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import threading
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from flask import Flask, jsonify, request, send_file, Response

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}
LABEL_FIELDS = [
    "pair_id",
    "label",
    "similarity_score",
    "score_hash",
    "score_mse",
    "score_ssim",
    "score_mobilenet",
    "annotator",
    "note",
    "timestamp",
]


@dataclass
class PairItem:
    pair_id: int
    img_a: str
    img_b: str
    stratum: str
    is_pcg: bool = False
    pcg_seed: int = 0


class LabelState:
    def __init__(self, workspace: Path, session_dir: Path, pairs: List[PairItem]) -> None:
        self.workspace = workspace
        self.session_dir = session_dir
        self.pairs = pairs
        self.labels_csv = session_dir / "labels.csv"
        self.export_csv = session_dir / "labeled_pairs_merged.csv"
        self._lock = threading.Lock()
        self.ensure_label_header()
        self.latest_labels = self._load_latest_labels()

    def _load_latest_labels(self) -> Dict[int, Dict[str, str]]:
        latest: Dict[int, Dict[str, str]] = {}
        if not self.labels_csv.exists():
            return latest

        with self.labels_csv.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    pid = int(row.get("pair_id", ""))
                except ValueError:
                    continue
                latest[pid] = row
        return latest

    def ensure_label_header(self) -> None:
        if not self.labels_csv.exists():
            with self.labels_csv.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=LABEL_FIELDS)
                writer.writeheader()
            return

        with self.labels_csv.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            existing_fields = reader.fieldnames or []
            rows = list(reader)

        # Already latest schema
        if all(field in existing_fields for field in LABEL_FIELDS):
            return

        # Migrate old schema to new schema (add similarity_score if missing)
        migrated_rows: List[Dict[str, str]] = []
        for row in rows:
            migrated_rows.append(
                {
                    "pair_id": row.get("pair_id", ""),
                    "label": row.get("label", ""),
                    "similarity_score": row.get("similarity_score", ""),
                    "score_hash": row.get("score_hash", ""),
                    "score_mse": row.get("score_mse", ""),
                    "score_ssim": row.get("score_ssim", ""),
                    "score_mobilenet": row.get("score_mobilenet", ""),
                    "annotator": row.get("annotator", ""),
                    "note": row.get("note", ""),
                    "timestamp": row.get("timestamp", ""),
                }
            )

        with self.labels_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=LABEL_FIELDS)
            writer.writeheader()
            writer.writerows(migrated_rows)

    def save_label(
        self,
        pair_id: int,
        label: int,
        annotator: str,
        note: str,
        similarity_score: float | None,
        score_hash: float | None = None,
        score_mse: float | None = None,
        score_ssim: float | None = None,
        score_mobilenet: float | None = None,
    ) -> Dict[str, str]:
        now = datetime.now().isoformat(timespec="seconds")
        row = {
            "pair_id": str(pair_id),
            "label": str(label),
            "similarity_score": "" if similarity_score is None else f"{similarity_score:.6f}",
            "score_hash": "" if score_hash is None else f"{score_hash:.6f}",
            "score_mse": "" if score_mse is None else f"{score_mse:.6f}",
            "score_ssim": "" if score_ssim is None else f"{score_ssim:.6f}",
            "score_mobilenet": "" if score_mobilenet is None else f"{score_mobilenet:.6f}",
            "annotator": annotator.strip() or "anonymous",
            "note": note.strip(),
            "timestamp": now,
        }

        with self._lock:
            self.ensure_label_header()
            with self.labels_csv.open("a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=LABEL_FIELDS)
                writer.writerow(row)
            self.latest_labels[pair_id] = row

        return row

    def get_status(self) -> Dict[str, int]:
        total = len(self.pairs)
        done = len(self.latest_labels)
        return {
            "total": total,
            "done": done,
            "remaining": max(0, total - done),
            "percent": int((done / total) * 100) if total > 0 else 0,
        }

    def build_export(self) -> Path:
        with self._lock:
            with self.export_csv.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "pair_id",
                        "img_a",
                        "img_b",
                        "stratum",
                        "is_pcg",
                        "pcg_seed",
                        "label",
                        "similarity_score",
                        "score_hash",
                        "score_mse",
                        "score_ssim",
                        "score_mobilenet",
                        "annotator",
                        "note",
                        "timestamp",
                    ],
                )
                writer.writeheader()
                for p in self.pairs:
                    latest = self.latest_labels.get(p.pair_id, {})
                    writer.writerow(
                        {
                            "pair_id": p.pair_id,
                            "img_a": p.img_a,
                            "img_b": p.img_b,
                            "stratum": p.stratum,
                            "is_pcg": int(p.is_pcg),
                            "pcg_seed": p.pcg_seed,
                            "label": latest.get("label", ""),
                            "similarity_score": latest.get("similarity_score", ""),
                            "score_hash": latest.get("score_hash", ""),
                            "score_mse": latest.get("score_mse", ""),
                            "score_ssim": latest.get("score_ssim", ""),
                            "score_mobilenet": latest.get("score_mobilenet", ""),
                            "annotator": latest.get("annotator", ""),
                            "note": latest.get("note", ""),
                            "timestamp": latest.get("timestamp", ""),
                        }
                    )
        return self.export_csv


def discover_images(workspace: Path, roots: List[str]) -> List[Path]:
    files: List[Path] = []
    for rel_root in roots:
        root = (workspace / rel_root).resolve()
        if not root.exists() or not root.is_dir():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
                files.append(p.resolve())
    return sorted(files)


def _parent_bucket(paths: List[Path]) -> Dict[str, List[int]]:
    buckets: Dict[str, List[int]] = {}
    for idx, p in enumerate(paths):
        key = str(p.parent)
        buckets.setdefault(key, []).append(idx)
    return buckets


def sample_pairs(
    image_paths: List[Path],
    sample_size: int,
    seed: int,
    same_dir_ratio: float = 0.35,
) -> List[Tuple[int, int, str]]:
    if len(image_paths) < 2:
        raise ValueError("Need at least 2 images to sample pairs.")

    rng = random.Random(seed)
    used = set()
    pairs: List[Tuple[int, int, str]] = []

    target_same = int(sample_size * same_dir_ratio)
    buckets = _parent_bucket(image_paths)
    valid_buckets = [arr for arr in buckets.values() if len(arr) >= 2]

    tries = 0
    while len(pairs) < target_same and tries < max(1000, sample_size * 40):
        tries += 1
        if not valid_buckets:
            break
        arr = rng.choice(valid_buckets)
        i, j = rng.sample(arr, 2)
        a, b = (i, j) if i < j else (j, i)
        if a == b or (a, b) in used:
            continue
        used.add((a, b))
        pairs.append((a, b, "same_dir"))

    tries = 0
    while len(pairs) < sample_size and tries < max(2000, sample_size * 80):
        tries += 1
        i, j = rng.sample(range(len(image_paths)), 2)
        a, b = (i, j) if i < j else (j, i)
        if a == b or (a, b) in used:
            continue
        used.add((a, b))
        pairs.append((a, b, "random"))

    if len(pairs) < sample_size:
        print(f"[WARN] Requested {sample_size} pairs, generated {len(pairs)} pairs.")

    return pairs


def build_mixed_pairs(
    image_paths: List[Path],
    sample_size: int,
    seed: int,
    workspace: Path,
    pcg_every: int = 3,
) -> List[PairItem]:
    """Build pair list where every Nth question is a deterministic PCG-generated variant pair."""
    if pcg_every < 2:
        pcg_every = 3

    rng = random.Random(seed)
    pcg_count = sample_size // pcg_every
    normal_count = sample_size - pcg_count

    normal_specs = sample_pairs(
        image_paths=image_paths,
        sample_size=normal_count,
        seed=seed,
        same_dir_ratio=0.35,
    )

    pairs: List[PairItem] = []
    normal_i = 0

    for pid in range(1, sample_size + 1):
        make_pcg = (pid % pcg_every == 0)
        if make_pcg:
            src_idx = rng.randrange(len(image_paths))
            pa = image_paths[src_idx].resolve().relative_to(workspace.resolve()).as_posix()
            # img_b is generated in browser from img_a using deterministic seed.
            pairs.append(
                PairItem(
                    pair_id=pid,
                    img_a=pa,
                    img_b="__PCG_GENERATED__",
                    stratum="pcg_generated",
                    is_pcg=True,
                    pcg_seed=(seed * 1000003 + pid * 9176) % 2147483647,
                )
            )
            continue

        if normal_i >= len(normal_specs):
            i, j = rng.sample(range(len(image_paths)), 2)
            stratum = "random"
        else:
            i, j, stratum = normal_specs[normal_i]
            normal_i += 1

        pa = image_paths[i].resolve().relative_to(workspace.resolve()).as_posix()
        pb = image_paths[j].resolve().relative_to(workspace.resolve()).as_posix()
        pairs.append(
            PairItem(
                pair_id=pid,
                img_a=pa,
                img_b=pb,
                stratum=stratum,
                is_pcg=False,
                pcg_seed=0,
            )
        )

    return pairs


def save_pairs_json(
    session_dir: Path,
    pairs: List[PairItem],
) -> List[PairItem]:
    payload = [
        {
            "pair_id": p.pair_id,
            "img_a": p.img_a,
            "img_b": p.img_b,
            "stratum": p.stratum,
            "is_pcg": p.is_pcg,
            "pcg_seed": p.pcg_seed,
        }
        for p in pairs
    ]
    out = session_dir / "pairs.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return pairs


def load_pairs_json(session_dir: Path) -> List[PairItem]:
    data = json.loads((session_dir / "pairs.json").read_text(encoding="utf-8"))
    return [
        PairItem(
            pair_id=int(x["pair_id"]),
            img_a=x["img_a"],
            img_b=x["img_b"],
            stratum=x.get("stratum", "random"),
            is_pcg=bool(x.get("is_pcg", False)),
            pcg_seed=int(x.get("pcg_seed", 0) or 0),
        )
        for x in data
    ]


def create_app(state: LabelState) -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index() -> Response:
        return Response(
            INDEX_HTML,
            mimetype="text/html",
        )

    @app.get("/api/similarity-pipeline-js")
    def similarity_pipeline_js():
        fp = (state.workspace / "static" / "lib" / "similarity-pipeline.js").resolve()
        if not fp.exists():
            return jsonify({"error": "similarity-pipeline.js not found"}), 404
        return send_file(str(fp), mimetype="application/javascript")

    @app.get("/api/status")
    def api_status():
        return jsonify(state.get_status())

    @app.get("/api/pair/<int:index>")
    def api_pair(index: int):
        if index < 0 or index >= len(state.pairs):
            return jsonify({"error": "index out of range"}), 404
        p = state.pairs[index]
        latest = state.latest_labels.get(p.pair_id)
        return jsonify(
            {
                "index": index,
                "total": len(state.pairs),
                "pair_id": p.pair_id,
                "img_a": p.img_a,
                "img_b": p.img_b,
                "stratum": p.stratum,
                "is_pcg": p.is_pcg,
                "pcg_seed": p.pcg_seed,
                "label": int(latest["label"]) if latest and latest.get("label", "").isdigit() else None,
                "similarity_score": float(latest["similarity_score"]) if latest and latest.get("similarity_score", "") not in ("", None) else None,
                "score_hash": float(latest["score_hash"]) if latest and latest.get("score_hash", "") not in ("", None) else None,
                "score_mse": float(latest["score_mse"]) if latest and latest.get("score_mse", "") not in ("", None) else None,
                "score_ssim": float(latest["score_ssim"]) if latest and latest.get("score_ssim", "") not in ("", None) else None,
                "score_mobilenet": float(latest["score_mobilenet"]) if latest and latest.get("score_mobilenet", "") not in ("", None) else None,
                "annotator": latest.get("annotator", "") if latest else "",
                "note": latest.get("note", "") if latest else "",
            }
        )

    @app.get("/api/image/<int:index>/<side>")
    def api_image(index: int, side: str):
        if index < 0 or index >= len(state.pairs):
            return jsonify({"error": "index out of range"}), 404
        p = state.pairs[index]
        if side not in {"a", "b"}:
            return jsonify({"error": "invalid side"}), 400

        if p.is_pcg and side == "b":
            return jsonify({"error": "side b is PCG-generated in browser"}), 400

        rel = p.img_a if side == "a" else p.img_b
        fp = (state.workspace / rel).resolve()
        if not fp.exists() or not fp.is_file():
            return jsonify({"error": "file not found"}), 404
        return send_file(str(fp))

    @app.post("/api/label")
    def api_label():
        data = request.get_json(silent=True) or {}
        pair_id = data.get("pair_id")
        label = data.get("label")
        similarity_score = data.get("similarity_score")
        score_hash = data.get("score_hash")
        score_mse = data.get("score_mse")
        score_ssim = data.get("score_ssim")
        score_mobilenet = data.get("score_mobilenet")
        annotator = data.get("annotator", "anonymous")
        note = data.get("note", "")

        if not isinstance(pair_id, int):
            return jsonify({"error": "pair_id must be int"}), 400
        if label not in (0, 1, 2, 3):
            return jsonify({"error": "label must be 0,1,2,3"}), 400
        if similarity_score is not None:
            try:
                similarity_score = float(similarity_score)
            except (TypeError, ValueError):
                return jsonify({"error": "similarity_score must be numeric or null"}), 400

        # Helper to safely parse raw feature floats
        def _parse_float(val):
            if val is None or str(val) == "": return None
            try: return float(val)
            except: return None
            
        score_hash = _parse_float(score_hash)
        score_mse = _parse_float(score_mse)
        score_ssim = _parse_float(score_ssim)
        score_mobilenet = _parse_float(score_mobilenet)

        if pair_id < 1 or pair_id > len(state.pairs):
            return jsonify({"error": "pair_id out of range"}), 404

        saved = state.save_label(
            pair_id=pair_id,
            label=label,
            annotator=str(annotator),
            note=str(note),
            similarity_score=similarity_score,
            score_hash=score_hash,
            score_mse=score_mse,
            score_ssim=score_ssim,
            score_mobilenet=score_mobilenet,
        )
        return jsonify({"ok": True, "saved": saved, "status": state.get_status()})

    @app.get("/api/export")
    def api_export():
        out = state.build_export()
        return send_file(str(out), as_attachment=True, download_name=out.name)

    return app


INDEX_HTML = r"""
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Similarity Manual Label Tool</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f6f7fb; color: #222; }
    .wrap { max-width: 1200px; margin: 0 auto; padding: 16px; }
    .top { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
    .card { background: white; border-radius: 10px; padding: 12px 14px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }
    .pair { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px; }
    .imgbox { background: white; border-radius: 10px; padding: 10px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }
    img { width: 100%; max-height: 520px; object-fit: contain; background: #111; }
    .meta { font-size: 13px; color: #555; margin-top: 8px; word-break: break-all; }
    .actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
    button { border: 0; border-radius: 8px; padding: 10px 12px; cursor: pointer; font-weight: 600; }
    .b0 { background: #f44336; color: white; }
    .b1 { background: #ff9800; color: white; }
    .b2 { background: #4caf50; color: white; }
    .nav { background: #3949ab; color: white; }
    .ghost { background: #eceff1; }
    input[type='text'] { padding: 8px 10px; border-radius: 8px; border: 1px solid #ccc; min-width: 220px; }
    .bar { width: 260px; height: 10px; background: #e0e0e0; border-radius: 99px; overflow: hidden; }
    .fill { height: 100%; background: #42a5f5; width: 0%; }
    .hint { font-size: 13px; color: #666; }
        .score { font-size: 14px; font-weight: 700; color: #1a237e; background: #e8eaf6; padding: 6px 10px; border-radius: 8px; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top card">
      <strong>Similarity 標註工具</strong>
      <span id="counter">-/-</span>
      <div class="bar"><div id="fill" class="fill"></div></div>
      <span id="percent">0%</span>
            <span id="simScore" class="score">Score: --</span>
      <input id="annotator" type="text" placeholder="標註者名稱 (例如 KC)" />
      <button class="ghost" id="exportBtn">匯出 CSV</button>
    </div>

    <div class="pair">
      <div class="imgbox">
        <img id="imgA" alt="A" />
        <div class="meta" id="metaA"></div>
      </div>
      <div class="imgbox">
        <img id="imgB" alt="B" />
        <div class="meta" id="metaB"></div>
      </div>
    </div>

    <div class="card" style="margin-top: 14px;">
      <div><strong>標註：</strong>0 = 不相似，1 = 有點相似，2 = 很相似</div>
      <div class="actions">
        <button class="b0" onclick="saveLabel(0)">0 不相似 (快捷鍵 0)</button>
        <button class="b1" onclick="saveLabel(1)">1 有點相似 (快捷鍵 1)</button>
        <button class="b2" onclick="saveLabel(2)">2 很相似 (快捷鍵 2)</button>
                <button class="b2" onclick="saveLabel(3)">3 Too Similar (快捷鍵 3)</button>
        <button class="nav" onclick="prevPair()">上一題 ←</button>
        <button class="nav" onclick="nextPair()">下一題 →</button>
      </div>
      <div class="hint" id="labelHint" style="margin-top: 8px;"></div>
            <div class="hint" style="margin-top: 8px;">提示：可使用鍵盤 0/1/2/3 標註，左右方向鍵切換題目。</div>
            <div class="hint" style="margin-top: 6px;">每 3 題有 1 題為 PCG 生成圖（使用 similarity-pipeline.js 同風格變換流程）。</div>
    </div>
  </div>

<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/mobilenet@latest"></script>
<script src="/api/similarity-pipeline-js"></script>
<script>
let currentIndex = 0;
let current = null;
let total = 0;
let currentSimilarityScore = null;
let currentScoreHash = null;
let currentScoreMse = null;
let currentScoreSsim = null;
let currentScoreMobileNet = null;
let aiModel = null;
let aiModelLoadingPromise = null;

const annotatorInput = document.getElementById('annotator');
annotatorInput.value = localStorage.getItem('sim_annotator') || '';
annotatorInput.addEventListener('change', () => {
  localStorage.setItem('sim_annotator', annotatorInput.value.trim());
});

async function loadStatus(){
  const s = await fetch('/api/status').then(r=>r.json());
  total = s.total;
  document.getElementById('percent').innerText = `${s.percent}%`;
  document.getElementById('fill').style.width = `${s.percent}%`;
}

function showHint(msg){
  document.getElementById('labelHint').innerText = msg || '';
}

function seededRandom(seed){
    let s = (seed >>> 0) || 1;
    return function(){
        s = (1664525 * s + 1013904223) >>> 0;
        return s / 4294967296;
    };
}

function clamp(v, min, max){
    return Math.max(min, Math.min(max, v));
}

function lerp(a, b, t){
    const tt = clamp(t, 0, 1);
    return a + (b - a) * tt;
}

async function ensureAIModel(){
    if(aiModel) return aiModel;
    if(aiModelLoadingPromise) return aiModelLoadingPromise;
    if(typeof mobilenet === 'undefined' || typeof tf === 'undefined'){
        return null;
    }
    aiModelLoadingPromise = mobilenet.load({ version: 2, alpha: 1.0 })
        .then((model) => {
            aiModel = model;
            tf.tidy(() => {
                aiModel.infer(tf.zeros([1, 224, 224, 3]), true);
            });
            return aiModel;
        })
        .catch(() => null)
        .finally(() => {
            aiModelLoadingPromise = null;
        });
    return aiModelLoadingPromise;
}

function loadImage(url){
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.crossOrigin = 'anonymous';
        img.onload = () => resolve(img);
        img.onerror = reject;
        img.src = url;
    });
}

function waitForImgElement(imgEl){
    return new Promise((resolve, reject) => {
        if(imgEl.complete && imgEl.naturalWidth > 0){
            resolve(imgEl);
            return;
        }
        imgEl.onload = () => resolve(imgEl);
        imgEl.onerror = reject;
    });
}

function canvasFromImgElement(imgEl){
    const c = document.createElement('canvas');
    c.width = imgEl.naturalWidth || imgEl.width;
    c.height = imgEl.naturalHeight || imgEl.height;
    const ctx = c.getContext('2d', { willReadFrequently: true });
    ctx.drawImage(imgEl, 0, 0, c.width, c.height);
    return c;
}

function sampleCanvasRGB(canvas, w=64, h=64){
    const c = document.createElement('canvas');
    c.width = w; c.height = h;
    const ctx = c.getContext('2d', { willReadFrequently: true });
    ctx.drawImage(canvas, 0, 0, w, h);
    return ctx.getImageData(0, 0, w, h).data;
}

function computeMSE(sampleA, canvasB){
    const w = 64, h = 64;
    const c = document.createElement('canvas');
    c.width = w; c.height = h;
    const ctx = c.getContext('2d', { willReadFrequently: true });
    ctx.drawImage(canvasB, 0, 0, w, h);
    const b = ctx.getImageData(0, 0, w, h).data;
    let mse = 0, n = 0;
    for(let i=0;i<b.length;i+=4){
        const dr = sampleA[i] - b[i];
        const dg = sampleA[i+1] - b[i+1];
        const db = sampleA[i+2] - b[i+2];
        mse += dr*dr + dg*dg + db*db;
        n++;
    }
    return mse / Math.max(1, n);
}

function computeGrayHist(canvas, bins=64){
    const w = canvas.width, h = canvas.height;
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    const data = ctx.getImageData(0, 0, w, h).data;
    const hist = new Array(bins).fill(0);
    for(let i=0;i<data.length;i+=4){
        const g = (data[i]*0.299 + data[i+1]*0.587 + data[i+2]*0.114) | 0;
        const idx = Math.min(bins - 1, (g / 256 * bins) | 0);
        hist[idx]++;
    }
    const tot = hist.reduce((a,b) => a + b, 0) || 1;
    return hist.map(v => v / tot);
}

function histDiff(h1, h2){
    let d = 0;
    for(let i=0;i<h1.length;i++) d += Math.abs(h1[i] - h2[i]);
    return d;
}

function computeAHash(canvas){
    const size = 8;
    const c = document.createElement('canvas');
    c.width = size; c.height = size;
    const ctx = c.getContext('2d', { willReadFrequently: true });
    ctx.drawImage(canvas, 0, 0, size, size);
    const data = ctx.getImageData(0, 0, size, size).data;
    let sum = 0;
    const gray = [];
    for(let i=0;i<data.length;i+=4){
        const g = (data[i]*0.299 + data[i+1]*0.587 + data[i+2]*0.114);
        gray.push(g); sum += g;
    }
    const avg = sum / gray.length;
    return gray.map(g => (g > avg ? '1' : '0')).join('');
}

function hammingHash(h1, h2){
    if(!h1 || !h2 || h1.length !== h2.length) return 64;
    let dist = 0;
    for(let i=0;i<h1.length;i++) if(h1[i] !== h2[i]) dist++;
    return dist;
}

function cosineSimilarityTensor(tA, tB){
    if(!tA || !tB || typeof tf === 'undefined') return 0;
    return tf.tidy(() => {
        const dot = tf.sum(tf.mul(tA, tB));
        const nA = tf.norm(tA);
        const nB = tf.norm(tB);
        const sim = tf.div(dot, tf.mul(nA, nB));
        return sim.dataSync()[0];
    });
}

function computeSSIM(canvasA, canvasB){
    const w = 64, h = 64;
    const cA = document.createElement('canvas'); cA.width = w; cA.height = h;
    const cB = document.createElement('canvas'); cB.width = w; cB.height = h;
    const ctxA = cA.getContext('2d', { willReadFrequently: true });
    const ctxB = cB.getContext('2d', { willReadFrequently: true });
    ctxA.drawImage(canvasA, 0, 0, w, h);
    ctxB.drawImage(canvasB, 0, 0, w, h);
    const dataA = ctxA.getImageData(0, 0, w, h).data;
    const dataB = ctxB.getImageData(0, 0, w, h).data;

    const lumaA = new Float32Array(w*h);
    const lumaB = new Float32Array(w*h);
    for(let i=0;i<w*h;i++){
        lumaA[i] = 0.299*dataA[i*4] + 0.587*dataA[i*4+1] + 0.114*dataA[i*4+2];
        lumaB[i] = 0.299*dataB[i*4] + 0.587*dataB[i*4+1] + 0.114*dataB[i*4+2];
    }

    const K1=0.01, K2=0.03, L=255;
    const C1=(K1*L)**2, C2=(K2*L)**2;
    const winSize=8;
    let mssimSum=0, count=0;
    for(let y=0;y<=h-winSize;y+=winSize){
        for(let x=0;x<=w-winSize;x+=winSize){
            let muA=0, muB=0, sumA2=0, sumB2=0, sumAB=0;
            for(let dy=0;dy<winSize;dy++){
                for(let dx=0;dx<winSize;dx++){
                    const idx=(y+dy)*w + (x+dx);
                    const va=lumaA[idx], vb=lumaB[idx];
                    muA+=va; muB+=vb;
                    sumA2+=va*va; sumB2+=vb*vb; sumAB+=va*vb;
                }
            }
            const N=winSize*winSize;
            muA/=N; muB/=N;
            const sigmaA2=(sumA2/N)-muA*muA;
            const sigmaB2=(sumB2/N)-muB*muB;
            const sigmaAB=(sumAB/N)-muA*muB;
            const ssim=((2*muA*muB + C1)*(2*sigmaAB + C2))/((muA*muA+muB*muB+C1)*(sigmaA2+sigmaB2+C2));
            mssimSum += ssim;
            count++;
        }
    }
    return count > 0 ? mssimSum / count : 0;
}

async function computePipelineStyleScore(canvasA, canvasB, difficulty=0.5){
    const d = clamp(difficulty, 0.05, 1);
    const sampleA = sampleCanvasRGB(canvasA);
    const mse = computeMSE(sampleA, canvasB);
    const hdiff = histDiff(computeGrayHist(canvasA), computeGrayHist(canvasB));
    const ssim = computeSSIM(canvasA, canvasB);
    const ham = hammingHash(computeAHash(canvasA), computeAHash(canvasB));

    let aiScore = 0;
    const model = await ensureAIModel();
    if(model && typeof tf !== 'undefined'){
        const embA = model.infer(canvasA, true);
        const embB = model.infer(canvasB, true);
        aiScore = cosineSimilarityTensor(embA, embB);
        if(embA && embA.dispose) embA.dispose();
        if(embB && embB.dispose) embB.dispose();
        aiScore = clamp(aiScore, 0, 1);
    }

    const mseMin = lerp(90*0.7, 90, d), mseMax = lerp(2600*0.85, 2600, d);
    const histMin = lerp(0.08*0.6, 0.08, d), histMax = lerp(0.42*0.85, 0.42, d);
    const ssimMin = lerp(0.55*0.9, 0.55, d), ssimMax = lerp(0.88*0.95, 0.88, d);
    const hamMin = lerp(8*0.9, 8, d), hamMax = lerp(26*0.9, 26, d);

    const mseScore = 1 - clamp((mse - mseMin) / (mseMax - mseMin), 0, 1);
    const hdiffScore = 1 - clamp((hdiff - histMin) / (histMax - histMin), 0, 1);
    const ssimScore = clamp((ssim - ssimMin) / (ssimMax - ssimMin), 0, 1);
    const diversityScore = clamp((ham - hamMin) / (hamMax - hamMin), 0, 1);

    const weights = (typeof SimilarityPipeline !== 'undefined' && SimilarityPipeline.config && SimilarityPipeline.config.weights)
        ? SimilarityPipeline.config.weights
        : { mseW: 0.05, hdiffW: 0.15, ssimW: 0.40, aiW: 0.30, diversityW: 0.10 };

    // Same weighting style as similarity-pipeline.js, now including AI (MobileNetV2 cosine).
    const score =
        mseScore * (weights.mseW ?? 0.05) +
        hdiffScore * (weights.hdiffW ?? 0.15) +
        ssimScore * (weights.ssimW ?? 0.40) +
        diversityScore * (weights.diversityW ?? 0.10) +
        aiScore * (weights.aiW ?? 0.30);

    return {
        score,
        mse,
        hdiff,
        ssim,
        ham,
        aiScore,
    };
}

async function computeAndShowSimilarityScore(){
    const scoreEl = document.getElementById('simScore');
    try {
        const imgAEl = document.getElementById('imgA');
        const imgBEl = document.getElementById('imgB');
        await Promise.all([waitForImgElement(imgAEl), waitForImgElement(imgBEl)]);
        const cA = canvasFromImgElement(imgAEl);
        const cB = canvasFromImgElement(imgBEl);
        const result = await computePipelineStyleScore(cA, cB, 0.5);
        currentSimilarityScore = Number(result.score.toFixed(6));
        currentScoreHash = Number(result.ham.toFixed(6));
        currentScoreMse = Number(result.mse.toFixed(6));
        currentScoreSsim = Number(result.ssim.toFixed(6));
        currentScoreMobileNet = Number(result.aiScore.toFixed(6));
        scoreEl.innerText = `Score: ${currentSimilarityScore.toFixed(4)} (AI=${result.aiScore.toFixed(3)})`;
    } catch (e) {
        currentSimilarityScore = null;
        currentScoreHash = null;
        currentScoreMse = null;
        currentScoreSsim = null;
        currentScoreMobileNet = null;
        scoreEl.innerText = 'Score: N/A';
    }
}

function avgColor(img){
    const s = 32;
    const c = document.createElement('canvas');
    c.width = s; c.height = s;
    const ctx = c.getContext('2d', { willReadFrequently: true });
    ctx.drawImage(img, 0, 0, s, s);
    const data = ctx.getImageData(0, 0, s, s).data;
    let r=0,g=0,b=0,n=0;
    for(let i=0;i<data.length;i+=4){
        r += data[i]; g += data[i+1]; b += data[i+2]; n++;
    }
    return `rgb(${(r/n)|0}, ${(g/n)|0}, ${(b/n)|0})`;
}

function rgbToHsv(r,g,b){
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r,g,b), min = Math.min(r,g,b);
    const d = max - min;
    let h = 0;
    if(d !== 0){
        if(max === r) h = ((g - b) / d + (g < b ? 6 : 0));
        else if(max === g) h = ((b - r) / d + 2);
        else h = ((r - g) / d + 4);
        h /= 6;
    }
    const s = max === 0 ? 0 : d / max;
    const v = max;
    return [h, s, v];
}

function hsvToRgb(h,s,v){
    let r=0,g=0,b=0;
    const i = Math.floor(h * 6);
    const f = h * 6 - i;
    const p = v * (1 - s);
    const q = v * (1 - f * s);
    const t = v * (1 - (1 - f) * s);
    switch(i % 6){
        case 0: r=v; g=t; b=p; break;
        case 1: r=q; g=v; b=p; break;
        case 2: r=p; g=v; b=t; break;
        case 3: r=p; g=q; b=v; break;
        case 4: r=t; g=p; b=v; break;
        case 5: r=v; g=p; b=q; break;
    }
    return [Math.round(r*255), Math.round(g*255), Math.round(b*255)];
}

function hasRectOverlap(rect, rects){
    for(const r of rects){
        if(!(rect.x + rect.w <= r.x || r.x + r.w <= rect.x || rect.y + rect.h <= r.y || r.y + r.h <= rect.y)){
            return true;
        }
    }
    return false;
}

function extractAlphaBounds(canvas, alphaThreshold=16){
    const w = canvas.width, h = canvas.height;
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    const data = ctx.getImageData(0, 0, w, h).data;
    let minX = w, minY = h, maxX = -1, maxY = -1;
    for(let y=0;y<h;y++){
        for(let x=0;x<w;x++){
            const a = data[(y*w + x)*4 + 3];
            if(a > alphaThreshold){
                if(x < minX) minX = x;
                if(y < minY) minY = y;
                if(x > maxX) maxX = x;
                if(y > maxY) maxY = y;
            }
        }
    }
    if(maxX < minX || maxY < minY) return null;
    return { x:minX, y:minY, w:maxX-minX+1, h:maxY-minY+1 };
}

function generateObjectCloneVariantDataUrlFromImage(src, d, rng){
    const w = src.naturalWidth || src.width;
    const h = src.naturalHeight || src.height;
    if(w <= 0 || h <= 0) return null;

    const srcCanvas = document.createElement('canvas');
    srcCanvas.width = w; srcCanvas.height = h;
    const sctx = srcCanvas.getContext('2d', { willReadFrequently: true });
    sctx.drawImage(src, 0, 0, w, h);

    const imgD = sctx.getImageData(0, 0, w, h);
    const dArr = imgD.data;
    function getCol(x,y){ const i=(y*w+x)*4; return [dArr[i],dArr[i+1],dArr[i+2],dArr[i+3]]; }
    const TL = getCol(0,0), TR = getCol(w-1,0), BL = getCol(0,h-1), BR = getCol(w-1,h-1);

    if(TL[3] > 10){
      const visited = new Uint8Array(w * h);
      let q = [];
      const pushQ = (px, py) => {
        const idx = py * w + px;
        if(!visited[idx]){ visited[idx] = 1; q.push(px, py); }
      };

      for(let x=0; x<w; x++){ pushQ(x, 0); pushQ(x, h-1); }
      for(let y=0; y<h; y++){ pushQ(0, y); pushQ(w-1, y); }
      
      let head = 0;
      while(head < q.length){
        const x = q[head++], y = q[head++];
        const tx = x / (w-1 || 1), ty = y / (h-1 || 1);
        const expR = TL[0] + (TR[0]-TL[0])*tx + (BL[0]-TL[0])*ty + (TL[0]-TR[0]-BL[0]+BR[0])*tx*ty;
        const expG = TL[1] + (TR[1]-TL[1])*tx + (BL[1]-TL[1])*ty + (TL[1]-TR[1]-BL[1]+BR[1])*tx*ty;
        const expB = TL[2] + (TR[2]-TL[2])*tx + (BL[2]-TL[2])*ty + (TL[2]-TR[2]-BL[2]+BR[2])*tx*ty;
        const pIdx = (y * w + x) * 4;
        
        if(Math.abs(dArr[pIdx]-expR)<40 && Math.abs(dArr[pIdx+1]-expG)<40 && Math.abs(dArr[pIdx+2]-expB)<40){
          dArr[pIdx+3] = 0;
          if(x>0) pushQ(x-1, y);
          if(x<w-1) pushQ(x+1, y);
          if(y>0) pushQ(x, y-1);
          if(y<h-1) pushQ(x, y+1);
        }
      }
      sctx.putImageData(imgD, 0, 0);
    }

    const bounds = extractAlphaBounds(srcCanvas, 18);
    if(!bounds) return null;

    const crop = document.createElement('canvas');
    crop.width = bounds.w; crop.height = bounds.h;
    crop.getContext('2d').drawImage(srcCanvas, bounds.x, bounds.y, bounds.w, bounds.h, 0, 0, bounds.w, bounds.h);

    const out = document.createElement('canvas');
    out.width = w; out.height = h;
    const octx = out.getContext('2d', { willReadFrequently: true });
    
    // Synthesize clean background gradient without the original milk carton
    const bgImgD = octx.createImageData(w, h);
    for(let y=0; y<h; y++){
      for(let x=0; x<w; x++){
        const tx = x / (w-1 || 1), ty = y / (h-1 || 1);
        const expR = TL[0] + (TR[0]-TL[0])*tx + (BL[0]-TL[0])*ty + (TL[0]-TR[0]-BL[0]+BR[0])*tx*ty;
        const expG = TL[1] + (TR[1]-TL[1])*tx + (BL[1]-TL[1])*ty + (TL[1]-TR[1]-BL[1]+BR[1])*tx*ty;
        const expB = TL[2] + (TR[2]-TL[2])*tx + (BL[2]-TL[2])*ty + (TL[2]-TR[2]-BL[2]+BR[2])*tx*ty;
        const idx = (y*w + x)*4;
        bgImgD.data[idx] = expR; bgImgD.data[idx+1] = expG; bgImgD.data[idx+2] = expB; bgImgD.data[idx+3] = 255;
      }
    }
    octx.putImageData(bgImgD, 0, 0);
            const dw = Math.max(8, Math.round(crop.width * scale));
            const dh = Math.max(8, Math.round(crop.height * scale));
            const x = Math.round(rng() * Math.max(0, w - dw));
            const y = Math.round(rng() * Math.max(0, h - dh));
            const margin = Math.round(8 + (14 - 8) * d);
            const rect = { x:x-margin, y:y-margin, w:dw+margin*2, h:dh+margin*2 };
            if(hasRectOverlap(rect, placed)) continue;
            placed.push(rect);
            octx.drawImage(crop, 0, 0, crop.width, crop.height, x, y, dw, dh);
            done = true;
            break;
        }
        if(!done && placed.length < 2) return null;
    }

    if(placed.length < 2) return null;
    return out.toDataURL('image/png');
}

async function generatePcgVariantDataUrl(sourceUrl, seed){
    const rng = seededRandom(seed || 1);
    const src = await loadImage(sourceUrl);
    const w = src.naturalWidth || src.width;
    const h = src.naturalHeight || src.height;
    const d = 0.65; // fixed mid-high test difficulty for PCG validation rounds

    const c = document.createElement('canvas');
    c.width = w; c.height = h;
    const ctx = c.getContext('2d', { willReadFrequently: true });

    // New variant family: clone extracted object(s) on blue background
    if(rng() < (0.20 + (0.40 - 0.20) * d)){
        const cloneUrl = generateObjectCloneVariantDataUrlFromImage(src, d, rng);
        if(cloneUrl) return cloneUrl;
    }

    ctx.fillStyle = avgColor(src);
    ctx.fillRect(0,0,w,h);

    const flipH = rng() < (0.15 + (0.5 - 0.15) * d);
    const flipV = rng() < (0.08 + (0.3 - 0.08) * d);
    // Mild combo: small rotation + perspective-like tilt (shear) + non-uniform scaling
    let rotDeg = (rng()*2 - 1) * (3.5 + (6.0 - 3.5) * d);
    const minRotDeg = (2.2 + (3.5 - 2.2) * d);
    if(Math.abs(rotDeg) < minRotDeg) rotDeg = rotDeg >= 0 ? minRotDeg : -minRotDeg;
    const rotRad = rotDeg * Math.PI / 180;
    let dx = (rng()*2 - 1) * (0.03 + (0.06 - 0.03) * d);
    let dy = (rng()*2 - 1) * (0.03 + (0.06 - 0.03) * d);
    const minScaleDelta = (0.02 + (0.04 - 0.02) * d);
    if(Math.abs(dx) < minScaleDelta) dx = dx >= 0 ? minScaleDelta : -minScaleDelta;
    if(Math.abs(dy) < minScaleDelta) dy = dy >= 0 ? minScaleDelta : -minScaleDelta;
    const sx = 1 + dx;
    const sy = 1 + dy;
    let tiltX = (rng()*2 - 1) * (0.015 + (0.04 - 0.015) * d);
    let tiltY = (rng()*2 - 1) * (0.01 + (0.03 - 0.01) * d);
    const minTiltX = (0.010 + (0.018 - 0.010) * d);
    const minTiltY = (0.008 + (0.015 - 0.008) * d);
    if(Math.abs(tiltX) < minTiltX) tiltX = tiltX >= 0 ? minTiltX : -minTiltX;
    if(Math.abs(tiltY) < minTiltY) tiltY = tiltY >= 0 ? minTiltY : -minTiltY;

    ctx.save();
    ctx.translate(w/2, h/2);
    ctx.transform(1, tiltY, tiltX, 1, 0, 0);
    ctx.rotate(rotRad);
    ctx.scale(flipH ? -sx : sx, flipV ? -sy : sy);
    ctx.drawImage(src, -w/2, -h/2, w, h);
    ctx.restore();

    if(rng() < (0.12 + (0.35 - 0.12) * d)){
        const modes = ['screen','overlay','soft-light'];
        const mode = modes[Math.floor(rng()*modes.length)];
        ctx.globalCompositeOperation = mode;
        let alpha = (0.12 + (0.30 - 0.12) * d) + (rng()*0.08 - 0.04);
        alpha = clamp(alpha, 0.10, 0.35);
        ctx.globalAlpha = alpha;
        ctx.save();
        const f2h = rng() < 0.5;
        const f2v = rng() < 0.3;
        ctx.translate(f2h ? w : 0, f2v ? h : 0);
        ctx.scale(f2h ? -1 : 1, f2v ? -1 : 1);
        const offX = (rng()*2 - 1) * (3.5 + (1.6 - 3.5) * d);
        const offY = (rng()*2 - 1) * (3.5 + (1.6 - 3.5) * d);
        ctx.drawImage(src, offX, offY);
        ctx.restore();
        ctx.globalAlpha = 1;
        ctx.globalCompositeOperation = 'source-over';
    }

    if(rng() < (0.35 + (0.85 - 0.35) * d)){
        const id = ctx.getImageData(0,0,w,h);
        const data = id.data;
        let hShift = (rng()*2 - 1) * (45 + (15 - 45) * d);
        const minShift = (18 + (8 - 18) * d);
        if(Math.abs(hShift) < minShift) hShift = hShift >= 0 ? minShift : -minShift;
        const sMul = 1 + (rng()*2 - 1) * (0.18 + (0.08 - 0.18) * d);
        for(let i=0;i<data.length;i+=4){
            if(data[i+3] < 16) continue;
            let [hh, ss, vv] = rgbToHsv(data[i], data[i+1], data[i+2]);
            hh = (hh + hShift / 360 + 1) % 1;
            ss = clamp(ss * sMul, 0, 1);
            const [rr, gg, bb] = hsvToRgb(hh, ss, vv);
            data[i] = rr; data[i+1] = gg; data[i+2] = bb;
        }
        ctx.putImageData(id,0,0);
    }

    // Blur removed intentionally.

    const pad = Math.round(rng() * (18 + (5 - 18) * d));
    if(pad > 0 && pad * 2 < Math.min(w,h)){
        const tmp = document.createElement('canvas');
        tmp.width = w; tmp.height = h;
        tmp.getContext('2d').drawImage(c, pad, pad, w - 2*pad, h - 2*pad, 0, 0, w, h);
        return tmp.toDataURL('image/png');
    }

    return c.toDataURL('image/png');
}

async function loadPair(index){
  const data = await fetch(`/api/pair/${index}`).then(r=>r.json());
  if(data.error){
    showHint(data.error);
    return;
  }
  current = data;
  currentIndex = data.index;

  document.getElementById('counter').innerText = `${data.index + 1} / ${data.total} (pair_id=${data.pair_id})`;
    const srcA = `/api/image/${data.index}/a`;
    document.getElementById('imgA').src = srcA;
    if(data.is_pcg){
        const pcgUrl = await generatePcgVariantDataUrl(srcA, data.pcg_seed || 1);
        document.getElementById('imgB').src = pcgUrl;
        document.getElementById('metaB').innerText = `PCG generated variant (seed=${data.pcg_seed})`;
    } else {
        document.getElementById('imgB').src = `/api/image/${data.index}/b`;
        document.getElementById('metaB').innerText = data.img_b;
    }
  document.getElementById('metaA').innerText = data.img_a;
    currentSimilarityScore = null;
    document.getElementById('simScore').innerText = 'Score: ...';
    await computeAndShowSimilarityScore();

    if(data.label === 0 || data.label === 1 || data.label === 2 || data.label === 3){
        const oldScore = data.similarity_score;
        const scoreText = oldScore === null || oldScore === undefined ? 'N/A' : Number(oldScore).toFixed(4);
        showHint(`目前標註：${data.label}（可覆蓋，舊分數=${scoreText}）`);
  } else {
        showHint(data.is_pcg ? '尚未標註（本題含 PCG 生成圖）' : '尚未標註');
  }
}

async function saveLabel(label){
  if(!current){ return; }
  const annotator = (annotatorInput.value || '').trim() || 'anonymous';

  const res = await fetch('/api/label', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            pair_id: current.pair_id,
            label,
            similarity_score: currentSimilarityScore,
            score_hash: currentScoreHash,
            score_mse: currentScoreMse,
            score_ssim: currentScoreSsim,
            score_mobilenet: currentScoreMobileNet,
            annotator,
            note: ''
        })
  }).then(r=>r.json());

  if(!res.ok){
    showHint(`儲存失敗: ${res.error || 'unknown'}`);
    return;
  }
    const scoreText = currentSimilarityScore === null ? 'N/A' : currentSimilarityScore.toFixed(4);
    showHint(`已儲存 pair_id=${current.pair_id}, label=${label}, score=${scoreText}`);
  await loadStatus();
  if(currentIndex < total - 1){
    await loadPair(currentIndex + 1);
  }
}

async function nextPair(){
  if(currentIndex < total - 1){
    await loadPair(currentIndex + 1);
  }
}

async function prevPair(){
  if(currentIndex > 0){
    await loadPair(currentIndex - 1);
  }
}

document.getElementById('exportBtn').addEventListener('click', ()=>{
  window.location.href = '/api/export';
});

window.addEventListener('keydown', async (e)=>{
  if(e.key === '0'){ await saveLabel(0); }
  else if(e.key === '1'){ await saveLabel(1); }
  else if(e.key === '2'){ await saveLabel(2); }
    else if(e.key === '3'){ await saveLabel(3); }
  else if(e.key === 'ArrowRight'){ await nextPair(); }
  else if(e.key === 'ArrowLeft'){ await prevPair(); }
});

(async function boot(){
  await loadStatus();
  await loadPair(0);
})();
</script>
</body>
</html>
"""


def build_or_load_pairs(
    workspace: Path,
    session_dir: Path,
    roots: List[str],
    sample_size: int,
    seed: int,
    pcg_every: int,
) -> List[PairItem]:
    pairs_json = session_dir / "pairs.json"
    if pairs_json.exists():
        print(f"[INFO] Reusing existing pairs: {pairs_json}")
        return load_pairs_json(session_dir)

    image_paths = discover_images(workspace, roots)
    print(f"[INFO] Found {len(image_paths)} images under roots={roots}")
    if len(image_paths) < 2:
        raise RuntimeError("Not enough images found. Check --roots.")

    pairs = build_mixed_pairs(
        image_paths=image_paths,
        sample_size=sample_size,
        seed=seed,
        workspace=workspace,
        pcg_every=pcg_every,
    )
    pairs = save_pairs_json(
        session_dir=session_dir,
        pairs=pairs,
    )
    print(f"[INFO] Generated {len(pairs)} sampled pairs -> {pairs_json}")
    return pairs


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(description="Manual similarity labeling tool (0/1/2).")
    parser.add_argument("--workspace", default=str(root), help="Workspace root path")
    parser.add_argument(
        "--roots",
        default="scripts/test photo for similarity_label_tool",
        help="Comma-separated roots to scan for images",
    )
    parser.add_argument("--sample-size", type=int, default=500, help="Number of pairs to sample")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--pcg-every", type=int, default=3, help="Inject one PCG-generated pair every N questions")
    parser.add_argument(
        "--session",
        default=f"similarity_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        help="Session name under heuristic_logs/similarity_labeling",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    parser.add_argument("--port", type=int, default=5055, help="Server port")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    roots = [x.strip() for x in args.roots.split(",") if x.strip()]

    session_dir = workspace / "heuristic_logs" / "similarity_labeling" / args.session
    session_dir.mkdir(parents=True, exist_ok=True)

    config_payload = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "workspace": workspace.as_posix(),
        "roots": roots,
        "sample_size": args.sample_size,
        "seed": args.seed,
        "pcg_every": args.pcg_every,
        "session": args.session,
    }
    (session_dir / "config.json").write_text(
        json.dumps(config_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    pairs = build_or_load_pairs(
        workspace=workspace,
        session_dir=session_dir,
        roots=roots,
        sample_size=args.sample_size,
        seed=args.seed,
        pcg_every=args.pcg_every,
    )

    state = LabelState(workspace=workspace, session_dir=session_dir, pairs=pairs)
    app = create_app(state)

    print("=" * 70)
    print("Similarity Label Tool 已啟動")
    print(f"Session: {args.session}")
    print(f"Pairs:   {len(pairs)}")
    print(f"URL:     http://{args.host}:{args.port}")
    print(f"Data:    {(session_dir).as_posix()}")
    print("標註規則：0=不相似, 1=有點相似, 2=很相似, 3=too similar")
    print(f"PCG規則：每 {args.pcg_every} 題有 1 題為 PCG 生成圖")
    print("=" * 70)

    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
