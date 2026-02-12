LED_OUTPUTS_BASE = ['LEDA', 'LEDB', 'LEDC', 'LEDD', 'LEDE', 'LEDF', 'LEDG']

LED_OUTPUTS = LED_OUTPUTS_BASE + ['LEDH', 'LEDI', 'LEDV']

LED_OUTPUTS_WITH_LASER = LED_OUTPUTS + ['LASER650']

LED_DIRECT_PWM = set(LED_OUTPUTS_BASE + ['LEDH'])
LED_VIRTUAL_COMPONENTS = {'LEDB', 'LEDI'}

PUMPS = ['Pump1', 'Pump2', 'Pump3', 'Pump4']

AS7341_CHANNELS = [
    'nm410',
    'nm440',
    'nm470',
    'nm510',
    'nm550',
    'nm583',
    'nm620',
    'nm670',
    'CLEAR',
    'NIR',
    'DARK',
    'ExtGPIO',
    'ExtINT',
    'FLICKER',
]

AS7341_DACS = ['ADC0', 'ADC1', 'ADC2', 'ADC3', 'ADC4', 'ADC5']

AS7341_SPECTRUM_BANDS = AS7341_CHANNELS[:9]
