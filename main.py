# for api
# run here!
from caesar.controller.inputController import createGuests
roomData = {}

# input
old_guess = 10
chanel = [1,2,3,"bus"]
max = [5,3,1,4]

guesses = createGuests(old_guess, chanel, max)
for guess in guesses:
    print(guess)

print(roomData)
roomData["1"] = guesses[0]
print(roomData)

