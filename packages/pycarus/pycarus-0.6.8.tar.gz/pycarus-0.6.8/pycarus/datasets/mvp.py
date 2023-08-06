from pathlib import Path
from typing import Callable, List, Tuple

from torch import Tensor
from torch.utils.data import Dataset

from pycarus.geometry.pcd import read_pcd
from pycarus.transforms.var import Compose

T_ITEM = Tuple[str, str, Tensor, Tensor]


class Mvp(Dataset):
    """Class implementing the MVP dataset as proposed in:

    Pan, L., Chen, X., Cai, Z., Zhang, J., Zhao, H., Yi, S., & Liu, Z. (2021).
    Variational Relational Point Completion Network.
    In Proceedings of the IEEE/CVF Conference on Computer Vision
        and Pattern Recognition (pp. 8524-8533).
    """

    def __init__(
        self,
        root: Path,
        split: str,
        num_points_gt: int,
        transforms_complete: List[Callable] = [],
        transforms_incomplete: List[Callable] = [],
        transforms_all: List[Callable] = [],
    ) -> None:
        """Create an instance of MVP dataset.

        Args:
            root: The path to the folder containing the dataset.
            split: The name of the split to load. Allowed values: train, val, test.
            num_points: The resolution for GT clouds. Allowed values: 2048, 4096, 8192, 16384.
            transforms_complete: The transform to apply to the complete pcds. Defaults to [].
            transforms_incomplete: The transform to apply to the incomplete pcds. Defaults to [].
            transforms_all: The transform to apply to both the complete
                            and the incomplete pcds. Defaults to [].
        """
        super().__init__()

        assert split in ["train", "val", "test"]
        assert num_points_gt in [2048, 4096, 8192, 16384]

        self.root = root

        self.categories: List[str] = []
        self.incomplete_paths: List[Path] = []
        self.complete_paths: List[Path] = []

        for c in sorted([s.name for s in self.root.iterdir()]):
            category_dir = self.root / c / split
            incomplete_dir = category_dir / "incomplete"
            complete_dir = category_dir / f"complete_{num_points_gt}"

            inc_paths = sorted(list(incomplete_dir.glob("*.ply")))
            self.incomplete_paths.extend(inc_paths)

            compl_paths = sorted(list(complete_dir.glob("*.ply")))
            self.complete_paths.extend(compl_paths)

            self.categories.extend([category_dir.name] * len(inc_paths))

        self.transform_complete = Compose(transforms_complete)
        self.transform_incomplete = Compose(transforms_incomplete)
        self.transform_all = Compose(transforms_all)

    def __len__(self) -> int:
        """Return the number of items in the dataset.

        Returns:
            The number of items in the dataset.
        """
        return len(self.incomplete_paths)

    def __getitem__(self, index: int) -> T_ITEM:
        """Return the item at the given index.

        Args:
            index: The index of the required item.

        Returns:
            - The category of the item.
            - The name of the item.
            - A tensor with the incomplete point cloud with shape (NUM_POINTS, 3).
            - A tensor with the complete point cloud with shape (NUM_POINTS, 3).
        """
        category = self.categories[index]
        name = self.incomplete_paths[index].stem
        incomplete = read_pcd(self.incomplete_paths[index])
        complete = read_pcd(self.complete_paths[index])

        incomplete = self.transform_all(self.transform_incomplete(incomplete))
        complete = self.transform_all(self.transform_complete(complete))

        return category, name, incomplete, complete
