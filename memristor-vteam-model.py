
import matplotlib.pyplot as plt

def vteam(V_set, V_reset,dv, R_on, R_off, n_vp, n_vn, w_i, d):
    v_prev = 0 # Initialize previous voltage
    w = w_i # Initialize w with initial doping level
    I, W = [], []   # Initialize lists to store current and w values
   
    V1 = [i*dv for i in range(0, int(V_set/dv))]                                        # 0 → V_set V
    V2 = [(int(V_set/dv)-i)*dv for i in range(0, int(V_set/dv))]                        # V_set → 0 V
    V3 = [i*-dv for i in range(0, int(abs(V_reset)/dv))]                                # 0 → V_reset V
    V4 = [(int(abs(V_reset)/dv)-i)*-dv for i in range(0, int(abs(V_reset)/dv))]         # V_reset → 0 V
    V = V1 + V2 + V3 + V4
    W1, W2, W3 = [None for _ in range(len(V))], [None for _ in range(len(V))], [None for _ in range(len(V))] # For storing w values when it hits limits

    k=0

    for v in V:

        if abs(v) > abs(v_prev):
            w = w + n_vp * v / (d*1e-9) if v > 0 else w + n_vn * v / (d*1e-9)
            if w >= d:
                w = d  # Ensure w does not exceed device thickness
            elif w <= 1:
                w = 1  # Ensure w does not go below 1 nm (fully undoped)
               
                

        i = v / (R_on * w / d + R_off * (1 - w / d))

        I.append(i) # store current
        W.append(w)   # store w
        v_prev = v
        k+=1
    return V,I, W

V_set = 3       # Set voltage (V)
V_reset = -3    # Reset voltage (V)
dv = 0.01       # Voltage step size (V)
R_on = 100      # On-state resistance (Ω)
R_off = 10000   # Off-state resistance (Ω)
n_vn = 3e-9     # Negative voltage doping sensitivity (m²/C)   
n_vp = 3e-9     # Positive voltage doping sensitivity (m²/C)
w_i = 1         # Initial doping level (nm)
d = 30          # oxide thickness (nm)

V,I,W = vteam(V_set, V_reset,dv, R_on, R_off, n_vp, n_vn, w_i, d)

# --- Subplots ---
fig, ax = plt.subplots(2, 1, figsize=(6,6), sharex=True)

# I-V curve
ax[0].plot(V, I)
ax[0].set_ylabel("Current (A)")
ax[0].set_title("I-V Curve of RRAM Device")

# State variable
ax[1].plot(V, W,'o')
ax[1].set_xlabel("Voltage (V)")
ax[1].set_ylabel("w (doping in nm)")
#ax[1].set_xlim(2.4, 3.0)
#ax[1].set_ylim(29, 31)

plt.tight_layout()
plt.show()