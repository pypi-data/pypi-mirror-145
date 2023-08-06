"""Fast wavelet transformation code with edge-padding."""
# Created by moritz wolter, 14.04.20
from typing import List, Optional, Sequence, Tuple, Union

import pywt
import torch

from ._util import Wavelet, _as_wavelet


def get_filter_tensors(
    wavelet: Union[Wavelet, str],
    flip: bool,
    device: Union[torch.device, str],
    dtype: torch.dtype = torch.float32,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """Convert input wavelet to filter tensors.

    Args:
        wavelet (Wavelet or str): A pywt wavelet compatible object or
                the name of a pywt wavelet.
        flip (bool): If true filters are flipped.
        device (torch.device) : PyTorch target device.
        dtype (torch.dtype): The data type sets the precision of the
               computation. Default: torch.float32.

    Returns:
        tuple: Tuple containing the four filter tensors
        dec_lo, dec_hi, rec_lo, rec_hi

    """
    wavelet = _as_wavelet(wavelet)

    def _create_tensor(filter: Sequence[float]) -> torch.Tensor:
        if flip:
            if isinstance(filter, torch.Tensor):
                return filter.flip(-1).unsqueeze(0).to(device)
            else:
                return torch.tensor(filter[::-1], device=device, dtype=dtype).unsqueeze(
                    0
                )
        else:
            if isinstance(filter, torch.Tensor):
                return filter.unsqueeze(0).to(device)
            else:
                return torch.tensor(filter, device=device, dtype=dtype).unsqueeze(0)

    dec_lo, dec_hi, rec_lo, rec_hi = wavelet.filter_bank
    dec_lo_tensor = _create_tensor(dec_lo)
    dec_hi_tensor = _create_tensor(dec_hi)
    rec_lo_tensor = _create_tensor(rec_lo)
    rec_hi_tensor = _create_tensor(rec_hi)
    return dec_lo_tensor, dec_hi_tensor, rec_lo_tensor, rec_hi_tensor


def _get_pad(data_len: int, filt_len: int) -> Tuple[int, int]:
    """Compute the required padding.

    Args:
        data_len (int): The length of the input vector.
        filt_len (int): The length of the used filter.

    Returns:
        tuple: The numbers to attach on the edges of the input.

    """
    # pad to ensure we see all filter positions and
    # for pywt compatability.
    # convolution output length:
    # see https://arxiv.org/pdf/1603.07285.pdf section 2.3:
    # floor([data_len - filt_len]/2) + 1
    # should equal pywt output length
    # floor((data_len + filt_len - 1)/2)
    # => floor([data_len + total_pad - filt_len]/2) + 1
    #    = floor((data_len + filt_len - 1)/2)
    # (data_len + total_pad - filt_len) + 2 = data_len + filt_len - 1
    # total_pad = 2*filt_len - 3

    # we pad half of the total requried padding on each side.
    padr = (2 * filt_len - 3) // 2
    padl = (2 * filt_len - 3) // 2

    # pad to even singal length.
    if data_len % 2 != 0:
        padr += 1

    return padr, padl


def _translate_boundary_strings(pywt_mode: str) -> str:
    """Translate pywt mode strings to pytorch mode strings.

    We support constant, zero, reflect and periodic.
    Unfortunately "constant" has different meanings in the
    pytorch and pywavelet communities.

    Raises:
        ValueError: If the padding mode is not supported.

    """
    if pywt_mode == "constant":
        pt_mode = "replicate"
    elif pywt_mode == "zero":
        pt_mode = "constant"
    elif pywt_mode == "reflect":
        pt_mode = pywt_mode
    elif pywt_mode == "periodic":
        pt_mode = "circular"
    else:
        raise ValueError("Padding mode not supported.")
    return pt_mode


def fwt_pad(
    data: torch.Tensor, wavelet: Union[Wavelet, str], mode: str = "reflect"
) -> torch.Tensor:
    """Pad the input signal to make the fwt matrix work.

    Args:
        data (torch.Tensor): Input data [batch_size, 1, time]
        wavelet (Wavelet or str): A pywt wavelet compatible object or
            the name of a pywt wavelet.
        mode (str): The desired way to pad.
            Supported modes are "reflect", "zero", "constant" and "periodic".
            Refection padding mirrors samples along the border.
            Zero padding pads zeros.
            Constant padding replicates border values.
            periodic padding repeats samples in a cyclic fashing.
            Defaults to reflect.

    Returns:
        torch.Tensor: A pytorch tensor with the padded input data

    """
    wavelet = _as_wavelet(wavelet)
    # convert pywt to pytorch convention.
    mode = _translate_boundary_strings(mode)

    padr, padl = _get_pad(data.shape[-1], len(wavelet.dec_lo))
    data_pad = torch.nn.functional.pad(data, [padl, padr], mode=mode)
    return data_pad


def fwt_pad2(
    data: torch.Tensor, wavelet: Union[Wavelet, str], mode: str = "reflect"
) -> torch.Tensor:
    """Pad data for the 2d FWT.

    Args:
        data (torch.Tensor): Input data with 4 dimensions.
        wavelet (Wavelet or str): A pywt wavelet compatible object or
            the name of a pywt wavelet.
        mode (str): The padding mode.
            Supported modes are "reflect", "zero", "constant" and "periodic".
            Defaults to reflect.

    Returns:
        The padded output tensor.

    """
    mode = _translate_boundary_strings(mode)

    wavelet = _as_wavelet(wavelet)
    padb, padt = _get_pad(data.shape[-2], len(wavelet.dec_lo))
    padr, padl = _get_pad(data.shape[-1], len(wavelet.dec_lo))
    data_pad = torch.nn.functional.pad(data, [padl, padr, padt, padb], mode=mode)
    return data_pad


def _outer(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """Torch implementation of numpy's outer for vectors."""
    a_flat = torch.reshape(a, [-1])
    b_flat = torch.reshape(b, [-1])
    a_mul = torch.unsqueeze(a_flat, dim=-1)
    b_mul = torch.unsqueeze(b_flat, dim=0)
    return a_mul * b_mul


def _flatten_2d_coeff_lst(
    coeff_lst_2d: List[
        Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor, torch.Tensor]]
    ],
    flatten_tensors: bool = True,
) -> List[torch.Tensor]:
    """Flattens a list of tensor tuples into a single list.

    Args:
        coeff_lst_2d (list): A pywt-style coefficient list of torch tensors.
        flatten_tensors (bool): If true, 2d tensors are flattened. Defaults to True.

    Returns:
        list: A single 1-d list with all original elements.
    """
    flat_coeff_lst = []
    for coeff in coeff_lst_2d:
        if isinstance(coeff, tuple):
            for c in coeff:
                if flatten_tensors:
                    flat_coeff_lst.append(c.flatten())
                else:
                    flat_coeff_lst.append(c)
        else:
            if flatten_tensors:
                flat_coeff_lst.append(coeff.flatten())
            else:
                flat_coeff_lst.append(coeff)
    return flat_coeff_lst


def construct_2d_filt(lo: torch.Tensor, hi: torch.Tensor) -> torch.Tensor:
    """Construct two dimensional filters using outer products.

    Args:
        lo (torch.Tensor): Low-pass input filter.
        hi (torch.Tensor): High-pass input filter

    Returns:
        torch.Tensor: Stacked 2d filters of dimension
            [filt_no, 1, height, width].
            The four filters are ordered ll, lh, hl, hh.

    """
    ll = _outer(lo, lo)
    lh = _outer(hi, lo)
    hl = _outer(lo, hi)
    hh = _outer(hi, hi)
    filt = torch.stack([ll, lh, hl, hh], 0)
    filt = filt.unsqueeze(1)
    return filt


def wavedec2(
    data: torch.Tensor,
    wavelet: Union[Wavelet, str],
    level: Optional[int] = None,
    mode: str = "reflect",
) -> List[Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor, torch.Tensor]]]:
    """Non seperated two dimensional wavelet transform.

    Args:
        data (torch.Tensor): The input data tensor of shape
            [batch_size, 1, height, width].
            2d inputs are interpreted as [height, width],
            3d inputs are interpreted as [batch_size, height, width].
        wavelet (Wavelet or str): A pywt wavelet compatible object or
            the name of a pywt wavelet.
        level (int): The number of desired scales.
            Defaults to None.
        mode (str): The padding mode. Options are
            "reflect", "zero", "constant" and "periodic".
            Defaults to "reflect".

    Returns:
        list: A list containing the wavelet coefficients.
              The coefficients are in pywt order. That is:
              [cAn, (cHn, cVn, cDn), … (cH1, cV1, cD1)] .
              A denotes approximation, H horizontal, V vertical
              and D diagonal coefficients.

    Examples::
        >>> import torch
        >>> import ptwt, pywt
        >>> import numpy as np
        >>> import scipy.misc
        >>> face = np.transpose(scipy.misc.face(),
                                [2, 0, 1]).astype(np.float64)
        >>> pytorch_face = torch.tensor(face).unsqueeze(1)
        >>> coefficients = ptwt.wavedec2(pytorch_face, pywt.Wavelet("haar"),
                                         level=2, mode="zero")

    """
    if data.dim() == 2:
        data = data.unsqueeze(0).unsqueeze(0)
    elif data.dim() == 3:
        data = data.unsqueeze(1)

    wavelet = _as_wavelet(wavelet)
    dec_lo, dec_hi, _, _ = get_filter_tensors(
        wavelet, flip=True, device=data.device, dtype=data.dtype
    )
    dec_filt = construct_2d_filt(lo=dec_lo, hi=dec_hi)

    if level is None:
        level = pywt.dwtn_max_level([data.shape[-1], data.shape[-2]], wavelet)

    result_lst: List[
        Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor, torch.Tensor]]
    ] = []
    res_ll = data
    for _ in range(level):
        res_ll = fwt_pad2(res_ll, wavelet, mode=mode)
        res = torch.nn.functional.conv2d(res_ll, dec_filt, stride=2)
        res_ll, res_lh, res_hl, res_hh = torch.split(res, 1, 1)
        result_lst.append((res_lh, res_hl, res_hh))
    result_lst.append(res_ll)
    return result_lst[::-1]


def waverec2(
    coeffs: List[Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor, torch.Tensor]]],
    wavelet: Union[Wavelet, str],
) -> torch.Tensor:
    """Reconstruct a signal from wavelet coefficients.

    Args:
        coeffs (list): The wavelet coefficient list produced by wavedec2.
        wavelet (Wavelet or str): A pywt wavelet compatible object or
            the name of a pywt wavelet.

    Returns:
        torch.Tensor: The reconstructed signal.

    Raises:
        ValueError: If `coeffs` is not in the shape as it is returned from `wavedec2`.

    Examples::
        >>> import ptwt, pywt, torch
        >>> import numpy as np
        >>> import scipy.misc
        >>> face = np.transpose(scipy.misc.face(),
                                [2, 0, 1]).astype(np.float64)
        >>> pytorch_face = torch.tensor(face).unsqueeze(1)
        >>> coefficients = ptwt.wavedec2(pytorch_face, pywt.Wavelet("haar"),
                                         level=2, mode="constant")
        >>> reconstruction = ptwt.waverec2(coefficients, pywt.Wavelet("haar"))

    """
    wavelet = _as_wavelet(wavelet)

    if not isinstance(coeffs[0], torch.Tensor):
        raise ValueError(
            "First element of coeffs must be the approximation coefficient tensor."
        )

    _, _, rec_lo, rec_hi = get_filter_tensors(
        wavelet, flip=False, device=coeffs[0].device, dtype=coeffs[0].dtype
    )
    filt_len = rec_lo.shape[-1]
    rec_filt = construct_2d_filt(lo=rec_lo, hi=rec_hi)

    res_ll = coeffs[0]
    for c_pos, res_lh_hl_hh in enumerate(coeffs[1:]):
        res_ll = torch.cat(
            [res_ll, res_lh_hl_hh[0], res_lh_hl_hh[1], res_lh_hl_hh[2]], 1
        )
        res_ll = torch.nn.functional.conv_transpose2d(res_ll, rec_filt, stride=2)

        # remove the padding
        padl = (2 * filt_len - 3) // 2
        padr = (2 * filt_len - 3) // 2
        padt = (2 * filt_len - 3) // 2
        padb = (2 * filt_len - 3) // 2
        if c_pos < len(coeffs) - 2:
            pred_len = res_ll.shape[-1] - (padl + padr)
            next_len = coeffs[c_pos + 2][0].shape[-1]
            pred_len2 = res_ll.shape[-2] - (padt + padb)
            next_len2 = coeffs[c_pos + 2][0].shape[-2]
            if next_len != pred_len:
                padr += 1
                pred_len = res_ll.shape[-1] - (padl + padr)
                assert (
                    next_len == pred_len
                ), "padding error, please open an issue on github "
            if next_len2 != pred_len2:
                padb += 1
                pred_len2 = res_ll.shape[-2] - (padt + padb)
                assert (
                    next_len2 == pred_len2
                ), "padding error, please open an issue on github "
        if padt > 0:
            res_ll = res_ll[..., padt:, :]
        if padb > 0:
            res_ll = res_ll[..., :-padb, :]
        if padl > 0:
            res_ll = res_ll[..., padl:]
        if padr > 0:
            res_ll = res_ll[..., :-padr]
    return res_ll


def wavedec(
    data: torch.Tensor,
    wavelet: Union[Wavelet, str],
    level: Optional[int] = None,
    mode: str = "reflect",
) -> List[torch.Tensor]:
    """Compute the analysis (forward) 1d fast wavelet transform.

    Args:
        data (torch.Tensor): Input time series of shape [batch_size, 1, time]
                             1d inputs are interpreted as [time],
                             2d inputs are interpreted as [batch_size, time].
        wavelet (Wavelet or str): A pywt wavelet compatible object or
            the name of a pywt wavelet.
        level (int): The scale level to be computed.
                               Defaults to None.
        mode (str): The desired padding mode. Padding extends the singal along
            the edges. Supported modes are "reflect", "zero", "constant"
            and "periodic". Defaults to "reflect".

    Returns:
        list: A list [cA_n, cD_n, cD_n-1, …, cD2, cD1]
        containing the wavelet coefficients. A denotes
        approximation and D detail coefficients.

    Examples:
        >>> import torch
        >>> import ptwt, pywt
        >>> import numpy as np
        >>> # generate an input of even length.
        >>> data = np.array([0, 1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 0])
        >>> data_torch = torch.from_numpy(data.astype(np.float32))
        >>> # compute the forward fwt coefficients
        >>> ptwt.wavedec(data_torch, pywt.Wavelet('haar'),
                         mode='zero', level=2)

    """
    if data.dim() == 1:
        # assume time series
        data = data.unsqueeze(0).unsqueeze(0)
    elif data.dim() == 2:
        # assume batched time series
        data = data.unsqueeze(1)

    dec_lo, dec_hi, _, _ = get_filter_tensors(
        wavelet, flip=True, device=data.device, dtype=data.dtype
    )
    filt_len = dec_lo.shape[-1]
    filt = torch.stack([dec_lo, dec_hi], 0)

    if level is None:
        level = pywt.dwt_max_level(data.shape[-1], filt_len)

    result_lst = []
    res_lo = data
    for _ in range(level):
        res_lo = fwt_pad(res_lo, wavelet, mode=mode)
        res = torch.nn.functional.conv1d(res_lo, filt, stride=2)
        res_lo, res_hi = torch.split(res, 1, 1)
        result_lst.append(res_hi.squeeze(1))
    result_lst.append(res_lo.squeeze(1))
    return result_lst[::-1]


def waverec(coeffs: List[torch.Tensor], wavelet: Union[Wavelet, str]) -> torch.Tensor:
    """Reconstruct a signal from wavelet coefficients.

    Args:
        coeffs (list): The wavelet coefficient list produced by wavedec.
        wavelet (Wavelet or str): A pywt wavelet compatible object or
            the name of a pywt wavelet.

    Returns:
        torch.Tensor: The reconstructed signal.

    Examples::
        >>> import torch
        >>> import ptwt, pywt
        >>> import numpy as np
        >>> # generate an input of even length.
        >>> data = np.array([0, 1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 0])
        >>> data_torch = torch.from_numpy(data.astype(np.float32))
        >>> # invert the fast wavelet transform.
        >>> ptwt.waverec(ptwt.wavedec(data_torch, pywt.Wavelet('haar'),
                                      mode='zero', level=2),
                         pywt.Wavelet('haar'))

    """
    _, _, rec_lo, rec_hi = get_filter_tensors(
        wavelet, flip=False, device=coeffs[-1].device, dtype=coeffs[-1].dtype
    )
    filt_len = rec_lo.shape[-1]
    filt = torch.stack([rec_lo, rec_hi], 0)

    res_lo = coeffs[0]
    for c_pos, res_hi in enumerate(coeffs[1:]):
        res_lo = torch.stack([res_lo, res_hi], 1)
        res_lo = torch.nn.functional.conv_transpose1d(res_lo, filt, stride=2).squeeze(1)

        # remove the padding
        padl = (2 * filt_len - 3) // 2
        padr = (2 * filt_len - 3) // 2
        if c_pos < len(coeffs) - 2:
            pred_len = res_lo.shape[-1] - (padl + padr)
            next_len = coeffs[c_pos + 2].shape[-1]
            if next_len != pred_len:
                padr += 1
                pred_len = res_lo.shape[-1] - (padl + padr)
                assert (
                    next_len == pred_len
                ), "padding error, please open an issue on github "
        if padl > 0:
            res_lo = res_lo[..., padl:]
        if padr > 0:
            res_lo = res_lo[..., :-padr]
    return res_lo
