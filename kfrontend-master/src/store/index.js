import { createStore } from "vuex";
import VuexPersist from "vuex-persist";

// Configuração do plugin para guarda a store no localstorage
const vuexPersist = new VuexPersist({
	key: "frontend",
	storage: window.localStorage,
});

// Criação da store
const store = createStore({
	plugins: [vuexPersist.plugin],
	state() {
		return {
			tournament: null,
			errorMessage: "",
			showGenericError: false,
			successMessage: "",
			user: null,
			lastView: "",
			showNavBar: true,
			showMargins: true,
			combatDetails: null,
		};
	},
	mutations: {
		// Saves Tournament Object for printing
		setTournament(state, tournament) {
			state.tournament = tournament;
		},
		// Guarda a última view visitada
		setLastView(state, view) {
			state.lastView = view;
		},
		// Guarda logged user
		setUser(state, user) {
			state.user = user;
		},
		// Stores a boolean to show the navBar (true) or hide them (false)
		setShowNavBar(state, show) {
			state.showNavBar = show;
		},
		// Stores a boolean to show the lateral margins (true) or hide them (false)
		setShowMargins(state, show) {
			state.showMargins = show;
		},
		// Stores combat details
		setCombatDetails(state, show) {
			state.combatDetails = show;
		},
	},
	getters: {
		getTournament: (state) => {
			return state.tournament;
		},
		getShowNavBar: (state) => {
			return state.showNavBar;
		},
		getShowMargins: (state) => {
			return state.showMargins;
		},
		getUser: (state) => {
			return state.user;
		},
		getUserRole: (state) => {
			return state.user?.user_role?.role?.name;
		},
		getLastView: (state) => {
			return state.lastView;
		},
		getCombatDetails: (state) => {
			return state.combatDetails;
		},
	},
});

export default store;
