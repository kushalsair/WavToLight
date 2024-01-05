# WavToLight
Conversion of Voice Wavelength to Colors, to observe mel-spectrum

Calculating RGB values given the wavelength of visible light.
    Arguments:
    * Wavelength:  Wavelength in nm.  Scalar floating.
    * MaxIntensity:  The RGB value for maximum intensity.  Scalar 
      integer.
    Returns:
    * 3-element list of RGB values for the input wavelength.  The
      values are scaled from 0 to MaxIntensity, where 0 is the
      lowest intensity and MaxIntensity is the highest.  Integer
      list.
    Visible light is in the range of 380-780 nm.  Outside of this
    range the returned RGB triple is [0,0,0].
  
