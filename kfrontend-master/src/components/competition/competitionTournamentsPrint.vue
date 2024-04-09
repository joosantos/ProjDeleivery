<template>
	<Loading v-if="loading" :size="10" />
	<div v-else class="p-6 max-w-max text-black text-left mx-auto">
		<div class="space-y-4">
			<ul role="list" class="relative z-0 divide-y divide-gray-200">
				<li
					v-for="tournament in competition.tournaments"
					v-show="tournament.show"
					:key="tournament.id"
					class="bg-white">
					<div class="relative items-center space-x-3 px-6 py-5 inline-flex">
						<div class="min-w-0 flex-1">
							<div>
								<p class="text-xl font-semibold text-gray-900">
									{{
										`${getTournamentName(tournament, t)} - (${
											tournament.inscriptionsCount
										} ${t("athletes")})`
									}}
								</p>
								<div
									v-for="inscription of tournament.inscriptions"
									v-show="inscription.confirmed && inscription.accepted"
									:key="inscription.athlete_competition_id">
									<p>
										{{
											`${getAthleteNameTeam(inscription.athlete_competition)}`
										}}
									</p>
								</div>
							</div>
						</div>
					</div>
				</li>
			</ul>
		</div>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import { ref } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { getTournamentName } from "@/services/competition.service.js";
import { getAthleteNameTeam } from "@/services/athlete.service.js";
import { useI18n } from "vue-i18n";
import store from "@/store";

let { t } = useI18n();
let loading = ref(true);
let competition = ref(null);

store.commit("setShowNavBar", false);
store.commit("setShowMargins", false);

const props = defineProps({
	// Competition ID
	competitionId: {
		type: String,
		required: true,
	},
});

authApi
	.get(`competitions/${props.competitionId}/print`)
	.then((response) => {
		competition.value = response.data;
		for (let tournament of competition.value.tournaments) {
			tournament.show = false;
			tournament.inscriptionsCount = 0;
			for (let inscription of tournament.inscriptions) {
				if (inscription.confirmed && inscription.accepted) {
					tournament.show = true;
					tournament.inscriptionsCount += 1;
				}
			}
		}
		competition.value.tournaments.sort((a, b) => {
			if (a.category.number_all_at_once !== b.category.number_all_at_once)
				return a.category.number_all_at_once ? 1 : -1;

			if (a.category.name !== b.category.name)
				return a.category.name < b.category.name ? -1 : 1;

			if (a.is_male != null && b.is_male != null) {
				if (a.is_male && !b.is_male) return -1;
				if (!a.is_male && b.is_male) return 1;
			}
			if (a.is_male == null) return -1;
			if (b.is_male == null) return 1;
			if (a.age_min != null && b.age_min != null) {
				let age = a.age_min - b.age_min;
				if (age < 0) return -1;
				if (age > 0) return 1;
			}

			if (
				(a.weight_min != null || a.weight_max != null) &&
				(b.weight_min != null || b.weight_max != null)
			) {
				if (a.weight_min != null && b.weight_min == null) return 1;
				if (b.weight_min != null && a.weight_min == null) return -1;
				let aMinWeight = a.weight_min == null ? a.weight_max : a.weight_min;
				let bMinWeight = b.weight_min == null ? b.weight_max : b.weight_min;
				if (aMinWeight > bMinWeight) return 1;
				if (aMinWeight < bMinWeight) return -1;
				return compareBelts(a, b);
			}
			return compareBelts(a, b);
		});
		loading.value = false;
	})
	.catch((error) => {
		errorHandling(error);
		loading.value = false;
	});

function compareBelts(a, b) {
	if (a.belt_min == null || b.belt_min == null) return 0;
	if (a.belt_min.order > b.belt_min.order) return -1;
	if (a.belt_min.order < b.belt_min.order) return 1;
	return 0;
}
</script>

<i18n>
{
  	"en_GB": {
		"seeTeam": "See Details",
        "athletes": "Athletes",
        "tournaments": "Tournaments",
        "team": "Group By Teams",
        "tourn": "Group By Tournaments",
        "open": "Open",
        "masc": "Masc.",
        "fem": "Fem.",
		"year": "{count} Year | {count} Years",
		"belts": {
			"white": "White",
			"white-yellow": "White and Yellow",
			"yellow": "Yellow",
			"yellow-orange": "Yellow and Orange",
			"orange": "Orange",
			"orange-purple": "Orange and Purple",
			"purple": "Purple",
			"purple-blue": "Purple and Blue",
			"blue": "Blue",
			"blue-green": "Blue and Green",
			"green": "Green",
			"brown-jr": "Brown Junior",
			"brown": "Brown",
			"black-jr": "Black Junior",
			"black": "Black",
			"duan-1": "Duan 1",
			"duan-2": "Duan 2",
			"duan-3": "Duan 3+",
		},
	},
	"pt_PT": {
		"seeTeam": "Ver detalhes",
        "athletes": "Atletas",
        "tournaments": "Torneios",
        "team": "Agrupar por Equipas",
        "tourn": "Agrupar por Torneios",
		"open": "Aberto",
		"masc": "Masculino",
		"fem": "Feminino",
		"year": "{count} Ano | {count} Anos",
		"belts": {
			"white": "Branco",
			"white-yellow": "Branco e Amarelo",
			"yellow": "Amarelo",
			"yellow-orange": "Amarelo e Laranja",
			"orange": "Laranja",
			"orange-purple": "Laranja e Púrpura",
			"purple": "Púrpura",
			"purple-blue": "Púrpura e Azul",
			"blue": "Azul",
			"blue-green": "Azul e Verde",
			"green": "Verde",
			"brown-jr": "Castanho Junior",
			"brown": "Castanho",
			"black-jr": "Preto Junior",
			"black": "Preto",
			"duan-1": "Duan 1",
			"duan-2": "Duan 2",
			"duan-3": "Duan 3+",
		},
	}
}
</i18n>
