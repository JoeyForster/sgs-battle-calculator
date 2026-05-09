const STORAGE_KEY = "sgs-turn-calculator-state-v3";
const ASSET_VERSION = "icons-20260508";

const statLabels = {
  currentHealth: "Current Health",
  maximumHealth: "Maximum Health",
  stackingValue: "Stacking Value",
  attackFactor: "Attack Factor",
  defenseFactor: "Defense Factor",
  moraleFactor: "Morale Factor",
  rateOfFire: "Rate of Fire",
  battleMorale: "Battle Morale",
  combatFactor: "Combat Factor",
  victoryPoints: "Victory Points",
};

const iconBase = "/static/icons";

const countryIcons = {
  albania: "flags/albania.svg",
  "austria-hungary": "flags/austria-hungary.svg",
  "austria hungary": "flags/austria-hungary.svg",
  bulgaria: "flags/bulgaria.svg",
  commonwealth: "flags/commonwealth.svg",
  finland: "flags/finland.svg",
  france: "flags/france.svg",
  germany: "flags/germany.svg",
  "german east africa": "flags/german-east-africa.svg",
  italy: "flags/italy.svg",
  japan: "flags/japan.svg",
  mexico: "flags/mexico.svg",
  romania: "flags/romania.svg",
  russia: "flags/russia.svg",
  serbia: "flags/serbia.svg",
  "soviet union": "flags/soviet-union.svg",
  turkey: "flags/turkey.svg",
  "ottoman empire": "flags/turkey.svg",
  "united kingdom": "flags/united-kingdom.svg",
  "british empire": "flags/british-empire.svg",
  "united states": "flags/united-states.svg",
  "united states of america": "flags/united-states.svg",
  usa: "flags/united-states.svg",
  us: "flags/united-states.svg",
  uk: "flags/united-kingdom.svg",
};

const unitTypeIcons = {
  standard: "units/standard.svg",
  armor: "units/armor.svg",
  artillery: "units/artillery.svg",
  mine: "units/mine.svg",
  fighter: "units/fighter.svg",
  bomber: "units/bomber.svg",
  cas: "units/cas.svg",
  cavalry: "units/cavalry.svg",
  mechanized: "units/mechanized.svg",
  support: "units/support.svg",
};

const traitIcons = {
  air: "traits/air.svg",
  air_support: "traits/air.svg",
  ambush: "traits/ambush.svg",
  anti_air: "traits/anti-air.svg",
  armor: "traits/armor.svg",
  artillery: "traits/artillery.svg",
  breakthrough: "traits/breakthrough.svg",
  cavalry: "traits/cavalry.svg",
  cav: "traits/cavalry.svg",
  dive_bomber: "traits/land-attack.svg",
  elite: "traits/elite.svg",
  fighter_bomber: "traits/land-attack.svg",
  fortification: "traits/fortification.svg",
  infantry: "traits/infantry.svg",
  land_attack: "traits/land-attack.svg",
  mechanized: "traits/mechanized.svg",
  mechanised: "traits/mechanized.svg",
  mine: "traits/minefield.svg",
  minefield: "traits/minefield.svg",
  pursuit: "traits/pursuit.svg",
  recon: "traits/recon.svg",
  reconnaissance: "traits/recon.svg",
};

const traitLabels = {
  air: "Air",
  air_support: "Air Support",
  ambush: "Ambush",
  anti_air: "Anti-Air",
  armor: "Armor",
  artillery: "Artillery",
  breakthrough: "Breakthrough",
  cavalry: "Cavalry",
  cav: "Cavalry",
  dive_bomber: "Dive Bomber",
  elite: "Elite",
  fighter_bomber: "Fighter Bomber",
  fortification: "Fortification",
  infantry: "Infantry",
  land_attack: "Land Attack",
  mechanized: "Mechanized",
  mechanised: "Mechanized",
  mine: "Mine",
  minefield: "Minefield",
  pursuit: "Pursuer",
  recon: "Recon",
  reconnaissance: "Reconnaissance",
};

const terrainPresets = [
  {
    id: "clear",
    name: "Clear",
    description: "Open ground with no combat adjustment.",
    attackerCombat: 0,
    defenderCombat: 0,
    attackerMorale: 0,
    defenderMorale: 0,
    pursuitAllowed: true,
    breakthroughAllowed: true,
  },
  {
    id: "forest",
    name: "Forest",
    description: "Tighter terrain favoring defense and limiting armored exploitation.",
    attackerCombat: -1,
    defenderCombat: 1,
    attackerMorale: 0,
    defenderMorale: 1,
    pursuitAllowed: false,
    breakthroughAllowed: false,
  },
  {
    id: "hills",
    name: "Hills",
    description: "Attacker penalty with a modest defender edge.",
    attackerCombat: -1,
    defenderCombat: 1,
    attackerMorale: 0,
    defenderMorale: 0,
    pursuitAllowed: false,
    breakthroughAllowed: false,
  },
  {
    id: "marsh",
    name: "Marsh",
    description: "Difficult ground with morale benefit for defenders.",
    attackerCombat: -1,
    defenderCombat: 1,
    attackerMorale: 0,
    defenderMorale: 1,
    pursuitAllowed: false,
    breakthroughAllowed: false,
  },
  {
    id: "desert",
    name: "Desert",
    description: "Sparse ground with no defensive cover.",
    attackerCombat: 0,
    defenderCombat: 0,
    attackerMorale: 0,
    defenderMorale: 0,
    pursuitAllowed: true,
    breakthroughAllowed: true,
  },
  {
    id: "fortified",
    name: "Fortified",
    description: "Prepared position, strong defender modifier.",
    attackerCombat: -1,
    defenderCombat: 2,
    attackerMorale: 0,
    defenderMorale: 1,
    pursuitAllowed: false,
    breakthroughAllowed: false,
    entrenched: true,
  },
];

const cardPresets = [
  {
    id: "prepared-assault",
    name: "Prepared Assault",
    side: "attacker",
    description: "+1 attack in Main and Phase rounds.",
    modifier: { attack: 1, rounds: ["main", "next"] },
  },
  {
    id: "defensive-fire",
    name: "Defensive Fire",
    side: "defender",
    description: "+1 defense in Main and Phase rounds.",
    modifier: { defense: 1, rounds: ["main", "next"] },
  },
  {
    id: "artillery-barrage",
    name: "Artillery Barrage",
    side: "attacker",
    description: "+1 artillery preparation fire.",
    modifier: { attack: 1, rounds: ["artillery"] },
  },
  {
    id: "ambush",
    name: "Ambush",
    side: "defender",
    description: "+1 defense for recon/main contact.",
    modifier: { defense: 1, rounds: ["recon", "main"] },
  },
  {
    id: "morale-boost",
    name: "Morale Boost",
    side: "both",
    description: "+1 battle morale.",
    modifier: { morale: 1, rounds: [] },
  },
  {
    id: "air-cover",
    name: "Air Cover",
    side: "both",
    description: "+1 air support fire.",
    battlePatch: { air_modifier: 1 },
  },
];

const glossaryTerms = [
  ["Current Health", "The unit's current remaining strength or hit points. Units at zero are removed when losses are applied."],
  ["Maximum Health", "The unit's full strength or hit point value before battle damage."],
  ["Stacking Value", "How much room the unit occupies in a region or stack. The calculator tracks it for reference."],
  ["Attack Factor", "The combat factor used when this unit fires as an attacker."],
  ["Defense Factor", "The combat factor used when this unit fires as a defender."],
  ["Morale Factor", "The unit morale value used in Battle Morale and panic checks."],
  ["Rate of Fire", "The number of shots a unit makes when eligible to fire in a battle round."],
  ["Battle Morale", "A side's staying power in battle, built from average unit morale, leaders, armor, air, terrain, cards, and boosters."],
  ["Combat Factor", "The final shot target after attack or defense value plus battle modifiers."],
  ["Armor Superiority", "An extra battle bonus when one side has at least twice the opponent's armor units and at least two armor units."],
  ["Elite", "A unit trait that lets a unit reroll its first failed shot."],
  ["Pursuer", "A unit trait that allows pursuit fire after an enemy rout if terrain permits."],
  ["Breakthrough", "A post-battle movement opportunity for eligible victorious attackers if the scenario and terrain allow it."],
  ["Entrenched Defender", "A prepared defending stack. Attackers suffer a combat penalty against it."],
  ["Loss Priority", "Whether the combat engine should assign hits to a unit early, normally, or late."],
  ["Victory Points", "Campaign score awarded here when you apply a battle result at end of turn."],
];

const scenarioPresets = [
  {
    id: "afrika-korps",
    name: "SGS Afrika Korps",
    scenarioName: "SGS Afrika Korps",
    attackerName: "Axis",
    defenderName: "Commonwealth",
    battleName: "Sidi Barrani",
    seed: 1941,
    selectedTerrainId: "desert",
    units: [
      unit({ id: "ak-axis-ari", side: "attacker", name: "132 Ariete Tank Brigade", country: "Italy", type: "armor", attack: 5, defense: 4, morale: 4, strength: 4, maxStrength: 4, traits: ["armor", "pursuit", "breakthrough"] }),
      unit({ id: "ak-axis-panzer", side: "attacker", name: "15th Panzer Regiment", country: "Germany", type: "armor", attack: 6, defense: 5, morale: 5, strength: 5, maxStrength: 5, rof: 2, traits: ["armor", "elite", "pursuit", "breakthrough"] }),
      unit({ id: "ak-axis-guns", side: "attacker", name: "88mm Artillery Detachment", country: "Germany", role: "support", type: "artillery", attack: 5, defense: 2, morale: 4, strength: 2, maxStrength: 2, traits: ["artillery"], lossPriority: "last" }),
      unit({ id: "ak-axis-stuka", side: "attacker", name: "Stuka Close Air Support Group", country: "Germany", domain: "air", type: "cas", attack: 5, defense: 3, morale: 4, strength: 2, maxStrength: 2, traits: ["air", "air_support", "dive_bomber", "land_attack"] }),
      unit({ id: "ak-cw-matilda", side: "defender", name: "Matilda Squadron", country: "United Kingdom", type: "armor", attack: 4, defense: 5, morale: 5, strength: 3, maxStrength: 3, traits: ["armor", "pursuit"] }),
      unit({ id: "ak-cw-armoured", side: "defender", name: "7th Armoured Brigade", country: "United Kingdom", type: "armor", attack: 4, defense: 5, morale: 4, strength: 4, maxStrength: 4, traits: ["armor", "pursuit"] }),
      unit({ id: "ak-cw-indian", side: "defender", name: "4th Indian Brigade", country: "United Kingdom", attack: 3, defense: 4, morale: 4, strength: 5, maxStrength: 5, traits: ["infantry"] }),
      unit({ id: "ak-cw-mine", side: "defender", name: "Minefield Screen", country: "Commonwealth", role: "support", type: "mine", attack: 4, defense: 4, morale: 2, strength: 2, maxStrength: 2, traits: ["mine", "minefield"], lossPriority: "first" }),
    ],
    attackerStack: ["ak-axis-ari", "ak-axis-panzer"],
    defenderStack: ["ak-cw-matilda", "ak-cw-indian"],
  },
  {
    id: "afrika-korps-tunisia",
    name: "SGS Afrika Korps: Tunisia",
    scenarioName: "SGS Afrika Korps: Tunisia",
    attackerName: "Axis",
    defenderName: "Allies",
    battleName: "Kasserine Pass",
    seed: 1943,
    selectedTerrainId: "hills",
    units: [
      unit({ id: "tun-axis-panzer", side: "attacker", name: "10th Panzer Kampfgruppe", country: "Germany", type: "armor", attack: 6, defense: 5, morale: 5, strength: 5, maxStrength: 5, traits: ["armor", "elite", "pursuit", "breakthrough"] }),
      unit({ id: "tun-axis-gren", side: "attacker", name: "Panzergrenadier Regiment", country: "Germany", attack: 4, defense: 4, morale: 4, strength: 4, maxStrength: 4, traits: ["mechanized", "pursuit"] }),
      unit({ id: "tun-axis-flak", side: "attacker", name: "Flak Artillery Battery", country: "Germany", role: "support", type: "artillery", attack: 5, defense: 3, morale: 4, strength: 2, maxStrength: 2, traits: ["artillery"], lossPriority: "last" }),
      unit({ id: "tun-allies-armored", side: "defender", name: "US Armored Combat Command", country: "United States", type: "armor", attack: 4, defense: 4, morale: 3, strength: 5, maxStrength: 5, traits: ["armor", "pursuit"] }),
      unit({ id: "tun-allies-infantry", side: "defender", name: "US Infantry Regiment", country: "United States", attack: 3, defense: 4, morale: 3, strength: 5, maxStrength: 5, traits: ["infantry"] }),
      unit({ id: "tun-allies-guns", side: "defender", name: "Field Artillery Battalion", country: "United States", role: "support", type: "artillery", attack: 4, defense: 3, morale: 3, strength: 2, maxStrength: 2, traits: ["artillery"], lossPriority: "last" }),
    ],
    attackerStack: ["tun-axis-panzer", "tun-axis-gren"],
    defenderStack: ["tun-allies-armored", "tun-allies-infantry"],
  },
  {
    id: "winter-war",
    name: "SGS Winter War",
    scenarioName: "SGS Winter War",
    attackerName: "Soviet Union",
    defenderName: "Finland",
    battleName: "Karelian Isthmus",
    seed: 1939,
    selectedTerrainId: "forest",
    units: [
      unit({ id: "ww-sov-rifle", side: "attacker", name: "Soviet Rifle Division", country: "Soviet Union", attack: 4, defense: 3, morale: 3, strength: 6, maxStrength: 6, rof: 2, traits: ["infantry"] }),
      unit({ id: "ww-sov-tank", side: "attacker", name: "Soviet Tank Brigade", country: "Soviet Union", type: "armor", attack: 5, defense: 4, morale: 3, strength: 4, maxStrength: 4, traits: ["armor", "pursuit"] }),
      unit({ id: "ww-sov-art", side: "attacker", name: "Soviet Artillery Group", country: "Soviet Union", role: "support", type: "artillery", attack: 5, defense: 2, morale: 3, strength: 3, maxStrength: 3, traits: ["artillery"], lossPriority: "last" }),
      unit({ id: "ww-fin-ski", side: "defender", name: "Finnish Ski Battalion", country: "Finland", attack: 4, defense: 5, morale: 5, strength: 3, maxStrength: 3, traits: ["infantry", "elite", "pursuit", "breakthrough"] }),
      unit({ id: "ww-fin-infantry", side: "defender", name: "Finnish Infantry Regiment", country: "Finland", attack: 3, defense: 5, morale: 5, strength: 4, maxStrength: 4, traits: ["infantry", "elite"] }),
      unit({ id: "ww-fin-mine", side: "defender", name: "Motti Ambush Screen", country: "Finland", role: "support", type: "mine", attack: 4, defense: 4, morale: 4, strength: 2, maxStrength: 2, traits: ["mine", "minefield", "ambush"], lossPriority: "first" }),
    ],
    attackerStack: ["ww-sov-rifle", "ww-sov-tank"],
    defenderStack: ["ww-fin-ski", "ww-fin-infantry"],
  },
  {
    id: "halls-montezuma",
    name: "SGS Halls of Montezuma",
    scenarioName: "SGS Halls of Montezuma",
    attackerName: "United States",
    defenderName: "Mexico",
    battleName: "Chapultepec",
    seed: 1847,
    selectedTerrainId: "fortified",
    units: [
      unit({ id: "hm-us-regulars", side: "attacker", name: "US Regular Infantry Brigade", country: "United States", attack: 4, defense: 4, morale: 4, strength: 5, maxStrength: 5, traits: ["infantry"] }),
      unit({ id: "hm-us-marines", side: "attacker", name: "US Marine Detachment", country: "United States", attack: 4, defense: 4, morale: 5, strength: 3, maxStrength: 3, traits: ["infantry", "elite"] }),
      unit({ id: "hm-us-art", side: "attacker", name: "Siege Artillery Battery", country: "United States", role: "support", type: "artillery", attack: 5, defense: 2, morale: 4, strength: 2, maxStrength: 2, traits: ["artillery"], lossPriority: "last" }),
      unit({ id: "hm-mx-line", side: "defender", name: "Mexican Line Infantry Brigade", country: "Mexico", attack: 3, defense: 4, morale: 4, strength: 5, maxStrength: 5, traits: ["infantry"] }),
      unit({ id: "hm-mx-cadets", side: "defender", name: "Military Academy Cadets", country: "Mexico", attack: 3, defense: 5, morale: 5, strength: 2, maxStrength: 2, traits: ["infantry", "elite"] }),
      unit({ id: "hm-mx-fort", side: "defender", name: "Fortified Guns", country: "Mexico", role: "support", type: "artillery", attack: 4, defense: 5, morale: 4, strength: 3, maxStrength: 3, traits: ["artillery", "fortification"], lossPriority: "last" }),
    ],
    attackerStack: ["hm-us-regulars", "hm-us-marines"],
    defenderStack: ["hm-mx-line", "hm-mx-cadets", "hm-mx-fort"],
  },
  {
    id: "heia-safari",
    name: "SGS Heia Safari",
    scenarioName: "SGS Heia Safari",
    attackerName: "German East Africa",
    defenderName: "British Empire",
    battleName: "East African Campaign",
    seed: 1916,
    selectedTerrainId: "forest",
    units: [
      unit({ id: "hs-ge-askari", side: "attacker", name: "Schutztruppe Askari Company", country: "German East Africa", attack: 4, defense: 4, morale: 5, strength: 3, maxStrength: 3, traits: ["infantry", "elite", "pursuit"] }),
      unit({ id: "hs-ge-raider", side: "attacker", name: "Field Raider Detachment", country: "German East Africa", attack: 4, defense: 3, morale: 5, strength: 2, maxStrength: 2, traits: ["infantry", "recon", "pursuit"] }),
      unit({ id: "hs-ge-guns", side: "attacker", name: "Light Gun Section", country: "German East Africa", role: "support", type: "artillery", attack: 3, defense: 2, morale: 4, strength: 1, maxStrength: 1, traits: ["artillery"], lossPriority: "last" }),
      unit({ id: "hs-uk-kar", side: "defender", name: "King's African Rifles Battalion", country: "British Empire", attack: 3, defense: 4, morale: 4, strength: 4, maxStrength: 4, traits: ["infantry"] }),
      unit({ id: "hs-uk-sa", side: "defender", name: "South African Mounted Column", country: "British Empire", attack: 4, defense: 3, morale: 4, strength: 3, maxStrength: 3, traits: ["cavalry", "pursuit"] }),
      unit({ id: "hs-uk-guns", side: "defender", name: "Imperial Field Artillery", country: "British Empire", role: "support", type: "artillery", attack: 4, defense: 2, morale: 3, strength: 2, maxStrength: 2, traits: ["artillery"], lossPriority: "last" }),
    ],
    attackerStack: ["hs-ge-askari", "hs-ge-raider"],
    defenderStack: ["hs-uk-kar", "hs-uk-sa"],
  },
  {
    id: "operation-hawaii",
    name: "SGS Operation Hawaii",
    scenarioName: "SGS Operation Hawaii",
    attackerName: "Imperial Japan",
    defenderName: "United States",
    battleName: "Oahu",
    seed: 1942,
    selectedTerrainId: "clear",
    units: [
      unit({ id: "oh-jp-snlF", side: "attacker", name: "Special Naval Landing Force", country: "Japan", attack: 5, defense: 4, morale: 5, strength: 4, maxStrength: 4, traits: ["infantry", "elite", "breakthrough"] }),
      unit({ id: "oh-jp-infantry", side: "attacker", name: "Japanese Infantry Regiment", country: "Japan", attack: 4, defense: 4, morale: 4, strength: 5, maxStrength: 5, traits: ["infantry"] }),
      unit({ id: "oh-jp-cas", side: "attacker", name: "Carrier Close Air Support", country: "Japan", domain: "air", type: "cas", attack: 5, defense: 3, morale: 4, strength: 2, maxStrength: 2, traits: ["air", "air_support", "land_attack"] }),
      unit({ id: "oh-us-marines", side: "defender", name: "US Marine Defense Battalion", country: "United States", attack: 4, defense: 5, morale: 5, strength: 4, maxStrength: 4, traits: ["infantry", "elite"] }),
      unit({ id: "oh-us-army", side: "defender", name: "US Army Infantry Regiment", country: "United States", attack: 3, defense: 4, morale: 4, strength: 5, maxStrength: 5, traits: ["infantry"] }),
      unit({ id: "oh-us-aa", side: "defender", name: "Coastal Anti-Aircraft Battery", country: "United States", role: "support", type: "artillery", attack: 3, defense: 4, morale: 4, strength: 2, maxStrength: 2, traits: ["artillery", "anti_air"], lossPriority: "last" }),
    ],
    attackerStack: ["oh-jp-snlF", "oh-jp-infantry"],
    defenderStack: ["oh-us-marines", "oh-us-army"],
  },
];

const els = {
  scenarioPreset: document.querySelector("#scenarioPreset"),
  loadPreset: document.querySelector("#loadPreset"),
  scenarioName: document.querySelector("#scenarioName"),
  turnNumber: document.querySelector("#turnNumber"),
  targetVp: document.querySelector("#targetVp"),
  themeToggle: document.querySelector("#themeToggle"),
  attackerLabel: document.querySelector("#attackerLabel"),
  defenderLabel: document.querySelector("#defenderLabel"),
  attackerVp: document.querySelector("#attackerVp"),
  defenderVp: document.querySelector("#defenderVp"),
  sideAttackerLabel: document.querySelector("#sideAttackerLabel"),
  sideDefenderLabel: document.querySelector("#sideDefenderLabel"),
  unitForm: document.querySelector("#unitForm"),
  unitSearch: document.querySelector("#unitSearch"),
  unitSideFilter: document.querySelector("#unitSideFilter"),
  unitLibrary: document.querySelector("#unitLibrary"),
  libraryCount: document.querySelector("#libraryCount"),
  saveState: document.querySelector("#saveState"),
  resetState: document.querySelector("#resetState"),
  battleName: document.querySelector("#battleName"),
  seed: document.querySelector("#seed"),
  provinceSize: document.querySelector("#provinceSize"),
  attackerName: document.querySelector("#attackerName"),
  defenderName: document.querySelector("#defenderName"),
  maxNextRounds: document.querySelector("#maxNextRounds"),
  defenderEntrenched: document.querySelector("#defenderEntrenched"),
  attackerBmPreview: document.querySelector("#attackerBmPreview"),
  defenderBmPreview: document.querySelector("#defenderBmPreview"),
  attackerStackTitle: document.querySelector("#attackerStackTitle"),
  defenderStackTitle: document.querySelector("#defenderStackTitle"),
  attackerStack: document.querySelector("#attackerStack"),
  defenderStack: document.querySelector("#defenderStack"),
  clearAttackers: document.querySelector("#clearAttackers"),
  clearDefenders: document.querySelector("#clearDefenders"),
  runBattle: document.querySelector("#runBattle"),
  applyTurn: document.querySelector("#applyTurn"),
  exportJson: document.querySelector("#exportJson"),
  resultStatus: document.querySelector("#resultStatus"),
  battleSummary: document.querySelector("#battleSummary"),
  roundTimeline: document.querySelector("#roundTimeline"),
  selectedTerrainLabel: document.querySelector("#selectedTerrainLabel"),
  terrainSearch: document.querySelector("#terrainSearch"),
  terrainList: document.querySelector("#terrainList"),
  cardSearch: document.querySelector("#cardSearch"),
  cardList: document.querySelector("#cardList"),
  activeCardCount: document.querySelector("#activeCardCount"),
  activeCards: document.querySelector("#activeCards"),
  glossarySearch: document.querySelector("#glossarySearch"),
  glossaryList: document.querySelector("#glossaryList"),
  jsonDialog: document.querySelector("#jsonDialog"),
  jsonPreview: document.querySelector("#jsonPreview"),
  closeJson: document.querySelector("#closeJson"),
};

let state = loadState();
let lastReport = null;
let lastPayload = null;

wireEvents();
renderAll();

function defaultState() {
  const preset = presetState("afrika-korps");
  return {
    ...preset,
    scenarioPresetId: "afrika-korps",
    theme: "dark",
    activeToolTab: "terrain",
    turnNumber: 1,
    targetVp: 5,
    attackerVp: 0,
    defenderVp: 0,
    provinceSize: 0,
    maxNextRounds: 3,
    defenderEntrenched: false,
    activeCards: [],
    lastOutcome: null,
  };
}

function starterUnits() {
  return presetState("afrika-korps").units;
}

function unit(overrides) {
  return {
    id: crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`,
    side: "attacker",
    name: "Unit",
    country: "",
    domain: "land",
    role: "combat",
    type: "standard",
    attack: 3,
    defense: 3,
    morale: 3,
    strength: 3,
    maxStrength: 3,
    stacking: 1,
    rof: 1,
    traits: ["infantry"],
    lossPriority: "normal",
    ...overrides,
  };
}

function presetState(id) {
  const preset = scenarioPresets.find((item) => item.id === id) || scenarioPresets[0];
  return {
    scenarioName: preset.scenarioName,
    attackerName: preset.attackerName,
    defenderName: preset.defenderName,
    battleName: preset.battleName,
    seed: preset.seed,
    selectedTerrainId: preset.selectedTerrainId,
    units: cloneUnits(preset.units),
    attackerStack: [...preset.attackerStack],
    defenderStack: [...preset.defenderStack],
  };
}

function cloneUnits(units) {
  return units.map((item) => ({
    ...item,
    traits: [...item.traits],
  }));
}

function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return defaultState();
  try {
    return { ...defaultState(), ...JSON.parse(raw) };
  } catch {
    return defaultState();
  }
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function wireEvents() {
  els.loadPreset.addEventListener("click", loadSelectedPreset);
  els.scenarioPreset.addEventListener("change", () => {
    state.scenarioPresetId = els.scenarioPreset.value;
    saveState();
  });
  els.themeToggle.addEventListener("click", () => {
    state.theme = state.theme === "dark" ? "light" : "dark";
    applyTheme();
    saveState();
  });
  document.querySelectorAll("[data-tool-tab]").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeToolTab = button.dataset.toolTab;
      saveState();
      renderToolTabs();
    });
  });
  [
    "scenarioName",
    "turnNumber",
    "targetVp",
    "battleName",
    "seed",
    "provinceSize",
    "attackerName",
    "defenderName",
    "maxNextRounds",
  ].forEach((id) => {
    els[id].addEventListener("input", () => {
      state[id] = valueFromInput(els[id]);
      saveState();
      renderAll();
    });
  });

  els.defenderEntrenched.addEventListener("change", () => {
    state.defenderEntrenched = els.defenderEntrenched.checked;
    saveState();
    renderAll();
  });

  els.unitForm.addEventListener("submit", addUnitFromForm);
  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-action]");
    if (!button) return;
    handleAction(button.dataset.action, button.dataset.id);
  });
  els.unitSearch.addEventListener("input", renderLibrary);
  els.unitSideFilter.addEventListener("change", renderLibrary);
  els.terrainSearch.addEventListener("input", renderTerrain);
  els.cardSearch.addEventListener("input", renderCards);
  els.glossarySearch.addEventListener("input", renderGlossary);
  els.clearAttackers.addEventListener("click", () => clearStack("attacker"));
  els.clearDefenders.addEventListener("click", () => clearStack("defender"));
  els.runBattle.addEventListener("click", runBattle);
  els.applyTurn.addEventListener("click", applyTurn);
  els.exportJson.addEventListener("click", showJson);
  els.closeJson.addEventListener("click", () => els.jsonDialog.close());
  els.saveState.addEventListener("click", () => {
    saveState();
    flashStatus("Saved current campaign state.");
  });
  els.resetState.addEventListener("click", () => {
    if (!confirm("Reset the calculator state?")) return;
    state = defaultState();
    lastReport = null;
    lastPayload = null;
    saveState();
    renderAll();
  });
}

function renderAll() {
  applyTheme();
  renderPresetSelect();
  syncFormValues();
  renderScoreboard();
  renderLibrary();
  renderStacks();
  renderTerrain();
  renderCards();
  renderActiveCards();
  renderGlossary();
  renderToolTabs();
  updateBmPreview();
}

function applyTheme() {
  document.body.dataset.theme = state.theme || "dark";
  els.themeToggle.textContent = state.theme === "dark" ? "Light Mode" : "Dark Mode";
}

function renderPresetSelect() {
  els.scenarioPreset.innerHTML = scenarioPresets
    .map((preset) => `<option value="${preset.id}">${escapeHtml(preset.name)}</option>`)
    .join("");
  els.scenarioPreset.value = state.scenarioPresetId || "afrika-korps";
}

function loadSelectedPreset() {
  const id = els.scenarioPreset.value;
  if (!confirm("Load this scenario preset and replace the current unit library and battlefield?")) return;
  const preset = presetState(id);
  state = {
    ...state,
    ...preset,
    scenarioPresetId: id,
    attackerVp: 0,
    defenderVp: 0,
    turnNumber: 1,
    activeCards: [],
    lastOutcome: null,
  };
  lastReport = null;
  lastPayload = null;
  saveState();
  renderAll();
  flashStatus(`Loaded ${scenarioPresets.find((item) => item.id === id).name}.`);
}

function renderToolTabs() {
  const active = state.activeToolTab || "terrain";
  document.querySelectorAll("[data-tool-tab]").forEach((button) => {
    button.classList.toggle("selected", button.dataset.toolTab === active);
  });
  document.querySelectorAll("[data-tool-panel]").forEach((panel) => {
    panel.hidden = panel.dataset.toolPanel !== active;
  });
}

function renderGlossary() {
  const query = els.glossarySearch.value.trim().toLowerCase();
  const terms = glossaryTerms.filter(([term, description]) =>
    `${term} ${description}`.toLowerCase().includes(query)
  );
  els.glossaryList.innerHTML =
    terms
      .map(
        ([term, description]) => `
          <article class="glossary-card">
            <h3>${escapeHtml(term)}</h3>
            <p>${escapeHtml(description)}</p>
          </article>
        `
      )
      .join("") || emptyState("No glossary terms match.");
}

function syncFormValues() {
  els.scenarioName.value = state.scenarioName;
  els.turnNumber.value = state.turnNumber;
  els.targetVp.value = state.targetVp;
  els.battleName.value = state.battleName;
  els.seed.value = state.seed;
  els.provinceSize.value = state.provinceSize;
  els.attackerName.value = state.attackerName;
  els.defenderName.value = state.defenderName;
  els.maxNextRounds.value = state.maxNextRounds;
  els.defenderEntrenched.checked = state.defenderEntrenched;
}

function renderScoreboard() {
  const attackerName = sideName("attacker");
  const defenderName = sideName("defender");
  els.attackerLabel.textContent = attackerName;
  els.defenderLabel.textContent = defenderName;
  els.sideAttackerLabel.textContent = attackerName;
  els.sideDefenderLabel.textContent = defenderName;
  els.attackerStackTitle.textContent = attackerName;
  els.defenderStackTitle.textContent = defenderName;
  els.attackerVp.textContent = state.attackerVp;
  els.defenderVp.textContent = state.defenderVp;
}

function renderLibrary() {
  const query = els.unitSearch.value.trim().toLowerCase();
  const sideFilter = els.unitSideFilter.value;
  const units = state.units.filter((item) => {
    const matchesQuery = [item.name, item.country, item.type, item.traits.join(" ")]
      .join(" ")
      .toLowerCase()
      .includes(query);
    const matchesSide = sideFilter === "all" || item.side === sideFilter;
    return matchesQuery && matchesSide;
  });
  els.libraryCount.textContent = `${state.units.length} unit${state.units.length === 1 ? "" : "s"}`;
  els.unitLibrary.innerHTML = units.map(renderLibraryUnit).join("") || emptyState("No units match.");
}

function renderLibraryUnit(item) {
  const inAttack = state.attackerStack.includes(item.id);
  const inDefense = state.defenderStack.includes(item.id);
  return `
    <article class="unit-card ${item.side}">
      <div class="unit-card-main">
        ${flagIcon(item)}
        <div>
          <h3>${escapeHtml(item.name)}</h3>
          <p class="unit-meta">
            ${unitTypeIcon(item)}
            <span>${escapeHtml(item.country || sideName(item.side))} · ${escapeHtml(typeLabel(item))}</span>
          </p>
        </div>
      </div>
      ${healthBar(item)}
      <div class="unit-stats">
        ${statPill(statLabels.currentHealth, item.strength)}
        ${statPill(statLabels.maximumHealth, item.maxStrength)}
        ${statPill(statLabels.stackingValue, item.stacking)}
        ${statPill(statLabels.attackFactor, item.attack)}
        ${statPill(statLabels.defenseFactor, item.defense)}
        ${statPill(statLabels.moraleFactor, item.morale)}
        ${statPill(statLabels.rateOfFire, item.rof)}
      </div>
      ${renderTraitRow(item.traits)}
      <div class="unit-actions">
        <button type="button" data-action="stage-attacker" data-id="${item.id}" ${inAttack ? "disabled" : ""}>Add Attacker</button>
        <button type="button" data-action="stage-defender" data-id="${item.id}" ${inDefense ? "disabled" : ""}>Add Defender</button>
        <button type="button" data-action="heal-unit" data-id="${item.id}">Full Health</button>
        <button type="button" data-action="remove-unit" data-id="${item.id}" class="danger">Delete</button>
      </div>
    </article>
  `;
}

function renderStacks() {
  els.attackerStack.innerHTML = renderStack("attacker");
  els.defenderStack.innerHTML = renderStack("defender");
}

function renderStack(side) {
  const ids = side === "attacker" ? state.attackerStack : state.defenderStack;
  const units = ids.map(findUnit).filter(Boolean);
  if (!units.length) return emptyState(`Add ${side === "attacker" ? "attacking" : "defending"} units.`);
  return units.map((item) => {
    const preview = projectedUnitState(item, side);
    const changed = preview.projected && preview.strength !== item.strength;
    const classes = [
      "stack-card",
      side,
      preview.destroyed ? "projected-dead" : "",
      changed && !preview.destroyed ? "projected-damaged" : "",
    ].filter(Boolean).join(" ");
    return `
      <article class="${classes}">
        <div class="unit-card-main">
          ${flagIcon(item)}
          <div>
            <h3>${escapeHtml(item.name)}</h3>
            <p class="unit-meta">
              ${unitTypeIcon(item)}
              <span>${escapeHtml(typeLabel(item))} · ${escapeHtml(traitSummary(item.traits))}</span>
            </p>
          </div>
        </div>
        ${projectedStatusBadge(item, preview)}
        ${healthBar(preview)}
        <div class="unit-stats">
          ${statPill(statLabels.currentHealth, preview.strength)}
          ${statPill(statLabels.maximumHealth, preview.maxStrength)}
          ${statPill(statLabels.stackingValue, item.stacking)}
          ${statPill(statLabels.attackFactor, item.attack)}
          ${statPill(statLabels.defenseFactor, item.defense)}
          ${statPill(statLabels.moraleFactor, item.morale)}
        </div>
        <div class="unit-actions">
          <button type="button" data-action="damage-unit" data-id="${item.id}">-1 Health</button>
          <button type="button" data-action="heal-one" data-id="${item.id}">+1 Health</button>
          <button type="button" data-action="unstage-${side}" data-id="${item.id}">Remove</button>
        </div>
      </article>
    `;
  }).join("");
}

function renderTerrain() {
  const query = els.terrainSearch.value.trim().toLowerCase();
  els.selectedTerrainLabel.textContent = getTerrain().name;
  els.terrainList.innerHTML = terrainPresets
    .filter((terrain) => `${terrain.name} ${terrain.description}`.toLowerCase().includes(query))
    .map((terrain) => `
      <button type="button" class="terrain-card ${terrain.id === state.selectedTerrainId ? "selected" : ""}" data-terrain-id="${terrain.id}">
        <span>
          <strong>${escapeHtml(terrain.name)}</strong>
          <small>${escapeHtml(terrain.description)}</small>
        </span>
        <span class="terrain-mods">
          <b>Attacker ${signed(terrain.attackerCombat)}</b>
          <b>Defender ${signed(terrain.defenderCombat)}</b>
        </span>
      </button>
    `).join("");

  document.querySelectorAll("[data-terrain-id]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedTerrainId = button.dataset.terrainId;
      const terrain = getTerrain();
      if (terrain.entrenched) state.defenderEntrenched = true;
      lastReport = null;
      saveState();
      renderAll();
    });
  });
}

function renderCards() {
  const query = els.cardSearch.value.trim().toLowerCase();
  els.cardList.innerHTML = cardPresets
    .filter((card) => `${card.name} ${card.description}`.toLowerCase().includes(query))
    .map((card) => `
      <article class="card-option">
        <div>
          <h3>${escapeHtml(card.name)}</h3>
          <p>${escapeHtml(card.description)}</p>
        </div>
        <div class="button-column">
          ${card.side === "attacker" || card.side === "both" ? `<button type="button" data-card-id="${card.id}" data-card-side="attacker">Add Attacker</button>` : ""}
          ${card.side === "defender" || card.side === "both" ? `<button type="button" data-card-id="${card.id}" data-card-side="defender">Add Defender</button>` : ""}
        </div>
      </article>
    `).join("");

  document.querySelectorAll("[data-card-id]").forEach((button) => {
    button.addEventListener("click", () => addCard(button.dataset.cardId, button.dataset.cardSide));
  });
}

function renderActiveCards() {
  els.activeCardCount.textContent = `${state.activeCards.length} active`;
  els.activeCards.innerHTML = state.activeCards.map((entry) => {
    const card = cardPresets.find((item) => item.id === entry.cardId);
    if (!card) return "";
    return `
      <div class="active-card">
        <span>${escapeHtml(card.name)} · ${escapeHtml(sideName(entry.side))}</span>
        <button type="button" data-active-card="${entry.id}">Remove</button>
      </div>
    `;
  }).join("") || emptyState("No active cards.");

  document.querySelectorAll("[data-active-card]").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeCards = state.activeCards.filter((entry) => entry.id !== button.dataset.activeCard);
      saveState();
      renderAll();
    });
  });
}

function handleAction(action, id) {
  if (action === "stage-attacker") addToStack("attacker", id);
  if (action === "stage-defender") addToStack("defender", id);
  if (action === "unstage-attacker") removeFromStack("attacker", id);
  if (action === "unstage-defender") removeFromStack("defender", id);
  if (action === "remove-unit") removeUnit(id);
  if (action === "heal-unit") setStrength(id, findUnit(id).maxStrength);
  if (action === "heal-one") setStrength(id, findUnit(id).strength + 1);
  if (action === "damage-unit") setStrength(id, findUnit(id).strength - 1);
}

function addUnitFromForm(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const traits = [...form.querySelectorAll("[name='unitTrait']:checked")].map((input) => input.value);
  const type = value("#unitType");
  const domain = value("#unitDomain");
  const role = value("#unitRole");
  const derivedTraits = new Set(traits);
  if (type === "armor") derivedTraits.add("armor");
  if (type === "artillery") derivedTraits.add("artillery");
  if (type === "mine") {
    derivedTraits.add("mine");
    derivedTraits.add("minefield");
  }
  if (type === "fighter") derivedTraits.add("fighter");
  if (type === "bomber") derivedTraits.add("bomber");
  if (type === "cas") {
    derivedTraits.add("air");
    derivedTraits.add("air_support");
    derivedTraits.add("land_attack");
  }
  if (!derivedTraits.size) derivedTraits.add("infantry");

  const maxStrength = numberValue("#unitMaxStrength", 1);
  const strength = Math.min(numberValue("#unitStrength", 1), maxStrength);
  const side = document.querySelector("[name='unitSide']:checked").value;
  const newUnit = unit({
    id: crypto.randomUUID(),
    side,
    name: value("#unitName") || "Unnamed Unit",
    country: value("#unitCountry"),
    domain,
    role,
    type,
    attack: numberValue("#unitAttack", 0),
    defense: numberValue("#unitDefense", 0),
    morale: numberValue("#unitMorale", 1),
    strength,
    maxStrength,
    stacking: numberValue("#unitStacking", 1),
    rof: numberValue("#unitRof", 1),
    traits: [...derivedTraits],
    lossPriority: type === "mine" ? "first" : role === "support" ? "last" : "normal",
  });

  state.units.push(newUnit);
  addToStack(side, newUnit.id, false);
  form.reset();
  document.querySelector("#sideAttacker").checked = true;
  document.querySelector("#unitStrength").value = 3;
  document.querySelector("#unitMaxStrength").value = 3;
  document.querySelector("#unitStacking").value = 1;
  document.querySelector("#unitAttack").value = 3;
  document.querySelector("#unitDefense").value = 3;
  document.querySelector("#unitMorale").value = 3;
  document.querySelector("#unitRof").value = 1;
  saveState();
  renderAll();
}

async function runBattle() {
  try {
    const payload = buildBattlePayload();
    lastPayload = payload;
    els.resultStatus.textContent = "Resolving battle...";
    const response = await fetch("/api/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const report = await response.json();
    if (!response.ok) {
      renderError(report.detail || report);
      return;
    }
    lastReport = report;
    state.lastOutcome = report.final;
    saveState();
    renderReport(report);
  } catch (error) {
    renderError(error.message);
  }
}

function applyTurn() {
  if (!lastReport) return;
  applySurvivors("attacker", lastReport.survivors.attacker);
  applySurvivors("defender", lastReport.survivors.defender);
  const winnerKey = lastReport.final.winner_key;
  if (winnerKey === "attacker") state.attackerVp += 1;
  if (winnerKey === "defender") state.defenderVp += 1;
  state.turnNumber += 1;
  state.seed += 1;
  state.activeCards = [];
  state.attackerStack = state.attackerStack.filter((id) => findUnit(id));
  state.defenderStack = state.defenderStack.filter((id) => findUnit(id));
  lastReport = null;
  saveState();
  renderAll();
  renderAppliedOutcome(winnerKey);
}

function applySurvivors(side, survivors) {
  const survivorMap = new Map(survivors.map((item) => [item.id, item]));
  const stagedIds = side === "attacker" ? state.attackerStack : state.defenderStack;
  for (const id of stagedIds) {
    const original = findUnit(id);
    const result = survivorMap.get(id);
    if (!original || !result) continue;
    original.strength = result.strength;
    original.panicked = result.panicked;
    original.destroyed = result.destroyed;
  }
  state.units = state.units.filter((item) => !item.destroyed && item.strength > 0);
}

function buildBattlePayload() {
  const attackerUnits = state.attackerStack.map(findUnit).filter(Boolean);
  const defenderUnits = state.defenderStack.map(findUnit).filter(Boolean);
  if (!attackerUnits.length || !defenderUnits.length) {
    throw new Error("Add at least one attacker and one defender before starting battle.");
  }

  const terrain = getTerrain();
  const battle = {
    region: state.battleName || "Battle",
    terrain: terrain.name,
    attacker_combat_modifier: terrain.attackerCombat,
    defender_combat_modifier: terrain.defenderCombat,
    attacker_morale_modifier: terrain.attackerMorale,
    defender_morale_modifier: terrain.defenderMorale,
    air_modifier: 0,
    artillery_modifier: 0,
    mine_modifier: 0,
    recon_modifier: 0,
    connection_defender_modifier: Number(state.provinceSize || 0),
    defender_entrenched: Boolean(state.defenderEntrenched),
    recon_allowed: true,
    pursuit_allowed: terrain.pursuitAllowed,
    breakthrough_allowed: terrain.breakthroughAllowed,
    armor_superiority_allowed: true,
    max_next_rounds: Number(state.maxNextRounds || 0),
  };

  const attackerModifiers = [];
  const defenderModifiers = [];
  for (const entry of state.activeCards) {
    const card = cardPresets.find((item) => item.id === entry.cardId);
    if (!card) continue;
    if (card.battlePatch) Object.assign(battle, card.battlePatch);
    if (card.modifier) {
      const modifier = {
        name: card.name,
        combat: card.modifier.combat || 0,
        attack: card.modifier.attack || 0,
        defense: card.modifier.defense || 0,
        morale: card.modifier.morale || 0,
        rounds: card.modifier.rounds || [],
        tags: card.modifier.tags || [],
      };
      if (entry.side === "attacker") attackerModifiers.push(modifier);
      if (entry.side === "defender") defenderModifiers.push(modifier);
    }
  }

  return {
    meta: {
      scenario_name: state.scenarioName,
      turn_number: Number(state.turnNumber || 1),
      date_label: `Turn ${state.turnNumber}`,
      active_side: sideName("attacker"),
      phase: "Battles",
      seed: Number(state.seed || 1),
    },
    battle,
    attacker: sidePayload("attacker", attackerUnits, attackerModifiers),
    defender: sidePayload("defender", defenderUnits, defenderModifiers),
  };
}

function sidePayload(side, units, modifiers) {
  return {
    name: sideName(side),
    leader: null,
    scenario_morale_bonus: 0,
    boosters: [],
    modifiers,
    retreat_policy: { mode: "never", prevent_pursuit: true },
    units: units.map(unitPayload),
  };
}

function unitPayload(item) {
  return {
    id: item.id,
    name: item.name,
    role: item.role,
    domain: item.domain,
    attack: Number(item.attack),
    defense: Number(item.defense),
    morale: Number(item.morale),
    strength: Number(item.strength),
    max_strength: Number(item.maxStrength),
    rof: Number(item.rof),
    tags: item.traits,
    loss_priority: item.lossPriority,
  };
}

function renderReport(report) {
  const winnerText = report.final.winner;
  const reachedTarget = nextScoreWouldWin(report.final.winner_key);
  els.resultStatus.textContent = reachedTarget
    ? `${winnerText} will win the campaign if this turn is applied.`
    : `${winnerText} won this battle. Review the log, then end the turn.`;
  els.applyTurn.disabled = false;
  els.battleSummary.innerHTML = `
    ${metric("Winner", report.final.winner)}
    ${metric("Reason", report.final.reason)}
    ${metric(statLabels.battleMorale, `${sideName("attacker")} ${report.initial_battle_morale.attacker.total} / ${sideName("defender")} ${report.initial_battle_morale.defender.total}`)}
    ${metric("Pursuit", report.final.pursuit_happened ? "Yes" : "No")}
    ${metric("Breakthrough", report.final.breakthrough_available ? "Available" : "Unavailable")}
    ${metric("Projected Score", scorePreview(report.final.winner_key))}
  `;
  els.roundTimeline.innerHTML = report.rounds.map(renderRound).join("");
  renderStacks();
}

function renderRound(round) {
  const label = phaseLabel(round.label);
  const rows = round.shots.slice(0, 24).map((shot) => `
    <tr>
      <td>${escapeHtml(sideName(shot.side))}</td>
      <td>${escapeHtml(shot.unit_name)}</td>
      <td>${shot.roll}${shot.reroll_of === null ? "" : `/${shot.reroll_of}`}</td>
      <td>${shot.modified_factor}</td>
      <td class="${shot.hit ? "hit" : "miss"}">${shot.hit ? "Hit" : "Miss"}</td>
    </tr>
  `).join("");
  return `
    <article class="round-card">
      <header>
        <h3>${escapeHtml(label)}</h3>
        <span>${statLabels.battleMorale}: ${escapeHtml(sideName("attacker"))} ${round.morale.attacker} / ${escapeHtml(sideName("defender"))} ${round.morale.defender}</span>
      </header>
      <ul>${round.events.map((event) => `<li>${escapeHtml(phaseText(event))}</li>`).join("")}</ul>
      ${round.shots.length ? `
        <table>
          <thead><tr><th>Side</th><th>Unit</th><th>Roll</th><th>${statLabels.combatFactor}</th><th>Result</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      ` : ""}
    </article>
  `;
}

function renderAppliedOutcome(winnerKey) {
  const winnerName = sideName(winnerKey);
  const campaignWon = state[`${winnerKey}Vp`] >= state.targetVp;
  els.resultStatus.textContent = campaignWon
    ? `${winnerName} reached ${state.targetVp} VP and wins.`
    : `${winnerName} won the turn. Destroyed units were removed.`;
  els.applyTurn.disabled = true;
  els.battleSummary.innerHTML = `
    ${metric("Applied winner", winnerName)}
    ${metric(`Current ${statLabels.victoryPoints}`, `${sideName("attacker")} ${state.attackerVp} / ${sideName("defender")} ${state.defenderVp}`)}
    ${metric("Upcoming Turn", state.turnNumber)}
    ${metric("Units remaining", state.units.length)}
  `;
  els.roundTimeline.innerHTML = "";
}

function updateBmPreview() {
  els.attackerBmPreview.textContent = roughBm("attacker");
  els.defenderBmPreview.textContent = roughBm("defender");
}

function roughBm(side) {
  const ids = side === "attacker" ? state.attackerStack : state.defenderStack;
  const units = ids.map(findUnit).filter((item) => item && item.role === "combat" && item.strength > 0);
  if (!units.length) return 0;
  const avg = Math.floor(units.reduce((sum, item) => sum + Number(item.morale), 0) / units.length + 0.5);
  const terrain = getTerrain();
  const terrainMorale = side === "attacker" ? terrain.attackerMorale : terrain.defenderMorale;
  const air = units.some((item) => item.domain === "air") ? 1 : 0;
  const armor = units.some((item) => item.traits.includes("armor")) ? 1 : 0;
  const cardMorale = state.activeCards.reduce((sum, entry) => {
    const card = cardPresets.find((item) => item.id === entry.cardId);
    if (!card || entry.side !== side || !card.modifier) return sum;
    return sum + (card.modifier.morale || 0);
  }, 0);
  return avg + terrainMorale + air + armor + cardMorale;
}

function showJson() {
  try {
    els.jsonPreview.value = JSON.stringify(lastPayload || buildBattlePayload(), null, 2);
    els.jsonDialog.showModal();
  } catch (error) {
    renderError(error.message);
  }
}

function addToStack(side, id, rerender = true) {
  const stack = side === "attacker" ? state.attackerStack : state.defenderStack;
  const other = side === "attacker" ? state.defenderStack : state.attackerStack;
  if (!stack.includes(id)) stack.push(id);
  removeItem(other, id);
  if (rerender) {
    saveState();
    renderAll();
  }
}

function removeFromStack(side, id) {
  const stack = side === "attacker" ? state.attackerStack : state.defenderStack;
  removeItem(stack, id);
  saveState();
  renderAll();
}

function clearStack(side) {
  if (side === "attacker") state.attackerStack = [];
  if (side === "defender") state.defenderStack = [];
  saveState();
  renderAll();
}

function removeUnit(id) {
  state.units = state.units.filter((item) => item.id !== id);
  removeItem(state.attackerStack, id);
  removeItem(state.defenderStack, id);
  saveState();
  renderAll();
}

function setStrength(id, value) {
  const item = findUnit(id);
  if (!item) return;
  item.strength = Math.max(0, Math.min(item.maxStrength, Number(value)));
  saveState();
  renderAll();
}

function addCard(cardId, side) {
  state.activeCards.push({ id: crypto.randomUUID(), cardId, side });
  saveState();
  renderAll();
}

function renderError(error) {
  els.resultStatus.textContent = "Could not resolve battle.";
  els.applyTurn.disabled = true;
  els.battleSummary.innerHTML = `<pre class="error-block">${escapeHtml(JSON.stringify(error, null, 2))}</pre>`;
  els.roundTimeline.innerHTML = "";
}

function metric(label, value) {
  return `<div class="metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(String(value))}</strong></div>`;
}

function statPill(label, value) {
  return `<span><b>${escapeHtml(label)}</b>${escapeHtml(value)}</span>`;
}

function healthBar(item) {
  const max = Math.max(1, Number(item.maxStrength || 1));
  const current = Math.max(0, Math.min(max, Number(item.strength || 0)));
  const percent = Math.round((current / max) * 100);
  const tone = percent <= 33 ? "critical" : percent <= 66 ? "wounded" : "healthy";
  return `
    <div class="health-block ${tone}" aria-label="${escapeHtml(item.name)} health ${current} of ${max}">
      <div class="health-row">
        <span>${statLabels.currentHealth}</span>
        <strong>${current} / ${max}</strong>
      </div>
      <div class="health-track">
        <span style="width: ${percent}%"></span>
      </div>
    </div>
  `;
}

function projectedUnitState(item, side) {
  if (!lastReport) return { ...item, projected: false, destroyed: false, panicked: false };
  const survivors = side === "attacker" ? lastReport.survivors.attacker : lastReport.survivors.defender;
  const result = survivors.find((unit) => unit.id === item.id);
  if (!result) return { ...item, projected: false, destroyed: false, panicked: false };
  return {
    ...item,
    strength: result.strength,
    maxStrength: result.max_strength,
    destroyed: result.destroyed || result.strength <= 0,
    panicked: result.panicked,
    projected: true,
  };
}

function projectedStatusBadge(original, preview) {
  if (!preview.projected) return "";
  if (preview.destroyed) {
    return `<div class="status-badge destroyed">Destroyed when End Turn is applied · ${statLabels.currentHealth} 0 / ${preview.maxStrength}</div>`;
  }
  if (preview.panicked) {
    return `<div class="status-badge panicked">Panicked after battle · ${statLabels.currentHealth} ${preview.strength} / ${preview.maxStrength}</div>`;
  }
  if (preview.strength < original.strength) {
    return `<div class="status-badge damaged">Damaged after battle · ${original.strength} to ${preview.strength} health</div>`;
  }
  return `<div class="status-badge ready">Survived battle unchanged</div>`;
}

function phaseLabel(label) {
  return String(label).replace(/^Next\b/, "Phase");
}

function phaseText(text) {
  return String(text)
    .replace(/\bNext (\d+)/g, "Phase $1")
    .replace(/\bNEXT\b/g, "PHASE")
    .replace(/\bnext rounds\b/gi, "phase rounds");
}

function emptyState(text) {
  return `<p class="empty">${escapeHtml(text)}</p>`;
}

function flagText(item) {
  const source = item.country || (item.side === "attacker" ? "A" : "D");
  return source.slice(0, 2).toUpperCase();
}

function flagIcon(item) {
  const label = item.country || sideName(item.side);
  const icon = countryIcons[normalizeIconKey(label)];
  if (!icon) {
    return `<div class="flag flag-fallback" title="${escapeHtml(label)}">${escapeHtml(flagText(item))}</div>`;
  }
  return `
    <div class="flag" title="${escapeHtml(label)}">
      <img src="${iconUrl(icon)}" alt="${escapeHtml(label)} flag" loading="lazy" />
    </div>
  `;
}

function unitTypeIcon(item) {
  const icon = unitTypeIcons[unitTypeIconKey(item)] || unitTypeIcons.standard;
  const label = typeLabel(item);
  return `<img class="type-icon" src="${iconUrl(icon)}" alt="" title="${escapeHtml(label)}" loading="lazy" />`;
}

function unitTypeIconKey(item) {
  if (item.type && unitTypeIcons[item.type]) return item.type;
  if (item.traits.includes("cavalry") || item.traits.includes("cav")) return "cavalry";
  if (item.traits.includes("mechanized") || item.traits.includes("mechanised")) return "mechanized";
  if (item.role === "support") return "support";
  return "standard";
}

function renderTraitRow(traits) {
  if (!traits.length) return emptyState("No traits.");
  return `<div class="trait-row">${traits.map(renderTraitChip).join("")}</div>`;
}

function renderTraitChip(trait) {
  const key = normalizeTraitKey(trait);
  const icon = traitIcons[key] || traitIcons.generic;
  const label = traitLabels[key] || titleCaseTrait(trait);
  return `
    <span title="${escapeHtml(label)}">
      <img class="trait-icon" src="${iconUrl(icon)}" alt="" loading="lazy" />
      ${escapeHtml(label)}
    </span>
  `;
}

function traitSummary(traits) {
  return traits.map((trait) => traitLabels[normalizeTraitKey(trait)] || titleCaseTrait(trait)).join(", ");
}

function typeLabel(item) {
  const domains = { land: "Land", air: "Air", sea: "Sea" };
  const types = {
    standard: "Standard Unit",
    armor: "Armored Unit",
    artillery: "Artillery Unit",
    mine: "Minefield Unit",
    fighter: "Fighter Aircraft",
    bomber: "Bomber Aircraft",
    cas: "Close Air Support Aircraft",
  };
  const role = item.role === "support" ? "Support" : "Combat";
  return `${domains[item.domain] || item.domain} ${role} · ${types[item.type] || item.type}`;
}

function iconUrl(path) {
  return `${iconBase}/${path}?v=${ASSET_VERSION}`;
}

function normalizeIconKey(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replaceAll("_", " ")
    .replace(/\s+/g, " ");
}

function normalizeTraitKey(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replaceAll("-", "_")
    .replace(/\s+/g, "_");
}

function titleCaseTrait(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .split(/\s+/)
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
}

function getTerrain() {
  return terrainPresets.find((terrain) => terrain.id === state.selectedTerrainId) || terrainPresets[0];
}

function findUnit(id) {
  return state.units.find((item) => item.id === id);
}

function removeItem(list, value) {
  const index = list.indexOf(value);
  if (index >= 0) list.splice(index, 1);
}

function value(selector) {
  return document.querySelector(selector).value.trim();
}

function numberValue(selector, fallback) {
  const value = Number(document.querySelector(selector).value);
  return Number.isFinite(value) ? value : fallback;
}

function valueFromInput(input) {
  if (input.type === "number") return Number(input.value);
  return input.value;
}

function signed(value) {
  return value > 0 ? `+${value}` : String(value);
}

function scorePreview(winnerKey) {
  const attacker = state.attackerVp + (winnerKey === "attacker" ? 1 : 0);
  const defender = state.defenderVp + (winnerKey === "defender" ? 1 : 0);
  return `${sideName("attacker")} ${attacker} / ${sideName("defender")} ${defender}`;
}

function sideName(side) {
  const raw = side === "attacker" ? state.attackerName : state.defenderName;
  const fallback = side === "attacker" ? "Attackers" : "Defenders";
  const trimmed = String(raw || "").trim();
  return trimmed || fallback;
}

function nextScoreWouldWin(winnerKey) {
  return state[`${winnerKey}Vp`] + 1 >= Number(state.targetVp);
}

function flashStatus(message) {
  els.resultStatus.textContent = message;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
