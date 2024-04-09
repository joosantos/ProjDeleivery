<template>
	<Loading v-if="loading" :size="10" />
	<div v-else class="p-6 w-full text-black text-left">
		<p class="text-2xl font-semibold text-center">
			{{ t("title") }}
		</p>

		<div
			class="max-w-max mx-auto grid grid-cols-1 px-4 py-2 bg-gray-100 border border-gray-400 rounded-xl">
			<p class="text-lg font-medium text-center">{{ t("athleteData") }}</p>
			<div class="inline-flex w-full justify-between">
				<p class="font-medium">{{ t("table.name") }}</p>
				<p class="ml-8 text-right w-full">
					{{ getAthleteNameTeam(inscription.athlete_competition) }}
				</p>
			</div>
			<div class="inline-flex">
				<p class="font-medium">{{ t("table.gender") }}</p>
				<p class="ml-8 text-right w-full">
					{{ getGender(inscription.athlete_competition) }}
				</p>
			</div>
			<div class="inline-flex">
				<p class="font-medium">{{ t("table.age") }}</p>
				<p class="ml-8 text-right w-full">
					{{ getAge(inscription.athlete_competition) }}
				</p>
			</div>
			<div class="inline-flex">
				<p class="font-medium min-w-max">{{ t("table.ageEnd") }}</p>
				<p class="ml-8 text-right w-full">
					{{ getAgeEnd(inscription.athlete_competition) }}
				</p>
			</div>
			<div class="inline-flex">
				<p class="font-medium">{{ t("table.weight") }}</p>
				<p class="ml-8 text-right w-full">
					{{ getWeight(inscription.athlete_competition) }}
				</p>
			</div>
			<div class="inline-flex">
				<p class="font-medium">{{ t("table.belt") }}</p>
				<p class="ml-8 text-right w-full">
					{{ getBelt(inscription.athlete_competition) }}
				</p>
			</div>
		</div>

		<div
			class="mt-4 lg:inline-flex space-x-8 bg-gray-100 border border-gray-400 rounded-full py-2 px-4 max-w-max relative left-1/2 -translate-x-1/2">
			<div class="text-center">
				<p class="font-medium text-lg">{{ t("athlete") }}</p>
				<p>{{ getAthleteNameTeam(inscription.athlete_competition) }}</p>
			</div>
			<div class="text-center">
				<p class="font-medium text-lg">{{ t("tournament") }}</p>
				<p>{{ getTournamentName(inscription.tournament, t) }}</p>
			</div>
			<div class="text-center">
				<p class="font-medium text-lg">{{ t("confirmed") }}</p>
				<div
					class="mx-auto max-w-max"
					@click="inscription.confirmed = !inscription.confirmed">
					<div
						v-if="inscription.confirmed"
						class="bg-green-100 rounded-full p-1 border border-green-500 cursor-pointer select-none hover:bg-green-200 hover:border-green-700 hover:text-green-700 text-green-500">
						<CheckIcon class="h-5 w-5" />
					</div>
					<div
						v-else
						class="bg-red-100 rounded-full p-1 border border-red-500 cursor-pointer select-none hover:bg-red-200 hover:border-red-700 hover:text-red-700 text-red-500">
						<XMarkIcon class="h-5 w-5" />
					</div>
				</div>
			</div>
			<div class="text-center">
				<p class="font-medium text-lg">{{ t("accepted") }}</p>
				<div
					class="mx-auto max-w-max"
					@click="inscription.accepted = !inscription.accepted">
					<div
						v-if="inscription.accepted"
						class="bg-green-100 rounded-full p-1 border border-green-500 cursor-pointer select-none hover:bg-green-200 hover:border-green-700 hover:text-green-700 text-green-500">
						<CheckIcon class="h-5 w-5" />
					</div>
					<div
						v-else
						class="bg-red-100 rounded-full p-1 border border-red-500 cursor-pointer select-none hover:bg-red-200 hover:border-red-700 hover:text-red-700 text-red-500">
						<XMarkIcon class="h-5 w-5" />
					</div>
				</div>
			</div>
		</div>

		<div class="mt-4 max-w-max mx-auto">
			<Button
				:loading="showSpinningWheel"
				:show-x="showX"
				:message="t('update')"
				:icon="PencilIcon"
				type="primary"
				@button-click="updateInscription" />
		</div>

		<div class="flex mx-auto max-w-max mt-4">
			<div class="inline-flex">
				<div class="flex">
					<SearchSelect
						:title="t('category')"
						:option-selected="categorySelected"
						:options="categories"
						:error="''"
						@selected="
							(option) => {
								categorySelected = option;
							}
						" />
				</div>
				<div class="max-w-max mt-4 ml-8">
					<Button
						:loading="showSpinningWheelCategory"
						:message="t('search')"
						type="primary"
						@button-click="getTournaments" />
				</div>
			</div>
		</div>

		<div
			v-if="tournaments.length"
			class="bg-gray-200 border border-gray-400 space-y-1 rounded-3xl py-1 px-4 mt-4 mx-auto max-w-max">
			<div v-for="tournament of tournaments" :key="tournament.id">
				<div class="inline-flex justify-between w-full space-x-8">
					<p>{{ getTournamentName(tournament, t) }}</p>
					<p
						class="text-blue-500 hover:text-blue-700 cursor-pointer select-none"
						@click="
							inscription.tournament = tournament;
							inscription.tournament_id = tournament.id;
						">
						{{ t("move") }}
					</p>
				</div>
			</div>
		</div>

		<InscriptionUpdates />
	</div>
</template>

<script setup>
import InscriptionUpdates from "@/components/competition/partials/inscriptionUpdates.vue";
import Loading from "@/components/partials/loading.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import Button from "@/components/partials/button.vue";
import { XMarkIcon, CheckIcon, PencilIcon } from "@heroicons/vue/24/solid";
import { ref } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { getTournamentName } from "@/services/competition.service.js";
import { getAthleteNameTeam } from "@/services/athlete.service.js";
import inscriptionsStore from "@/stores/inscriptions.js";
import { useI18n } from "vue-i18n";
import toast from "@/toast";
import router from "@/router";

let { t } = useI18n();
let loading = ref(true);
let inscription = ref(null);
let showSpinningWheel = ref(false);
let showX = ref(false);
let showSpinningWheelCategory = ref(false);
let categorySelected = ref(null);
let categories = ref([]);
let tournaments = ref([]);
let originalTournament = ref(null);

const props = defineProps({
	// Competition ID
	tournamentId: {
		type: String,
		required: true,
	},
	// Team ID
	athleteCompetitionId: {
		type: String,
		required: true,
	},
});

authApi
	.get(`inscriptions/${props.tournamentId}/${props.athleteCompetitionId}`)
	.then((response) => {
		inscription.value = response.data;
		originalTournament.value = inscription.value.tournament;
		categorySelected.value = inscription.value.tournament.category_id;

		authApi
			.get(`competitions/${inscription.value.tournament.competition_id}/get-categories`)
			.then((response) => {
				for (let category of response.data) {
					categories.value.push({ id: category.id, name: category.name });
				}
				loading.value = false;
			});
	})
	.catch((error) => {
		errorHandling(error);
		loading.value = false;
	});

function getTournaments() {
	showSpinningWheelCategory.value = true;
	authApi
		.get(
			`tournaments/competitions/${inscription.value.tournament.competition_id}/categories/${categorySelected.value}`
		)
		.then((response) => {
			tournaments.value = response.data;
			if (tournaments.value.length == 0) return;

			tournaments.value.sort(function (a, b) {
				if (a.category.name == b.category.name) {
					if (a.age_min == b.age_min && a.age_max == b.age_max) {
						if (a.is_male == b.is_male) {
							if (a.weight_min == null) {
								if (b.weight_min == null) {
									return a.weight_max - b.weight_max;
								}
								return -1;
							}
							if (b.weight_min == null) {
								return 1;
							}
							return a.weight_min - b.weight_min;
						}
						return !a.is_male - !b.is_male;
					}
					if (a.age_min == null) {
						return b.age_min - a.age_max;
					}
					if (b.age_min == null) {
						return a.age_min - b.age_max;
					}
					return a.age_min - b.age_min;
				}
				if (a.category.name < b.category.name) return -1;

				if (a.category.name > b.category.name) return 1;
			});
			showSpinningWheelCategory.value = false;
		})
		.catch((e) => {
			errorHandling(e);
			showSpinningWheelCategory.value = false;
		});
}

function updateInscription() {
	showSpinningWheel.value = true;
	showX.value = false;
	authApi
		.put(
			`inscriptions/${originalTournament.value.id}/${inscription.value.athlete_competition_id}`,
			{
				tournament_id: inscription.value.tournament_id,
				confirmed: inscription.value.confirmed,
				accepted: inscription.value.accepted,
			}
		)
		.then((response) => {
			const athletes = inscription.value.athlete_competition.athletes_group.map(
				(a) => a.athlete
			);
			console.log(response.data);
			inscriptionsStore.commit("setNewUpdate", {
				oldTournament: originalTournament.value,
				newTournament: response.data.tournament,
				athletes: athletes,
				team: athletes[0].team,
			});
			showSpinningWheel.value = false;
			toast.success(t("updated"));
			originalTournament.value = response.data.tournament;
			router.replace({
				name: "Inscription Edit",
				params: {
					tournamentId: response.data.tournament_id,
					athleteCompetitionId: response.data.athlete_competition_id,
				},
			});
		})
		.catch((error) => {
			errorHandling(error);
			showSpinningWheel.value = false;
			showX.value = true;
		});
}

function getGender(athlete) {
	let genderString = "";
	for (let athlete_group of athlete.athletes_group) {
		genderString += `${athlete_group.athlete.is_male ? t("masc") : t("fem")}, `;
	}
	return genderString.slice(0, genderString.length - 2);
}

function getAge(athlete) {
	let today = new Date();
	let ageString = "";
	for (let athlete_group of athlete.athletes_group) {
		let birthDate = new Date(athlete_group.athlete.birthday);
		let age = today.getFullYear() - birthDate.getFullYear();
		let m = today.getMonth() - birthDate.getMonth();
		if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
			age--;
		}
		ageString += `${age}, `;
	}
	return ageString.slice(0, ageString.length - 2);
}

function getAgeEnd(athlete) {
	let today = new Date();
	let dateStart = new Date(today.getFullYear(), 11, 31);

	let ageString = "";
	for (let athlete_group of athlete.athletes_group) {
		let birthDate = new Date(athlete_group.athlete.birthday);
		let diff = dateStart.getTime() - birthDate.getTime();
		let age = Math.floor(diff / (1000 * 60 * 60 * 24 * 365.25));
		ageString += `${age}, `;
	}
	return ageString.slice(0, ageString.length - 2);
}

function getWeight(athlete) {
	let weightString = "";
	for (let athlete_group of athlete.athletes_group) {
		weightString += `${athlete_group.athlete.weight} Kg, `;
	}
	return weightString.slice(0, weightString.length - 2);
}

function getBelt(athlete) {
	let beltString = "";
	for (let athlete_group of athlete.athletes_group) {
		if (athlete_group.athlete.belt == null) beltString += `${t("belts.noBelt")}, `;
		else beltString += `${t(`belts.${athlete_group.athlete.belt.name}`)}, `;
	}
	return beltString.slice(0, beltString.length - 2);
}
</script>

<i18n>
{
  	"en_GB": {
		"table": {
			"name": "Name",
			"gender": "Gender",
			"age": "Age",
			"weight": "Weight",
			"belt": "Belt",
			"ageEnd": "Age at the end of the year",
		},
		"title": "Inscription Edit",
		"athleteData": "Athlete Data",
		"category": "Category",
		"update": "Update Inscription",
		"search": "Search",
		"athlete": "Athlete",
		"tournament": "Tournament",
		"confirmed": "Confirmed",
		"accepted": "Accepted",
		"move": "Move Inscription Here",
		"updated": "Inscription Updated!",
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
			"noBelt": "No Belt",
		},
	},
	"pt_PT": {
		"table": {
			"name": "Nome",
			"gender": "Género",
			"age": "Idade",
			"weight": "Peso",
			"belt": "Cinto",
			"ageEnd": "Idade no final do ano",
		},
		"title": "Editar Inscrição",
		"athleteData": "Dados do Atleta",
		"category": "Categoria",
		"update": "Atualizar Inscrição",
		"search": "Pesquisar",
		"athlete": "Atleta",
		"tournament": "Torneio",
		"confirmed": "Confirmado",
		"accepted": "Aceite",
		"move": "Mover Inscrição Para Aqui",
		"updated": "Inscrição Atualizada!",
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
			"noBelt": "No Belt",
		},
	}
}
</i18n>
