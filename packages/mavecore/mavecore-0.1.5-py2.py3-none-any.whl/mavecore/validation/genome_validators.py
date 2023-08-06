# TODO Django dependent, Django forms, whole file needs to be refactored
"""
Validator functions for the fields of the following classes:
    WildTypeSequence
    ReferenceGenome
    TargetGene
    ReferenceMap
    GenomicInterval

Most validation should validate one specific field, unless fields need
to be validated against each other.
"""
from fqfa.validator.validator import dna_bases_validator, amino_acids_validator
from mavecore.validation.exceptions import ValidationError

from mavecore.validation import constants

from mavecore.validation.utilities import is_null


# min_start_validator = MinValueValidator(
#    1, message=_("Start coordinate must be a positive integer.")
# )
# min_end_validator = MinValueValidator(
#    1, message=_("End coordinate must be a positive integer.")
# )


class WildTypeSequence:
    """
    Basic model specifying a wild-type sequence.

    Parameters
    ----------
    sequence : `models.CharField`
        The wild type DNA sequence that is related to the `target`. Will
        be converted to upper-case upon instantiation.

    sequence_type : `models.CharField`
        Protein sequence (amino acids) or DNA (nucleotides)
    """

    class SequenceType:
        """ """

        DNA = "dna"
        PROTEIN = "protein"
        INFER = "infer"

        @classmethod
        def detect_sequence_type(cls, sequence):
            # TODO
            # confirm sequence parameter type
            """
            This function determines if the sequence is a DNA or protein sequence and
            returns "dna" if it is DNA or "protein" if it is protein. An error is raised
            if it is neither.

            Parameters
            __________
            sequence : str

            Returns
            _______
            str
                "dna" or "protein" depending on if the sequence is a DNA or protein sequence.

            Raises
            ______
            ValueError
                If sequence parameter is not protein or DNA.
            """
            if sequence_is_dna(sequence):
                return cls.DNA
            elif sequence_is_protein(sequence):
                return cls.PROTEIN
            else:
                raise ValueError(
                    f"Unknown sequence '{sequence}'. It is not protein or DNA."
                )

        @classmethod
        def is_protein(cls, value):
            """

            Parameters
            __________
            value :

            Returns
            _______

            """
            return value == cls.PROTEIN

        @classmethod
        def is_dna(cls, value):
            """

            Parameters
            __________
            value :

            Returns
            _______

            """
            return value == cls.DNA

        @classmethod
        def choices(cls):
            """

            Returns
            _______
            """
            return [(cls.INFER, "Infer"), (cls.DNA, "DNA"), (cls.PROTEIN, "Protein")]

    class Meta:
        """ """

        verbose_name = "Reference sequence"
        verbose_name_plural = "Reference sequences"

    def __str__(self):
        """

        Returns
        _______

        """
        return self.get_sequence()

    # sequence = models.TextField(
    #    default=None,
    #    blank=False,
    #    null=False,
    #    verbose_name="Reference sequence",
    #    validation=[validate_wildtype_sequence],
    # )
    # sequence_type = models.CharField(
    #    blank=True,
    #    null=False,
    #    default=SequenceType.INFER,
    #    verbose_name="Reference sequence type",
    #    max_length=32,
    #    choices=SequenceType.choices(),
    # )

    @property
    def is_dna(self):
        """

        Returns
        _______

        """
        return self.__class__.SequenceType.is_dna(self.sequence_type)

    @property
    def is_protein(self):
        """

        Returns
        _______

        """
        return self.__class__.SequenceType.is_protein(self.sequence_type)

    def save(self, *args, **kwargs):
        """

        Parameters
        __________
        args :
        kwargs :

        Returns
        _______

        """
        if self.sequence is not None:
            self.sequence = self.sequence.upper()
            self.sequence_type = (
                (self.__class__.SequenceType.detect_sequence_type(self.sequence))
                if self.__class__.SequenceType.INFER
                else self.sequence_type
            )

        return super().save(*args, **kwargs)

    def get_sequence(self):
        """

        Returns
        _______

        """
        return self.sequence.upper()

    def is_attached(self):
        """

        Returns
        _______

        """
        return getattr(self, "target", None) is not None


# GenomicInterval
# ------------------------------------------------------------------------- #
def validate_interval_start_lteq_end(start, end):
    """
    This function validates whether or not an interval's starting coordinate is less than
    or equal to that interval's ending coordinate.

    Parameters
    __________
    start : int
        The interval's starting coordinate.
    end : int
        The interval's ending coordinate.

    Returns
    _______
    None
        If start is NoneType or end is NoneType.

    Raises
    ______
    ValidationError
        If an interval's starting coordinate is greater than the ending coordinate.
    """
    # Intervals may be underspecified, but will be ignored so skip validation.
    if start is None or end is None:
        return
    if start > end:
        raise ValidationError(
            (
                "An interval's starting coordinate cannot be greater than the "
                "ending coordinate."
            )
        )


def validate_strand(value):
    # TODO
    # find the type of value
    """
    This function validates a GenomicInterval strand and raises an error if the strand is invalid.

    Parameters
    __________
    value :
        The Genomic Interval strand to be validated.

    Raises
    ______
    ValidationError
        If GenomicInterval strand is not positive or negative.
    """
    if value not in ("+", "-"):
        raise ValidationError("GenomicInterval strand must be either '+' or '-'")


def validate_chromosome(value):
    # TODO
    # add description and type for value parameter
    """

    Parameters
    __________
    value :

    Returns
    _______
    None
        If value is NoneType.

    Raises
    ______
    ValidationError
        If chromosome identifier is null.
    """
    # Intervals may be underspecified, but will be ignored so skip validation.
    if value is None:
        return
    if is_null(value):
        raise ValidationError("Chromosome identifier must not be null.")


def validate_unique_intervals(intervals):
    # TODO
    # add description and interval parameter type plus description
    """

    Parameters
    __________
    intervals :

    Raises
    ______
    ValidationError
        If the same interval was specified twice.
    """
    for interval1 in intervals:
        for interval2 in intervals:
            if (
                (interval1.pk is not None)
                and (interval2.pk is not None)
                and (interval1.pk == interval2.pk)
            ):
                continue
            elif interval1 is interval2:
                continue
            elif interval1.equals(interval2):
                raise ValidationError("You can not specify the same interval twice.")


# WildTypeSequence
# ------------------------------------------------------------------------- #
def validate_wildtype_sequence(seq, as_type="any"):
    # TODO
    # add description to as_type parameter
    """
    This function checks whether or not seq is a wildtype sequence.

    Parameters
    __________
    seq : str
        The sequence being validated.
    as_type : str
        (default = "any")

    Raises
    ______
    ValidationError
        If seq is not a valid wild type sequence.
    ValidationError
        If seq is not a valid DNA or protein reference sequence.
    """
    # from .models import WildTypeSequence

    # Explicitly check for these cases as they are also valid AA sequences.
    if is_null(seq):
        raise ValidationError(
            "'%(seq)s' is not a valid wild type sequence."  # , params={"seq": seq}
        )

    seq = seq.upper()
    is_dna = dna_bases_validator(seq) is not None
    is_aa = amino_acids_validator(seq) is not None

    if as_type == WildTypeSequence.SequenceType.DNA and not is_dna:
        raise ValidationError(
            "'%(seq)s' is not a valid DNA reference sequence."  # ,
            # params={"seq": seq},
        )
    elif as_type == WildTypeSequence.SequenceType.PROTEIN and not is_aa:
        raise ValidationError(
            "'%(seq)s' is not a valid protein reference sequence."  # ,
            # params={"seq": seq},
        )
    elif (as_type == "any" or WildTypeSequence.SequenceType.INFER) and not (
        is_dna or is_aa
    ):
        raise ValidationError(
            "'%(seq)s' is not a valid DNA or protein reference sequence."  # ,
            # params={"seq": seq},
        )


def sequence_is_dna(seq):
    """
    This function checks if seq is a DNA sequence.

    Parameters
    __________
    seq : str
        The sequence to be validated.

    Returns
    _______
    bool
        True if the dna_bases_validator returns a match object.
    """
    # Explicitly check for these cases as they are also valid AA sequences.
    if is_null(seq):
        return False
    seq = seq.upper()
    return dna_bases_validator(seq) is not None


def sequence_is_protein(seq):
    """
    This function check if seq is a protein sequence.

    Parameters
    __________
    seq : str
        The sequence being validated.

    Returns
    _______
    bool
        True if seq is not null, is a DNA sequence or amino_acids_validator returns a match object.
    """
    # Explicitly check for these cases as they are also valid AA sequences.
    if is_null(seq):
        return False
    seq = seq.upper()
    if dna_bases_validator(seq) is not None:
        return False  # Very likely a DNA sequence if only ATG
    return amino_acids_validator(seq) is not None


# ReferenceGenome
# ------------------------------------------------------------------------- #
def validate_organism_name(organism_name):
    # TODO
    # confirm organism_name type
    """
    This function validates the organism name by checking that the name is not null.

    Parameters
    __________
    organism_name : str
        The organism name to be validated.

    Raises
    ______
    ValidationError
        If the organism name is null.
    """
    if is_null(organism_name):
        raise ValidationError("Species name must not be null.")


def validate_reference_genome_has_one_external_identifier(referencegenome):
    # TODO
    # revise description, make sure it is accurate
    # anything greater than 0 will return True, so should it be == 1 or > 0?
    # determine what type referencegenome is
    """
    This function validates whether or not the reference genome has one external identifier.
    An error is raised if

    Parameters
    __________
    referencegenome :

    Raises
    ______
    ValidationError
        If
    """
    if not referencegenome.genome_id:
        raise ValidationError(
            "Only one external identifier can be specified for a reference" "genome."
        )


def validate_genome_short_name(value):
    # TODO
    # confirm the type of the value parameter
    """
    This function validates the genome short name and raises an error if the value is null.

    Parameters
    __________
    value : str
        The genome short name to be validated.

    Raises
    ______
    ValidationError
        If the genome short name is null.
    """
    if is_null(value):
        raise ValidationError("Genome short name must not be null.")


# ReferenceMap
# ------------------------------------------------------------------------- #
def validate_map_has_unique_reference_genome(annotations):
    # TODO
    # check the type of annotations
    # add description to annotations parameter
    """
    This function validates whether or not each map in annotations has a
    unique reference genome and raises an error if this is not the case.

    Parameters
    __________
    annotations :

    Raises
    ______
    ValidationError
        If each reference map does not specify a different reference genome.
    """
    genomes = set([str(a.get_reference_genome_name()).lower() for a in annotations])
    if len(genomes) < len(annotations):
        raise ValidationError(
            "Each reference map must specify a different reference genome."
        )


def validate_map_has_at_least_one_interval(reference_map):
    """
    This function validates that a reference map has at least one interval and raises an error
    if this is not the case.

    Parameters
    __________
    reference_map :
        Reference map.

    Raises
    ______
    ValidationError
        If the reference_map does not have at least one interval.
    """
    if not reference_map.get_intervals().count():
        raise ValidationError(
            "You must specify at least one interval for each reference map."
        )


def validate_at_least_one_map(reference_maps):
    """
    This function validates whether a target has at least one reference map specified
    and raises an error if it does not.

    Parameters
    __________
    reference_maps :


    Raises
    ______
    ValidationError
        If the target does not have at least one reference map specified.
    """
    if not len(reference_maps):
        raise ValidationError(
            "A target must have at least one reference map specified."
        )


def validate_one_primary_map(reference_maps):
    """
    This function validates the existence of one primary reference map and raises an error
    if it does not exist.

    Parameters
    __________
    reference_maps :

    Raises
    ______
    ValidationError
        If target has less than or more than one primary reference map.
    """
    primary_count = sum(a.is_primary_reference_map() for a in reference_maps)
    if primary_count > 1 or primary_count < 1:
        raise ValidationError("A target must have one primary reference map.")


# TargetGene
# ------------------------------------------------------------------------- #
def validate_gene_name(gene_name):
    # TODO
    # confirm gene_name type
    """
    This function checks to see if a gene name is null and raises and error if it is.

    Parameters
    __________
    gene_name : str
        The gene name.

    Raises
    ______
    ValidationError
        If gene name (value parameter) is null.
    """
    if is_null(gene_name):
        raise ValidationError("Gene name must not be null.")
