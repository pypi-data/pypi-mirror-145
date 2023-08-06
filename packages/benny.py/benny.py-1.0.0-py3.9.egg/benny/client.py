import requests

from typing import Union

from .utils import fml
from .utils import image

class Client:
    def __init__(self, version="v1") -> None:
        """
        Initialize the client

        Args:
            version (str): The version of the API to use
        """

        self.base_url = f"https://api.benny.fun/{version}"

    def cat(self) -> str:
        """
        Get a random cat image

        Returns:
            str: The URL of the cat image
        """

        resp = requests.get(f"{self.base_url}/cat")
        return resp.json()["image"]

    def dog(self) -> str:
        """
        Get a random dog image

        Returns:
            str: The URL of the dog image
        """        

        resp = requests.get(f"{self.base_url}/dog")
        return resp.json()["image"]

    def meme(self) -> str:
        """
        Get a random meme

        Returns:
            str: The URL of the meme
        """        

        resp = requests.get(f"{self.base_url}/meme")
        return resp.json()["meme"]

    def minion(self) -> str:
        """
        Get a random minion meme

        Returns:
            str: The URL of the minion meme
        """    

        resp = requests.get(f"{self.base_url}/minion")
        return resp.json()["minion"]

    def dadjoke(self) -> str:
        """
        Get a random dad joke

        Returns:
            str: The text of the dad joke
        """    

        resp = requests.get(f"{self.base_url}/dadjoke")
        return resp.json()["text"]

    def roast(self) -> str:
        """
        Get a random roast

        Returns:
            str: The text of the roast
        """    

        resp = requests.get(f"{self.base_url}/roast")
        return resp.json()["text"]

    def fml(self) -> fml.FML:
        """
        Get a random fml article

        Returns:
            fml.FML: The fml article
        """

        resp = requests.get(f"{self.base_url}/fml")

        if resp.status_code == 200:
            return fml.FML(resp.json()["author"], resp.json()["place"], resp.json()["text"], resp.json()["time"])
        
        else:
            return self.fml()

    def yomomma(self) -> str:
        """
        Get a random yomomma joke

        Returns:
            str: The text of the yomomma joke
        """    

        resp = requests.get(f"{self.base_url}/yomomma")
        return resp.json()["text"]

    def brainfuck(self, text: str) -> str:
        """
        Convert text to brainfuck code.

        Args:
            text (str): The text to convert to brainfuck code

        Returns:
            str: The brainfuck code.
        """    

        url = f"{self.base_url}/brainfuck"
        params = {"text": text}
        resp = requests.get(url, params=params)

        return resp.json()["text"]

    def trash(self, face: str, trash: str) -> image.Image:
        """
        Throw out the trash

        Args:
            face (str): The face to throw out the trash
            trash (str): The trash to throw out

        Returns:
            image.Image: The image of the trash
        """

        url = f"{self.base_url}/trash"
        params = {"face": face, "trash": trash}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def discord_message(self, text: str, username: str, avatar: str) -> image.Image:
        """
        Create a fake discord message

        Args:
            text (str): The text of the message
            username (str): The username of the message
            avatar (str): The avatar of the message

        Returns:
            image.Image: The image of the message
        """

        url = f"{self.base_url}/discordmessage"
        params = {"text": text, "username": username, "avatar": avatar}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def am_i_a_joke(self, image: str) -> image.Image:
        """
        Are you a joke?

        Args:
            image (str): The image to check

        Returns:
            image.Image: The image of the result
        """

        url = f"{self.base_url}/amiajoke"
        params = {"image": image}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def bad(self, image: str) -> image.Image:
        """
        Has someone been bad?

        Args:
            image (str): The image/user to tell off

        Returns:
            image.Image: The image of the result
        """

        url = f"{self.base_url}/bad"
        params = {"image": image}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def calling(self, text: str) -> image.Image:
        """
        Call the phone with your text

        Args:
            text (str): The text in the box

        Returns:
            image.Image: The image of the result
        """

        url = f"{self.base_url}/calling"
        params = {"text": text}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def captcha(self, text: str) -> image.Image:
        """
        Create a captcha

        Args:
            text (str): The text to put in the captcha

        Returns:
            image.Image: The image of the captcha
        """

        url = f"{self.base_url}/captcha"
        params = {"text": text}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def facts(self, text: str) -> image.Image:
        """
        Make something a fact

        Args:
            text (str): The text to make a fact

        Returns:
            image.Image: The image of the fact
        """

        url = f"{self.base_url}/facts"
        params = {"text": text}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def salty(self, image: str) -> image.Image:
        """
        Make someone salty

        Args:
            image (str): The image to make salty

        Returns:
            image.Image: The image of the result
        """

        url = f"{self.base_url}/salty"
        params = {"image": image}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def scroll(self, text: str) -> image.Image:
        """
        Make a scroll

        Args:
            text (str): The text to put in the scroll

        Returns:
            image.Image: The image of the scroll
        """

        url = f"{self.base_url}/scroll"
        params = {"text": text}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def shame(self, image: str) -> image.Image:
        """
        Shame someone

        Args:
            image (str): The image to shame

        Returns:
            image.Image: The image of the result
        """
            
        url = f"{self.base_url}/shame"
        params = {"image": image}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def what(self, image: str) -> image.Image:
        """
        what

        Args:
            image (str): The image for the what meme

        Returns:
            image.Image: The image of the meme
        """

        url = f"{self.base_url}/what"
        params = {"image": image}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def joke_over_head(self, image: str) -> image.Image:
        """
        Hhaaha.. joke

        Args:
            image (str): The image for the joke

        Returns:
            image.Image: The image of the meme
        """

        url = f"{self.base_url}/jokeoverhead"
        params = {"image": image}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def achievement(self, text: str, icon: int = 10) -> image.Image:
        """
        Create a fake Minecraft achievement

        Args:
            text (str): The text for the achievement
            icon (int): The icon for the achievement

        Returns:
            image.Image: The image of the achievement
        """

        url = f"{self.base_url}/achievement"
        params = {"text": text, "icon": icon}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def challenge(self, text: str, icon: int = 10) -> image.Image:
        """
        Create a fake Minecraft challenge

        Args:
            text (str): The text for the challenge
            icon (int): The icon for the challenge

        Returns:
            image.Image: The image of the challenge
        """

        url = f"{self.base_url}/challenge"
        params = {"text": text, "icon": icon}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def ship(self, user_one: str, user_two: str) -> image.Image:
        """
        Ship two people

        Args:
            user_one (str): The first user
            user_two (str): The second user

        Returns:
            image.Image: The image of the ship
        """

        url = f"{self.base_url}/ship"
        params = {"user": user_one, "user2": user_two}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def did_you_mean(self, top: str, bottom: str) -> image.Image:
        """
        Did you mean?

        Args:
            top (str): The original text
            bottom (str): The replacement text

        Returns:
            image.Image: The image of the result
        """

        url = f"{self.base_url}/didyoumean"
        params = {"top": top, "bottom": bottom}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def drake(self, top: str, bottom: str) -> image.Image:
        """
        Make a drake meme

        Args:
            top (str): The top text
            bottom (str): The bottom text

        Returns:
            image.Image: The image of the meme
        """

        url = f"{self.base_url}/drake"
        params = {"top": top, "bottom": bottom}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def floor(self, top: str, bottom: str) -> image.Image:
        """
        Make a floor meme

        Args:
            top (str): The top text
            bottom (str): The bottom text

        Returns:
            image.Image: The image of the meme
        """

        url = f"{self.base_url}/floor"
        params = {"top": top, "bottom": bottom}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def pornhub(self, text_one: str, text_two: str) -> image.Image:
        """
        Make a fake pornhub logo

        Args:
            text_one (str): The first text
            text_two (str): The second text

        Returns:
            image.Image: The image of the meme
        """

        url = f"{self.base_url}/pornhub"
        params = {"text": text_one, "text2": text_two}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    def communism(self, image: str) -> image.Image:
        """
        Overlay the communism flag on an image

        Args:
            image (str): The image to overlay the flag on

        Returns:
            image.Image: The image of the result
        """

        url = f"{self.base_url}/communism"
        params = {"image": image}
        resp = requests.get(url, params=params)

        return image.Image(resp)

    discordmessage = discord_message
    amiajoke = am_i_a_joke
    jokeoverhead = joke_over_head
    didyoumean = did_you_mean

    random_cat = cat
    random_dog = dog

    dad_joke = dadjoke
    yomomma_joke = yomomma