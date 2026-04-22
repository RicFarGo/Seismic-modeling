import matplotlib.pyplot as plt


def plot_final_twt_tracks(final_df):
    """Plot GR, DENSITY, VELOCIDAD, AI, RC, SYNTHETIC in TWT."""
    fig, axes = plt.subplots(nrows=1, ncols=6, figsize=(18, 10), sharey=True)

    y = final_df["TWT_MS_REG"]

    axes[0].plot(final_df["GR"], y, color="green", linewidth=0.9)
    axes[0].set_xlabel("GR")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(final_df["RHOB"], y, color="red", linewidth=0.9)
    axes[1].set_xlabel("DENSITY")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(final_df["VEL_FROM_SONIC_MPS"], y, color="darkblue", linewidth=0.9)
    axes[2].set_xlim(1500, 6000)
    axes[2].set_xlabel("VELOCIDAD (m/s)")
    axes[2].grid(True, alpha=0.3)

    axes[3].plot(final_df["AI_FILTERED"], y, color="purple", linewidth=0.9)
    axes[3].set_xlabel("AI")
    axes[3].grid(True, alpha=0.3)

    axes[4].plot(final_df["RC"], y, color="black", linewidth=0.9)
    axes[4].set_xlim(-1, 1)
    axes[4].set_xlabel("RC")
    axes[4].grid(True, alpha=0.3)

    axes[5].plot(final_df["SYNTHETIC"], y, color="navy", linewidth=0.9)
    axes[5].set_xlabel("SYNTHETICO")
    axes[5].grid(True, alpha=0.3)

    axes[0].set_ylabel("TWT (ms)")
    axes[0].invert_yaxis()

    for ax in axes:
        ax.tick_params(axis="both", labelsize=9)

    plt.tight_layout()
    plt.show()
