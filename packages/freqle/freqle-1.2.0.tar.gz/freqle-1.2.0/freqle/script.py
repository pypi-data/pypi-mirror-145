
from freqle import cluster
import numpy as np

import matplotlib.pyplot as plt
import time

pal = cluster(Nbh = 20000, n_mus = 300, cluster_eta = 1e3)
pal.populate(v = True)
pal.build_mass_grid()
pal.emit_GW(v = True, maximum_det_freq = 2048)
pal.calc_freq_distr(remove_outliers = False, v = True)
pal.plot_freq_distr(mu = .4e-12)


mus = np.linspace(0.4e-12, 1.2e-12, 5)

for mu in mus:
    mu_index = np.abs(mu - pal.boson_grid).argmin()
    mu_value = pal.boson_grid[mu_index]
    tau_gw = pal.tau_gw[mu_index]
    tau_inst = pal.tau_inst[mu_index]
    tau = tau_gw + tau_inst
    plt.plot(pal.massesUM, tau, '.', label = f'{mu_value*1e12:.2f}$\cdot 10^{-12}eV$')

plt.yscale('log')
plt.title("Time of formation + time of emission vs Bh masses")
plt.xlabel('BH masses')
plt.ylabel("time $[s]$")
plt.axhline(y = pal.cluster_eta_sec, label = f'{pal.cluster_eta:.1E} yrs')
plt.legend()
plt.show()

mu = 1e-12
mu_index = np.abs(mu - pal.boson_grid).argmin()
mu_value = pal.boson_grid[mu_index]
tau_gw = pal.tau_gw[mu_index]
tau_inst = pal.tau_inst[mu_index]
old_em_time = pal.cluster_eta_sec-tau_inst
act_em_time = np.minimum(pal.cluster_eta_sec, tau_gw) - tau_inst
plt.plot(pal.massesUM, old_em_time, '.', label = f'{mu_value*1e12:.2f}$\cdot 10^{-12}eV$, old')
plt.plot(pal.massesUM, act_em_time, '.', label = f'{mu_value*1e12:.2f}$\cdot 10^{-12}eV$, true')
plt.legend()
plt.yscale('log')
plt.show()







