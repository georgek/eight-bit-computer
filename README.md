# 8-bit Computer

This is stuff for the 8-bit computer.

## EEPROM

The EEPROM scripts output bytes that can be written to an EEPROM.

To write stuff using [eepromino](https://github.com/georgek/eepromino):

```sh
python <script> | eepromino write -
```

- display.py: for the 7-segment display,
- microcode.py: for the CPU microcode.
