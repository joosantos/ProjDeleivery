<template>
	<div>
		<ConfirmationModal
			:open="openConfirmationModal"
			:title="t('removeFromTeam')"
			:message="
				t('DoYouReallyWantToRemoveAthleteFromYourTeam', { name: athleteToDelete?.name })
			"
			:button-text="t('remove')"
			:loading="confirmationLoading"
			:show-x="confirmationShowX"
			@close="openConfirmationModal = false"
			@deleted="deleteAthlete" />
		<InscriptionModal
			:open="openInscriptionsModal"
			:competition-id="selected?.id + ''"
			:competition-start="selected?.competition_start + ''"
			:team-id="props.teamId"
			:competition-calculate-age-start-year="selected?.calculate_age_start_year || false"
			@close="openInscriptionsModal = false" />
		<ShowInscriptionsModal
			:open="showInscriptions"
			:competition-id="selected?.id + ''"
			:competition-name="selected?.name + ''"
			:team-id="props.teamId"
			@close="showInscriptions = false" />
		<Loading v-if="loading" :size="10" />
		<div v-else class="flex flex-col xl:flex-row xl:space-x-8 mx-4 mt-10 h-full">
			<div class="w-full text-center overflow-x-auto xl:overflow-x-hidden">
				<p class="text-center text-3xl font-medium text-blue-900">
					{{ t("athlete.self", 2) }}
				</p>

				<FormTemplate
					class="mt-2 z-10"
					:loading="loadingSearch"
					@clear-form="resetForm"
					@submit-form="changeParams">
					<div class="grid w-full">
						<div class="inline-flex space-x-4 w-full">
							<!-- Is Federated -->
							<SearchSelect
								class="w-full"
								:title="t('forms.athleteIsFederated')"
								:option-selected="form.federated"
								:options="FEDERATED_OPTIONS"
								:error="''"
								:useTranslations="true"
								@selected="
									(option) => {
										form.federated = option;
									}
								" />

							<!-- Federation Number -->
							<CustomInput
								class="w-full"
								:label="t('forms.federationNumber')"
								type="text"
								:name="'federationNumber'"
								:mask="'#####'"
								:option-selected="form.federationNumber"
								:error="''"
								@value-changed="(option) => (form.federationNumber = option)" />

							<!-- Name -->
							<CustomInput
								class="w-full"
								:label="t('forms.athleteName')"
								type="text"
								:name="'name'"
								:option-selected="form.name"
								:error="''"
								@value-changed="(option) => (form.name = option)" />
						</div>
						<div class="inline-flex space-x-4 w-full">
							<!-- Age -->
							<CustomInput
								class="w-full"
								:label="t('forms.athleteAge')"
								type="text"
								:name="'age'"
								:option-selected="form.age"
								:mask="'###'"
								:error="''"
								@value-changed="(option) => (form.age = option)" />

							<!-- Belt -->
							<SearchSelect
								class="w-full"
								:title="t('forms.athleteBelt')"
								:option-selected="form.belt"
								:options="belts"
								:error="''"
								:useTranslations="true"
								@selected="
									(option) => {
										form.belt = option;
									}
								" />

							<!-- Order By -->
							<SearchSelect
								class="w-full"
								:title="t('forms.orderBy')"
								:option-selected="form.orderBy"
								:options="ORDERBY_OPTIONS"
								:error="''"
								:useTranslations="true"
								@selected="
									(option) => {
										form.orderBy = option;
									}
								" />
						</div>
					</div>
				</FormTemplate>
				<div class="inline-flex space-x-4 mt-2 w-full">
					<div class="ml-auto min-w-max">
						<router-link
							:to="{
								name: 'Insurance Requests',
								params: { teamId: props.teamId },
							}">
							<Button
								:message="t('insuranceRequests')"
								type="primary"
								:pill="true"
								:size="'small'"
								:icon-left="true"
								@button-click="null" />
						</router-link>
					</div>
					<div class="min-w-max">
						<router-link
							:to="{
								name:
									store.getters.getUserRole === 'ADMIN'
										? 'Athlete Details'
										: 'Coach Athlete Details',
								params:
									store.getters.getUserRole === 'ADMIN'
										? { athleteId: '0' }
										: { teamId: props.teamId, athleteId: '0' },
							}">
							<Button
								:message="t('addNewAthlete')"
								type="success"
								:icon="PlusIcon"
								:pill="true"
								:size="'small'"
								:icon-left="true"
								@button-click="null" />
						</router-link>
					</div>
				</div>
				<Loading v-if="loadingSearch" :size="10" />
				<div v-else>
					<AthletesTable
						class="mt-2"
						:athletes="athletesPage.results"
						:team-id="props.teamId"
						@remove-athlete="
							(athlete) => {
								athleteToDelete = athlete;
								openConfirmationModal = true;
							}
						" />

					<!-- Pagination -->
					<div class="mx-auto mt-4 max-w-max">
						<Pagination
							:pages="Math.ceil(athletesPage.n_results / RESULTS_PER_PAGE)"
							:current="Number(currentPage)"
							@page-change="changeParams" />
					</div>
				</div>
			</div>
			<div class="hidden xl:flex flex-row items-center">
				<div class="flex flex-1 border border-gray-400 h-full mt-12 rounded-full"></div>
			</div>
			<div v-if="canShowInscriptions" class="w-full mt-4 xl:mt-0 min-h-full relative">
				<div class="sticky top-40">
					<p class="text-center text-3xl font-medium text-blue-900">
						{{ t("openInscriptions") }}
					</p>
					<Loading v-if="loadingInscriptions" :size="10" />
					<RadioGroup v-else v-model="selected" class="mt-12">
						<RadioGroupLabel class="sr-only">
							{{ t("openInscriptions") }}
						</RadioGroupLabel>
						<div class="space-y-4">
							<RadioGroupOption
								v-for="competition in competitions"
								:key="competition.id"
								as="template"
								:value="competition">
								<div>
									<div class="ml-auto max-w-max">
										<Button
											:message="t('showInscriptions')"
											type="primary"
											@button-click="
												selected = competition;
												showInscriptions = true;
											" />
									</div>
									<div
										:class="[
											'relative block rounded-lg border bg-white px-6 py-4 shadow-sm focus:outline-none mt-2',
											(competition.timer ||
												store.getters.getUserRole == 'ADMIN') &&
												'cursor-pointer',
										]"
										@click="
											competition.timer ||
											store.getters.getUserRole == 'ADMIN'
												? (openInscriptionsModal = true)
												: null
										">
										<div
											class="md:inline-flex text-center md:text-left justify-between w-full">
											<div class="font-medium text-gray-900 text-lg">
												{{ competition.name }}
											</div>
											<div
												v-if="competition.timer != null"
												class="text-gray-500">
												{{
													competition.timer
														? `${t("inscriptionsEndIn")} ${
																competition.timer
														  }`
														: t("inscriptionsEnded")
												}}
											</div>
										</div>
										<span
											class="pointer-events-none absolute -inset-px rounded-lg"
											aria-hidden="true" />
									</div>
								</div>
							</RadioGroupOption>
						</div>
					</RadioGroup>
				</div>
			</div>
			<div v-else class="w-full text-center mt-8">
				<h3 class="text-3xl font-semibold">
					{{ t("teamNotInsured") }}
				</h3>
				<p>
					{{
						t(
							"pleaseInsureYourTeamFirstorContactAdministratorsToBeAbleToSignUpAthletesToCompetitions"
						)
					}}
				</p>
			</div>
		</div>
	</div>
</template>

<script setup>
import InscriptionModal from "@/components/coach/modals/inscriptionAthletes.vue";
import ShowInscriptionsModal from "@/components/coach/modals/showInscriptions.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import FormTemplate from "@/components/partials/inputs/formTemplate.vue";
import AthletesTable from "@/components/coach/partials/athletesTable.vue";
import Pagination from "@/components/partials/pagination/pagination.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Button from "@/components/partials/button.vue";
import Loading from "@/components/partials/loading.vue";
import ConfirmationModal from "@/components/partials/messages/confirmation.vue";
import { authApi, errorHandling } from "@/services/api";
import store from "@/store";
import toast from "@/toast.js";
import { RadioGroup, RadioGroupLabel, RadioGroupOption } from "@headlessui/vue";
import { PlusIcon } from "@heroicons/vue/24/solid";
import { ref, onMounted, computed, watch } from "vue";
import router from "@/router";
import { useRoute } from "vue-router";
import { useI18n } from "vue-i18n";

const props = defineProps({
	teamId: {
		type: String,
		required: true,
	},
});

const { t } = useI18n({ useScope: "global" });
const route = useRoute();
const loading = ref(true);
const loadingInscriptions = ref(true);
const competitions = ref([]);
const selected = ref(null);
const openInscriptionsModal = ref(false);
const showInscriptions = ref(false);
const openConfirmationModal = ref(false);
const confirmationLoading = ref(false);
const confirmationShowX = ref(false);

const athleteToDelete = ref(null);
const athletesPage = ref([]);
const currentPage = ref(1);
const loadingSearch = ref(true);
const belts = ref([]);
const RESULTS_PER_PAGE = 20;
const FEDERATED_OPTIONS = ref([
	{
		id: "",
		name: "",
	},
	{
		id: "true",
		name: "federated",
	},
	{
		id: "false",
		name: "notFederated",
	},
]);
const ORDERBY_OPTIONS = ref([
	{ id: "name", name: "name" },
	{ id: "federation_number", name: "federationNumber" },
]);
const form = ref({
	federated: "",
	federationNumber: "",
	name: "",
	age: "",
	belt: "",
	orderBy: "name",
});
const canShowInscriptions = ref(true);
const team = ref(null);

onMounted(async () => {
	getAthletes();

	try {
		const [{ data: beltsApi }, { data: teamApi }] = await Promise.all([
			authApi.get("belts"),
			authApi.get(`teams/${props.teamId}`),
		]);
		belts.value = [
			{ id: "", name: "" },
			{ id: "nobelt", name: "belts.ungraduated" },
			...beltsApi.map((belt) => ({ name: `belts.${belt.name}`, id: belt.id })),
		];
		team.value = teamApi;
		canShowInscriptions.value =
			!!team.value?.federated_in_current_season || store.getters.getUserRole == "ADMIN";
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
	}

	if (canShowInscriptions.value) {
		try {
			const { data: comp } = await authApi.get("competitions?competition_ended=false");
			competitions.value = comp;
			for (let competition of competitions.value) {
				let countDownDate = new Date(competition.inscriptions_end);
				getTimeLeft(competition, countDownDate);
				setInterval(() => {
					getTimeLeft(competition, countDownDate);
				}, 1000);
			}
		} catch (e) {
			errorHandling(e);
		} finally {
			loadingInscriptions.value = false;
		}
	}
});

const getTimeLeft = (competition, countDownDate) => {
	const now = new Date();
	competition.timer = "";
	if (countDownDate.getTime() > now.getTime()) {
		const distance = countDownDate.getTime() - now.getTime();
		const days = Math.floor(distance / (1000 * 60 * 60 * 24));
		const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
		const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
		const seconds = Math.floor((distance % (1000 * 60)) / 1000);

		competition.timer =
			(days == 0 ? "" : days + ` ${t("days")}, `) +
			hours.toString().padStart(2, "0") +
			":" +
			minutes.toString().padStart(2, "0") +
			":" +
			seconds.toString().padStart(2, "0");
	}
};

const resetForm = () => {
	form.value = {
		federated: "",
		federationNumber: "",
		name: "",
		age: "",
		belt: "",
		orderBy: "name",
	};
	currentPage.value = 1;
};

const changeParams = (pageNumber = 1) => {
	currentPage.value = Number(pageNumber);
	let newUrlString = `${route.path}?page=${currentPage.value}`;

	if (form.value.federated) newUrlString += `&federated=${form.value.federated}`;
	if (form.value.federationNumber)
		newUrlString += `&federation_number=${form.value.federationNumber}`;
	if (form.value.name) newUrlString += `&name=${form.value.name}`;
	if (form.value.age) newUrlString += `&age=${form.value.age}`;
	if (form.value.belt) newUrlString += `&belt=${form.value.belt}`;
	if (form.value.orderBy) newUrlString += `&orderBy=${form.value.orderBy}`;

	if (newUrlString == route.fullPath) return;
	history.pushState({}, null, route.fullPath);
	router.replace(newUrlString);
};

const getAthletes = async () => {
	loadingSearch.value = true;
	let url = `athletes?teams=${[props.teamId]}&limit=${RESULTS_PER_PAGE}&skip=${
		(Number(currentPage.value) - 1) * RESULTS_PER_PAGE
	}`;
	if (form.value.federated) url += `&federated=${form.value.federated}`;
	if (form.value.federationNumber) url += `&federation_number=${form.value.federationNumber}`;
	if (form.value.name) url += `&name=${form.value.name}`;
	if (form.value.age) url += `&age=${form.value.age}`;
	if (form.value.belt) url += `&belts=${[form.value.belt]}`;
	if (form.value.orderBy) url += `&order_by=${form.value.orderBy}`;

	try {
		const { data } = await authApi.get(url);
		athletesPage.value = data;
	} catch (e) {
		toast.error(t("athletesApi"));
	} finally {
		loadingSearch.value = false;
	}
};

function deleteAthlete() {
	confirmationShowX.value = false;
	confirmationLoading.value = true;
	try {
		authApi.put(`athletes/remove-from-team/${athleteToDelete.value.id}/${props.teamId}`);
		openConfirmationModal.value = false;
		getAthletes();
	} catch (e) {
		errorHandling(error);
		confirmationShowX.value = true;
	} finally {
		confirmationLoading.value = false;
	}
}

watch(
	() => route.fullPath,
	() => {
		form.value.federated = route.query.federated || "";
		form.value.federationNumber = route.query.federation_number || "";
		form.value.name = route.query.name || "";
		form.value.age = route.query.age || "";
		form.value.belt = route.query.belt || "";
		form.value.orderby = route.query.orderby || "name";
		getAthletes();
	},
	{ immediate: true }
);
</script>
