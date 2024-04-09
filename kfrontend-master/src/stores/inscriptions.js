import { createStore } from "vuex";
import VuexPersist from "vuex-persist";

// Configuração do plugin para guarda a store no localstorage
const vuexPersist = new VuexPersist({
	key: "inscriptionsStore",
	storage: window.localStorage,
});

// Criação da store
const inscriptionsStore = createStore({
	plugins: [vuexPersist.plugin],
	state() {
		return {
			inscriptionsUpdates: {},
		};
	},
	mutations: {
		// New Inscription Update
		setNewUpdate(state, {oldTournament, newTournament, athletes, team}) {
			if (team == null) team = {abbreviation: "NT", name: "No Team"};
			if (!(team.abbreviation in state.inscriptionsUpdates)) state.inscriptionsUpdates[team.abbreviation] = {team: team, updates: []};
			
			state.inscriptionsUpdates[team.abbreviation].updates.push({"oldTournament": oldTournament, "newTournament": newTournament, "athletes": athletes});
		},
		// Remove all updates
		clearUpdates(state) {
			state.inscriptionsUpdates = {};
		},
		removeTeam(state, teamAbbreviation) {
			delete state.inscriptionsUpdates[teamAbbreviation];
		},
	},
	getters: {
		getUpdates: (state) => {
			return state.inscriptionsUpdates;
		},
		getUpdatesOfTeam: (state, teamAbbreviation) => {
			return state.inscriptionsUpdates[teamAbbreviation].updates;
		},
	},
});

export default inscriptionsStore;
