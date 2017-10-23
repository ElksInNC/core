"""The tests for the uptime sensor platform."""
import unittest
from unittest.mock import patch
from datetime import timedelta

from homeassistant.util.async import run_coroutine_threadsafe
from homeassistant.setup import setup_component
from homeassistant.components.sensor.uptime import UptimeSensor
from tests.common import get_test_home_assistant


class TestUptimeSensor(unittest.TestCase):
    """Test the uptime sensor."""

    def setUp(self):
        """Set up things to run when tests begin."""
        self.hass = get_test_home_assistant()

    def tearDown(self):
        """Stop everything that was started."""
        self.hass.stop()

    def test_uptime_min_config(self):
        """Test minimum uptime configutation."""
        config = {
            'sensor': {
                'platform': 'uptime',
            }
        }
        assert setup_component(self.hass, 'sensor', config)

    def test_uptime_sensor_name_change(self):
        """Test uptime sensor with different name."""
        config = {
            'sensor': {
                'platform': 'uptime',
                'name': 'foobar',
            }
        }
        assert setup_component(self.hass, 'sensor', config)

    def test_uptime_sensor_config_hours(self):
        """Test uptime sensor with hours defined in config."""
        config = {
            'sensor': {
                'platform': 'uptime',
                'unit_of_measurement': 'hours',
            }
        }
        assert setup_component(self.hass, 'sensor', config)

    def test_uptime_sensor_days_output(self):
        """Test uptime sensor output data."""
        sensor = UptimeSensor('test', 'days')
        self.assertEqual(sensor.unit_of_measurement, 'days')
        new_time = sensor.initial + timedelta(days=1)
        with patch('homeassistant.util.dt.now', return_value=new_time):
            run_coroutine_threadsafe(
                sensor.async_update(),
                self.hass.loop
            ).result()
            self.assertEqual(format(round(sensor.state, 2), '.2f'), 1.00)
        new_time = sensor.initial + timedelta(days=111.499)
        with patch('homeassistant.util.dt.now', return_value=new_time):
            run_coroutine_threadsafe(
                sensor.async_update(),
                self.hass.loop
            ).result()
            self.assertEqual(format(round(sensor.state, 2), '.2f'), 111.50)

    def test_uptime_sensor_hours_output(self):
        """Test uptime sensor output data."""
        sensor = UptimeSensor('test', 'hours')
        self.assertEqual(sensor.unit_of_measurement, 'hours')
        new_time = sensor.initial + timedelta(hours=16)
        with patch('homeassistant.util.dt.now', return_value=new_time):
            run_coroutine_threadsafe(
                sensor.async_update(),
                self.hass.loop
            ).result()
            self.assertEqual(format(round(sensor.state, 2), '.2f'), 16.00)
        new_time = sensor.initial + timedelta(hours=72.499)
        with patch('homeassistant.util.dt.now', return_value=new_time):
            run_coroutine_threadsafe(
                sensor.async_update(),
                self.hass.loop
            ).result()
            self.assertEqual(format(round(sensor.state, 2), '.2f'), 72.50)
