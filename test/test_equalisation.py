import pytest
import numpy.testing as npt

from qampy import signals, equalisation
from qampy.core import impairments
from qampy.core import equalisation as cequalisation


class TestReturnObject(object):
    s = signals.ResampledQAM(16, 2 ** 16, fb=20e9, fs=40e9, nmodes=2)
    os = 2

    def test_apply_filter_basic(self):
        s2 = impairments.simulate_transmission(self.s, self.s.fb, self.s.fs, snr=20, dgd=100e-12)
        wx, err = equalisation.equalise_signal(s2, 1e-3, Ntaps=11)
        s3 = equalisation.apply_filter(s2, wx)
        assert type(s3) is type(self.s)

    def test_eq_applykw(self):
        s2 = impairments.simulate_transmission(self.s, self.s.fb, self.s.fs, snr=20, dgd=100e-12)
        s3, wx, err = equalisation.equalise_signal(s2, 1e-3, Ntaps=11, apply=True)
        assert type(s3) is type(self.s)

    def test_eq_applykw_dual(self):
        s2 = impairments.simulate_transmission(self.s, self.s.fb, self.s.fs, snr=20, dgd=100e-12)
        s3, wx, err = equalisation.dual_mode_equalisation(s2, (1e-3, 1e-3), 11, apply=True)
        assert type(s3) is type(self.s)

    @pytest.mark.xfail(reason="The core equalisation functions are not expected to preserve subclasses")
    def test_apply_filter_adv(self):
        s2 = impairments.simulate_transmission(self.s, self.s.fb, self.s.fs, snr=20, dgd=100e-12)
        wx, err = cequalisation.equalise_signal(s2, self.os, 1e-3, s2.M, Ntaps=11)
        s3 = equalisation.apply_filter(s2, self.os, wx)
        assert type(s3) is type(self.s)

class TestEqualisation(object):

    @pytest.mark.parametrize("N", [1,2,3])
    def test_nd_dualmode(self, N):
        import numpy as np
        from qampy import impairments
        s = signals.ResampledQAM(16, 2 ** 16, fb=20e9, fs=40e9, nmodes=N)
        s2 = impairments.change_snr(s, 25)
        E, wx, err = equalisation.dual_mode_equalisation(s2, (1e-3, 1e-3), 11, apply=True, adaptive_stepsize=(True,True))
        assert np.mean(E.cal_ber() < 1e-3)
