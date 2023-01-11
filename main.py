import random
import time
import webbrowser
import creds
import openai

openai.api_key = creds.api_key

wordlist = ["submarine", "dog", "cat", "bird", "couch", "chair", "house", "piano", "backpack",
            "mountain", "table", "computer", "tree", "television", "microwave", "oven", "fish",
            "shoe", "ice cream", "toilet paper", "football", "soccer", "baseball", "cell phone", "basketball",
            "volleyball", "banana", "apple", "orange", "monkey", "horse", "pumpkin", "toilet", "water", "bottle",
            "skittles", "door knob", "light switch", "cookie", "OREO", "french fry", "clock", "snow", "ice","fire",
            "rain", "map", "chocolate bar", "tennis ball", "napkin", "plate", "frisbee", "cup", "painting",
            "dollar bill", "coin", "watermelon", "lion", "baby", "bike", "man", "girl", "school", "book", "pencil",
            "hat", "whale", "bus", "ostrich", "cupcake", "cake", "dress", "bat", "taco", "burrito", "road", "toy",
            "leaf", "cheese", "plant", "metal", "wall", "boat", "car", "cow", "sheep", "wood", "spatula", "bed",
            "candle", "headphones", "stuffed animal"]


def getWords():
    a = random.randint(0, len(wordlist) - 1)

    b = random.randint(0, len(wordlist) - 1)
    while b == a:
        b = random.randint(0, len(wordlist) - 1)

    return [wordlist[a], wordlist[b]]


def generateImage(words):
    textToGenerate = "A " + words[0] + " " + words[1]
    # print(textToGenerate)

    response = openai.Image.create(
      prompt=textToGenerate,
      n=2,
      size="1024x1024"
    )

    # url = response["data"][0]["url"]

    # webbrowser.open(url)
    return response


def startRound(res, words):
    roundScore = 0
    print("\nType in your guesses:")

    # getWords which returns a list
    # words = getWords()

    # generateImage
    # generateImage(words)
    # maybe put this later so that you can do two image

    # open the url here
    url = res["data"][0]["url"]

    webbrowser.open(url)

    wordsGuessed = 0

    nextImageOpened = False
    while True:
        guess = input("Enter a guess: ")
        if guess in words:
            if not nextImageOpened:
                roundScore += 2
            else:
                roundScore += 1
            print("Correct")
            wordsGuessed += 1
        elif guess == "next" and not nextImageOpened:
            url = res["data"][1]["url"]
            webbrowser.open(url)
            nextImageOpened = True
        elif guess != "done":
            print("Incorrect")
        else:
            break

        if wordsGuessed == 2:
            print("You got both words!")
            break

    if roundScore == 1:
        print("\nWow, you scored " + str(roundScore) + " point\n")
    else:
        print("\nWow, you scored " + str(roundScore) + " points\n")

    print("The image was a " + words[0] + " " + words[1] + "\n")

    return roundScore


def playTurn(teamName, roundNumber):
    time.sleep(1)
    print("Round " + roundNumber + ":")
    time.sleep(0.5)
    print(teamName + "'s turn")
    time.sleep(0.5)
    print("Generating image...")
    words = getWords()
    ret = generateImage(words)
    print("Image generated")
    isReady = input("Type \"ready\" when you want to start\n")
    # While loop for not ready
    while isReady != "ready":
        isReady = input("Type \"ready\" when you want to start\n")

    return startRound(ret, words)


print("Welcome to charades with DALL·E")
time.sleep(1)

team1Score = 0
team2Score = 0


team1 = input("Enter name of team 1: ")
team2 = input("Enter name of team 2: ")
while team2 == team1:
    print("Please type a different name")
    team2 = input("Enter name of team 2: ")

team1Score += playTurn(team1, "1")

team2Score += playTurn(team2, "1")


team2Score += playTurn(team1, "2")

team1Score += playTurn(team2, "2")


team1Score += playTurn(team1, "3")

team2Score += playTurn(team2, "3")


team2Score += playTurn(team1, "4")

team1Score += playTurn(team2, "4")


team1Score += playTurn(team1, "5")

team2Score += playTurn(team2, "5")

time.sleep(1)
print("\nThis is the end of the game")
time.sleep(0.5)
print("The winner is:")
time.sleep(1)

if team1Score > team2Score:
    print(team1 + " with " + str(team1Score) + " points!")
    print(team2 + " got " + str(team2Score) + " points.")

elif team2Score > team1Score:
    print(team2 + " with " + str(team2Score) + " points!")
    print(team1 + " got " + str(team1Score) + " points.")

else:
    print("Nobody, you each scored " + str(team2Score) + " points!")
