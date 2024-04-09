<template>
	<AssociateAthleteToCoach
		:open="openModal"
		:coach-name="coachToAssociate?.name || ''"
		:coach-id="coachToAssociate?.id || ''"
		@close="
			() => {
				openModal = false;
				coachToAssociate = null;
			}
		"
		@reload="search" />
	<div>
		<h1 class="text-left text-3xl font-semibold">{{ t("coachesList") }}</h1>
		<FormTemplate :loading="loading" @clear-form="resetForm" @submit-form="changeParams">
			<div class="inline-flex max-w-max mx-auto space-x-8">
				<CustomInput
					class="w-full"
					:label="t('forms.name')"
					type="text"
					:name="'name'"
					:option-selected="name"
					:error="''"
					@value-changed="(option) => (name = option)" />

				<SearchSelect
					class="w-full"
					:options="ASSOCIATE_STATUS"
					:title="t('forms.athleteAssociated')"
					:option-selected="coachAssociated"
					:use-translations="true"
					:error="''"
					@selected="(option) => (coachAssociated = option)" />
			</div>
		</FormTemplate>
		<Loading v-if="loading" :size="10" />
		<div v-else class="space-y-2 mt-2 grid">
			<router-link
				v-for="coach of coachesPage.results"
				:key="coach.id"
				class="px-2 py-1 bg-blue-100 cursor-pointer rounded hover:bg-blue-200 border border-blue-300 xl:inline-flex xl:gap-x-4 gap-y-2 xl:gap-y-0 w-full text-center"
				:to="
					coach.athlete_id
						? { name: 'Athlete Details', params: { athleteId: coach.athlete_id } }
						: ''
				">
				<p class="text-xl font-semibold my-auto">
					{{ coach.name }}
				</p>
				<p v-if="coach.athlete" class="my-auto">
					{{ `${coach.athlete.team.name} (${coach.athlete.team.abbreviation})` }}
				</p>
				<p v-if="coach.athlete" class="my-auto">
					{{
						t("federationNumberNumber", {
							number: coach.athlete.private_info.federation_number,
						})
					}}
				</p>
				<p v-if="coach.athlete" class="my-auto">
					{{ t("nif", { nif: coach.athlete.private_info.nif || t("noNif") }) }}
				</p>
				<p v-if="coach.athlete" class="my-auto">
					{{
						t("cc", {
							cc:
								coach.athlete.private_info.identification_document.number ||
								t("noCC"),
						})
					}}
				</p>
				<div class="m-auto xl:mr-0 min-w-max max-w-max">
					<Button
						v-if="!coach.athlete_id"
						:message="t('associateAthleteToCoach')"
						:type="'success'"
						:pill="true"
						:icon-left="true"
						:icon="PlusIcon"
						:size="'small'"
						@click.prevent="
							() => {
								coachToAssociate = coach;
								openModal = true;
							}
						" />
					<Button
						v-else
						:message="t('associateAnotherAthleteToCoach')"
						:type="'warning'"
						:pill="true"
						:icon-left="true"
						:icon="PencilIcon"
						:size="'small'"
						@click.prevent="
							() => {
								coachToAssociate = coach;
								openModal = true;
							}
						" />
				</div>
			</router-link>

			<!-- Pagination -->
			<div class="mx-auto mt-4 max-w-max">
				<Pagination
					:pages="Math.ceil(coachesPage.n_results / RESULTS_PER_PAGE)"
					:current="Number(currentPage) + 1"
					@page-change="changeParams" />
			</div>
		</div>
	</div>
</template>

<script setup>
import Button from "@/components/partials/button.vue";
import FormTemplate from "@/components/partials/inputs/formTemplate.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Loading from "@/components/partials/loading.vue";
import AssociateAthleteToCoach from "@/components/admin/modals/associateAthleteToCoach.vue";
import Pagination from "@/components/partials/pagination/pagination.vue";
import { PlusIcon, PencilIcon } from "@heroicons/vue/24/solid";
import { ref, watch } from "vue";
import { authApi, errorHandling } from "@/services/api";
import router from "@/router";
import { useRoute } from "vue-router";
import { useI18n } from "vue-i18n";

const { t } = useI18n({ useScope: "global" });
const RESULTS_PER_PAGE = 15;
const ASSOCIATE_STATUS = [
	{
		id: "null",
		name: "all",
	},
	{ id: "true", name: "atlheteAssociated" },
	{ id: "false", name: "athleteNotAssociated" },
];
const route = useRoute();
const loading = ref(true);
const coachesPage = ref(null);
const currentPage = ref(0);
const openModal = ref(false);
const coachToAssociate = ref("");
const name = ref("");
const coachAssociated = ref("null");

const search = async () => {
	loading.value = true;
	let url = `users/?is_coach=true&limit=${RESULTS_PER_PAGE}&skip=${
		currentPage.value * RESULTS_PER_PAGE
	}`;
	if (name.value) url += `&name=${name.value}`;
	if (coachAssociated.value != "null") url += `&athlete_associated=${coachAssociated.value}`;

	try {
		const { data } = await authApi.get(url);
		coachesPage.value = data;
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
	}
};

const resetForm = () => {
	name.value = "";
	coachAssociated.value = "null";
};

const changeParams = (pageNumber = 1) => {
	currentPage.value = Number(pageNumber) - 1;
	let newUrlString = `${route.path}?page=${currentPage.value + 1}`;
	if (name.value) newUrlString += `&name=${name.value}`;
	if (coachAssociated.value != "null")
		newUrlString += `&athlete_associated=${coachAssociated.value}`;

	if (newUrlString == route.fullPath) return;
	history.pushState({}, null, route.fullPath);
	router.replace(newUrlString);
};

watch(
	() => route.fullPath,
	() => {
		currentPage.value = Number(route.query.page) - 1 || "0";
		search();
	},
	{ immediate: true }
);
</script>
