# ============================================
# Don't Dwindle, Don! (DDD) by Aaron Jared Lee
# Resource Management Simulator
# OOP Streamlit Version — v6
# ============================================

import streamlit as st
import json
import base64
import os

# --- FUNCTION TO MAKE IMAGE CLICKABLE ---
def img_to_bytes(img_path):
    if not os.path.exists(img_path):
        st.error(f"Error: Image not found at {img_path}")
        return ""
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def clickable_image(image_path, button_text="Click Me", use_container_width=True):
    img_base64 = img_to_bytes(image_path)
    if not img_base64:
        return False
        
    html = f'''
    <style>
        .image-button {{
            background: none;
            border: none;
            padding: 0;
            cursor: pointer;
            width: 100%;
            display: flex;
            justify-content: center;
        }}
        .image-button img {{
            width: 100%;
            max-width: 800px;
            transition: transform 0.1s;
        }}
        .image-button img:hover {{
            transform: scale(1.05);
        }}
    </style>
    <form action="" method="get" style="margin: 0; padding: 0;">
        <button class="image-button" type="submit" name="{button_text}" style="width: fit-content; margin: 0 auto; display: block;">
            <img src="data:image/png;base64,{img_base64}" alt="{button_text}">
        </button>
    </form>
    '''
    
    st.markdown(html, unsafe_allow_html=True)
    
    query_params = st.query_params
    if button_text in query_params:
        st.query_params.clear() 
        return True
    return False
# ---------------------------------------

st.set_page_config(
    page_title="Don't Dwindle, Don!",
    page_icon="⛏️",
    layout="wide"
)
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

    # ============================================
    # MORALE SCALING (Varies by Day)
    # ============================================
    def get_morale_accept(self):
        table = {1: 5, 2: 4, 3: 3, 4: 2, 5: 2}
        return table.get(self.day, 2)

    def get_morale_deny(self):
        table = {1: 3, 2: 4, 3: 5, 4: 7, 5: 8}
        return table.get(self.day, 8)

    def get_morale_reject(self):
        table = {1: 5, 2: 7, 3: 9, 4: 11, 5: 13}
        return table.get(self.day, 13)

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
        self.day = data.get("day", 1)
        self.player.food = data.get("food", 50)
        self.player.water = data.get("water", 50)
        self.player.medicine = data.get("medicine", 20)
        self.player.gold = data.get("gold", 100)
        self.player.happiness = data.get("happiness", 70)
        self.doculog = data.get("doculog", [])
        self.day_summaries = data.get("day_summaries", [])
        self.start_happiness = data.get("start_happiness", 70)
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
        missing = []
        for resource, amount in zip(npc.resources, npc.amounts):
            if getattr(self.player, resource) < amount:
                missing.append(f"{amount} {resource}")
        return len(missing) == 0, missing

    def fulfill_request(self, npc):
        for resource, amount in zip(npc.resources, npc.amounts):
            current = getattr(self.player, resource)
            setattr(self.player, resource, current - amount)
        morale_change = self.get_morale_accept()
        self.player.happiness += morale_change
        npc.accepted = True
        npc.status = "fine"
        return morale_change

    def report_dwarf(self, npc, morale_change):
        change_str = f"**Morale {'+' if morale_change >= 0 else ''}{morale_change}**"

        if len(npc.resources) == 1:
            resource = npc.resources[0]
            if npc.accepted is True:
                if resource == "food":
                    return f"✅ {npc.name} the {npc.role}: Food is restocked. {npc.name}'s kin will get to eat tonight. {change_str}"
                elif resource == "water":
                    return f"✅ {npc.name} the {npc.role}: Water is restocked. The crops have been moistened and are able to grow a little more. {change_str}"
                elif resource == "medicine":
                    return f"✅ {npc.name} the {npc.role}: Medicine is restocked. {npc.name} breathes a sigh of relief as the injured workers' wounds can finally be taken care of. {change_str}"
                elif resource == "gold":
                    if npc.name == "Grimwald":
                        return f"✅ Grimwald the Blacksmith: The gold is handed over. 'My thanks, Don. I'll have the forges roaring by morning.' {change_str}"
                    return f"✅ {npc.name} the {npc.role}: Gold received. {change_str}"
            elif npc.status == "denied":
                if resource == "food":
                    return f"⚠️ {npc.name} the {npc.role}: The growls of their stomach are audible. Their kin and the rest of the hold will soon follow... {change_str}"
                elif resource == "water":
                    return f"⚠️ {npc.name} the {npc.role}: A drought begins to fester among the hold. The crops are withering... {change_str}"
                elif resource == "medicine":
                    return f"⚠️ {npc.name} the {npc.role}: The conditions of the sick workers worsen. The lives of your fellow-men may start dwindling... {change_str}"
                elif resource == "gold":
                    if npc.name == "Grimwald":
                        return f"⚠️ Grimwald the Blacksmith: He stares at the empty coffer. 'No gold? Then no repairs. Don't let the forges grow too cold, Don.' {change_str}"
                    return f"⚠️ {npc.name} the {npc.role}: The forges remain broken. {change_str}"
            elif npc.status == "rejected":
                if resource == "food":
                    return f"❌ {npc.name} the {npc.role}: They glare at you with resentment. They will remember you being the reason their kin will starve. {change_str}"
                elif resource == "water":
                    return f"❌ {npc.name} the {npc.role}: {npc.name} flashes a visible frown and leaves. {change_str}"
                elif resource == "medicine":
                    return f"❌ {npc.name} the {npc.role}: A grim shadow looms over {npc.name}'s face. {change_str}"
                elif resource == "gold":
                    if npc.name == "Grimwald":
                        return f"❌ Grimwald the Blacksmith: He shakes his head slowly. 'So that's how it be then, huh? I'll remember this, Don.' {change_str}"
                    return f"❌ {npc.name} the {npc.role}: They shake their head in disappointment. {change_str}"
        else:
            resource_str = " and ".join(
                f"{amount} {resource}" for resource, amount in zip(npc.resources, npc.amounts)
            )
            if npc.accepted is True:
                return f"✅ {npc.name} the {npc.role}: Received {resource_str}. They nod with gratitude. {change_str}"
            elif npc.status == "denied":
                return f"⚠️ {npc.name} the {npc.role}: Requested {resource_str}, but the hold couldn't spare it. {change_str}"
            elif npc.status == "rejected":
                return f"❌ {npc.name} the {npc.role}: Request for {resource_str} was rejected. They leave with a heavy heart. {change_str}"

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
    # Center the image using columns
    img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
    
    with img_col2:
        # Make sure the filename matches exactly what you uploaded to the assets folder
        st.image("assets/title_screen.png", use_container_width=True)
        
    st.write("") 
    
    if clickable_image("assets/start_button.png", button_text="BEGIN_MANAGEMENT"):
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

    if game.day == 4:
        st.error("⚠️ **CAVE FLOOD WARNING** ⚠️")
        st.warning(
            "Overnight, flood-water from the upper tunnels broke through an old wall. "
            "The lower mines have become flooded; The hold's supplies are scattered, and the "
            "dwarves are stretched thinner than ever.\n\n"
            "**From here on out, things will only get worse, Don.** "
            "The requests will grow heavier. The resources will grow scarcer. "
            "Every decision from this day forward could mean the difference between "
            "the hold's survival and its fall."
            "And as always, Don, Don't Dwindle."
        )
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
                morale_change = game.fulfill_request(npc)
            else:
                morale_change = -game.get_morale_deny()
                game.player.happiness += morale_change
                npc.accepted = False
                npc.status = "denied"

            entry = game.report_dwarf(npc, morale_change)
            game.doculog.append(entry)
            st.session_state.request_index += 1
            st.session_state.requests_this_day += 1
            st.rerun()

    with col_b:
        if st.button("❌ REJECT", use_container_width=True):
            morale_change = -game.get_morale_reject()
            game.player.happiness += morale_change
            npc.accepted = False
            npc.status = "rejected"

            entry = game.report_dwarf(npc, morale_change)
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

    # ============================================
    # TODAY'S DECISION STATISTICS
    # ============================================
    st.divider()
    st.subheader("--- Today's Decision Statistics ---")

    today_start = max(0, len(game.doculog) - st.session_state.requests_this_day)
    todays_entries = game.doculog[today_start:]

    accepted_count = sum(1 for e in todays_entries if e.startswith("✅"))
    denied_count = sum(1 for e in todays_entries if e.startswith("⚠️"))
    rejected_count = sum(1 for e in todays_entries if e.startswith("❌"))
    total = len(todays_entries)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Requests", total)
    col2.metric("✅ Accepted", accepted_count)
    col3.metric("⚠️ Denied", denied_count)
    col4.metric("❌ Rejected", rejected_count)

    morale_change = game.player.happiness - game.start_happiness
    if morale_change > 0:
        st.success(f"📈 Net morale change today: **+{morale_change}**")
    elif morale_change < 0:
        st.error(f"📉 Net morale change today: **{morale_change}**")
    else:
        st.info("No net morale change today.")

    st.divider()

    with st.expander("📖 Open Don's Docu-log (Today's Entries)"):
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
