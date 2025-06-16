from argparse import ArgumentParser

import valon_synth

parser = ArgumentParser(description="Program Valon Synthesizer")
parser.add_argument(
    "--port", type=str, default="/dev/ttyUSB0", help="Serial port to use"
)
parser.add_argument(
    "--use_ref", action="store_true", help="Use external 10 MHz reference"
)
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument(
    "-f",
    "--flash",
    action="store_true",
    default=True,
    help="Flash the synthesizer after programming",
)
args = parser.parse_args()

FREQ = 500.0  # MHz
verbose = args.verbose

s = valon_synth.Synthesizer(args.port)

if args.use_ref:  # use external 10 MHz reference
    s.set_reference(10)
r = s.set_ref_select(e_not_i=int(args.use_ref))  # ext: 1, int: 0
if not r:
    raise RuntimeError("Failed to set reference select")

if verbose:
    print("Input reference:", s.get_reference())
    if s.get_ref_select():
        print("Using external reference")
    else:
        print("Using internal reference")

for synth in (valon_synth.SYNTH_A, valon_synth.SYNTH_B):
    r = s.set_frequency(synth, FREQ)
    if not r:
        raise RuntimeError(f"Failed to set frequency for synth {synth}.")
    if verbose:
        print(f"Frequency set to {FREQ} MHz for synth {synth}")
        print(f"Current frequency for synth {synth}: {s.get_frequency(synth)} MHz")
    r = s.set_rf_level(synth, 5)
    if not r:
        raise RuntimeError(f"Failed to set RF level for synth {synth}")
    if verbose:
        print("RF level set to 5 dBm")
        print(f"RF level is {s.get_rf_level(synth)} dBm.")

if args.flash:
    s.flash()
