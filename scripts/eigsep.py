import valon_synth

FREQ = 500.

s = valon_synth.Synthesizer("/dev/ttyUSB0")
#s.set_reference(10)
s.set_ref_select(e_not_i=0)
print("Input reference:", s.get_reference(), s.get_ref_select())
flash = True
for i in [0, 8]:
    print("Channel %d"%i)
    if s.set_frequency(i, FREQ):
        print("Frequency set to %f MHz"%FREQ)
        print("Frequency is %f MHz"%s.get_frequency(i))
    else:
        print("Frequency set failed")
        flash = False
    if s.set_rf_level(i, 5):
        print("RF level set to 5 dBm")
        print("RF level is %d dBm"%s.get_rf_level(i))
    else:
        print("RF level set failed")
        flash = False

if flash:
    s.flash()
