from typing import Optional, Any, Dict, Union, List

from pyrasgo.api.connection import Connection
from pyrasgo import schemas


class Accelerator(Connection):
    """
    Primitive Class representing a Rasgo Accelerator
    """
    def __init__(
            self,
            api_accelerator: Union[schemas.Accelerator, schemas.AcceleratorBulk],
            **kwargs
    ):
        super().__init__(**kwargs)
        self._api_accelerator = api_accelerator

    def __repr__(self) -> str:
        """
        Get string representation of this Accelerator
        """
        return f"Accelerator(id={self.id}, " \
               f"name={self.name}, " \
               f"description={self.description})"

    @property
    def id(self) -> int:
        """
        Return the Id for this Accelerator
        """
        return self._api_accelerator.id

    @property
    def template(self) -> str:
        """
        Return the template for this Accelerator
        """
        # If the api object came from the bulk call,  it won't
        # have this property set. So make an api call to set it
        if not hasattr(self._api_accelerator, 'template'):
            resp = self._get(
                f"/accelerators/{self.id}", api_version=2
            ).json()
            self._api_accelerator = schemas.Accelerator(**resp)
        return self._api_accelerator.template

    @property
    def description(self) -> Optional[str]:
        """
        Return the description of this Accelerator
        """
        return self._api_accelerator.description.description

    @property
    def name(self) -> str:
        """
        Return the name of this Accelerator
        """
        return self._api_accelerator.description.name

    @property
    def arguments(self) -> List[schemas.AcceleratorArgument]:
        """
        Return the name of this Accelerator
        """
        return self._api_accelerator.description.arguments

    def apply(self, name: str, args: Dict[str, Any]) -> None:
        """
        Applies the given set of arguments to the Accelerator to generate
        a new DRAFT Dataset in the UI, with the given name.

        Args:
            name: Name of the created dataset
            args: Arguments of the Accelerator
        """
        from pyrasgo.api import Create
        Create().dataset_from_accelerator(
            accelerator_id=self.id,
            name=name,
            accelerator_args=args
        )
