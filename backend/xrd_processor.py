"""
XRD (X-ray Diffraction) 数据处理模块
使用高斯展宽将稀疏 PXRD 输入转换为固定网格的稠密向量
"""

import numpy as np
import torch


def xrd_process(
    xrd,
    resolution=None,
    src_len=None,
    min_angle=5.0,
    max_angle=90.0,
    step=0.01,
    sigma=0.1,
):
    """
    Convert sparse PXRD inputs into a fixed-grid dense vector using Gaussian broadening.

    Args:
        xrd: Input XRD data (numpy array or torch tensor), shape [N, 2]
             - Column 0: 2-theta angles (degrees)
             - Column 1: Intensities
        resolution: (deprecated, kept for compatibility) Not used in new implementation
        src_len: (deprecated, kept for compatibility) Not used in new implementation
        min_angle: Minimum 2-theta angle (degrees), default=5.0
        max_angle: Maximum 2-theta angle (degrees), default=90.0
        step: Grid resolution (degrees), default=0.01
        sigma: Standard deviation for Gaussian broadening (degrees), default=0.1

    Returns:
        pos_emb: Position embeddings (grid indices), shape [grid_length, 1]
        sign_emb: Signal embeddings (broadened and normalized intensities), shape [grid_length, 1]
    """
    # Convert to torch tensor if numpy array
    if isinstance(xrd, np.ndarray):
        xrd = torch.from_numpy(xrd).float()
    else:
        xrd = xrd.float()

    # Find all signals (peaks with non-zero intensity) within the specified angle range
    signal_mask = (
        (xrd[:, 1] != 0) & (xrd[:, 0] >= min_angle) & (xrd[:, 0] <= max_angle)
    )
    if signal_mask.sum() == 0:
        # No signals found in range, return zero-filled arrays
        grid_length = int((max_angle - min_angle) / step) + 1
        pos_emb = torch.arange(grid_length, dtype=torch.float).unsqueeze(1)
        sign_emb = torch.zeros((grid_length, 1), dtype=torch.float)
        return pos_emb, sign_emb

    # Extract peaks (angles and intensities) within range
    peak_angles = xrd[signal_mask, 0]  # [num_peaks]
    peak_intensities = xrd[signal_mask, 1]  # [num_peaks]

    # Create fixed grid
    grid_length = int((max_angle - min_angle) / step) + 1
    grid_angles = torch.linspace(min_angle, max_angle, grid_length)  # [grid_length]

    # Apply Gaussian broadening using broadcasting
    # Shape: [num_peaks, grid_length]
    diff = grid_angles.unsqueeze(0) - peak_angles.unsqueeze(1)
    gaussian_weights = torch.exp(-0.5 * (diff / sigma) ** 2)

    # Weight by peak intensities and sum across all peaks
    broadened_intensities = (gaussian_weights * peak_intensities.unsqueeze(1)).sum(
        dim=0
    )

    # Normalize intensities to [0, 1]
    max_intensity = broadened_intensities.max()
    if max_intensity > 0:
        normalized_intensities = broadened_intensities / max_intensity
    else:
        normalized_intensities = broadened_intensities

    # Create position embeddings (grid indices)
    pos_emb = torch.arange(grid_length, dtype=torch.float).unsqueeze(1)
    sign_emb = normalized_intensities.unsqueeze(1)

    return pos_emb, sign_emb
