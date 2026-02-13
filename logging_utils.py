"""
Chi.Bio Logging Utilities

Provides consistent logging for device-related events, hardware failures,
communication events, and measurements.

Usage:
    from logging_utils import LoggerContext

    # After sysData is initialized in main app
    logger_ctx = LoggerContext(logger, sysData)

    # Then use the methods
    logger_ctx.log_device_event(logging.INFO, 'M0', 'LED calibration completed')
    logger_ctx.log_hardware_failure('M1', 'Multiplexer', attempts=5, fatal=False)
"""

import logging


class LoggerContext:
    """Logging helper that keeps dependencies explicit and testable."""

    def __init__(self, logger, sys_data):
        self._logger = logger
        self._sys_data = sys_data

    def _format_device_message(self, device_id, message):
        try:
            device_name = self._sys_data[device_id].get('DeviceID', 'unknown')
            return f'{message} on {device_id} ({device_name})'
        except (TypeError, KeyError, AttributeError):
            return f'{message} on {device_id}'

    def log_device_event(self, level, device_id, message, exc_info=False):
        """Log device-specific events with consistent formatting."""
        full_msg = self._format_device_message(device_id, message)
        self._logger.log(level, full_msg, exc_info=exc_info)

    def log_hardware_failure(self, device_id, component, attempts, fatal=False, exc_info=False):
        """Log hardware communication failures with appropriate severity."""
        level = logging.CRITICAL if fatal else logging.WARNING
        message = f'Failed to communicate to {component} {attempts} times'
        self.log_device_event(level, device_id, message, exc_info=exc_info)

    def log_comm_event(self, device_id, component, event_type, details='', level=logging.DEBUG):
        """Log communication events with hardware devices."""
        message = f'{component} {event_type}'
        if details:
            message += f': {details}'
        self.log_device_event(level, device_id, message)

    def log_measurement(self, device_id, sensor, value, unit='', level=logging.DEBUG):
        """Log sensor measurements in a consistent format."""
        unit_str = f' {unit}' if unit else ''
        message = f'{sensor} measurement: {value}{unit_str}'
        self.log_device_event(level, device_id, message)
