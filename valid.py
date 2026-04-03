#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
valid_model_qed_sa_ttest_v5.py

Evaluate BASE vs DPO vs MolGPT on QED, SA, FCD, KL with 10 groups × 100 generations per group
(n_scaffolds × n_per = 100). Uses scaffold-conditioned generation for all three models.

Features vs v1–v4:
- Per‑scaffold local accumulator (bug fix): stop when each scaffold reaches n_per (no global-mod bug)
- Watchdog controls: --max_wall_per_scaffold_sec, --max_tries_per_scaffold
- Small local batches for MolGPT: --molgpt_local_batch
- GPT-2 max tries factor: --gpt2_max_tries_factor
- Faster RDKit option: --fast_sanitize
- Optional: --skip_sa to speed up (no SA calculation)
- Parallelized QED/SA/FP: --n_jobs
- Scaffold caching per group: --cache_scaffolds
- MolGPT top_k auto-clamp to vocab size to avoid range errors
- Backward-compatible utils.sample() (no max_new_tokens usage)

Outputs:
- CSV: per_group_metrics_qed_sa_fcd_kl.csv
- JSON: ttest_pairwise_summary.json

Example:
python valid_model_qed_sa_ttest_v5.py \
  --zinc_csv /data/home/brian1501/Minsu/Final_research/250k_rndm_zinc_drugs_clean_3.csv \
  --out_dir  /data/home/brian1501/Minsu/Final_research/Validation/results \
  --base_ckpt /data/home/brian1501/Minsu/Final_research/gpt2-scaffold-finetuned/checkpoint-841476 \
  --dpo_ckpt  /data/home/brian1501/Minsu/Final_research/dpo_ckpt_final_3/checkpoint-313 \
  --molgpt_weight /data/home/brian1501/Minsu/Final_research/Validation/model/molgpt/weights/moses_scaf_wholeseq_qed.pt \
  --molgpt_stoi   /data/home/brian1501/Minsu/Final_research/Validation/model/molgpt/train/moses2_stoi.json \
  --molgpt_root   /data/home/brian1501/Minsu/Final_research/Validation/model/molgpt/generate \
  --hgraph_smiles /data/home/brian1501/Minsu/Final_research/Validation/results/hgraph_smiles_1.csv \
  --ref2_csv /data/home/brian1501/Minsu/Final_research/approved_drugs_with_smiles.csv \
  --ref2_smiles_col smiles \
  --n_scaffolds 10 --n_per 10 --groups 10 \
  --batch_size 128 --temperature 1.0 --top_k 16 \
  --max_wall_per_scaffold_sec 60 \
  --max_tries_per_scaffold 600 \
  --molgpt_local_batch 64 \
  --gpt2_max_tries_factor 25 \
  --fast_sanitize --n_jobs 8 --cache_scaffolds \
  --seed 17 --cuda_device 4
"""
import os, sys, re, json, argparse, random, types, time
from pathlib import Path
from typing import List, Tuple, Dict

import numpy as np
import pandas as pd

from rdkit import Chem, RDLogger
from rdkit.Chem import QED, AllChem
from rdkit.Chem.Scaffolds import MurckoScaffold

RDLogger.DisableLog("rdApp.*")

# ---------------- Small logger ----------------
def _now():
    import datetime as _dt
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def log(msg): print(f"[{_now()}] {msg}", flush=True)

# ---------------- SA scorer ----------------
def _ensure_sascorer():
    try:
        import sascorer  # type: ignore
        return sascorer
    except Exception:
        pass
    sc_path = os.environ.get("SASCORE_PY", "")
    if sc_path and os.path.isfile(sc_path):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("sascorer", sc_path)
            mod = importlib.util.module_from_spec(spec)
            assert spec and spec.loader
            spec.loader.exec_module(mod)  # type: ignore
            return mod
        except Exception as e:
            print(f"[WARN] Failed to import sascorer from {sc_path}: {e}", flush=True)
    print("[WARN] sascorer not found (set $SASCORE_PY). SA will be None.", flush=True)
    return None
_SASCORER = _ensure_sascorer()

# ---------------- Moses shim for MolGPT utils ----------------
def ensure_moses_shim():
    try:
        import moses.utils  # type: ignore
        return
    except Exception:
        pass
    moses_mod = types.ModuleType("moses")
    moses_utils_mod = types.ModuleType("moses.utils")
    def get_mol(smiles: str):
        try:
            return Chem.MolFromSmiles(smiles) if smiles else None
        except Exception:
            return None
    moses_utils_mod.get_mol = get_mol
    sys.modules["moses"] = moses_mod
    sys.modules["moses.utils"] = moses_utils_mod
    log("Injected moses shim")

# ---------------- MolGPT path helper ----------------
def ensure_molgpt_in_path(molgpt_root: Path) -> Path:
    root = Path(molgpt_root).resolve()
    def _ok(p: Path) -> bool:
        return (p / "model.py").exists() and (p / "utils.py").exists()
    if _ok(root):
        if str(root) not in sys.path: sys.path.insert(0, str(root))
        log(f"MolGPT repo fixed to: {root}")
        return root
    parent = root.parent
    if _ok(parent):
        if str(parent) not in sys.path: sys.path.insert(0, str(parent))
        log(f"MolGPT repo fixed to parent: {parent} (from {root})")
        return parent
    raise ImportError(f"MolGPT repo not found at {root} (expect model.py & utils.py)")

# ---------------- Tokenization helpers for MolGPT ----------------
SMI_TOKEN_PATTERN = r"(\[[^\]]+]|<|Br?|Cl?|N|O|S|P|F|I|b|c|n|o|s|p|\(|\)|\.|=|#|-|\+|\\|\/|:|~|@|\?|>|\*|\$|\%[0-9]{2}|[0-9])"
REGEX = re.compile(SMI_TOKEN_PATTERN)

def tokenizable_by_molgpt_as_is(scaf: str, stoi: dict, scaffold_maxlen: int) -> bool:
    toks = REGEX.findall(scaf)
    if not all(t in stoi for t in toks): return False
    return len(toks) <= scaffold_maxlen

def murcko_scaffold(smi: str):
    m = Chem.MolFromSmiles(smi)
    if m is None: return None
    sc = MurckoScaffold.GetScaffoldForMol(m)
    return Chem.MolToSmiles(sc, isomericSmiles=True)

# ---------------- Fingerprints & metrics ----------------
FP_BITS = 2048

def smiles_to_ecfp4(smi: str, n_bits: int = FP_BITS) -> np.ndarray | None:
    mol = Chem.MolFromSmiles(smi)
    if mol is None: return None
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=n_bits)
    arr = np.zeros((n_bits,), dtype=np.float32)
    AllChem.DataStructs.ConvertToNumpyArray(fp, arr)
    return arr

from concurrent.futures import ThreadPoolExecutor

def fp_batch(smiles: List[str], n_jobs=1) -> np.ndarray:
    if n_jobs and n_jobs != 1:
        if n_jobs <= 0:
            import os as _os
            n_jobs = max(1, (_os.cpu_count() or 4))
        with ThreadPoolExecutor(max_workers=n_jobs) as ex:
            fps = list(ex.map(smiles_to_ecfp4, smiles))
    else:
        fps = [smiles_to_ecfp4(s) for s in smiles]
    fps = [x for x in fps if x is not None]
    if not fps: raise ValueError("No valid SMILES in list for fingerprinting.")
    return np.vstack(fps)

def frechet_distance(X: np.ndarray, Y: np.ndarray) -> float:
    from scipy.linalg import sqrtm
    mu1, mu2 = X.mean(0), Y.mean(0)
    s1, s2 = np.cov(X, rowvar=False), np.cov(Y, rowvar=False)
    covmean = sqrtm(s1 @ s2)
    if np.iscomplexobj(covmean): covmean = covmean.real
    return float(np.sum((mu1 - mu2) ** 2) + np.trace(s1 + s2 - 2 * covmean))

def kl_hist(A: np.ndarray, B: np.ndarray, bins: int = 50) -> float:
    from scipy.stats import entropy
    max_bits = A.shape[1]
    hA, _ = np.histogram(A.sum(1), bins=bins, range=(0, max_bits), density=True)
    hB, _ = np.histogram(B.sum(1), bins=bins, range=(0, max_bits), density=True)
    return float(entropy(hA + 1e-10, hB + 1e-10))

# ---------------- QED/SA (fast option) ----------------
def _mol_from_smiles(s, fast=False):
    try:
        if fast:
            m = Chem.MolFromSmiles(s, sanitize=False)
            if m:  # lazy sanitize with error capture
                Chem.SanitizeMol(m, catchErrors=True)
            return m
        else:
            return Chem.MolFromSmiles(s)
    except Exception:
        return None

def props_qed_sa_means(smiles_list: List[str], fast=False, skip_sa=False, n_jobs=1) -> Tuple[float | None, float | None, int, int]:
    qed_vals, sa_vals = [], []
    if n_jobs and n_jobs != 1:
        if n_jobs <= 0:
            import os as _os
            n_jobs = max(1, (_os.cpu_count() or 4) // 2)
        with ThreadPoolExecutor(max_workers=n_jobs) as ex:
            mols = list(ex.map(lambda s: _mol_from_smiles(s, fast), smiles_list))
    else:
        mols = [_mol_from_smiles(s, fast) for s in smiles_list]
    for m in mols:
        if not m: continue
        try:
            q = float(QED.qed(m))
            if np.isfinite(q): qed_vals.append(q)
        except Exception:
            pass
        if (not skip_sa) and (_SASCORER is not None):
            try:
                sa = float(_SASCORER.calculateScore(m))
                if np.isfinite(sa): sa_vals.append(sa)
            except Exception:
                pass
    q_mean = float(np.mean(qed_vals)) if qed_vals else None
    s_mean = float(np.mean(sa_vals)) if sa_vals else None
    return q_mean, s_mean, len(qed_vals), len(sa_vals)

# ---------------- MolGPT meta (for scaffold length constraints) ----------------
import torch
def load_molgpt_meta(weight_path: Path, stoi_json: Path) -> Tuple[dict, int, int, bool, int]:
    try:
        state = torch.load(weight_path, map_location="cpu", weights_only=True)
    except TypeError:
        state = torch.load(weight_path, map_location="cpu")
    block_size = int(state["pos_emb"].shape[1]) if "pos_emb" in state else 54
    ckpt_mask = None
    for k in ("blocks.0.attn.mask", "blocks.0.attn.register_buffer_mask"):
        if k in state and isinstance(state[k], torch.Tensor):
            ckpt_mask = state[k]; break
    S_mask = int(ckpt_mask.shape[-1]) if ckpt_mask is not None else block_size
    has_prop = ("prop_nn.weight" in state)
    scaffold_maxlen = S_mask - block_size - (1 if has_prop else 0)
    stoi = json.load(open(stoi_json, "r"))
    vocab_size = int(state["head.weight"].shape[0]) if "head.weight" in state else len(stoi)
    return stoi, scaffold_maxlen, block_size, has_prop, vocab_size

# ---------------- GPT-2 (BASE/DPO) generation ----------------
from transformers import GPT2Tokenizer, GPT2LMHeadModel
@torch.inference_mode()
def load_gpt2_and_tok(ckpt_path: Path, cuda_index: int = 0):
    log(f"Loading GPT-2 from {ckpt_path} (cuda:{cuda_index}) …")
    TOK = GPT2Tokenizer.from_pretrained("gpt2")
    special = {}
    if TOK.pad_token is None:           special["pad_token"] = "[PAD]"
    if "[SEP]" not in TOK.get_vocab():  special["sep_token"] = "[SEP]"
    if TOK.eos_token in ("", None):     special["eos_token"] = "[EOS]"
    if special: TOK.add_special_tokens(special)
    model = GPT2LMHeadModel.from_pretrained(ckpt_path)
    model.resize_token_embeddings(len(TOK))
    model.config.pad_token_id = TOK.pad_token_id
    device = torch.device(f"cuda:{cuda_index}" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda":
        torch.cuda.set_device(cuda_index)
    log("GPT-2 loaded.")
    return TOK, model.to(device).eval(), device, TOK.sep_token

@torch.inference_mode()
def generate_n_gpt2(model, TOK, device, SEP, scaffold: str, n_per: int = 10, tries_factor: int = 40,
                      tag: str = "GPT2", idx: int | None = None, total: int | None = None):
    prompt = f"Scaffold: {scaffold} {SEP}"  # shorter prompt for speed
    if idx is not None and total is not None:
        log(f"[{tag}] scaff {idx}/{total} start")
    outs, tries, max_tries = [], 0, n_per * max(10, int(tries_factor))
    while len(outs) < n_per and tries < max_tries:
        ids = model.generate(
            **TOK(prompt, return_tensors="pt").to(device),
            do_sample=True, num_beams=1, temperature=1.05, top_p=0.95,
            repetition_penalty=1.1, max_new_tokens=64,
            eos_token_id=TOK.eos_token_id, pad_token_id=TOK.pad_token_id,
        )
        smi = TOK.decode(ids[0][-64:], skip_special_tokens=True).split()[0]
        m = Chem.MolFromSmiles(smi)
        if m: outs.append(Chem.MolToSmiles(m))
        tries += 1
        if tries % 5 == 0:
            if idx is not None and total is not None:
                log(f"[{tag}] scaff {idx}: tries={tries}, got={len(outs)}/{n_per}")
            else:
                log(f"[{tag}] tries={tries}, got={len(outs)}/{n_per} for scaffold")
    return outs

def eval_gpt2_scaffolded(scaffolds: List[str], ckpt_path: Path, n_per: int, cuda_index: int, tries_factor: int, tag: str = "GPT2"):
    TOK, M, device, SEP = load_gpt2_and_tok(ckpt_path, cuda_index=cuda_index)
    all_outs = []
    for i, sc in enumerate(scaffolds, 1):
        outs = generate_n_gpt2(M, TOK, device, SEP, sc, n_per=n_per, tries_factor=tries_factor, tag=tag, idx=i, total=len(scaffolds))
        all_outs.extend(outs)
    log(f"[{tag}] generation done: total={len(all_outs)}")
    return all_outs

# ---------------- MolGPT generation ----------------
@torch.inference_mode()
def eval_molgpt_scaffolded(scaffolds: List[str], weight_path: Path,
                           stoi_json: Path,
                           n_per: int, batch_size: int,
                           temperature: float, top_k: int,
                           cuda_index: int,
                           max_wall_per_scaffold_sec: int = 120,
                           max_tries_per_scaffold: int = 2000,
                           local_batch_override: int | None = None):
    ensure_moses_shim()
    from model import GPT, GPTConfig
    from utils import sample

    device = torch.device(f"cuda:{cuda_index}" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda":
        torch.cuda.set_device(cuda_index)

    try:
        state = torch.load(weight_path, map_location="cpu", weights_only=True)
    except TypeError:
        state = torch.load(weight_path, map_location="cpu")

    block_size = int(state["pos_emb"].shape[1]) if "pos_emb" in state else 54
    ckpt_mask = None
    for k in ("blocks.0.attn.mask", "blocks.0.attn.register_buffer_mask"):
        if k in state and isinstance(state[k], torch.Tensor):
            ckpt_mask = state[k]; break
    S_mask = int(ckpt_mask.shape[-1]) if ckpt_mask is not None else block_size
    has_prop = ("prop_nn.weight" in state)
    vocab_size = int(state["head.weight"].shape[0]) if "head.weight" in state else None

    scaf_max_model = S_mask - block_size - (1 if has_prop else 0)
    scaf_max_runtime = max(1, scaf_max_model - 1)

    stoi = json.load(open(stoi_json, "r"))
    itos = {i: ch for ch, i in stoi.items()}

    mconf = GPTConfig(
        vocab_size or len(stoi), block_size,
        num_props=(1 if has_prop else 0),
        n_layer=8, n_head=8, n_embd=256,
        scaffold=True, scaffold_maxlen=scaf_max_model,
        lstm=False, lstm_layers=0,
    )
    model = GPT(mconf)
    model.load_state_dict(state, strict=True)
    model.to(device).eval()

    # start token (heuristic)
    def choose_start_token(stoi_dict, rng=None):
        import random as _r
        rng = rng or _r
        cands = [t for t in ["C","c","N","O","S","P","F","I","("] if t in stoi_dict]
        return rng.choice(cands) if cands else rng.choice(list(stoi_dict.keys()))
    start_tok = choose_start_token(stoi)
    x_ctx_ids = [stoi[start_tok]]
    x_ctx = torch.tensor(x_ctx_ids, dtype=torch.long)[None, ...].repeat(batch_size, 1).to(device)

    # clamp top_k to vocab
    vocab_n = (vocab_size if vocab_size is not None else len(stoi))
    if top_k is None or int(top_k) <= 0:
        top_k_arg = None
    else:
        top_k_arg = int(min(int(top_k), max(1, int(vocab_n) - 1)))

    outs = []
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    torch.set_grad_enabled(False)

    for i, scaf in enumerate(scaffolds, 1):
        log(f"[MolGPT] scaff {i}/{len(scaffolds)} start")
        start_t = time.time()

        tokens = REGEX.findall(scaf)
        if any(t not in stoi for t in tokens):
            log(f"[MolGPT][WARN] scaffold {i} not tokenizable; skipping")
            continue
        tokens = tokens[:scaf_max_runtime]
        tokens_padded = tokens + ['<'] * max(0, (scaf_max_model - len(tokens)))
        sca_ids = [stoi[t] for t in tokens_padded[:scaf_max_model]]
        sca_tensor = torch.tensor(sca_ids, dtype=torch.long)[None, ...].repeat(batch_size, 1).to(device)

        target_n, tries = n_per, 0
        local_batch = min(batch_size, local_batch_override or 128)
        curr = []  # per-scaffold accumulator

        while len(curr) < target_n:
            # watchdogs
            if tries >= max_tries_per_scaffold:
                log(f"[MolGPT][WARN] giving up on scaff {i} after {tries} tries (curr={len(curr)}/{target_n})")
                break
            if time.time() - start_t > max_wall_per_scaffold_sec:
                log(f"[MolGPT][WARN] timeout on scaff {i} after {int(time.time()-start_t)}s (curr={len(curr)}/{target_n}); moving on")
                break

            # small-batch sampling
            x_ctx_local = x_ctx[:local_batch]
            sca_tensor_local = sca_tensor[:local_batch]
            try:
                y = sample(
                    model, x_ctx_local, block_size,
                    temperature=float(temperature), sample=True, top_k=top_k_arg,
                    prop=None if (not has_prop) else torch.full((local_batch, 1), 1.0, device=device),
                    scaffold=sca_tensor_local
                )
            except TypeError:
                y = sample(
                    model, x_ctx_local, block_size,
                    temperature=float(temperature), sample=True, top_k=top_k_arg,
                    prop=None if (not has_prop) else torch.full((local_batch, 1), 1.0, device=device),
                    scaffold=sca_tensor_local
                )
            for gen_ids in y:
                if len(curr) >= target_n:
                    break
                completion = ''.join([itos.get(int(i), '') for i in gen_ids]).replace('<','')
                m = Chem.MolFromSmiles(completion)
                if m:
                    curr.append(Chem.MolToSmiles(m, isomericSmiles=False))
            tries += 1
            if tries % 5 == 0:
                log(f"[MolGPT] scaff {i}: tries={tries}, got={len(curr)}/{target_n}")

        outs.extend(curr)
        if len(curr) < target_n:
            log(f"[MolGPT][INFO] scaff {i} finished with {len(curr)}/{target_n}")

    log(f"[MolGPT] generation done: total={len(outs)}")
    if len(outs) == 0:
        log("[MolGPT][WARN] No valid molecules generated. Consider tuning temperature/top_k or scaffold filter.")
    return outs

# ---------------- ZINC scaffolds & filtering ----------------
def extract_scaffolds_from_zinc_filtered(zinc_csv: Path, n_scaffolds: int, seed: int,
                                         stoi: dict, scaffold_maxlen: int) -> Tuple[List[str], Dict[str, str]]:
    log("Reading ZINC CSV & extracting Murcko scaffolds…")
    df = pd.read_csv(zinc_csv)
    df["smiles"] = df["smiles"].astype(str).str.strip()
    df = df[df["smiles"].apply(lambda s: Chem.MolFromSmiles(s) is not None)]
    df["scaffold"] = df["smiles"].map(murcko_scaffold)
    df = df.dropna(subset=["scaffold"])
    scaf_table = df.groupby("scaffold").first().reset_index()[["scaffold","smiles"]]
    log(f"Total unique scaffolds: {len(scaf_table)}")
    # stable order
    scaf_table = scaf_table.sort_values("scaffold", kind="mergesort").reset_index(drop=True)

    picked_scaffolds, picked_refs = [], []
    for _, row in scaf_table.iterrows():
        sc = row["scaffold"]
        if tokenizable_by_molgpt_as_is(sc, stoi, scaffold_maxlen):
            picked_scaffolds.append(sc)
            picked_refs.append(row["smiles"])
            if len(picked_scaffolds) >= n_scaffolds:
                break
    if len(picked_scaffolds) < n_scaffolds:
        raise ValueError(f"Only {len(picked_scaffolds)} scaffolds are MolGPT-tokenizable (need {n_scaffolds}).")
    ref_map = dict(zip(picked_scaffolds, picked_refs))
    log(f"Sampled {n_scaffolds} MolGPT-tokenizable scaffolds.")
    return picked_scaffolds, ref_map

# ---------------- Helpers ----------------
def load_ref2_smiles(csv_path: Path, smiles_col: str) -> List[str]:
    log(f"Reading reference-2 SMILES from {csv_path} (col='{smiles_col}') …")
    df = pd.read_csv(csv_path)
    if smiles_col not in df.columns:
        raise ValueError(f"Column '{smiles_col}' not in {csv_path}")
    smiles = df[smiles_col].astype(str).str.strip().tolist()
    smiles = [s for s in smiles if Chem.MolFromSmiles(s) is not None]
    log(f"Ref2 loaded: {len(smiles)} valid SMILES")
    return smiles

def align_by_scaff_multiple(gens: List[str], scs: List[str], n_per: int, ref_map: Dict[str, str]) -> Tuple[List[str], List[str]]:
    refs = []
    for sc in scs:
        if sc in ref_map:
            refs.extend([ref_map[sc]] * n_per)
    L = min(len(gens), len(refs))
    return gens[:L], refs[:L]

# ---------------- Main ----------------
def main():
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    ap = argparse.ArgumentParser()
    ap.add_argument("--zinc_csv",       type=Path, required=True)
    ap.add_argument("--out_dir",        type=Path, required=True)

    ap.add_argument("--base_ckpt",      type=Path, required=True)
    ap.add_argument("--dpo_ckpt",       type=Path, required=True)

    ap.add_argument("--molgpt_weight",  type=Path, required=True)
    ap.add_argument("--molgpt_stoi",    type=Path, required=True)
    ap.add_argument("--molgpt_root",    type=Path, required=True)

    ap.add_argument("--hgraph_smiles",  type=Path, default=None)  # unused in stats; left for parity

    ap.add_argument("--ref2_csv",       type=Path, required=True)
    ap.add_argument("--ref2_smiles_col",type=str,  default="smiles")

    ap.add_argument("--n_scaffolds",    type=int,  default=10)
    ap.add_argument("--n_per",          type=int,  default=10)
    ap.add_argument("--groups",         type=int,  default=10)
    ap.add_argument("--batch_size",     type=int,  default=512)
    ap.add_argument("--temperature",    type=float,default=0.9)
    ap.add_argument("--top_k",          type=int,  default=0)
    ap.add_argument("--seed",           type=int,  default=17)
    ap.add_argument("--cuda_device",    type=int,  default=0)

    # Speed / control options
    ap.add_argument("--max_wall_per_scaffold_sec", type=int, default=120)
    ap.add_argument("--max_tries_per_scaffold",    type=int, default=2000)
    ap.add_argument("--molgpt_local_batch",        type=int, default=128)
    ap.add_argument("--gpt2_max_tries_factor",     type=int, default=40)
    ap.add_argument("--fast_sanitize", action="store_true", help="Use sanitize=False then lazy sanitize to speed RDKit")
    ap.add_argument("--skip_sa", action="store_true", help="Skip SA calculation to speed up")
    ap.add_argument("--n_jobs", type=int, default=0, help="Parallel workers for metrics (0=auto, 1=no parallel)")
    ap.add_argument("--no_cache_scaffolds", action="store_true", help="Disable scaffold caching (enabled by default)")
    # internal: cache_scaffolds defaults to True unless --no_cache_scaffolds is set

    args = ap.parse_args()

    # default: cache enabled unless user disables it
    args.cache_scaffolds = not bool(getattr(args, 'no_cache_scaffolds', False))

    args.out_dir.mkdir(parents=True, exist_ok=True)

    random.seed(args.seed); np.random.seed(args.seed); torch.manual_seed(args.seed)

    # MolGPT path & meta
    ensure_molgpt_in_path(args.molgpt_root)
    stoi, scaffold_maxlen, _, _, vocab_size = load_molgpt_meta(args.molgpt_weight, args.molgpt_stoi)

    # Pre-load REF2 full list (reuse across groups)
    ref2_all = load_ref2_smiles(args.ref2_csv, args.ref2_smiles_col)

    # Prepare models once
    TOK_base, M_base, dev_base, SEP_base = load_gpt2_and_tok(args.base_ckpt, cuda_index=args.cuda_device)
    TOK_dpo,  M_dpo,  dev_dpo,  SEP_dpo  = load_gpt2_and_tok(args.dpo_ckpt,  cuda_index=args.cuda_device)

    # Results collectors
    per_group_rows = []

    for g in range(args.groups):
        seed_g = args.seed + g
        random.seed(seed_g); np.random.seed(seed_g); torch.manual_seed(seed_g)
        log(f"=== Group {g+1}/{args.groups} (seed={seed_g}) ===")

        # Select scaffolds (or load cached)
        cache_file = args.out_dir / f"scaffolds_group_{g+1}.json"
        if args.cache_scaffolds and cache_file.exists():
            try:
                _cache = json.load(open(cache_file, 'r'))
                scaffolds = _cache['scaffolds']
                zinc_ref_map = _cache['zinc_ref_map']
                log(f"Loaded cached scaffolds for group {g+1}")
            except Exception:
                scaffolds, zinc_ref_map = extract_scaffolds_from_zinc_filtered(
                    args.zinc_csv, args.n_scaffolds, seed_g, stoi, scaffold_maxlen
                )
        else:
            scaffolds, zinc_ref_map = extract_scaffolds_from_zinc_filtered(
                args.zinc_csv, args.n_scaffolds, seed_g, stoi, scaffold_maxlen
            )
            if args.cache_scaffolds:
                json.dump({"scaffolds": scaffolds, "zinc_ref_map": zinc_ref_map}, open(cache_file, 'w'))
                log(f"Cached scaffolds for group {g+1} → {cache_file}")

        # Generate BASE
        base_gen = []
        for i, sc in enumerate(scaffolds, 1):
            outs = generate_n_gpt2(M_base, TOK_base, dev_base, SEP_base, sc, n_per=args.n_per, tries_factor=args.gpt2_max_tries_factor, tag="BASE", idx=i, total=len(scaffolds))
            base_gen.extend(outs)
        # Generate DPO
        dpo_gen = []
        for i, sc in enumerate(scaffolds, 1):
            outs = generate_n_gpt2(M_dpo, TOK_dpo, dev_dpo, SEP_dpo, sc, n_per=args.n_per, tries_factor=args.gpt2_max_tries_factor, tag="DPO", idx=i, total=len(scaffolds))
            dpo_gen.extend(outs)
        # Generate MolGPT
        mgpt_gen = eval_molgpt_scaffolded(
            scaffolds=scaffolds,
            weight_path=args.molgpt_weight,
            stoi_json=args.molgpt_stoi,
            n_per=args.n_per,
            batch_size=args.batch_size,
            temperature=args.temperature,
            top_k=args.top_k,
            cuda_index=args.cuda_device,
            max_wall_per_scaffold_sec=args.max_wall_per_scaffold_sec,
            max_tries_per_scaffold=args.max_tries_per_scaffold,
            local_batch_override=args.molgpt_local_batch
        )

        # Align with ZINC refs by scaffold
        base_Z, zinc_Z = align_by_scaff_multiple(base_gen, scaffolds, args.n_per, zinc_ref_map)
        dpo_Z,  _      = align_by_scaff_multiple(dpo_gen,  scaffolds, args.n_per, zinc_ref_map)
        mgpt_Z, _      = align_by_scaff_multiple(mgpt_gen, scaffolds, args.n_per, zinc_ref_map)

        # Prepare REF2 matched slices (same order for fairness)
        rnd = random.Random(seed_g + 101)
        ref2_pool = ref2_all[:]  # copy
        rnd.shuffle(ref2_pool)
        ref2_base = ref2_pool[:len(base_Z)]
        ref2_dpo  = ref2_pool[:len(dpo_Z)]
        ref2_mgpt = ref2_pool[:len(mgpt_Z)]

        # Compute metrics per model & reference
        def compute_all(gen_list: List[str], refZ_list: List[str], ref2_list: List[str]):
            Q, S, nQ, nS = props_qed_sa_means(gen_list, fast=args.fast_sanitize, skip_sa=args.skip_sa, n_jobs=args.n_jobs)
            # fingerprints
            Xg   = fp_batch(gen_list, n_jobs=args.n_jobs)
            Xz   = fp_batch(refZ_list, n_jobs=args.n_jobs)
            Xr2  = fp_batch(ref2_list, n_jobs=args.n_jobs)
            fcd_z   = frechet_distance(Xg, Xz)
            fcd_r2  = frechet_distance(Xg, Xr2)
            kl_z    = kl_hist(Xg, Xz)
            kl_r2   = kl_hist(Xg, Xr2)
            return dict(qed_mean=Q, sa_mean=S, n_qed=nQ, n_sa=nS,
                        FCD_refZ=fcd_z, FCD_ref2=fcd_r2, KL_refZ=kl_z, KL_ref2=kl_r2)

        metrics_base = compute_all(base_Z, zinc_Z, ref2_base)
        metrics_dpo  = compute_all(dpo_Z,  zinc_Z, ref2_dpo)
        metrics_mgpt = compute_all(mgpt_Z, zinc_Z, ref2_mgpt)

        row_base = {"group": g+1, "model": "BASE"} | metrics_base
        row_dpo  = {"group": g+1, "model": "DPO"}  | metrics_dpo
        row_mgpt = {"group": g+1, "model": "MolGPT"} | metrics_mgpt
        per_group_rows.extend([row_base, row_dpo, row_mgpt])

    # Save per-group metrics
    df = pd.DataFrame(per_group_rows)
    csv_path = args.out_dir / "per_group_metrics_qed_sa_fcd_kl.csv"
    df.to_csv(csv_path, index=False)

    # Pairwise t-tests across groups (Welch's)
    from scipy.stats import ttest_ind
    pairs = [("BASE", "DPO"), ("BASE", "MolGPT"), ("DPO", "MolGPT")]
    metrics = ["qed_mean", "sa_mean", "FCD_refZ", "FCD_ref2", "KL_refZ", "KL_ref2"]
    ttest_out = {}
    for a,b in pairs:
        ttest_out[f"{a}_vs_{b}"] = {}
        A = df[df["model"] == a]
        B = df[df["model"] == b]
        for m in metrics:
            xa = A[m].dropna().to_numpy()
            xb = B[m].dropna().to_numpy()
            if len(xa) >= 2 and len(xb) >= 2:
                t, p = ttest_ind(xa, xb, equal_var=False)
                ttest_out[f"{a}_vs_{b}"][m] = {"t": float(t), "p": float(p),
                                               "mean_a": float(np.mean(xa)), "mean_b": float(np.mean(xb))}
            else:
                ttest_out[f"{a}_vs_{b}"][m] = {"t": None, "p": None, "mean_a": float(np.mean(xa)) if len(xa) else None,
                                               "mean_b": float(np.mean(xb)) if len(xb) else None}

    json_path = args.out_dir / "ttest_pairwise_summary.json"
    json.dump(ttest_out, open(json_path, "w"), indent=2)

    log(f"Saved per-group metrics → {csv_path}")
    log(f"Saved t-test summary   → {json_path}")
    log("Done.")

if __name__ == "__main__":
    main()
