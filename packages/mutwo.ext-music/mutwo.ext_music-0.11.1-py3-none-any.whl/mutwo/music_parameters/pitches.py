"""Submodule for the parameter pitch.

'Pitch' is defined as any object that knows a :attr:`frequency` attribute.
The two major modern tuning systems Just intonation and Equal-divided-octave
are supported by the :class:`JustIntonationPitch` and :class:`EqualDividedOctavePitch` classes.
For using Western nomenclature (e.g. c, d, e, f, ...) :mod:`mutwo` offers the
:class:`WesternPitch` class (which inherits from :class:`EqualDividedOctavePitch`).
For a straight frequency-based approach one may use :class:`DirectPitch`.

If desired the default concert pitch can be adjusted after importing :mod:`mutwo`:

    >>> from mutwo import music_parameters
    >>> music_parameters.configurations.DEFAULT_CONCERT_PITCH = 443

All pitch objects with a concert pitch attribute that become initialised after
overriding the default concert pitch value will by default use the new
overridden default concert pitch value.
"""

from __future__ import annotations

import bisect
import collections
import copy
import functools
import math
import numbers
import operator
import typing
import warnings

import primesieve  # type: ignore
from primesieve import numpy as primesieve_numpy

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

from mutwo import core_constants
from mutwo import core_utilities
from mutwo import music_parameters


__all__ = (
    "DirectPitchInterval",
    "DirectPitch",
    "JustIntonationPitch",
    "Partial",
    "EqualDividedOctavePitch",
    "WesternPitch",
    "MidiPitch",
    "CommonHarmonic",
)

ConcertPitch = typing.Union[core_constants.Real, music_parameters.abc.Pitch]
PitchClassOrPitchClassName = typing.Union[core_constants.Real, str]


class DirectPitchInterval(music_parameters.abc.PitchInterval):
    """Simple interval class which gets directly assigned by its cents value

    :param cents: Defines how big or small the interval is.
    :type cents: float
    """

    def __init__(self, cents: float):
        self.cents = cents

    @property
    def cents(self) -> float:
        return self._cents

    @cents.setter
    def cents(self, cents: float):
        self._cents = cents


class DirectPitch(music_parameters.abc.Pitch):
    """A simple pitch class that gets directly initialised by its frequency.

    :param frequency: The frequency of the ``DirectPitch`` object.

    May be used when a converter class needs a pitch object, but there is
    no need or desire for a complex abstraction of the respective pitch
    (that classes like ``JustIntonationPitch`` or ``WesternPitch`` offer).

    **Example:**

    >>> from mutwo.music_parameters import pitches
    >>> my_pitch = pitches.DirectPitch(440)
    """

    def __init__(self, frequency: core_constants.Real, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._frequency = float(frequency)

    @property
    def frequency(self) -> float:
        """The frequency of the pitch."""

        return self._frequency

    def __repr__(self) -> str:
        return "DirectPitch(frequency = {})".format(self.frequency)

    @core_utilities.add_copy_option
    def add(
        self, pitch_interval: music_parameters.abc.PitchInterval, mutate: bool = False
    ) -> DirectPitch:
        self._frequency = self.cents_to_ratio(pitch_interval.cents) * self.frequency
        return self

    @core_utilities.add_copy_option
    def subtract(
        self, pitch_interval: music_parameters.abc.PitchInterval, mutate: bool = False
    ) -> DirectPitch:
        self._frequency = self.frequency / self.cents_to_ratio(pitch_interval.cents)
        return self


class MidiPitch(music_parameters.abc.Pitch):
    """Pitch that is defined by its midi pitch number.

    :param midi_pitch_number: The midi pitch number of the pitch. Floating
        point numbers are possible for microtonal deviations from the
        chromatic scale.
    :type midi_pitch_number: float

    **Example:**

    >>> from mutwo.music_parameters import pitches
    >>> middle_c = pitches.MidiPitch(60)
    >>> middle_c_quarter_tone_high = pitches.MidiPitch(60.5)
    """

    def __init__(self, midi_pitch_number: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._midi_pitch_number = midi_pitch_number

    def __repr__(self) -> str:
        return f"{type(self).__name__}(midi_pitch_number = {self.midi_pitch_number})"

    @property
    def frequency(self) -> float:
        difference_to_middle_a = self.midi_pitch_number - 69
        return float(440 * self.cents_to_ratio(difference_to_middle_a * 100))

    @property
    def midi_pitch_number(self) -> float:
        return self._midi_pitch_number

    @midi_pitch_number.setter
    def midi_pitch_number(self, new_midi_pitch_number: float):
        self._midi_pitch_number = new_midi_pitch_number

    @core_utilities.add_copy_option
    def add(
        self, pitch_interval: music_parameters.abc.PitchInterval, mutate: bool = False
    ) -> MidiPitch:
        self.midi_pitch_number = self.hertz_to_midi_pitch_number(
            self.cents_to_ratio(pitch_interval.cents) * self.frequency
        )
        return self

    @core_utilities.add_copy_option
    def subtract(
        self, pitch_interval: music_parameters.abc.PitchInterval, mutate: bool = False
    ) -> MidiPitch:
        self.midi_pitch_number = self.hertz_to_midi_pitch_number(
            self.frequency / self.cents_to_ratio(pitch_interval.cents)
        )
        return self


class JustIntonationPitch(
    music_parameters.abc.Pitch, music_parameters.abc.PitchInterval
):
    """Pitch that is defined by a frequency ratio and a reference pitch.

    :param ratio_or_exponent_tuple: The frequency ratio of the ``JustIntonationPitch``.
        This can either be a string that indicates the frequency ratio (for
        instance: "1/1", "3/2", "9/2", etc.), or a ``fractions.Fraction``
        object that indicates the frequency ratio (for instance:
        ``fractions.Fraction(3, 2)``, ``fractions.Fraction(7, 4)``) or
        an Iterable that is filled with integer that represents the exponent_tuple
        of the respective prime numbers of the decomposed frequency ratio. The prime
        numbers are rising and start with 2. Therefore the tuple ``(2, 0, -1)``
        would return the frequency ratio ``4/5`` because
        ``(2 ** 2) * (3 ** 0) * (5 ** -1) = 4/5``.
    :param concert_pitch: The reference pitch of the tuning system (the pitch for a
        frequency ratio of 1/1). Can either be another ``Pitch`` object or any number
        to indicate a particular frequency in Hertz.

    The resulting frequency is calculated by multiplying the frequency ratio
    with the respective reference pitch.

    **Example:**

    >>> from mutwo.music_parameters import pitches
    >>> # 3 different variations of initialising the same pitch
    >>> pitches.JustIntonationPitch('3/2')
    >>> import fractions
    >>> pitches.JustIntonationPitch(fractions.Fraction(3, 2))
    >>> pitches.JustIntonationPitch((-1, 1))
    >>> # using a different concert pitch
    >>> pitches.JustIntonationPitch('7/5', concert_pitch=432)
    """

    def __init__(
        self,
        ratio_or_exponent_tuple: typing.Union[
            str, fractions.Fraction, typing.Iterable[int]
        ] = "1/1",
        concert_pitch: ConcertPitch = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if concert_pitch is None:
            concert_pitch = music_parameters.configurations.DEFAULT_CONCERT_PITCH

        self.exponent_tuple = (
            self._translate_ratio_or_fractions_argument_to_exponent_tuple(
                ratio_or_exponent_tuple
            )
        )
        self.concert_pitch = concert_pitch  # type: ignore

    # ###################################################################### #
    #                      static private methods                            #
    # ###################################################################### #
    @staticmethod
    def _adjust_exponent_lengths(
        exponent_tuple0: tuple, exponent_tuple1: tuple
    ) -> tuple:
        r"""Adjust two exponent_tuple, e.g. make their length equal.

        The length of the longer JustIntonationPitch is the reference.

        Arguments:
            * exponent_tuple0: first exponent_tuple to adjust
            * exponent_tuple1: second exponent_tuple to adjust
        >>> v0 = (1, 0, -1)
        >>> v1 = (1,)
        >>> v0_adjusted, v1_adjusted = JustIntonationPitch._adjust_exponent_lengths(v0, v1)
        >>> v0_adjusted
        (1, 0, -1)
        >>> v1_adjusted
        (1, 0, 0)
        """

        length0 = len(exponent_tuple0)
        length1 = len(exponent_tuple1)
        if length0 > length1:
            return exponent_tuple0, exponent_tuple1 + (0,) * (length0 - length1)
        else:
            return exponent_tuple0 + (0,) * (length1 - length0), exponent_tuple1

    @staticmethod
    def _adjust_ratio(ratio: fractions.Fraction, border: int) -> fractions.Fraction:
        r"""Multiply or divide a fractions.Fraction - Object with the border,

        until it is equal or bigger than 1 and smaller than border.

        Arguments:
            * ratio: The Ratio, which shall be adjusted
            * border
        >>> ratio0 = fractions.Fraction(1, 3)
        >>> ratio1 = fractions.Fraction(8, 3)
        >>> border = 2
        >>> JustIntonationPitch._adjust_ratio(ratio0, border)
        fractions.Fraction(4, 3)
        >>> JustIntonationPitch._adjust_ratio(ratio1, border)
        fractions.Fraction(4, 3)

        """

        if border > 1:
            while ratio >= border:
                ratio /= border
            while ratio < 1:
                ratio *= border
        return ratio

    @staticmethod
    def _adjust_float(float_: float, border: int) -> float:
        r"""Multiply float with border, until it is <= 1 and > than border.

        Arguments:
            * float_: The float, which shall be adjusted
            * border
        >>> float0 = 0.5
        >>> float1 = 2
        >>> border = 2
        >>> JustIntonationPitch._adjust_float(float0, border)
        1
        >>> JustIntonationPitch._adjust_float(float1, border)
        1
        """

        if border > 1:
            while float_ > border:
                try:
                    float_ /= border
                except OverflowError:
                    float_ //= border
            while float_ < 1:
                float_ *= border
        return float_

    @staticmethod
    def _adjust_exponent_tuple(
        exponent_tuple: tuple, primes: tuple, border: int
    ) -> tuple:
        r"""Adjust a exponent_tuple and its primes depending on the border.

        Arguments:
            * exponent_tuple: The exponent_tuple, which shall be adjusted
            * primes: Its corresponding primes
            * border
        >>> exponent_tuple0 = (1,)
        >>> primes0 = (3,)
        >>> border = 2
        >>> JustIntonationPitch._adjust_exponent_tuple(exponent_tuple0, primes0, border)
        ((-1, 1), (2, 3))

        """  # TODO(DOCSTRING) Make proper description what actually happens

        if exponent_tuple:
            if border > 1:
                multiplied = functools.reduce(
                    operator.mul, (p ** e for p, e in zip(primes, exponent_tuple))
                )
                res = math.log(border / multiplied, border)
                if res < 0:
                    res -= 1
                res = int(res)
                primes = (border,) + primes
                exponent_tuple = (res,) + exponent_tuple
            return exponent_tuple, primes
        return (1,), (1,)

    @staticmethod
    def _discard_nulls(iterable: typing.Iterable[int]) -> tuple[int, ...]:
        r"""Discard all zeros after the last not 0 - element of an arbitary iterable.

        Return a tuple.
        Arguments:
            * iterable: the iterable, whose 0 - elements shall
              be discarded

        >>> tuple0 = (1, 0, 2, 3, 0, 0, 0)
        >>> ls = [1, 3, 5, 0, 0, 0, 2, 0]
        >>> JustIntonationPitch._discard_nulls(tuple0)
        (1, 0, 2, 3)
        >>> JustIntonationPitch._discard_nulls(ls)
        (1, 3, 5, 0, 0, 0, 2)
        """

        iterable = tuple(iterable)
        c = 0
        for i in reversed(iterable):
            if i != 0:
                break
            c += 1
        if c != 0:
            return iterable[:-c]
        return iterable

    @staticmethod
    def _exponent_tuple_to_pair(exponent_tuple: tuple, primes: tuple) -> tuple:
        r"""Transform a JustIntonationPitch to a (numerator, denominator) - pair.

        Arguments are:
            * JustIntonationPitch -> The exponent_tuple of prime numbers
            * primes -> the referring prime numbers
        >>> myJustIntonationPitch0 = (1, 0, -1)
        >>> myJustIntonationPitch1 = (0, 2, 0)
        >>> myVal0 = (2, 3, 5)
        >>> myVal1 = (3, 5, 7)
        >>> JustIntonationPitch._exponent_tuple_to_pair(myJustIntonationPitch0, myVal0)
        (2, 5)
        >>> JustIntonationPitch._exponent_tuple_to_pair(myJustIntonationPitch0, myVal1)
        (3, 7)
        >>> JustIntonationPitch._exponent_tuple_to_pair(myJustIntonationPitch1, myVal1)
        (25, 1)
        """

        numerator = 1
        denominator = 1
        for number, exponent in zip(primes, exponent_tuple):
            if exponent > 0:
                numerator *= pow(number, exponent)
            elif exponent < 0:
                denominator *= pow(number, -exponent)
        return numerator, denominator

    @staticmethod
    def _exponent_tuple_to_ratio(
        exponent_tuple: tuple, primes: tuple
    ) -> fractions.Fraction:
        r"""Transform a JustIntonationPitch to a fractions.Fraction - Object

        (if installed to a quicktions.fractions.Fraction - Object,
        otherwise to a fractions.fractions.Fraction - Object).

        Arguments are:
            * JustIntonationPitch -> The exponent_tuple of prime numbers
            * primes -> the referring prime numbers for the underlying
                      ._exponent_tuple - Argument (see JustIntonationPitch._exponent_tuple).
        >>> myJustIntonationPitch0 = (1, 0, -1)
        >>> myPrimes= (2, 3, 5)
        >>> JustIntonationPitch._exponent_tuple_to_ratio(myJustIntonationPitch0, myPrimes)
        2/5
        """

        numerator, denominator = JustIntonationPitch._exponent_tuple_to_pair(
            exponent_tuple, primes
        )
        return JustIntonationPitch._adjust_ratio(
            fractions.Fraction(numerator, denominator), 1
        )

    @staticmethod
    def _exponent_tuple_to_float(exponent_tuple: tuple, primes: tuple) -> float:
        r"""Transform a JustIntonationPitch to a float.

        Arguments are:
            * JustIntonationPitch -> The exponent_tuple of prime numbers
            * primes -> the referring prime numbers for the underlying
                      ._exponent_tuple - Argument (see JustIntonationPitch._exponent_tuple).
            * primes-shift -> how many prime numbers shall be skipped
                            (see JustIntonationPitch.primes_shift)

        >>> myJustIntonationPitch0 = (1, 0, -1)
        >>> myJustIntonationPitch1 = (0, 2, 0)
        >>> myPrimes = (2, 3, 5)
        >>> JustIntonationPitch._exponent_tuple_to_float(myJustIntonationPitch0, myPrimes)
        0.4
        """

        numerator, denominator = JustIntonationPitch._exponent_tuple_to_pair(
            exponent_tuple, primes
        )
        try:
            return numerator / denominator
        except OverflowError:
            return numerator // denominator

    @staticmethod
    def _ratio_to_exponent_tuple(ratio: fractions.Fraction) -> tuple:
        r"""Transform a fractions.Fraction - Object to a vector of exponent_tuple.

        :param ratio: The fractions.Fraction, which shall be transformed

        **Example:**

        >>> try:
        >>>     from quicktions import fractions.Fraction
        >>> except ImportError:
        >>>     from fractions import fractions.Fraction
        >>> myRatio0 = fractions.Fraction(3, 2)
        >>> JustIntonationPitch._ratio_to_exponent_tuple(myRatio0)
        (-1, 1)
        """

        factorised_numerator = core_utilities.factors(ratio.numerator)
        factorised_denominator = core_utilities.factors(ratio.denominator)

        factorised_num = core_utilities.factorise(ratio.numerator)
        factorised_den = core_utilities.factorise(ratio.denominator)

        biggest_prime = max(factorised_num + factorised_den)
        exponent_tuple = [0] * primesieve.count_primes(biggest_prime)

        for prime, fac in factorised_numerator:
            if prime > 1:
                exponent_tuple[primesieve.count_primes(prime) - 1] += fac

        for prime, fac in factorised_denominator:
            if prime > 1:
                exponent_tuple[primesieve.count_primes(prime) - 1] -= fac

        return tuple(exponent_tuple)

    @staticmethod
    def _indigestibility(num: int) -> float:
        """Calculate _indigestibility of a number

        The implementation follows Clarence Barlows definition
        given in 'The Ratio Book' (1992).
        Arguments:
            * num -> integer, whose _indigestibility value shall be calculated

        **Example:**

        >>> JustIntonationPitch._indigestibility(1)
        0
        >>> JustIntonationPitch._indigestibility(2)
        1
        >>> JustIntonationPitch._indigestibility(3)
        2.6666666666666665
        """

        decomposed = core_utilities.factorise(num)
        return JustIntonationPitch._indigestibility_of_factorised(decomposed)

    @staticmethod
    def _indigestibility_of_factorised(decomposed):
        decomposed = collections.Counter(decomposed)
        decomposed = zip(decomposed.values(), decomposed.keys())
        summed = ((power * pow(prime - 1, 2)) / prime for power, prime in decomposed)
        return 2 * sum(summed)

    @staticmethod
    def _count_accidentals(accidentals: str) -> int:
        accidental_counter = collections.Counter({"f": 0, "s": 0})
        accidental_counter.update(accidentals)
        for accidental in accidentals:
            if accidental not in ("f", "s"):
                message = "Found unknown accidental '{}' which will be ignored".format(
                    accidental
                )
                warnings.warn(message)
        return (1 * accidental_counter["s"]) - (1 * accidental_counter["f"])

    @staticmethod
    def _get_accidentals(n_accidentals: int) -> str:
        if n_accidentals > 0:
            return "s" * n_accidentals
        else:
            return "f" * abs(n_accidentals)

    # ###################################################################### #
    #                            private methods                             #
    # ###################################################################### #

    def _translate_ratio_or_fractions_argument_to_exponent_tuple(
        self,
        ratio_or_exponent_tuple: typing.Union[
            str, fractions.Fraction, typing.Iterable[int]
        ],
    ) -> tuple[int, ...]:
        if isinstance(ratio_or_exponent_tuple, str):
            numerator, denominator = ratio_or_exponent_tuple.split("/")
            exponent_tuple = self._ratio_to_exponent_tuple(
                fractions.Fraction(int(numerator), int(denominator))
            )
        elif isinstance(ratio_or_exponent_tuple, typing.Iterable):
            exponent_tuple = tuple(ratio_or_exponent_tuple)
        elif hasattr(ratio_or_exponent_tuple, "numerator") and hasattr(
            ratio_or_exponent_tuple, "denominator"
        ):
            exponent_tuple = self._ratio_to_exponent_tuple(
                fractions.Fraction(
                    ratio_or_exponent_tuple.numerator,
                    ratio_or_exponent_tuple.denominator,
                )
            )
        else:
            message = "Unknown type '{}' of object '{}' for 'ratio_or_exponent_tuple' argument.".format(
                type(ratio_or_exponent_tuple), ratio_or_exponent_tuple
            )
            raise NotImplementedError(message)
        return exponent_tuple

    @core_utilities.add_copy_option
    def _math(  # type: ignore
        self, other: JustIntonationPitch, operation: typing.Callable
    ) -> JustIntonationPitch:
        exponent_tuple0, exponent_tuple1 = JustIntonationPitch._adjust_exponent_lengths(
            self.exponent_tuple, other.exponent_tuple
        )
        self.exponent_tuple = tuple(
            operation(x, y) for x, y in zip(exponent_tuple0, exponent_tuple1)
        )

    # ###################################################################### #
    #                            magic methods                               #
    # ###################################################################### #

    def __float__(self) -> float:
        """Return the float of a JustIntonationPitch - object.

        These are the same:
            float(myJustIntonationPitch.ratio) == float(myJustIntonationPitch).
        Note the difference that the second version might be slightly
        more performant.

        **Example:**

        >>> jip0 = JustIntonationPitch((-1, 1))
        >>> float(jip0)
        1.5
        >>> float(jip0.ratio)
        1.5
        """

        return self._exponent_tuple_to_float(self.exponent_tuple, self.prime_tuple)

    def __repr__(self) -> str:
        ratio = str(self.ratio)
        if len(ratio) == 1:
            ratio += "/1"
        return f"{type(self).__name__}('{ratio}')"

    def __abs__(self):
        if self.numerator > self.denominator:
            return copy.deepcopy(self)
        else:
            exponent_tuple = tuple(-v for v in iter(self.exponent_tuple))
            return type(self)(exponent_tuple, self.concert_pitch)

    # ###################################################################### #
    #                            properties                                  #
    # ###################################################################### #

    @property
    def exponent_tuple(self) -> tuple:
        return self._exponent_tuple

    @exponent_tuple.setter
    def exponent_tuple(
        self,
        exponent_tuple: typing.Iterable[int],
    ) -> None:
        self._exponent_tuple = self._discard_nulls(exponent_tuple)

    @property
    def prime_tuple(self) -> tuple:
        r"""Return ascending list of primes, until the highest contained Prime.

        **Example:**

        >>> jip0 = JustIntonationPitch((0, 1, 2))
        >>> jip0.exponent_tuple
        (2, 3, 5)
        >>> jip1 = JustIntonationPitch((0, -1, 0, 0, 1), 1)
        >>> jip1.exponent_tuple
        (2, 3, 5, 7, 11)
        """

        return tuple(primesieve_numpy.n_primes(len(self.exponent_tuple)))

    @property
    def occupied_primes(self) -> tuple:
        """Return all occurring prime numbers of a JustIntonationPitch object."""

        return tuple(
            prime
            for prime, exponent in zip(self.prime_tuple, self.exponent_tuple)
            if exponent != 0
        )

    @property
    def concert_pitch(self) -> music_parameters.abc.Pitch:
        return self._concert_pitch

    @concert_pitch.setter
    def concert_pitch(self, concert_pitch: ConcertPitch) -> None:
        if not isinstance(concert_pitch, music_parameters.abc.Pitch):
            concert_pitch = DirectPitch(concert_pitch)

        self._concert_pitch = concert_pitch

    @property
    def frequency(self) -> float:
        return float(self.ratio * self.concert_pitch.frequency)

    @property
    def ratio(self) -> fractions.Fraction:
        """Return the JustIntonationPitch transformed to a Ratio.

        **Example:**

        >>> jip0 = JustIntonationPitch((0, 0, 1,))
        >>> jip0.ratio
        fractions.Fraction(5, 4)
        >>> jip0 = JustIntonationPitch("3/2")
        >>> jip0.ratio
        fractions.Fraction(3, 2)
        """

        return JustIntonationPitch._exponent_tuple_to_ratio(
            self.exponent_tuple, self.prime_tuple
        )

    @property
    def numerator(self) -> int:
        """Return the numerator of a JustIntonationPitch - object.

        **Example:**

        >>> jip0 = JustIntonationPitch((0, -1,))
        >>> jip0.numerator
        1
        """

        numerator = 1
        for number, exponent in zip(self.prime_tuple, self.exponent_tuple):
            if exponent > 0:
                numerator *= pow(number, exponent)
        return numerator

    @property
    def denominator(self) -> int:
        """Return the denominator of :class:`JustIntonationPitch`.

        **Example:**

        >>> jip0 = JustIntonationPitch((0, 1,))
        >>> jip0.denominator
        1
        """

        denominator = 1
        for number, exponent in zip(self.prime_tuple, self.exponent_tuple):
            if exponent < 0:
                denominator *= pow(number, -exponent)
        return denominator

    @property
    def cents(self) -> float:
        return self.ratio_to_cents(self.ratio)

    @property
    def factorised(self) -> tuple:
        """Return factorised / decomposed version of itsef.

        **Example:**

        >>> jip0 = JustIntonationPitch((0, 0, 1,))
        >>> jip0.factorised
        (2, 2, 5)
        >>> jip1 = JustIntonationPitch("7/6")
        >>> jip1.factorised
        (2, 3, 7)
        """

        exponent_tuple = self.exponent_tuple
        prime_tuple = self.prime_tuple
        exponent_tuple_adjusted, primes_adjusted = type(self)._adjust_exponent_tuple(
            exponent_tuple, prime_tuple, 1
        )
        decomposed = (
            [p] * abs(e) for p, e in zip(primes_adjusted, exponent_tuple_adjusted)
        )
        return tuple(functools.reduce(operator.add, decomposed))

    @property
    def factorised_numerator_and_denominator(self) -> tuple:
        exponent_tuple = self.exponent_tuple
        prime_tuple = self.prime_tuple
        exponent_tuple_adjusted, prime_tuple_adjusted = type(
            self
        )._adjust_exponent_tuple(exponent_tuple, prime_tuple, 1)
        numerator_denominator: list[list[list[int]]] = [[[]], [[]]]
        for prime, exponent in zip(prime_tuple_adjusted, exponent_tuple_adjusted):
            if exponent > 0:
                idx = 0
            else:
                idx = 1
            numerator_denominator[idx].append([prime] * abs(exponent))
        return tuple(
            functools.reduce(operator.add, decomposed)
            for decomposed in numerator_denominator
        )

    @property
    def octave(self) -> int:
        ct = self.cents
        ref, exp = 1200, 0
        while ref * exp <= ct:
            exp += 1
        while ref * exp > ct:
            exp -= 1
        return exp

    @property
    def helmholtz_ellis_just_intonation_notation_commas(
        self,
    ) -> music_parameters.CommaCompound:
        """Commas of JustIntonationPitch."""

        prime_to_exponent_dict = {
            prime: exponent
            for prime, exponent in zip(self.prime_tuple, self.exponent_tuple)
            if exponent != 0 and prime not in (2, 3)
        }
        return music_parameters.CommaCompound(
            prime_to_exponent_dict,
            music_parameters.configurations.DEFAULT_PRIME_TO_COMMA_DICT,
        )

    @property
    def closest_pythagorean_interval(self) -> JustIntonationPitch:
        if len(self.helmholtz_ellis_just_intonation_notation_commas) > 0:
            closest_pythagorean_interval = self - type(self)(
                functools.reduce(
                    operator.mul, self.helmholtz_ellis_just_intonation_notation_commas
                )
            )
            closest_pythagorean_interval.normalize()
        else:
            closest_pythagorean_interval = self.normalize(mutate=False)  # type: ignore

        return closest_pythagorean_interval

    @property
    def cent_deviation_from_closest_western_pitch_class(self) -> float:
        deviation_by_helmholtz_ellis_just_intonation_notation_commas = (
            JustIntonationPitch(
                self.helmholtz_ellis_just_intonation_notation_commas.ratio
            ).cents
        )
        closest_pythagorean_interval = self.closest_pythagorean_interval
        if len(closest_pythagorean_interval.exponent_tuple) >= 2:
            pythagorean_deviation = self.closest_pythagorean_interval.exponent_tuple[
                1
            ] * (JustIntonationPitch("3/2").cents - 700)
        else:
            pythagorean_deviation = 0
        return (
            deviation_by_helmholtz_ellis_just_intonation_notation_commas
            + pythagorean_deviation
        )

    @property
    def blueprint(  # type: ignore
        self, ignore: typing.Sequence[int] = (2,)
    ) -> tuple[tuple[int, ...], ...]:
        blueprint = []
        for factorised in self.factorised_numerator_and_denominator:
            factorised = tuple(fac for fac in factorised if fac not in ignore)
            counter = collections.Counter(collections.Counter(factorised).values())
            if counter:
                maxima = max(counter.keys())
                blueprint.append(tuple(counter[idx + 1] for idx in range(maxima)))
            else:
                blueprint.append(tuple([]))
        return tuple(blueprint)

    @property
    def tonality(self) -> bool:
        """Return the tonality (bool) of a JustIntonationPitch - object.

        The tonality of a JustIntonationPitch   - may be True (otonality) if
        the exponent of the highest occurring prime number is a
        positive number and False if the exponent is a
        negative number (utonality).

        **Example:**

        >>> jip0 = JustIntonationPitch((-2. 1))
        >>> jip0.tonality
        True
        >>> jip1 = JustIntonationPitch((-2, -1))
        >>> jip1.tonality
        False
        >>> jip2 = JustIntonationPitch([])
        >>> jip2.tonality
        True
        """

        if self.exponent_tuple:
            maxima = max(self.exponent_tuple)
            minima = min(self.exponent_tuple)
            test = (
                maxima <= 0 and minima < 0,
                minima < 0
                and self.exponent_tuple.index(minima)
                > self.exponent_tuple.index(maxima),
            )
            if any(test):
                return False

        return True

    @property
    def harmonic(self) -> int:
        """Return the nth - harmonic / subharmonic the pitch may represent.

        :return: May be positive for harmonic and negative for
            subharmonic pitches. If the return - value is 0,
            the interval may occur neither between the first harmonic
            and any other pitch of the harmonic scale nor
            between the first subharmonic in the and any other
            pitch of the subharmonic scale.

        **Example:**

        >>> jip0 = JustIntonationPitch((0, 1))
        >>> jip0.ratio
        fractions.Fraction(3, 2)
        >>> jip0.harmonic
        3
        >>> jip1 = JustIntonationPitch((-1,), 2)
        >>> jip1.harmonic
        -3
        """

        ratio = self.ratio

        if ratio.denominator % 2 == 0:
            return ratio.numerator
        elif ratio.numerator % 2 == 0:
            return -ratio.denominator
        elif ratio == fractions.Fraction(1, 1):
            return 1
        else:
            return 0

    @property
    def primes_for_numerator_and_denominator(self) -> tuple:
        return tuple(
            tuple(sorted(set(core_utilities.factorise(n))))
            for n in (self.numerator, self.denominator)
        )

    @property
    def harmonicity_wilson(self) -> int:
        decomposed = self.factorised
        return int(sum(filter(lambda x: x != 2, decomposed)))

    @property
    def harmonicity_vogel(self) -> int:
        decomposed = self.factorised
        decomposed_filtered = tuple(filter(lambda x: x != 2, decomposed))
        am_2 = len(decomposed) - len(decomposed_filtered)
        return int(sum(decomposed_filtered) + am_2)

    @property
    def harmonicity_euler(self) -> int:
        """Return the 'gradus suavitatis' of euler.

        A higher number means a less consonant interval /
        a more complicated harmony.
        euler(1/1) is definied as 1.

        **Example:**

        >>> jip0 = JustIntonationPitch((0, 1,))
        >>> jip1 = JustIntonationPitch()
        >>> jip2 = JustIntonationPitch((0, 0, 1,))
        >>> jip3 = JustIntonationPitch((0, 0, -1,))
        >>> jip0.harmonicity_euler
        4
        >>> jip1.harmonicity_euler
        1
        >>> jip2.harmonicity_euler
        7
        >>> jip3.harmonicity_euler
        8
        """

        decomposed = self.factorised
        return 1 + sum(x - 1 for x in decomposed)

    @property
    def harmonicity_barlow(self) -> float:
        r"""Calculate the barlow-harmonicity of an interval.

        This implementation follows Clarence Barlows definition, given
        in 'The Ratio Book' (1992).

        A higher number means a more harmonic interval / a less
        complex harmony.

        barlow(1/1) is definied as infinite.

        **Example:**

        >>> jip0 = JustIntonationPitch((0, 1,))
        >>> jip1 = JustIntonationPitch()
        >>> jip2 = JustIntonationPitch((0, 0, 1,))
        >>> jip3 = JustIntonationPitch((0, 0, -1,))
        >>> jip0.harmonicity_barlow
        0.27272727272727276
        >>> jip1.harmonicity_barlow # 1/1 is infinite harmonic
        inf
        >>> jip2.harmonicity_barlow
        0.11904761904761904
        >>> jip3.harmonicity_barlow
        -0.10638297872340426
        """

        def sign(x):
            return (1, -1)[x < 0]

        numerator_denominator_decomposed = self.factorised_numerator_and_denominator
        indigestibility_numerator = JustIntonationPitch._indigestibility_of_factorised(
            numerator_denominator_decomposed[0]
        )
        indigestibility_denominator = (
            JustIntonationPitch._indigestibility_of_factorised(
                numerator_denominator_decomposed[1]
            )
        )
        if indigestibility_numerator == 0 and indigestibility_denominator == 0:
            return float("inf")
        return sign(indigestibility_numerator - indigestibility_denominator) / (
            indigestibility_numerator + indigestibility_denominator
        )

    @property
    def harmonicity_simplified_barlow(self) -> float:
        r"""Calculate a simplified barlow-harmonicity of an interval.

        This implementation follows Clarence Barlows definition, given
        in 'The Ratio Book' (1992), with the difference that
        only positive numbers are returned and that (1/1) is
        defined as 1 instead of infinite.

        >>> jip0 = JustIntonationPitch((0, 1,))
        >>> jip1 = JustIntonationPitch()
        >>> jip2 = JustIntonationPitch((0, 0, 1,))
        >>> jip3 = JustIntonationPitch((0, 0, -1,))
        >>> jip0.harmonicity_simplified_barlow
        0.27272727272727276
        >>> jip1.harmonicity_simplified_barlow # 1/1 is not infinite but 1
        1
        >>> jip2.harmonicity_simplified_barlow
        0.11904761904761904
        >>> jip3.harmonicity_simplified_barlow # positive return value
        0.10638297872340426
        """

        barlow = abs(self.harmonicity_barlow)
        if barlow == float("inf"):
            return 1
        return barlow

    @property
    def harmonicity_tenney(self) -> float:
        r"""Calculate Tenneys harmonic distance of an interval

        A higher number
        means a more consonant interval / a less
        complicated harmony.

        tenney(1/1) is definied as 0.

        >>> jip0 = JustIntonationPitch((0, 1,))
        >>> jip1 = JustIntonationPitch()
        >>> jip2 = JustIntonationPitch((0, 0, 1,))
        >>> jip3 = JustIntonationPitch((0, 0, -1,))
        >>> jip0.harmonicity_tenney
        2.584962500721156
        >>> jip1.harmonicity_tenney
        0.0
        >>> jip2.harmonicity_tenney
        4.321928094887363
        >>> jip3.harmonicity_tenney
        -0.10638297872340426
        """

        ratio = self.ratio
        num = ratio.numerator
        de = ratio.denominator
        return math.log(num * de, 2)

    @property
    def level(self) -> int:
        if self.prime_tuple:
            return abs(
                functools.reduce(
                    math.gcd, tuple(filter(lambda x: x != 0, self.exponent_tuple))  # type: ignore
                )
            )
        else:
            return 1

    # ###################################################################### #
    #                            public methods                              #
    # ###################################################################### #

    def get_closest_pythagorean_pitch_name(self, reference: str = "a") -> str:
        """"""

        # TODO(for future usage: type reference as typing.Literal[] instead of str)

        # TODO(split method, make it more readable)

        # TODO(Add documentation)

        diatonic_pitch_name, accidentals = reference[0], reference[1:]
        n_accidentals_in_reference = JustIntonationPitch._count_accidentals(accidentals)
        position_of_diatonic_pitch_in_cycle_of_fifths = (
            music_parameters.constants.DIATONIC_PITCH_NAME_CYCLE_OF_FIFTH_TUPLE.index(
                diatonic_pitch_name
            )
        )

        closest_pythagorean_interval = self.closest_pythagorean_interval
        try:
            n_fifths = closest_pythagorean_interval.exponent_tuple[1]
        # for 1/1
        except IndexError:
            n_fifths = 0

        # 1. Find new diatonic pitch name
        n_steps_in_diatonic_pitch_name = n_fifths % 7
        nth_diatonic_pitch = (
            position_of_diatonic_pitch_in_cycle_of_fifths
            + n_steps_in_diatonic_pitch_name
        ) % 7
        new_diatonic_pitch = (
            music_parameters.constants.DIATONIC_PITCH_NAME_CYCLE_OF_FIFTH_TUPLE[
                nth_diatonic_pitch
            ]
        )

        # 2. Find new accidentals
        n_accidentals_in_closest_pythagorean_pitch = (
            (position_of_diatonic_pitch_in_cycle_of_fifths + n_fifths) // 7
        ) + n_accidentals_in_reference
        new_accidentals = JustIntonationPitch._get_accidentals(
            n_accidentals_in_closest_pythagorean_pitch
        )

        return "".join((new_diatonic_pitch, new_accidentals))

    def get_pitch_interval(
        self, pitch_to_compare: music_parameters.abc.Pitch
    ) -> music_parameters.abc.PitchInterval:
        if isinstance(pitch_to_compare, JustIntonationPitch):
            return pitch_to_compare - self
        else:
            return super().get_pitch_interval(pitch_to_compare)

    @core_utilities.add_copy_option
    def register(self, octave: int) -> JustIntonationPitch:  # type: ignore
        """Move :class:`JustIntonationPitch` to the given octave.

        :param octave: 0 for the octave from 1/1 to 2/1, negative values for octaves
            below 1/1 and positive values for octaves above 2/1.
        :type octave: int

        **Example:**

        >>> from mutwo.music_parameters import pitches
        >>> p = pitches.JustIntonationPitch('3/2')
        >>> p.register(1)
        >>> p
        JustIntonationPitch(6/2)
        >>> p.register(-1)
        >>> p
        JustIntonationPitch(3/4)
        >>> p.register(0)
        >>> p
        JustIntonationPitch(3/2)
        """

        normalized_just_intonation_pitch = self.normalize(mutate=False)  # type: ignore
        factor = 2 ** abs(octave)
        if octave < 1:
            added = type(self)(fractions.Fraction(1, factor))
        else:
            added = type(self)(fractions.Fraction(factor, 1))
        self.exponent_tuple = (normalized_just_intonation_pitch + added).exponent_tuple  # type: ignore

    @core_utilities.add_copy_option
    def move_to_closest_register(  # type: ignore
        self, reference: JustIntonationPitch
    ) -> JustIntonationPitch:
        reference_register = reference.octave

        best = None
        for adaption in range(-1, 2):
            candidate: JustIntonationPitch = self.register(reference_register + adaption, mutate=False)  # type: ignore
            difference = abs((candidate - reference).cents)
            set_best = True
            if best and difference > best[1]:
                set_best = False

            if set_best:
                best = (candidate, difference)

        if best:
            self.exponent_tuple = best[0].exponent_tuple
        else:
            raise NotImplementedError(
                f"Couldn't find closest register of '{self}' to '{reference}'."
            )

    @core_utilities.add_copy_option
    def normalize(self, prime: int = 2) -> JustIntonationPitch:  # type: ignore
        """Normalize :class:`JustIntonationPitch`.

        :param prime: The normalization period (2 for octave,
            3 for twelfth, ...). Default to 2.
        :type prime: int

        **Example:**

        >>> from mutwo.music_parameters import pitches
        >>> p = pitches.JustIntonationPitch('12/2')
        >>> p.normalize()
        >>> p
        JustIntonationPitch(3/2)
        """
        ratio = self.ratio
        adjusted = type(self)._adjust_ratio(ratio, prime)
        self.exponent_tuple = (
            self._translate_ratio_or_fractions_argument_to_exponent_tuple(adjusted)
        )

    @core_utilities.add_copy_option
    def inverse(  # type: ignore
        self, axis: typing.Optional[JustIntonationPitch] = None
    ) -> JustIntonationPitch:
        """Inverse current pitch on given axis.

        :param axis: The :class:`JustIntonationPitch` from which the
            pitch shall be inversed.
        :type axis: JustIntonationPitch, optional

        **Example:**

        >>> from mutwo.music_parameters import pitches
        >>> p = pitches.JustIntonationPitch('3/2')
        >>> p.inverse()
        >>> p
        JustIntonationPitch(2/3)
        """

        if axis is None:
            exponent_tuple = tuple(map(lambda x: -x, self.exponent_tuple))
        else:
            distance = self - axis
            exponent_tuple = (axis - distance).exponent_tuple
        self.exponent_tuple = exponent_tuple

    @core_utilities.add_copy_option
    def add(
        self, pitch_interval: music_parameters.abc.PitchInterval
    ) -> JustIntonationPitch:
        """Add :class:`JustIntonationPitch` to current pitch.

        :param other: The :class:`JustIntonationPitch` to add to
            the current pitch.

        **Example:**

        >>> from mutwo.music_parameters import pitches
        >>> p = pitches.JustIntonationPitch('3/2')
        >>> p.add(pitches.JustIntonationPitch('3/2'))
        >>> p
        JustIntonationPitch(9/4)
        """
        if isinstance(pitch_interval, JustIntonationPitch):
            self._math(pitch_interval, operator.add)
        else:
            self.exponent_tuple = self._ratio_to_exponent_tuple(
                self.ratio * self.cents_to_ratio(pitch_interval.cents)
            )
        return self

    @core_utilities.add_copy_option
    def subtract(
        self, pitch_interval: music_parameters.abc.PitchInterval
    ) -> JustIntonationPitch:
        """Subtract :class:`JustIntonationPitch` from current pitch.

        :param other: The :class:`JustIntonationPitch` to subtract from
            the current pitch.

        **Example:**

        >>> from mutwo.music_parameters import pitches
        >>> p = pitches.JustIntonationPitch('9/4')
        >>> p.subtract(pitches.JustIntonationPitch('3/2'))
        >>> p
        JustIntonationPitch(3/2)
        """

        if isinstance(pitch_interval, JustIntonationPitch):
            self._math(pitch_interval, operator.sub)
        else:
            self.exponent_tuple = self._ratio_to_exponent_tuple(
                self.ratio / self.cents_to_ratio(pitch_interval.cents)
            )
        return self

    @core_utilities.add_copy_option
    def intersection(
        self, other: JustIntonationPitch, strict: bool = False
    ) -> JustIntonationPitch:
        """Make intersection with other :class:`JustIntonationPitch`.

        :param other: The :class:`JustIntonationPitch` to build the
            intersection with.
        :param strict: If set to ``True`` only exponent_tuple are included
            into the intersection if their value is equal. If set to
            ``False`` the method will also include exponent_tuple if both
            pitches own them on the same axis but with different values
            (the method will take the smaller exponent).
        :type strict: bool

        **Example:**

        >>> from mutwo.music_parameters import pitches
        >>> p0 = pitches.JustIntonationPitch('5/3')
        >>> p0.intersection(pitches.JustIntonationPitch('7/6'))
        >>> p0
        JustIntonationPitch(1/3)
        >>> p1 = pitches.JustIntonationPitch('9/7')
        >>> p1.intersection(pitches.JustIntonationPitch('3/2'))
        >>> p1
        JustIntonationPitch(3/1)
        >>> p2 = pitches.JustIntonationPitch('9/7')
        >>> p2.intersection(pitches.JustIntonationPitch('3/2'), strict=True)
        >>> p2
        JustIntonationPitch(1/1)
        """

        def is_negative(number: int):
            return number < 0

        def intersect_exponent_tuple(exponent_tuple: tuple[int, int]) -> int:
            intersected_exponent = 0

            if strict:
                test_for_valid_strict_mode = exponent_tuple[0] == exponent_tuple[1]
            else:
                test_for_valid_strict_mode = True

            if 0 not in exponent_tuple and test_for_valid_strict_mode:
                are_negative = (is_negative(exponent) for exponent in exponent_tuple)
                all_are_negative = all(are_negative)
                all_are_positive = all(not boolean for boolean in are_negative)

                if all_are_negative:
                    intersected_exponent = max(exponent_tuple)
                elif all_are_positive:
                    intersected_exponent = min(exponent_tuple)

            return intersected_exponent

        intersected_exponent_tuple = tuple(
            map(
                intersect_exponent_tuple, zip(self.exponent_tuple, other.exponent_tuple)
            )
        )
        self.exponent_tuple = intersected_exponent_tuple


class Partial(object):
    """Abstract representation of a harmonic spectrum partial.

    :param nth_partial: The number of the partial (starting with 1
        for the root note).
    :type nth_partial: int
    :param tonality: ``True`` for overtone and ``False`` for a (theoretical)
        undertone. Default to ``True``.
    :type tonality: bool

    **Example:**

    >>> from mutwo.music_parameters import pitches
    >>> strong_clarinet_partials = (
        pitches.Partial(1),
        pitches.Partial(3),
        pitches.Partial(5),
        pitches.Partial(7),
    )
    """

    def __init__(self, nth_partial: int, tonality: bool = True):
        self._nth_partial = nth_partial
        self._tonality = tonality

    @property
    def nth_partial(self) -> int:
        return self._nth_partial

    @property
    def tonality(self) -> int:
        return self._tonality

    def __repr__(self) -> str:
        return f"Partial({self.nth_partial}, {self.tonality})"


class CommonHarmonic(JustIntonationPitch):
    """:class:`JustIntonationPitch` which is the common harmonic between two or more other pitches.

    :param partials: Tuple which contains partial numbers.
    :type partials: tuple[Partial, ...]
    :param ratio_or_exponent_tuple: see the documentation of :class:`JustIntonationPitch`
    :type ratio_or_exponent_tuple: typing.Union[str, fractions.Fraction, typing.Iterable[int]]
    :param concert_pitch: see the documentation of :class:`JustIntonationPitch`
    :type concert_pitch: typing.Union[core_constants.Real, music_parameters.abc.Pitch]
    """

    def __init__(
        self,
        partial_tuple: tuple[Partial, ...],
        ratio_or_exponent_tuple: typing.Union[
            str, fractions.Fraction, typing.Iterable[int]
        ] = "1/1",
        concert_pitch: ConcertPitch = None,
        *args,
        **kwargs,
    ):
        super().__init__(ratio_or_exponent_tuple, concert_pitch, *args, **kwargs)
        self.partial_tuple = partial_tuple

    def __repr__(self) -> str:
        return f"CommonHarmonic({self.ratio}, {self.partial_tuple})"


class EqualDividedOctavePitch(music_parameters.abc.Pitch):
    """Pitch that is tuned to an Equal divided octave tuning system.

    :param n_pitch_classes_per_octave: how many pitch classes in each octave
        occur (for instance 12 for a chromatic system, 24 for quartertones, etc.)
    :param pitch_class: The pitch class of the new :class:`EqualDividedOctavePitch` object.
    :param octave: The octave of the new :class:`EqualDividedOctavePitch` object (where 0 is
        the middle octave, 1 is one octave higher and -1 is one octave lower).
    :param concert_pitch_pitch_class: The pitch class of the reference pitch (for
        instance 9 in a chromatic 12 tone system where `a` should be the reference
        pitch).
    :param concert_pitch_octave: The octave of the reference pitch.
    :param concert_pitch: The frequency of the reference pitch (for instance 440 for a).

    >>> from mutwo.music_parameters import pitches
    >>> # making a middle `a`
    >>> pitches.EqualDividedOctavePitch(12, 9, 4, 9, 4, 440)
    """

    def __init__(
        self,
        n_pitch_classes_per_octave: int,
        pitch_class: core_constants.Real,
        octave: int,
        concert_pitch_pitch_class: core_constants.Real,
        concert_pitch_octave: int,
        concert_pitch: ConcertPitch = None,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )
        if concert_pitch is None:
            concert_pitch = music_parameters.configurations.DEFAULT_CONCERT_PITCH

        self._n_pitch_classes_per_octave = n_pitch_classes_per_octave
        self.pitch_class = pitch_class
        self.octave = octave
        self.concert_pitch_pitch_class = concert_pitch_pitch_class
        self.concert_pitch_octave = concert_pitch_octave
        self.concert_pitch = concert_pitch  # type: ignore

    def _assert_correct_pitch_class(self, pitch_class: core_constants.Real) -> None:
        """Makes sure the respective pitch_class is within the allowed range."""

        try:
            assert all(
                (pitch_class <= self.n_pitch_classes_per_octave - 1, pitch_class >= 0)
            )
        except AssertionError:
            message = (
                "Invalid pitch class {}!. Pitch_class has to be in range (min = 0, max"
                " = {}).".format(pitch_class, self.n_pitch_classes_per_octave - 1)
            )
            raise ValueError(message)

    def _fetch_n_pitch_classes_difference(
        self,
        pitch_interval_or_n_pitch_classes_difference: typing.Union[
            music_parameters.abc.PitchInterval, core_constants.Real
        ],
    ) -> core_constants.Real:
        if isinstance(
            pitch_interval_or_n_pitch_classes_difference,
            music_parameters.abc.PitchInterval,
        ):
            return (
                pitch_interval_or_n_pitch_classes_difference.cents
                / self.n_cents_per_step
            )
        else:
            return pitch_interval_or_n_pitch_classes_difference

    @property
    def n_pitch_classes_per_octave(self) -> int:
        """Defines in how many different pitch classes one octave get divided."""
        return self._n_pitch_classes_per_octave

    @property
    def concert_pitch(self) -> music_parameters.abc.Pitch:
        """The referential concert pitch for the respective pitch object."""
        return self._concert_pitch

    @concert_pitch.setter
    def concert_pitch(self, concert_pitch: ConcertPitch) -> None:
        if not isinstance(concert_pitch, music_parameters.abc.Pitch):
            concert_pitch = DirectPitch(concert_pitch)

        self._concert_pitch = concert_pitch

    @property
    def concert_pitch_pitch_class(self) -> core_constants.Real:
        """The pitch class of the referential concert pitch."""
        return self._concert_pitch_pitch_class

    @concert_pitch_pitch_class.setter
    def concert_pitch_pitch_class(self, pitch_class: core_constants.Real) -> None:
        self._assert_correct_pitch_class(pitch_class)
        self._concert_pitch_pitch_class = pitch_class

    @property
    def pitch_class(self) -> core_constants.Real:
        """The pitch class of the pitch."""
        return self._pitch_class

    @pitch_class.setter
    def pitch_class(self, pitch_class: core_constants.Real) -> None:
        self._assert_correct_pitch_class(pitch_class)
        self._pitch_class = pitch_class

    @property
    def step_factor(self):
        """The factor with which to multiply a frequency to reach the next pitch."""
        return pow(2, 1 / self.n_pitch_classes_per_octave)

    @property
    def n_cents_per_step(self) -> float:
        """This property describes how many cents are between two adjacent pitches."""
        return self.ratio_to_cents(self.step_factor)

    @property
    def frequency(self) -> float:
        n_octaves_distant_to_concert_pitch = self.octave - self.concert_pitch_octave
        n_pitch_classes_distant_to_concert_pitch = (
            self.pitch_class - self.concert_pitch_pitch_class
        )
        distance_to_concert_pitch_in_cents = (
            n_octaves_distant_to_concert_pitch * 1200
        ) + (self.n_cents_per_step * n_pitch_classes_distant_to_concert_pitch)
        distance_to_concert_pitch_as_factor = self.cents_to_ratio(
            distance_to_concert_pitch_in_cents
        )
        return float(self.concert_pitch.frequency * distance_to_concert_pitch_as_factor)

    def __sub__(self, other: EqualDividedOctavePitch) -> core_constants.Real:
        """Calculates the interval between two ``EqualDividedOctave`` pitches."""

        try:
            assert self.n_pitch_classes_per_octave == other.n_pitch_classes_per_octave
        except AssertionError:
            message = (
                "Can't calculate the interval between to different"
                " EqualDividedOctavePitch objects with different value for"
                " 'n_pitch_classes_per_octave'."
            )
            raise ValueError(message)

        n_pitch_classes_difference = self.pitch_class - other.pitch_class
        n_octaves_difference = self.octave - other.octave
        return n_pitch_classes_difference + (
            n_octaves_difference * self.n_pitch_classes_per_octave
        )

    def _math(
        self,
        n_pitch_classes_difference: core_constants.Real,
        operator: typing.Callable[
            [core_constants.Real, core_constants.Real], core_constants.Real
        ],
    ) -> None:
        new_pitch_class = operator(self.pitch_class, n_pitch_classes_difference)
        n_octaves_difference = new_pitch_class // self.n_pitch_classes_per_octave
        new_pitch_class = new_pitch_class % self.n_pitch_classes_per_octave
        new_octave = self.octave + n_octaves_difference
        self.pitch_class = new_pitch_class
        self.octave = int(new_octave)

    @core_utilities.add_copy_option
    def add(  # type: ignore
        self,
        pitch_interval_or_n_pitch_classes_difference: typing.Union[
            music_parameters.abc.PitchInterval, core_constants.Real
        ],
    ) -> EqualDividedOctavePitch:  # type: ignore
        """Transposes the ``EqualDividedOctavePitch`` by n_pitch_classes_difference."""

        n_pitch_classes_difference = self._fetch_n_pitch_classes_difference(
            pitch_interval_or_n_pitch_classes_difference
        )
        self._math(n_pitch_classes_difference, operator.add)

    @core_utilities.add_copy_option
    def subtract(  # type: ignore
        self,
        pitch_interval_or_n_pitch_classes_difference: typing.Union[
            music_parameters.abc.PitchInterval, core_constants.Real
        ],
    ) -> EqualDividedOctavePitch:  # type: ignore
        """Transposes the ``EqualDividedOctavePitch`` by n_pitch_classes_difference."""

        n_pitch_classes_difference = self._fetch_n_pitch_classes_difference(
            pitch_interval_or_n_pitch_classes_difference
        )
        self._math(n_pitch_classes_difference, operator.sub)


# TODO(add something similar to scamps SpellingPolicy (don't hard code
# if mutwo shall write a flat or sharp)
# TODO(add translation from octave number to notated octave (4 -> ', 5 -> '', ..))


class WesternPitch(EqualDividedOctavePitch):
    """Pitch with a traditional Western nomenclature.

    :param pitch_class_or_pitch_class_name: Name or number of the pitch class of the
        new ``WesternPitch`` object. The nomenclature is English (c, d, e, f, g, a, b).
        It uses an equal divided octave system in 12 chromatic steps. Accidentals are
        indicated by (s = sharp) and (f = flat). Further microtonal accidentals are
        supported (see
        :const:`mutwo.music_parameters.configurations.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT`
        for all supported accidentals).
    :param octave: The octave of the new :class:`WesternPitch` object. Indications for the
        specific octave follow the MIDI Standard where 4 is defined as one line.

    >>> from mutwo.music_parameters import pitches
    >>> pitches.WesternPitch('cs', 4)  # c-sharp 4
    >>> pitches.WesternPitch('aqs', 2)  # a-quarter-sharp 2
    """

    def __init__(
        self,
        pitch_class_or_pitch_class_name: PitchClassOrPitchClassName = 0,
        octave: int = 4,
        concert_pitch_pitch_class: core_constants.Real = None,
        concert_pitch_octave: int = None,
        concert_pitch: ConcertPitch = None,
        *args,
        **kwargs,
    ):
        if concert_pitch_pitch_class is None:
            concert_pitch_pitch_class = (
                music_parameters.configurations.DEFAULT_CONCERT_PITCH_PITCH_CLASS_FOR_WESTERN_PITCH
            )

        if concert_pitch_octave is None:
            concert_pitch_octave = (
                music_parameters.configurations.DEFAULT_CONCERT_PITCH_OCTAVE_FOR_WESTERN_PITCH
            )

        (
            pitch_class,
            pitch_class_name,
        ) = self._translate_pitch_class_or_pitch_class_name_to_pitch_class_and_pitch_class_name(
            pitch_class_or_pitch_class_name
        )
        super().__init__(
            12,
            pitch_class,
            octave,
            concert_pitch_pitch_class,
            concert_pitch_octave,
            concert_pitch,
            *args,
            **kwargs,
        )

        self._pitch_class_name = pitch_class_name

    @staticmethod
    def _translate_pitch_class_or_pitch_class_name_to_pitch_class_and_pitch_class_name(
        pitch_class_or_pitch_class_name: PitchClassOrPitchClassName,
    ) -> tuple:
        """Helper function to initialise a WesternPitch from a number or a string.

        A number has to represent the pitch class while the name has to use
        the Western English nomenclature with the form
        DIATONICPITCHCLASSNAME-ACCIDENTAL (e.g. "cs" for c-sharp,
        "gqf" for g-quarter-flat, "b" for b)
        """
        if isinstance(pitch_class_or_pitch_class_name, numbers.Real):
            pitch_class = float(pitch_class_or_pitch_class_name)
            pitch_class_name = WesternPitch._translate_pitch_class_to_pitch_class_name(
                pitch_class_or_pitch_class_name
            )
        elif isinstance(pitch_class_or_pitch_class_name, str):
            pitch_class = WesternPitch._translate_pitch_class_name_to_pitch_class(
                pitch_class_or_pitch_class_name
            )
            pitch_class_name = pitch_class_or_pitch_class_name
        else:
            message = "Can't initalise pitch_class by '{}' of type '{}'.".format(
                pitch_class_or_pitch_class_name, type(pitch_class_or_pitch_class_name)
            )
            raise TypeError(message)

        return pitch_class, pitch_class_name

    @staticmethod
    def _translate_accidental_to_pitch_class_modifications(
        accidental: str,
    ) -> core_constants.Real:
        """Helper function to translate an accidental to its pitch class modification.

        Raises an error if the accidental hasn't been defined yet in
        mutwo.music_parameters.configurations.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT.
        """
        try:
            return music_parameters.configurations.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT[
                accidental
            ]
        except KeyError:
            message = (
                "Can't initialise WesternPitch with unknown accidental {}!".format(
                    accidental
                )
            )
            raise NotImplementedError(message)

    @staticmethod
    def _translate_pitch_class_name_to_pitch_class(
        pitch_class_name: str,
    ) -> float:
        """Helper function to translate a pitch class name to its respective number.

        +/-1 is defined as one chromatic step. Smaller floating point numbers
        represent microtonal inflections..
        """
        diatonic_pitch_class_name, accidental = (
            pitch_class_name[0],
            pitch_class_name[1:],
        )
        diatonic_pitch_class = (
            music_parameters.constants.DIATONIC_PITCH_NAME_TO_PITCH_CLASS_DICT[
                diatonic_pitch_class_name
            ]
        )
        pitch_class_modification = (
            WesternPitch._translate_accidental_to_pitch_class_modifications(accidental)
        )
        return float(diatonic_pitch_class + pitch_class_modification)

    @staticmethod
    def _translate_difference_to_closest_diatonic_pitch_to_accidental(
        difference_to_closest_diatonic_pitch: core_constants.Real,
    ) -> str:
        """Helper function to translate a number to the closest known accidental."""

        closest_pitch_class_modification: fractions.Fraction = core_utilities.find_closest_item(
            difference_to_closest_diatonic_pitch,
            tuple(
                music_parameters.configurations.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT.keys()
            ),
        )
        closest_accidental = music_parameters.configurations.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            closest_pitch_class_modification
        ]
        return closest_accidental

    @staticmethod
    def _translate_pitch_class_to_pitch_class_name(
        pitch_class: core_constants.Real,
        previous_pitch_class: typing.Optional[core_constants.Real] = None,
        previous_pitch_class_name: typing.Optional[str] = None,
    ) -> str:
        """Helper function to translate a pitch class in number to a string.

        The returned pitch class name uses a Western nomenclature of English
        diatonic note names. Accidental names are defined in
        mutwo.music_parameters.configurations.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT.
        For floating point numbers the closest accidental will be chosen.
        """

        # NOTE: it is quite difficult to estimate a new pitch class name from the previous pitch
        # class name. This doesn't work perfect. If this should work someday, you will need
        # to write something like a "Interval" class.

        if previous_pitch_class_name and previous_pitch_class and pitch_class != 0:
            previous_diatonic_pitch_class_name = previous_pitch_class_name[0]
            previous_diatonic_pitch_class_index = (
                music_parameters.constants.ASCENDING_DIATONIC_PITCH_NAME_TUPLE.index(
                    previous_diatonic_pitch_class_name
                )
            )
            previous_diatonic_pitch_class = (
                music_parameters.constants.DIATONIC_PITCH_NAME_TO_PITCH_CLASS_DICT[
                    previous_diatonic_pitch_class_name
                ]
            )
            n_pitch_classes_difference = pitch_class - previous_pitch_class
            n_diatonic_pitches_to_move = bisect.bisect_left(
                tuple(
                    music_parameters.constants.DIATONIC_PITCH_NAME_TO_PITCH_CLASS_DICT.values()
                ),
                n_pitch_classes_difference % 12,
            )
            absolute_new_diatonic_pitch_class_index = (
                previous_diatonic_pitch_class_index + n_diatonic_pitches_to_move
            )
            new_diatonic_pitch_class_index = (
                absolute_new_diatonic_pitch_class_index
                % len(music_parameters.constants.ASCENDING_DIATONIC_PITCH_NAME_TUPLE)
            )
            diatonic_pitch = (
                music_parameters.constants.ASCENDING_DIATONIC_PITCH_NAME_TUPLE[
                    new_diatonic_pitch_class_index
                ]
            )
            diatonic_pitch_class = (
                music_parameters.constants.DIATONIC_PITCH_NAME_TO_PITCH_CLASS_DICT[
                    diatonic_pitch
                ]
            )

            n_pitch_classes_moved_between_diatonic_pitches = (
                diatonic_pitch_class - previous_diatonic_pitch_class
            )
            accidental_adjustments = (
                n_pitch_classes_difference
                - n_pitch_classes_moved_between_diatonic_pitches
            )

            previous_accidental_adjustments = (
                previous_pitch_class - previous_diatonic_pitch_class
            )
            accidental_adjustments += previous_accidental_adjustments

            n_octaves_difference = absolute_new_diatonic_pitch_class_index // len(
                music_parameters.constants.ASCENDING_DIATONIC_PITCH_NAME_TUPLE
            )

        else:
            diatonic_pitch_classes = tuple(
                music_parameters.constants.DIATONIC_PITCH_NAME_TO_PITCH_CLASS_DICT.values()
            )
            closest_diatonic_pitch_class_index = core_utilities.find_closest_index(
                pitch_class, diatonic_pitch_classes
            )
            diatonic_pitch_class = diatonic_pitch_classes[
                closest_diatonic_pitch_class_index
            ]
            diatonic_pitch = tuple(
                music_parameters.constants.DIATONIC_PITCH_NAME_TO_PITCH_CLASS_DICT.keys()
            )[closest_diatonic_pitch_class_index]

            accidental_adjustments = pitch_class - diatonic_pitch_class

        accidental = (
            WesternPitch._translate_difference_to_closest_diatonic_pitch_to_accidental(
                accidental_adjustments
            )
        )

        pitch_class_name = f"{diatonic_pitch}{accidental}"
        return pitch_class_name

    @classmethod
    def from_midi_pitch_number(cls, midi_pitch_number: float) -> WesternPitch:
        pitch_number = midi_pitch_number - 12
        pitch_class_number = pitch_number % 12
        octave_number = pitch_number // 12
        return cls(pitch_class_number, octave=octave_number)

    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, self.name)

    def _math(
        self,
        n_pitch_classes_difference: core_constants.Real,
        operator: typing.Callable[
            [core_constants.Real, core_constants.Real], core_constants.Real
        ],
    ) -> None:
        new_pitch_class = operator(self.pitch_class, n_pitch_classes_difference)
        n_octaves_difference = new_pitch_class // self.n_pitch_classes_per_octave
        new_pitch_class = new_pitch_class % self.n_pitch_classes_per_octave
        new_octave = self.octave + n_octaves_difference
        self.pitch_class = new_pitch_class
        self.octave = int(new_octave)

    @property
    def name(self) -> str:
        """The name of the pitch in Western nomenclature."""

        return "{}{}".format(self._pitch_class_name, self.octave)

    @property
    def pitch_class_name(self) -> str:
        """The name of the pitch class in Western nomenclature.

        Mutwo uses the English nomenclature for pitch class names:
            (c, d, e, f, g, a, b)
        """

        return self._pitch_class_name

    @pitch_class_name.setter
    def pitch_class_name(self, pitch_class_name: str):
        self._pitch_class = self._translate_pitch_class_name_to_pitch_class(
            pitch_class_name
        )
        self._pitch_class_name = pitch_class_name

    @EqualDividedOctavePitch.pitch_class.setter  # type: ignore
    def pitch_class(self, pitch_class: core_constants.Real):
        if hasattr(self, "_pitch_class_name"):
            previous_pitch_class = self._pitch_class
            previous_pitch_class_name = self._pitch_class_name
        else:
            previous_pitch_class = None
            previous_pitch_class_name = None

        self._pitch_class_name = self._translate_pitch_class_to_pitch_class_name(
            pitch_class, previous_pitch_class, previous_pitch_class_name
        )
        self._pitch_class = pitch_class
