<script setup>
import CustomInput from "@/components/partials/inputs/customInput.vue";
import { ref, onMounted } from "vue";
import { unauthApi } from "@/services/api";
import { genericError } from "@/toast.js";
import CompetitionButton from "@/components/athletes/partials/competitionButton.vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n({ useScope: "global" });
const state = ref({
	season: new Date().getFullYear().toString(),
});
const competitions = ref([]);
const emit = defineEmits(["updateStatistics"]);

onMounted(() => {
	getCompetitions(state.value.season);
});

const getCompetitions = async (option) => {
	state.value.season = option;
	if (Number(state.value.season) < 2020) {
		return;
	}

	try {
		const { data } = await unauthApi.get(`competitions?year=${state.value.season}`);
		competitions.value = data;
	} catch {
		genericError();
	}
};
</script>

<template>
	<form action="">
		<CustomInput
			:type="'text'"
			:mask="'####'"
			:name="'season'"
			:label="t('season')"
			:option-selected="state.season"
			:error="''"
			@value-changed="getCompetitions" />
	</form>
	<div class="grid grid-cols-4 gap-x-4 gap-y-4 mt-4">
		<CompetitionButton
			v-for="competition of competitions"
			:key="competition.id"
			:name="competition.name"
			:selected="competition.selected || false"
			@click="
				(competition.selected = !competition.selected),
					emit('updateStatistics', competitions)
			" />
	</div>
</template>
