
# Don't Dwindle, Don!
# Resource Management Simulator
# OOP CLI Prototype

class Player:
    def __init__(self, name):
        self.name = name
        self.food = 50
        self.water = 50
        self.medicine = 20
        self.money = 100
        self.happiness = 70

    def show_resources(self):
        print("\n--- Resources ---")
        print(f"Food: {self.food}")
        print(f"Water: {self.water}")
        print(f"Medicine: {self.medicine}")
        print(f"Money: ₱{self.money}")
        print(f"Happiness: {self.happiness}")


class NPC:
    def __init__(self, name, request, resource, amount):
        self.name = name
        self.request = request
        self.resource = resource
        self.amount = amount


class Game:
    def __init__(self):
        self.player = None

        self.npcs = [
            NPC(
                "Mira",
                "needs food for her family.",
                "food",
                10
            ),
            NPC(
                "Leo",
                "needs water for the farm.",
                "water",
                8
            ),
            NPC(
                "Tomas",
                "needs medicine for the clinic.",
                "medicine",
                5
            )
        ]

    def login(self):
        print("================================")
        print("      DON'T DWINDLE, DON!")
        print("================================")

        name = input("\nEnter your name: ")
        input("Enter password: ")

        self.player = Player(name)

        print("\nLogin successful!")

    def new_game(self):
        print("\n--- NEW SAVE ---")
        print("Welcome, Don!")
        self.player.show_resources()

        input("\nPress Enter to begin Day 1...")

    def handle_requests(self):
        for npc in self.npcs:

            print("\n================================")
            print("NPC REQUEST")
            print("================================")

            print(f"{npc.name} {npc.request}")
            print(
                f"Requested: {npc.amount} "
                f"{npc.resource}"
            )

            print("\n1. Accept")
            print("2. Reject")

            choice = input("Choice: ")

            if choice == "1":

                current = getattr(
                    self.player,
                    npc.resource
                )

                if current >= npc.amount:

                    setattr(
                        self.player,
                        npc.resource,
                        current - npc.amount
                    )

                    self.player.happiness += 5

                    print("\nRequest accepted!")

                else:

                    print("\nNot enough resources.")

            else:

                self.player.happiness -= 5

                print("\nRequest rejected.")

            self.player.show_resources()

            input("\nPress Enter to continue...")

    def evaluation(self):
        print("\n================================")
        print("       END OF DAY 1")
        print("================================")

        self.player.show_resources()

        print("\n--- Evaluation ---")

        if self.player.happiness >= 70:
            print("Village Status: THRIVING")
        elif self.player.happiness >= 50:
            print("Village Status: STABLE")
        else:
            print("Village Status: STRUGGLING")

        print(
            "\nThe village's health and happiness "
            "depend on your decisions."
        )

        input("\nPress Enter for upgrades...")

    def upgrades(self):
        print("\n================================")
        print("         UPGRADE SHOP")
        print("================================")

        print(f"Money: ₱{self.player.money}")

        print("\n1. Increase Food +10 (₱50)")
        print("2. Increase Water +10 (₱50)")
        print("3. Skip")

        choice = input("\nChoice: ")

        if choice == "1" and self.player.money >= 50:
            self.player.food += 10
            self.player.money -= 50
            print("\nFood increased!")

        elif choice == "2" and self.player.money >= 50:
            self.player.water += 10
            self.player.money -= 50
            print("\nWater increased!")

        else:
            print("\nNo upgrade selected.")

    def run(self):
        self.login()

        print("\n1. Start New Save")
        print("2. Exit")

        choice = input("\nChoice: ")

        if choice == "1":

            self.new_game()
            self.handle_requests()
            self.evaluation()
            self.upgrades()

            print("\n================================")
            print("         BEGIN NEW DAY")
            print("================================")

            input(
                "\nPress Enter to continue..."
            )

            print("\n================================")
            print("        END OF PROTOTYPE")
            print("================================")

            print(
                "\nThank you for playing "
                "Don't Dwindle, Don!"
            )

        else:
            print("\nGame exited.")


# Start the program
game = Game()
game.run()

