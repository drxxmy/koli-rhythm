import json
import os


class Performance:
    """The class used to represent a player's performance.

    Methods
    -------
    update_accuracy()
        Used to update accuracy.
    update_combo(grade)
        Used to update combo.
    update_hits_counter(grade)
        Used to update hit counters.
    get_grade(progress)
        Used to get a grade regarding progress.
    add_score(grade)
        Used to get a grade regarding progress.
    """

    def __init__(self, player_name: str) -> None:
        """
        Parameters
        ----------
        player_name : str
            Player username.

        Raises
        ------
        AssertionError
            player_name is not a string.
        """
        assert isinstance(player_name, str), "player_name must be a string."
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.max_possible_combo = 0
        self.accuracy = 100.0
        self.perfect_hits = 0
        self.good_hits = 0
        self.bad_hits = 0
        self.misses = 0
        self.player_name = player_name

    def update_accuracy(self) -> None:
        """Used to update accuracy."""
        chisl = 300 * self.perfect_hits + 100 * self.good_hits + 50 * self.bad_hits
        znam = 300 * (self.perfect_hits + self.good_hits + self.bad_hits + self.misses)
        if znam != 0:
            self.accuracy = chisl / znam * 100

    def update_combo(self, grade: str) -> None:
        """Used to update combo.

        Parameters
        ----------
        grade : str
            Last grade.

        Raises
        ------
        AssertionError
            grade is not a string.
        """
        assert isinstance(grade, str), "grade must be a string."
        if grade != "Miss!":
            self.combo += 1
        else:
            if self.combo >= self.max_combo:
                self.max_combo = self.combo
            self.combo = 0

    def update_hits_counter(self, grade: str) -> None:
        """Used to update hit counters.

        Parameters
        ----------
        grade : str
            Last grade.

        Raises
        ------
        AssertionError
            grade is not a string.
        """
        assert isinstance(grade, str), "grade must be a string."
        if grade == "Perfect!":
            self.perfect_hits += 1
        elif grade == "Good!":
            self.good_hits += 1
        elif grade == "Bad!":
            self.bad_hits += 1
        else:
            self.misses += 1

    def get_grade(self, progress: float) -> str:
        """Used to get a grade regarding progress.

        Parameters
        ----------
        progress : float
            Hit progress.

        Raises
        ------
        AssertionError
            progress is not a float.

        Returns
        ----------
        str
            Grade.
        """
        assert isinstance(progress, float), "progress must be a float."
        if progress >= 0.7 and progress < 0.8 or progress > 1.2 and progress <= 1.3:
            return "Bad!"
        elif progress >= 0.8 and progress < 0.9 or progress > 1.1 and progress <= 1.2:
            return "Good!"
        elif progress >= 0.9 and progress <= 1.1:
            return "Perfect!"
        else:
            return "Miss!"

    def add_score(self, grade: str) -> None:
        """Used to get a grade regarding progress.

        Parameters
        ----------
        grade : str
            Last grade.

        Raises
        ------
        AssertionError
            grade is not a string.
        """
        assert isinstance(grade, str), "grade must be a string."
        if self.combo < 10:
            score_multiplier = 1
        else:
            score_multiplier = int(self.combo * 0.1)
        if grade == "Bad!":
            self.score += 50 * score_multiplier
        elif grade == "Good!":
            self.score += 100 * score_multiplier
        elif grade == "Perfect!":
            self.score += 300 * score_multiplier


class Leaderboard:
    """The abstract class used to represent a menu.

    Methods
    -------
    load(chart_name)
        Used to load leaderboards for a certain chart.
    save(chart_name)
        Used to save leaderboards for a certain chart.
    add(performance)
        Used to add performance to performances list.
    remove(performance)
        Used to remove performance from performances list.
    get_all_performances()
        Used to get all performances.
    """

    def __init__(self) -> None:
        self.performances = []

    def load(self, chart_name: str):
        """Used to load leaderboards for a certain chart.

        Parameters
        ----------
        chart_name : str
            Chart name.

        Raises
        ------
        AssertionError
            chart_name is not a string.
        """
        assert isinstance(chart_name, str), "chart_name must be a string."
        chart_locataion = os.path.join("src", "charts", chart_name, "leaderboard.json")
        try:
            with open(chart_locataion, "r") as leaderboard:
                data = json.load(leaderboard)
                leaderboard.close()
        except FileNotFoundError as error:
            print(f"Caught {type(error)}: error")

        self.performances.clear()
        scores = data["scores"]
        for result in scores:
            performance = Performance(result["data"]["player_name"])
            performance.score = result["data"]["score"]
            performance.combo = result["data"]["combo"]
            performance.max_combo = result["data"]["max_combo"]
            performance.max_possible_combo = result["data"]["max_possible_combo"]
            performance.accuracy = result["data"]["accuracy"]
            performance.perfect_hits = result["data"]["perfect_hits"]
            performance.good_hits = result["data"]["good_hits"]
            performance.bad_hits = result["data"]["bad_hits"]
            performance.misses = result["data"]["misses"]
            self.performances.append(performance)

    def save(self, chart_name: str):
        """Used to save leaderboards for a certain chart.

        Parameters
        ----------
        chart_name : str
            Chart name.

        Raises
        ------
        AssertionError
            chart_name is not a string.
        """
        assert isinstance(chart_name, str), "chart_name must be a string."
        file_name = "leaderboard.json"
        file_location = os.path.join("src", "charts", chart_name, file_name)
        output = {}
        performances = []
        for performance in self.performances:
            score = {}
            data = {}
            score["id"] = self.performances.index(performance)
            data["score"] = performance.score
            data["combo"] = performance.combo
            data["max_combo"] = performance.max_combo
            data["max_possible_combo"] = performance.max_possible_combo
            data["accuracy"] = performance.accuracy
            data["perfect_hits"] = performance.perfect_hits
            data["good_hits"] = performance.good_hits
            data["bad_hits"] = performance.bad_hits
            data["misses"] = performance.misses
            data["player_name"] = performance.player_name
            score["data"] = data
            performances.append(score)
        output["scores"] = performances
        try:
            with open(file_location, "w") as write_file:
                json.dump(output, write_file)
        except FileExistsError as error:
            print(f"Caught {type(error)}: error")

    def add(self, performance: Performance) -> None:
        """Used to add performance to performances list.

        Parameters
        ----------
        performance : Performance
            Performance of a player.

        Raises
        ------
        AssertionError
            performance is not an instance of the Performance class.
        """
        assert isinstance(
            performance, Performance
        ), "performance must be an instance of the Performance class."
        self.performances.append(performance)

    def remove(self, performance: Performance) -> None:
        """Used to remove performance from performances list.

        Parameters
        ----------
        performance : Performance
            Performance of a player.

        Raises
        ------
        AssertionError
            performance is not an instance of the Performance class.
        """
        assert isinstance(
            performance, Performance
        ), "performance must be an instance of the Performance class."
        self.performances.remove(performance)

    def get_all_performances(self) -> list:
        """Used to get all performances.

        Returns
        ----------
        list
            List of all performances.
        """
        return self.performances
