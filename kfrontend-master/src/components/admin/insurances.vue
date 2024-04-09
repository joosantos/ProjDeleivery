<template>
	<AddAthletesToInsuranceGroup
		:open="openModalAddInsuranceToGroup"
		:ids="insurancesToAddToGroup"
		@close="openModalAddInsuranceToGroup = false"
		@added="
			() => {
				search();
				removeSelection();
			}
		" />
	<TeamSelectModal
		:open="openSelectTeamModal"
		@close="openSelectTeamModal = false"
		@selected="getExcelOfAll" />
	<Loading v-if="loading" :size="10" />
	<div v-else>
		<!-- Search Form -->
		<FormTemplate
			class="z-10 w-"
			:loading="loadingSearch"
			@clear-form="resetForm"
			@submit-form="changeParams">
			<div class="inline-flex space-x-4 w-full">
				<!-- Year -->
				<CustomInput
					class="w-full"
					:label="t('forms.insuranceYear')"
					type="text"
					:name="'year'"
					:mask="'####'"
					:option-selected="year"
					:error="''"
					@value-changed="(option) => (year = option)" />

				<!-- Status -->
				<SearchMultiSelect
					class="w-full"
					:title="t('forms.insuranceStatus')"
					:option-selected="status"
					:options="allStatus"
					:useTranslations="true"
					@selected="
						(option) => {
							status = option;
						}
					" />

				<!-- Name -->
				<CustomInput
					class="w-full"
					:label="t('forms.athleteName')"
					type="text"
					:name="'name'"
					:option-selected="name"
					:error="''"
					@value-changed="(option) => (name = option)" />

				<!-- Insurance Type -->
				<SearchMultiSelect
					class="w-full"
					:title="t('forms.insuranceType')"
					:option-selected="insuranceType"
					:options="insuranceTypes"
					@selected="
						(option) => {
							insuranceType = option;
						}
					" />

				<!-- Team Abbreviation -->
				<CustomInput
					class="w-full"
					:label="t('forms.teamAbbreviation')"
					type="text"
					:name="'teamAbbreviation'"
					:option-selected="teamAbbreviation"
					:error="''"
					@value-changed="(option) => (teamAbbreviation = option)" />

				<!-- Insurance Group -->
				<SearchSelect
					class="w-full"
					:title="t('forms.insuranceGroup')"
					:option-selected="insuranceGroup"
					:options="insuranceGroups"
					:error="''"
					:useTranslations="true"
					@selected="
						(option) => {
							insuranceGroup = option;
						}
					" />

				<!-- Group by -->
				<SearchSelect
					class="w-full"
					:title="t('forms.groupBy')"
					:option-selected="groupBy"
					:options="groupByOptions"
					:error="''"
					:useTranslations="true"
					@selected="
						(option) => {
							groupBy = option;
						}
					" />
			</div>
			<div class="w-full inline-flex gap-x-4">
				<div class="space-x-4 inline-flex">
					<Button
						class="min-w-max max-w-min"
						:message="t('getExcelOfTheSearchedAthletes')"
						:type="'primary'"
						:pill="true"
						:size="'small'"
						:laoding="loadingExcel"
						@button-click="getExcelOfAll" />
					<Button
						class="min-w-max max-w-min"
						:message="t('getExcelOfAllTeams')"
						:type="'primary'"
						:pill="true"
						:size="'small'"
						:laoding="loadingExcelTeams"
						@button-click="getExcelOfTeams" />
					<Button
						class="min-w-max max-w-min ml-auto"
						:message="t('getExcelOfAllInsuredAthletesOfTeam')"
						:type="'success'"
						:pill="true"
						:size="'small'"
						:laoding="loadingExcelTeam"
						@button-click="openSelectTeamModal = true" />
				</div>
				<div v-if="!showGroupped" class="w-full inline-flex">
					<div class="w-full" />
					<div v-if="selectInsurancesToGroup" class="inline-flex gap-x-4">
						<Button
							class="min-w-max max-w-min"
							:message="t('cancel')"
							:type="'danger'"
							:pill="true"
							:size="'small'"
							@button-click="removeSelection" />
						<Button
							class="min-w-max max-w-min"
							:message="t('chooseInsuranceGroup')"
							:type="'success'"
							:pill="true"
							:size="'small'"
							:icon-left="true"
							:icon="PlusIcon"
							@button-click="openModalInsuranceGroup" />
					</div>
					<Button
						v-else
						class="min-w-max max-w-min"
						:message="t('addAthletesToInsuranceGroup')"
						:type="'success'"
						:pill="true"
						:size="'small'"
						@button-click="selectInsurancesToGroup = true" />
				</div>
			</div>
		</FormTemplate>

		<!-- Insurances List -->
		<Loading v-if="loadingSearch || insurancePage == null" :size="10" />
		<div v-else-if="!insurancePage?.results?.length">
			<h1 class="font-bold text-xl py-4">
				{{ t("noInsurances") }}
			</h1>
		</div>
		<div v-else class="mt-2">
			<InsurancesGrouppedList
				v-if="showGroupped"
				:insurances="insurancePage.results || []"
				:groupped-by="groupByView" />

			<div v-else class="space-y-2">
				<button
					v-for="insurance of insurancePage.results || []"
					:key="insurance.id"
					@click="
						selectInsurancesToGroup
							? toogleInsurance(insurance.id)
							: router.push({
									name: 'Insurances Group Details',
									query: {
										insuranceid: insurance.id,
									},
							  })
					"
					:class="[
						'flex flex-col md:grid md:grid-cols-6 border w-full rounded-xl px-4 py-1',
						insurancesToAddToGroup.findIndex((a) => a === insurance.id) === -1
							? 'bg-blue-100 border-blue-300 hover:bg-blue-300'
							: 'bg-blue-300 border-blue-500 hover:bg-blue-500',
					]">
					<div class="md:col-span-3 md:inline-flex">
						<img
							class="w-20 h-20 rounded-full mx-auto md:mx-0 my-auto"
							:src="
								insurance.insured_entity.athlete?.profile_picture_url
									? `https://kempo-files.fra1.digitaloceanspaces.com/${insurance.insured_entity.athlete.profile_picture_url}`
									: '/defaultUserImage.png'
							"
							:alt="`Profile picture for ${insurance.insured_entity.name}`" />
						<div class="md:text-left md:ml-4">
							<h1 class="text-2xl font-semibold">
								{{
									insurance.insured_entity.athlete?.name ||
									insurance.insured_entity.team?.name ||
									"undefined"
								}}
							</h1>
							<div v-if="insurance.insured_entity.athlete_id" class="text-lg">
								<p>
									{{
										t("birthday", {
											date: new Date(
												insurance.insured_entity.athlete.birthday
											).toLocaleDateString("pt-pt"),
										})
									}}
								</p>
								<p>
									{{
										t("nif", {
											nif:
												insurance.insured_entity.athlete.private_info.nif ||
												t("notSet"),
										})
									}}
									{{
										t("cc", {
											cc:
												insurance.insured_entity.athlete.private_info
													.identification_document.number || t("notSet"),
										})
									}}
								</p>
							</div>
							<div v-else>
								<p>{{ t("team") }}</p>
								<p>{{ insurance.insured_entity.team.abbreviation }}</p>
							</div>
						</div>
					</div>
					<h1 class="font-medium text-xl md:text-left my-auto">
						{{ insurance.insurance_type.name }}
					</h1>

					<h1 class="md:col-span-1 text-xl font-medium md:text-left my-auto">
						{{
							insurance.insurance_group?.name
								? `${t("group")} ${insurance.insurance_group.name}`
								: t("noInsuranceGroup")
						}}
					</h1>

					<h1 class="md:col-span-1 text-xl font-medium md:text-left my-auto">
						{{ t(insurance.status) }}
					</h1>
				</button>
			</div>

			<!-- Pagination -->
			<div class="mx-auto mt-4 max-w-max">
				<Pagination
					:pages="Math.ceil(insurancePage.n_results / RESULTS_PER_PAGE)"
					:current="Number(currentPage) + 1"
					@page-change="changeParams" />
			</div>
		</div>
	</div>
</template>

<script setup>
import Button from "@/components/partials/button.vue";
import Loading from "@/components/partials/loading.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import SearchMultiSelect from "@/components/partials/inputs/searchMultiSelect.vue";
import FormTemplate from "@/components/partials/inputs/formTemplate.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Pagination from "@/components/partials/pagination/pagination.vue";
import AddAthletesToInsuranceGroup from "@/components/admin/modals/addAthletesToInsuranceGroup.vue";
import TeamSelectModal from "@/components/admin/modals/teamSelect.vue";
import { PlusIcon } from "@heroicons/vue/24/solid";
import InsurancesGrouppedList from "@/components/admin/partials/insurancesGrouppedList.vue";
import { ref, watch, onMounted } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { useI18n } from "vue-i18n";
import router from "@/router";
import toast from "@/toast.js";
import { useRoute } from "vue-router";

let { t } = useI18n({ useScope: "global" });
const route = useRoute();
const loading = ref(true);
const loadingSearch = ref(true);
const loadingExcelTeams = ref(false);
const RESULTS_PER_PAGE = 12;
const groupByOptions = [
	{ id: "", name: "none" },
	{ id: "payment_comprovatives", name: "paymentComprovatives" },
	{ id: "insurance_groups", name: "insuranceGroups" },
];
const allStatus = [
	{ id: "pending", name: "pending" },
	{ id: "accepted", name: "accepted" },
	{ id: "denied", name: "denied" },
	{ id: "other", name: "other" },
];
const insuranceTypes = ref([]);
const insuranceGroups = ref([
	{ id: "", name: "all" },
	{ id: "without", name: "withoutGroup" },
]);
const initialPromises = [];
const insurancePage = ref(null);
const currentPage = ref(1);
const year = ref(new Date().getFullYear().toString());
const insuranceType = ref([]);
const name = ref("");
const status = ref([]);
const teamAbbreviation = ref("");
const insuranceGroup = ref("");
const groupBy = ref("");
const groupByView = ref("");
const showGroupped = ref(false);
const selectInsurancesToGroup = ref(false);
const insurancesToAddToGroup = ref([]);
const openModalAddInsuranceToGroup = ref(false);
const loadingExcel = ref(false);
const loadingExcelTeam = ref(false);
const openSelectTeamModal = ref(false);

onMounted(async () => {
	initialPromises.push(
		authApi.get("insurance-types").then((response) => {
			insuranceTypes.value.push(...response.data);
		})
	);
	initialPromises.push(
		authApi.get("insurance-groups").then((response) => {
			insuranceGroups.value.push(...response.data);
		})
	);
	try {
		await Promise.all(initialPromises);
		loading.value = false;
		loadingSearch.value = false;
	} catch (e) {
		errorHandling(e);
	}
});

const resetForm = () => {
	year.value = new Date().getFullYear().toString();
	status.value = [];
	name.value = "";
	insuranceType.value = [];
	teamAbbreviation.value = "";
	insuranceGroup.value = "";
	groupBy.value = "";
};

const changeParams = (pageNumber = 1) => {
	if (Number(year.value) < 1900) year.value = "";

	currentPage.value = Number(pageNumber) - 1;
	let newUrlString = `${route.path}?page=${currentPage.value}`;

	if (year.value) newUrlString += `&year=${year.value}`;
	if (name.value) newUrlString += `&name=${name.value}`;
	if (insuranceType.value.length)
		newUrlString += `&insurancetype=${insuranceType.value.join("&insurancetype=")}`;
	if (teamAbbreviation.value) newUrlString += `&teamabbreviation=${teamAbbreviation.value}`;
	if (insuranceGroup.value) newUrlString += `&insurancegroup=${insuranceGroup.value}`;
	if (status.value.length) newUrlString += `&status=${status.value.join("&status=")}`;
	if (groupBy.value) newUrlString += `&groupby=${groupBy.value}`;

	if (newUrlString == route.fullPath) return;
	history.pushState({}, null, route.fullPath);
	router.replace(newUrlString);
};

const search = async () => {
	loadingSearch.value = true;
	let searchString = `insurances/${groupBy.value ? "get-groupped" : ""}?skip=${
		currentPage.value
	}&limit=${RESULTS_PER_PAGE}`;

	if (year.value) searchString += `&year=${year.value}`;
	if (name.value) searchString += `&athlete_name=${name.value}`;
	if (insuranceType.value.length)
		searchString += `&insurance_type=${insuranceType.value.join("&insurance_type=")}`;
	if (teamAbbreviation.value) searchString += `&team_abbreviation=${teamAbbreviation.value}`;
	if (insuranceGroup.value) searchString += `&group=${insuranceGroup.value}`;
	if (status.value.length) searchString += `&status=${status.value.join("&status=")}`;
	if (groupBy.value) searchString += `&group_by=${groupBy.value}`;

	try {
		const { data } = await authApi.get(searchString);
		insurancePage.value = data;
	} catch (error) {
		errorHandling(error);
	} finally {
		loading.value = false;
		loadingSearch.value = false;
	}
};

const toogleInsurance = (id) => {
	const index = insurancesToAddToGroup.value.findIndex((a) => a === id);
	if (index === -1) {
		insurancesToAddToGroup.value.push(id);
	} else {
		insurancesToAddToGroup.value.splice(index, 1);
	}
};

const openModalInsuranceGroup = () => {
	if (!insurancesToAddToGroup.value.length) {
		toast.error(t("error.selectAtLeastOneInsurance"));
		return;
	}
	openModalAddInsuranceToGroup.value = true;
};

const removeSelection = () => {
	insurancesToAddToGroup.value = [];
	selectInsurancesToGroup.value = false;
};

const getExcelOfTeams = async () => {
	loadingExcelTeams.value = true;
	try {
		const { data } = await authApi.get("insurances/get-teams-excel", {
			responseType: "blob",
		});
		const docURL = URL.createObjectURL(data);
		const a = document.createElement("a");
		a.download = "federacoes_equipas.xlsx";
		a.href = docURL;
		a.target = "_self";
		a.click();

		setTimeout(function () {
			// For Firefox it is necessary to delay revoking the ObjectURL
			a.remove();
			URL.revokeObjectURL(docURL);
		}, 100);
	} catch (e) {
		errorHandling(e);
	} finally {
		loadingExcelTeams.value = false;
	}
};

const getExcelOfAll = async (teamId = null, teamName = null) => {
	if (teamId) loadingExcelTeam.value = true;
	else loadingExcel.value = true;
	let url = "";
	if (teamId) url = `insurances/get-excel?year=${year.value}&team_id=${teamId}`;
	else {
		url = `insurances/get-excel?year=${year.value}`;
		if (name.value) url += `&name=${name.value}`;
		if (insuranceType.value.length)
			url += `&insurance_type=${insuranceType.value.join("&insurance_type=")}`;
		if (teamAbbreviation.value) url += `&team_abbreviation=${teamAbbreviation.value}`;
		if (insuranceGroup.value) url += `&group=${insuranceGroup.value}`;
	}

	try {
		const { data } = await authApi.get(url, {
			responseType: "blob",
		});
		let file_name = "federacoes.xlsx";
		if (teamId) {
			if (!teamName) {
				const { data: teamData } = await authApi.get(`teams/${teamId}`);
				file_name = `${teamData.name}_${teamData.abbreviation}_federacoes.xlsx`;
			} else file_name = `${teamName}_federacoes.xlsx`;
		}
		const docURL = URL.createObjectURL(data);
		const a = document.createElement("a");
		a.download = file_name;
		a.href = docURL;
		a.target = "_self";
		a.click();

		setTimeout(function () {
			// For Firefox it is necessary to delay revoking the ObjectURL
			a.remove();
			URL.revokeObjectURL(docURL);
		}, 100);
	} catch (e) {
		errorHandling(e);
	} finally {
		loadingExcel.value = false;
		loadingExcelTeam.value = false;
	}
};

watch(
	() => route.fullPath,
	() => {
		year.value = route.query.year || new Date().getFullYear().toString();
		name.value = route.query.name || "";
		insuranceType.value = [];
		if (route.query.insurancetype) {
			if (typeof route.query.insurancetype === "string")
				insuranceType.value = [route.query.insurancetype];
			else insuranceType.value = route.query.insurancetype;
		}
		teamAbbreviation.value = route.query.teamabbreviation || "";
		insuranceGroup.value = route.query.insurancegroup || "";
		currentPage.value = route.query.page || "0";
		status.value = [];
		if (route.query.status) {
			if (typeof route.query.status === "string") status.value = [route.query.status];
			else status.value = route.query.status;
		}
		groupBy.value = route.query.groupby || "";
		groupByView.value = groupBy.value;
		showGroupped.value = !!groupBy.value;
		search();
	},
	{ immediate: true }
);
</script>
