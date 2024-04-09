<template>
	<div v-if="store.getters.getTournament.category.category_type.name == 'Tournament'">
		<Bracket2
			v-if="store.getters.getTournament.matches.length < 2"
			:tournament="store.getters.getTournament" />
		<Bracket3
			v-else-if="store.getters.getTournament.matches.length < 4"
			:tournament="store.getters.getTournament" />
		<Bracket4
			v-else-if="store.getters.getTournament.matches.length < 5"
			:tournament="store.getters.getTournament" />
		<Bracket8
			v-else-if="store.getters.getTournament.matches.length < 9"
			:tournament="store.getters.getTournament" />
		<Bracket16
			v-else-if="store.getters.getTournament.matches.length < 17"
			:tournament="store.getters.getTournament" />
		<Bracket32
			v-else-if="store.getters.getTournament.matches.length < 33"
			:tournament="store.getters.getTournament" />
		<p v-else>
			{{ t("tournament.matchesError") }}
		</p>
	</div>
	<ListTournament v-else :tournament="store.getters.getTournament" />
</template>

<script setup>
import Bracket2 from "@/components/partials/skeletons/bracket2.vue";
import Bracket3 from "@/components/partials/skeletons/bracket3.vue";
import Bracket4 from "@/components/partials/skeletons/bracket4.vue";
import Bracket8 from "@/components/partials/skeletons/bracket8.vue";
import Bracket16 from "@/components/partials/skeletons/bracket16.vue";
import Bracket32 from "@/components/partials/skeletons/bracket32.vue";
import ListTournament from "@/components/partials/skeletons/listTournament.vue";
import { useI18n } from "vue-i18n";
import store from "@/store";

let { t } = useI18n();

store.commit("setShowNavBar", false);
store.commit("setShowMargins", false);
setTimeout(() => {
	print();
}, 200);
</script>

<i18n>
{
	"en_GB": {
		"day": "Day {count}",
		"morning": "Morning",
		"afternoon": "Afternoon",
		"tournament": {
			"notLoaded": "Wasn't possible to load the tournament",
			"matchesError": "The tournament has more than 32 matches"
		},
		"table": {
			"name": "Name",
			"matches": "Matches",
			"preview": "Show Tournament"
		}
	},
	"pt_PT": {
	}
}
</i18n>
