<template>
	<Loading v-if="loading" />
	<div v-else class="px-6 overflow-x-auto lg:overflow-x-visible">
		<div class="lg:sticky pt-4 lg:pt-0 relative lg:top-[7.25rem] bg-white z-10">
			<!-- Show Results, Print to PDF and edit tournament buttons -->
			<div class="inline-flex w-full mb-2">
				<p class="text-xl font-bold uppercase">{{ competitionName }}</p>
				<div class="ml-auto mr-20 inline-flex space-x-4">
					<router-link
						target="_blank"
						class="border border-blue-900 rounded-md max-w-max lg:min-w-max px-2 py-1 bg-blue-100 hover:bg-blue-300 active:bg-blue-500 select-none cursor-pointer"
						:to="
							store.getters.getUserRole == 'ADMIN'
								? {
										name: 'See Time Left',
										params: { competitionId: props.competition },
								  }
								: {
										name: 'Show Combats By Area',
										params: { competitionId: props.competition },
								  }
						">
						{{ t("showMatchesInEachArea") }}
					</router-link>
					<router-link
						target="_blank"
						class="border border-blue-900 rounded-md max-w-max lg:min-w-max px-2 py-1 bg-blue-100 hover:bg-blue-300 active:bg-blue-500 select-none cursor-pointer"
						:to="{ name: 'Statistics', params: { competition: props.competition } }">
						{{ t("showResults") }}
					</router-link>
					<router-link
						v-if="store.getters.getUserRole == 'ADMIN'"
						target="_blank"
						class="border border-blue-900 rounded-md max-w-max lg:min-w-max px-2 py-1 bg-green-200 hover:bg-blue-300 active:bg-blue-500 select-none cursor-pointer"
						:to="{
							name: 'Show Tournaments By Team',
							params: { competitionId: props.competition },
						}">
						{{ t("showTournamentsByTeam") }}
					</router-link>
					<router-link
						v-if="store.getters.getUserRole == 'ADMIN'"
						target="_blank"
						class="border border-blue-900 rounded-md max-w-max lg:min-w-max px-2 py-1 bg-blue-100 hover:bg-blue-300 active:bg-blue-500 select-none cursor-pointer"
						:to="{
							name: 'Print Competition',
							params: { competitionId: props.competition },
						}">
						{{ t("printPDF") }}
					</router-link>
					<router-link
						v-if="store.getters.getUserRole == 'ADMIN'"
						target="_blank"
						class="border border-blue-900 rounded-md max-w-max lg:min-w-max px-2 py-1 bg-blue-100 hover:bg-blue-300 active:bg-blue-500 select-none cursor-pointer"
						:to="{
							name: 'Competition Tournaments Print',
							params: { competitionId: props.competition },
						}">
						{{ t("printTournamentListPDF") }}
					</router-link>
					<router-link
						v-if="store.getters.getUserRole == 'ADMIN'"
						target="_blank"
						class="border border-blue-900 rounded-md max-w-max lg:min-w-max px-2 py-1 bg-blue-100 hover:bg-blue-300 active:bg-blue-500 select-none cursor-pointer"
						:to="{
							name: 'Edit Tournaments',
							params: { competitionId: props.competition },
						}">
						{{ t("editTournaments") }}
					</router-link>
				</div>
			</div>

			<form
				class="flex flex-col md:flex-row space-x-6 items-center pb-2 w-full relative gap-y-4 lg:gap-y-0"
				@submit.prevent="changeParams">
				<!-- Admin show 0 Matches Tournaments -->
				<div
					v-if="store.getters.getUser?.user_role?.role?.name == 'ADMIN'"
					class="flex mt-4 lg:mt-auto">
					<ToogleInput
						:label="t('showCompetition.form.showZero')"
						:sub-label="''"
						:option-selected="state.showZero"
						@value-changed="
							(option) => {
								state.showZero = option;
							}
						" />
				</div>
				<!-- Male and Female Toggles -->
				<div class="flex flex-col md:flex-row lg:gap-x-4 gap-y-4 lg:gap-y-0">
					<ToogleInput
						:label="t('masc')"
						:sub-label="''"
						:option-selected="state.male"
						@value-changed="
							(option) => {
								state.male = option;
							}
						" />
					<ToogleInput
						:label="t('fem')"
						:sub-label="''"
						:option-selected="state.female"
						@value-changed="
							(option) => {
								state.female = option;
							}
						" />
				</div>

				<!-- Category Search -->
				<div class="flex">
					<SearchSelect
						:title="t('showCompetition.form.category')"
						:option-selected="state.category"
						:options="categories"
						:error="''"
						@selected="
							(option) => {
								state.category = option;
							}
						" />
				</div>

				<!-- Age Input -->
				<div class="flex flex-col">
					<CustomInput
						:label="t('showCompetition.form.age')"
						type="text"
						:mask="'###'"
						:name="'age'"
						:option-selected="state.age"
						:error="''"
						@value-changed="
							(option) => {
								state.age = option;
							}
						" />
				</div>

				<!-- Area Search -->
				<div class="flex">
					<SearchSelect
						:title="t('showCompetition.form.area.label')"
						:option-selected="state.area"
						:options="areas"
						:error="''"
						@selected="
							(option) => {
								state.area = option;
							}
						" />
				</div>

				<!-- Day Search -->
				<div class="flex">
					<SearchSelect
						:title="t('showCompetition.form.day.label')"
						:option-selected="state.day"
						:options="days"
						:error="''"
						@selected="
							(option) => {
								state.day = option;
							}
						" />
				</div>

				<!-- Time of the Day Search -->
				<div class="flex">
					<SearchSelect
						:title="t('showCompetition.form.time')"
						:option-selected="state.time"
						:options="times"
						:error="''"
						@selected="
							(option) => {
								state.time = option;
							}
						" />
				</div>

				<!-- Athlete's Name Input -->
				<div class="flex flex-col">
					<CustomInput
						:label="t('showCompetition.form.athleteName')"
						type="text"
						:name="'athlete'"
						:option-selected="state.athlete"
						:error="''"
						@value-changed="
							(option) => {
								state.athlete = option;
							}
						" />
				</div>

				<!-- Team's Abrreviation Input -->
				<div class="flex flex-col">
					<CustomInput
						:label="t('showCompetition.form.team')"
						type="text"
						:name="'team'"
						:option-selected="state.team"
						:error="''"
						@value-changed="
							(option) => {
								state.team = option;
							}
						" />
				</div>

				<div>
					<Button
						:message="t('showCompetition.form.search')"
						type="primary"
						size="small"
						:submit="true"
						:pill="true"
						:outline="true" />
				</div>
			</form>

			<div class="max-w-max">
				<Button
					:message="t('showCompetition.form.clearHistory')"
					type="primary"
					size="small"
					:submit="false"
					:pill="true"
					:outline="false"
					@click="tournamentsHistoryStore.commit('clearIds')" />
			</div>
			<p class="pb-2 ml-1">
				{{
					t("numberTournamentsShowing", {
						first: limit * (currentPage - 1) + 1,
						second: limit * (currentPage - 1) + tournaments.results.length,
						total: tournaments.n_results,
					})
				}}
			</p>
		</div>
		<div class="bg-gray-100 border border-gray-300 rounded-xl mt-2 text-center">
			<Loading v-if="loadingSearch" :size="10" />
			<div v-else-if="!tournaments?.results?.length">
				<h1 class="font-bold text-xl py-4">
					{{ t("noTournamentsToShow") }}
				</h1>
			</div>
			<div v-else>
				<div
					v-for="tournament of tournaments.results"
					:key="tournament.id"
					class="w-full px-4 py-2">
					<div
						:class="[
							'bg-blue-100 rounded-xl py-1 px-2 border border-blue-300',
							tournamentsHistoryStore.getters.getIds.findIndex(
								(a) => a === tournament.id
							) !== -1 && 'bg-indigo-200 border-blue-400',
						]">
						<router-link
							class="mt-2 flex flex-col md:inline-flex md:flex-row justify-between w-full cursor-pointer hover:bg-blue-200 rounded-xl px-4 py-1 group"
							:to="{
								name: 'Show Tournament',
								params: { tournament: tournament.id },
							}"
							@click="tournamentsHistoryStore.commit('addNewId', tournament.id)"
							@click.middle="
								tournamentsHistoryStore.commit('addNewId', tournament.id)
							">
							<h1 class="text-2xl font-semibold md:text-left">
								{{ getTournamentName(tournament, t) }}
							</h1>
							<p
								class="mt-1 text-blue-500 group-hover:text-blue-800 group-hover:font-medium cursor-pointer select-none">
								{{ t("showCompetition.table.show") }}
							</p>
						</router-link>
						<div
							class="flex flex-col md:inline-flex md:flex-row justify-between w-full">
							<div
								class="grid grid-cols-2 grid-rows-2 max-w-max gap-y-2 mt-2 mx-auto md:mx-0">
								<div class="inline-flex w-full">
									<div class="w-12">
										<UserIcon
											class="h-7 w-7 text-gray-800 ml-1 relative left-1/2 -translate-x-1/2" />
									</div>
									<h3 class="text-left font-normal text-lg ml-2">
										{{
											t("showCompetition.table.athletes", {
												count: tournament.inscriptions.length,
											})
										}}
									</h3>
								</div>
								<div class="inline-flex w-full">
									<div class="w-12">
										<TournamentBracket
											class="h-8 w-8 text-gray-800 ml-1 -mt-0.5 relative left-1/2 -translate-x-1/2" />
									</div>
									<h3 class="text-left font-normal text-lg ml-2">
										{{
											t("showCompetition.table.matches", {
												count: tournament.matches.length,
											})
										}}
									</h3>
								</div>
								<div class="inline-flex w-full">
									<div class="w-12">
										<Square2StackIcon
											class="h-7 w-7 text-gray-800 ml-1 relative left-1/2 -translate-x-1/2" />
									</div>
									<h3 class="text-left font-normal text-lg ml-2">
										{{
											t(
												"showCompetition.table.area",
												{
													area:
														tournament.area == null
															? 0
															: tournament.area,
												},
												tournament.area == null ? 0 : tournament.area
											)
										}}
									</h3>
								</div>
								<div v-if="tournament.day != null" class="inline-flex w-full">
									<div class="w-12">
										<ClockIcon
											:class="[
												'h-7 w-7 ml-1 relative left-1/2 -translate-x-1/2',
												tournament.morning
													? 'text-blue-700'
													: 'text-orange-500',
											]" />
									</div>
									<h3
										:class="[
											'text-left font-normal text-lg ml-2',
											tournament.morning
												? 'text-blue-700'
												: 'text-orange-500',
										]">
										{{
											t(
												"showCompetition.table.time",
												{
													day: tournament.day,
												},
												tournament.morning ? 1 : 2
											)
										}}
									</h3>
								</div>
							</div>
							<div
								v-if="store.getters.getUser?.user_role?.role?.name == 'ADMIN'"
								class="w-50 flex flex-col gap-y-2 mt-2">
								<LinkTable
									:router-to="{
										name: 'Edit Tournament',
										params: {
											competition: tournament.competition_id,
											tournament: tournament.id,
										},
									}"
									:text="t('showCompetition.table.edit')" />
							</div>
						</div>
					</div>
				</div>
				<div class="mx-auto mt-4 max-w-max">
					<Pagination
						:pages="Math.ceil(tournaments.n_results / limit)"
						:current="currentPage"
						@page-change="changePage" />
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import tournamentsHistoryStore from "@/stores/tournamentsHistory.js";
import ToogleInput from "@/components/partials/inputs/toogle.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Loading from "@/components/partials/loading.vue";
import Pagination from "@/components/partials/pagination/pagination.vue";
import Button from "@/components/partials/button.vue";
import { authApi, unauthApi, errorHandling } from "@/services/api";
import { UserIcon } from "@heroicons/vue/24/solid";
import { Square2StackIcon, ClockIcon } from "@heroicons/vue/24/outline";
import TournamentBracket from "@/components/icons/tournamentBracket.vue";
import LinkTable from "@/components/competition/partials/linkTable.vue";
import { getTournamentName } from "@/services/competition.service.js";
import { ref, watch } from "vue";
import store from "@/store";
import router from "@/router";
import { useI18n } from "vue-i18n";
import { useRoute } from "vue-router";

let { t } = useI18n({ useScope: "global" });

const route = useRoute();
const props = defineProps({
	// ID of the competition
	competition: {
		type: String,
		required: true,
	},
});

let categories = ref([{ id: "null", name: t("all") }]);
const areas = ref([
	{ id: "all", name: t("all") },
	{ id: "null", name: t("showCompetition.form.area.option", { area: 0 }, 0) },
	{ id: "1", name: t("showCompetition.form.area.option", { area: 1 }, 1) },
	{ id: "2", name: t("showCompetition.form.area.option", { area: 2 }, 2) },
	{ id: "3", name: t("showCompetition.form.area.option", { area: 3 }, 3) },
	{ id: "4", name: t("showCompetition.form.area.option", { area: 4 }, 4) },
	{ id: "5", name: t("showCompetition.form.area.option", { area: 5 }, 5) },
	{ id: "6", name: t("showCompetition.form.area.option", { area: 6 }, 6) },
	{ id: "7", name: t("showCompetition.form.area.option", { area: 7 }, 7) },
	{ id: "8", name: t("showCompetition.form.area.option", { area: 8 }, 8) },
	{ id: "9", name: t("showCompetition.form.area.option", { area: 9 }, 9) },
	{ id: "10", name: t("showCompetition.form.area.option", { area: 10 }, 10) },
	{ id: "11", name: t("showCompetition.form.area.option", { area: 11 }, 11) },
	{ id: "12", name: t("showCompetition.form.area.option", { area: 12 }, 12) },
]);
const days = ref([
	{ id: "all", name: t("all") },
	{ id: "1", name: t("showCompetition.form.day.option", { day: 1 }) },
	{ id: "2", name: t("showCompetition.form.day.option", { day: 2 }) },
	{ id: "3", name: t("showCompetition.form.day.option", { day: 3 }) },
]);
const times = ref([
	{ id: "null", name: t("all") },
	{ id: "M", name: t("showCompetition.form.morning") },
	{ id: "A", name: t("showCompetition.form.afternoon") },
]);
let tournaments = ref(null);
let loading = ref(true);
let loadingSearch = ref(true);
let state = ref({
	male: route.query.male ? route.query.male == "true" : true,
	female: route.query.female ? route.query.female == "true" : true,
	age: route.query.age || "",
	category: route.query.category || "null",
	area: route.query.area || "all",
	day: route.query.day || "all",
	time: route.query.time || "null",
	showZero: route.query.showZero ? route.query.showZero == "true" : true,
	athlete: route.query.athlete || "",
	team: route.query.team || "",
});
let competitionName = ref("");
let currentPage = ref(1);
const limit = ref(20);

unauthApi.get(`competitions/${props.competition}/get-categories`).then(({ data }) => {
	categories.value = [{ id: "null", name: t("all") }, ...data];
});

let promise =
	store.getters.getUser?.user_role?.role?.name == "ADMIN"
		? authApi.get(`competitions/name/${props.competition}`)
		: unauthApi.get(`competitions/name/${props.competition}`);
promise.then((response) => {
	competitionName.value = response.data;
});
changeParams();

watch(
	() => route.fullPath,
	() => {
		state.value.male = route.query.male ? route.query.male == "true" : true;
		state.value.female = route.query.female ? route.query.female == "true" : true;
		state.value.age = route.query.age || "";
		state.value.category = route.query.category || "null";
		state.value.area = route.query.area || "all";
		state.value.day = route.query.day || "all";
		state.value.time = route.query.time || "null";
		state.value.showZero = route.query.showZero ? route.query.showZero == "true" : true;
		state.value.athlete = route.query.athlete || "";
		state.value.team = route.query.team || "";

		search();
	}
);

function changeParams() {
	let stringReplace = `${route.path}?male=${state.value.male}&female=${state.value.female}&age=${
		state.value.age
	}&category=${state.value.category}&area=${state.value.area}&day=${state.value.day}&time=${
		state.value.time
	}&showZero=${state.value.showZero}&athlete=${state.value.athlete.trim()}&team=${state.value.team
		.trim()
		.toUpperCase()}`;
	if (stringReplace == route.fullPath) {
		search();
		return;
	}
	currentPage.value = 1;
	if (route.fullPath !== route.path) history.pushState({}, null, route.fullPath);
	router.replace(stringReplace);
}

function search() {
	loadingSearch.value = true;
	let searchString = `tournaments?competition_id=${props.competition}`;
	if (state.value.category != "null") searchString += `&category_id=${state.value.category}`;
	if (state.value.male !== state.value.female) searchString += `&is_male=${state.value.male}`;
	if (state.value.age) searchString += `&age=${state.value.age}`;
	if (state.value.area !== "all") {
		searchString += `&area=${state.value.area}`;
		if (state.value.area === "null") searchString += "&area=-1";
		else searchString += `&area=${state.value.area}`;
	}
	if (state.value.day !== "all") searchString += `&day=${state.value.day}`;
	if (state.value.time !== "null") searchString += `&time=${state.value.time}`;
	if (state.value.athlete.trim()) searchString += `&athlete=${state.value.athlete.trim()}`;
	if (state.value.team.trim()) searchString += `&team=${state.value.team.trim()}`;
	if (store.getters.getUser?.user_role?.role?.name == "ADMIN")
		searchString += `&show_zero=${state.value.showZero}`;

	searchString += `&skip=${(currentPage.value - 1) * limit.value}`;

	let promise =
		store.getters.getUser == null ? unauthApi.get(searchString) : authApi.get(searchString);
	promise
		.then((response) => {
			tournaments.value = response.data;
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
	changeParams();
}
</script>
