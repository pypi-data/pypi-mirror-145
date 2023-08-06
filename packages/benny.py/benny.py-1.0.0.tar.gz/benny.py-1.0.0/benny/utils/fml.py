class FML:
    def __init__(self, author: str, place: str, text: str, time: str) -> None:
        """
        Initialize a FML object.
        
        Args:
            author (str): The author of the FML.
            place (str): The place of the FML.
            text (str): The text of the FML.
            time (str): The time of the FML.
        """

        self.author = author
        self.place = place
        self.text = text
        self.time = time

    def __str__(self) -> str:
        """
        Return a string representation of the FML.

        Returns:
            str: The string representation of the FML.
        """

        return f"{self.text}"