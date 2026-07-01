# analysis/phase7_summary/vmd_render_snapshot.tcl
# Renders the 5-HT2A equilibrated snapshot (membrane or receptor-only).
# Usage: cd to this directory, then: source vmd_render_snapshot.tcl

# ── Choose which snapshot to render ───────────────────────────────────────────
# Option A: receptor + membrane (translucent membrane figure)
# Option B: receptor + psilocin only (clean crystal-structure-style figure)
# Option C: receptor only (no ligand)
# Comment/uncomment the set lines below to pick one.

# Option A
set pdb_file    "5ht2ar_membrane_snapshot.pdb"
set has_membrane 1
set output_name "Figure_5HT2A_psilocin_membrane"

# Option B (uncomment these and comment Option A to switch)
# set pdb_file    "5ht2ar_receptor_psilocin.pdb"
# set has_membrane 0
# set output_name "Figure_5HT2A_psilocin_receptor"

# Option C
# set pdb_file    "5ht2ar_receptor_snapshot.pdb"
# set has_membrane 0
# set output_name "Figure_5HT2A_receptor"

# ── Per-system configuration ──────────────────────────────────────────────────

set ligand_sel  "resname LIG"

# Snapshot lipid resnames have an X suffix from MDAnalysis export
set lipid_sel   "resname POPCX POPEX POPIX POPSX DOPCX PAPCX PAPEX PAPSX SDPCX SDPEX SDPSX SAPIX CHL1X BGALX CER1X PSM SSM and noh"

# ── Visual tuning ─────────────────────────────────────────────────────────────

set protein_color    10
set ligand_color     4
set membrane_color   2
set membrane_opacity 0.15
set view_scale       0.5
set render_width     2400
set render_height    1920

# ── Load structure (PDB only, no PSF) ─────────────────────────────────────────

mol delete all
mol new $pdb_file

# ── Representations ───────────────────────────────────────────────────────────

mol delrep 0 top

# Rep 0: protein
mol representation NewCartoon
mol selection {protein}
mol material AOChalky
mol color ColorID $protein_color
mol addrep top

# Rep 1: ligand
mol representation Licorice 0.3 12.0 12.0
mol selection "$ligand_sel"
mol material AOChalky
mol color ColorID $ligand_color
mol addrep top

if {$has_membrane} {
    # Rep 2: lipids as licorice (off by default; toggle with: mol showrep top 2 on)
    mol representation Licorice 0.1 12.0 12.0
    mol selection "$lipid_sel"
    mol material AOChalky
    mol color ResType
    mol addrep top
    mol showrep top 2 off

    # Rep 3: membrane as translucent QuickSurf
    mol representation QuickSurf 1.0 0.5 1.0 1.0
    mol selection "$lipid_sel"
    mol material Transparent
    mol color ColorID $membrane_color
    mol addrep top
}

# ── Display ───────────────────────────────────────────────────────────────────

display backgroundgradient off
color Display Background white

light 0 on
light 1 on
light 2 off
light 3 off

display cuemode Linear
display cuestart 0.50
display cueend 10.00
display shadows on
display ambientocclusion on
display aoambient 0.90
display aodirect 0.40

material change opacity Transparent $membrane_opacity

# ── View ──────────────────────────────────────────────────────────────────────

display resetview
rotate x by 90
scale to $view_scale
axes location Off
rock off
display resize $render_width $render_height

# ── Render helper ─────────────────────────────────────────────────────────────

proc render_figure {} {
    global output_name
    puts "Rendering to ${output_name}.ppm (this may take a few minutes)..."
    render TachyonInternal ${output_name}.ppm
    exec magick ${output_name}.ppm ${output_name}.png
    file delete ${output_name}.ppm
    puts "Done: ${output_name}.png"
}

puts "────────────────────────────────────────────────"
puts "Loaded: $pdb_file"
puts "Scene ready. Rotate/zoom to adjust, then type:"
puts "  render_figure"
puts "────────────────────────────────────────────────"
