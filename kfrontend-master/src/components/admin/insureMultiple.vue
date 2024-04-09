<template>
	<Loading v-if="loading" :size="10" />
	<div v-else>
		<FormAthlete
			id="insuranceInformationForm"
			:title="t('insureMultiple.form.title')"
			:subtitle="t('insureMultiple.form.subT')"
			:button-save="t('insureMultiple.form.insure')"
			:show-loading="showSpinningWheel"
			:show-x="showX"
			:button-edit="''"
			:can-edit="true"
			@submited="insureAtlhetes"
			@edit="null">
			<!-- Insured Type Input -->
			<div class="col-span-12 md:col-span-4 lg:col-span-3">
				<SearchSelect
					:options="insuredTypes"
					:title="t('insureMultiple.form.insuredType')"
					:option-selected="state.insuredType"
					:error="
						v$.insuredType.$errors.length == 0 ? '' : v$.insuredType.$errors[0].$message
					"
					@selected="(option) => (state.insuredType = option)" />
			</div>
			<!-- Insurance Type Input -->
			<div class="col-span-12 md:col-span-4 lg:col-span-3">
				<SearchSelect
					:options="insuranceTypes"
					:title="t('insureMultiple.form.insuranceType')"
					:option-selected="state.insuranceType"
					:error="
						v$.insuranceType.$errors.length == 0
							? ''
							: v$.insuranceType.$errors[0].$message
					"
					@selected="(option) => (state.insuranceType = option)" />
			</div>
			<!-- Insurance Group Input -->
			<div class="col-span-12 md:col-span-4 lg:col-span-3">
				<SearchSelect
					:options="insuranceGroups"
					:title="t('insureMultiple.form.insuranceGroup')"
					:option-selected="state.insuranceGroup"
					:error="
						v$.insuranceGroup.$errors.length == 0
							? ''
							: v$.insuranceGroup.$errors[0].$message
					"
					@selected="(option) => (state.insuranceGroup = option)" />
			</div>
			<!-- Insurance Start Date Input -->
			<div class="col-span-12 md:col-span-6 lg:col-span-4">
				<DateInput
					:label="t('insureMultiple.form.insuranceStart')"
					:name="'insuranceStart'"
					:option-selected="state.insuranceStart"
					:error="
						v$.insuranceStart.$errors.length == 0
							? ''
							: v$.insuranceStart.$errors[0].$message
					"
					@value-changed="setDateStart" />
			</div>
			<div class="hidden lg:block" />
			<!-- Insurance End Date Input -->
			<div class="col-span-12 md:col-span-6 lg:col-span-4">
				<DateInput
					:label="t('insureMultiple.form.insuranceEnd')"
					:name="'insuranceEnd'"
					:option-selected="state.insuranceEnd"
					:error="
						v$.insuranceEnd.$errors.length == 0
							? ''
							: v$.insuranceEnd.$errors[0].$message
					"
					@value-changed="setDateEnd" />
			</div>

			<div class="col-span-12 sm:col-span-4">
				<ToogleInput
					:name="'federationRequests'"
					:label="t('insureMultiple.form.federationRequests')"
					:option-selected="state.federationRequests"
					:error="''"
					@value-changed="(option) => (state.federationRequests = option)" />
			</div>
			<div class="col-span-12 sm:col-span-4">
				<ToogleInput
					:name="'federationActive'"
					:label="t('insureMultiple.form.federationActive')"
					:option-selected="state.federationActive"
					:error="''"
					@value-changed="(option) => (state.federationActive = option)" />
			</div>

			<div class="col-span-12 sm:col-span-4 sm:col-start-1">
				<CustomInput
					:label="t('insureMultiple.form.federationYear')"
					type="number"
					:name="'federationYear'"
					:option-selected="state.federationYear.toString()"
					:error="''"
					@value-changed="(option) => (state.federationYear = option)" />
			</div>

			<div
				class="col-start-1 md:col-start-1 col-span-12 md:col-span-6"
				@keypress.enter.prevent="searchAthletesByTeam">
				<CustomInput
					:label="t('insureMultiple.form.team')"
					type="text"
					:name="'team'"
					:option-selected="teamSearch"
					:error="teamSearchError"
					@value-changed="(option) => (teamSearch = option.toUpperCase())" />
			</div>
			<div class="col-span-12 md:col-span-6 lg:col-span-3 mt-auto">
				<Button
					:message="t('insureMultiple.form.search')"
					:loading="loadingAthletesTeam"
					type="primary"
					:submit="false"
					@button-click="searchAthletesByTeam" />
			</div>

			<div
				class="col-start-1 md:col-start-1 col-span-12 md:col-span-6"
				@keypress.enter.prevent="searchAthletes">
				<CustomInput
					:label="t('insureMultiple.form.name')"
					type="text"
					:name="'name'"
					:option-selected="nameSearch"
					:error="nameSearchError"
					@value-changed="(option) => (nameSearch = option)" />
			</div>
			<div class="col-span-12 md:col-span-6 lg:col-span-3 mt-auto">
				<Button
					:message="t('insureMultiple.form.search')"
					:loading="loadingAthletes"
					type="primary"
					:submit="false"
					@button-click="searchAthletes" />
			</div>

			<div class="col-span-12 md:col-span-6 lg:col-span-4">
				<p class="text-center font-medium text-xl">
					{{ t("insureMultiple.athletes.search") }}
				</p>
			</div>
			<div class="hidden lg:block col-span-1" />
			<div class="hidden md:block md:col-span-6 lg:col-span-4">
				<p class="text-center font-medium text-xl">
					{{ t("insureMultiple.athletes.insure") }}
				</p>
			</div>
			<div
				class="md:col-start-1 lg:col-start-1 col-span-12 md:col-span-6 lg:col-span-4 bg-gray-100 min-h-[4rem] rounded border border-gray-300 px-2 py-2 max-h-96 overflow-y-auto">
				<div v-for="athlete of athletes" :key="athlete.id" class="flex">
					<button
						v-show="athlete.show"
						class="inline-flex px-2 py-px hover:bg-gray-300 cursor-pointer rounded w-full group"
						@click.prevent="
							() => {
								athlete.show = false;
								athletesToInsure.push(athlete);
							}
						">
						<p>
							{{
								t("fedNum", {
									num: athlete?.private_info?.federation_number
										?.toString()
										.padStart(5, "0"),
								})
							}}
						</p>
						<p class="ml-2">
							{{ athlete.name }}
						</p>
						<p v-if="athlete.team" class="ml-2">
							{{ `(${athlete.team.abbreviation})` }}
						</p>
						<div class="ml-auto mt-1 invisible group-hover:visible">
							<ArrowRightIcon class="w-4 h-4 hidden md:block" />
							<ArrowDownIcon class="w-4 h-4 block md:hidden" />
						</div>
					</button>
				</div>
			</div>
			<div class="hidden lg:block col-span-1" />
			<div class="block md:hidden col-span-12">
				<p class="text-center font-medium text-xl">
					{{ t("insureMultiple.athletes.insure") }}
				</p>
			</div>
			<div
				class="col-span-12 md:col-span-6 lg:col-span-4 bg-gray-100 min-h-[4rem] rounded border border-gray-300 px-2 py-2 max-h-96 overflow-y-auto">
				<div v-for="(athlete, index) of athletesToInsure" :key="athlete.id" class="flex">
					<button
						class="inline-flex px-2 py-px hover:bg-gray-300 cursor-pointer rounded w-full group"
						@click.prevent="
							() => {
								athletes.findIndex((a) => a.id === athlete.id) !== -1
									? (athletes.find((a) => a.id === athlete.id).show = true)
									: null;
								athletesToInsure.splice(index, 1);
							}
						">
						<p>
							{{
								t("fedNum", {
									num: athlete?.private_info?.federation_number
										?.toString()
										.padStart(5, "0"),
								})
							}}
						</p>
						<p class="ml-2">
							{{ athlete.name }}
						</p>
						<p v-if="athlete.team" class="ml-2">
							{{ `(${athlete.team.abbreviation})` }}
						</p>
						<div class="ml-auto mt-1 invisible group-hover:visible">
							<ArrowLeftIcon class="w-4 h-4 hidden md:block" />
							<ArrowUpIcon class="w-4 h-4 block md:hidden" />
						</div>
					</button>
				</div>
			</div>
		</FormAthlete>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import ToogleInput from "@/components/partials/inputs/toogle.vue";
import DateInput from "@/components/partials/inputs/dateInput.vue";
import FormAthlete from "@/components/partials/templates/formAthlete.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Button from "@/components/partials/button.vue";
import { ArrowUpIcon, ArrowRightIcon, ArrowDownIcon, ArrowLeftIcon } from "@heroicons/vue/24/solid";
import { ref, watch } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { useI18n } from "vue-i18n";
import toast from "@/toast.js";
import router from "@/router";
import { required, helpers } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";

let { t } = useI18n({ useScope: "global" });
let loading = ref(true);
let loadingAthletes = ref(false);
let loadingAthletesTeam = ref(false);
let showSpinningWheel = ref(false);
let showX = ref(false);
let insuredTypes = ref([]);
let insuranceTypes = ref([]);
let insuranceGroups = ref([]);
let athletes = ref([]);
let nameSearch = ref("");
let teamSearch = ref("");
let initialPromises = [];
let nameSearchError = ref("");
let teamSearchError = ref("");
let athletesToInsure = ref([]);
const req = helpers.withMessage(t("error.required"), required);
const startDate = helpers.withMessage(
	t("error.startDate"),
	(value) => parseDate(value) < parseDate(state.value.insuranceEnd)
);
const endDate = helpers.withMessage(
	t("error.endDate"),
	(value) => parseDate(value) > parseDate(state.value.insuranceStart)
);
let state = ref({
	insuredType: "",
	insuranceType: "",
	insuranceGroup: "",
	insuranceStart: "",
	insuranceEnd: "",
	federationActive: true,
	federationRequests: false,
	federationYear: new Date().getFullYear(),
});

let rules = {
	insuredType: {
		required: req,
	},
	insuranceType: {
		required: req,
	},
	insuranceGroup: {},
	insuranceStart: {
		required: req,
		startDate: startDate,
	},
	insuranceEnd: {
		required: req,
		endDate: endDate,
	},
};

let v$ = useVuelidate(rules, state, { $scope: "insuranceModal" });

initialPromises.push(
	authApi.get("insured-types").then((response) => {
		insuredTypes.value = response.data;
	})
);
initialPromises.push(
	authApi.get("insurance-types").then((response) => {
		insuranceTypes.value = response.data;
	})
);
initialPromises.push(
	authApi.get("insurance-groups").then((response) => {
		insuranceGroups.value.push({ id: "", name: t("none") });
		insuranceGroups.value.push(...response.data);
	})
);

Promise.all(initialPromises)
	.then(() => {
		loading.value = false;
	})
	.catch((error) => {
		errorHandling(error);
	});

watch(
	() => state.value.insuranceStart,
	() => {
		let aux = state.value.insuranceStart.split("-");
		state.value.insuranceEnd = `${aux[0]}-${aux[1]}-${(Number(aux[2]) + 1).toString()}`;
	}
);

function setDateStart(option) {
	state.value.insuranceStart = option;
	let day = Number(option.split("-")[0]);
	let month = Number(option.split("-")[1]);
	let year = Number(option.split("-")[2]);
	if (day == 29 && month == 2) {
		day = 28;
	}
	state.value.insuranceEnd = `${day}-${month}-${year + 1}`;
}

function setDateEnd(option) {
	state.value.insuranceEnd = option;
	let day = option.split("-")[0];
	let month = option.split("-")[1];
	let year = Number(option.split("-")[2]);
	if (day == 29 && month == 2) {
		day = 28;
	}
	state.value.insuranceStart = `${day}-${month}-${year - 1}`;
}

function searchAthletes() {
	nameSearchError.value = "";
	if (nameSearch.value.trim() == "") {
		nameSearchError.value = t("error.required");
		return;
	}
	loadingAthletes.value = true;
	authApi
		.get(
			`athletes/name/${nameSearch.value.trim()}${
				state.value.federationRequests
					? `?federation_requests_year=${state.value.federationYear}`
					: ""
			}`
		)
		.then((response) => {
			athletes.value = response.data;
			for (let athlete of athletes.value) {
				let index = athletesToInsure.value.findIndex((a) => a.id === athlete.id);
				athlete.show = index === -1;
			}
			loadingAthletes.value = false;
		})
		.catch((error) => {
			errorHandling(error);
			loadingAthletes.value = false;
		});
}

function searchAthletesByTeam() {
	teamSearchError.value = "";
	if (teamSearch.value.trim() == "") {
		teamSearchError.value = t("error.required");
		return;
	}
	loadingAthletesTeam.value = true;
	authApi
		.get(
			`athletes/team/abbreviation/${teamSearch.value.trim()}${
				state.value.federationRequests
					? `?federation_requests_year=${state.value.federationYear}`
					: ""
			}`
		)
		.then((response) => {
			athletes.value = response.data;
			for (let athlete of athletes.value) {
				let index = athletesToInsure.value.findIndex((a) => a.id === athlete.id);
				athlete.show = index === -1;
			}
			loadingAthletesTeam.value = false;
		})
		.catch((error) => {
			loadingAthletesTeam.value = false;
			errorHandling(error);
		});
}

function parseDate(dateString) {
	let aux = dateString.split("-");
	return new Date(aux[2], aux[1] - 1, aux[0]);
}

async function insureAtlhetes() {
	showX.value = false;
	showSpinningWheel.value = true;
	let isFormValid = await v$.value.$validate();
	if (!isFormValid || !athletesToInsure.value.length) {
		showX.value = true;
		showSpinningWheel.value = false;
		if (!athletesToInsure.value.length) toast.error(t("error.noAthlete"));
		return;
	}

	let ids = [];
	for (let athlete of athletesToInsure.value) {
		ids.push(athlete.id);
	}
	let apiData = {
		insured_type_id: state.value.insuredType,
		insurance_type_id: state.value.insuranceType,
		insurance_group_id: state.value.insuranceGroup,
		insurance_start_date: state.value.insuranceStart,
		insurance_end_date: state.value.insuranceEnd,
		insured_entities: ids,
		federation_active: state.value.federationActive,
		federation_year: state.value.federationYear,
	};

	authApi
		.post("insurances/multi", apiData)
		.then(() => {
			toast.success(t("insureMultiple.form.success"));
			showSpinningWheel.value = false;
			setTimeout(() => {
				router.push({ name: "Insurances" });
			}, 1000);
		})
		.catch((error) => {
			errorHandling(error);
			showSpinningWheel.value = false;
			showX.value = true;
		});
}
</script>
