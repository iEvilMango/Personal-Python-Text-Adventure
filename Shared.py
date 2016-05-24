def prompt_for(prompt, valid_responses):
	while(True):
		print (prompt)
		options = ""
		for item in valid_responses:
			options += "[" + str(item) + "] "
		print(options) # [1,2,3]  => [1] [2] [3]

		response = input("")
		for possible in valid_responses:
			if (str(response).lower() == str(possible).lower()):
				return possible

		for possible in valid_responses:
			if (str(response).lower() in str(possible).lower()):
				return possible

		if (str(response).lower() == "quit"):
			quit()
		print(str(response) + " is not a valid input, try again, or [quit]")

def random_range(base_value, percent_range):
	value_bonus = random.randint(0, percent_range + 1)
	output = base_value - (base_value * (percent_range / 2) / 100)
	return output + (value_bonus * base_value / 100)
