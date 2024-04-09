<template>
	<Modal :open="props.open" :outside-click="true" :show-x="true" @close="emit('close')">
		<ConfirmationModal
			:open="openConfirmationModal && athleteChosen != null"
			:title="t('associateAthlete')"
			:message="t('associateAthleteConfirmation', { name: athleteChosen?.name || '' })"
			:button-text="t('confirm')"
			:is-delete="false"
			@close="openConfirmationModal = false"
			@confirmed="associateAthlete" />
		<h1>{{ t("associateCoachNameToAthlete", { name: props.coachName }) }}</h1>

		<FormTemplate :loading="loading" @clear-form="resetForm" @submit-form="search">
			<div class="inline-flex w-full gap-x-8">
				<CustomInput
					class="w-full"
					:label="t('forms.athleteName')"
					type="text"
					:name="'name'"
					:option-selected="name"
					:error="''"
					@value-changed="(option) => (name = option)" />
				<CustomInput
					class="w-full"
					:label="t('forms.teamAbbreviation')"
					type="text"
					:name="'teamAbbreviation'"
					:option-selected="teamAbbreviation"
					:error="''"
					@value-changed="(option) => (teamAbbreviation = option)" />
			</div>
		</FormTemplate>
		{{ props.coachId }}
		<Loading v-if="loading" :size="10" />
		<div v-else class="grid mt-4 gap-y-1">
			<button
				v-for="athlete of athletesPage.results"
				:key="athlete.id"
				class="bg-blue-200 rounded-lg border border-blue-400 inline-flex justify-between hover:bg-blue-300 px-1 py-0.5"
				@click="
					() => {
						athleteChosen = athlete;
						openConfirmationModal = true;
					}
				">
				<div class="inline-flex gap-x-2">
					<p>
						{{ athlete.name }}
					</p>
					<p>
						{{ `(${athlete.team?.abbreviation || t("noTeam")})` }}
					</p>
				</div>
				<p>
					{{ new Date(athlete.birthday).toLocaleDateString("pt-pt") }}
				</p>
			</button>

			<!-- Pagination -->
			<div class="mx-auto mt-4 max-w-max">
				<Pagination
					:pages="Math.ceil(athletesPage.n_results / RESULTS_PER_PAGE)"
					:current="Number(currentPage) + 1"
					@page-change="changePage" />
			</div>
		</div>
	</Modal>
</template>

<script setup>
import ConfirmationModal from "@/components/partials/messages/confirmation.vue";
import Modal from "@/components/partials/modal.vue";
import Loading from "@/components/partials/loading.vue";
import FormTemplate from "@/components/partials/inputs/formTemplate.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Pagination from "@/components/partials/pagination/pagination.vue";
import { authApi, errorHandling } from "@/services/api";
import { useI18n } from "vue-i18n";
import { ref, watch } from "vue";

let { t } = useI18n({ useScope: "global" });
const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	coachId: {
		type: String,
		required: true,
	},
	coachName: {
		type: String,
		reuqired: true,
	},
});

const RESULTS_PER_PAGE = 20;
const loading = ref(true);
const name = ref(props.coachName);
const teamAbbreviation = ref("");
const currentPage = ref(0);
const athletesPage = ref(null);
const openConfirmationModal = ref(false);
const athleteChosen = ref(null);
const emit = defineEmits(["close", "reload"]);

const changePage = (newPage = 1) => {
	currentPage.value = newPage - 1;
	search();
};

const search = async () => {
	loading.value = true;
	try {
		const { data } = await authApi.get(
			`athletes?name=${name.value}&team_abbreviation=${
				teamAbbreviation.value
			}&limit=${RESULTS_PER_PAGE}&skip=${currentPage.value * RESULTS_PER_PAGE}`
		);
		athletesPage.value = data;
	} catch (e) {
		console.log(e);
		errorHandling(e);
	} finally {
		loading.value = false;
	}
};

const resetForm = () => {
	name.value = props.coachName;
	teamAbbreviation.value = "";
	currentPage.value = 0;
};

const associateAthlete = async () => {
	openConfirmationModal.value = false;
	loading.value = true;
	try {
		const { data } = await authApi.put(`users/${props.coachId}/associate-athlete`, {
			athlete_id: athleteChosen.value.id,
		});
		athleteChosen.value = null;
		emit("reload");
		emit("close");
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
	}
};

watch(
	() => props.open,
	(after) => {
		if (!after) return;
		loading.value = true;
		athletesPage.value = null;
		resetForm();
		search();
	}
);
</script>
