import numpy as np


def calculate_dts_error_grid(pred_glucose, true_glucose):
    """
    Calculates the percentage of points in each zone of the DTS Error Grid.
    Args:
        pred_glucose (list or np.array): Monitor/Predicted glucose values.
        true_glucose (list or np.array): Reference/Ground truth glucose values.
    Returns:
        dict: Percentage of points falling into Zones A, B, C, D, and E,
              rounded to 2 decimal places.
    """
    pred = np.asarray(pred_glucose, dtype=float)
    ref = np.asarray(true_glucose, dtype=float)

    total = len(ref)
    if total == 0:
        return {
            "DTS_A_ZONE_PERCENT": 0.0,
            "DTS_B_ZONE_PERCENT": 0.0,
            "DTS_C_ZONE_PERCENT": 0.0,
            "DTS_D_ZONE_PERCENT": 0.0,
            "DTS_E_ZONE_PERCENT": 0.0,
        }

    # --- Upper Boundaries (Monitor > Reference) ---
    b_up = np.where(ref <= 50, 60,   (540 / 450) * (ref - 50) + 60)
    c_up = np.where(ref <= 50, 86.5, (513.5 / 297) * (ref - 50) + 86.5)
    d_up = np.where(ref <= 50, 124,  (476 / 191) * (ref - 50) + 124)
    e_up = np.where(ref <= 50, 179,  (421 / 117) * (ref - 50) + 179)

    # --- Lower Boundaries (Monitor < Reference) ---
    b_low = np.where(ref <= 62.5, 0, (430 / 537.5) * (ref - 62.5) + 50)
    c_low = np.where(ref <= 97.5, 0, (257 / 502.5) * (ref - 97.5) + 50)
    d_low = np.where(ref <= 153,  0, (147 / 447) * (ref - 153) + 50)
    e_low = np.where(ref <= 238,  0, (76 / 362) * (ref - 238) + 50)

    # --- Zone Assignments ---
    zone_a = (pred <= b_up) & (pred >= b_low)
    zone_b = ((pred <= c_up) & (pred > b_up)) | ((pred < b_low) & (pred >= c_low))
    zone_c = ((pred <= d_up) & (pred > c_up)) | ((pred < c_low) & (pred >= d_low))
    zone_d = ((pred <= e_up) & (pred > d_up)) | ((pred < d_low) & (pred >= e_low))
    zone_e = (pred > e_up) | (pred < e_low)

    return {
        "DTS_A_ZONE_PERCENT": round((np.sum(zone_a) / total) * 100, 2),
        "DTS_B_ZONE_PERCENT": round((np.sum(zone_b) / total) * 100, 2),
        "DTS_C_ZONE_PERCENT": round((np.sum(zone_c) / total) * 100, 2),
        "DTS_D_ZONE_PERCENT": round((np.sum(zone_d) / total) * 100, 2),
        "DTS_E_ZONE_PERCENT": round((np.sum(zone_e) / total) * 100, 2),
    }


def calculate_rmse(pred, true):
    """Returns the Root Mean Squared Error, rounded to 2 decimal places."""
    pred = np.asarray(pred, dtype=float)
    true = np.asarray(true, dtype=float)
    return round(float(np.sqrt(np.mean((pred - true) ** 2))), 2)


def calculate_mard(pred, true):
    """Returns the Mean Absolute Relative Difference (%), rounded to 2 decimal places."""
    pred = np.asarray(pred, dtype=float)
    true = np.asarray(true, dtype=float)
    # Exclude any zero reference values to avoid division by zero.
    valid = true != 0
    if not np.any(valid):
        return 0.0
    return round(float(np.mean(np.abs(pred[valid] - true[valid]) / true[valid]) * 100), 2)