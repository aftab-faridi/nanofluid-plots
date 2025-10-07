import matplotlib.pyplot as plt

# Densities (kg/m³)
densities = {"Co": 8900, "GO": 1800, "Ag": 10500, "TiO2": 4250, "EG": 1115}

# Volume fractions (%) to plot
volume_percents = [0.005, 0.05, 0.1, 0.5, 1.0]


# Function to convert volume % to weight %
def vol_to_wt_percent(phi_percent, rho_s, rho_f):
    phi = phi_percent / 100  # convert to decimal
    w = ((rho_s * phi) / ((rho_s * phi) + (rho_f * (1 - phi)))) * 100
    return w


# Font name for labels (Times New Roman)
font_name = "Times New Roman"

# Prepare data for plotting
plt.figure(figsize=(8, 6))
for material in ["Co", "GO", "Ag", "TiO2"]:
    weight_percents = [
        vol_to_wt_percent(v, densities[material], densities["EG"])
        for v in volume_percents
    ]
    plt.plot(volume_percents, weight_percents, marker="o", label=material)

# Formatting with mathtext for subscript 2 in TiO₂
plt.xlabel("Volume Fraction (%)", fontsize=12, fontweight="bold", fontname=font_name)
plt.ylabel("Weight Fraction (%)", fontsize=12, fontweight="bold", fontname=font_name)
plt.title(
    "Volume % vs Weight % Conversion\n(Co, GO, Ag, TiO$_2$ in Ethylene Glycol)",
    fontsize=12,
    fontweight="bold",
    fontname=font_name,
)
plt.legend(fontsize=12, frameon=True, prop={"family": font_name, "weight": "bold"})
plt.grid(True)
plt.tight_layout()

# Save figure
plt.savefig("volume_vs_weight_conversion_graph.png", dpi=300)
plt.show()
