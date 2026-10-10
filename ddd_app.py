# ============================================
# Don't Dwindle, Don! (DDD) by Aaron Jared Lee
# Resource Management Simulator
# OOP Streamlit Version — v5 (Inheritance + 5 Days)
# ============================================

import streamlit as st
import json

st.set_page_config(
    page_title="Don't Dwindle, Don!",
    page_icon="⛏️",
    layout="wide"
)


# ============================================
# CHARACTER CLASS (Parent)
# ============================================
class Character:
    """Base class for all characters in the game."""
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def introduce(self):
        return f"I am {self.name}, the {self.role}."


# ============================================
# PLAYER CLASS (Inherits Character)
# ============================================
class Player(Character):
    def __init__(self, name):
        super().__init__(name, "Resource Manager")
        self.food = 50
        self.water = 50
        self.medicine = 20
        self.gold = 100
        self.happiness = 70


# ============================================
# NPC CLASS (Inherits Character)
# ============================================
class NPC(Character):
    def __init__(self, name, request, resources, amounts, role, intro=None):
        super().__init__(name, role)
        self.request = request
        self.resources = resources
        self.amounts = amounts
        self.intro = intro
        self.accepted = None
        self.status = "fine"

    def react(self):
        """Polymorphism — each dwarf reacts differently."""
        if self.status == "rejected":
            if self.role == "Miner":
                return "glare"
            elif self.role == "Farmer":
                return "frown"
            elif self.role == "Healer":
                return "grim"
            elif self.role == "Blacksmith":
                return "disappointed"
            else:
                return "sad"
        return "neutral"


# ============================================
# GAME CLASS
# ============================================
class Game:
    MAX_DAY = 5

    def __init__(self):
        self.player = None
        self.day = 1
        self.start_happiness = 70
        self.doculog = []
        self.gold_income = 0
        self.npcs = []
        self.day_summaries = []

        self.load_day(1)

    def load_day(self, day):
        if day == 1:
            self.npcs = [
                NPC("Brunhilda", "needs food for her kin, their stomachs growing louder by the day.",
                    ["food"], [10], "Miner"),
                NPC("Thrain", "needs water for the mushroom farm before the mushrooms dry up.",
                    ["water"], [8], "Farmer"),
                NPC("Durin", "needs medicine for the infirmary in order to tend to the sick and the wounded.",
                    ["medicine"], [5], "Healer"),
            ]
        elif day == 2:
            self.npcs = [
                NPC("Brunhilda", "needs extra food for an extra refugee along with the rest of her kin.",
                    ["food"], [12], "Miner"),
                NPC("Thrain", "needs more water as the ground dries up faster than he expected, threatening the loss of crops.",
                    ["water"], [10], "Farmer"),
                NPC("Durin", "needs more medicine — the sick are multiplying.",
                    ["medicine"], [8], "Healer"),
                NPC(
                    "Grimwald",
                    "needs gold to repair the forges.",
                    ["gold"],
                    [20],
                    "Blacksmith",
                    intro="A stout dwarf with soot-stained hands steps forward. 'Name's Grimwald, yeah. I'm the head of the forge, the heart of our hold. Without repairs, we'll lose our edge. And without our edge, we'll lose everything.'"
                ),
            ]
        elif day == 3:
            self.npcs = [
                NPC("Brunhilda", "makes a request for more food as more hungry wails can be heard in the distance.",
                    ["food"], [15], "Miner"),
                NPC("Thrain", "needs water to moisten the soil for the mycelium to thrive.",
                    ["water"], [12], "Farmer"),
                NPC("Durin", "needs more medicine as a new fever spreads in the mines.",
                    ["medicine"], [10], "Healer"),
                NPC("Grimwald", "requests for more gold funding in order to reheat the forges.",
                    ["gold"], [25], "Blacksmith"),
                NPC(
                    "Sigrun",
                    "needs rare herbs for the hold's protective wards.",
                    ["medicine"],
                    [6],
                    "Runekeeper",
                    intro="An elderly dwarf in rune-stitched robes approaches. 'I be Sigrun, guardian of ye wards. The old barrier runes over yonder weaken with each passing night. Without rare herbs to renew them, dark things will find their way in.'"
                ),
            ]
        elif day == 4:
            # Day 4: 5 dwarves, each demands 2 resources at half of Day 3 amounts
            self.npcs = [
                NPC("Brunhilda", "needs food and water — the tunnels are cold and her kin are both hungry and thirsty.",
                    ["food", "water"], [8, 6], "Miner"),
                NPC("Thrain", "needs water and food — his farmhands are hungry and the soil is dry.",
                    ["water", "food"], [6, 5], "Farmer"),
                NPC("Durin", "needs medicine and water — the wounded need tending and the wells are low.",
                    ["medicine", "water"], [5, 6], "Healer"),
                NPC("Grimwald", "needs gold and food — the forge crew is hungry and the repairs remain unfinished.",
                    ["gold", "food"], [13, 6], "Blacksmith"),
                NPC("Sigrun", "needs medicine and gold — the wards require both herbs and offerings.",
                    ["medicine", "gold"], [3, 10], "Runekeeper"),
            ]
        elif day >= 5:
            # Day 5: 5 dwarves, 2 resources each (slightly higher than Day 4)
            self.npcs = [
                NPC("Brunhilda", "needs food and water — the hold grows desperate.",
                    ["food", "water"], [10, 8], "Miner"),
                NPC("Thrain", "needs water and food — the farm is failing.",
                    ["water", "food"], [8, 6], "Farmer"),
                NPC("Durin", "needs medicine and water — illness spreads and the wells are dry.",
                    ["medicine", "water"], [6, 8], "Healer"),
                NPC("Grimwald", "needs gold and food — the forges need tending and the crew must be fed.",
                    ["gold", "food"], [15, 8], "Blacksmith"),
                NPC("Sigrun", "needs medicine and gold — the wards fade faster than she can renew them.",
                    ["medicine", "gold"], [4, 12], "Runekeeper"),
            ]

    def new_game(self):
        self.player = Player("Don")
        self.day = 1
        self.doculog = []
        self.day_summaries = []
        self.load_day(1)

    def to_dict(self):
        return {
            "day": self.day,
            "food": self.player.food,
            "water": self.player.water,
            "medicine": self.player.medicine,
            "gold": self.player.gold,
            "happiness": self.player.happiness,
            "doculog": self.doculog,
            "day_summaries": self.day_summaries,
            "start_happiness": self.start_happiness,
        }

    def load_from_dict(self, data):
        self.player = Player("Don")
        self.day = data["day"]
        self.player.food = data["food"]
        self.player.water = data["water"]
        self.player.medicine = data["medicine"]
        self.player.gold = data["gold"]
        self.player.happiness = data["happiness"]
        self.doculog = data["doculog"]
        self.day_summaries = data["day_summaries"]
        self.start_happiness = data["start_happiness"]
        self.load_day(self.day)

    def apply_yesterday_consequences(self):
        if not self.day_summaries:
            return []
        last = self.day_summaries[-1]
        consequences = []

        if last["morale_end"] < 40:
            self.player.happiness -= 5
            consequences.append("😟 The hold's low morale lingers. Some dwarves woke up angry (−5 morale).")
        elif last["morale_end"] >= 80:
            self.player.happiness += 3
            consequences.append("😊 The hold's good spirits continue. Your fellow dwarves greet you with warmth (+3 morale).")

        if last["food_end"] < 15:
            consequences.append("🍞 Food supplies are critically low. Some dwarves begin to starve.")
        if last["medicine_end"] < 8:
            self.player.happiness -= 5
            consequences.append("💊 Sick dwarves went untreated overnight (−5 morale).")
        if last["water_end"] < 15:
            consequences.append("💧 The wells ran dry overnight. The next day begins with worry.")

        return consequences

    def check_request(self, npc):
        """Return (can_afford, missing_list)."""
        missing = []
        for resource, amount in zip(npc.resources, npc.amounts):
            if getattr(self.player, resource) < amount:
                missing.append(f"{amount} {resource}")
        return len(missing) == 0, missing

    def fulfill_request(self, npc):
        """Deduct resources and increase morale."""
        for resource, amount in zip(npc.resources, npc.amounts):
            current = getattr(self.player, resource)
            setattr(self.player, resource, current - amount)
        self.player.happiness += 5
        npc.accepted = True
        npc.status = "fine"

    def report_dwarf(self, npc):
        # Single resource (Days 1–3)
        if len(npc.resources) == 1:
            resource = npc.resources[0]
            if npc.accepted is True:
                if resource == "food":
                    return f"✅ {npc.name} the {npc.role}: Food is restocked. {npc.name}'s kin will get to eat tonight."
                elif resource == "water":
                    return f"✅ {npc.name} the {npc.role}: Water is restocked. The crops have been moistened and are able to grow a little more."
                elif resource == "medicine":
                    return f"✅ {npc.name} the {npc.role}: Medicine is restocked. {npc.name} breathes a sigh of relief as the injured workers' wounds can finally be taken care of."
                elif resource == "gold":
                    if npc.name == "Grimwald":
                        return f"✅ Grimwald the Blacksmith: The gold is handed over. 'My thanks, Don. I'll have the forges roaring by morning.'"
                    return f"✅ {npc.name} the {npc.role}: Gold received."
            elif npc.status == "denied":
                if resource == "food":
                    return f"⚠️ {npc.name} the {npc.role}: The growls of their stomach are audible. Their kin and the rest of the hold will soon follow..."
                elif resource == "water":
                    return f"⚠️ {npc.name} the {npc.role}: A drought begins to fester among the hold. The crops are withering..."
                elif resource == "medicine":
                    return f"⚠️ {npc.name} the {npc.role}: The conditions of the sick workers worsen. The lives of your fellow-men may start dwindling..."
                elif resource == "gold":
                    if npc.name == "Grimwald":
                        return f"⚠️ Grimwald the Blacksmith: He stares at the empty coffer. 'No gold? Then no repairs. Don't let the forges grow too cold, Don.'"
                    return f"⚠️ {npc.name} the {npc.role}: The forges remain broken."
            elif npc.status == "rejected":
                if resource == "food":
                    return f"❌ {npc.name} the {npc.role}: They glare at you with resentment. They will remember you being the reason their kin will starve."
                elif resource == "water":
                    return f"❌ {npc.name} the {npc.role}: {npc.name} flashes a visible frown and leaves."
                elif resource == "medicine":
                    return f"❌ {npc.name} the {npc.role}: A grim shadow looms over {npc.name}'s face."
                elif resource == "gold":
                    if npc.name == "Grimwald":
                        return f"❌ Grimwald the Blacksmith: He shakes his head slowly. 'So that's how it be then, huh? I'll remember this, Don.'"
                    return f"❌ {npc.name} the {npc.role}: They shake their head in disappointment."

        # Multiple resources (Days 4–5)
        else:
            resource_str = " and ".join(
                f"{amount} {resource}" for resource, amount in zip(npc.resources, npc.amounts)
            )
            if npc.accepted is True:
                return f"✅ {npc.name} the {npc.role}: Received {resource_str}. They nod with gratitude."
            elif npc.status == "denied":
                return f"⚠️ {npc.name} the {npc.role}: Requested {resource_str}, but the hold couldn't spare it."
            elif npc.status == "rejected":
                return f"❌ {npc.name} the {npc.role}: Request for {resource_str} was rejected. They leave with a heavy heart."

        return f"— {npc.name} made no request today."

    def calculate_income(self):
        morale = self.player.happiness
        if morale >= 90:
            return 40
        elif morale >= 70:
            return 30
        elif morale >= 50:
            return 20
        elif morale >= 30:
            return 10
        elif morale >= 10:
            return 0
        else:
            return -10

    def check_game_over(self):
        return self.player.happiness <= 0


# ============================================
# SESSION STATE INIT
# ============================================
if "game" not in st.session_state:
    st.session_state.game = Game()
    st.session_state.screen = "title"
    st.session_state.request_index = 0
    st.session_state.day_consequences = []
    st.session_state.requests_this_day = 0

game = st.session_state.game


# ============================================
# SIDEBAR
# ============================================
if st.session_state.screen in ["play", "evaluation", "upgrades", "new_day"]:
    st.sidebar.title("⛏️ Hold Resources")
    st.sidebar.metric("🍞 Food", game.player.food)
    st.sidebar.metric("💧 Water", game.player.water)
    st.sidebar.metric("💊 Medicine", game.player.medicine)
    st.sidebar.metric("💰 Gold", game.player.gold)
    st.sidebar.metric("😊 Morale", game.player.happiness)
    st.sidebar.divider()
    st.sidebar.caption(f"📅 Day {game.day} of {Game.MAX_DAY}")

    st.sidebar.divider()
    save_data = json.dumps(game.to_dict(), indent=2)
    st.sidebar.download_button(
        label="💾 Save Game",
        data=save_data,
        file_name=f"ddd_save_day{game.day}.json",
        mime="application/json",
        use_container_width=True
    )


# ============================================
# TITLE SCREEN
# ============================================
if st.session_state.screen == "title":
    st.title("⛏️ DON'T DWINDLE, DON!")
    st.subheader("A Dwarven Resource Management Game")
    st.divider()
    st.write("You are **Don**, the Resource Manager of the Hold.")
    st.write("Your fellow dwarves will come to you with all kinds of requests — food, water, medicine, gold.")
    st.write("Every choice you make affects the hold's morale and survival.")
    st.write("")
    st.write("**And as always Don, remember our Hold's motto: Don't Dwindle!**")
    st.divider()

    if st.button("▶️ BEGIN MANAGEMENT", type="primary", use_container_width=True):
        game.new_game()
        st.session_state.request_index = 0
        st.session_state.day_consequences = []
        st.session_state.requests_this_day = 0
        st.session_state.screen = "play"
        st.rerun()

    st.divider()
    with st.expander("📂 Load a Saved Game"):
        uploaded = st.file_uploader("Upload a saved game file", type="json", label_visibility="collapsed")
        if uploaded is not None:
            try:
                data = json.load(uploaded)
                game.load_from_dict(data)
                st.session_state.request_index = 0
                st.session_state.requests_this_day = 0
                st.session_state.day_consequences = []
                st.session_state.screen = "play"
                st.success(f"Loaded Day {data['day']} save!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to load save: {e}")


# ============================================
# NEW DAY INTRO
# ============================================
elif st.session_state.screen == "new_day":
    st.title(f"🌅 Day {game.day} Begins")
    st.divider()

    if st.session_state.day_consequences:
        st.subheader("📋 Consequences from Yesterday")
        for c in st.session_state.day_consequences:
            st.warning(c)
    else:
        st.subheader("📋 A New Day Dawns")
        st.write("The hold is quiet. Dwarves prepare for the day ahead.")

    st.divider()
    st.write("**Remember not to dwindle, Don.**")

    if st.button("▶️ BEGIN DAY", type="primary", use_container_width=True):
        game.start_happiness = game.player.happiness
        st.session_state.request_index = 0
        st.session_state.requests_this_day = 0
        st.session_state.screen = "play"
        st.rerun()


# ============================================
# PLAY SCREEN
# ============================================
elif st.session_state.screen == "play":
    idx = st.session_state.request_index

    if idx >= len(game.npcs):
        st.session_state.screen = "evaluation"
        st.rerun()

    npc = game.npcs[idx]

    st.title(f"📜 Dwarf Request — Day {game.day}")
    st.divider()

    if npc.intro:
        st.info(npc.intro)
        st.divider()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"### 🧔 {npc.name}")
        st.caption(f"*{npc.role}*")
    with col2:
        st.markdown(f"**{npc.name}** {npc.request}")
        st.markdown("**Requested:**")
        for resource, amount in zip(npc.resources, npc.amounts):
            st.markdown(f"- {amount} {resource}")

    st.divider()

    can_afford, missing = game.check_request(npc)

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("✅ ACCEPT", use_container_width=True, type="primary"):
            if can_afford:
                game.fulfill_request(npc)
            else:
                npc.accepted = False
                npc.status = "denied"
                game.player.happiness -= 5

            entry = game.report_dwarf(npc)
            game.doculog.append(entry)
            st.session_state.request_index += 1
            st.session_state.requests_this_day += 1
            st.rerun()

    with col_b:
        if st.button("❌ REJECT", use_container_width=True):
            game.player.happiness -= 5
            npc.accepted = False
            npc.status = "rejected"

            entry = game.report_dwarf(npc)
            game.doculog.append(entry)
            st.session_state.request_index += 1
            st.session_state.requests_this_day += 1
            st.rerun()

    if game.doculog:
        st.divider()
        st.subheader("📖 Don's Docu-log")
        for entry in game.doculog[-5:]:
            st.write(entry)


# ============================================
# EVALUATION SCREEN
# ============================================
elif st.session_state.screen == "evaluation":
    st.title(f"🌙 END OF DAY {game.day}")
    st.divider()

    st.subheader("--- Hold Evaluation ---")

    if game.player.happiness >= 70:
        status = "THRIVING"
        mood = "The hold hums with song and the clanging of hammers."
    elif game.player.happiness >= 50:
        status = "STABLE"
        mood = "The hold endures, though whispers of worry echo throughout the tunnels."
    else:
        status = "STRUGGLING"
        mood = "The hold is grim. Dwarves mutter among themselves."

    st.markdown(f"### Hold Status: **{status}**")
    st.write(mood)

    st.divider()
    st.subheader("--- Day's Outcome ---")
    if game.player.happiness > game.start_happiness:
        st.success("🌟 The hold's spirit has risen today. Don's leadership has not gone unnoticed.")
    elif game.player.happiness < game.start_happiness:
        st.error("💀 The hold's morale has fallen. A shadow hangs over the hold.")
    else:
        st.info("⚖️ The hold remains unchanged. Neither joy nor sorrow stirs the tunnels tonight.")

    st.divider()
    st.subheader("💰 Hold Income")
    income = game.calculate_income()
    game.gold_income = income
    game.player.gold += income

    if income > 0:
        st.success(f"The mines produce **+{income} gold** today.")
    elif income < 0:
        st.error(f"Desertion and disrepair cost the hold **{income} gold**.")
    else:
        st.warning("No gold is produced today.")

    st.divider()
    st.subheader("--- Hold Outlook ---")
    warnings = []
    if game.player.food < 20:
        warnings.append("🍞 The granaries run low. Hunger stalks the tunnels.")
    if game.player.water < 20:
        warnings.append("💧 The wells are dry. The mushroom farms wither.")
    if game.player.medicine < 10:
        warnings.append("💊 The infirmary lacks supplies. Disease begins to spread.")
    if game.player.happiness < 40:
        warnings.append("😟 Morale is broken. Some dwarves speak of leaving the hold.")

    if warnings:
        for w in warnings:
            st.warning(w)
    else:
        st.write("No critical warnings today.")

    st.divider()
    st.write("**Remember not to dwindle, Don.**")

    st.divider()

    with st.expander("📖 Open Don's Docu-log (Today's Entries)"):
        today_start = max(0, len(game.doculog) - st.session_state.requests_this_day)
        todays_entries = game.doculog[today_start:]
        if todays_entries:
            for entry in todays_entries:
                st.write(entry)
        else:
            st.write("No entries today.")

    with st.expander("📚 View Full Docu-log (All Days)"):
        if game.doculog:
            for entry in game.doculog:
                st.write(entry)
        else:
            st.write("The Docu-log is empty.")

    if game.check_game_over():
        st.session_state.screen = "game_over"
        st.rerun()

    if st.button("▶️ GO TO FORGE & MARKET", type="primary", use_container_width=True):
        game.day_summaries.append({
            "day": game.day,
            "morale_end": game.player.happiness,
            "food_end": game.player.food,
            "water_end": game.player.water,
            "medicine_end": game.player.medicine,
        })
        st.session_state.screen = "upgrades"
        st.rerun()


# ============================================
# UPGRADES SCREEN
# ============================================
elif st.session_state.screen == "upgrades":
    st.title("🔨 FORGE & MARKET")
    st.divider()

    st.markdown(f"### Gold: 💰 {game.player.gold}")
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🍞 Food +10")
        st.write("**Cost:** 50 Gold")
        if st.button("Buy Food", use_container_width=True, disabled=game.player.gold < 50):
            game.player.food += 10
            game.player.gold -= 50
            st.success("Food stores increased!")
            st.rerun()

    with col2:
        st.markdown("### 💧 Water +10")
        st.write("**Cost:** 50 Gold")
        if st.button("Buy Water", use_container_width=True, disabled=game.player.gold < 50):
            game.player.water += 10
            game.player.gold -= 50
            st.success("Water stores increased!")
            st.rerun()

    with col3:
        st.markdown("### 💊 Medicine +5")
        st.write("**Cost:** 60 Gold")
        if st.button("Buy Medicine", use_container_width=True, disabled=game.player.gold < 60):
            game.player.medicine += 5
            game.player.gold -= 60
            st.success("Medicine stores increased!")
            st.rerun()

    st.divider()

    if game.day >= Game.MAX_DAY:
        if st.button("▶️ END THE BETA", use_container_width=True, type="primary"):
            st.session_state.screen = "end"
            st.rerun()
    else:
        if st.button("▶️ BEGIN NEXT DAY", use_container_width=True, type="primary"):
            game.day += 1
            game.load_day(game.day)
            st.session_state.day_consequences = game.apply_yesterday_consequences()
            st.session_state.screen = "new_day"
            st.rerun()


# ============================================
# END OF BETA SCREEN
# ============================================
elif st.session_state.screen == "end":
    st.title("🌅 A NEW DAWN BREAKS")
    st.divider()
    st.write(f"Thank you for playing **Don't Dwindle, Don!**")
    st.write(f"**Days survived:** {Game.MAX_DAY}")
    st.write("")
    st.write("This is the end of the beta.")
    st.write("More days, dwarves, and challenges to come.")
    st.divider()

    st.subheader("--- Final Docu-log ---")
    for entry in game.doculog:
        st.write(entry)

    st.divider()
    if st.button("🔁 PLAY AGAIN", type="primary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ============================================
# GAME OVER SCREEN
# ============================================
elif st.session_state.screen == "game_over":
    st.title("💀 THE HOLD HAS FALLEN")
    st.divider()
    st.write("The morale of your people reached zero.")
    st.write("Dwarves abandoned the hold. Don's leadership has failed.")
    st.write(f"**Days survived:** {game.day}")
    st.divider()
    if st.button("🔁 TRY AGAIN", type="primary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
