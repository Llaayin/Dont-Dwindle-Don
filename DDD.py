# ============================================
# Don't Dwindle, Don! (DDD)
# Resource Management Simulator
# OOP CLI Prototype — v3 Dwarven Hold Edition
# ============================================

class Player:
    def __init__(self, name):
        self.name = name
        self.food = 50
        self.water = 50
        self.medicine = 20
        self.gold = 100
        self.happiness = 70

    def show_resources(self):
        print("\n--- Hold Resources ---")
        print(f"Food: {self.food}")
        print(f"Water: {self.water}")
        print(f"Medicine: {self.medicine}")
        print(f"Gold: {self.gold}")
        print(f"Morale: {self.happiness}")


class NPC:
    def __init__(self, name, request, resource, amount, role):
        self.name = name
        self.request = request
        self.resource = resource
        self.amount = amount
        self.role = role

        # Track how the player treated this NPC
        self.accepted = None      # True / False / None
        self.status = "fine"      # fine / hungry / thirsty / sick / upset


class Game:
    def __init__(self):
        self.player = None

        self.npcs = [
            NPC("Brunhilda", "needs food for her kin.", "food", 10, "Miner"),
            NPC("Thrain", "needs water for the mushroom farm.", "water", 8, "Farmer"),
            NPC("Durin", "needs medicine for the infirmary.", "medicine", 5, "Healer"),
        ]

    # ============================================
    # LOGIN
    # ============================================
    def login(self):
        print("================================")
        print("      DON'T DWINDLE, DON!")
        print("================================")

        name = input("\nEnter your name: ")
        input("Enter password: ")

        self.player = Player(name)
        print("\nLogin successful!")

    # ============================================
    # NEW GAME
    # ============================================
    def new_game(self):
        print("\n--- NEW SAVE ---")
        print("Welcome, Don!")
        self.player.show_resources()
        input("\nPress Enter to begin Day 1...")

    # ============================================
    # HANDLE REQUESTS
    # ============================================
    def handle_requests(self):
        for npc in self.npcs:

            print("\n================================")
            print("DWARF REQUEST")
            print("================================")

            print(f"{npc.name} the {npc.role} {npc.request}")
            print(f"Requested: {npc.amount} {npc.resource}")

            print("\n1. Accept")
            print("2. Reject")

            choice = input("Choice: ")

            if choice == "1":
                current = getattr(self.player, npc.resource)

                if current >= npc.amount:
                    setattr(self.player, npc.resource, current - npc.amount)
                    self.player.happiness += 5
                    npc.accepted = True
                    npc.status = "fine"
                    print("\nRequest accepted!")
                else:
                    npc.accepted = False
                    npc.status = "denied"
                    print("\nNot enough resources.")
                    self.player.happiness -= 5

            else:
                self.player.happiness -= 5
                npc.accepted = False
                npc.status = "rejected"
                print("\nRequest rejected.")

            self.player.show_resources()
            input("\nPress Enter to continue...")

    # ============================================
    # DETAILED EVALUATION (UPGRADED)
    # ============================================
    def evaluation(self):
        print("\n================================")
        print("       END OF DAY 1")
        print("================================")

        self.player.show_resources()

        print("\n--- Hold Evaluation ---")

        # Overall status
        if self.player.happiness >= 70:
            status = "THRIVING"
            mood = "The hold hums with song and hammer-fall."
        elif self.player.happiness >= 50:
            status = "STABLE"
            mood = "The hold endures, though whispers of worry echo in the tunnels."
        else:
            status = "STRUGGLING"
            mood = "The hold is grim. Dwarves mutter in the dark."

        print(f"Hold Status: {status}")
        print(mood)

        # Villager-specific status updates (UPGRADED)
        print("\n--- Dwarf Reports ---")
        for npc in self.npcs:
            self.report_dwarf(npc)

        # Resource-based warnings
        print("\n--- Hold Outlook ---")
        if self.player.food < 20:
            print("🍞 The granaries run low. Hunger stalks the tunnels.")
        if self.player.water < 20:
            print("💧 The wells are dry. The mushroom farms wither.")
        if self.player.medicine < 10:
            print("💊 The infirmary lacks supplies. Coughs spread in the mines.")
        if self.player.happiness < 40:
            print("😟 Morale is broken. Some dwarves speak of leaving the hold.")

        print("\nThe hold's fate rests on your judgment, Don.")
        input("\nPress Enter for upgrades...")

    # ============================================
    # PER-DWARF REPORT (NEW)
    # ============================================
    def report_dwarf(self, npc):
        # If accepted — report based on what they got
        if npc.accepted is True:
            if npc.resource == "food":
                print(f"✅ {npc.name} the {npc.role}: Well-fed. Her kin eat tonight.")
            elif npc.resource == "water":
                print(f"✅ {npc.name} the {npc.role}: Refreshed. The farm is watered.")
            elif npc.resource == "medicine":
                print(f"✅ {npc.name} the {npc.role}: Stocked. The sick will mend.")

        # If denied due to lack of resources
        elif npc.status == "denied":
            if npc.resource == "food":
                print(f"⚠️ {npc.name} the {npc.role}: Hungry. Her kin go without.")
            elif npc.resource == "water":
                print(f"⚠️ {npc.name} the {npc.role}: Parched. The farm dries.")
            elif npc.resource == "medicine":
                print(f"⚠️ {npc.name} the {npc.role}: Empty-handed. The sick worsen.")

        # If rejected by choice
        elif npc.status == "rejected":
            if npc.resource == "food":
                print(f"❌ {npc.name} the {npc.role}: Bitter. She feels abandoned by the hold.")
            elif npc.resource == "water":
                print(f"❌ {npc.name} the {npc.role}: Resentful. He mutters of leaving.")
            elif npc.resource == "medicine":
                print(f"❌ {npc.name} the {npc.role}: Despairing. He fears for the sick.")

    # ============================================
    # UPGRADES
    # ============================================
    def upgrades(self):
        print("\n================================")
        print("         FORGE & MARKET")
        print("================================")

        print(f"Gold: {self.player.gold}")

        print("\n1. Buy Food +10 (50 Gold)")
        print("2. Buy Water +10 (50 Gold)")
        print("3. Skip")

        choice = input("\nChoice: ")

        if choice == "1" and self.player.gold >= 50:
            self.player.food += 10
            self.player.gold -= 50
            print("\nFood stores increased!")

        elif choice == "2" and self.player.gold >= 50:
            self.player.water += 10
            self.player.gold -= 50
            print("\nWater stores increased!")

        else:
            print("\nNo trade made.")

    # ============================================
    # RUN
    # ============================================
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
            print("         A NEW DAWN BREAKS")
            print("================================")

            input("\nPress Enter to continue...")

            print("\n================================")
            print("        END OF PROTOTYPE")
            print("================================")

            print("\nThank you for playing Don't Dwindle, Don!")

        else:
            print("\nThe hold gates close behind you.")


# Start the program
game = Game()
game.run()
