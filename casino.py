import random
from colorama import Fore, Style


class Casino:
    def __init__(self):
        self.symbols = ["🍒", "🍋", "🍇", "🍉", "🔔", "💎"]

    def playSlotMachine(self, bet):

        result = [random.choice(self.symbols) for _ in range(3)]
        print(f"{Fore.RED}🎰 Slot Machine Result:{Style.RESET_ALL}", " ".join(result))

        if result[0] == result[1] == result[2]:
            winnings = bet * 10
            print(f"{Fore.GREEN}🎉 Jackpot! You won ${winnings}!{Style.RESET_ALL}")
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            winnings = bet * 2
            print(f"{Fore.GREEN}🎉 You won ${winnings}!{Style.RESET_ALL}")
        else:
            winnings = -bet
            print(f"{Fore.RED}😢 You lost ${bet}.{Style.RESET_ALL}")

        return winnings