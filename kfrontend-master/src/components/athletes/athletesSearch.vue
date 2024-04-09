<template>
	<Loading v-if="loading" :size="10" />
	<div v-else>
		<!-- Athlete's form -->
		<FormTemplate :loading="loading" @clear-form="resetForm" @submit-form="changeParams">
			<div class="grid sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-5 gap-x-8 gap-y-2">
				<SearchSelect
					class="w-full"
					:options="GENDER"
					:title="t('forms.athleteGender')"
					:option-selected="form.gender"
					:use-translations="true"
					:error="''"
					@selected="(option) => (form.gender = option)" />
				<CustomInput
					class="w-full"
					:label="t('forms.athleteName')"
					type="text"
					:name="'name'"
					:option-selected="form.name"
					:error="''"
					@value-changed="(option) => (form.name = option)" />
				<CustomInput
					class="w-full"
					:label="t('forms.athleteAgeMin')"
					type="text"
					:mask="'###'"
					:name="'ageMin'"
					:option-selected="form.ageMin"
					:error="''"
					@value-changed="(option) => (form.ageMin = option)" />
				<CustomInput
					class="w-full"
					:label="t('forms.athleteAgeMax')"
					type="text"
					:mask="'###'"
					:name="'ageMax'"
					:option-selected="form.ageMax"
					:error="''"
					@value-changed="(option) => (form.ageMax = option)" />
				<SearchSelect
					class="w-full"
					:options="FEDERATIONS"
					:title="t('forms.athleteIsFederated')"
					:option-selected="form.federated"
					:use-translations="true"
					:error="''"
					@selected="(option) => (form.federated = option)" />
				<SearchMultiSelect
					class="w-full"
					:options="REGIONS"
					:title="t('forms.region')"
					:option-selected="form.regions"
					:use-translations="true"
					@selected="(option) => (form.regions = option)" />
				<SearchMultiSelect
					class="w-full"
					:options="DISTRICTS"
					:title="t('forms.district')"
					:option-selected="form.districts"
					:use-translations="true"
					@selected="(option) => (form.districts = option)" />
				<SearchMultiSelect
					class="w-full"
					:title="t('forms.belt')"
					:option-selected="form.belts"
					:options="belts"
					:use-translations="true"
					@selected="
						(option) => {
							form.belts = option;
						}
					" />
				<SearchSelect
					:options="ADAPTED"
					:title="t('forms.athleteIsAdapted')"
					:option-selected="form.adapted"
					:useTranslations="true"
					:error="''"
					@selected="(option) => (form.adapted = option)" />
				<SearchMultiSelect
					class="w-full"
					:title="t('forms.teams')"
					:option-selected="form.teams"
					:options="teams"
					@selected="
						(option) => {
							form.teams = option;
						}
					" />
			</div>
		</FormTemplate>

		<!-- List and pagination -->
		<Loading v-if="loadingSearch || athletesPage == null" :size="10" />
		<div v-else>
			<!-- List -->
			<p>Showing {{ athletesPage.results.length }} of {{ athletesPage.n_results }}</p>
			<div class="gap-y-1 grid grid-cols-1 2xl:grid-cols-4 lg:grid-cols-2 gap-x-2">
				<router-link
					v-for="athlete of athletesPage.results"
					:key="athlete.id"
					:to="{ name: 'Athlete Page', params: { athleteId: athlete.id } }"
					target="_blank"
					class="rounded-full bg-blue-200 px-2 py-0.5 border border-blue-400 inline-flex justify-between hover:bg-blue-300 hover:border-blue-500">
					<p class="my-auto">{{ athlete.name }}</p>
					<Tooltip :text="t('edit')">
						<router-link
							:to="{
								name: 'Athlete Details',
								params: {
									athleteId: athlete.id,
								},
							}"
							target="_blank">
							<PencilIcon
								class="w-7 h-7 border border-yellow-500 hover:border-yellow-700 text-yellow-500 bg-yellow-200 rounded-full p-1 cursor-pointer hover:bg-yellow-400 hover:text-yellow-700" />
						</router-link>
					</Tooltip>
				</router-link>
			</div>

			<!-- Pagination -->
			<div class="mx-auto mt-4 max-w-max">
				<Pagination
					:pages="Math.ceil(athletesPage.n_results / RESULTS_PER_PAGE)"
					:current="Number(currentPage) + 1"
					@page-change="changeParams" />
			</div>
		</div>
	</div>
</template>

<script setup>
import FormTemplate from "@/components/partials/inputs/formTemplate.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import Pagination from "@/components/partials/pagination/pagination.vue";
import SearchMultiSelect from "@/components/partials/inputs/searchMultiSelect.vue";
import Tooltip from "@/components/partials/templates/tooltip.vue";
import { PencilIcon } from "@heroicons/vue/24/solid";
import Loading from "@/components/partials/loading.vue";
import REGIONS from "@/constants/regions";
import DISTRICTS from "@/constants/districts";
import { authApi, errorHandling } from "@/services/api";
import { ref, watch, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute } from "vue-router";
import router from "@/router";

const { t } = useI18n({ useScope: "global" });
const route = useRoute();

const GENDER = [
	{
		id: "none",
		name: "",
	},
	{
		id: "true",
		name: "masc",
	},
	{
		id: "false",
		name: "fem",
	},
];
const FEDERATIONS = [
	{
		id: "none",
		name: "all",
	},
	{
		id: "true",
		name: "federated",
	},
	{
		id: "false",
		name: "notFederated",
	},
];
const ADAPTED = [
	{
		id: "none",
		name: "",
	},
	{
		id: "true",
		name: "athleteAdapted",
	},
	{
		id: "false",
		name: "athleteNotAdapted",
	},
];
const RESULTS_PER_PAGE = 40;

const loading = ref(true);
const loadingSearch = ref(true);
const athletesPage = ref(null);
const currentPage = ref(1);
const belts = ref([]);
const teams = ref([]);
const form = ref({
	name: "",
	federated: "true",
	ageMin: "",
	ageMax: "",
	gender: "none",
	regions: [],
	districts: [],
	belts: [],
	adapted: "none",
	teams: [],
});

onMounted(async () => {
	try {
		const [{ data: beltsData }, { data: teamsData }] = await Promise.all([
			authApi.get("belts"),
			authApi.get("teams"),
		]);
		belts.value = beltsData.map((belt) => ({ name: `belts.${belt.name}`, id: belt.id }));
		belts.value.splice(0, 0, { id: "nobelt", name: "belts.ungraduated" });
		teams.value = teamsData.map((team) => ({
			name: `${team.name} (${team.abbreviation})`,
			id: team.id,
		}));
		teams.value.splice(0, 0, { id: "noteam", name: t("noTeam") });
	} catch (e) {
		errorHandling(e);
	}
});

const resetForm = () => {
	form.value.name = "";
	form.value.federated = "none";
	form.value.ageMin = "";
	form.value.ageMax = "";
	form.value.gender = "none";
	form.value.regions = [];
	form.value.districts = [];
	form.value.belts = [];
	form.value.teams = [];
};

const changeParams = (pageNumber = 1) => {
	currentPage.value = Number(pageNumber) - 1;
	let newUrlString = `${route.path}?page=${currentPage.value}`;

	if (form.value.name) newUrlString += `&name=${form.value.name}`;
	if (form.value.federated !== "none") newUrlString += `&federated=${form.value.federated}`;
	if (form.value.ageMin) newUrlString += `&age_min=${form.value.ageMin}`;
	if (form.value.ageMax) newUrlString += `&age_max=${form.value.ageMax}`;
	if (form.value.gender !== "none") newUrlString += `&gender=${form.value.gender}`;
	if (form.value.regions.length)
		newUrlString += `&regions=${form.value.regions.join("&regions=")}`;
	if (form.value.districts.length)
		newUrlString += `&districts=${form.value.districts.join("&districts=")}`;
	if (form.value.belts.length) newUrlString += `&belts=${form.value.belts.join("&belts=")}`;
	if (form.value.adapted !== "none") newUrlString += `&adapted=${form.value.adapted}`;
	if (form.value.teams.length) newUrlString += `&teams=${form.value.teams.join("&teams=")}`;

	if (newUrlString == route.fullPath) return;
	history.pushState({}, null, route.fullPath);
	router.replace(newUrlString);
};

const search = async () => {
	loadingSearch.value = true;
	let searchString = `athletes?skip=${
		currentPage.value * RESULTS_PER_PAGE
	}&limit=${RESULTS_PER_PAGE}`;

	if (form.value.name) searchString += `&name=${form.value.name}`;
	if (form.value.federated !== "none") searchString += `&federated=${form.value.federated}`;
	if (form.value.ageMin) searchString += `&age_min=${form.value.ageMin}`;
	if (form.value.ageMax) searchString += `&age_max=${form.value.ageMax}`;
	if (form.value.gender !== "none") searchString += `&is_male=${form.value.gender}`;
	if (form.value.regions.length)
		searchString += `&regions=${form.value.regions.join("&regions=")}`;
	if (form.value.districts.length)
		searchString += `&districts=${form.value.districts.join("&districts=")}`;
	if (form.value.belts.length) searchString += `&belts=${form.value.belts.join("&belts=")}`;
	if (form.value.adapted !== "none") searchString += `&adapted=${form.value.adapted}`;
	if (form.value.teams.length) searchString += `&teams=${form.value.teams.join("&teams=")}`;

	try {
		const { data } = await authApi.get(searchString);
		athletesPage.value = data;
	} catch (error) {
		errorHandling(error);
	} finally {
		loading.value = false;
		loadingSearch.value = false;
	}
};

watch(
	() => route.fullPath,
	() => {
		form.value.name = route.query.name || "";
		form.value.federated = route.query.federated || "true";
		form.value.ageMin = route.query.age_min || "";
		form.value.ageMax = route.query.age_max || "";
		form.value.gender = route.query.gender || "none";
		form.value.adapted = route.query.adapted || "none";
		form.value.regions = [];
		form.value.belts = [];
		form.value.districts = [];
		form.value.teams = [];
		if (route.query.regions) {
			if (typeof route.query.regions === "string") form.value.regions = [route.query.regions];
			else form.value.regions = route.query.regions;
		}
		if (route.query.belts) {
			if (typeof route.query.belts === "string") form.value.belts = [route.query.belts];
			else form.value.belts = route.query.belts;
		}
		if (route.query.districts) {
			if (typeof route.query.districts === "string")
				form.value.districts = [route.query.districts];
			else form.value.districts = route.query.districts;
		}
		if (route.query.teams) {
			if (typeof route.query.teams === "string") form.value.teams = [route.query.teams];
			else form.value.teams = route.query.teams;
		}
		currentPage.value = route.query.page || "0";
		search();
	},
	{ immediate: true }
);
</script>
