# AGENTS.md — Mt. Abu 1.2m Slit Spectrograph, Tip-Tilt Guider & Annular Field Imager

## 1. Mission & Engineering Context
You are assisting an instrumentation engineer at the **Physical Research Laboratory (PRL), Mount Abu Observatory (Gurushikhar)** in building a **3D mechanical & optical CAD assembly in FreeCAD** (using FreeCAD Python scripting and vendor `.step` files) for a Cassegrain instrument on the **Mt. Abu 1.2m Telescope**.

### Core Telescope & Environment Parameters
- **Telescope:** Mt. Abu 1.2m Cassegrain ($D_{\text{tel}} = 1200\text{ mm}$)
- **Focal Ratio:** $f/13$ ($f_{\text{tel}} = 15,600\text{ mm}$, marginal cone half-angle $= 2.20^\circ = 38.4\text{ mrad}$)
- **Focal-Plane Plate Scale:** **$13.2\text{ arcsec/mm}$** (**$75.63\ \mu\text{m/arcsec}$**; $1.0\text{ arcmin} = 4.538\text{ mm}$)
- **Cassegrain Mounting Flange & Back-Focus:** Telescope mounting flange sits at **$Z = -350\text{ mm}$** ($350\text{ mm}$ upstream of focal plane $Z = 0$), with an axial travel range of **$Z = -300\text{ mm}$ to $Z = -400\text{ mm}$** ($\pm 50\text{ mm}$ travel via slotted rails or spacer spools to accommodate commissioning focus uncertainty).
- **Flange Clear Aperture:** Flange opening and entrance baffle tube must be **$\ge 85\text{–}100\text{ mm}$ ID** (at $Z = -400\text{ mm}$, the $f/13$ cone expands by $30.8\text{ mm}$ over the $43.3\text{ mm}$ full-frame sensor diagonal, requiring $\ge 74.1\text{ mm}$ unvignetted optical aperture).
- **Observatory Environment:** Unheated dome at Gurushikhar; winter operating temperatures reach **$0^\circ\text{C}$ to $+5^\circ\text{C}$**. All actuators/optics must tolerate $\le 0^\circ\text{C}$ (piezo stages rated $-20^\circ\text{C}$ to $+80^\circ\text{C}$ are mandatory; voice-coil stages rated $\ge +5^\circ\text{C}$ are excluded).

### Three-Branch Optical Architecture
1. **Branch A — Pierced Pick-Off Mirror & Annular Field Imager (Acquisition):**
   - A $\varnothing 50.8\text{ mm}$ ($2''$) protected-silver flat mirror (`M1`) sits at the telescope $f/13$ primary focus at $45^\circ$, with a central **$\varnothing 4.6\text{ mm}$ ($1.0\text{ arcmin}$) hole** bored at $45^\circ$ (parallel to the incoming telescope beam).
   - The surrounding **annular field ($1.0'$ inner hole $\rightarrow 7.93' \times 5.29'$ outer box)** reflects into a **1:1 macro relay (William Optics RedCat 51 WIFD, $f=250\text{ mm}$)** onto a **Full-Frame Monochrome CMOS camera (ZWO ASI6200MM Pro, $36 \times 24\text{ mm}$)** for field identification and offset star acquisition.
2. **Branch B — Fine Guiding & Calibration Injection (Post-Hole):**
   - Light passing through the $\varnothing 4.6\text{ mm}$ hole enters a **1:1 pupil relay** ($f=130\text{ mm}$ doublets `L1`, `L2`) placing a **$10.0\text{ mm}$ collimated pupil** onto a **PI S-335.2SHM2 Fast Steering Mirror** ($70\text{ mrad}$ optical throw $= 2.0\text{ arcmin}$ sky range, giving $2.0\times$ margin over the $1.0'$ field and $0\%$ pupil walk on the spectrograph grating).
   - Downstream of `L2`, a **motorized flip mirror (`MFF101/M`)** injects $f/13$ calibration lamp light on demand, followed by a **92%T / 8%R pellicle beamsplitter** sending 8% to a high-speed fine-guider camera (`ZWO ASI290MM Mini`) that closes the optical tip-tilt loop at $1\text{–}20\text{ Hz}$, and 92% to the spectrograph slit.
3. **Branch C — Low-Resolution Slit Spectrograph ($R \approx 500$):**
   - A **$150\ \mu\text{m} \times 3\text{ mm}$ air slit (`S150R`, $2.0''$ seeing)** feeds a **$f = 200\text{ mm}$ collimator (`L_COL`)** ($15.4\text{ mm}$ collimated pupil) $\rightarrow$ **$600\text{ lines/mm}$ @ $600\text{ nm}$ VPH transmission grating (`VPH`)** ($20.8^\circ$ total beam deviation, Littrow $\alpha=\beta=10.4^\circ$) $\rightarrow$ **$f = 100\text{ mm}$ camera doublet (`L_CAM`)** ($0.5\times$ demagnification, $f/6.5$) $\rightarrow$ **APS-C Cooled Monochrome CMOS camera (`ZWO ASI2600MM Pro`, $23.5 \times 15.7\text{ mm}$)** capturing $450\text{–}750\text{ nm}$ across $18.3\text{ mm}$ at $R \approx 480\text{–}530$.

---

## 2. Non-Negotiable Optical & Mechanical Design Rules
1. **Optical vs. Mechanical Deflection ($2\times$ Rule):** Reflected beam deflection is always twice the mirror mechanical tilt ($\theta_{\text{opt}} = 2\,\theta_{\text{mech}}$).
2. **$45^\circ$ Projected Clear Aperture:** Any circular optic tilted at $45^\circ$ shrinks by $\cos 45^\circ = 0.7071$ along the fold axis. Never place a $0.5''$ ($12.5\text{ mm}$) mirror in a $9\text{–}15\text{ mm}$ beam at $45^\circ$; always use **$\varnothing 25.4\text{ mm}$ ($1''$)** or **$\varnothing 50.8\text{ mm}$ ($2''$)** optics.
3. **Angled Hole on Pierced Mirror (`M1`):** The $\varnothing 4.6\text{ mm}$ hole in `M1` MUST be bored **parallel to the incoming telescope beam ($+Z$, at $45^\circ$ to the mirror surface)** with a $45^\circ$ rear countersink/chamfer. Drilling perpendicular ($90^\circ$) to the $9.5\text{ mm}$-thick glass creates an internal cylinder wall that vignettes the $1.0'$ central field.
4. **Pellicle Beamsplitter Only:** Because `BS` sits in a converging $f/13$ cone, it MUST be a **$2\text{–}5\ \mu\text{m}$ nitrocellulose pellicle** (`BP108` / `#39-480`). Never substitute a thick plate or cube beamsplitter (which introduces severe astigmatism, coma, and ghosting).
5. **Order-Sorting Filter:** Include a $\varnothing 50.8\text{ mm}$ **GG400 / GG420 longpass filter** ahead of the slit or camera lens to block second-order UV/blue light ($\lambda < 400\text{ nm}$) from overlapping $700\text{–}750\text{ nm}$.
6. **Monolithic Optical Baseplate:** Bolt all post-FSM spectrograph components (`SLIT -> L_COL -> VPH -> L_CAM -> C_SPEC`) onto a single **$10\text{–}12\text{ mm}$ CNC-milled 6061-T6 aluminum deck** inside the instrument tub so gravitational flexure across telescope elevation angles remains $< 1$ binned pixel ($< 15\ \mu\text{m}$).
7. **Incoming Telescope Beam Keep-Out Cone:** Define a strictly forbidden keep-out frustum from **$Z = -400\text{ mm}$ ($\varnothing 85\text{ mm}$)** tapering to **$Z = 0\text{ mm}$ ($\varnothing 55\text{ mm}$)** along `(0, 0, +1)`. No non-pierced component (folded RedCat 51, fold mirror, truss struts, brackets, wiring) may intrude inside this cone (`distToShape >= 2.0 mm`).
8. **Commissioning Focus Travel ($\pm 50\text{ mm}$):** The internal optical chassis mounts to the $Z = -350\text{ mm}$ Cassegrain flange via slotted axial guide rails ($Z \in [-400, -300]\text{ mm}$) or bolted spacer spools to accommodate the $30\text{–}40\text{ cm}$ focus uncertainty at first light without re-machining the instrument tub.

---

## 3. Master COTS Bill of Materials & Official CAD / Product Links

| ID | Subsystem | Component & Model | Vendor & SKU | Key Dimensions & Optical Spec | Official Product & CAD Links |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **M1** | Pick-Off | **Pierced Flat Mirror** (Custom mod of $2''$ Protected-Ag flat) | Thorlabs `PF20-03-P01` (base blank) | $\varnothing 50.8\text{ mm} \times 9.5\text{ mm}$ thick; $\varnothing 4.6\text{ mm}$ hole bored at $45^\circ$ + rear chamfer | [Thorlabs PF20-03-P01 (STEP)](https://www.thorlabs.com/thorproduct.cfm?partnumber=PF20-03-P01) |
| **M_F1** | Annular Imager | **$2''$ Annular Fold Mirror + Kinematic Mount** | Thorlabs `PF20-03-P01` + `KM200` | $\varnothing 50.8\text{ mm}$ protected-Ag mirror; folds 1:1 RedCat path into compact tub | [Thorlabs KM200 (STEP)](https://www.thorlabs.com/thorproduct.cfm?partnumber=KM200) |
| **L_RC** | Annular Imager | **William Optics RedCat 51 WIFD** ($f=250\text{ mm}$, $f/4.9$ Petzval) | William Optics (`RedCat 51 WIFD`) | Length $346\text{ mm}$, Dew shield $\varnothing 80\text{ mm}$, M48/M54 rear thread; used at **1:1 conjugate** ($500\text{ mm}$ obj / $500\text{ mm}$ img) | [WO RedCat 51 WIFD Page](https://williamoptics.com/products/redcat-51-wifd) *(Model as stepped cylinder from 2D manual)* |
| **C_FF** | Annular Imager | **ZWO ASI6200MM Pro** (Full-Frame Mono, IMX455) | ZWO (`ASI6200MM-P`) | Body $\varnothing 90\text{ mm} \times 97\text{ mm}$ L; $17.5\text{ mm}$ flange-to-sensor; M54x0.75 female | [ZWO Manuals & STEP Downloads](https://www.zwoastro.com/downloads/manuals) |
| **L1, L2** | 1:1 Pupil Relay | **$\varnothing 30\text{ mm}$, $f = 130\text{ mm}$ Achromatic Doublets** ($\times 2$) | Edmund Optics `#49-361` / Thorlabs `AC300-130` | $\varnothing 30\text{ mm}$ OD; forms $10.0\text{ mm}$ collimated pupil at `FSM` and restores $f/13$ at `SLIT` | [Edmund Optics #49-361 (STEP)](https://www.edmundoptics.com/p/30mm-dia-x-130mm-fl-vis-0deg-coated-achromatic-lens/12095/) |
| **FSM** | Tip-Tilt Stage | **PI S-335.2SHM2** Piezo Tip/Tilt Platform w/ $1''$ Mirror | Physik Instrumente (`S-335.2SHM2`) | $70\text{ mrad}$ opt. ($35\text{ mrad}$ mech.) range; $\varnothing 25.4\text{ mm}$ mirror; $-20^\circ\text{C}$ to $+80^\circ\text{C}$ | [PI S-335 Product & CAD Page](https://www.pi-usa.us/en/products/fast-steering-mirrors-fsm-and-piezo-tiptilt-platforms-for-active-optics/s-335-piezo-tip-tilt-platform-202300) |
| **DRV** | Tip-Tilt Driver | **3-Ch $0\text{–}120\text{ V}$ Open-Loop Piezo Amplifier + 16-Bit DAC** | Thorlabs `MDT693B` + `NI USB-6002` | $\ge 20\text{ mA}$/ch; closed optically via 8% guider camera feedback loop | [Thorlabs MDT693B Page](https://www.thorlabs.com/thorproduct.cfm?partnumber=MDT693B) |
| **M_CAL** | Calibration | **Motorized Flip Mirror + $1''$ Protected-Ag Mirror** | Thorlabs `MFF101/M` + `PF10-03-P01` | $90^\circ$ motorized flipper; injects $f/13$ calibration light ahead of `BS` | [Thorlabs MFF101/M (STEP)](https://www.thorlabs.com/thorproduct.cfm?partnumber=MFF101/M) |
| **BS** | Guider Split | **$\varnothing 25.4\text{ mm}$ 8R / 92T Pellicle Beamsplitter + Mount** | Edmund Optics `#39-480` / Thorlabs `BP108` + `CM1-DCH/M` | $\varnothing 25.4\text{ mm}$ clear aperture; $45^\circ$ kinematic pellicle mount | [EO #39-480](https://www.edmundoptics.com/p/254mm-clear-aperture-8r92t-pellicle-beamsplitter/11840/) \| [Thorlabs BP108 (STEP)](https://www.thorlabs.com/thorproduct.cfm?partnumber=BP108) |
| **C_GD** | Fine Guider | **ZWO ASI290MM Mini** (or **ASI174MM Mini**) | ZWO (`ASI290MM-Mini`) | $1.25''$ barrel ($\varnothing 31.75\text{ mm} \times 61\text{ mm}$ L); $8.5\text{ mm}$ backfocus; $2.9\ \mu\text{m}$ px | [ZWO Manuals & STEP Downloads](https://www.zwoastro.com/downloads/manuals) |
| **SLIT** | Spectrograph | **$150\ \mu\text{m} \times 3\text{ mm}$ Precision Mounted Air Slit** | Thorlabs `S150R` / EO `#38-561` | $\varnothing 25.4\text{ mm}$ ($1''$) housing; $2.0'' \times 40''$ sky aperture at $f/13$ | [Thorlabs S150R (STEP)](https://www.thorlabs.com/thorproduct.cfm?partnumber=S150R) |
| **FLT** | Spectrograph | **$\varnothing 50.8\text{ mm}$ GG400 Longpass Order-Sorting Filter** | Thorlabs `FGL400M` / EO `#46-055` | Cuts $\lambda < 400\text{ nm}$ to prevent 2nd-order overlap at $700\text{–}750\text{ nm}$ | [Thorlabs FGL400M (STEP)](https://www.thorlabs.com/thorproduct.cfm?partnumber=FGL400M) |
| **L_COL** | Spectrograph | **$\varnothing 30\text{ mm}$, $f = 200\text{ mm}$ Achromatic Doublet** | Thorlabs `AC300-200-A` / EO `#49-364` | $\varnothing 30\text{ mm}$ OD; produces $15.4\text{ mm}$ collimated pupil | [Thorlabs AC300-200-A (STEP)](https://www.thorlabs.com/thorproduct.cfm?partnumber=AC300-200-A) |
| **VPH** | Spectrograph | **$600\text{ lines/mm}$ @ $600\text{ nm}$ CWL VPH Grating** | Wasatch Photonics (`600 l/mm @ 600 nm`, $2''$) | $\varnothing 50.8\text{ mm} \times 6.0\text{ mm}$ thick; Littrow $\alpha=\beta=10.4^\circ$ ($20.8^\circ$ total bend) | [Wasatch VPH Astronomical Gratings](https://wasatchphotonics.com/product-category/gratings/astronomy/) |
| **M_VPH** | Spectrograph | **$2''$ Rotation Stage + Kinematic Grating Mount** | Thorlabs `PR01/M` + `KM200PM/M` | Sets $10.4^\circ$ grating tilt and fine-tunes central wavelength | [Thorlabs PR01/M (STEP)](https://www.thorlabs.com/thorproduct.cfm?partnumber=PR01/M) \| [KM200PM/M (STEP)](https://www.thorlabs.com/thorproduct.cfm?partnumber=KM200PM/M) |
| **L_CAM** | Spectrograph | **$\varnothing 50.8\text{ mm}$, $f = 100\text{ mm}$ Achromatic Doublet** | Thorlabs `AC508-100-A` / EO `#49-283` | $\varnothing 50.8\text{ mm}$ ($2''$) OD prevents vignetting of dispersed blue/red edges | [Thorlabs AC508-100-A (STEP)](https://www.thorlabs.com/thorproduct.cfm?partnumber=AC508-100-A) |
| **C_SPEC** | Spectrograph | **ZWO ASI2600MM Pro** (APS-C Cooled Mono, IMX571) | ZWO (`ASI2600MM-P`) | Body $\varnothing 90\text{ mm} \times 97\text{ mm}$ L; $17.5\text{ mm}$ flange-to-sensor; $23.5 \times 15.7\text{ mm}$ sensor | [ZWO Manuals & STEP Downloads](https://www.zwoastro.com/downloads/manuals) |

---

## 4. Global 3D Coordinate System & Exact Station Anchors
To prevent spatial overlaps (`M1` colliding with `FSM`, or RedCat colliding with the spectrograph) and wrong mirror orientations, **every FreeCAD script MUST use this right-handed global coordinate frame**:

- **Global Origin `(0, 0, 0)`:** Center of the **$\varnothing 4.6\text{ mm}$ hole** on the front reflective face of `M1` (coincident with the Mt. Abu 1.2m $f/13$ primary focal plane).
- **`+Z` Axis `(0, 0, +1)`:** Direction of incoming light from the telescope primary mirror.
- **Plane Separation Rule (Guaranteed Zero Overlap):**
  - **Branch A (Annular Imager)** operates exclusively in **`Z = 0, X >= 0, Y <= 0`**.
  - **Relay (`L1 -> FSM`)** travels along **`X = 0, Y = 0, Z in [0, +260]`** (`260 mm` separation between `M1` and `FSM`).
  - **Branch B/C (Post-FSM Guider & Spectrograph)** operates exclusively in **`Z >= +260, Y >= 0`**.

| Station ID | Optical Center `(X, Y, Z)` (mm) | Incoming Ray Dir | Outgoing Ray Dir | Mirror / Grating Surface Normal $\mathbf{n}$ |
| :--- | :--- | :--- | :--- | :--- |
| **`M1` (Pierced Mirror)** | `(0.0, 0.0, 0.0)` | `(0, 0, +1)` | **Annular:** `(+1, 0, 0)`<br>**Hole:** `(0, 0, +1)` | `(+0.7071, 0.0, -0.7071)` |
| **`M_F1` ($2''$ Fold Mirror)** | `(300.0, 0.0, 0.0)` | `(+1, 0, 0)` | `(0, -1, 0)` | `(-0.7071, -0.7071, 0.0)` |
| **`L_RC` (RedCat 51 $H_1$)** | `(300.0, -200.0, 0.0)` | `(0, -1, 0)` | `(0, -1, 0)` | Optical axis `(0, -1, 0)` ($s_o = 500\text{ mm}$) |
| **`C_FF` (ASI6200MM Sensor)** | `(300.0, -760.0, 0.0)` | `(0, -1, 0)` | Sensor plane | Sensor faces `(0, +1, 0)` ($s_i = 500\text{ mm}$ from $H_2$) |
| **`L1` (Relay Collimator)** | `(0.0, 0.0, 130.0)` | `(0, 0, +1)` | `(0, 0, +1)` | Optical axis `(0, 0, +1)` ($f = 130\text{ mm}$) |
| **`FSM` (PI S-335 Mirror)** | `(0.0, 0.0, 260.0)` | `(0, 0, +1)` | `(0, +1, 0)` | `(0.0, +0.7071, -0.7071)` |
| **`L2` (Relay Camera)** | `(0.0, 130.0, 260.0)` | `(0, +1, 0)` | `(0, +1, 0)` | Optical axis `(0, +1, 0)` ($f = 130\text{ mm}$) |
| **`M_CAL` (Flip Mirror)** | `(0.0, 165.0, 260.0)` | `(0, +1, 0)` | `(0, +1, 0)` *(stowed)* | Flips into `(0, 165, 260)` for calibration |
| **`BS` (92/8 Pellicle)** | `(0.0, 210.0, 260.0)` | `(0, +1, 0)` | **92%:** `(0, +1, 0)`<br>**8%:** `(0, 0, +1)` | `(0.0, -0.7071, +0.7071)` |
| **`C_GD` (ASI290MM Sensor)** | `(0.0, 210.0, 310.0)` | `(0, 0, +1)` | Sensor plane | Sensor faces `(0, -1, 0)` ($50\text{ mm}$ past `BS`) |
| **`SLIT` ($150\ \mu\text{m}$ Slit)** | `(0.0, 260.0, 260.0)` | `(0, +1, 0)` | `(0, +1, 0)` | Slit length along `Z` (or `X`), width along `X` (or `Z`) |
| **`L_COL` ($f=200\text{ mm}$)** | `(0.0, 460.0, 260.0)` | `(0, +1, 0)` | `(0, +1, 0)` | Optical axis `(0, +1, 0)` ($200\text{ mm}$ past `SLIT`) |
| **`VPH` ($600\text{ l/mm}$ Grating)** | `(0.0, 610.0, 260.0)` | `(0, +1, 0)` | `(-0.3551, +0.9348, 0)` | Grating normal tilted $10.4^\circ$ in `X-Y`; beam bends $20.8^\circ$ toward `-X` |
| **`L_CAM` ($f=100\text{ mm}$)** | `(-28.4, 684.8, 260.0)` | `(-0.3551, +0.9348, 0)` | `(-0.3551, +0.9348, 0)` | Optical axis rotated $+20.8^\circ$ around `+Z` ($80\text{ mm}$ past `VPH`) |
| **`C_SPEC` (ASI2600MM Sensor)** | `(-63.9, 778.3, 260.0)` | `(-0.3551, +0.9348, 0)` | Sensor plane | Sensor faces `(+0.3551, -0.9348, 0)` ($100\text{ mm}$ past `L_CAM`) |

---

## 5. FreeCAD AI Agent Workflow & Verification Protocol
When generating or modifying FreeCAD Python scripts:
1. **Run `layout_skeleton.py` First:** Verify that the parametric ray lines, optical surfaces, and bounding-box envelopes build cleanly and pass the programmatic `distToShape()` collision check with zero warnings.
2. **Normalize Imported `.step` Origins Before Placing:** Vendor STEP exports (Thorlabs, PI, ZWO) often place `(0, 0, 0)` at a rear flange, corner mounting hole, or arbitrary assembly datum. Always inspect `shape.BoundBox`, translate the local shape so its **functional optical datum** (front mirror face center, lens optical center, slit aperture center, or camera sensor plane) sits at local `(0, 0, 0)` with local optical axis along `+Z` (or surface normal along `+Z`), and **only then** apply the global `FreeCAD.Placement(pos, rot)` from `step_manifest.json`.
3. **Always Run Pair-Wise Clearance Check:** At the end of every script, compute `shape_i.distToShape(shape_j)[0]` for all non-mating solid pairs and print an explicit `PASS / COLLISION` table. Never consider a layout complete if any non-mating components have clearance `< 2.0 mm`.