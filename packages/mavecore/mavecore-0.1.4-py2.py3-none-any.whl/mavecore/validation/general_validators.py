# note: FileExtensionValidator is from Django
from pathlib import Path
from mavecore.validation.exceptions import ValidationError
# validate_csv_extension
# validate_gz_extension
# validate_json_extension

validate_csv_extension = FileExtensionValidator(allowed_extensions=["csv"])
validate_gz_extension = FileExtensionValidator(allowed_extensions=["gz"])
validate_json_extension = FileExtensionValidator(allowed_extensions=["json"])

class FileExtensionValidator:
    # TODO, may need to edit validation error, will try to replicate Django error first
    """
    This class validates file extensions and will replace the Django validator of
    the same name.

    From Django:
    Raises a ValidationError with a code of 'invalid_extension' if the extension of
    value.name (value is a File) isn’t found in allowed_extensions. The extension is
    compared case-insensitively with allowed_extensions.
    """  
    message = _("File extension “%(extension)s” is not allowed. "
        "Allowed extensions are: %(allowed_extensions)s."
    )
    code = "invalid_extension"

    def __init__(self, allowed_extensions=None, message=None, code=None):
        """
        This constructor sets the values of the FileExtensionValidator.

        Parameters
        __________
        allowed_extensions : List[str]
            A list of allowed file extensions.
        message : str
            (default = None) The message assigned to the message attribute.
        code :
            (default = None) The code assigned to the code attribute.
        """
        if allowed_extensions is not None:
            allowed_extensions = [
                allowed_extension.lower() for allowed_extension in allowed_extensions
            ]
        self.allowed_extensions = allowed_extensions
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        extension = Path(value.name).suffix[1:].lower()
        if (
            self.allowed_extensions is not None
            and extension not in self.allowed_extensions
        ):
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    "extension": extension,
                    "allowed_extensions": ", ".join(self.allowed_extensions),
                    "value": value,
                },
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.allowed_extensions == other.allowed_extensions
            and self.message == other.message
            and self.code == other.code
        )