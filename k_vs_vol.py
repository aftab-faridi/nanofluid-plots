import numpy as np
import matplotlib.pyplot as plt

# Densities (kg/m³)
densities = {"Co": 8900, "GO": 1800, "Ag": 10500, "TiO2": 4250, "EG": 1115}

# Base fluid thermal conductivity (EG) in W/mK
k_f = 0.253

# Nanoparticle thermal conductivities (W/mK) aligned with your grouping
k_s = {
    "Ag": 429,
    "TiO2": 8.9538,
    "GO": 5000,
    "Co": 100,
}

# Volume fractions (%) to evaluate
volume_percents = np.array([0.005, 0.05, 0.1, 0.5, 1.0])


def vol_to_wt_percent(phi_percent, rho_s, rho_f):
    phi = phi_percent / 100  # convert to decimal
    w = ((rho_s * phi) / ((rho_s * phi) + (rho_f * (1 - phi)))) * 100
    return w


def calc_ratio(k_s, k_base, phi):
    numerator = k_s + 2 * k_base - 2 * phi * (k_base - k_s)
    denominator = k_s + 2 * k_base + 2 * phi * (k_base - k_s)
    return numerator / denominator


# Prepare lists to store thermal conductivities
k_nf_list = []
k_hnf_list = []
k_tri_hnf_list = []
k_tet_hnf_list = []

for vol_total in volume_percents:
    # Calculate weight fractions from volume fractions for each particle
    # Using your order: Ag, TiO2, GO, Co

    w_Ag = vol_to_wt_percent(vol_total, densities["Ag"], densities["EG"]) / 100
    w_TiO2 = vol_to_wt_percent(vol_total, densities["TiO2"], densities["EG"]) / 100
    w_GO = vol_to_wt_percent(vol_total, densities["GO"], densities["EG"]) / 100
    w_Co = vol_to_wt_percent(vol_total, densities["Co"], densities["EG"]) / 100

    # NOTE: Using weight fractions as proxy for volume fractions phi_i for Maxwell formula
    # Step 1: Nanofluid (Ag only)
    ratio_nf = calc_ratio(k_s["Ag"], k_f, w_Ag)
    k_nf = ratio_nf * k_f

    # Step 2: Hybrid nanofluid (Ag + TiO2)
    ratio_hnf = calc_ratio(k_s["TiO2"], k_nf, w_TiO2)
    k_hnf = ratio_hnf * k_nf

    # Step 3: Tri-hybrid nanofluid (Ag + TiO2 + GO)
    ratio_tri_hnf = calc_ratio(k_s["GO"], k_hnf, w_GO)
    k_tri_hnf = ratio_tri_hnf * k_hnf

    # Step 4: Tetra-hybrid nanofluid (Ag + TiO2 + GO + Co)
    ratio_tet_hnf = calc_ratio(k_s["Co"], k_tri_hnf, w_Co)
    k_tet_hnf = ratio_tet_hnf * k_tri_hnf

    k_nf_list.append(k_nf)
    k_hnf_list.append(k_hnf)
    k_tri_hnf_list.append(k_tri_hnf)
    k_tet_hnf_list.append(k_tet_hnf)

# Convert to numpy arrays
k_nf_list = np.array(k_nf_list)
k_hnf_list = np.array(k_hnf_list)
k_tri_hnf_list = np.array(k_tri_hnf_list)
k_tet_hnf_list = np.array(k_tet_hnf_list)

# Calculate ratios to base fluid for plotting
ratio_nf = k_nf_list / k_f
ratio_hnf = k_hnf_list / k_f
ratio_tri_hnf = k_tri_hnf_list / k_f
ratio_tet_hnf = k_tet_hnf_list / k_f

# Plotting
font_name = "Times New Roman"
plt.figure(figsize=(10, 7))

plt.plot(volume_percents, ratio_nf, marker="o", label="Ag/EG (Nanofluid)")
plt.plot(
    volume_percents, ratio_hnf, marker="s", label="Ag-TiO$_2$/EG (Hybrid Nanofluid)"
)
plt.plot(
    volume_percents,
    ratio_tri_hnf,
    marker="^",
    label="Ag-TiO$_2$-GO/EG (Tri-Hybrid Nanofluid)",
)
plt.plot(
    volume_percents,
    ratio_tet_hnf,
    marker="d",
    label="Ag-TiO$_2$-GO-Co/EG (Tetra-Hybrid Nanofluid)",
)

plt.xlabel(
    "Solid Volume Fractions (%)", fontsize=14, fontweight="bold", fontname=font_name
)
plt.ylabel(
    "Thermal Conductivity Ratio", fontsize=14, fontweight="bold", fontname=font_name
)
plt.title(
    "Thermal Conductivity Ratio vs Solid Volume Fractions %\n(Co, GO, Ag, TiO$_2$ in Ethylene Glycol)",
    fontsize=16,
    fontweight="bold",
    fontname=font_name,
)

plt.grid(True)
plt.legend(fontsize=12, prop={"family": font_name, "weight": "bold"})
plt.tight_layout()

plt.savefig("thermal_conductivity_weight_fraction_conversion.png", dpi=300)
plt.show()
