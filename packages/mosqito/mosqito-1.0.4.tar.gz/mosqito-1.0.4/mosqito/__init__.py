from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum

from mosqito.sq_metrics.loudness.loudness_ecma.loudness_ecma import loudness_ecma
from mosqito.sq_metrics.loudness.loudness_zwst.loudness_zwst import loudness_zwst
from mosqito.sq_metrics.loudness.loudness_zwst.loudness_zwst_freq import loudness_zwst_freq
from mosqito.sq_metrics.loudness.loudness_zwst.loudness_zwst_perseg import loudness_zwst_perseg

from mosqito.sq_metrics.loudness.loudness_zwtv.loudness_zwtv import loudness_zwtv

from mosqito.sq_metrics.loudness.utils.equal_loudness_contours import equal_loudness_contours

from mosqito.sq_metrics.tonality.prominence_ratio_ecma.pr_ecma_st import pr_ecma_st
from mosqito.sq_metrics.tonality.prominence_ratio_ecma.pr_ecma_tv import pr_ecma_tv
from mosqito.sq_metrics.tonality.prominence_ratio_ecma.pr_ecma_freq import pr_ecma_freq

from mosqito.sq_metrics.tonality.tone_to_noise_ecma.tnr_ecma_st import tnr_ecma_st
from mosqito.sq_metrics.tonality.tone_to_noise_ecma.tnr_ecma_tv import tnr_ecma_tv
from mosqito.sq_metrics.tonality.tone_to_noise_ecma.tnr_ecma_freq import tnr_ecma_freq

from mosqito.sq_metrics.roughness.roughness_dw.roughness_dw import roughness_dw
from mosqito.sq_metrics.roughness.roughness_dw.roughness_dw_freq import roughness_dw_freq


from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_st import sharpness_din_st
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_tv import sharpness_din_tv
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import sharpness_din_from_loudness
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_perseg import sharpness_din_perseg
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_freq import sharpness_din_freq

from mosqito.sq_metrics.loudness.utils.sone_to_phon import sone_to_phon
from mosqito.utils.isoclose import isoclose
from mosqito.utils.load import load
from mosqito.utils.sine_wave_generator import sine_wave_generator
from mosqito.utils.time_segmentation import time_segmentation

# Colors and linestyles
COLORS = [
    "#69c3c5",
    "#9969c4",
    "#c46b69",
    "#95c469",
    "#2a6c6e",
]
