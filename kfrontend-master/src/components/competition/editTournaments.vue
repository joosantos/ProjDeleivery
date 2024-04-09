<template>
	<Loading v-if="loading" />
	<div v-else class="px-6 overflow-x-auto lg:overflow-x-visible">
		<p class="font-semibold text-3xl">{{ competitionName }}</p>
		<!-- Get Categories -->
		<div
			class="flex flex-col md:flex-row space-x-6 items-center pb-2 w-full relative gap-y-4 lg:gap-y-0 mt-4">
			<!-- Category Search -->
			<form class="flex" @submit.prevent="search">
				<SearchSelect
					:title="t('cat')"
					:option-selected="state.category"
					:options="categories"
					:error="''"
					@selected="
						(option) => {
							state.category = option;
							sort();
						}
					" />
				<div class="max-w-max ml-8 mt-4">
					<Button
						:loading="showSpinningWheel"
						:message="t('search')"
						type="primary"
						:submit="true"
						@button-click="null" />
				</div>
			</form>
			<div v-if="state.category != ''" class="max-w-max ml-8 mt-4">
				<Button :message="t('create')" type="success" @button-click="create" />
			</div>
		</div>
		<!-- Search -->
		<div
			class="flex flex-col md:flex-row space-x-6 items-center pb-2 w-full relative gap-y-4 lg:gap-y-0">
			<!-- Name Input -->
			<div class="flex flex-col">
				<CustomInput
					:label="t('name')"
					type="text"
					:name="'name'"
					:option-selected="state.name"
					:error="''"
					@value-changed="
						(option) => {
							state.name = option;
							sort();
						}
					" />
			</div>
		</div>

		<!-- Tournaments Edit -->
		<div>
			<form
				v-for="tournament of tournaments"
				:id="tournament.id"
				:key="tournament.id"
				@submit.prevent="update(tournament)">
				<div v-show="tournament.show" class="inline-flex text-lg">
					<p class="min-w-max mt-7 mr-4">{{ tournament.category.name }}</p>

					<!-- Gender Search -->
					<div class="flex">
						<SearchSelect
							:title="t('gender')"
							:option-selected="tournament.is_male + ''"
							:options="genders"
							:error="''"
							@selected="
								(option) => {
									tournament.is_male = option;
								}
							" />
					</div>

					<div class="w-20 ml-4">
						<CustomInput
							:label="t('ageMin')"
							type="text"
							:mask="'###'"
							:name="`${tournament.id}#age_min`"
							:option-selected="tournament.age_min + ''"
							:error="''"
							@value-changed="
								(option) => {
									tournament.age_min = option;
								}
							" />
					</div>
					<MinusIcon class="h-5 w-5 mt-8" />
					<div class="w-20">
						<CustomInput
							:label="t('ageMax')"
							type="text"
							:mask="'###'"
							:name="`${tournament.id}#age_max`"
							:option-selected="tournament.age_max + ''"
							:error="''"
							@value-changed="
								(option) => {
									tournament.age_max = option;
								}
							" />
					</div>
					<div class="w-40 ml-4">
						<CustomInput
							:label="t('weightMin')"
							type="text"
							:mask="'###'"
							:name="`${tournament.id}#weight_min`"
							:option-selected="tournament.weight_min + ''"
							:error="''"
							@value-changed="
								(option) => {
									tournament.weight_min = option;
								}
							" />
					</div>
					<MinusIcon class="h-5 w-5 mt-8 rotate-[-80deg]" />
					<div class="w-40">
						<CustomInput
							:label="t('weightMax')"
							type="text"
							:mask="'###'"
							:name="`${tournament.id}#weight_max`"
							:option-selected="tournament.weight_max + ''"
							:error="''"
							@value-changed="
								(option) => {
									tournament.weight_max = option;
								}
							" />
					</div>
					<div class="w-40 ml-4">
						<SearchSelect
							:options="belts"
							:title="t('beltMin')"
							:option-selected="tournament.belt_min_id"
							:error="''"
							@selected="(option) => (tournament.belt_min_id = option)" />
					</div>
					<MinusIcon class="h-5 w-5 mt-8 rotate-[-80deg]" />
					<div class="w-40">
						<SearchSelect
							:options="belts"
							:title="t('beltMax')"
							:option-selected="tournament.belt_max_id"
							:error="''"
							@selected="(option) => (tournament.belt_max_id = option)" />
					</div>
					<div class="max-w-max ml-8 mt-4">
						<Button
							:loading="showSpinningWheel"
							:message="t('update')"
							:submit="true"
							type="primary"
							@button-click="null" />
					</div>
					<div
						v-if="!inscriptionsStarted || competitionName == 'DEFAULTS'"
						class="max-w-max ml-8 mt-4">
						<Button
							:loading="showSpinningWheel"
							:message="t('delete')"
							:submit="false"
							type="danger"
							@button-click="deleteTournament(tournament.id)" />
					</div>
				</div>
			</form>
		</div>
	</div>
</template>

<script setup>
import Button from "@/components/partials/button.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Loading from "@/components/partials/loading.vue";
import { MinusIcon } from "@heroicons/vue/24/solid";
import { authApi, errorHandling } from "@/services/api";
import { getTournamentName } from "@/services/competition.service.js";
import { ref } from "vue";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

const props = defineProps({
	// ID of the competition
	competitionId: {
		type: String,
		required: true,
	},
});

let genders = ref([
	{ id: "null", name: t("open") },
	{ id: "true", name: t("masc") },
	{ id: "false", name: t("fem") },
]);
let categories = ref([]);
let competitionName = ref("");
let state = ref({
	male: true,
	female: true,
	age: "",
	category: "",
	name: "",
	area: "all",
	day: "all",
	time: "all",
	showZero: true,
});
let tournaments = ref([]);
let loading = ref(true);
let belts = ref([]);
let showSpinningWheel = ref(false);
let inscriptionsStarted = ref(false);
let allBets = ref([]);

let promises = [];

promises.push(
	authApi.get(`competitions/${props.competitionId}/get-categories`).then((response) => {
		for (let category of response.data) {
			categories.value.push({ id: category.id, name: category.name });
		}
	})
);

promises.push(
	authApi.get(`competitions/name/${props.competitionId}`).then((response) => {
		competitionName.value = response.data;
	})
);

promises.push(
	authApi.get("belts").then((response) => {
		allBets.value = response.data;
		belts.value.push({ name: t(`belts.none`), id: "none" });
		for (let belt of response.data) {
			belts.value.push({ name: t(`belts.${belt.name}`), id: belt.id });
		}
	})
);

promises.push(
	authApi.get(`competitions/${props.competitionId}/inscriptions-started`).then((response) => {
		inscriptionsStarted.value = response.data;
	})
);

Promise.all(promises)
	.then(() => {
		loading.value = false;
	})
	.catch(() => {
		toast.error(t("notLoaded"));
	});

function sort() {
	for (let tourn of tournaments.value) {
		tourn.show = false;
		if (
			state.value.name != "" &&
			getTournamentName(tourn, t).toUpperCase().indexOf(state.value.name.toUpperCase()) == -1
		) {
			continue;
		}
		tourn.show = true;
	}
}

function search() {
	loading.value = true;
	authApi
		.get(`tournaments/competitions/${props.competitionId}/categories/${state.value.category}`)
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
			sort();
			loading.value = false;
		})
		.catch((e) => {
			errorHandling(e);
			loading.value = false;
		});
}

function create() {
	loading.value = true;
	authApi
		.post(`tournaments`, {
			competition_id: props.competitionId,
			category_id: state.value.category,
		})
		.then(() => {
			toast.success(t("created"));
			search();
		})
		.catch((error) => {
			errorHandling(error);
			loading.value = false;
		});
}

function update(tournament) {
	tournament.is_male =
		tournament.is_male.toString() == "null" ? null : tournament.is_male.toString() == "true";
	tournament.age_min =
		tournament.age_min == null || tournament.age_min == "" ? null : Number(tournament.age_min);
	tournament.age_max =
		tournament.age_max == null || tournament.age_max == "" ? null : Number(tournament.age_max);
	tournament.weight_min =
		tournament.weight_min == null || tournament.weight_min == ""
			? null
			: Number(tournament.weight_min);
	tournament.weight_max =
		tournament.weight_max == null || tournament.weight_max == ""
			? null
			: Number(tournament.weight_max);
	if (
		isNaN(tournament.age_min) ||
		isNaN(tournament.age_max) ||
		isNaN(tournament.weight_min) ||
		isNaN(tournament.weight_max) ||
		tournament.age_min < 0 ||
		tournament.age_max < 0 ||
		tournament.weight_min < 0 ||
		tournament.weight_max < 0
	) {
		toast.error("invalidInput");
		return;
	}
	if (
		tournament.belt_min_id != tournament.belt_max_id &&
		(tournament.belt_min_id == null || tournament.belt_max_id == null)
	) {
		toast.error("invalidInput");
		return;
	}
	let beltMinOrder = allBets.value.find((a) => a.id == tournament.belt_min_id)?.order;
	let beltMaxOrder = allBets.value.find((a) => a.id == tournament.belt_max_id)?.order;
	if (beltMaxOrder < beltMinOrder) {
		toast.error("invalidInput");
		return;
	}
	loading.value = true;
	authApi
		.put(`tournaments/${tournament.id}`, {
			is_male: tournament.is_male,
			age_min: tournament.age_min,
			age_max: tournament.age_max,
			weight_min: tournament.weight_min,
			weight_max: tournament.weight_max,
			belt_min_id: tournament.belt_min_id,
			belt_max_id: tournament.belt_max_id,
		})
		.then(() => {
			toast.success(t("updated"));
			search();
		})
		.catch((error) => {
			errorHandling(error);
			loading.value = false;
		});
}

function deleteTournament(tournamentId) {
	loading.value = true;
	authApi
		.delete(`tournaments/${tournamentId}`)
		.then(() => {
			toast.success(t("deleted"));
			search();
		})
		.catch((error) => {
			errorHandling(error);
			loading.value = false;
		});
}
</script>

<i18n>
{
	"en_GB": {
		"create": "Create new Tournament",
		"updated": "Tournament Updated",
		"deleted": "Tournament Deleted",
		"delete": "Delete",
		"invalidInput": "Invalid Input Data",
		"search": "See Tournaments",
		"update": "Update",
		"allCategories": "All Categories",
		"gender": "Gender",
		"editTournaments": "Edit Tournaments",
		"open": "Open",
		"masc": "Masculine",
		"fem": "Feminine",
		"year": "{count} Year | {count} Years",
		"notLoaded": "Wasn't possible to load the competition",
		"cat": "Category",
		"name": "Filter By Name",
		"ageMin": "Age Min",
		"ageMax": "Age Max",
		"weightMin": "Weight Min",
		"weightMax": "Weight Max",
		"beltMin": "Belt Min",
		"beltMax": "Belt Max",
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
			"none": "None"
		},
	},
	"pt_PT": {
		"create": "Criar um novo torneio",
		"updated": "Torneio Atualizado",
		"deleted": "Torneio Apagado",
		"delete": "Apagar",
		"invalidInput": "Dados Inválidos",
		"search": "Ver torneios",
		"update": "Update",
		"allCategories": "Todas as Categorias",
		"gender": "Género",
		"editTournaments": "Editar Torneios",
		"open": "Aberto",
		"masc": "Masculino",
		"fem": "Feminino",
		"year": "{count} Ano | {count} Anos",
		"notLoaded": "Não foi possível carregar as competições",
		"cat": "Categoria",
		"name": "Filtrar por Nome",
		"ageMin": "Id. Min",
		"ageMax": "Id. Max",
		"weightMin": "Peso Min",
		"weightMax": "Peso Max",
		"beltMin": "Cinto Min",
		"beltMax": "Cinto Max",
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
			"none": "Nenhum"
		},
	}
}
</i18n>
