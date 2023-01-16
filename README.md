# "UNTESTED" Proof of concept Kingblade X10III tuning wavefile generator

    usage: kbx3wave [-h] [-o OUTPUT] [--invert] [--no-normalization] colorfile

    "UNTESTED" Proof of concept Kingblade X10III tuning wavefile generator

    positional arguments:
    colorfile             QR code data from official app

    options:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                            Write wavefile to OUTPUT
    --invert              Invert output signal
    --no-normalization    Skip color normalization


## Usage

    python kbx3wave default_colors.txt

    python kbx3wave default_colors.txt -o tune.wav
