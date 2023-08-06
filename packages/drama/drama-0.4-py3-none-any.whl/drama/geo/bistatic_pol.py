import numpy as np
import scipy.interpolate as interpolate

from drama.geo.derived_geo import BistaticRadarGeometry


def elfouhaily( psi_i, phi_i, theta_i,
                phi_s, theta_s ):
    """
    Compute the polarization angle of the wave scattered by a perfectly
    conducting surface (with respect to the incident wave polarization), based
    on:
        Elfouhaily, T. et al, A new bistatic model for electromagnetic
        scattering from perfectly conducting random surfaces, Waves in Random
        Media, 1999.

    Parameters
    ----------
    psi_i : float
        polarization orientation of the incident field. psi=0, pi/2 -> H,V
    phi_i : float
        azimuth angle of the source
    theta_i : float
        elevation angle of the source
    phi_s : float
        azimuth angle of the receiver
    theta_s : float
        elevation angle of the receiver

    Returns
    -------
    pol_ang_1: float
        first-iteration polarization rotation of the scattered field with
        respect to the incident one
    pol_ang_2: float
        second-iteration polarization rotation of the scattered field with
        respect to the incident one
    pol_ang_2: float
        first + second-iteration polarization rotation
    P_s_1 : float
        Polarization vector of first-iteration field
    P_s_2 : float
        Polarization vector of second-iteration field
    P_s : float
        P_s_1 + P_s_2. Total polarization vector
    """
    # v_i = np.zeros(3)
    v_i1 = - np.sin(theta_i) * np.sin(phi_i)
    v_i2 = np.sin(theta_i) * np.cos(phi_i)
    v_i3 = -np.cos(theta_i)
    v_i = np.stack( (v_i1, v_i2, v_i3), axis = -1 )
    # Compute scattering (STEREOID) plane normal
    # v_s = np.zeros(3)
    v_s1 = np.sin(theta_s) * np.sin(phi_s)
    v_s2 = - np.sin(theta_s) * np.cos(phi_s)
    v_s3 = np.cos(theta_s)
    v_s = np.stack( (v_s1, v_s2, v_s3), axis = -1 )

    # Wave vector difference
    q = v_s - v_i
    q_h = q.copy()
    q_h[ ..., 2 ] = 0

    Q_h = (v_s / (v_s[ ..., 2 ])[ ..., np.newaxis ] + v_i / (v_i[ ..., 2 ])[ ..., np.newaxis ]) / 2
    Q_h[ ..., 2 ] = 0
    # Incidence field polarization vector
    p_i_v = np.cross( v_i, np.array( [ 0., 0., 1. ] ) )
    p_i_h = np.cross( v_i, p_i_v )
    p_i_v = p_i_v / np.linalg.norm( p_i_v, axis = -1 )[ ..., np.newaxis ]
    p_i_h = p_i_h / np.linalg.norm( p_i_h, axis = -1 )[ ..., np.newaxis ]

    P_i = (np.cos(psi_i)[ ..., np.newaxis ] * p_i_h
           + np.sin(psi_i)[ ..., np.newaxis ] * p_i_v)
    P_h = np.cross(np.array([ 0., 0., 1. ]), P_i )

    # Scattered field polarization vectors
    p_s_v = np.cross( -v_s, np.array( [ 0., 0., 1. ] ) )
    p_s_h = np.cross( -v_s, p_s_v )
    p_s_v = p_s_v / np.linalg.norm( p_s_v, axis = -1 )[ ..., np.newaxis ]
    p_s_h = p_s_h / np.linalg.norm( p_s_h, axis = -1 )[ ..., np.newaxis ]

    ################################
    # First-iteration polarization #
    ################################

    P_s_1 = np.cross( np.cross( q / (q[ ..., 2 ])[ ..., np.newaxis ], P_i ), v_s )
    P_s_1 = P_s_1 / np.linalg.norm( P_s_1, axis = -1 )[ ..., np.newaxis ]

    # Polarization rotation
    cos_psi_s = np.einsum( "...i,...i", P_s_1, p_s_h )
    sin_psi_s = np.einsum( "...i,...i", P_s_1, p_s_v )

    # print(psi_i.shape)
    pol_ang_1 = np.arctan2(sin_psi_s, cos_psi_s) - psi_i

    #################################
    # Second-iteration polarization #
    #################################
    P_s_2 = np.cross( 2 * np.einsum( "...i,...i", q_h / (q[ ..., 2 ])[ ..., np.newaxis ], P_h )[ ..., np.newaxis ] * Q_h
                      - np.einsum( "...i,...i", q_h / (q[ ..., 2 ])[ ..., np.newaxis ], Q_h )[ ..., np.newaxis ] * P_h,
                      v_s )
    cos_psi_s = np.einsum( "...i,...i", P_s_2, p_s_h )
    sin_psi_s = np.einsum( "...i,...i", P_s_2, p_s_v )
    pol_ang_2 = np.arctan2(sin_psi_s, cos_psi_s) - psi_i

    ######################
    # Total polarization #
    ######################
    P_s = P_s_1 + P_s_2
    cos_psi_s = np.einsum( "...i,...i", P_s, p_s_h )
    sin_psi_s = np.einsum( "...i,...i", P_s, p_s_v )
    pol_ang = np.arctan2(sin_psi_s, cos_psi_s) - psi_i

    return pol_ang_1, pol_ang_2, pol_ang, P_s_1, P_s_2, P_s


class CompanionPolarizations(BistaticRadarGeometry):
    """
    This class calculates useful geometric relations.

    Parameters
    ----------
    par_file : str or pathlib.Path
        Parameter file defining orbit, etc
    companion_delay : float
        separation in seconds of companion satellite

    Attributes
    ----------
    qH : np.array
        Receive horizontal polarisation vector.
    qV: np.array
        Receive vertical polarisation vector.
    qO: np.array
        Receive out-of-plane polarisation vector.
    qI: np.array
        Receive in-plane polarisation vector.
    pI: np.array
        Transmit in-plane polarisation vector.
    IOrot : np.array
        Rotation matrix from HV basis to IO basis.
    """
    def __init__(self, par_file, companion_delay=None):
        self.ready = False
        super().__init__(par_file, companion_delay)
        # Receive Polarizarions
        # Horizontal Polarization
        # \hat{r}_r x \hat{z}
        z_n = np.array([0,0,1]).reshape((1, 1, 3))
        self.qH = np.cross(z_n, self.r_v_r, axis=-1)
        self.qH = self.qH / np.linalg.norm(self.qH, axis=2)[..., np.newaxis]
        self.qV = np.cross(self.r_v_r, self.qH, axis=-1)
        self.qV = self.qV / np.linalg.norm(self.qV, axis=2)[..., np.newaxis]
        # Out-of-plane
        self.qO = np.cross(self.r_v_t, self.r_v_r, axis=-1)
        self.qO = self.qO / np.linalg.norm(self.qO, axis=2)[..., np.newaxis]
        if self.qO[:,:,2].mean() < 0:
            self.qO = - self.qO
        # In-plane
        self.qI = np.cross(self.qO, self.r_v_r, axis=-1)
        self.pI = np.cross(self.qO, self.r_v_t, axis=-1)
        # Rotation w.r.t. H-V
        self.IOrot = np.arctan2(np.sum(self.qO * self.qV, axis=-1), np.sum(self.qO * self.qH, axis=-1)) - np.pi/2

        #self.qO = self.qO / np.linalg.norm(self.qO, axis=2)[..., np.newaxis]
        # Principal Polarizations
        # Receive
        # Major
        aux = self.r_v_t + self.r_v_r
        self.qM = np.cross(np.cross(aux, z_n, axis=-1),
                           self.r_v_r, axis=-1)
        self.qM = self.qM / np.linalg.norm(self.qM, axis=2)[..., np.newaxis]
        # Minor
        self.qm = np.cross( self.qM, self.r_v_r, axis=-1)
        self.PRProt = np.arctan2(np.sum(self.qM * self.qV, axis=-1), np.sum(self.qM * self.qH, axis=-1)) - np.pi/2
        # Transmit Polarizations
        self.pH = np.cross(z_n, self.r_v_t, axis=-1)
        self.pH = self.pH / np.linalg.norm(self.pH, axis=2)[..., np.newaxis]
        self.pV = np.cross(self.r_v_t, self.pH, axis=-1)
        self.pV = self.pV / np.linalg.norm(self.pV, axis=2)[..., np.newaxis]

        self.pM = np.cross(np.cross(aux, z_n, axis=-1),
                           self.r_v_t, axis=-1)
        self.pM = self.pM / np.linalg.norm(self.pM, axis=2)[..., np.newaxis]
        # Minor
        self.pm = np.cross( self.pM, self.r_v_t, axis=-1)
        self.PTProt = np.arctan2(np.sum(self.pM * self.pV, axis=-1), np.sum(self.pM * self.pH, axis=-1)) - np.pi/2
        self.IOTrot = np.arctan2(np.sum(self.qO * self.pV, axis=-1), np.sum(self.qO * self.pH, axis=-1)) - np.pi/2
        self.ready = True
        # Initialize latitude
        self.lat = 0

    @property
    def lat(self):
        """ """
        return self._lat

    @lat.setter
    def lat(self, lat):
        """ """
        self.set_lat(lat)

    def set_lat(self, lat):
        """

        Parameters
        ----------
        lat :

        Returns
        -------

        """

        if not self.ready:
            return None
        super().set_lat(lat)
        self._lat = lat
        mid_range = int(self.swth_t.lats.shape[1] / 2)
        lats = self.swth_t.lats
        asclats = lats[self.swth_t.asc_idx[0] : self.swth_t.asc_idx[1], mid_range]
        dsclats = lats[self.swth_t.asc_idx[1] :, mid_range]
        self.__asc_latind = np.argmin(np.abs(asclats - lat)) + self.swth_t.asc_idx[0]
        self.__dsc_latind = np.argmin(np.abs(dsclats - lat)) + self.swth_t.asc_idx[1]
        self.swth_t.lat = lat
        self.swth_r.lat = lat
        # Ascending
        self.__asc_incm2IOrot = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.IOrot[self.__asc_latind],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__asc_incm2IOTrot = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.IOTrot[self.__asc_latind],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__asc_incm2PRProt = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.PRProt[self.__asc_latind],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__asc_incm2PTProt = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            self.PTProt[self.__asc_latind],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        # Descending
        self.__dsc_incm2IOrot = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.IOrot[self.__dsc_latind],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__dsc_incm2IOTrot = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.IOTrot[self.__dsc_latind],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__dsc_incm2PRProt = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.PRProt[self.__dsc_latind],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__dsc_incm2PTProt = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            self.PTProt[self.__dsc_latind],
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        # Now Elfouhaily Polarizations
        # # TODO: Add 2nd order rotations for H tx, this is all for V tx
        # Ascending
        theta_i = self.swth_t.master_inc[self.__asc_latind]
        theta_s = self.inc2slave_inc(theta_i, ascending=True)
        psi_pm = self.PTProt[self.__asc_latind]
        phi_s = self.inc2bistatic_angle_az(theta_i, ascending=True)
        (rot_ang_1, rot_ang_2, rot_ang_tot,
         Ps1, Ps2, Ps_tot) = elfouhaily(np.pi/2, 0,
                                        theta_i, phi_s,
                                        theta_s)
        self.elfrot = rot_ang_tot
        self.KAfrot = rot_ang_1
        self.__asc_incm2Elfouhailyrot_vtx = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            rot_ang_tot,
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__asc_incm2KArot_vtx = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            rot_ang_1,
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__asc_incm2Elfouhaily_Vtx_normp1 = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            np.linalg.norm(Ps1, axis=-1),
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__asc_incm2Elfouhaily_Vtx_normp2 = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            np.linalg.norm(Ps_tot, axis=-1),
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        # H tx
        (rot_ang_1, rot_ang_2, rot_ang_tot,
         Ps1, Ps2, Ps_tot) = elfouhaily(0, 0,
                                        theta_i, phi_s,
                                        theta_s)
        self.__asc_incm2Elfouhailyrot_htx = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            rot_ang_tot,
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__asc_incm2KArot_htx = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            rot_ang_1,
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__asc_incm2Elfouhaily_Htx_normp1 = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            np.linalg.norm(Ps1, axis=-1),
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__asc_incm2Elfouhaily_Htx_normp2 = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            np.linalg.norm(Ps_tot, axis=-1),
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        # q_m (minor PTP) tx
        (rot_ang_1, rot_ang_2, rot_ang_tot,
         Ps1, Ps2, Ps_tot) = elfouhaily(psi_pm, 0,
                                        theta_i, phi_s,
                                        theta_s)
        self.__asc_incm2Elfouhaily_pmtx_normp2 = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            np.linalg.norm(Ps_tot, axis=-1),
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        # q_M (mayor PTP) tx
        (rot_ang_1, rot_ang_2, rot_ang_tot,
         Ps1, Ps2, Ps_tot) = elfouhaily(psi_pm + np.pi/2, 0,
                                        theta_i, phi_s,
                                        theta_s)
        self.__asc_incm2Elfouhaily_pMtx_normp2 = interpolate.interp1d(
            self.swth_t.master_inc[self.__asc_latind],
            np.linalg.norm(Ps_tot, axis=-1),
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        ############
        # Descending
        theta_i = self.swth_t.master_inc[self.__dsc_latind]
        theta_s = self.inc2slave_inc(theta_i, ascending=False)
        psi_pm = self.PTProt[self.__dsc_latind]
        phi_s = self.inc2bistatic_angle_az(theta_i, ascending=False)
        (rot_ang_1, rot_ang_2, rot_ang_tot,
         Ps1, Ps2, Ps_tot) = elfouhaily(np.pi/2, 0,
                                        theta_i, phi_s,
                                        theta_s)

        self.__dsc_incm2Elfouhailyrot_vtx = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            rot_ang_tot,
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__dsc_incm2KArot_vtx = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            rot_ang_1,
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__dsc_incm2Elfouhaily_Vtx_normp1 = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            np.linalg.norm(Ps1, axis=-1),
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__dsc_incm2Elfouhaily_Vtx_normp2 = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            np.linalg.norm(Ps_tot, axis=-1),
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        # H-tx
        (rot_ang_1, rot_ang_2, rot_ang_tot,
         Ps1, Ps2, Ps_tot) = elfouhaily(np.pi/2, 0,
                                        theta_i, phi_s,
                                        theta_s)
        self.__dsc_incm2Elfouhailyrot_htx = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            rot_ang_tot,
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__dsc_incm2KArot_htx = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            rot_ang_1,
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__dsc_incm2Elfouhaily_Htx_normp1 = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            np.linalg.norm(Ps1, axis=-1),
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        self.__dsc_incm2Elfouhaily_Htx_normp2 = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            np.linalg.norm(Ps_tot, axis=-1),
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        # q_m (minor PTP) tx
        (rot_ang_1, rot_ang_2, rot_ang_tot,
         Ps1, Ps2, Ps_tot) = elfouhaily(psi_pm, 0,
                                        theta_i, phi_s,
                                        theta_s)
        self.__dsc_incm2Elfouhaily_pmtx_normp2 = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            np.linalg.norm(Ps_tot, axis=-1),
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )
        # q_M (mayor PTP) tx
        (rot_ang_1, rot_ang_2, rot_ang_tot,
         Ps1, Ps2, Ps_tot) = elfouhaily(psi_pm + np.pi/2, 0,
                                        theta_i, phi_s,
                                        theta_s)
        self.__dsc_incm2Elfouhaily_pMtx_normp2 = interpolate.interp1d(
            self.swth_t.master_inc[self.__dsc_latind],
            np.linalg.norm(Ps_tot, axis=-1),
            "quadratic",
            bounds_error=False,
            fill_value=np.NaN,
        )

    def inc2IOrot(self, inc_m, ascending=True):
        """ Returns the rotation of the In-plane out-of-plane basis
            w.r.t. the H-V basis

        Parameters
        ----------
        inc :

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if ascending:
            return self.__asc_incm2IOrot(inc_m)
        else:
            return self.__dsc_incm2IOrot(inc_m)

    def inc2IOTrot(self, inc_m, ascending=True):
        """ Returns the rotation of the In-plane out-of-plane transmit basis
            w.r.t. the H-V basis

        Parameters
        ----------
        inc :

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if ascending:
            return self.__asc_incm2IOTrot(inc_m)
        else:
            return self.__dsc_incm2IOTrot(inc_m)

    def inc2PRProt(self, inc_m, ascending=True):
        """ Returns the rotation of the In-plane out-of-plane basis
            w.r.t. the H-V basis

        Parameters
        ----------
        inc :

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if ascending:
            return self.__asc_incm2PRProt(inc_m)
        else:
            return self.__dsc_incm2PRProt(inc_m)

    def inc2PTProt(self, inc_m, ascending=True):
        """ Returns the rotation of the In-plane out-of-plane basis
            w.r.t. the H-V basis

        Parameters
        ----------
        inc :

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if ascending:
            return self.__asc_incm2PTProt(inc_m)
        else:
            return self.__dsc_incm2PTProt(inc_m)

    def inc2Elfouhailiyrot(self, inc_m, ascending=True, order=2, txpol='V'):
        """ Returns the rotation of the second-order scattering According
        Elfouhaily '99

        Parameters
        ----------
        inc :

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if (txpol == 'V' or txpol == 'v'):
            if order == 2:
                if ascending:
                    return self.__asc_incm2Elfouhailyrot_vtx(inc_m)
                else:
                    return self.__dsc_incm2Elfouhailyrot_vtx(inc_m)
            elif order == 1:
                if ascending:
                    return self.__asc_incm2KArot_vtx(inc_m)
                else:
                    return self.__dsc_incm2KArot_vtx(inc_m)
            else:
                print("Elfouhaily rotations only defined for order 1 (KA) and 2")
        elif (txpol == 'H' or txpol == 'h'):
            if order == 2:
                if ascending:
                    return self.__asc_incm2Elfouhailyrot_htx(inc_m)
                else:
                    return self.__dsc_incm2Elfouhailyrot_htx(inc_m)
            elif order == 1:
                if ascending:
                    return self.__asc_incm2KArot_htx(inc_m)
                else:
                    return self.__dsc_incm2KArot_htx(inc_m)
            else:
                print("Elfouhaily rotations only defined for order 1 (KA) and 2")

    def inc2Elfouhailiynorm(self, inc_m, ascending=True, order=2, txpol='V'):
        """ Returns the norm of the scattering polarization vector according
        Elfouhaily '99

        Parameters
        ----------
        inc :

        ascending :
             (Default value = True)

        Returns
        -------

        """
        if (txpol == 'V' or txpol == 'v'):
            if order == 2:
                if ascending:
                    return self.__asc_incm2Elfouhaily_Vtx_normp2(inc_m)
                else:
                    return self.__dsc_incm2Elfouhaily_Vtx_normp2(inc_m)
            elif order == 1:
                if ascending:
                    return self.__asc_incm2Elfouhaily_Vtx_normp1(inc_m)
                else:
                    return self.__dsc_incm2Elfouhaily_Vtx_normp1(inc_m)
            else:
                print("Elfouhaily polarization vectors only defined for order 1 (KA) and 2")
        elif (txpol == 'H' or txpol == 'h'):
            if order == 2:
                if ascending:
                    return self.__asc_incm2Elfouhaily_Htx_normp2(inc_m)
                else:
                    return self.__dsc_incm2Elfouhaily_Htx_normp2(inc_m)
            elif order == 1:
                if ascending:
                    return self.__asc_incm2Elfouhaily_Htx_normp1(inc_m)
                else:
                    return self.__dsc_incm2Elfouhaily_Htx_normp1(inc_m)
            else:
                print("Elfouhaily polarization vectors only defined for order 1 (KA) and 2")
        elif (txpol == 'M' or txpol == 'qM'):
            if order == 2:
                if ascending:
                    return self.__asc_incm2Elfouhaily_pMtx_normp2(inc_m)
                else:
                    return self.__dsc_incm2Elfouhaily_pMtx_normp2(inc_m)
            elif order == 1:
                return 1 + np.zeros_like(inc_m)
            else:
                print("Elfouhaily polarization vectors only defined for order 1 (KA) and 2")
        elif (txpol == 'm' or txpol == 'qm'):
            if order == 2:
                if ascending:
                    return self.__asc_incm2Elfouhaily_pmtx_normp2(inc_m)
                else:
                    return self.__dsc_incm2Elfouhaily_pmtx_normp2(inc_m)
            elif order == 1:
                return 1 + np.zeros_like(inc_m)
            else:
                print("Elfouhaily polarization vectors only defined for order 1 (KA) and 2")
        else:
            print("txpol can be H or V")

# %%
if __name__ == '__main__':
    import os
    from matplotlib import pyplot as plt
    stereoid_dir = os.path.expanduser("~/Documents/CODE/STEREOID")
    # drama_dir = os.path.expanduser("~/Code/drama")
    run_id = "2021_1"
    par_dir = os.path.join(stereoid_dir, "PAR")
    par_file = os.path.join(par_dir, ("Hrmny_%s.cfg" % run_id))
    bsgeo = CompanionPolarizations(par_file=par_file, companion_delay= -400e3/7.4e3)
#%%
    bsgeo.r_v_t[1000,100]
    bsgeo.r_v_r[1000,100]
    print(bsgeo.qV[1000,250])
    print(bsgeo.qH[1000,250])
    print(bsgeo.qO[1000,250])
    print(bsgeo.qI[1000,250])
    print(bsgeo.qM[1000,250])
    print(bsgeo.qm[1000,250])
    np.sum(bsgeo.qH[1000,250] * bsgeo.r_v_r[1000,250])
    bsgeo.qO[:,:,2].max()
    bsgeo.IOrot[1000,100]
    np.degrees(bsgeo.inc2IOrot(np.radians(25)))
    np.degrees(bsgeo.inc2PRProt(np.radians(25)))
    (np.degrees(bsgeo.inc2Elfouhailiyrot(np.radians(25))))
    (np.degrees(bsgeo.inc2Elfouhailiyrot(np.radians(25),order=1)))
    #%%
    inc = np.linspace(25, 45)
    plt.figure()
    plt.plot(inc,np.degrees(bsgeo.inc2IOrot(np.radians(inc))) , label='$q_O$')
    plt.plot(inc,np.degrees(bsgeo.inc2PRProt(np.radians(inc))) , label='$q_M$')
    plt.plot(inc,np.degrees(-bsgeo.inc2Elfouhailiyrot(np.radians(inc),order=1)) , label='$q_{KA}$')
    plt.plot(inc,np.degrees(-bsgeo.inc2Elfouhailiyrot(np.radians(inc),order=2)) , label='$q_{2nd}$')
    plt.grid(True)
    plt.legend()
    #plt.savefig("pol_rotations.png")
    #bsgeo.elfrot
    #np.degrees(bsgeo.kktheta_s)
    #bsgeo.kkphi_s
#%%
    bsgeo.swth_t.master_inc.mean()
    theta_i = np.linspace( 20, 45 )
    theta_s = np.linspace( 18, 44 )
    phi_s = 1 * np.linspace( 50, 20 )/10
    (rot_ang_1, rot_ang_2, rot_ang_tot, Ps1, Ps2, Ps_tot) = elfouhaily( 90, 0, theta_i, phi_s, theta_s )
    rot_ang_tot
    np.cross([1,1,0], [0,1,0])
#%%
    psi_i = np.pi/2 + np.zeros(5)
    phi_i = 0
    theta_i = np.radians(np.linspace(20,40,5))
    phi_s = np.zeros_like(theta_i) + np.radians(30)
    theta_s = theta_i - np.radians(5)
    elfouhaily(psi_i, phi_i, theta_i,phi_s, theta_s )
