"""
Instrument and Operator classes
"""
# Standard library modules
import warnings
import logging

# Non-standard modules
from obspy.core.inventory.response import (Response, InstrumentSensitivity
                                           as obspy_Sensitivity)

# obsinfo modules
from .instrument_component import (InstrumentComponent)

warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger("obsinfo")


class Instrument(object):    # Was a Channel subclass, but don't see why
    """
    An instrument is an ensemble of a sensor, a datalogger and possibly a
    preamplifier. It also includes a selected configuration for each one of
    these instrument components.

    Attributes:
        datalogger (:class:`Datalogger`)
        sensor: (:class:`Sensor`)
        preamplifier: (:class:`Preamplifier`)
        sample_rate (float): from datalogger sample rate
        delay_correction (float): from datalogger delay correction
        seed_band_base_code (str): from sensor band base code
        seed_instrument_code (str): from sensor instrument code
        seed_orientation (str): from orientation in the channel itself
    """

    def __init__(self, attributes_dict, channel_modif={}):
        """
        Constructor

        :param attributes_dict_or_list: instrument attributes
        :type attributes_dict_or_list: dictionary/ObsMetadata object or list
            of dictionaries//ObsMetadata objects
        :param channel_modif: modification of attributes per channel specified
            in stations
        :type channel_modif: dict or object of :class:`ObsMetadata`
        """
        self.correction = None
        self.delay = None

        if not attributes_dict:
            msg = 'No instrument attributes'
            warnings.warn(msg)
            logger.error(msg)
            raise TypeError()

        datalogger_config_selector = attributes_dict.get_configured_element(
            'datalogger_configuration', channel_modif, {}, None)
        sensor_config_selector = attributes_dict.get_configured_element(
            'sensor_configuration', channel_modif, {}, None)
        preamplifier_config_selector = attributes_dict.get_configured_element(
            'preamplifier_configuration', channel_modif, {}, None)

        self.sensor = InstrumentComponent.dynamic_class_constructor(
            'sensor',
            attributes_dict, channel_modif, sensor_config_selector)
        self.preamplifier = InstrumentComponent.dynamic_class_constructor(
            'preamplifier',
            attributes_dict, channel_modif, preamplifier_config_selector)
        self.datalogger = InstrumentComponent.dynamic_class_constructor(
            'datalogger',
            attributes_dict, channel_modif, datalogger_config_selector)
        # add the three component response stages
        self.combine_response_stages()

        # Validate inputs and outputs of complete response sequence and
        # correct delay
        self.integrate_response_stages()
        self.obspy_stages = [x.to_obspy() for x in self.response_stages]
        self.obspy_response = self.to_obspy()
        self.add_sensitivity(self.obspy_response)

    def __repr__(self):
        return f'\nInstrument(Polarity="{self.polarity}", '\
               f'Output sample rate={self.total_output_sample_rate})'

    def combine_response_stages(self):
        """
        Adds all response stages as obsinfo and obpsy objects and renumbers
        them
        """
        response_st = self.sensor.response_stages.stages

        if self.preamplifier and self.preamplifier.response_stages:
            response_st += self.preamplifier.response_stages.stages

        response_st += self.datalogger.response_stages.stages

        # Order the stage_sequence_numbers
        for i in range(len(response_st)):
            response_st[i].stage_sequence_number = i+1

        self.response_stages = response_st

    def integrate_response_stages(self):
        """
        Integrates the stages with one another

        1) Renumber stages sequentially
        2) Verify/set units and sample rates
        3) Assure same frequency is used for consecutive PZ filters
        4) Calculate global polarity of the whole set of response stages
        5) Set global response delay correction
        6) Validate sample_rate expressed in datalogger component is equal to
           global response sample rate
        """
        # Stack response stages
        stages = self.response_stages

        prev_stage = stages[0]
        prev_frequency = prev_stage.filter.normalization_frequency \
            if prev_stage.filter.type == 'PolesZeros' else None
        prev_polarity = prev_stage.polarity
        accum_sample_rate = prev_stage.output_sample_rate

        for this_stage in stages[1:]:
            # 2a) Verify continuity of units
            if prev_stage.output_units != this_stage.input_units:
                msg = f'Stage {prev_stage.stage_sequence_number} and '\
                      f'{this_stage.stage_sequence_number} units don\'t match'
                warnings.warn(msg)
                logger.error(msg)
                raise ValueError(msg)

            # 2b) Verify/set continuity of sample rate
            if prev_stage.input_sample_rate:
                if not this_stage.decimation_factor:
                    msg = f'No decimation factor for stage '\
                          f'{this_stage.stage_sequence_number}, assuming = 1'
                    warnings.warn(msg)
                    logger.warning(msg)
                    this_stage.decimation_factor = 1
                next_input_rate = prev_stage.input_sample_rate \
                    / this_stage.decimation_factor

                if this_stage.input_sample_rate:
                    if this_stage.output_sample_rate != next_input_rate:
                        msg = f'stage {this_stage.stage_sequence_number} '\
                              f'sample rate {this_stage.output_sample_rate} '\
                              f'!= expected {next_input_rate}'
                        warnings.warn(msg)
                        logger.error(msg)
                        raise ValueError(msg)
                else:
                    this_stage.input_sample_rate = accum_sample_rate

            # 2c) Calculate/verify delay and correction
            if this_stage.input_sample_rate:
                this_stage.calculate_delay()
            if self.correction is None and self.delay is not None:
                self.correction = self.delay

            # 3) Station XML requires that all PZ stages have the same
            #    normalization frequency.  Check this condition
            if prev_frequency and prev_frequency != 0 \
                    and this_stage.filter.type == 'PolesZeros':
                if prev_frequency != this_stage.filter.normalization_frequency:
                    msg = 'Normalization frequencies for PZ stages '\
                          f'{prev_stage.stage_sequence_number} and '\
                          f'{this_stage.stage_sequence_number} don\'t match'
                    warnings.warn(msg)
                    logger.warning(msg)
                prev_frequency = this_stage.filter.normalization_frequency

            # 4) Calculate global polarity
            if not this_stage.polarity:  # default polarity is positive
                this_stage.polarity = 1

            prev_polarity *= this_stage.polarity

            prev_stage = this_stage
            prev_frequency = prev_stage.filter.normalization_frequency \
                if prev_stage.filter.type == 'PolesZeros' else None
            accum_sample_rate = prev_stage.output_sample_rate

        # 5) Out of the loop: check global output sample rate
        total_expected_sample_rate = accum_sample_rate

        if not total_expected_sample_rate == self.sample_rate:
            msg = f'Datalogger declared sample rate {self.sample_rate} is '\
                  'different from calculated overall sample rate of stages '\
                  f'{total_expected_sample_rate}'
            warnings.warn(msg)
            logger.warning(msg)

        # Set global response attributes
        self.polarity = prev_polarity
        self.total_output_sample_rate = accum_sample_rate

    def to_obspy(self):
        """
        Return equivalent obspy class

        Returns:
            ():class:`obspy.core.inventory.response.Response`)
        """
        return Response(resource_id=None,
                        instrument_sensitivity=None,
                        instrument_polynomial=None,
                        response_stages=self.obspy_stages)

    def add_sensitivity(self, obspy_response):
        """
        Adds sensitivity to an obspy Response object
        Based on ..misc.obspy_routines.response_with_sensitivity

        Args:
            obspy_response (:class:`obspy.core.inventory.response.Response`):
        """

        response_stg = self.response_stages
        true_input_units = input_units = response_stg[0].input_units
        output_units = response_stg[-1].output_units

        if "PA" in true_input_units.upper():
            # MAKE OBSPY THINK ITS M/S TO CORRECTLY CALCULATE SENSITIVITY
            input_units = "M/S"
        gain_prod = 1.
        for stage in response_stg:
            gain_prod *= stage.gain

        sensitivity = obspy_Sensitivity(
            gain_prod,
            # gain_frequency could be provided, according to StationXML, but we
            # assume it's equal to the gain frequency of first stage
            response_stg[0].gain_frequency,
            input_units=input_units,
            output_units=output_units,
            input_units_description=response_stg[0].input_units_description,
            output_units_description=response_stg[-1].output_units_description
            )

        obspy_response.instrument_sensitivity = sensitivity
        # obspy_response.recalculate_overall_sensitivity(sensitivity.frequency)
        obspy_response.instrument_sensitivity.input_units = true_input_units
        obspy_response.instrument_sensitivity.output_units = output_units

    def get_response_stage(self, num):
        """
        Returns the response stage in a given position

        Args:
            num (int): stage number, starting with zero and ordered from
                sensor to datalogger
        """
        # All response stages are at the instrument_component level
        stages = self.response_stages
        assert(num <= stages[-1].stage_sequence_number), \
            'response stage out of range: {num}'
        return stages[num]

    @property
    def equipment_datalogger(self):
        return self.datalogger.equipment

    @property
    def equipment_sensor(self):
        return self.sensor.equipment

    @property
    def equipment_preamplifier(self):
        return self.preamplifier.equipment

    @property
    def sample_rate(self):
        return self.datalogger.sample_rate

    @property
    def delay_correction(self):
        return self.delay_correction

    @property
    def seed_band_base_code(self):
        return self.sensor.seed_band_base_code

    @property
    def seed_instrument_code(self):
        return self.sensor.seed_instrument_code

    @property
    def seed_orientation(self):
        """
        Same as orientation. Kept for compatibility.
        """
        return self.orientation
