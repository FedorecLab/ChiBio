"""
Chi.Bio Logging Utilities

Provides consistent logging functions for device-related events, hardware failures,
communication events, and measurements.

Usage:
    from logging_utils import setup_logging_utils, log_device_event, log_hardware_failure
    
    # After sysData is initialized in main app
    setup_logging_utils(logger, sysData)
    
    # Then use the functions
    log_device_event(logging.INFO, 'M0', 'LED calibration completed')
    log_hardware_failure('M1', 'Multiplexer', attempts=5, fatal=False)
"""

import logging

# Module-level variables set by setup_logging_utils()
_logger = None
_sysData = None


def setup_logging_utils(logger, sysData):
    """Initialize the logging utilities with logger and sysData references.
    
    Args:
        logger: The logger instance to use for all logging operations
        sysData: Reference to the global sysData dictionary for device info lookup
    """
    global _logger, _sysData
    _logger = logger
    _sysData = sysData


def log_device_event(level, device_id, message, exc_info=False):
    """Log device-specific events with consistent formatting.
    
    Args:
        level: logging level (e.g., logging.INFO, logging.WARNING)
        device_id: Device ID (e.g., 'M0', 'M1')
        message: Log message
        exc_info: Whether to include exception traceback
    
    Usage:
        log_device_event(logging.INFO, 'M0', 'LED calibration completed')
        log_device_event(logging.ERROR, 'M1', 'Sensor malfunction', exc_info=True)
    """
    if _logger is None:
        raise RuntimeError("Logging utils not initialized. Call setup_logging_utils() first.")
    
    # Safely get device ID string, handling cases where sysData might not be initialized
    try:
        device_name = _sysData[device_id].get('DeviceID', 'unknown')
        full_msg = f'{message} on {device_id} ({device_name})'
    except (TypeError, KeyError, AttributeError):
        full_msg = f'{message} on {device_id}'
    
    _logger.log(level, full_msg, exc_info=exc_info)


def log_hardware_failure(device_id, component, attempts, fatal=False, exc_info=False):
    """Log hardware communication failures with appropriate severity.
    
    Args:
        device_id: Device ID (e.g., 'M0', 'M1')
        component: Hardware component name (e.g., 'Multiplexer', 'PWM', 'DAC')
        attempts: Number of failed attempts
        fatal: Whether this is a fatal error requiring shutdown
        exc_info: Whether to include exception traceback
    
    Usage:
        log_hardware_failure('M0', 'Multiplexer', attempts=3, fatal=False)
        log_hardware_failure('M1', 'PWM', attempts=10, fatal=True)
    """
    level = logging.CRITICAL if fatal else logging.WARNING
    message = f'Failed to communicate to {component} {attempts} times'
    log_device_event(level, device_id, message, exc_info=exc_info)


def log_comm_event(device_id, component, event_type, details='', level=logging.DEBUG):
    """Log communication events with hardware devices.
    
    Args:
        device_id: Device ID (e.g., 'M0', 'M1')
        component: Hardware component (e.g., 'AS7341', 'ThermometerInternal')
        event_type: Type of event ('success', 'retry', 'timeout', etc.)
        details: Additional details about the event
        level: Logging level to use
    
    Usage:
        log_comm_event('M0', 'AS7341', 'success')
        log_comm_event('M1', 'AS7341', 'retry', 'timeout after 100ms', level=logging.WARNING)
    """
    message = f'{component} {event_type}'
    if details:
        message += f': {details}'
    log_device_event(level, device_id, message)


def log_measurement(device_id, sensor, value, unit='', level=logging.DEBUG):
    """Log sensor measurements in a consistent format.
    
    Args:
        device_id: Device ID (e.g., 'M0', 'M1')
        sensor: Sensor name (e.g., 'OD', 'Thermostat', 'Spectrometer')
        value: Measured value
        unit: Optional unit string
        level: Logging level to use
    
    Usage:
        log_measurement('M0', 'OD', 0.452, 'AU')
        log_measurement('M1', 'Temperature', 37.5, '°C', level=logging.INFO)
    """
    unit_str = f' {unit}' if unit else ''
    message = f'{sensor} measurement: {value}{unit_str}'
    log_device_event(level, device_id, message)
