import numpy as np
import scipy.interpolate as interpolate
import scipy.constants

from drama.geo import geometry as geom
from drama.geo.swath_geo import SingleSwath


class BistaticRadarGeometry(object):
    """
    This class calculates useful geometric relations.

    Parameters
    ----------
    orbit_height : float
        orbit height above surface
    r_planet : float
        radious of planet, default's to Earth's
    gm_planet : float
        mass of planet, default's to Earths
    degrees : bool
        if set, everything is in degrees, defaults to False.
    """
    def __init__(self, par_file, companion_delay=None):
        self.swth_t = SingleSwath(par_file=par_file)
        # copy conf one level-up
        self.conf = self.swth_t.conf
        if companion_delay is None:
            self.swth_r = self.swth_t
        else:
            self.swth_r = SingleSwath(par_file=par_file,
                                      companion_delay=companion_delay)
        # Satellite pointing
        companion_pointing = geom.companion_pointing(self.swth_t.xyz,
                                                     self.swth_r.r_ecef,
                                                     self.swth_r.v_ecef,tilt=90)
        self.euler_xyz_satcoord = companion_pointing.euler_xyz
        # transformation matrix from sat coordinates to local Coordinates
        self.sat2ecef = companion_pointing.sat_xyz
        self.local2ecef = np.stack((self.swth_t.local_x,
                                    self.swth_t.local_y,
                                    self.swth_t.local_z), axis=3)
        self.sat2local = np.einsum("imkj,ikl->imjl", self.local2ecef, self.sat2ecef)
        # antenna axes in sat Coordinates
        self.antaxes_sat = companion_pointing.sat
        # antenna axes in local Coordinates
        self.antaxes_local = np.einsum("imjk,ikl->imjl", self.sat2local, companion_pointing.sat)
        self.los_t_ecef = self.swth_t.xyz - self.swth_t.r_ecef[:, np.newaxis, :]
        self.los_r_ecef = self.swth_t.xyz - self.swth_r.r_ecef[:, np.newaxis, :]
        # transform to local coordinate System
        self.r_t = np.zeros_like(self.los_t_ecef)
        self.r_r = np.zeros_like(self.los_t_ecef)
        self.v_t = np.zeros_like(self.los_t_ecef)
        self.v_r = np.zeros_like(self.los_t_ecef)
        self.r_t[..., 0] = np.sum(self.los_t_ecef * self.swth_t.local_x, axis=-1)
        self.r_t[..., 1] = np.sum(self.los_t_ecef * self.swth_t.local_y, axis=-1)
        self.r_t[..., 2] = np.sum(self.los_t_ecef * self.swth_t.local_z, axis=-1)
        self.r_r[..., 0] = np.sum(self.los_r_ecef * self.swth_t.local_x, axis=-1)
        self.r_r[..., 1] = np.sum(self.los_r_ecef * self.swth_t.local_y, axis=-1)
        self.r_r[..., 2] = np.sum(self.los_r_ecef * self.swth_t.local_z, axis=-1)
        ashp = (self.r_t.shape[0], 1, self.r_t.shape[2])
        self.v_t[..., 0] = np.sum(self.swth_t.v_ecef.reshape(ashp) * self.swth_t.local_x, axis=-1)
        self.v_t[..., 1] = np.sum(self.swth_t.v_ecef.reshape(ashp) * self.swth_t.local_y, axis=-1)
        self.v_t[..., 2] = np.sum(self.swth_t.v_ecef.reshape(ashp) * self.swth_t.local_z, axis=-1)
        self.v_r[..., 0] = np.sum(self.swth_r.v_ecef.reshape(ashp) * self.swth_t.local_x, axis=-1)
        self.v_r[..., 1] = np.sum(self.swth_r.v_ecef.reshape(ashp) * self.swth_t.local_y, axis=-1)
        self.v_r[..., 2] = np.sum(self.swth_r.v_ecef.reshape(ashp) * self.swth_t.local_z, axis=-1)
        # Now an additional line of sight for an antenna separated by a certain Baseline
        r_r2 = self.r_r + self.antaxes_local[...,1]  # this adds baseline along antenna axis_
        r_r2_n = np.linalg.norm(r_r2, axis=2)
        self.r_v_r2 = r_r2 / r_r2_n[:,:, np.newaxis]

        # Magnitude (norm) of r_t and r_r
        self.r_n_t = np.linalg.norm(self.r_t, axis=2)
        self.r_n_r = np.linalg.norm(self.r_r, axis=2)
        self.r_v_t = self.r_t / self.r_n_t[:,:, np.newaxis]
        self.r_v_r = self.r_r / self.r_n_r[:,:, np.newaxis]
        # Monostatic equivalent
        # we do not want to normalize here, since the loss in the maginute (w.r.t. 2, for the monostatic case)
        # is useful information as it applies also to the effective wavenumber.
        self.r_2w_me = self.r_v_t + self.r_v_r
        # angle of incidence for ME
        self.k_scaling_me = np.linalg.norm(self.r_2w_me, axis=-1)
        self.inc_me = np.arccos(np.abs(self.r_2w_me[...,2])/self.k_scaling_me)
        self.k_scaling_me = self.k_scaling_me / 2
        # Time derivative of bistatic range
        v_t_rad = np.sum(self.v_t * self.r_v_t, axis=2)
        v_r_rad = np.sum(self.v_r * self.r_v_r, axis=2)
        self.dr_b = -v_t_rad - v_r_rad
        # Second derivative
        self.ddr_b = ((np.sum(self.v_t**2, axis=2) - v_t_rad**2) / self.r_n_t
                      + (np.sum(self.v_r**2, axis=2) - v_r_rad**2) / self.r_n_r)
        # Surface gradient of r_b
        self.sgrad_r_b = self.r_v_t[:, :, 0:2] + self.r_v_r[:, :, 0:2]
        # Surface gradient of dr_b (time-derivative of r_b)
        self.sgrad_dr_b = ((v_t_rad[:,:, np.newaxis] * self.r_v_t[:, :, 0:2] - self.v_t[:, :, 0:2]) / self.r_n_t[:,:, np.newaxis]
                           + (v_r_rad[:,:, np.newaxis] * self.r_v_r[:, :, 0:2] - self.v_r[:, :, 0:2]) / self.r_n_r[:,:, np.newaxis])
        # Initialize latitude
        self.lat = 0

    @property
    def lat(self):
        """ """
        return self._lat

    @lat.setter
    def lat(self, lat):
        self.set_lat(lat)

    def set_lat(self, lat):
        self._lat = lat
        mid_range = int(self.swth_t.lats.shape[1] / 2)
        lats = self.swth_t.lats
        asclats = lats[self.swth_t.asc_idx[0] : self.swth_t.asc_idx[1], mid_range]
        dsclats = lats[self.swth_t.asc_idx[1] :, mid_range]
        self.__asc_latind = np.argmin(np.abs(asclats - lat)) + self.swth_t.asc_idx[0]
        self.__dsc_latind = np.argmin(np.abs(dsclats - lat)) + self.swth_t.asc_idx[1]
        self.swth_t.lat = lat
        self.swth_r.lat = lat
        self._asc_incm2dot_r_b = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.dr_b[self.__asc_latind],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._asc_incm2ddot_r_b = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.ddr_b[self.__asc_latind],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._asc_incm2sgrad_r_b_x = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.sgrad_r_b[self.__asc_latind, :, 0],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._asc_incm2sgrad_r_b_y = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.sgrad_r_b[self.__asc_latind, :, 1],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._asc_incm2sgrad_dr_b_x = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.sgrad_dr_b[self.__asc_latind, :, 0],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._asc_incm2sgrad_dr_b_y = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.sgrad_dr_b[self.__asc_latind, :, 1],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._asc_incm2inc_me = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.inc_me[self.__asc_latind, :],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._asc_incm2k_scaling_me = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.k_scaling_me[self.__asc_latind, :],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._asc_incm2r_n_t = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.r_n_t[self.__asc_latind, :],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._asc_incm2r_n_r = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.r_n_r[self.__asc_latind, :],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        # Descending
        self._dsc_incm2dot_r_b = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.dr_b[self.__dsc_latind],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._dsc_incm2ddot_r_b = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.ddr_b[self.__dsc_latind],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._dsc_incm2sgrad_r_b_x = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.sgrad_r_b[self.__dsc_latind, :, 0],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._dsc_incm2sgrad_r_b_y = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.sgrad_r_b[self.__dsc_latind, :, 1],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._dsc_incm2sgrad_dr_b_x = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.sgrad_dr_b[self.__dsc_latind, :, 0],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._dsc_incm2sgrad_dr_b_y = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.sgrad_dr_b[self.__dsc_latind, :, 1],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._dsc_incm2inc_me = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.inc_me[self.__dsc_latind, :],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._dsc_incm2k_scaling_me = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.k_scaling_me[self.__dsc_latind, :],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._dsc_incm2r_n_t = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.r_n_t[self.__dsc_latind, :],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self._dsc_incm2r_n_r = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.r_n_r[self.__dsc_latind, :],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )

    def inc2r_t(self, inc, ascending=True):
        """ Returns range to transmitter

        Parameters
        ----------
        inc : float or np.ndarray

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if ascending:
            return self._asc_incm2r_n_t(inc)
        else:
            return self._dsc_incm2r_n_t(inc)

    def inc2r_r(self, inc, ascending=True):
        """ Returns range to receiver

        Parameters
        ----------
        inc : float or np.ndarray

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if ascending:
            return self._asc_incm2r_n_r(inc)
        else:
            return self._dsc_incm2r_n_r(inc)

    def inc2me_inc(self, inc, ascending=True):
        """ Returns angle of incidence of monostatic equivalent

        Parameters
        ----------
        inc : float or np.ndarray

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if ascending:
            return self._asc_incm2inc_me(inc)
        else:
            return self._dsc_incm2inc_me(inc)

    def inc2me_k_scaling(self, inc, ascending=True):
        """ Returns the amplitude scaling of the bistatic wavenumber.
        The result should be 1 in the monostatic case, and zero if the
        bistatic angle is pi.

        Parameters
        ----------
        inc : float or np.ndarray

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if ascending:
            return self._asc_incm2k_scaling_me(inc)
        else:
            return self._dsc_incm2k_scaling_me(inc)

    def inc2bistatic_angle_az(self, inc_m, ascending=True):
        """
        Calculates the azimuth projected bistatic angle.

        Parameters
        ----------
        inc : float or ndarray
            Incidence angle on the surface.
        ascending : bool
            If true, return the results for the ascending par of the orbit
            (Default value = True).

        Returns
        -------
        float or ndarray
            The bistatic angle between the two instruments.
        """
        cmp_nrth = self.swth_r.inc2northing(inc_m, ascending=ascending)
        ref_nrth = self.swth_t.inc2northing(inc_m, ascending=ascending)
        return (cmp_nrth - ref_nrth)

    def inc2slave_inc(self, inc, ascending=True):
        """

        Parameters
        ----------
        inc :

        ascending :
             (Default value = True)

        Returns
        -------

        """
        return self.swth_r.inc2slave_inc(inc, ascending=ascending)

    def inc2dot_r_b(self, inc, ascending=True):
        """

        Parameters
        ----------
        inc :

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if ascending:
            return self._asc_incm2dot_r_b(inc)
        else:
            return self._dsc_incm2dot_r_b(inc)

    def inc2ddot_r_b(self, inc, ascending=True):
        """

        Parameters
        ----------
        inc :

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if ascending:
            return self._asc_incm2ddot_r_b(inc)
        else:
            return self._dsc_incm2ddot_r_b(inc)

    def inc2sgrad_r_b(self, inc, ascending=True):
        """

        Parameters
        ----------
        inc :

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if ascending:
            grad_x = self._asc_incm2sgrad_r_b_x(inc)
            grad_y = self._asc_incm2sgrad_r_b_y(inc)
            return np.stack([grad_x, grad_y], axis=-1)
        else:
            grad_x = self._dsc_incm2sgrad_r_b_x(inc)
            grad_y = self._dsc_incm2sgrad_r_b_y(inc)
            return np.stack([grad_x, grad_y], axis=-1)

    def inc2sgrad_dot_r_b(self, inc, ascending=True):
        """

        Parameters
        ----------
        inc :

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if ascending:
            grad_x = self._asc_incm2sgrad_dr_b_x(inc)
            grad_y = self._asc_incm2sgrad_dr_b_y(inc)
            return np.stack([grad_x, grad_y], axis=-1)
        else:
            grad_x = self._dsc_incm2sgrad_dr_b_x(inc)
            grad_y = self._dsc_incm2sgrad_dr_b_y(inc)
            return np.stack([grad_x, grad_y], axis=-1)

    def train_off_track_displacement(self, inc, dotr_s=1, ascending=True):
        """
        Calculates displacement of target in SAR image due to a motion induced
        derivative of the bistatic range.

        Parameters
        ----------
        inc : float | np.ndarray
            Incident angle, in radians.
        dotr_s: float
            Time derivative of bistatic range due to target motion.
        ascending : bool
             If true, ascending orbit, else descending (Default value = True).

        Returns
        -------
        tuple
            Tuple containing the temporal offset, the offset in the azimuth
            (cross-track) direction, and a tuple containing parameters related
            to the derivatives. The latter contains three variables: the ratio
            of the first derivative of the bistatic range wrt to the azimuth
            distance to the second derivative, the derivate of the bistatic
            range wrt to time, the 2nd derivate of the bistatic range wrt to and
            an alternative expression for the temporal offset.
            time
        """
        # azimuth (time) shift
        c1 = self.inc2sgrad_r_b(inc, ascending=ascending)[:, 0] / self.inc2sgrad_dot_r_b(inc, ascending=ascending)[:, 0]
        d_r_b = self.inc2dot_r_b(inc, ascending=ascending)
        dd_r_b = self.inc2ddot_r_b(inc, ascending=ascending)
        dta = (dd_r_b * c1 - d_r_b - dotr_s)

        dta2 = dta - np.sqrt((dd_r_b * c1 - d_r_b)**2 + dotr_s * (dotr_s + 2 * dd_r_b))
        dta = dta - np.sign(dta) * np.sqrt((dd_r_b * c1 - d_r_b - dotr_s)**2 + 2 * c1 * dd_r_b * dotr_s)
        dta2 = dta2 / dd_r_b
        dta = dta / dd_r_b
        dx = (dd_r_b * dta + dotr_s) / self.inc2sgrad_dot_r_b(inc, ascending=ascending)[:, 0]
        return dta, dx, (c1, d_r_b, dd_r_b, dta2)

    def k_ground(self, df, dta, f0=None, ascending=True):
        if f0 is None:
            f0 = self.conf.sar.f0
        k0 = 2 * np.pi * f0 / scipy.constants.c
        dk = df * 2 * np.pi / scipy.constants.c
        if ascending:
            orbind = self.__asc_latind
        else:
            orbind = self.__dsc_latind
        v_t = self.v_t[orbind]
        v_r = self.v_r[orbind]
        r_i = self.r_v_t[orbind]
        r_s = self.r_v_r[orbind]
        dr_i = (np.sum(r_i * v_t, axis=-1)[..., np.newaxis] * r_i - v_t) / self.r_n_t[orbind, ...,np.newaxis]
        dr_s = (np.sum(r_s * v_r, axis=-1)[..., np.newaxis] * r_s - v_r) / self.r_n_r[orbind, ...,np.newaxis]
        kv = (k0 + dk) * (r_i + r_s) + k0 * (dr_i + dr_s) * dta
        return kv

    def dk_ground_dt(self, f0=None, ascending=True):
        """
        Derivative of bistatic wavenumber vector at the ground w.r.t. azimuth time.

        Parameters
        ----------
        f0 : float
            Carrier frequency, defaults to value in conf file passed to initialize function.
        ascending : bool
            True for ascending.

        Returns
        -------
        np.ndarray
            The derivative w.r.t azimuth time.
        """
        if f0 is None:
            f0 = self.conf.sar.f0
        k0 = 2 * np.pi * f0 / scipy.constants.c
        if ascending:
            orbind = self.__asc_latind
        else:
            orbind = self.__dsc_latind
        v_t = self.v_t[orbind]
        v_r = self.v_r[orbind]
        r_i = self.r_v_t[orbind]
        r_s = self.r_v_r[orbind]
        dr_i = (np.sum(r_i * v_t, axis=-1)[..., np.newaxis] * r_i - v_t) / self.r_n_t[orbind, ...,np.newaxis]
        dr_s = (np.sum(r_s * v_r, axis=-1)[..., np.newaxis] * r_s - v_r) / self.r_n_r[orbind, ...,np.newaxis]
        dkvdt = k0 * (dr_i + dr_s)
        return dkvdt

    def dk_ground_df(self, ascending=True):
        """
        Derivative of bistatic wavenumber vector at the ground w.r.t. frequency.

        Parameters
        ----------
        ascending : bool
            True for ascending.

        Returns
        -------
        np.ndarray
            The derivative w.r.t frequency.
        """
        if ascending:
            orbind = self.__asc_latind
        else:
            orbind = self.__dsc_latind
        r_i = self.r_v_t[orbind]
        r_s = self.r_v_r[orbind]
        dkvdf = 2 * np.pi / scipy.constants.c * (r_i + r_s)
        return dkvdf

    def dk_ground_dbati(self, f0=None, ascending=True):
        """
        Derivative of bistatic wavenumber vector at the ground w.r.t. baseline
        (or along-track position on receive antenna).

        Parameters
        ----------
        f0 : float
            Carrier frequency, defaults to value in conf file passed to initialize function.
        ascending : bool
            True for ascending.

        Returns
        -------
        np.ndarray
            The derivative w.r.t the baseline.
        """
        if f0 is None:
            f0 = self.conf.sar.f0
        k0 = 2 * np.pi * f0 / scipy.constants.c
        if ascending:
            orbind = self.__asc_latind
        else:
            orbind = self.__dsc_latind
        #v_t = self.v_t[orbind]
        #v_r = self.v_r[orbind]
        #r_i = self.r_v_t[orbind]
        r_s = self.r_v_r[orbind]
        r_s2 = self.r_v_r2[orbind]
        #dr_i = (np.sum(r_i * v_t, axis=-1)[..., np.newaxis] * r_i - v_t) / self.r_n_t[orbind, ...,np.newaxis]
        #dr_s = (np.sum(r_s * v_r, axis=-1)[..., np.newaxis] * r_s - v_r) / self.r_n_r[orbind, ...,np.newaxis]
        #dr_s2 = (np.sum(r_s2 * v_r, axis=-1)[..., np.newaxis] * r_s - v_r) / self.r_n_r[orbind, ...,np.newaxis]
        dkvdbati = k0 * (r_s2 - r_s)
        return dkvdbati

    def bati2insarpar(self, inc, f0=None, ascending=True):
        """
        Computes short-baseline InSAR paramters for a 1 m baseline along antenna
        axis.

        Parameters
        ----------
        inc: float, np.ndarray
            angle of incidence of incident wave, in radians
        f0 : float
            Carrier frequency, defaults to value in conf file passed to initialize function.
        ascending : bool
            True for ascending.

        Returns
        -------
        dict
            A dictionary with:
            'dfdb': The frequency (spectral) shift, in Hz, per 1 m baseline
            'dtdb': The ati lag per 1 m baseline
            'dkzdb': The delta kz (i.e. 2\pi/h_amb) per 1 m baseline
            'dkzdb_rar': The delta kz for the real-aperture interferometer,
            i.e. without coregistration, which only applies if also no SAR
            processing is done.
        """
        if ascending:
            orbind = self.__asc_latind
        else:
            orbind = self.__dsc_latind
        dkdt = self.dk_ground_dt(f0=f0, ascending=ascending)
        dkdf = self.dk_ground_df(ascending=ascending)
        dkdbati = self.dk_ground_dbati(f0=f0, ascending=ascending)
        A = np.zeros((dkdt.shape[0],2,2))
        A[:, :, 0] = dkdf[:,0:2]
        A[:, :, 1] = dkdt[:,0:2]
        invA = np.linalg.inv(A)
        b = - dkdbati[:, 0:2]
        df_dt = np.einsum("...ij,...j->...i", invA, b)
        # dkz of second antenna after alignment
        dkz = dkdbati[:,2] + dkdt[:, 2] * df_dt[:,1] + dkdf[:, 2] * df_dt[:,0]
        inc_m = self.swth_t.master_inc[orbind, :]
        inc2dfdb = interpolate.interp1d(inc_m, df_dt[:,0],
                                        "quadratic",
                                        bounds_error=False,
                                        fill_value=np.NaN)
        inc2dtdb = interpolate.interp1d(inc_m, df_dt[:,1],
                                        "quadratic",
                                        bounds_error=False,
                                        fill_value=np.NaN)
        inc2dkzdb = interpolate.interp1d(inc_m, dkz,
                                         "quadratic",
                                         bounds_error=False,
                                         fill_value=np.NaN)
        inc2dkz0db = interpolate.interp1d(inc_m, dkdbati[:,2],
                                         "quadratic",
                                         bounds_error=False,
                                         fill_value=np.NaN)
        return {"dfdb": inc2dfdb(inc),
                "dtdb": inc2dtdb(inc),
                "dkzdb":inc2dkzdb(inc),
                "dkzdb_rar":inc2dkz0db(inc)}

    def inc2specsup(self, inc, mode='IWS', ascending=True, f0=None):
        """Calculate the spectral support from the incidence angle.

        Parameters
        ----------
        inc : float
            incidence angle of incident wave (radians).
        mode : string
            'IWS' (default).
        ascending : bool
            True for ascending orbit, False for descending.
        f0 : float
            carrier frequency to superseed value read from config file.

        Returns
        -------
        dictionary
            Corners of spectral support region and other goodies.
        """
        if ascending:
            orbind = self.__asc_latind
        else:
            orbind = self.__dsc_latind
        if f0 is None:
            f0 = self.conf.sar.f0
        inc_m = self.swth_t.master_inc[orbind, :]
        inc_ind = np.argmin(np.abs(inc-inc_m))
        inc_near = np.radians(self.conf.IWS.inc_near)
        inc_far = np.radians(self.conf.IWS.inc_far)
        swath = np.where(np.logical_and(inc > inc_near, inc < inc_far))[0]
        sw = 0
        if swath.size > 0:
            sw = swath[0]
        proc_bw = self.conf.IWS.proc_bw[sw]
        pulse_bw = self.conf.IWS.pulse_bw[sw]
        dta =proc_bw/(self.inc2ddot_r_b((inc))/(scipy.constants.c/f0))
        v11 = self.k_ground(-pulse_bw/2, -dta/2, f0=f0, ascending=ascending)[inc_ind]
        v21 = self.k_ground(pulse_bw/2, -dta/2, f0=f0, ascending=ascending)[inc_ind]
        v12 = self.k_ground(-pulse_bw/2, dta/2, f0=f0, ascending=ascending)[inc_ind]
        v22 = self.k_ground(pulse_bw/2, dta/2, f0=f0, ascending=ascending)[inc_ind]
        kv0 = self.k_ground(0, 0, f0=f0, ascending=ascending)[inc_ind]
        bs0 = self.k_ground(-1.5* pulse_bw/2, 0, f0=f0, ascending=ascending)[inc_ind]
        bs1 = self.k_ground(1.5*pulse_bw/2, 0, f0=f0, ascending=ascending)[inc_ind]
        return {'inc': inc, 'dbw': proc_bw, 'pbw': pulse_bw,
                'specsup': (v11, v21, v12, v22), 'center': kv0,  'bisect': (bs0, bs1) }

    def spectral_mask(self, inc, daz, mode='IWS', ascending=True, f0=None, drg=None,
                      baseband=False, Nx=128, Ny=128):
        """
        Find the positions of the spectral support region for a set of incidence
        angles and return the corresponding mask.

        Parameters
        ----------
        inc : float
            incidence angle of incident wave (radians).
        daz : float
            Azimuth sampling of focused imate, in m.
        mode : string
            'IWS' (default).
        ascending : bool
            Self-explainatory.
        f0 : float
            carrier frequency to superseed value read from config file.
        drg : float
            Range sampling of focused imate, in m. If not given an oversampling of
            1.1 is assumed.
        baseband : bool
            If True, spectrum is centered at zero.
        Nx : int
            number of kx samples.
        Ny : int
            number of ky samples.

        Returns
        -------
        dictionary
            Spectral support mask and kx and ky vectors.
        """
        from matplotlib.path import Path
        support = self.inc2specsup(inc, mode=mode, ascending=ascending, f0=f0)
        verts = np.zeros((4 , 2))
        verts[0,:] = support['specsup'][0][0:2]
        verts[1,:] = support['specsup'][1][0:2]
        verts[2,:] = support['specsup'][3][0:2]
        verts[3,:] = support['specsup'][2][0:2]

        if drg is None:
            drg = scipy.constants.c/2/support['pbw']/1.1/np.sin(support['inc'])
        if baseband:
            kx = 2*np.pi * np.fft.fftshift(np.fft.fftfreq(256, drg))
            ky = 2*np.pi * np.fft.fftshift(np.fft.fftfreq(256, daz))
            verts[:, 0] = verts[:, 0] - support['center'][0]
            verts[:, 1] = verts[:, 1] - support['center'][1]
        else:
            kx = 2*np.pi * np.fft.fftshift(np.fft.fftfreq(Nx, drg)) + support['center'][0]
            ky = 2*np.pi * np.fft.fftshift(np.fft.fftfreq(Ny, daz)) + support['center'][1]
        kkx, kky = np.meshgrid(kx,ky)
        poly_path=Path(verts)
        mask = 1.0 * poly_path.contains_points(np.stack((kkx.flatten(),kky.flatten()), axis=-1)).reshape(kkx.shape)
        for amb in [-2,-1,1,2]:
            mask_a = poly_path.contains_points(np.stack((kkx.flatten(),kky.flatten() + amb * 2*np.pi/daz), axis=-1)).reshape(kkx.shape)
            mask = mask + 1.0 * mask_a
        return {"kx": kx, "ky": ky, "mask": mask}

# %%
if __name__ == '__main__':
    import os
    from matplotlib import pyplot as plt
    stereoid_dir = os.path.expanduser("~/Documents/CODE/STEREOID")
    # drama_dir = os.path.expanduser("~/Code/drama")
    run_id = "2021_1"
    par_dir = os.path.join(stereoid_dir, "PAR")
    par_file = os.path.join(par_dir, ("Hrmny_%s.cfg" % run_id))
    bsgeo = BistaticRadarGeometry(par_file=par_file, companion_delay= 350e3/7.4e3)

#%%
    bsgeo.v_t[3000,::40]
    bsgeo.swth_t._incident.shape
    inc = np.linspace(23, 45, 100)
    plt.figure()
    #plt.plot(np.degrees(bsgeo.swth_t._incident[4000]), bsgeo.dr_b[4000]/0.054)
    plt.plot(inc, bsgeo.inc2dot_r_b(np.radians(inc))/0.054, linewidth=2)
    plt.plot(inc, bsgeo.inc2dot_r_b(np.radians(inc), ascending=False)/0.054, linewidth=2)
    plt.figure()
    plt.plot(inc, bsgeo.inc2ddot_r_b(np.radians(inc))/0.054, linewidth=2)
    plt.plot(inc, bsgeo.inc2ddot_r_b(np.radians(inc), ascending=False)/0.054, linewidth=2)
    #plt.plot(np.degrees(bsgeo.swth_t._incident[3000]), bsgeo.ddr_b[3000]/0.054)
    plt.figure()
    sgrad_r_b = bsgeo.inc2sgrad_r_b(np.radians(inc))
    sgrad_r_b[10]
    sgrad_dr_b = bsgeo.inc2sgrad_dot_r_b(np.radians(inc))
    plt.plot(inc, np.degrees(np.arctan(sgrad_r_b[:,1]/sgrad_r_b[:,0])))
    plt.plot(inc, -np.degrees(np.arctan(sgrad_dr_b[:,1]/sgrad_dr_b[:,0])))
    #plt.plot(inc, sgrad_r_b[:,1]/sgrad_r_b[:,0])
    #plt.plot(inc, sgrad_dr_b[:,1]/sgrad_dr_b[:,0])
    plt.figure()
    plt.plot(inc, bsgeo.inc2r_t(np.radians(inc))/1e3, label="$R_{t, asc}$")
    plt.plot(inc, bsgeo.inc2r_r(np.radians(inc))/1e3, label="$R_{r, asc}$")
    plt.plot(inc, bsgeo.inc2r_t(np.radians(inc), ascending=False)/1e3 + 1, label="$R_{t, dsc}$")
    plt.plot(inc, bsgeo.inc2r_r(np.radians(inc), ascending=False)/1e3, label="$R_{r, dsc}$")
    plt.grid(True)
    plt.legend()
#%%
    # train off track shift
    plt.figure()
    dta, dx, (c1, d_r_b, dd_r_b, dta2) = bsgeo.train_off_track_displacement(np.radians(inc))
    plt.plot(inc, dx, linewidth=2, label=r"$\Delta x$")
    plt.plot(inc, dta * 7e3, linewidth=2, label=r"$\Delta y$")
    # plt.plot(inc, dta2 * 7e3, linewidth=2, label=r"$\Delta y$")
    plt.ylabel("Offset [m]")
    plt.xlabel("Tx angle of incidence [deg]")
    plt.legend()
    d_r_b[10] * dta[10]
    dx[10]
    bsgeo.inc2sgrad_dot_r_b(np.radians(35))
    #plt.savefig("train_off_track_offsets.png")
    plt.figure()
    plt.plot(inc, 90+np.degrees(np.arctan(dta * 7e3/dx)), linewidth=2) #, label=r"$\Delta y$")
    plt.plot(inc, np.degrees(np.arctan(sgrad_r_b[:,1]/sgrad_r_b[:,0])))
    # plt.plot(inc, dta2 * 7e3, linewidth=2)
#%%
    specmask = bsgeo.spectral_mask(np.radians(30), 10, drg=2.5, baseband=False, ascending=False)
    plt.figure()
    plt.imshow(specmask["mask"], origin='lower')
    plt.figure()
    plt.imshow(np.fft.fftshift(np.real(np.fft.ifft2(np.fft.fft2(specmask["mask"])**2))), origin='lower')
    plt.colorbar()
#%%
    print(bsgeo.antaxes_sat[1000])
    # print(bsgeo.antaxes_sat[3000])
    print(bsgeo.antaxes_local[1500,200])
    plt.figure()
    plt.plot(bsgeo.antaxes_sat[:,0,1],label='x')
    plt.plot(bsgeo.antaxes_sat[:,1,1],label='y')
    plt.plot(bsgeo.antaxes_sat[:,2,1],label='z')
    plt.legend()
    plt.figure()
    plt.plot(bsgeo.antaxes_local[3000,:,0,1],label='x')
    plt.plot(bsgeo.antaxes_local[3000,:,1,1],label='y')
    plt.plot(bsgeo.antaxes_local[3000,:,2,1],label='z')
    plt.legend()
    bsgeo.r_r.shape
#%%
    inc = np.linspace(30,45)
    atipar = bsgeo.bati2insarpar(np.radians(inc))
    plt.figure()
    plt.plot(inc,atipar["dtdb"]*9)
    plt.figure()
    plt.plot(inc,atipar["dfdb"]*9)
    plt.figure()
    plt.plot(inc, 2*np.pi/atipar["dkzdb"]/9)
    plt.plot(inc, 2*np.pi/atipar["dkzdb_rar"]/9,"--")
