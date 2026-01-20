from pathlib import Path
import re
import shutil
import subprocess
import textwrap

WRAP_WIDTH = 100  # adjust for how "wide" you want your PDF text

PATIENT_RE = re.compile(r"^\s*patient\s*:\s*(.*)\s*$", re.IGNORECASE)
THERAPIST_RE = re.compile(r"^\s*therapist\s*:\s*(.*)\s*$", re.IGNORECASE)

def pick_pdf_engine() -> str:
    for engine in ("pdflatex", "xelatex", "lualatex"):
        if shutil.which(engine):
            return engine
    raise RuntimeError(
        "No LaTeX engine found (pdflatex/xelatex/lualatex).\n"
        "Install one on Ubuntu/Debian with:\n"
        "  sudo apt install texlive-latex-base texlive-latex-recommended texlive-fonts-recommended"
    )

def wrap_with_hanging_indent(prefix: str, content: str, width: int) -> str:
    """
    Wrap content to 'width' with a hanging indent so subsequent lines align
    under the content part (after 'prefix ').
    """
    prefix = prefix.rstrip()
    content = content.strip()

    if not content:
        return f"{prefix} "

    first_width = max(20, width - (len(prefix) + 1))
    first_line_parts = textwrap.wrap(
        content,
        width=first_width,
        break_long_words=False,
        break_on_hyphens=False,
    )
    if not first_line_parts:
        return f"{prefix} "

    lines = [f"{prefix} {first_line_parts[0]}"]
    indent = " " * (len(prefix) + 1)

    rest = " ".join(first_line_parts[1:]).strip()
    if rest:
        more = textwrap.wrap(
            rest,
            width=max(20, width - len(indent)),
            break_long_words=False,
            break_on_hyphens=False,
        )
        lines.extend([indent + s for s in more])

    return "\n".join(lines)

def number_exchanges(md_text: str, width: int = WRAP_WIDTH) -> str:
    """
    Turn:
      Patient: ...
      Therapist: ...
      Patient: ...
      Therapist: ...
    into:
      1.
      Patient: ...
      
      Therapist: ...
      
      2.
      ...
    Rules:
    - Start a new numbered block at each Patient line.
    - Therapist lines are included in the current block (if any).
    - Unknown lines are appended to the current block; if no block yet, kept as-is.
    """
    out = []
    n = 0
    in_block = False

    def start_block():
        nonlocal n, in_block
        if in_block:
            # blank line between blocks
            out.append("")
        n += 1
        out.append(f"[{n}]\n")
        in_block = True

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip()

        # preserve truly empty lines inside a block as a single blank line
        if not line.strip():
            if in_block and (not out or out[-1] != ""):
                out.append("")
            elif not in_block:
                out.append("")
            continue

        pm = PATIENT_RE.match(line)
        if pm:
            start_block()
            content = pm.group(1)
            out.append(wrap_with_hanging_indent("Patient:", content, width))
            out.append("")  # blank line between Patient and Therapist in the same block
            continue

        tm = THERAPIST_RE.match(line)
        if tm:
            # If a file starts with Therapist (weird), create a block anyway
            if not in_block:
                start_block()
            content = tm.group(1)
            out.append(wrap_with_hanging_indent("Therapist:", content, width))
            continue

        # Any other line: keep it, but if we're in a block, wrap it as plain text.
        if in_block:
            wrapped = textwrap.fill(
                line.strip(),
                width=width,
                break_long_words=False,
                break_on_hyphens=False,
            )
            out.append(wrapped)
        else:
            out.append(line)

    # ensure trailing newline
    return "\n".join(out).rstrip() + "\n"

def pandoc_to_pdf(md_path: Path, pdf_path: Path):
    engine = pick_pdf_engine()
    subprocess.run(
        [
            "pandoc",
            str(md_path),
            "-o",
            str(pdf_path),
            f"--pdf-engine={engine}",
            "--wrap=preserve",
        ],
        check=True,
    )

def process_directory(folder: Path):
    md_files = sorted(folder.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {folder.resolve()}")
        return

    for md_file in md_files:
        original = md_file.read_text(encoding="utf-8")
        transformed = number_exchanges(original, WRAP_WIDTH)

        numbered_md = md_file.with_name(md_file.stem + "_numbered.md")
        numbered_md.write_text(transformed, encoding="utf-8")

        pdf_path = md_file.with_suffix(".pdf")
        pandoc_to_pdf(numbered_md, pdf_path)

        print(f"✔ {md_file.name} -> {numbered_md.name} -> {pdf_path.name}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 md_to_pdf.py <folder>")
        raise SystemExit(1)
    process_directory(Path(sys.argv[1]))
