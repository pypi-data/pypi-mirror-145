from unittest import TestCase

from mavecore.validation.genome_validators import WildTypeSequence

# from mavetools.validation.genome_factories import (
#    ReferenceMapFactory,
#    ReferenceGenomeFactory,
#    GenomicIntervalFactory,
# )


from mavecore.validation.genome_validators import (
    validate_wildtype_sequence,
    validate_gene_name,
    validate_genome_short_name,
    validate_organism_name,
    sequence_is_protein,
    sequence_is_dna,
)
from mavecore.validation.exceptions import ValidationError

from mavecore.validation.constants import null_values_list


class TestWildTypeSequenceValidators(TestCase):
    """
    Tests validation associated with :class:`WildTypeSequence`. Tests:

        - validate_wildtype_sequence
    """

    def test_ve_not_a_sequence_of_nucleotides_or_aa(self):
        with self.assertRaises(ValidationError):
            validate_wildtype_sequence("2823d")

    def test_ve_null(self):
        for v in null_values_list:
            with self.assertRaises(ValidationError):
                validate_wildtype_sequence(v)

    def test_passes_lowercase_nucleotides(self):
        validate_wildtype_sequence("atcg")

    def test_passes_uppercase_nucleotides(self):
        validate_wildtype_sequence("ATCG")

    def test_passes_lowercase_aa(self):
        validate_wildtype_sequence("MDLSALRVEE")

    def test_passes_uppercase_aa(self):
        validate_wildtype_sequence("MDLSALRVEE".lower())

    def test_pass_validate_dna_sequence(self):
        validate_wildtype_sequence("ATCG", as_type=WildTypeSequence.SequenceType.DNA)

    def test_pass_validate_protein_sequence(self):
        validate_wildtype_sequence(
            "MDLS", as_type=WildTypeSequence.SequenceType.PROTEIN
        )

    def test_fails_validate_as_type_dna_but_seq_is_protein(self):
        validate_wildtype_sequence(
            "MDLS", as_type=WildTypeSequence.SequenceType.PROTEIN
        )
        with self.assertRaises(ValidationError):
            validate_wildtype_sequence(
                "MDLS", as_type=WildTypeSequence.SequenceType.DNA
            )

    def test_fail_validate_as_type_protein_when_sequence_is_invalid(self):
        with self.assertRaises(ValidationError):
            validate_wildtype_sequence(
                "ABC", as_type=WildTypeSequence.SequenceType.PROTEIN
            )


class TestIsProteinSequence(TestCase):
    def test_false_null(self):
        for v in null_values_list:
            self.assertFalse(sequence_is_protein(v))

    def test_false_dna_sequence(self):
        # Favor dna sequences when only ATCG
        self.assertFalse(sequence_is_protein("ATCG"))
        self.assertFalse(sequence_is_protein("atc"))

    def test_true_aa_sequence(self):
        self.assertTrue(sequence_is_protein("MDLSALRVEEATC"))
        self.assertTrue(sequence_is_protein("MDLSALRVEEATC".lower()))


class TestIsDNASequence(TestCase):
    def test_false_null(self):
        for v in null_values_list:
            self.assertFalse(sequence_is_protein(v))

    def test_true_dna_sequence(self):
        self.assertTrue(sequence_is_dna("ATCG"))
        self.assertTrue(sequence_is_dna("atc"))

    def test_false_aa_sequence(self):
        self.assertFalse(sequence_is_dna("MDLSALRVEEATC"))
        self.assertFalse(sequence_is_dna("MDLSALRVEEATC".lower()))


class TestReferenceGenomeValidators(TestCase):
    """
    Tests validation associated with :class:`ReferenceGenome`:

        - validate_reference_genome_has_one_external_identifier
        - validate_organism_name
        - validate_genome_short_name
    """

    def test_ve_null_organism_name(self):
        for v in null_values_list:
            with self.assertRaises(ValidationError):
                validate_organism_name(v)

    def test_ve_null_genome_short_name(self):
        for v in null_values_list:
            with self.assertRaises(ValidationError):
                validate_genome_short_name(v)


class TestTargetGeneValidators(TestCase):
    """
    Tests validation asscociated with :class:`TargetGene`:

        - validate_gene_name
        - validate_target_has_one_primary_reference_map
    """

    def test_ve_null_gene_name(self):
        for v in null_values_list:
            with self.assertRaises(ValidationError):
                validate_gene_name(v)
