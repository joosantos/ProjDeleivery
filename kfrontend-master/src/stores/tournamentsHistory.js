import { createStore } from "vuex";
import VuexPersist from "vuex-persist";

// Configuração do plugin para guarda a store no localstorage
const vuexPersist = new VuexPersist({
	key: "tournamentsHistoryStore",
	storage: window.localStorage,
});

// Criação da store
const tournamentsHistoryStore = createStore({
	plugins: [vuexPersist.plugin],
	state() {
		return {
			idsVisited: [],
		};
	},
	mutations: {
		addNewId(state, id) {
			if (state.idsVisited.findIndex(a => a === id) === -1) {
				state.idsVisited.push(id);
			}
		},
		// Remove all updates
		clearIds(state) {
			state.idsVisited = [];
		},
	},
	getters: {
		getIds: (state) => {
			return state.idsVisited;
		},
	},
});

export default tournamentsHistoryStore;
