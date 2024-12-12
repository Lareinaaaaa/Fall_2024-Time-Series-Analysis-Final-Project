"""
Created by Jiajun Chen and Xinyue on Dec 8 2024
"""


from sdkim_class import beta_tv_torch
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

torch.set_printoptions(precision=6)
dtype = torch.float64
device = torch.device("cpu")

# MODEL SUBTYPE: choose between 'DyEKIM', 'DyEKIMext' or 'DyNoKIM'
modtype = 'DyEKIM'

if modtype == 'DyEKIM':
    # DyEKIM without h0
    inds = torch.eye(5)
    inds = inds[:4, :]

elif modtype == 'DyEKIMext':
    # DyEKIM with h0
    inds = torch.eye(5)

else:
    # DyNoKIM
    inds = torch.ones((1, 5))
    inds[0, 4] = 0

model = beta_tv_torch(beta_scal_inds=inds)

npz = np.load('example_simulation.npz')

f_T = torch.tensor(npz['f_T'])
s_T = torch.tensor(npz['s_T'])
J = torch.tensor(npz['J'])
extfields = torch.tensor(npz['h'])
covariates_T = torch.tensor(npz['covariates_T'])
covcouplings = torch.tensor(npz['covcouplings'])
sdd_pars = torch.tensor(npz['sdd_pars'])

N_sample = f_T.shape[2]

for sam in range(N_sample):
    s_T_samp = s_T[:, :, sam]
    f_T_samp = f_T[:, :, sam]
    
    # Call the modified estimate_MS with matrix visualizations
    infJ, infh = model.estimate_MS(s_T_samp)

    # Convert infJ and infh into tensors for further calculations
    J_est = torch.tensor(infJ)
    extfields_est = torch.tensor(infh)

    # Scatter plot for J comparison with error color coding
    errors_J = np.abs(J.view(-1).data.numpy() - infJ.ravel())  # Calculate errors
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        J.view(-1).data.numpy(), infJ.ravel(), c=errors_J, cmap="coolwarm", alpha=0.8, edgecolor='k'
    )
    plt.colorbar(scatter, label="Error Magnitude")
    plt.xlabel("True J")
    plt.ylabel("Estimated J")
    plt.title(f"True vs Estimated J (Sample {sam+1})")
    plt.grid()
    plt.show()

    # Scatter plot for external fields comparison with error color coding
    errors_h = np.abs(extfields.data.numpy() - infh)  # Calculate errors
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        extfields.data.numpy(), infh, c=errors_h, cmap="coolwarm", alpha=0.8, edgecolor='k'
    )
    plt.colorbar(scatter, label="Error Magnitude")
    plt.xlabel("True External Fields")
    plt.ylabel("Estimated External Fields")
    plt.title(f"True vs Estimated External Fields (Sample {sam+1})")
    plt.grid()
    plt.show()

    # Estimate constant beta
    unc_mean_est = model.estimate_const_beta(
        s_T_samp, J_est, extfields_est, covariates_T, covcouplings, lr=0.05, Steps=300
    )

    # Estimate targeted beta parameters
    sdd_est = model.estimate_targeted(
        unc_mean_est, s_T_samp, J_est, extfields_est, covariates_T, covcouplings,
        lr=0.1, Steps=300, rel_improv_tol=5e-9
    )

    # Filter dynamic parameters
    f_T_est = model.filter_dyn_par(s_T_samp, J_est, extfields_est, sdd_est, covariates_T, covcouplings)

    # Plot the original and estimated time series
    plt.figure(figsize=(10, 5))
    plt.plot(torch.exp(f_T_samp).data.numpy(), label="True f_T", alpha=0.7)
    plt.plot(torch.exp(f_T_est - torch.mean(f_T_est, 0)).data.numpy(), label="Estimated f_T", linestyle="--", alpha=0.7)
    plt.legend()
    plt.title(f"True vs Estimated Time Series (Sample {sam+1})")
    plt.grid()
    plt.show()
