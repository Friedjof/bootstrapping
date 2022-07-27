import random


class Bootstrap:
    def __init__(self, org: list | None = None) -> None:
        if org is None:
            self.org: list = []
        else:
            self.org: list = org

        self.samples: list = []

    def choice(self, nr_of_samples: int) -> list:
        """
        Bootstrapping
        """
        for i in range(nr_of_samples):
            temp_sample: list = []
            for j in range(len(self.org)):
                temp_sample.append(random.choice(self.org))
            self.samples.append(temp_sample)
        return self.samples
