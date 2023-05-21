class UserInput:
    @staticmethod
    def multiline_input():
        # Prompt user for multiline input
        print("Enter some text (type 'done' on a new line to finish):")
        text = ""
        while True:
            line = input()
            if line == "done":
                break
            else:
                text += line
        return text
