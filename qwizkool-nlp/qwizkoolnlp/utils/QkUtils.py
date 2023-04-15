import time

class QkUtils:
    """
    Utils for Qwizkool classes

    """

    def animate(self, text, delay):
        for c in text:
            time.sleep(delay)
            print(c, end='', flush=True)
        print()    


    def input_number(self, message, valid_range):
        while True:
            try:
                user_input = int(input(message)) 
                if user_input not in valid_range:
                    raise ValueError("Not in range") 
                break
            except ValueError:
                print("Not a valid selection! Try again.")
                continue

        return user_input 

    def input_continue(self):
        while True:
            user_input = input('\nContinue? [y/n]: ') 
            if user_input == 'y':
                return True
            elif user_input == 'n':
                return False
            else:
                continue      
     
