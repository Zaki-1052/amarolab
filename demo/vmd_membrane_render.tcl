# demo/vmd_membrane_render.tcl
# VMD Tcl script for membrane protein figure rendering.
# Usage: cd to directory with files, then: source vmd_membrane_render.tcl
# Sets up the scene for review. Type `render_figure` when ready to render.

# ── Per-system configuration ──────────────────────────────────────────────────

set psf_file      "step5_assembly.psf"
set pdb_file      "step5_assembly.pdb"

# Change for each protein system
set ligand_sel    "resname 6DX"
set lipid_sel     "resname POPC POPE POPI POPS CHL1 and noh"
set output_name   "Figure_MOR_naloxone_membrane"

# ── Visual tuning ─────────────────────────────────────────────────────────────

# VMD ColorIDs: 0=blue, 1=red, 2=gray, 3=orange, 4=yellow, 7=green, 10=cyan
set protein_color    10
set ligand_color     4
set membrane_color   2

# 0.0 = invisible, 1.0 = solid; 0.10-0.20 works well on white backgrounds
set membrane_opacity 0.15

# Smaller = more zoomed out; 0.5 is good for receptor + G protein complexes
set view_scale       0.5

set render_width     2400
set render_height    1920

# ── Load structure (PSF first for proper topology) ────────────────────────────

mol delete all
mol new $psf_file
mol addfile $pdb_file

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
puts "Scene ready. Rotate/zoom to adjust, then type:"
puts "  render_figure"
puts ""
puts "Useful commands:"
puts "  mol showrep top 2 on          ;# show lipid sticks instead"
puts "  mol showrep top 3 off         ;# hide translucent membrane"
puts "  material change opacity Transparent 0.20  ;# adjust membrane opacity"
puts "  scale to 0.4                  ;# zoom out more"
puts "────────────────────────────────────────────────"
