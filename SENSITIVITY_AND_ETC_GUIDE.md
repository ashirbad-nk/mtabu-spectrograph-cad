# Mount Abu Slit Spectrograph: Astronomical Sensitivity & Exposure Time Guide

Comprehensive sensitivity analysis, signal-to-noise ratio (SNR) modeling, and observing guidelines for the **Mount Abu Slit Spectrograph & Guider** when mounted on the **Mt. Abu 1.2m Cassegrain ($f/13$)** and **Mt. Abu 2.5m ($f/8$)** telescopes at Gurushikhar, Mount Abu Observatory, Physical Research Laboratory (PRL).

---

## 1. Executive Summary & Sensitivity Comparison

The instrument features two instantly switchable observing regimes via the dual-slit mechanism (`CFS1/M`):
* **Mode 1 — Kinematic & Medium-Resolution ($R \approx 1060$, $75\ \mu\text{m}$ slit):** $5.7\text{ \AA}$ resolution element, resolving nova ejecta, stellar kinematics, and accretion dynamics down to $V \approx 19.8$ ($1.2\text{m}$) and $V \approx 20.5$ ($2.5\text{m}$) in a standard $30\text{-minute}$ frame.
* **Mode 2 — High-Throughput / Faint-Object ($R \approx 530$, $150\ \mu\text{m}$ slit):** $11.3\text{ \AA}$ resolution element, maximizing photon capture for supernovae classification, faint AGN, and transient alerts down to $V \approx 20.4$ ($1.2\text{m}$) and $V \approx 21.3$ ($2.5\text{m}$) in $30\text{ minutes}$, and reaching $V \approx 22.5\text{–}23.4$ in deep co-adds.

### Key Science Regimes & Limiting Magnitudes

| Science Target / Program | Integration Time ($t_{\text{exp}}$) | Target SNR | Mt. Abu 1.2m ($f/13$) | Mt. Abu 2.5m ($f/8$) | Advantage on 2.5m |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Fast Transient / Supernova Confirmation** | $300\text{ s}$ ($5\text{ min}$) | $\text{SNR} = 10$ | **$V = 18.9$** | **$V = 20.0$** | $+1.1\text{ mag}$ ($3.0\times$ faster) |
| **Standard Classification & Redshift** | $1800\text{ s}$ ($30\text{ min}$) | $\text{SNR} = 10$ | **$V = 20.4$** | **$V = 21.3$** | $+0.9\text{ mag}$ ($2.5\times$ faster) |
| **High-Quality Stellar Spectroscopy** | $1800\text{ s}$ ($30\text{ min}$) | $\text{SNR} = 30$ | **$V = 19.0$** | **$V = 19.9$** | $+0.9\text{ mag}$ ($2.5\times$ faster) |
| **Deep Emission-Line Detection** | $3600\text{ s}$ ($1\text{ hour}$) | $\text{SNR} = 3$ | **$V = 22.3$** | **$V = 23.0$** | $+0.7\text{ mag}$ ($2.2\times$ faster) |
| **Ultra-Deep Co-added Survey Limit** | $7200\text{ s}$ ($2\text{ hours}$) | $\text{SNR} = 3$ | **$V = 22.7$** | **$V = 23.4$** | $+0.7\text{ mag}$ ($2.2\times$ faster) |

*(Assumptions: Dark sky $V_{\text{sky}} = 21.2\text{ mag/arcsec}^2$, median seeing $1.5''$, Sony IMX571 in High Conversion Gain mode, $2\times$ spatial binning).*

---

## 2. Complete Optical Throughput Budget

The spectrograph uses all high-performance dielectric and protected silver surfaces with a Wasatch volume phase holographic (VPH) grating:

$$\eta_{\text{tot}}(\lambda) = T_{\text{atm}}(\lambda) \cdot T_{\text{tel}} \cdot T_{\text{opt}} \cdot \eta_{\text{slit}}(\theta_{\text{seeing}}, w_{\text{slit}}) \cdot \text{QE}(\lambda)$$

| Subsystem Component | Optical Specification | Transmission ($T$) | Cumulative Throughput |
| :--- | :--- | :---: | :---: |
| **Atmosphere ($T_{\text{atm}}$)** | Zenith extinction at Mt. Abu ($1680\text{ m}$) | $0.85$ | $0.850$ |
| **Telescope Primary + Secondary** | Enhanced Ag / fresh protected Al | $0.77$ | $0.655$ |
| **Pick-Off Flat `M1`** | Thorlabs `PF20-03-P01` protected silver | $0.98$ | $0.642$ |
| **Fast Steering Mirror (`FSM`)** | Physik Instrumente protected silver | $0.98$ | $0.629$ |
| **Pellicle Beamsplitter (`BP108`)** | $92\%\text{T} / 8\%\text{R}$ nitrocellulose | $0.92$ | $0.579$ |
| **Collimator Doublet (`AC254-200-A`)** | $\varnothing 25.4\text{ mm}$, BBAR AR-coated | $0.98$ | $0.567$ |
| **Octave Longpass Filter (`FGL475M`)** | $\varnothing 25.4\text{ mm}$ in collimated beam | $0.92$ | $0.522$ |
| **VPH Grating (`600 l/mm @ 600 nm`)** | Wasatch astronomical transmission grating | $0.85$ | $0.444$ |
| **Camera Doublet (`AC508-100-A`)** | $\varnothing 50.8\text{ mm}$, BBAR AR-coated | $0.98$ | $0.435$ |
| **Detector (`ZWO ASI2600MM Pro`)** | Sony IMX571 back-illuminated silicon QE | $0.85$ | **$\mathbf{0.370}$ (Pre-slit)** |

### Slit Geometric Efficiency ($\eta_{\text{slit}}$)
For a Gaussian seeing disk $\theta_{\text{seeing}}$ ($\sigma = \theta_{\text{seeing}} / 2.355$):
$$\eta_{\text{slit}} = \text{erf}\left(\frac{w_{\text{slit}}/2}{\sqrt{2}\,\sigma}\right)$$

* **1.2m Telescope ($f/13$, $13.22''/\text{mm}$):**
  - $150\ \mu\text{m}$ ($1.98''$) in $1.5''$ seeing: $\mathbf{94.2\%}$ (with FSM active tip-tilt lock).
  - $75\ \mu\text{m}$ ($0.99''$) in $1.5''$ seeing: $\mathbf{72.5\%}$ (with FSM active tip-tilt lock; $52.1\%$ without).
* **2.5m Telescope ($f/8$, $10.31''/\text{mm}$):**
  - $150\ \mu\text{m}$ ($1.55''$) in $1.2''$ seeing: $\mathbf{85.2\%}$ ($78.0\%$ in $1.5''$ seeing).
  - $75\ \mu\text{m}$ ($0.77''$) in $1.2''$ seeing: $\mathbf{53.8\%}$.

Net peak total system efficiency (top of atmosphere to detected photo-electrons) is **$25.2\%\text{–}34.8\%$**, delivering exceptional sensitivity.

---

## 3. Signal, Sky & Noise Formulation

Target photon flux per Angstrom at top of atmosphere for Vega magnitude $m_V$:
$$F_{\text{target}}(\lambda) = 1000 \times 10^{-0.4\,m_V}\quad [\text{photons cm}^{-2}\text{ s}^{-1}\text{ \AA}^{-1}]$$

Detected target photo-electrons per spectral resolution element ($\Delta\lambda = 6000\text{ \AA} / R$):
$$S = F_{\text{target}} \cdot \Delta\lambda \cdot A_{\text{eff}} \cdot \eta_{\text{tot}} \cdot t_{\text{exp}}$$

Detected sky background photo-electrons:
$$B_{\text{sky}} = 1000 \times 10^{-0.4\,V_{\text{sky}}} \cdot \Omega_{\text{sky}} \cdot \Delta\lambda \cdot A_{\text{eff}} \cdot \eta_{\text{sky}} \cdot t_{\text{exp}}$$
where $\Omega_{\text{sky}} = w_{\text{slit}} \times h_{\text{ext}}\text{ arcsec}^2$.

Total Noise and Signal-to-Noise Ratio:
$$\sigma_{\text{tot}} = \sqrt{S + B_{\text{sky}} + N_{\text{pix}} \cdot (\sigma_{\text{RN}}^2 + D_{\text{dark}} \cdot t_{\text{exp}})}$$
$$\text{SNR} = \frac{S}{\sigma_{\text{tot}}}$$

Using the Sony IMX571 in High Conversion Gain (HCG mode, Gain 100), read noise is only **$1.45\ e^-/\text{pixel}$** with dark current **$< 0.0005\ e^-/\text{px/s}$** at $-10^\circ\text{C}$, ensuring observations at $t \ge 300\text{ s}$ are entirely **sky-background limited**.

---

## 4. Master Limiting Magnitude Tables

### 4.1 Mode 2: Low-Resolution / Faint-Object ($R \approx 530$, $150\ \mu\text{m}$ slit)

| Integration Time | Mt. Abu 1.2m ($\text{SNR}=3$) | Mt. Abu 1.2m ($\text{SNR}=10$) | Mt. Abu 1.2m ($\text{SNR}=30$) | Mt. Abu 2.5m ($\text{SNR}=3$) | Mt. Abu 2.5m ($\text{SNR}=10$) | Mt. Abu 2.5m ($\text{SNR}=30$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$60\text{ s}$ ($1\text{ min}$)** | $18.78$ | $17.30$ | $15.67$ | $19.90$ | $18.46$ | $16.93$ |
| **$300\text{ s}$ ($5\text{ min}$)** | $20.38$ | $18.93$ | $17.35$ | $21.36$ | $19.96$ | $18.50$ |
| **$900\text{ s}$ ($15\text{ min}$)** | $21.32$ | $19.90$ | $18.39$ | $22.17$ | $20.80$ | $19.42$ |
| **$1800\text{ s}$ ($30\text{ min}$)** | $21.83$ | $20.44$ | $18.99$ | $22.62$ | $21.27$ | $19.93$ |
| **$3600\text{ s}$ ($1\text{ hour}$)** | $22.30$ | $20.92$ | $19.53$ | $23.04$ | $21.70$ | $20.40$ |
| **$7200\text{ s}$ ($2\text{ hours}$)** | $22.72$ | $21.37$ | $20.03$ | $23.44$ | $22.11$ | $20.84$ |

### 4.2 Mode 1: Medium-Resolution / Kinematics ($R \approx 1060$, $75\ \mu\text{m}$ slit)

| Integration Time | Mt. Abu 1.2m ($\text{SNR}=3$) | Mt. Abu 1.2m ($\text{SNR}=10$) | Mt. Abu 1.2m ($\text{SNR}=30$) | Mt. Abu 2.5m ($\text{SNR}=3$) | Mt. Abu 2.5m ($\text{SNR}=10$) | Mt. Abu 2.5m ($\text{SNR}=30$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$60\text{ s}$ ($1\text{ min}$)** | $18.00$ | $16.45$ | $14.68$ | $18.97$ | $17.47$ | $15.80$ |
| **$300\text{ s}$ ($5\text{ min}$)** | $19.66$ | $18.13$ | $16.39$ | $20.53$ | $19.07$ | $17.46$ |
| **$900\text{ s}$ ($15\text{ min}$)** | $20.67$ | $19.18$ | $17.52$ | $21.44$ | $20.02$ | $18.50$ |
| **$1800\text{ s}$ ($30\text{ min}$)** | $21.24$ | $19.78$ | $18.18$ | $21.94$ | $20.54$ | $19.09$ |
| **$3600\text{ s}$ ($1\text{ hour}$)** | $21.75$ | $20.32$ | $18.80$ | $22.39$ | $21.01$ | $19.62$ |
| **$7200\text{ s}$ ($2\text{ hours}$)** | $22.20$ | $20.81$ | $19.36$ | $22.80$ | $21.45$ | $20.11$ |

---

## 5. Moon Phase & Seeing Sensitivity Tradeoffs

### 5.1 Moon Phase Impact on Limiting Magnitude ($1800\text{ s}$, $\text{SNR}=10$)
* **Dark Sky (New Moon, $V_{\text{sky}} = 21.2\text{ mag/arcsec}^2$):** $V = 20.44$ ($1.2\text{m}$) / $V = 21.27$ ($2.5\text{m}$).
* **Grey Sky (Quarter Moon, $V_{\text{sky}} = 19.5\text{ mag/arcsec}^2$):** $V = 19.79$ ($1.2\text{m}$) / $V = 20.58$ ($2.5\text{m}$) ($\Delta m = -0.65\text{ mag}$).
* **Bright Sky (Full Moon, $V_{\text{sky}} = 18.0\text{ mag/arcsec}^2$):** $V = 18.91$ ($1.2\text{m}$) / $V = 19.65$ ($2.5\text{m}$) ($\Delta m = -1.53\text{ mag}$).

> [!TIP]
> Observations of bright targets ($V < 15.0$) are photon-noise dominated by the star itself and are **completely unaffected by lunar phase**. Bright time should be scheduled for standard stars, stellar kinematics, and bright binaries, reserving dark/grey time for faint transients ($V > 18.0$).

---

## 6. Using the Interactive Command-Line ETC Tool

The standalone calculator `etc_calculator.py` requires zero external packages and runs directly with Python 3:

```bash
# 1. Print full comparison tables for both telescopes
python3 etc_calculator.py --table

# 2. Compute expected SNR for a target
python3 etc_calculator.py --tel 1.2 --mode 530 --mag 18.5 --texp 1800

# 3. Find limiting magnitude for SNR = 10 in a 30-minute exposure
python3 etc_calculator.py --tel 1.2 --mode 530 --texp 1800 --snr 10

# 4. Find exposure time required to achieve SNR = 30 on a 19th mag star with the 2.5m
python3 etc_calculator.py --tel 2.5 --mode 1060 --mag 19.0 --snr 30

# 5. Run built-in self-verification unit tests
python3 etc_calculator.py --verify
```
