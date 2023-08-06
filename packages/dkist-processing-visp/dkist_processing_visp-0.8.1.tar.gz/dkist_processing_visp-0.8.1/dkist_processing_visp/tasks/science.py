"""ViSP science calibration task."""
import logging
from typing import Generator
from typing import Iterable
from typing import Union

import numpy as np
from astropy.io import fits
from astropy.time import Time
from astropy.time import TimeDelta
from dkist_processing_common.tasks.mixin.quality import QualityMixin
from dkist_processing_math.arithmetic import divide_arrays_by_array
from dkist_processing_math.arithmetic import subtract_array_from_arrays
from dkist_processing_math.statistics import average_numpy_arrays
from dkist_processing_pac import generic
from dkist_processing_pac.TelescopeModel import TelescopeModel

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.parsers.visp_l0_fits_access import VispL0FitsAccess
from dkist_processing_visp.tasks.mixin.corrections import CorrectionsMixin
from dkist_processing_visp.tasks.mixin.input_frame_loaders import InputFrameLoadersMixin
from dkist_processing_visp.tasks.mixin.intermediate_frame_helpers import (
    IntermediateFrameHelpersMixin,
)
from dkist_processing_visp.tasks.visp_base import VispTaskBase


class ScienceCalibration(
    VispTaskBase,
    IntermediateFrameHelpersMixin,
    InputFrameLoadersMixin,
    CorrectionsMixin,
    QualityMixin,
):
    """
    Task class for Visp science calibration of polarized and non-polarized data.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs
    """

    record_provenance = True

    def run(self):
        """
        Run Visp science calibration.

        - Do initial array corrections (dark, solar gain, geometric, spectral)
        - Average beams together
        - Apply a telescope polarization correction (polarized data only)
        - Write out L1 science frames
        - Record quality metrics


        Returns
        -------
        None

        """
        telescope_db = generic.get_default_telescope_db()

        with self.apm_task_step("Do basic corrections"):
            self.do_basic_corrections()

        with self.apm_processing_step("Combining beams"):
            logging.info("Combining beams")
            averaged_beams = self.average_beams()

        if self.constants.correct_for_polarization:
            with self.apm_processing_step("Correcting telescope polarization"):
                final_fits_access = self.telescope_polarization_correction(
                    averaged_beams, telescope_db
                )
        else:
            final_fits_access = averaged_beams

        # Save the final output files
        with self.apm_writing_step("Writing calibrated arrays"):
            logging.info("Writing calibrated arrays")
            self.write_calibrated_array(final_fits_access)

        with self.apm_processing_step("Computing and logging quality metrics"):
            no_of_raw_science_frames: int = self.scratch.count_all(
                tags=[
                    VispTag.input(),
                    VispTag.frame(),
                    VispTag.task("OBSERVE"),
                ],
            )

            self.quality_store_task_type_counts(
                task_type="OBSERVE", total_frames=no_of_raw_science_frames
            )

    def do_basic_corrections(self):
        """Do initial array corrections (dark, solar gain, geometric, spectral). Apply a polarization correction to polarized data only."""
        for exp_time in self.constants.observe_exposure_times:
            for beam in range(1, self.constants.num_beams + 1):
                if self.constants.correct_for_polarization:
                    logging.info(f"Load demodulation matrices for beam {beam}")
                    demod_matrices = self.intermediate_frame_helpers_load_demod_matrices(
                        beam_num=beam
                    )
                try:
                    dark_array = self.intermediate_frame_helpers_load_dark_array(
                        beam=beam, exposure_time=exp_time
                    )
                except StopIteration:
                    raise ValueError(f"No matching dark found for {exp_time = } s")

                for dsps_repeat in range(1, self.constants.num_dsps_repeats + 1):
                    for raster_step in range(0, self.constants.num_raster_steps):
                        apm_str = f"{beam = }, {dsps_repeat = }, and {raster_step = }"
                        with self.apm_processing_step(f"Basic corrections for {apm_str}"):
                            logging.info(f"Processing observe frames from {apm_str}")
                            # Initialize array_stack and headers
                            if self.constants.correct_for_polarization:
                                # Create the 3D stack of corrected modulated arrays
                                array_stack = np.zeros(
                                    (
                                        dark_array.shape[0],
                                        dark_array.shape[1],
                                        self.constants.num_modstates,
                                    )
                                )
                                header_stack = []
                            else:
                                array_stack = None
                                header_stack = None
                            for modstate in range(1, self.constants.num_modstates + 1):
                                # Correct the arrays
                                (corrected_arrays, corrected_headers,) = self.correct_frames(
                                    beam=beam,
                                    modstate=modstate,
                                    raster_step=raster_step,
                                    dsps_repeat=dsps_repeat,
                                    exp_time=exp_time,
                                    dark_array=dark_array,
                                )
                                if self.constants.correct_for_polarization:
                                    # Add this result to the 3D stack
                                    array_stack[:, :, modstate - 1] = next(corrected_arrays)
                                    header_stack.append(next(corrected_headers))

                        if self.constants.correct_for_polarization:
                            with self.apm_processing_step("Applying polarization correction"):
                                intermediate_arrays = self.polarization_correction(
                                    array_stack, demod_matrices
                                )
                                intermediate_headers = self._compute_date_keys(header_stack)

                        else:
                            # TODO: The multiple-exp-per science frame bug can be fixed by removing this next
                            intermediate_headers = self._compute_date_keys(next(corrected_headers))
                            intermediate_arrays = next(corrected_arrays)

                        with self.apm_writing_step("Writing intermediate arrays"):
                            self.intermediate_frame_helpers_write_arrays(
                                arrays=intermediate_arrays,
                                headers=intermediate_headers,
                                beam=beam,
                                dsps_repeat=dsps_repeat,
                                raster_step=raster_step,
                                file_id=intermediate_headers["FILE_ID"],
                                task="INTERMEDIATE_ARRAYS",
                            )

    def write_calibrated_array(self, final_fits_access):
        """
        For polarized data, write out calibrated science frames for all 4 Stokes parameters. For non-polarized data, write out calibrated science frames for Stokes I only.

        Parameters
        ----------
        final_fits_access
            Corrected frames object

        """
        for final_object in final_fits_access:
            if self.constants.correct_for_polarization:  # Write all 4 stokes params
                for i, stokes_param in enumerate(self.constants.stokes_params):
                    final_data = self._re_dummy_data(final_object.data[:, :, i])
                    self.write_cal_array(
                        data=final_data,
                        header=final_object.header,
                        stokes=stokes_param,
                        raster_step=final_object.raster_scan_step,
                        dsps_repeat=final_object.current_dsps_repeat,
                    )
            else:  # Only write stokes I
                final_data = self._re_dummy_data(final_object.data)
                self.write_cal_array(
                    data=final_data,
                    header=final_object.header,
                    stokes="I",
                    raster_step=final_object.raster_scan_step,
                    dsps_repeat=final_object.current_dsps_repeat,
                )

    def correct_frames(
        self,
        beam: int,
        modstate: int,
        raster_step: int,
        dsps_repeat: int,
        exp_time: float,
        dark_array: np.ndarray,
    ):
        """
        Correct this frame.

        Generally the algorithm is:
            1. Gather all geometric and observe object(s) for this beam, raster_step, DSPS repeat and modstate
            2. For polarimetric data, average arrays
            3. Dark correct the array(s)
            4. Solar Gain correct the array(s)
            5. Geo correct the array(s)
            6. Spectral correct arrays



        Parameters
        ----------
        beam
            The beam number for this single step
        modstate
            The modulator state for this single step
        raster_step
            The slit step for this single step
        dsps_repeat
            The current dataset parameters repeat
        exp_time
            The exposure time for this single step
        dark_array
            The dark array to be used during dark correction




        Returns
        -------
            Corrected array(s), header(s)
        """
        angle = self.intermediate_frame_helpers_load_angle(beam=beam)
        state_offset = self.intermediate_frame_helpers_load_state_offset(
            beam=beam, modstate=modstate
        )
        spec_shift = self.intermediate_frame_helpers_load_spec_shift(beam=beam)

        # Get the headers and arrays as iterables
        observe_headers = (
            obj.header
            for obj in self.input_frame_loaders_observe_fits_access_generator(
                modstate=modstate,
                raster_step=raster_step,
                dsps_repeat=dsps_repeat,
                exposure_time=exp_time,
            )
        )
        observe_arrays = (
            self.input_frame_loaders_get_beam(obj.data, beam)
            for obj in self.input_frame_loaders_observe_fits_access_generator(
                modstate=modstate,
                raster_step=raster_step,
                dsps_repeat=dsps_repeat,
                exposure_time=exp_time,
            )
        )

        dark_corrected_arrays = next(subtract_array_from_arrays(observe_arrays, dark_array))

        solar_gain_array = self.intermediate_frame_helpers_load_solar_gain_array(
            beam=beam, modstate=modstate
        )
        gain_corrected_arrays = next(
            divide_arrays_by_array(dark_corrected_arrays, solar_gain_array)
        )

        geo_corrected_arrays = next(
            self.corrections_correct_geometry(gain_corrected_arrays, state_offset, angle)
        )

        spectral_corrected_arrays = self.corrections_remove_spec_geometry(
            geo_corrected_arrays, spec_shift
        )

        return spectral_corrected_arrays, observe_headers

    @staticmethod
    def polarization_correction(array_stack: np.ndarray, demod_matrices: np.ndarray) -> np.ndarray:
        """
        Apply a polarization correction to an array by multiplying the array stack by the demod matrices.

        Parameters
        ----------
        array_stack : np.ndarray
            (x, y, M) stack of corrected arrays with M modulation states

        demod_matrices : np.ndarray
            (x, y, 4, M) stack of demodulation matrices with 4 stokes planes and M modulation states


        Returns
        -------
        np.ndarray
            (x, y, 4) ndarray with the planes being IQUV
        """
        demodulated_array = np.sum(demod_matrices * array_stack[:, :, None, :], axis=3)
        return demodulated_array

    def telescope_polarization_correction(
        self,
        inst_demod_objects: Iterable[VispL0FitsAccess],
        telescope_db: str,
    ) -> Generator[VispL0FitsAccess, None, None]:
        """
        Apply a telescope polarization correction.

        Parameters
        ----------
        inst_demod_objects
            Demodulated averaged objects
        telescope_db : str
            Telescope polarization correction loaded from telescope database


        Returns
        -------
        Generator
            Object with telescope corrections applied

        """
        for obj in inst_demod_objects:
            wavelength = obj.wavelength
            obstime = Time(obj.time_obs)
            tm = TelescopeModel(obj.azimuth, obj.elevation, obj.table_angle)
            tm.load_from_database(telescope_db, obstime.mjd, wavelength)
            mueller_matrix = tm.generate_inverse_telescope_model(M12=True, include_parallactic=True)
            obj.data = self.polarization_correction(obj.data, mueller_matrix)
            yield obj

    @staticmethod
    def _compute_date_keys(headers: Union[Iterable[fits.Header], fits.Header]) -> fits.Header:
        """
        Generate correct DATE-??? header keys from a set of input headers.

        Keys are computed thusly:
        * DATE-BEG - The (Spec-0122) DATE-OBS of the earliest input header
        * DATE-END - The (Spec-0122) DATE-OBS of the latest input header, plus the FPA exposure time

        Returns
        -------
        fits.Header
            A copy of the earliest header, but with correct DATE-??? keys
        """
        if isinstance(headers, fits.Header) or isinstance(
            headers, fits.hdu.compressed.CompImageHeader
        ):
            headers = [headers]

        sorted_obj_list = sorted(
            [VispL0FitsAccess.from_header(h) for h in headers], key=lambda x: Time(x.time_obs)
        )
        date_beg = sorted_obj_list[0].time_obs
        exp_time = TimeDelta(sorted_obj_list[-1].fpa_exposure_time_ms / 1000.0, format="sec")
        date_end = (Time(sorted_obj_list[-1].time_obs) + exp_time).isot

        header = sorted_obj_list[0].header
        header["DATE-BEG"] = date_beg
        header["DATE-END"] = date_end

        return header

    def average_beams(self) -> Generator[VispL0FitsAccess, None, None]:
        """
        Get matching arrays for beam 1 and 2 and average together.

        Returns
        -------
        Generator
            Single averaged beam object

        """
        # Get matching arrays for beam 1 and beam 2
        # average them
        # yield a single result array
        corrected_fits_access_beam1 = self.intermediate_frame_helpers_fits_access_generator(
            tags=[
                VispTag.task("INTERMEDIATE_ARRAYS"),
                VispTag.beam(1),
            ]
        )
        for beam1_fits_access in corrected_fits_access_beam1:
            beam2_fits_access = self.matching_beam_2_fits_access(beam1_fits_access)
            header = beam1_fits_access.header
            avg_array = average_numpy_arrays([beam1_fits_access.data, beam2_fits_access.data])
            hdu = fits.PrimaryHDU(header=header, data=avg_array)
            yield VispL0FitsAccess(hdu=hdu, name=None)

    def _re_dummy_data(self, data: np.ndarray):
        """
        Add the dummy dimension that we have been secretly squeezing out during processing.

        The dummy dimension is required because its corresponding WCS axis contains important information.

        Parameters
        ----------
        data : np.ndarray
            Corrected data
        """
        logging.debug(f"Adding dummy WCS dimension to array with shape {data.shape}")
        return data[None, :, :]

    def matching_beam_2_fits_access(self, beam_1_fits_access: VispL0FitsAccess) -> VispL0FitsAccess:
        """
        Find matching beam 2 object for a given beam 1 object.

        Parameters
        ----------
        beam_1_fits_access : VispL0FitsAccess
            Beam 1 object

        Returns
        -------
        VispL0FitsAccess
            Beam 2 object
        """
        all_tags = list(self.scratch.tags(beam_1_fits_access.name))
        all_tags.remove(VispTag.beam(1))
        all_tags.append(VispTag.beam(2))
        try:
            matching_objs = self.fits_data_read_fits_access(tags=all_tags, cls=VispL0FitsAccess)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Could not find a beam2 match for {beam_1_fits_access.name}"
            ) from e
        return next(matching_objs)

    def write_cal_array(
        self,
        data: np.ndarray,
        header: fits.Header,
        stokes: str,
        raster_step: int,
        dsps_repeat: int,
    ) -> None:
        """
        Write out calibrated array.

        Parameters
        ----------
        data : np.ndarray
            calibrated data to write out

        header : fits.Header
            calibrated header to write out

        stokes : str
            Stokes parameter of this step. 'I', 'Q', 'U', or 'V'

        raster_step : int
            The slit step for this step

        dsps_repeat : int
            The current dataset parameters repeat


        Returns
        -------
        None
        """
        tags = [
            VispTag.calibrated(),
            VispTag.frame(),
            VispTag.stokes(stokes),
            VispTag.raster_step(raster_step),
            VispTag.dsps_repeat(dsps_repeat),
        ]
        hdul = fits.HDUList([fits.PrimaryHDU(header=header, data=data)])
        self.fits_data_write(hdu_list=hdul, tags=tags)

        filename = next(self.read(tags=tags))
        logging.info(f"Wrote intermediate file for {tags = } to {filename}")
