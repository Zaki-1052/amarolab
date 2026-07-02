# charmm-gui/vmd_trajectory.tcl
# Loads the 10 ns production trajectory and sets up publication-quality representations.
# Usage: cd to amarolab/, then: source charmm-gui/vmd_trajectory.tcl
# Note: loading 10 DCDs on 280K atoms takes a minute. QuickSurf membrane is slow; allow 30-60s.

# ── Per-system configuration ──────────────────────────────────────────────────

set psf_file    "openmm/step5_input.psf"
set num_dcds    10
set dcd_prefix  "openmm/step7"

set receptor_sel "segname PROA PROB PROC"
set gprotein_sel "segname PROD PROE PROF PROG PROH PROI PROJ"
set ligand_sel   "segname HETA"
set lipid_sel    "segname MEMB and noh"

set output_dir   "renders"
set output_name  "trajectory"

# ── Visual tuning ─────────────────────────────────────────────────────────────

set gprotein_color   3
set membrane_color   2
set membrane_opacity 0.15

set view_scale       0.35
set render_width     2400
set render_height    1920

# ── Load structure and trajectory ─────────────────────────────────────────────

mol delete all
mol new $psf_file type psf

for {set i 1} {$i <= $num_dcds} {incr i} {
    puts "Loading ${dcd_prefix}_${i}.dcd ..."
    mol addfile ${dcd_prefix}_${i}.dcd type dcd waitfor all
}

puts "Loaded [molinfo top get numframes] frames."

# ── PBC wrapping ──────────────────────────────────────────────────────────────

package require pbctools
pbc wrap -center com -centersel "protein" -compound residue -all
puts "PBC wrapping complete."

# ── Representations ───────────────────────────────────────────────────────────

mol delrep 0 top

# Rep 0: receptor cartoon, colored by segment (PROA/PROB/PROC each get a color)
mol representation NewCartoon 0.3 10.0 4.1 0
mol selection "$receptor_sel"
mol material AOChalky
mol color SegName
mol addrep top

# Rep 1: G protein cartoon, single color
mol representation NewCartoon 0.3 10.0 4.1 0
mol selection "$gprotein_sel"
mol material AOChalky
mol color ColorID $gprotein_color
mol addrep top

# Rep 2: psilocin as licorice, colored by element
mol representation Licorice 0.3 12.0 12.0
mol selection "$ligand_sel"
mol material AOChalky
mol color Name
mol addrep top

# Rep 3: lipid sticks (off by default; toggle with: mol showrep top 3 on)
mol representation Licorice 0.1 12.0 12.0
mol selection "$lipid_sel"
mol material AOChalky
mol color ResType
mol addrep top
mol showrep top 3 off

# Rep 4: membrane as translucent QuickSurf
mol representation QuickSurf 1.0 0.5 2.0 1.0
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

# ── Render helpers ────────────────────────────────────────────────────────────

proc render_frame {{suffix ""}} {
    global output_dir output_name
    set f [molinfo top get frame]
    if {$suffix eq ""} {
        set suffix "frame${f}"
    }
    set base "${output_dir}/${output_name}_${suffix}"
    puts "Rendering to ${base}.ppm ..."
    render TachyonInternal ${base}.ppm
    exec magick ${base}.ppm ${base}.png
    file delete ${base}.ppm
    puts "Done: ${base}.png"
}

proc goto {f} {
    animate goto $f
    puts "Frame $f / [expr {[molinfo top get numframes] - 1}]"
}

puts "────────────────────────────────────────────────"
puts "Trajectory loaded: [molinfo top get numframes] frames"
puts ""
puts "Navigation:"
puts "  goto 0                        ;# jump to frame"
puts "  goto [expr {[molinfo top get numframes] - 1}]   ;# last frame"
puts ""
puts "Rendering:"
puts "  render_frame                  ;# render current frame (auto-named)"
puts "  render_frame side_first       ;# render with custom suffix"
puts ""
puts "Useful toggles:"
puts "  mol showrep top 3 on          ;# show lipid sticks"
puts "  mol showrep top 4 off         ;# hide translucent membrane"
puts "  material change opacity Transparent 0.20  ;# adjust membrane opacity"
puts "────────────────────────────────────────────────"
