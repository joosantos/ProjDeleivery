<template>
	<Loading v-if="loading" :size="10" />
	<div v-else>
		<h1 class="text-3xl font-semibold">
			{{
				props.teamId == 1
				? t("athletes.noTeam")
				: t("athletes.team", {
					team: team == null ? "" : `${team?.name} (${team?.abbreviation})`,
				})
			}}
		</h1>
		<form class="inline-flex space-x-4 relative left-1/2 -translate-x-1/2" @submit.prevent="changeParams">
			<div class="mt-auto mb-2">
				<ToogleInput :label="t('filter.federated')" :name="'isFederated'" :option-selected="isFederated" :error="''"
					@value-changed="(option) => (isFederated = option)" />
			</div>
			<div>
				<CustomInput type="text" :label="t('filter.name')" :name="'filterByName'" :option-selected="athleteName"
					:error="''" @value-changed="(option) => {
							athleteName = option;
						}
						" />
			</div>
			<div class="mt-auto">
				<Trash :text="t('filter.clear')" @button-click="() => {
						athleteName = '';
						isFederated.value = false;
					}
					" />
			</div>
			<div class="mt-auto">
				<Button :message="t('search')" type="primary" :submit="true" :pill="true" :outline="true" />
			</div>
		</form>
		<Loading v-if="loadingSearch" :size="10" />
		<div v-else>
			<div v-if="!athletePage.total_elements">
				<p class="text-3xl font-semibold text-center mt-4">{{ t("noAthletes") }}</p>
			</div>
			<div v-else class="2xl:w-3/4 mt-8 mx-auto grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-x-4 gap-y-4">
				<router-link v-for="athlete of athletePage.athletes" :key="athlete.id"
					:to="{ name: 'Athlete Details', params: { athleteId: athlete.id } }"
					class="col-span-1 flex flex-col bg-blue-100 px-8 pb-2 pt-4 rounded-lg border border-blue-700 hover:bg-blue-200">
					<div class="justify-between inline-flex">
						<p class="text-left text-lg font-medium">
							{{ athlete.name }}
						</p>
						<p class="ml-auto">
							{{
								t("years", {
									year:
										new Date(
											new Date(Date.now()) - new Date(athlete.birthday)
										).getUTCFullYear() - 1970,
								})
							}}
						</p>
					</div>
					<div>
						<p>
							{{
								athlete.private_info.federation_active
								? t("federated", {
									number: athlete.private_info.federation_number.toString().padStart(
										5,
										"0"
									),
								})
								: t("notFederated")
							}}
						</p>
					</div>
				</router-link>
			</div>
			<div v-if="athletePage.total_elements != 0" class="mx-auto mt-4 max-w-max w-full">
				<Pagination :pages="athletePage.total_pages" :current="currentPage" @page-change="changePage" />
			</div>
		</div>
	</div>
</template>

<script setup>
import CustomInput from "@/components/partials/inputs/customInput.vue";
import ToogleInput from "@/components/partials/inputs/toogle.vue";
import Trash from "@/components/partials/inputs/trash.vue";
import Loading from "@/components/partials/loading.vue";
import Button from "@/components/partials/button.vue";
import Pagination from "@/components/partials/pagination/pagination.vue";
import { ref, watch } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { useI18n } from "vue-i18n";
import router from "@/router";
import { useRoute } from "vue-router";

const props = defineProps({
	teamId: {
		type: String,
		required: true,
	},
});

let { t } = useI18n();
const route = useRoute();
let athletePage = ref([]);
let loading = ref(true);
let athleteName = ref("");
let isFederated = ref(false);
let currentPage = ref(1);
let loadingSearch = ref(false);
let team = ref(null);

watch(
	() => route.fullPath,
	() => {
		athleteName.value = route.query.name || "";
		currentPage.value = Number(route.query.page) || 1;

		search();
	},
	{ immediate: true }
);

if (props.teamId != "1") {
	authApi.get(`teams/${props.teamId}`).then((response) => {
		team.value = response.data;
	});
}

function changeParams(initial) {
	let stringReplace = `${route.path}?name=${athleteName.value}&federated=${isFederated.value}&page=${currentPage.value}`;
	if (!initial && stringReplace == route.fullPath) {
		search();
		return;
	}
	currentPage.value = 1;
	history.pushState({}, null, route.fullPath);
	router.replace(stringReplace);
}

function search() {
	loadingSearch.value = true;
	let searchString = `athletes/query?team=${props.teamId}&name=${athleteName.value}&federated=${isFederated.value}&page=${currentPage.value}`;

	authApi
		.get(searchString)
		.then((response) => {
			athletePage.value = response.data;
			loading.value = false;
			loadingSearch.value = false;
		})
		.catch((error) => {
			errorHandling(error);
			loading.value = false;
			loadingSearch.value = false;
		});
}

function changePage(pageNumber) {
	currentPage.value = pageNumber;
	changeParams(false);
}
</script>

<i18n>
{
	"en_GB": {
		"filter": {
			"name": "Filter by Name",
			"federated": "Athlete is Federated",
			"clear": "Clear Filters",
		},
		"athletes": {
			"noTeam": "All Athletes without a Team",
			"team": "All Athletes of the team {team}",
		},
		"noAthletes": "No Athletes to Show",
		"years": "{year} Years Old",
		"notFederated": "Not Federated",
		"federated": "Federated, Nº. {number}",
		"search": "Search",
	},
	"pt_PT": {
		"filter": {
			"name": "Filtrar por Nome",
			"federated": "Atleta é Federado",
			"clear": "Limpar Filtros"
		},
		"athletes": {
			"noTeam": "Todos os Atletas sem Equipa",
			"team": "Todos os Atletas da equipa {team}",
		},
		"noAthletes": "Sem Atletas para Mostrar",
		"years": "{year} Anos",
		"notFederated": "Não Federado",
		"federated": "Federado, Nº. {number}",
		"search": "Pesquisar",
	}
}
</i18n>
