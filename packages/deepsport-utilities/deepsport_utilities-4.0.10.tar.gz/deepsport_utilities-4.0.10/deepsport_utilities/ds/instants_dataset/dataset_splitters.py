import random
import dataclasses
from deepsport_utilities.utils import split_equally, Subset, SubsetType

@dataclasses.dataclass
class DeepSportDatasetSplitter: # pylint: disable=too-few-public-methods
    validation_pc: int = 15
    additional_keys_usage: str = "skip"
    folds: str = "ABCDE"
    split = {
        "A": ['KS-FR-CAEN', 'KS-FR-LIMOGES', 'KS-FR-ROANNE'],
        "B": ['KS-FR-NANTES', 'KS-FR-BLOIS', 'KS-FR-FOS'],
        "C": ['KS-FR-LEMANS', 'KS-FR-MONACO', 'KS-FR-STRASBOURG'],
        "D": ['KS-FR-GRAVELINES', 'KS-FR-STCHAMOND', 'KS-FR-POITIERS'],
        "E": ['KS-FR-NANCY', 'KS-FR-BOURGEB', 'KS-FR-VICHY'],
    }
    @staticmethod
    def count_keys_per_arena_label(keys):
        """returns a dict of (arena_label: number of keys of that arena)"""
        bins = {}
        for key in keys:
            bins[key.arena_label] = bins.get(key.arena_label, 0) + 1
        return bins
    @staticmethod
    def count_keys_per_game_id(keys):
        """returns a dict of (game_id: number of keys of that game)"""
        bins = {}
        for key in keys:
            bins[key.game_id] = bins.get(key.game_id, 0) + 1
        return bins
    def __call__(self, dataset, fold=0):
        keys = list(dataset.keys.all())
        assert 0 <= fold <= len(self.folds)-1, "Invalid fold index"

        testing_fold = self.folds[fold]
        testing_keys = [k for k in keys if k.arena_label in self.split[testing_fold]]

        remaining_arena_labels = [label for f in self.folds.replace(testing_fold, "") for label in self.split[f]]
        remaining_keys = [k for k in keys if k.arena_label in remaining_arena_labels]

        # Backup random seed
        random_state = random.getstate()
        random.seed(fold)

        validation_keys = random.sample(remaining_keys, len(remaining_keys)*self.validation_pc//100)
        training_keys = [k for k in remaining_keys if k not in validation_keys]

        additional_keys = [k for k in keys if k not in training_keys+validation_keys+testing_keys]

        if additional_keys:
            if self.additional_keys_usage == "testing":
                testing_keys += additional_keys
            elif self.additional_keys_usage == "training":
                training_keys += additional_keys
            elif self.additional_keys_usage == "validation":
                validation_keys += additional_keys
            elif self.additional_keys_usage in ["none", "skip"]:
                pass
            else:
                raise ValueError("They are additional arena labels that I don't know what to do with. Please tell me the 'additional_keys_usage' argument")

        # Restore random seed
        random.setstate(random_state)

        return [
            Subset(name="training", subset_type=SubsetType.TRAIN, keys=training_keys, dataset=dataset),
            Subset(name="validation", subset_type=SubsetType.EVAL, keys=validation_keys, dataset=dataset, repetitions=1),
            Subset(name="testing", subset_type=SubsetType.EVAL, keys=testing_keys, dataset=dataset, repetitions=1),
        ]

@dataclasses.dataclass
class ArenaLabelFoldsDatasetSplitter(DeepSportDatasetSplitter):
    folds: str = "ABCDE"
    test_fold: str = "A"
    def __post_init__(self):
        assert self.test_fold in self.split, f"Requested test_fold ({self.test_fold}) doesn't exist. Choose among {list(self.split)}."
        assert all([fold in self.split for fold in self.folds]), f"One of the selected folds ({self.folds}) don't exist. Choose among {list(self.split)}."
        self.folds = self.folds.replace(self.test_fold, "") # make sure test_fold is not used at training or validation
    def __call__(self, dataset, fold=0):
        assert 0 <= fold < len(self.folds)
        keys = list(dataset.keys.all())

        testing_arena_labels = self.split[self.test_fold]
        testing_keys = [k for k in keys if k.arena_label in testing_arena_labels]

        validation_arena_labels = self.split[self.folds[fold]]
        validation_keys = [k for k in keys if k.arena_label in validation_arena_labels]

        training_arena_labels = [arena_label for i in range(len(self.folds)) if i != fold for arena_label in self.split[self.folds[i]]]
        training_keys = [k for k in keys if k.arena_label in training_arena_labels]

        return [
            Subset(name="training", subset_type=SubsetType.TRAIN, keys=training_keys, dataset=dataset),
            Subset(name="validation", subset_type=SubsetType.EVAL, keys=validation_keys, dataset=dataset),
            Subset(name="testing", subset_type=SubsetType.EVAL, keys=testing_keys, dataset=dataset),
        ]

@dataclasses.dataclass
class OfficialFoldsDatasetSplitter(DeepSportDatasetSplitter):
    folds: str = "ABCDE"
    eval_folds: str = "DE"
    def __post_init__(self):
        assert all([fold in self.split for fold in self.eval_folds]), f"Requested evaluation folds ({self.eval_folds}) doesn't exist. Choose among {list(self.split)}."
        assert all([fold in self.split for fold in self.folds]), f"One of the selected folds ({self.folds}) don't exist. Choose among {list(self.split)}."
    def __call__(self, dataset, fold=0):
        dataset_keys = list(dataset.keys.all())
        subset_type = lambda n: SubsetType.EVAL if n in self.eval_folds else SubsetType.TRAIN
        keys = lambda n: [k for k in dataset_keys if k.arena_label in self.split[n]]
        raise NotImplementedError("Subsets order should be checked")
        return [
            Subset(name=n, subset_type=subset_type(n), keys=keys(n), dataset=dataset) for n in self.folds
        ]

class KFoldsArenaLabelsTestingDatasetSplitter(DeepSportDatasetSplitter):
    def __init__(self, fold_count=8, validation_pc=15):
        self.fold_count = fold_count
        self.validation_pc = validation_pc

    def __call__(self, dataset, fold=0):
        keys = list(dataset.keys.all())
        assert fold >= 0 and fold < self.fold_count

        keys_dict = self.count_keys_per_arena_label(keys)
        keys_lists = split_equally(keys_dict, self.fold_count)

        testing_keys = [k for k in keys if k.arena_label in keys_lists[fold]]
        remaining_keys = [k for k in keys if k not in testing_keys]

        # Backup random seed
        random_state = random.getstate()
        random.seed(fold)

        validation_keys = random.sample(remaining_keys, len(keys)*self.validation_pc//100)

        # Restore random seed
        random.setstate(random_state)

        training_keys = [k for k in remaining_keys if k not in validation_keys]

        return [
            Subset(name="training", subset_type=SubsetType.TRAIN, keys=training_keys, dataset=dataset),
            Subset(name="validation", subset_type=SubsetType.EVAL, keys=validation_keys, dataset=dataset, repetitions=5),
            Subset(name="testing", subset_type=SubsetType.EVAL, keys=testing_keys, dataset=dataset, repetitions=5),
        ]

class SingleArenaDatasetSplitter(DeepSportDatasetSplitter):
    def __init__(self, specific_arena_label):
        self.specific_arena_label = specific_arena_label
        self.fold_count = 5
    def __call__(self, dataset, fold=0):
        keys = list(dataset.keys.all())
        specific_keys = [k for k in keys if k.arena_label == self.specific_arena_label]
        d = self.count_keys_per_game_id(specific_keys)
        s = split_equally(d, K=self.fold_count)

        testing_keys = [k for k in specific_keys if k.game_id in s[(fold+0)%self.fold_count]]
        validation_keys = [k for k in specific_keys if k.game_id in s[(fold+1)%self.fold_count]]
        training_keys = [k for k in specific_keys if k not in testing_keys and k not in validation_keys]

        return [
            Subset(name="training", subset_type=SubsetType.TRAIN, keys=training_keys, dataset=dataset),
            Subset(name="validation", subset_type=SubsetType.EVAL, keys=validation_keys, dataset=dataset, repetitions=5),
            Subset(name="testing", subset_type=SubsetType.EVAL, keys=testing_keys, dataset=dataset, repetitions=5),
        ]

class TestingArenaLabelsDatasetSplitter():
    def __init__(self, testing_arena_labels, validation_pc=15):
        self.testing_arena_labels = testing_arena_labels
        self.validation_pc = validation_pc
        assert isinstance(self.testing_arena_labels, list)

    def __call__(self, dataset, fold=0):
        keys = list(dataset.keys.all())
        testing_keys = [k for k in keys if k.arena_label in self.testing_arena_labels]
        remaining_keys = [k for k in keys if k not in testing_keys]

        # Backup random seed
        random_state = random.getstate()
        random.seed(fold)

        validation_keys = random.sample(remaining_keys, len(keys)*self.validation_pc//100) if self.validation_pc else []

        # Restore random seed
        random.setstate(random_state)

        training_keys = [k for k in remaining_keys if k not in validation_keys]

        subsets = [
            Subset(name="training", subset_type=SubsetType.TRAIN, keys=training_keys, dataset=dataset),
            Subset(name="validation", subset_type=SubsetType.EVAL, keys=validation_keys, dataset=dataset, repetitions=2),
            Subset(name="testing", subset_type=SubsetType.EVAL, keys=testing_keys, dataset=dataset, repetitions=2),
        ]

        return [s for s in subsets if len(s.keys) > 0]
