import hou
import json
import re
import os

# Only these keys are allowed in the JSON (match your style)
ALLOWED_BASES = {
    "RS_aovSuffix",
    "RS_aovID",
    "RS_aovMaterialDenoise",
    "RS_aovCryptomatteType",
    "RS_aovCustomShader",
    "RS_aovCustomDT",
}

def to_jsonable(val):
    if isinstance(val, tuple):
        return list(val)
    return val

def export_filtered_rs_aovs(node, output_path=None):
    if node is None:
        raise RuntimeError("No node provided.")
    if node.type().name() != "Redshift_AOVs":
        raise RuntimeError(f"Selected node is '{node.type().name()}', not 'Redshift_AOVs'.")

    # Match RS_<something>_<index>
    rx = re.compile(r"^(RS_[A-Za-z0-9_]+)_(\d+)$")
    grouped = {}  # idx -> { parm_name: value }

    for p in node.parms():
        m = rx.match(p.name())
        if not m:
            continue
        base, idx = m.group(1), int(m.group(2))
        if base not in ALLOWED_BASES:
            continue

        try:
            val = p.eval()
        except hou.OperationFailed:
            continue

        v = to_jsonable(val)
        if isinstance(v, float) and v.is_integer():
            v = int(v)

        grouped.setdefault(idx, {})
        grouped[idx][p.name()] = v

    # Build ordered list by index; require at least Suffix & ID
    aov_list = []
    for idx in sorted(grouped.keys()):
        entry = grouped[idx]
        has_suffix = f"RS_aovSuffix_{idx}" in entry
        has_id = f"RS_aovID_{idx}" in entry
        if not (has_suffix and has_id):
            continue  # skip incomplete rows

        # Keep only allowed keys for this index (already filtered),
        # but re-order for nice readability: Suffix, ID, MaterialDenoise, then the optional ones
        ordered = {}
        for key in (f"RS_aovSuffix_{idx}", f"RS_aovID_{idx}", f"RS_aovMaterialDenoise_{idx}",
                    f"RS_aovCryptomatteType_{idx}", f"RS_aovCustomShader_{idx}", f"RS_aovCustomDT_{idx}"):
            if key in entry:
                ordered[key] = entry[key]

        aov_list.append(ordered)

    payload = {"aovs": aov_list}
    text = json.dumps(payload, indent=4)

    # Copy to clipboard
    try:
        hou.ui.copyTextToClipboard(text)
    except Exception:
        pass

    # Write to file if requested
    if output_path:
        with open(output_path, "w") as f:
            f.write(text)
        print(f"✅ Exported Redshift AOVs to {output_path}")

    # Also print to the Python Shell
    print(text)
    return text

# --- Run on the first selected node
sel = hou.selectedNodes()
if not sel:
    raise RuntimeError("Select a Redshift_AOVs node first.")

# Choose export path (change as needed)
path = hou.ui.selectFile(title="Save AOV JSON", file_type=hou.fileType.Any, collapse_sequences=False)
path = hou.expandString(path) if path else None
export_filtered_rs_aovs(sel[0], path)
