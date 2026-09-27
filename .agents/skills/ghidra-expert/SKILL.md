---
name: ghidra-expert
description: Guides agents on Ghidra reverse-engineering - processors vs loaders, memory maps, Sleigh/cspec, and SNES/65816 edge cases. Use when working with Ghidra, disassembly, processor modules, loaders, LoROM, 65816, cspec/slaspec, offset mismatch, or Ghidra MCP.
---

# Ghidra Expert

Apply when the task involves Ghidra setup, SNES/65816 disassembly, processor modules, loaders, memory mapping, or fixing validation/import errors.

## Core Concepts

### Processors vs Loaders

| Role | What it does | Where it lives | Artifact |
|------|--------------|----------------|----------|
| **Processor module** | Defines CPU instruction set (opcodes, registers, addressing). | `Ghidra/Processors/<Name>/` (e.g. `65816`) | Folder with `data/languages/` (.cspec, .ldefs, .pspec, .slaspec, .sinc). |
| **Loader** | Recognizes file format and maps bytes into Ghidra memory (e.g. LoROM, header strip). | `Ghidra/Extensions/Ghidra/` (built extension) | Java extension (Gradle build). |

Use both for SNES: loader = correct addresses; processor = 65816 disassembly. Raw Binary + 65816 without a loader gives **offset mismatch** (file offset != SNES address).

### Memory Map and Addresses

- **Raw Binary import:** File offset = Ghidra address (flat). No LoROM layout; trace addresses (e.g. $8DED84) will not match.
- **SNES loader (LoROM):** Maps ROM into SNES bank layout so Ghidra addresses match console (e.g. $8DED84 in trace = $8DED84 in Ghidra). Handles .smc 512-byte header when present.
- **Processor options:** For 65816, set MF/XF/EF and register values (DBR, PBR, DP, SP) at entry points as needed.

## Main Functions (Quick Reference)

- **Import:** File → Import; choose format (e.g. SNES ROM via loader, or Raw Binary) and language (e.g. 65816).
- **Analysis:** Auto-analysis after import (or later); can disable and set memory map/entry points first.
- **Memory map:** Window → Memory Map; add blocks if not set by loader.
- **Processor options:** Right-click instruction → Processor Options (flags) or Set Register Values.
- **Symbols / labels:** Listing and Symbol Tree; create labels, functions, data.
- **Decompiler:** Per-function; quality depends on processor spec (65816 decompilation is often weak per upstream notes).
- **Extensions:** File → Install Extensions (ZIP); enable in File → Configure → Developer. Restart after install.

## Edge Cases and Fixes

### cspec validation (Ghidra 12+)

- **Error:** `unexpected attribute "type"` at line/column in .cspec (e.g. SleighLanguageValidator, BasicCompilerSpec).
- **Cause:** Older processor .cspec used `type="unknown"` on `<prototype>`; Ghidra 12 schema disallows it.
- **Fix:** Remove the `type="unknown"` attribute from the `<prototype>` tag in the processor's .cspec (e.g. `65816.cspec`). Leave other attributes (name, extrapop, stackshift, strategy).

### Extension version mismatch

- **Symptom:** "Version mismatch" when installing an extension (e.g. GhidraMCP, 65816) on newer Ghidra.
- **Typical outcome:** Extension often still loads; test before assuming failure. If it fails, update extension for current Ghidra API or use a fork that targets that version.

### Offset mismatch (SNES ROM)

- **Symptom:** Addresses in Ghidra do not match trace/docs (e.g. $8DED84).
- **Causes:** (1) Raw Binary import (flat mapping), (2) .smc header not stripped so all offsets shifted.
- **Fix:** Use an SNES loader that sets LoROM map and handles header; re-import the ROM with the loader.

### Loader default processor (65816 vs 6502)

- Some SNES loader forks changed default language from 65816 to 6502 "to enable detection." For real SNES (65816 CPU), keep or restore **65816** as the loader's default/expected language; 6502 is wrong for SNES.

### Processor module layout

- **Install:** Folder must be named exactly what the language expects (e.g. `65816`) and placed in `Ghidra/Processors/`. Release ZIPs can ship with top-level `65816/` for drag-and-drop.
- **Sleigh compile errors:** Unused or invalid labels in .slaspec can cause build failures; comment out or fix per fork (e.g. qwertymodo's 65816 Sleigh fix).

## Best Practices and Tricks

- **Assess analysis quality:** Use Program Tree / Memory Map and entropy or overview to spot unanalyzed, encrypted, or compressed regions.
- **Non-returning functions:** If a function never returns (e.g. exit, abort), mark it: right-click in decompiler → Edit Function Signature → check **No Return**. Stops Ghidra from treating following bytes as code.
- **Refine data types:** Improve decompilation by defining or correcting data types (structures, pointers) so the decompiler’s assumptions match the binary.
- **Version tracking:** For multiple builds of the same binary, use Version Tracking to copy comments, renames, and markup from one version to another via correlators.
- **Scripting:** Use Ghidra scripts (Python or Java) to automate analysis, rename in bulk, or emulate; headless for batch.
- **Emulator:** Built-in emulator can run code to decrypt strings or follow behavior; combine with scripts for repeatable workflows.

## Official Documentation and External Links

| Resource | URL / Path |
|----------|------------|
| **Ghidra official docs** (Getting Started, API, What’s New, 2026) | https://ghidradocs.com/ |
| **NSA Ghidra GitHub** (source, FAQ, DevGuide) | https://github.com/NationalSecurityAgency/ghidra |
| **Improving disassembly/decompilation** (PDF) | https://ghidra.re/ghidra_docs/GhidraClass/Advanced/improvingDisassemblyAndDecompilation.pdf |

## MCP and Companion Skills

| Resource | Purpose |
|----------|---------|
| **resonance7-ghidra MCP (this workspace)** | MCP server key in `.agents/mcp.json` is **resonance7-ghidra**. Use that server key when calling Ghidra MCP tools. Bridge: `projects/ghidra-tools/src/GhidraMCP-3.2.0/bridge_mcp_ghidra.py`. Guidance lives in this skill's MCP section. |
| **Game Boy / FFL** | Separate platform from SNES: DMG/LR35902, Game Boy memory maps, and FFL disassembly are out of scope for this skill. Consult the relevant workspace docs if available. |

## Workspace References

| Topic | Location |
|-------|----------|
| resonance7-ghidra MCP (bridge, server name, when to use) | This skill (MCP and Companion Skills section) + `projects/ghidra-tools/src/GhidraMCP-3.2.0/bridge_mcp_ghidra.py` |
| 65816 cspec (Ghidra 12 fix) | `ghidra_12.0.3_PUBLIC_.../Ghidra/Processors/65816/data/languages/65816.cspec` |
| Upstream processor (fork source) | achan1989/ghidra-65816 (archived); qwertymodo fork has Sleigh fix. |
| Upstream loader (fork source) | achan1989/ghidra-snes-loader (archived); ogarvey fork has 11.4 compat (revert 6502→65816); qwertymodo has API fix. |

## When to Use This Skill

- User asks about Ghidra, SNES disassembly, 65816, loaders, or processor modules.
- Errors during import (cspec, validation, Sleigh).
- Addresses in Ghidra not matching traces or docs (offset mismatch).
- Deciding between Raw Binary vs loader, or processor vs loader responsibilities.
- Setting up or troubleshooting Ghidra MCP (see MCP_SETUP.md and this skill's MCP section).

## What Not to Put Here

- Full Sleigh/slaspec syntax: use Ghidra docs or processor source.
- Step-by-step GUI clicks for every menu: only where it resolves an edge case or workspace workflow.
- Game-specific logic (e.g. Apocalypse Gaia hooks): that stays in session logs and project asm/docs.
