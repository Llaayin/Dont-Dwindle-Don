# ============================================
# Don't Dwindle, Don! (DDD) by Aaron Jared Lee
# Resource Management Simulator
# OOP Streamlit Version
# ============================================

import streamlit as st

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Don't Dwindle, Don!",
    page_icon="⛏️",
    layout="wide"
)


# ============================================
# PLAYER CLASS
# ============================================
class Player:
    def __init__(self, name):
        self.name = name
        self.food = 50
        self.water = 50
        self.medicine = 20
        self.gold = 100
        self.happiness = 70


# ============================================
# NPC CLASS
# ============================================
class NPC:
    def __init__(self, name, request, resource, amount, role):
        self.name = name
        self.request = request
        self.resource = resource
        self.amount = amount
        self.role = role
        self.accepted = None
        self.status = "fine"


# ============================================
# GAME CLASS
# ============================================
class Game:
    def __init__(self):
        self.player = None
        self.npcs = [
            NPC("Brunhilda", "needs food for her kin.", "food", 10, "Miner"),
            NPC("Thrain", "needs water for the mushroom farm.", "water", 8, "Farmer"),
            NPC("Durin", "needs medicine for the infirmary.", "medicine", 5, "Healer"),
        ]
        self.start_happiness = 70
        self.doculog = []

    def new_game(self):
        self.player = Player("Don")
        self.doculog = []

    def report_dwarf(self, npc):
        if npc.accepted is True:
            if npc.resource == "food":
                return f"✅ {npc.name} the {npc.role}: Food is restocked. Brunhilde and her kin will get to eat tonight."
            elif npc.resource == "water":
                return f"✅ {npc.name} the {npc.role}: Water is restocked. The crops have been moistened and are able to grow a little more."
            elif npc.resource == "medicine":
                return f"✅ {npc.name} the {npc.role}: Medicine is restocked. Durin breathes a sigh of relief as the injureds workers' wounds can finally be taken care of."
        elif npc.status == "denied":
            if npc.resource == "food":
                return f"⚠️ {npc.name} the {npc.role}: The growls of her stomach are audible. Her kin and the rest of the hold will soon follow..."
            elif npc.resource == "water":
                return f"⚠️ {npc.name} the {npc.role}: A drought begins to fester among the hold. The crops are withering, soon to be followed by your brethren if more isn't procured soon..."
            elif npc.resource == "medicine":
                return f"⚠️ {npc.name} the {npc.role}: The conditions of the sick workers worsen. The lives of your fellow-men may start dwindling..."
        elif npc.status == "rejected":
            if npc.resource == "food":
                return f"❌ {npc.name} the {npc.role}: She glares at you with resentment. She will remember you being the reason her kin will starve."
            elif npc.resource == "water":
                return f"❌ {npc.name} the {npc.role}: Thrain flashes a visible frown and leaves. He mutters prayers under his breath, hoping the crops can hold out a little longer."
            elif npc.resource == "medicine":
                return f"❌ {npc.name} the {npc.role}: A grim shadow looms over his face. Durin fears for the worst as the injured workers' wounds will worsen over time."


# ============================================
# SESSION STATE INIT
# ============================================
if "game" not in st.session_state:
    st.session_state.game = Game()
    st.session_state.screen = "title"
    st.session_state.request_index = 0

game = st.session_state.game


# ============================================
# SIDEBAR — RESOURCES
# ============================================
if st.session_state.screen in ["play", "evaluation", "upgrades", "end"]:
    st.sidebar.title("⛏️ Hold Resources")
    st.sidebar.metric("🍞 Food", game.player.food)
    st.sidebar.metric("💧 Water", game.player.water)
    st.sidebar.metric("💊 Medicine", game.player.medicine)
    st.sidebar.metric("💰 Gold", game.player.gold)
    st.sidebar.metric("😊 Morale", game.player.happiness)


# ============================================
# SCREEN: TITLE
# ============================================
if st.session_state.screen == "title":
    st.title("⛏️ DON'T DWINDLE, DON!")
    st.subheader("A Dwarven Resource Management Game")
    st.divider()
    st.write("You are **Don**, leader of a dwarven hold.")
    st.write("Dwarves come to you with requests — food, water, medicine.")
    st.write("Every choice affects the hold's morale and survival.")
    st.write("")
    st.write("**Remember our motto: Don't dwindle!**")
    st.divider()

    if st.button("▶️ BEGIN MANAGEMENT", type="primary", use_container_width=True):
        game.new_game()
        st.session_state.request_index = 0
        st.session_state.screen = "play"
        st.rerun()


# ============================================
# SCREEN: PLAY (Dwarf Requests)
# ============================================
elif st.session_state.screen == "play":
    idx = st.session_state.request_index

    # If all requests handled → go to evaluation
    if idx >= len(game.npcs):
        st.session_state.screen = "evaluation"
        st.rerun()

    npc = game.npcs[idx]

    st.title("📜 Dwarf Request")
    st.divider()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"### 🧔 {npc.name}")
        st.caption(f"*{npc.role}*")
    with col2:
        st.markdown(f"**{npc.name}** {npc.request}")
        st.markdown(f"**Requested:** {npc.amount} {npc.resource}")

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("✅ ACCEPT", use_container_width=True, type="primary"):
            current = getattr(game.player, npc.resource)
            if current >= npc.amount:
                setattr(game.player, npc.resource, current - npc.amount)
                game.player.happiness += 5
                npc.accepted = True
                npc.status = "fine"
            else:
                npc.accepted = False
                npc.status = "denied"
                game.player.happiness -= 5

            entry = game.report_dwarf(npc)
            game.doculog.append(entry)
            st.session_state.request_index += 1
            st.rerun()

    with col_b:
        if st.button("❌ REJECT", use_container_width=True):
            game.player.happiness -= 5
            npc.accepted = False
            npc.status = "rejected"

            entry = game.report_dwarf(npc)
            game.doculog.append(entry)
            st.session_state.request_index += 1
            st.rerun()

    # Show Don's DocuLog so far
    if game.doculog:
        st.divider()
        st.subheader("📖 Don's Docu-log")
        for entry in game.doculog:
            st.write(entry)


# ============================================
# SCREEN: EVALUATION
# ============================================
elif st.session_state.screen == "evaluation":
    st.title("🌙 END OF DAY 1")
    st.divider()

    st.subheader("--- Hold Evaluation ---")

    # Overall status
    if game.player.happiness >= 70:
        status = "THRIVING"
        mood = "The hold hums with song and the clanging of hammers."
    elif game.player.happiness >= 50:
        status = "STABLE"
        mood = "The hold endures, though whispers of worry echo throughout the tunnels."
    else:
        status = "STRUGGLING"
        mood = "The hold is grim. Dwarves mutter among themselves, unsure of whether they'll live to see tomorrow."

    st.markdown(f"### Hold Status: **{status}**")
    st.write(mood)

    st.divider()
    st.subheader("--- Day's Outcome ---")
    if game.player.happiness > game.start_happiness:
        st.success("🌟 The hold's spirit has risen today. The dwarves work with renewed vigor, their bellies full and their hearts light. Don's leadership has not gone unnoticed.")
    elif game.player.happiness < game.start_happiness:
        st.error("💀 The hold's morale has fallen. Grumbles echo through the tunnels, and the dwarves' gaze fall on Don with doubt. A shadow hangs over the hold.")
    else:
        st.info("⚖️ The hold remains unchanged. Neither joy nor sorrow stirs the tunnels tonight.")

    # ============================================
    # NEW: MORALE-BASED GOLD INCOME
    # ============================================
    st.divider()
    st.subheader("💰 Hold Income")

    morale = game.player.happiness
    if morale >= 90:
        income = 40
        income_msg = "The mines roar with activity. Every dwarf works with purpose."
    elif morale >= 70:
        income = 30
        income_msg = "The forges burn bright. The hold produces steadily."
    elif morale >= 50:
        income = 20
        income_msg = "Work continues, though at a measured pace."
    elif morale >= 30:
        income = 10
        income_msg = "Few hammers fall. The hold's output is thin."
    elif morale >= 10:
        income = 0
        income_msg = "The mines sit silent. No gold is produced today."
    else:
        income = -10
        income_msg = "Desertion and disrepair cost the hold gold."

    game.player.gold += income
    game.gold_income = income  # store for display later

    st.write(income_msg)

    if income > 0:
        st.success(f"💰 Gold gained: **+{income}**")
    elif income < 0:
        st.error(f"💸 Gold lost: **{income}**")
    else:
        st.warning("No change in gold.")

    # ============================================
    # HOLDOUT LOOKOUT WARNINGS
    # ============================================
    st.divider()
    st.subheader("--- Hold Outlook ---")
    warnings = []
    if game.player.food < 20:
        warnings.append("🍞 The granaries run low. Hunger stalks the tunnels.")
    if game.player.water < 20:
        warnings.append("💧 The wells are dry. The mushroom farms wither.")
    if game.player.medicine < 10:
        warnings.append("💊 The infirmary lacks supplies. Disease begins to spread in the mines.")
    if game.player.happiness < 40:
        warnings.append("😟 Morale is broken. Some dwarves speak of leaving the hold.")

    if warnings:
        for w in warnings:
            st.warning(w)
    else:
        st.write("No critical warnings today.")

    st.divider()
    st.write("**Remember not to dwindle, Don. The hold has no time for mistakes.**")

    if st.button("▶️ GO TO FORGE & MARKET", type="primary", use_container_width=True):
        st.session_state.screen = "upgrades"
        st.rerun()


# ============================================
# SCREEN: UPGRADES (Forge & Market)
# ============================================
elif st.session_state.screen == "upgrades":
    st.title("🔨 FORGE & MARKET")
    st.divider()

    st.markdown(f"### Gold: 💰 {game.player.gold}")
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🍞 Food Upgrade")
        st.write("Increase Food +10")
        st.write("**Cost:** 50 Gold")
        if st.button("Buy Food +10", use_container_width=True, disabled=game.player.gold < 50):
            game.player.food += 10
            game.player.gold -= 50
            st.success("Food stores increased!")
            st.rerun()

    with col2:
        st.markdown("### 💧 Water Upgrade")
        st.write("Increase Water +10")
        st.write("**Cost:** 50 Gold")
        if st.button("Buy Water +10", use_container_width=True, disabled=game.player.gold < 50):
            game.player.water += 10
            game.player.gold -= 50
            st.success("Water stores increased!")
            st.rerun()

    with col3:
        st.markdown("### ⏭️ Skip")
        st.write("Leave without buying")
        st.write("&nbsp;")
        if st.button("Skip", use_container_width=True):
            st.session_state.screen = "end"
            st.rerun()

    st.divider()
    if st.button("▶️ CONTINUE TO NEXT DAY", use_container_width=True, type="primary"):
        st.session_state.screen = "end"
        st.rerun()


# ============================================
# SCREEN: END
# ============================================
elif st.session_state.screen == "end":
    st.title("🌅 A NEW DAWN BREAKS")
    st.divider()

    st.write("Thank you for playing **Don't Dwindle, Don!**")
    st.write("This is the end of the prototype.")
    st.write("")

    if st.button("🔁 PLAY AGAIN", use_container_width=True, type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
